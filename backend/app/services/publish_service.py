"""
Publish service - Static site generation and deployment
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.site import Site
from app.models.page import Page
from app.models.site_version import SiteVersion
from app.models.site_settings import SiteSettings
from app.models.nav_menu import NavMenu
from uuid import UUID
from datetime import datetime
import logging
import boto3
import os

logger = logging.getLogger(__name__)

# AWS configuration
S3_SITES_BUCKET = os.getenv("AWS_SITES_BUCKET", "ai-wb-sites-959545103699")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")
CLOUDFRONT_DISTRIBUTION_ID = os.getenv("CLOUDFRONT_DISTRIBUTION_ID", "E23RQWEJSVII7S")
CLOUDFRONT_DOMAIN = os.getenv("CLOUDFRONT_DOMAIN", "d2raj73d783uqn.cloudfront.net")

s3_client = boto3.client('s3', region_name=S3_REGION)
cloudfront_client = boto3.client('cloudfront', region_name=S3_REGION)


class PublishService:
    """Service for publishing sites to S3 + CloudFront"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def publish_site(self, site_id: UUID, user_id: UUID, notes: str | None = None) -> SiteVersion:
        """
        Generate static HTML from GrapesJS data and publish to S3.

        Steps:
        1. Fetch all pages for the site
        2. Fetch site settings and nav menus
        3. Render each page's HTML with injected elements
        4. Generate sitemap.xml and robots.txt
        5. Upload all files to S3
        6. Create CloudFront invalidation
        7. Create SiteVersion record
        8. Update Site.current_version_id

        Args:
            site_id: Site to publish
            user_id: User performing the publish
            notes: Optional publish notes

        Returns:
            Created SiteVersion
        """
        # Get site
        site_result = await self.db.execute(
            select(Site).where(Site.id == site_id)
        )
        site = site_result.scalar_one_or_none()

        if not site:
            raise ValueError("Site not found")

        # Get all active pages
        pages_result = await self.db.execute(
            select(Page).where(
                Page.site_id == site_id,
                Page.status == "active"
            ).order_by(Page.sort_order, Page.created_at)
        )
        pages = pages_result.scalars().all()

        if not pages:
            raise ValueError("Site has no pages to publish")

        # Get site settings
        settings_result = await self.db.execute(
            select(SiteSettings).where(SiteSettings.site_id == site_id)
        )
        settings = settings_result.scalar_one_or_none()

        # Get nav menus
        menus_result = await self.db.execute(
            select(NavMenu).where(NavMenu.site_id == site_id)
        )
        menus = menus_result.scalars().all()

        # Build navigation HTML
        nav_html = self._build_navigation(pages, menus)

        # Build footer HTML
        footer_html = self._build_footer(settings)

        # Get next version number
        last_version_result = await self.db.execute(
            select(SiteVersion).where(
                SiteVersion.site_id == site_id
            ).order_by(SiteVersion.version_number.desc()).limit(1)
        )
        last_version = last_version_result.scalar_one_or_none()
        version_number = (last_version.version_number + 1) if last_version else 1

        # S3 prefix for this version
        s3_prefix = f"{site.tenant_id}/{site_id}/v{version_number}/"

        # Generate and upload pages
        uploaded_files = []

        for page in pages:
            # Build complete HTML
            html_content = self._render_page(
                page=page,
                nav_html=nav_html,
                footer_html=footer_html,
                settings=settings
            )

            # Determine file path
            if page.is_homepage or page.slug == "home":
                file_key = f"{s3_prefix}index.html"
            else:
                file_key = f"{s3_prefix}{page.slug}/index.html"

            # Upload to S3
            s3_client.put_object(
                Bucket=S3_SITES_BUCKET,
                Key=file_key,
                Body=html_content.encode('utf-8'),
                ContentType='text/html',
                CacheControl='max-age=300'
            )

            uploaded_files.append(file_key)
            logger.info(f"Uploaded page: {file_key}")

        # Generate and upload sitemap.xml
        sitemap_content = self._generate_sitemap(site, pages)
        sitemap_key = f"{s3_prefix}sitemap.xml"
        s3_client.put_object(
            Bucket=S3_SITES_BUCKET,
            Key=sitemap_key,
            Body=sitemap_content.encode('utf-8'),
            ContentType='application/xml'
        )
        uploaded_files.append(sitemap_key)

        # Generate and upload robots.txt
        robots_content = self._generate_robots(site, s3_prefix)
        robots_key = f"{s3_prefix}robots.txt"
        s3_client.put_object(
            Bucket=S3_SITES_BUCKET,
            Key=robots_key,
            Body=robots_content.encode('utf-8'),
            ContentType='text/plain'
        )
        uploaded_files.append(robots_key)

        # Create snapshot of current state
        snapshot = {
            "pages": [
                {
                    "id": str(page.id),
                    "slug": page.slug,
                    "title": page.title,
                    "is_homepage": page.is_homepage
                }
                for page in pages
            ],
            "settings": settings.__dict__ if settings else {},
            "menus": [
                {
                    "position": menu.position,
                    "items": menu.items
                }
                for menu in menus
            ]
        }

        # Create version record
        version = SiteVersion(
            site_id=site_id,
            version_number=version_number,
            snapshot=snapshot,
            s3_prefix=s3_prefix,
            published_by=user_id,
            published_at=datetime.utcnow(),
            is_current=True,
            notes=notes
        )

        # Mark previous versions as not current
        previous_versions_result = await self.db.execute(
            select(SiteVersion).where(
                SiteVersion.site_id == site_id,
                SiteVersion.is_current == True
            )
        )
        previous_versions = previous_versions_result.scalars().all()

        for prev_version in previous_versions:
            prev_version.is_current = False

        self.db.add(version)
        await self.db.flush()

        # Update site
        site.current_version_id = version.id
        site.status = "published"
        site.published_at = datetime.utcnow()
        site.publish_url = f"https://{CLOUDFRONT_DOMAIN}/{site.tenant_id}/{site_id}/v{version_number}/"

        await self.db.commit()
        await self.db.refresh(version)

        # Invalidate CloudFront cache
        try:
            cloudfront_client.create_invalidation(
                DistributionId=CLOUDFRONT_DISTRIBUTION_ID,
                InvalidationBatch={
                    'Paths': {
                        'Quantity': 1,
                        'Items': [f"/{site.tenant_id}/{site_id}/*"]
                    },
                    'CallerReference': f"{site_id}-{version_number}-{int(datetime.utcnow().timestamp())}"
                }
            )
            logger.info(f"CloudFront invalidation created for site {site_id}")
        except Exception as e:
            logger.error(f"Failed to create CloudFront invalidation: {str(e)}")
            # Don't fail the publish if invalidation fails

        logger.info(f"Site published: {site_id} version {version_number}")
        return version

    async def rollback_to_version(self, site_id: UUID, version_id: UUID) -> bool:
        """Rollback site to a previous version"""
        # Get version
        version_result = await self.db.execute(
            select(SiteVersion).where(
                SiteVersion.id == version_id,
                SiteVersion.site_id == site_id
            )
        )
        version = version_result.scalar_one_or_none()

        if not version:
            raise ValueError("Version not found")

        # Get site
        site_result = await self.db.execute(
            select(Site).where(Site.id == site_id)
        )
        site = site_result.scalar_one_or_none()

        if not site:
            raise ValueError("Site not found")

        # Mark all versions as not current
        all_versions_result = await self.db.execute(
            select(SiteVersion).where(SiteVersion.site_id == site_id)
        )
        all_versions = all_versions_result.scalars().all()

        for v in all_versions:
            v.is_current = False

        # Mark this version as current
        version.is_current = True

        # Update site
        site.current_version_id = version_id
        site.publish_url = f"https://{CLOUDFRONT_DOMAIN}/{version.s3_prefix}"

        await self.db.commit()

        # Invalidate CloudFront cache
        try:
            cloudfront_client.create_invalidation(
                DistributionId=CLOUDFRONT_DISTRIBUTION_ID,
                InvalidationBatch={
                    'Paths': {
                        'Quantity': 1,
                        'Items': [f"/{site.tenant_id}/{site_id}/*"]
                    },
                    'CallerReference': f"{site_id}-rollback-{int(datetime.utcnow().timestamp())}"
                }
            )
        except Exception as e:
            logger.error(f"Failed to create CloudFront invalidation: {str(e)}")

        logger.info(f"Site rolled back: {site_id} to version {version.version_number}")
        return True

    async def get_version_history(self, site_id: UUID) -> list[SiteVersion]:
        """Get all published versions of a site"""
        result = await self.db.execute(
            select(SiteVersion).where(
                SiteVersion.site_id == site_id
            ).order_by(SiteVersion.version_number.desc())
        )
        return result.scalars().all()

    def _build_navigation(self, pages: list[Page], menus: list[NavMenu]) -> str:
        """Build navigation HTML from pages and menus"""
        # Find header menu
        header_menu = next((m for m in menus if m.position == "header"), None)

        if header_menu and header_menu.items:
            # Use custom menu
            nav_items = []
            for item in header_menu.items:
                label = item.get('label', '')
                url = item.get('url', '#')
                target = item.get('target', '_self')
                nav_items.append(f'<a href="{url}" target="{target}" class="text-gray-700 hover:text-blue-600 px-3 py-2">{label}</a>')

            nav_html = '\n'.join(nav_items)
        else:
            # Auto-generate from pages
            nav_items = []
            for page in pages:
                if page.status == "active":
                    url = "/" if page.is_homepage else f"/{page.slug}/"
                    nav_items.append(f'<a href="{url}" class="text-gray-700 hover:text-blue-600 px-3 py-2">{page.title}</a>')

            nav_html = '\n'.join(nav_items)

        return f'''
<nav class="bg-white shadow-sm">
  <div class="container mx-auto px-4 py-4 flex justify-between items-center">
    <div class="text-2xl font-bold text-blue-600">Logo</div>
    <div class="flex space-x-4">
      {nav_html}
    </div>
  </div>
</nav>
'''

    def _build_footer(self, settings: SiteSettings | None) -> str:
        """Build footer HTML from settings"""
        company_name = settings.company_name if settings else "My Company"
        year = datetime.utcnow().year

        social_links_html = ""
        if settings and settings.social_links:
            social_items = []
            for platform, url in settings.social_links.items():
                if url:
                    social_items.append(f'<a href="{url}" class="text-gray-400 hover:text-gray-300">{platform.title()}</a>')
            if social_items:
                social_links_html = '<div class="flex space-x-4 mt-4">' + ' '.join(social_items) + '</div>'

        return f'''
<footer class="bg-gray-800 text-white py-8 mt-12">
  <div class="container mx-auto px-4 text-center">
    <p class="text-gray-400">&copy; {year} {company_name}. All rights reserved.</p>
    {social_links_html}
  </div>
</footer>
'''

    def _render_page(
        self,
        page: Page,
        nav_html: str,
        footer_html: str,
        settings: SiteSettings | None
    ) -> str:
        """Render complete page HTML with injected elements"""
        # Extract SEO meta
        seo_title = page.seo_meta.get('title') if page.seo_meta else page.title
        seo_description = page.seo_meta.get('description', '') if page.seo_meta else ''
        seo_keywords = page.seo_meta.get('keywords', '') if page.seo_meta else ''

        # Custom head code
        custom_head = settings.custom_head_code if settings else ""

        # Custom body code
        custom_body = settings.custom_body_code if settings else ""

        # Analytics code
        analytics_code = ""
        if settings and settings.analytics_id:
            analytics_code = f'''
<!-- Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={settings.analytics_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{settings.analytics_id}');
</script>
'''

        # Build complete HTML
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{seo_title}</title>
  <meta name="description" content="{seo_description}">
  <meta name="keywords" content="{seo_keywords}">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    {page.css or ''}
  </style>
  {analytics_code}
  {custom_head}
</head>
<body>
  {nav_html}
  <main>
    {page.html}
  </main>
  {footer_html}
  {custom_body}
</body>
</html>
'''

    def _generate_sitemap(self, site: Site, pages: list[Page]) -> str:
        """Generate sitemap.xml"""
        base_url = site.publish_url or f"https://{CLOUDFRONT_DOMAIN}/{site.tenant_id}/{site.id}/"

        urls = []
        for page in pages:
            if page.status == "active":
                if page.is_homepage:
                    loc = base_url
                else:
                    loc = f"{base_url}{page.slug}/"

                urls.append(f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{page.updated_at.strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>''')

        urls_xml = '\n'.join(urls)

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_xml}
</urlset>
'''

    def _generate_robots(self, site: Site, s3_prefix: str) -> str:
        """Generate robots.txt"""
        base_url = site.publish_url or f"https://{CLOUDFRONT_DOMAIN}/{s3_prefix}"

        return f'''User-agent: *
Allow: /

Sitemap: {base_url}sitemap.xml
'''
