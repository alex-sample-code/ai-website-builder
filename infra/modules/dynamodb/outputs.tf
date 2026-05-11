output "page_views_table_name" {
  description = "DynamoDB page views table name"
  value       = aws_dynamodb_table.page_views.name
}

output "page_views_table_arn" {
  description = "DynamoDB page views table ARN"
  value       = aws_dynamodb_table.page_views.arn
}

output "page_view_daily_table_name" {
  description = "DynamoDB daily page views table name"
  value       = aws_dynamodb_table.page_view_daily.name
}

output "page_view_daily_table_arn" {
  description = "DynamoDB daily page views table ARN"
  value       = aws_dynamodb_table.page_view_daily.arn
}
