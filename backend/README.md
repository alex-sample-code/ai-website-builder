# AI Website Builder - Backend API

FastAPI-based backend for the AI Website Builder platform.

## 🏗️ Architecture

- **Framework**: FastAPI 0.115.0 with Python 3.12
- **Database**: PostgreSQL 16 with async SQLAlchemy 2.0
- **Cache**: Redis 7
- **Authentication**: AWS Cognito + JWT
- **AI**: AWS Bedrock Claude Sonnet 4.6 (placeholder for Task 3)
- **Storage**: AWS S3 + CloudFront
- **Analytics**: DynamoDB

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection & session management
│   │
│   ├── models/              # SQLAlchemy models (14 models)
│   │   ├── tenant.py        # Tenant (multi-tenancy)
│   │   ├── user.py          # User accounts
│   │   ├── site.py          # Website sites
│   │   ├── page.py          # Website pages
│   │   ├── site_version.py  # Version control
│   │   ├── site_settings.py # Site configuration
│   │   ├── nav_menu.py      # Navigation menus
│   │   ├── asset.py         # Uploaded files
│   │   ├── ai_session.py    # AI generation sessions
│   │   ├── blog.py          # Blog posts, categories, tags
│   │   ├── form.py          # Form definitions & submissions
│   │   ├── integration.py   # Third-party integrations
│   │   ├── audit_log.py     # Activity logs
│   │   └── team_invitation.py # Team member invitations
│   │
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── common.py        # Base schemas
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── site.py
│   │   ├── page.py
│   │   ├── blog.py
│   │   ├── form.py
│   │   └── ai_session.py
│   │
│   ├── api/                 # API routes
│   │   └── v1/
│   │       ├── __init__.py  # API router aggregation
│   │       ├── health.py    # Health check endpoints
│   │       ├── auth.py      # Authentication (register, login, /me)
│   │       ├── sites.py     # Site CRUD
│   │       └── pages.py     # Page CRUD
│   │
│   ├── auth/                # Authentication & authorization
│   │   ├── jwt.py           # JWT token verification
│   │   ├── cognito.py       # AWS Cognito client
│   │   └── deps.py          # FastAPI dependencies (get_current_user, etc.)
│   │
│   ├── services/            # Business logic layer
│   │   ├── site_service.py      # Site operations
│   │   ├── publish_service.py   # Publishing to S3 + CloudFront
│   │   └── ai_service.py        # AI generation (placeholder for Task 3)
│   │
│   └── utils/               # Utility functions
│
├── alembic/                 # Database migrations
│   ├── versions/
│   │   └── 001_initial_migration.py  # All 14 tables
│   └── env.py               # Alembic configuration
│
├── requirements.txt         # Python dependencies
├── Dockerfile              # Production Docker image
└── .env.example            # Environment variables template
```

## 🗄️ Database Models

### Core Entities
1. **Tenant** - Multi-tenant isolation (companies/organizations)
2. **User** - User accounts with role-based access
3. **Site** - Websites created by tenants
4. **Page** - Individual pages within sites
5. **SiteVersion** - Version control for published sites
6. **SiteSettings** - Site-wide configuration
7. **NavMenu** - Navigation menu configurations

### Content & Assets
8. **Asset** - Uploaded files (images, documents)
9. **BlogPost**, **BlogCategory**, **BlogTag** - Blog functionality
10. **FormDefinition**, **FormSubmission** - Custom forms & inquiries

### AI & Integrations
11. **AISession** - AI website generation sessions
12. **Integration** - Third-party service integrations
13. **AuditLog** - Activity tracking
14. **TeamInvitation** - Team member invitations

## 🔐 Authentication Flow

1. **Register**: `POST /api/v1/auth/register`
   - Creates Cognito user
   - Creates database user + tenant
   - Returns JWT tokens

2. **Login**: `POST /api/v1/auth/login`
   - Authenticates via Cognito
   - Returns JWT tokens

3. **Protected Routes**:
   - Use `get_current_user` dependency
   - Automatic tenant isolation via `tenant_id`
   - Role-based access control (owner/editor/viewer)

## 🚀 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/forgot-password` - Forgot password

