"""
Application configuration
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AI Website Builder"
    VERSION: str = "0.1.0"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "postgresql://admin:password@localhost:5432/ai_website_builder"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AWS Settings
    AWS_REGION: str = "us-east-1"
    AWS_ACCOUNT_ID: str = "959545103699"

    # S3 Buckets
    S3_SITES_BUCKET: str = "ai-wb-sites-959545103699"
    S3_ASSETS_BUCKET: str = "ai-wb-assets-959545103699"
    S3_TEMPLATES_BUCKET: str = "ai-wb-templates-959545103699"

    # Bedrock
    BEDROCK_MODEL_ID: str = "us.anthropic.claude-sonnet-4-6"
    BEDROCK_REGION: str = "us-east-1"

    # Cognito
    COGNITO_USER_POOL_ID: str = ""
    COGNITO_CLIENT_ID: str = ""
    COGNITO_REGION: str = "us-east-1"

    # DynamoDB Tables
    DYNAMODB_PAGE_VIEWS_TABLE: str = "ai-wb-page-views"
    DYNAMODB_PAGE_VIEW_DAILY_TABLE: str = "ai-wb-page-view-daily"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
