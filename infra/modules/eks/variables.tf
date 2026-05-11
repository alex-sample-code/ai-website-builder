variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "eks_cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
}

variable "service_account" {
  description = "Kubernetes service account name"
  type        = string
}

variable "sites_bucket_arn" {
  description = "ARN of sites S3 bucket"
  type        = string
}

variable "assets_bucket_arn" {
  description = "ARN of assets S3 bucket"
  type        = string
}

variable "templates_bucket_arn" {
  description = "ARN of templates S3 bucket"
  type        = string
}

variable "page_views_table_arn" {
  description = "ARN of page views DynamoDB table"
  type        = string
}

variable "page_view_daily_table_arn" {
  description = "ARN of daily page views DynamoDB table"
  type        = string
}

variable "db_secret_arn" {
  description = "ARN of database credentials secret"
  type        = string
}
