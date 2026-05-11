output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_instance_endpoint
  sensitive   = true
}

output "rds_secret_arn" {
  description = "ARN of the Secrets Manager secret containing DB credentials"
  value       = module.rds.db_password_secret_arn
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = module.redis.redis_endpoint
}

output "cognito_user_pool_id" {
  description = "Cognito User Pool ID"
  value       = module.cognito.user_pool_id
}

output "cognito_user_pool_client_id" {
  description = "Cognito User Pool Client ID"
  value       = module.cognito.user_pool_client_id
}

output "s3_sites_bucket" {
  description = "S3 bucket for published sites"
  value       = module.s3.sites_bucket_name
}

output "s3_assets_bucket" {
  description = "S3 bucket for user assets"
  value       = module.s3.assets_bucket_name
}

output "s3_templates_bucket" {
  description = "S3 bucket for templates"
  value       = module.s3.templates_bucket_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID for platform"
  value       = module.cloudfront.platform_distribution_id
}

output "cloudfront_distribution_domain" {
  description = "CloudFront distribution domain name"
  value       = module.cloudfront.platform_distribution_domain
}

output "irsa_role_arn" {
  description = "IRSA role ARN for EKS service account"
  value       = module.eks_irsa.role_arn
}

output "kubernetes_namespace" {
  description = "Kubernetes namespace"
  value       = kubernetes_namespace.app.metadata[0].name
}

output "dynamodb_page_views_table" {
  description = "DynamoDB page views table name"
  value       = module.dynamodb.page_views_table_name
}

output "dynamodb_page_view_daily_table" {
  description = "DynamoDB daily page views table name"
  value       = module.dynamodb.page_view_daily_table_name
}

output "acm_certificate_arn" {
  description = "ACM certificate ARN"
  value       = module.route53_acm.acm_certificate_arn
}
