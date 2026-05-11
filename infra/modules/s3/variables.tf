variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "sites_bucket_name" {
  description = "S3 bucket name for published sites"
  type        = string
}

variable "assets_bucket_name" {
  description = "S3 bucket name for user assets"
  type        = string
}

variable "templates_bucket_name" {
  description = "S3 bucket name for templates"
  type        = string
}
