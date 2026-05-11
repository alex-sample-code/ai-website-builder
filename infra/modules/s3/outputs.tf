output "sites_bucket_name" {
  description = "Name of the sites S3 bucket"
  value       = aws_s3_bucket.sites.id
}

output "sites_bucket_arn" {
  description = "ARN of the sites S3 bucket"
  value       = aws_s3_bucket.sites.arn
}

output "sites_bucket_domain_name" {
  description = "Domain name of the sites S3 bucket"
  value       = aws_s3_bucket.sites.bucket_regional_domain_name
}

output "assets_bucket_name" {
  description = "Name of the assets S3 bucket"
  value       = aws_s3_bucket.assets.id
}

output "assets_bucket_arn" {
  description = "ARN of the assets S3 bucket"
  value       = aws_s3_bucket.assets.arn
}

output "templates_bucket_name" {
  description = "Name of the templates S3 bucket"
  value       = aws_s3_bucket.templates.id
}

output "templates_bucket_arn" {
  description = "ARN of the templates S3 bucket"
  value       = aws_s3_bucket.templates.arn
}