### Sites
- `GET /api/v1/sites` - List all sites
- `POST /api/v1/sites` - Create site
- `GET /api/v1/sites/{id}` - Get site details
- `PUT /api/v1/sites/{id}` - Update site
- `DELETE /api/v1/sites/{id}` - Delete site

### Pages
- `GET /api/v1/sites/{site_id}/pages` - List pages
- `POST /api/v1/sites/{site_id}/pages` - Create page
- `GET /api/v1/sites/{site_id}/pages/{id}` - Get page with GrapesJS data
- `PUT /api/v1/sites/{site_id}/pages/{id}` - Update page
- `PUT /api/v1/sites/{site_id}/pages/{id}/content` - Quick content update
- `DELETE /api/v1/sites/{site_id}/pages/{id}` - Delete page
- `PUT /api/v1/sites/{site_id}/pages/reorder` - Reorder pages

### Health
- `GET /health` - Basic health check
- `GET /api/v1/health` - Health check
- `GET /api/v1/health/db` - Database health
- `GET /api/v1/health/full` - Full system health

## 🛠️ Development Setup

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- PostgreSQL 16 (via Docker)
- Redis 7 (via Docker)

### Quick Start

1. **Start services**:
```bash
make dev
```

This starts:
- Backend API at http://localhost:8000
- PostgreSQL at localhost:5432
- Redis at localhost:6379
- LocalStack (S3, DynamoDB) at localhost:4566
- API Docs at http://localhost:8000/api/docs

2. **Run migrations**:
```bash
make migrate
```

3. **View logs**:
```bash
make dev-logs
```

4. **Stop services**:
```bash
make dev-down
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://admin:password@postgres:5432/ai_website_builder

# Redis
REDIS_URL=redis://redis:6379/0

# AWS (use production values or LocalStack)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test  # For LocalStack
AWS_SECRET_ACCESS_KEY=test  # For LocalStack
AWS_ENDPOINT_URL=http://localstack:4566  # For LocalStack

# Cognito
COGNITO_USER_POOL_ID=us-east-1_UkKMQIN1R
COGNITO_CLIENT_ID=7kji0ar3m8g81pjr0fnkrpsirb

# S3 Buckets
S3_SITES_BUCKET=ai-wb-sites-959545103699
S3_ASSETS_BUCKET=ai-wb-assets-959545103699
S3_TEMPLATES_BUCKET=ai-wb-templates-959545103699
```

## 📊 Database Migrations

### Create new migration:
```bash
make migrate-create
```

### Apply migrations:
```bash
make migrate
```

### Migration files:
Located in `alembic/versions/`

## 🧪 Testing

```bash
make test
```

Runs pytest with coverage report.

## 📝 Code Quality

### Linting:
```bash
make lint
```

### Formatting:
```bash
make format
```

Uses:
- Black for code formatting
- Ruff for linting
- MyPy for type checking

## 🔒 Security

- JWT token verification via AWS Cognito
- Row-level tenant isolation
- Role-based access control (RBAC)
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Input validation (Pydantic)

## 📦 Dependencies

Key dependencies:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy[asyncio]` - Async ORM
- `asyncpg` - Async PostgreSQL driver
- `alembic` - Database migrations
- `pydantic-settings` - Configuration management
- `python-jose` - JWT handling
- `boto3` - AWS SDK
- `redis` - Caching
- `httpx` - HTTP client

## 🚧 TODO (Task 3 - AI Integration)

The following AI functionality is stubbed out for Task 3:
- [ ] Bedrock Claude integration
- [ ] AI conversation flow
- [ ] Website generation from conversation
- [ ] GrapesJS template generation
- [ ] Image placeholder generation
- [ ] SEO optimization

## 📚 API Documentation

When running in development mode, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 🤝 Contributing

1. Create a feature branch
2. Make changes
3. Run tests and linting
4. Create pull request

## 📄 License

Proprietary - All rights reserved
