output "hosted_zone_id" {
  description = "Route53 hosted zone ID"
  value       = data.aws_route53_zone.main.zone_id
}

output "hosted_zone_name" {
  description = "Route53 hosted zone name"
  value       = data.aws_route53_zone.main.name
}

output "acm_certificate_arn" {
  description = "ACM certificate ARN"
  value       = aws_acm_certificate.main.arn
}

output "acm_certificate_domain" {
  description = "ACM certificate domain"
  value       = aws_acm_certificate.main.domain_name
}
