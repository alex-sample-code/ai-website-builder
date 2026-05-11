"""
Application configuration
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AI Website Builder"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://www.chinabjalex.com",
        "https://api.chinabjalex.com"
    ]

    # Database - async PostgreSQL
    DATABASE_URL: str = "postgresql+asyncpg://admin:password@localhost:5432/ai_website_builder"
    DB_ECHO: bool = False  # Set to True for SQL query logging
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 50

    # AWS Settings
    AWS_REGION: str = "us-east-1"
    AWS_ACCOUNT_ID: str = "959545103699"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_ENDPOINT_URL: Optional[str] = None  # For LocalStack in development

    # S3 Buckets
    S3_SITES_BUCKET: str = "ai-wb-sites-959545103699"
    S3_ASSETS_BUCKET: str = "ai-wb-assets-959545103699"
    S3_TEMPLATES_BUCKET: str = "ai-wb-templates-959545103699"

    # CloudFront
    CLOUDFRONT_DISTRIBUTION_ID: str = "E23RQWEJSVII7S"
    CLOUDFRONT_DOMAIN: str = "d2raj73d783uqn.cloudfront.net"

    # Bedrock AI
    BEDROCK_MODEL_ID: str = "us.anthropic.claude-sonnet-4-6"
    BEDROCK_REGION: str = "us-east-1"
    BEDROCK_MAX_TOKENS: int = 64000
    BEDROCK_TEMPERATURE: float = 1.0

    # Cognito
    COGNITO_USER_POOL_ID: str = "us-east-1_UkKMQIN1R"
    COGNITO_CLIENT_ID: str = "7kji0ar3m8g81pjr0fnkrpsirb"
    COGNITO_REGION: str = "us-east-1"
    COGNITO_JWKS_URL: Optional[str] = None  # Auto-generated from pool ID

    # DynamoDB Tables
    DYNAMODB_PAGE_VIEWS_TABLE: str = "ai-wb-page-views"
    DYNAMODB_PAGE_VIEW_DAILY_TABLE: str = "ai-wb-page-view-daily"

    # JWT Settings
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Email (SES)
    SES_SENDER_EMAIL: str = "noreply@chinabjalex.com"
    SES_REGION: str = "us-east-1"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PUBLIC_FORM_SUBMIT: int = 10

    # AI Quotas (default)
    DEFAULT_AI_QUOTA_FREE: int = 3
    DEFAULT_AI_QUOTA_PRO: int = 50
    DEFAULT_AI_QUOTA_ENTERPRISE: int = -1  # Unlimited

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    ALLOWED_DOCUMENT_TYPES: List[str] = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ]

    # Celery (for background tasks)
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or console

    # Security
    SECRET_KEY: str = "change-this-to-a-random-secret-key-in-production"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-generate JWKS URL if not provided
        if not self.COGNITO_JWKS_URL and self.COGNITO_USER_POOL_ID:
            self.COGNITO_JWKS_URL = (
                f"https://cognito-idp.{self.COGNITO_REGION}.amazonaws.com/"
                f"{self.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
            )


settings = Settings()
