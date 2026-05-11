# Data sources
data "aws_eks_cluster" "main" {
  name = var.eks_cluster_name
}

data "aws_iam_openid_connect_provider" "eks" {
  url = data.aws_eks_cluster.main.identity[0].oidc[0].issuer
}

# IAM role for service account
resource "aws_iam_role" "irsa" {
  name = "${var.project_name}-irsa-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = data.aws_iam_openid_connect_provider.eks.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${replace(data.aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub" = "system:serviceaccount:${var.namespace}:${var.service_account}"
            "${replace(data.aws_iam_openid_connect_provider.eks.url, "https://", "")}:aud" = "sts.amazonaws.com"
          }
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-irsa-role"
  }
}

# IAM policy for S3 access
resource "aws_iam_policy" "s3_access" {
  name        = "${var.project_name}-s3-access"
  description = "Policy for S3 bucket access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          var.sites_bucket_arn,
          "${var.sites_bucket_arn}/*",
          var.assets_bucket_arn,
          "${var.assets_bucket_arn}/*",
          var.templates_bucket_arn,
          "${var.templates_bucket_arn}/*"
        ]
      }
    ]
  })
}

# IAM policy for Bedrock access
resource "aws_iam_policy" "bedrock_access" {
  name        = "${var.project_name}-bedrock-access"
  description = "Policy for Bedrock API access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM policy for DynamoDB access
resource "aws_iam_policy" "dynamodb_access" {
  name        = "${var.project_name}-dynamodb-access"
  description = "Policy for DynamoDB access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchGetItem",
          "dynamodb:BatchWriteItem"
        ]
        Resource = [
          var.page_views_table_arn,
          var.page_view_daily_table_arn
        ]
      }
    ]
  })
}

# IAM policy for CloudFront access
resource "aws_iam_policy" "cloudfront_access" {
  name        = "${var.project_name}-cloudfront-access"
  description = "Policy for CloudFront management"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "cloudfront:CreateDistribution",
          "cloudfront:GetDistribution",
          "cloudfront:UpdateDistribution",
          "cloudfront:DeleteDistribution",
          "cloudfront:CreateInvalidation",
          "cloudfront:GetInvalidation",
          "cloudfront:ListDistributions"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM policy for SES access
resource "aws_iam_policy" "ses_access" {
  name        = "${var.project_name}-ses-access"
  description = "Policy for SES email sending"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM policy for Secrets Manager access
resource "aws_iam_policy" "secrets_access" {
  name        = "${var.project_name}-secrets-access"
  description = "Policy for Secrets Manager access"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          var.db_secret_arn
        ]
      }
    ]
  })
}

# Attach policies to role
resource "aws_iam_role_policy_attachment" "s3" {
  role       = aws_iam_role.irsa.name
  policy_arn = aws_iam_policy.s3_access.arn
}

resource "aws_iam_role_policy_attachment" "bedrock" {
  role       = aws_iam_role.irsa.name
  policy_arn = aws_iam_policy.bedrock_access.arn
}

resource "aws_iam_role_policy_attachment" "dynamodb" {
  role       = aws_iam_role.irsa.name
  policy_arn = aws_iam_policy.dynamodb_access.arn
}

resource "aws_iam_role_policy_attachment" "cloudfront" {
  role       = aws_iam_role.irsa.name
  policy_arn = aws_iam_policy.cloudfront_access.arn
}

resource "aws_iam_role_policy_attachment" "ses" {
  role       = aws_iam_role.irsa.name
  policy_arn = aws_iam_policy.ses_access.arn
}

resource "aws_iam_role_policy_attachment" "secrets" {
  role       = aws_iam_role.irsa.name
  policy_arn = aws_iam_policy.secrets_access.arn
}
