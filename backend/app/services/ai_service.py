"""
AI service - Bedrock integration for website generation
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ai_session import AISession
from app.models.site import Site
from app.models.page import Page
from uuid import UUID, uuid4
from typing import AsyncGenerator
from datetime import datetime
import logging
import json
import boto3
import os
import io
# Document processing
import PyPDF2
from docx import Document as DocxDocument
logger = logging.getLogger(__name__)
# Bedrock configuration
MODEL_ID = "us.anthropic.claude-sonnet-4-6"  # Cross-Region inference profile
S3_BUCKET = os.getenv("AWS_ASSETS_BUCKET", "ai-wb-assets-959545103699")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")
bedrock_runtime = boto3.client('bedrock-runtime', region_name=S3_REGION)
s3_client = boto3.client('s3', region_name=S3_REGION)
SYSTEM_PROMPT = """You are an expert web designer specializing in creating professional, modern websites for businesses.
Your role is to:
1. Ask clarifying questions to understand the client's business, goals, and aesthetic preferences
2. Collect information about: company name, industry, target audience, brand colors, desired pages, style preferences
3. Generate complete, professional HTML/CSS code for websites that are:
   - Modern and visually appealing
   - Responsive (mobile-first design)
   - Built with Tailwind CSS classes
   - Semantic HTML5
   - Accessible (WCAG compliant)
   - SEO-friendly
When generating websites:
- Use https://placehold.co/ for placeholder images (e.g., https://placehold.co/1200x600)
- Include proper meta tags and semantic structure
- Use Tailwind CSS utility classes throughout
- Create clear, professional copy based on the company info provided
- Include a navigation header and footer on all pages
- Make pages visually balanced with appropriate whitespace
Output format for site generation must be valid JSON with this structure:
{
  "config": {
    "company_name": "...",
    "industry": "...",
    "colors": {"primary": "...", "secondary": "..."},
    "style": "..."
  },
  "pages": [
    {
      "slug": "home",
      "title": "Home",
      "html": "<!DOCTYPE html>...",
      "css": "/* Custom CSS */",
      "seo_meta": {
        "title": "...",
        "description": "...",
        "keywords": "..."
      }
    }
  ]
}
Be conversational and helpful when gathering requirements, but output structured JSON when generating the site."""
class AIService:
    """Service for AI-powered website generation using Bedrock"""
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_session(
        self,
        tenant_id: UUID,
        site_id: UUID | None = None,
        company_info: str | None = None
    ) -> AISession:
        """Create a new AI generation session"""
        session = AISession(
            tenant_id=tenant_id,
            site_id=site_id,
            company_info=company_info,
            conversation={"messages": []},
            status="in_progress",
            model_id=MODEL_ID
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        logger.info(f"AI session created: {session.id}")
        return session
    async def upload_document(
        self,
        session_id: UUID,
        filename: str,
        content: bytes,
        content_type: str
    ) -> str:
        """
        Upload and extract text from company document.
        Supports PDF, DOCX, and TXT files.
        """
        # Get session
        result = await self.db.execute(
            select(AISession).where(AISession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise ValueError("Session not found")
        # Extract text based on file type
        extracted_text = ""
        if content_type == "application/pdf":
            # Extract from PDF
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                extracted_text += page.extract_text() + "\n"
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Extract from DOCX
            docx_file = io.BytesIO(content)
            doc = DocxDocument(docx_file)
            for paragraph in doc.paragraphs:
                extracted_text += paragraph.text + "\n"
        elif content_type == "text/plain":
            # Plain text
            extracted_text = content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported file type: {content_type}")
        # Upload to S3
        s3_key = f"ai-sessions/{session.tenant_id}/{session_id}/{filename}"
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=content,
            ContentType=content_type
        )
        # Update session
        session.company_info = extracted_text
        session.company_info_s3_key = s3_key
        await self.db.commit()
        logger.info(f"Document uploaded and processed for session {session_id}")
        return extracted_text
    async def send_message_streaming(
        self,
        session_id: UUID,
        message: str
    ) -> AsyncGenerator[dict, None]:
        """
        Send a message to AI and stream the response.
        Uses Bedrock Converse API with streaming.
        """
        # Get session
        result = await self.db.execute(
            select(AISession).where(AISession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise ValueError("Session not found")
        # Initialize conversation if needed
        if not session.conversation or "messages" not in session.conversation:
            session.conversation = {"messages": []}
        # Add user message
        session.conversation["messages"].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.utcnow().isoformat()
        })
        # Build messages for Bedrock Converse API
        messages = []
        for msg in session.conversation["messages"]:
            messages.append({
                "role": msg["role"],
                "content": [{"text": msg["content"]}]
            })
        # Add company info context if available
        system_messages = [{"text": SYSTEM_PROMPT}]
        if session.company_info:
            system_messages.append({
                "text": f"\nCompany Information:\n{session.company_info[:2000]}"  # Limit context
            })
        # Call Bedrock with streaming
        try:
            response = bedrock_runtime.converse_stream(
                modelId=MODEL_ID,
                messages=messages,
                system=system_messages,
                inferenceConfig={
                    "maxTokens": 4096,
                    "temperature": 0.7,
                    
                }
            )
            # Stream response
            assistant_message = ""
            stream = response.get('stream')
            if stream:
                for event in stream:
                    if 'contentBlockDelta' in event:
                        delta = event['contentBlockDelta']['delta']
                        if 'text' in delta:
                            chunk_text = delta['text']
                            assistant_message += chunk_text
                            # Yield chunk
                            yield {
                                "type": "content",
                                "text": chunk_text
                            }
                    elif 'messageStop' in event:
                        # Message complete
                        break
                    elif 'metadata' in event:
                        metadata = event['metadata']
                        if 'usage' in metadata:
                            session.input_tokens = metadata['usage'].get('inputTokens', 0)
                            session.output_tokens = metadata['usage'].get('outputTokens', 0)
            # Add assistant message to conversation
            session.conversation["messages"].append({
                "role": "assistant",
                "content": assistant_message,
                "timestamp": datetime.utcnow().isoformat()
            })
            await self.db.commit()
            logger.info(f"AI message processed for session {session_id}")
        except Exception as e:
            logger.error(f"Bedrock API error: {str(e)}")
            raise
    async def generate_site(
        self,
        session_id: UUID,
        regenerate: bool = False
    ) -> Site:
        """
        Generate complete website from AI session data.
        Uses Bedrock Claude to generate HTML/CSS for all pages.
        """
        start_time = datetime.utcnow()
        # Get session
        result = await self.db.execute(
            select(AISession).where(AISession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise ValueError("Session not found")
        # Build generation prompt
        conversation_summary = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in session.conversation.get("messages", [])[-10:]  # Last 10 messages
        ])
        generation_prompt = f"""Based on our conversation, please generate a complete professional website.
