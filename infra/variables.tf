variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
  default     = "959545103699"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "ai-website-builder"
}

# VPC Configuration
variable "vpc_id" {
  description = "Existing VPC ID"
  type        = string
  default     = "vpc-0ff408f14aecb4363"
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for RDS and Redis"
  type        = list(string)
  default = [
    "subnet-06a7755a28d242d10", # us-east-1a
    "subnet-0ec08327d53513ce6", # us-east-1b
    "subnet-04c4b09df3b467415"  # us-east-1c
  ]
}

variable "public_subnet_ids" {
  description = "Public subnet IDs for ALB"
  type        = list(string)
  default = [
    "subnet-097171e1328af8777", # us-east-1a
    "subnet-0e9822121d53f1f9d", # us-east-1b
    "subnet-01b43b037b4ba70f5"  # us-east-1c
  ]
}

# EKS Configuration
variable "eks_cluster_name" {
  description = "Existing EKS cluster name"
  type        = string
  default     = "ai-site-builder"
}

variable "eks_namespace" {
  description = "Kubernetes namespace for the application"
  type        = string
  default     = "ai-website-builder"
}

# RDS Configuration
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t4g.medium"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "ai_website_builder"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "admin"
}

variable "db_allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

# Redis Configuration
variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t4g.micro"
}

# Domain Configuration
variable "domain_name" {
  description = "Domain name for the platform"
  type        = string
  default     = "chinabjalex.com"
}

# S3 Bucket Names
variable "sites_bucket_name" {
  description = "S3 bucket for published sites"
  type        = string
  default     = "ai-wb-sites-959545103699"
}

variable "assets_bucket_name" {
  description = "S3 bucket for user assets"
  type        = string
  default     = "ai-wb-assets-959545103699"
}

variable "templates_bucket_name" {
  description = "S3 bucket for templates"
  type        = string
  default     = "ai-wb-templates-959545103699"
}

# DynamoDB Configuration
variable "page_views_table_name" {
  description = "DynamoDB table for page views"
  type        = string
  default     = "ai-wb-page-views"
}

variable "page_view_daily_table_name" {
  description = "DynamoDB table for daily aggregated page views"
  type        = string
  default     = "ai-wb-page-view-daily"
}
