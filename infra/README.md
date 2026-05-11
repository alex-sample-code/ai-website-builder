# AI Website Builder - Infrastructure

This directory contains Terraform configurations for deploying the AI Website Builder infrastructure on AWS.

## Prerequisites

- Terraform >= 1.5.0
- AWS CLI configured with appropriate credentials
- Existing resources:
  - VPC: `vpc-0ff408f14aecb4363`
  - EKS cluster: `ai-site-builder`
  - Route53 hosted zone for `chinabjalex.com`

## Architecture

The infrastructure includes:

- **RDS PostgreSQL 16**: Business data storage (db.t4g.medium)
- **ElastiCache Redis 7**: Session cache and AI context (cache.t4g.micro)
- **S3 Buckets**: Static sites, user assets, and templates
- **CloudFront**: CDN for platform frontend
- **Cognito**: User authentication and management
- **DynamoDB**: Page view analytics (on-demand)
- **EKS IRSA**: Service account with permissions for S3, Bedrock, SES, etc.

## Setup

1. **Initialize Terraform backend**:

First, create the S3 backend bucket if it doesn't exist:

```bash
aws s3 mb s3://terraform-state-959545103699 --region us-east-1
aws s3api put-bucket-versioning \
  --bucket terraform-state-959545103699 \
  --versioning-configuration Status=Enabled

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

2. **Configure variables**:

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your specific values
```

3. **Initialize Terraform**:

```bash
terraform init
```

4. **Plan infrastructure changes**:

```bash
terraform plan -out=tfplan
```

5. **Apply infrastructure** (after review):

```bash
terraform apply tfplan
```

## Modules

### RDS
- PostgreSQL 16 instance
- Automated backups (7 days retention)
- Password stored in AWS Secrets Manager
- Private subnet only, accessible from EKS

### Redis
- ElastiCache Redis 7.1
- Single node (can be upgraded to cluster)
- LRU eviction policy
- Private subnet only

### S3
- Three buckets: sites, assets, templates
- Versioning enabled
- Server-side encryption
- CORS configured for web access

### CloudFront
- Standard distribution for platform frontend
- Custom domain support (www.chinabjalex.com, api.chinabjalex.com)
- HTTPS with ACM certificate
- Origin Access Control for S3

### Cognito
- User pool with email authentication
- Custom attribute: tenant_id
- MFA optional
- OAuth 2.0 flows enabled

### DynamoDB
- Page views table with TTL (90 days)
- Daily aggregated views table
- On-demand capacity mode

### EKS IRSA
- IAM role for service account
- Permissions: S3, Bedrock, DynamoDB, CloudFront, SES, Secrets Manager

### Route53 & ACM
- Wildcard SSL certificate (*.chinabjalex.com)
- DNS validation
- Managed by ACM

## Outputs

After applying, Terraform will output:

- RDS endpoint and credentials ARN
- Redis endpoint
- Cognito User Pool ID and Client ID
- S3 bucket names
- CloudFront distribution details
- IRSA role ARN

## Security

- All database credentials stored in AWS Secrets Manager
- RDS and Redis in private subnets only
- S3 buckets not publicly accessible
- CloudFront Origin Access Control enforced
- IAM roles follow least privilege principle

## Cost Estimation

Initial monthly cost: ~$300-500

- EKS: ~$120 (2x t3.large nodes)
- RDS: ~$50 (db.t4g.medium single-AZ)
- Redis: ~$15 (cache.t4g.micro)
- S3 + CloudFront: ~$20 (low traffic)
- Bedrock: ~$50-100 (usage-based)
- Other services: ~$20

## Notes

- DO NOT run `terraform destroy` in production without backup
- Always review `terraform plan` before applying
- State file is stored in S3 with encryption
- Lock state is managed via DynamoDB

## Next Steps

After infrastructure is deployed:

1. Update backend configuration with RDS endpoint and credentials
2. Configure Kubernetes deployments with IRSA service account
3. Set up CI/CD pipelines
4. Configure Route53 DNS records for CloudFront