Conversation summary:
{conversation_summary}
Company information:
{session.company_info[:2000] if session.company_info else "Not provided"}
Generate a complete website with:
1. Homepage (slug: "home")
2. About Us page (slug: "about")
3. Contact page (slug: "contact")
4. Any other pages discussed (e.g., services, products, portfolio)
Output ONLY valid JSON in the exact format specified. Do not include any explanatory text outside the JSON.
Use Tailwind CSS classes, include responsive design, and use placeholder images from https://placehold.co/."""
        # Call Bedrock for generation
        try:
            response = bedrock_runtime.converse(
                modelId=MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": generation_prompt}]
                    }
                ],
                system=[{"text": SYSTEM_PROMPT}],
                inferenceConfig={
                    "maxTokens": 64000,  # Large output for full site
                    "temperature": 0.5,  # Lower temperature for more consistent output
                    
                }
            )
            # Extract generated content
            output_text = response['output']['message']['content'][0]['text']
            # Parse JSON output
            # Try to extract JSON from code blocks if present
            if "```json" in output_text:
                json_start = output_text.find("```json") + 7
                json_end = output_text.find("```", json_start)
                output_text = output_text[json_start:json_end].strip()
            elif "```" in output_text:
                json_start = output_text.find("```") + 3
                json_end = output_text.find("```", json_start)
                output_text = output_text[json_start:json_end].strip()
            site_data = json.loads(output_text)
            # Update token usage
            usage = response.get('usage', {})
            session.input_tokens = (session.input_tokens or 0) + usage.get('inputTokens', 0)
            session.output_tokens = (session.output_tokens or 0) + usage.get('outputTokens', 0)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI output as JSON: {str(e)}")
            logger.error(f"Output was: {output_text[:500]}")
            raise ValueError(f"AI generated invalid JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Site generation error: {str(e)}")
            raise
        # Create or update site
        if session.site_id:
            site_result = await self.db.execute(
                select(Site).where(Site.id == session.site_id)
            )
            site = site_result.scalar_one_or_none()
        else:
            site = None
        if not site:
            # Create new site
            company_name = site_data.get("config", {}).get("company_name", "My Website")
            site = Site(
                tenant_id=session.tenant_id,
                name=company_name,
                status="draft",
                settings_snapshot=site_data.get("config")
            )
            self.db.add(site)
            await self.db.flush()
            session.site_id = site.id
        # Store generated config
        session.generated_config = site_data.get("config")
        session.generated_pages = site_data.get("pages")
        session.status = "completed"
        session.generation_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        # Create pages
        for idx, page_data in enumerate(site_data.get("pages", [])):
            # Check if page already exists
            page_result = await self.db.execute(
                select(Page).where(
                    Page.site_id == site.id,
                    Page.slug == page_data.get("slug", f"page-{idx}")
                )
            )
            existing_page = page_result.scalar_one_or_none()
            if existing_page and not regenerate:
                # Skip if not regenerating
                continue
            # Create or update page
            page = existing_page if existing_page else Page(
                site_id=site.id,
                slug=page_data.get("slug", f"page-{idx}"),
                is_homepage=(page_data.get("slug") == "home")
            )
            page.title = page_data.get("title", "Untitled")
            page.html = page_data.get("html", "")
            page.css = page_data.get("css", "")
            page.seo_meta = page_data.get("seo_meta", {})
            page.status = "active"
            # Build GrapesJS-compatible data structure
            # This is a simplified version - in production, you'd parse the HTML properly
            page.grapesjs_data = {
                "html": page.html,
                "css": page.css,
                "components": [],  # Would need proper parsing
                "style": []
            }
            if not existing_page:
                self.db.add(page)
        await self.db.commit()
        await self.db.refresh(site)
        logger.info(f"Site generated: {site.id} from session {session_id}")
        return site
    async def regenerate_page(
        self,
        session_id: UUID,
        page_slug: str,
        feedback: str
    ) -> dict:
        """Regenerate a specific page based on feedback"""
        # Get session
        result = await self.db.execute(
            select(AISession).where(AISession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session or not session.site_id:
            raise ValueError("Session or site not found")
        # Get page
        page_result = await self.db.execute(
            select(Page).where(
                Page.site_id == session.site_id,
                Page.slug == page_slug
            )
        )
        page = page_result.scalar_one_or_none()
        if not page:
            raise ValueError("Page not found")
        # Build regeneration prompt
        regeneration_prompt = f"""Please regenerate the "{page.title}" page based on this feedback:
Feedback: {feedback}
Current page content:
{page.html[:1000]}
Generate an improved version following the same JSON format as before, but only for this single page.
Output valid JSON with the structure: {{"slug": "...", "title": "...", "html": "...", "css": "...", "seo_meta": {{}}}}"""
        # Call Bedrock
        try:
            response = bedrock_runtime.converse(
                modelId=MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": regeneration_prompt}]
                    }
                ],
                system=[{"text": SYSTEM_PROMPT}],
                inferenceConfig={
                    "maxTokens": 16000,
                    "temperature": 0.6,
                    
                }
            )
            output_text = response['output']['message']['content'][0]['text']
            # Parse JSON
            if "```json" in output_text:
                json_start = output_text.find("```json") + 7
                json_end = output_text.find("```", json_start)
                output_text = output_text[json_start:json_end].strip()
            page_data = json.loads(output_text)
            # Update page
            page.html = page_data.get("html", page.html)
            page.css = page_data.get("css", page.css)
            page.seo_meta = page_data.get("seo_meta", page.seo_meta)
            await self.db.commit()
            logger.info(f"Page regenerated: {page.id} in session {session_id}")
            return {
                "success": True,
                "page_id": page.id,
                "slug": page.slug
            }
        except Exception as e:
            logger.error(f"Page regeneration error: {str(e)}")
            raise
