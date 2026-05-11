variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "page_views_table_name" {
  description = "DynamoDB table name for page views"
  type        = string
}

variable "page_view_daily_table_name" {
  description = "DynamoDB table name for daily page views"
  type        = string
}
