# Data sources
data "aws_vpc" "main" {
  id = var.vpc_id
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }

  filter {
    name   = "tag:Name"
    values = ["*private*"]
  }
}

data "aws_caller_identity" "current" {}

# Kubernetes namespace
resource "kubernetes_namespace" "app" {
  metadata {
    name = var.eks_namespace

    labels = {
      name    = var.eks_namespace
      project = var.project_name
    }
  }
}

# RDS PostgreSQL
module "rds" {
  source = "./modules/rds"

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = var.vpc_id
  subnet_ids         = var.private_subnet_ids
  db_name            = var.db_name
  db_username        = var.db_username
  instance_class     = var.db_instance_class
  allocated_storage  = var.db_allocated_storage
  eks_cluster_name   = var.eks_cluster_name
}

# ElastiCache Redis
module "redis" {
  source = "./modules/redis"

  project_name     = var.project_name
  environment      = var.environment
  vpc_id           = var.vpc_id
  subnet_ids       = var.private_subnet_ids
  node_type        = var.redis_node_type
  eks_cluster_name = var.eks_cluster_name
}

# S3 Buckets
module "s3" {
  source = "./modules/s3"

  project_name          = var.project_name
  environment           = var.environment
  sites_bucket_name     = var.sites_bucket_name
  assets_bucket_name    = var.assets_bucket_name
  templates_bucket_name = var.templates_bucket_name
}

# CloudFront
module "cloudfront" {
  source = "./modules/cloudfront"

  project_name        = var.project_name
  environment         = var.environment
  domain_name         = var.domain_name
  acm_certificate_arn = module.route53_acm.acm_certificate_arn
  sites_bucket_name   = module.s3.sites_bucket_name

  depends_on = [module.route53_acm]
}

# Cognito
module "cognito" {
  source = "./modules/cognito"

  project_name = var.project_name
  environment  = var.environment
  domain_name  = var.domain_name
}

# DynamoDB
module "dynamodb" {
  source = "./modules/dynamodb"

  project_name               = var.project_name
  environment                = var.environment
  page_views_table_name      = var.page_views_table_name
  page_view_daily_table_name = var.page_view_daily_table_name
}

# Route53 and ACM
module "route53_acm" {
  source = "./modules/route53"

  domain_name = var.domain_name
}

# EKS IRSA (IAM Role for Service Account)
module "eks_irsa" {
  source = "./modules/eks"

  project_name      = var.project_name
  environment       = var.environment
  eks_cluster_name  = var.eks_cluster_name
  namespace         = kubernetes_namespace.app.metadata[0].name
  service_account   = "ai-website-builder-sa"

  # S3 buckets
  sites_bucket_arn     = module.s3.sites_bucket_arn
  assets_bucket_arn    = module.s3.assets_bucket_arn
  templates_bucket_arn = module.s3.templates_bucket_arn

  # DynamoDB tables
  page_views_table_arn      = module.dynamodb.page_views_table_arn
  page_view_daily_table_arn = module.dynamodb.page_view_daily_table_arn

  # Secrets Manager
  db_secret_arn = module.rds.db_password_secret_arn
}

# Create Kubernetes service account
resource "kubernetes_service_account" "app" {
  metadata {
    name      = "ai-website-builder-sa"
    namespace = kubernetes_namespace.app.metadata[0].name

    annotations = {
      "eks.amazonaws.com/role-arn" = module.eks_irsa.role_arn
    }
  }

  automount_service_account_token = true
}
