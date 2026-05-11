output "platform_distribution_id" {
  description = "CloudFront distribution ID for platform"
  value       = aws_cloudfront_distribution.platform.id
}

output "platform_distribution_domain" {
  description = "CloudFront distribution domain name"
  value       = aws_cloudfront_distribution.platform.domain_name
}

output "platform_distribution_arn" {
  description = "CloudFront distribution ARN"
  value       = aws_cloudfront_distribution.platform.arn
}
