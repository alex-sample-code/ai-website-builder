# CloudFront Origin Access Control for S3
resource "aws_cloudfront_origin_access_control" "sites" {
  name                              = "${var.project_name}-sites-oac"
  description                       = "OAC for sites bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# CloudFront distribution for platform (frontend + API)
resource "aws_cloudfront_distribution" "platform" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${var.project_name} platform distribution"
  default_root_object = "index.html"
  price_class         = "PriceClass_100"

  aliases = ["www.${var.domain_name}", "api.${var.domain_name}"]

  # Origin for static frontend (S3 or can be updated to ALB later)
  origin {
    domain_name              = var.sites_bucket_name
    origin_id                = "S3-${var.sites_bucket_name}"
    origin_access_control_id = aws_cloudfront_origin_access_control.sites.id
    origin_path              = "/platform"
  }

  # Default cache behavior for frontend
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${var.sites_bucket_name}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
  }

  # Custom error responses for SPA
  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }

  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"
  }

  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name = "${var.project_name}-platform-distribution"
  }
}

# S3 bucket policy to allow CloudFront OAC
data "aws_s3_bucket" "sites" {
  bucket = var.sites_bucket_name
}

resource "aws_s3_bucket_policy" "sites_cloudfront" {
  bucket = data.aws_s3_bucket.sites.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontOAC"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${data.aws_s3_bucket.sites.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.platform.arn
          }
        }
      }
    ]
  })
}
