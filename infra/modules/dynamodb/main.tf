# DynamoDB table for page views (raw events)
resource "aws_dynamodb_table" "page_views" {
  name           = var.page_views_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "site_id"
  range_key      = "timestamp_visitor"

  attribute {
    name = "site_id"
    type = "S"
  }

  attribute {
    name = "timestamp_visitor"
    type = "S"
  }

  ttl {
    enabled        = true
    attribute_name = "ttl"
  }

  point_in_time_recovery {
    enabled = var.environment == "prod"
  }

  tags = {
    Name = var.page_views_table_name
  }
}

# DynamoDB table for daily aggregated page views
resource "aws_dynamodb_table" "page_view_daily" {
  name         = var.page_view_daily_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "site_id"
  range_key    = "date_page"

  attribute {
    name = "site_id"
    type = "S"
  }

  attribute {
    name = "date_page"
    type = "S"
  }

  point_in_time_recovery {
    enabled = var.environment == "prod"
  }

  tags = {
    Name = var.page_view_daily_table_name
  }
}
