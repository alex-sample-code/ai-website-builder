# AI Website Builder

An AI-powered SaaS platform for building professional websites through conversational AI, with a visual editor for customization and one-click publishing to custom domains.

## Overview

This platform enables small and medium businesses to create professional websites through:
- **AI Conversational Builder**: Generate complete websites through natural dialogue
- **Visual Editor**: Fine-tune with GrapesJS drag-and-drop editor
- **One-Click Publishing**: Deploy to CDN with custom domain support
- **Management Dashboard**: Post-launch content management, forms, analytics

## Architecture

- **Backend**: Python (FastAPI) on AWS EKS
- **Frontend**: React + TypeScript + GrapesJS
- **AI Engine**: AWS Bedrock (Claude Sonnet 4.6)
- **Database**: Amazon RDS PostgreSQL 16 + DynamoDB (analytics)
- **Storage**: Amazon S3 (sites, assets, templates)
- **CDN**: CloudFront with multi-tenant distribution
- **Authentication**: Amazon Cognito

## Project Structure

```
ai-website-builder/
├── backend/              # Python FastAPI application
│   ├── app/
│   │   ├── main.py      # Application entry point
│   │   ├── config.py    # Configuration
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── api/         # API routes
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utilities
│   ├── alembic/         # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # React application
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── infra/               # Terraform infrastructure
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       ├── rds/
│       ├── redis/
│       ├── s3/
│       ├── cloudfront/
│       ├── cognito/
│       ├── dynamodb/
│       ├── eks/
│       └── route53/
├── docs/
│   └── PRD.md           # Product Requirements Document
├── docker-compose.yml   # Local development
├── Makefile            # Common commands
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for frontend development)
- Python 3.12+ (for backend development)
- AWS CLI (for infrastructure deployment)
- Terraform 1.5+ (for infrastructure)

### Local Development

1. **Start all services**:
```bash
make dev
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- LocalStack (S3, DynamoDB) on port 4566
- Backend API on port 8000
- Frontend on port 3000

2. **Setup local AWS resources**:
```bash
make setup-local-aws
```

3. **Run database migrations**:
```bash
make migrate
```

4. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### Available Commands

```bash
# Development
make dev              # Start development environment
make dev-down         # Stop services
make dev-logs         # View logs
make dev-clean        # Clean up everything

# Infrastructure
make infra-init       # Initialize Terraform
make infra-plan       # Plan infrastructure changes
make infra-apply      # Apply infrastructure (CAUTION)

# Database
make migrate          # Run migrations
make migrate-create   # Create new migration

# Quality
make test             # Run tests
make lint             # Run linters
make format           # Format code
```

## Infrastructure Deployment

See [infra/README.md](infra/README.md) for detailed infrastructure setup instructions.

### Existing Resources

The following AWS resources already exist and are reused:
- VPC: `vpc-0ff408f14aecb4363` (10.0.0.0/16)
- EKS Cluster: `ai-site-builder` (Kubernetes 1.32)
- Region: `us-east-1`

### Resources to be Created

- RDS PostgreSQL 16 (db.t4g.medium)
- ElastiCache Redis 7 (cache.t4g.micro)
- S3 buckets (3): sites, assets, templates
- CloudFront distribution for platform
- Cognito User Pool
- DynamoDB tables (2): page views, daily aggregates
- EKS namespace and IRSA role
- ACM certificate for *.chinabjalex.com

## Tech Stack

### Backend
- Python 3.12
- FastAPI (async web framework)
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Boto3 (AWS SDK)
- PostgreSQL 16
- Redis 7

### Frontend
- React 18
- TypeScript
- Vite (build tool)
- GrapesJS (page builder)
- Ant Design (UI components)
- Tailwind CSS
- AWS Amplify (auth)

### Infrastructure
- AWS EKS (Kubernetes)
- Amazon RDS PostgreSQL
- Amazon ElastiCache Redis
- Amazon S3
- Amazon CloudFront
- Amazon Cognito
- Amazon Bedrock
- Amazon DynamoDB
- Terraform

## Development Workflow

1. **Feature Development**:
   - Create feature branch from `master`
   - Develop locally using `make dev`
   - Write tests
   - Run linting: `make lint`
   - Format code: `make format`

2. **Database Changes**:
   - Create migration: `make migrate-create`
   - Review generated migration
   - Apply: `make migrate`

3. **Testing**:
   - Run tests: `make test`
   - Check coverage report

4. **Infrastructure Changes**:
   - Update Terraform files in `infra/`
   - Plan changes: `make infra-plan`
   - Review plan carefully
   - Apply: `make infra-apply` (after approval)

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://admin:password@localhost:5432/ai_website_builder
REDIS_URL=redis://localhost:6379/0
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-6
S3_SITES_BUCKET=ai-wb-sites-959545103699
S3_ASSETS_BUCKET=ai-wb-assets-959545103699
S3_TEMPLATES_BUCKET=ai-wb-templates-959545103699
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_COGNITO_USER_POOL_ID=your-pool-id
VITE_COGNITO_CLIENT_ID=your-client-id
```

## Documentation

- [Product Requirements Document](docs/PRD.md)
- [Infrastructure Setup](infra/README.md)
- [API Documentation](http://localhost:8000/api/docs) (when running)

## Cost Estimation

**Initial (0-100 tenants)**: ~$300-500/month
- EKS: ~$120
- RDS: ~$50
- Redis: ~$15
- S3 + CloudFront: ~$20
- Bedrock: ~$50-100 (usage-based)
- Other: ~$20

## Security

- All credentials stored in AWS Secrets Manager
- RDS and Redis in private subnets
- S3 buckets not publicly accessible
- CloudFront Origin Access Control enforced
- IAM roles follow least privilege
- Cognito for authentication
- MFA supported

## Contributing

1. Read the PRD: `docs/PRD.md`
2. Follow the development workflow
3. Ensure tests pass
4. Follow code style guidelines

## License

Proprietary - All rights reserved

## Support

For questions or issues, please contact the development team.
