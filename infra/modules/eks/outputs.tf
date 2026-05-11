output "role_arn" {
  description = "ARN of the IRSA role"
  value       = aws_iam_role.irsa.arn
}

output "role_name" {
  description = "Name of the IRSA role"
  value       = aws_iam_role.irsa.name
}
