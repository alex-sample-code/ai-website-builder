# AI Website Builder - AWS Infrastructure Resources

**Region:** us-east-1
**AWS Account:** 959545103699
**VPC:** vpc-0ff408f14aecb4363 (eks-vpc, 10.0.0.0/16)
**Created:** 2026-05-11

---

## 1. Networking

### VPC (Pre-existing)
- **VPC ID:** vpc-0ff408f14aecb4363
- **Name:** eks-vpc
- **CIDR:** 10.0.0.0/16

### Subnets (Pre-existing)

**Private Subnets:**
- subnet-06a7755a28d242d10 (us-east-1a, 10.0.128.0/20, eks-subnet-private1-us-east-1a)
- subnet-0ec08327d53513ce6 (us-east-1b, 10.0.144.0/20, eks-subnet-private2-us-east-1b)
- subnet-04c4b09df3b467415 (us-east-1c, 10.0.160.0/20, eks-subnet-private3-us-east-1c)
- subnet-038a4df0121efa8be (us-east-1d, 10.0.101.0/24, eks-subnet-private4-us-east-1d)

**Public Subnets:**
- subnet-097171e1328af8777 (us-east-1a, 10.0.0.0/20, eks-subnet-public1-us-east-1a)
- subnet-0e9822121d53f1f9d (us-east-1b, 10.0.16.0/20, eks-subnet-public2-us-east-1b)
- subnet-01b43b037b4ba70f5 (us-east-1c, 10.0.32.0/20, eks-subnet-public3-us-east-1c)

### Security Groups

**ALB Security Group**
- **ID:** sg-0889572eb6e1239a0
- **Name:** ai-wb-alb-sg
- **Description:** Security group for AI Website Builder ALB - allows traffic from CloudFront
- **Ingress Rules:**
  - Port 443 (HTTPS) from CloudFront managed prefix list (pl-3b927c52)
  - *Note: Port 80 could not be added due to security group rules limit from CloudFront prefix list size*

**RDS Security Group**
- **ID:** sg-00131e4ccd212db84
- **Name:** ai-wb-rds-sg
- **Description:** Security group for AI Website Builder RDS PostgreSQL
- **Ingress Rules:**
  - Port 5432 (PostgreSQL) from EKS cluster security group (sg-0943b35f818cc7c6a)

**Redis Security Group**
- **ID:** sg-031568627c3c86cda
- **Name:** ai-wb-redis-sg
- **Description:** Security group for AI Website Builder Redis
- **Ingress Rules:**
  - Port 6379 (Redis) from EKS cluster security group (sg-0943b35f818cc7c6a)

---

## 2. Compute

### EKS Cluster
- **Name:** ai-website-builder
- **Status:** ACTIVE
- **Kubernetes Version:** 1.31
- **Cluster Role ARN:** arn:aws:iam::959545103699:role/eksClusterRole
- **Cluster Security Group:** sg-0943b35f818cc7c6a
- **VPC Config:** Private subnets (subnet-06a7755a28d242d10, subnet-0ec08327d53513ce6, subnet-04c4b09df3b467415)
- **Endpoint:** Use `aws eks describe-cluster --name ai-website-builder --query 'cluster.endpoint'` to retrieve

### EKS Node Group
- **Name:** ai-wb-nodes
- **Status:** ACTIVE
- **Instance Types:** t3.large
- **Scaling:** Min: 2, Max: 4, Desired: 2
- **Node Role ARN:** arn:aws:iam::959545103699:role/eksNodeRole
- **Subnets:** subnet-06a7755a28d242d10, subnet-0ec08327d53513ce6, subnet-04c4b09df3b467415

---

## 3. Database

### RDS PostgreSQL
- **Instance Identifier:** ai-wb-postgres
- **Status:** AVAILABLE
- **Engine:** PostgreSQL 16.13
- **Instance Class:** db.t4g.medium
- **Storage:** 20 GB gp3 (3000 IOPS, 125 MB/s throughput)
- **Database Name:** ai_website_builder
- **Master Username:** dbadmin
- **Master Password:** Stored in AWS Secrets Manager (ai-wb/rds-password)
- **Secrets Manager ARN:** arn:aws:secretsmanager:us-east-1:959545103699:secret:ai-wb/rds-password-6Zk5v9
- **VPC Security Group:** sg-00131e4ccd212db84
- **Subnet Group:** ai-wb-db-subnet
- **Publicly Accessible:** No
- **Endpoint:** ai-wb-postgres.cwcf9hkggcry.us-east-1.rds.amazonaws.com:5432
- **Connection String:** postgresql://dbadmin:PASSWORD@ai-wb-postgres.cwcf9hkggcry.us-east-1.rds.amazonaws.com:5432/ai_website_builder

### ElastiCache Redis
- **Cluster ID:** ai-wb-redis
- **Status:** AVAILABLE
- **Engine:** Redis 7.1
- **Node Type:** cache.t4g.micro
- **Number of Nodes:** 1
- **VPC Security Group:** sg-031568627c3c86cda
- **Subnet Group:** ai-wb-redis-subnet
- **Endpoint:** ai-wb-redis.xfshub.0001.use1.cache.amazonaws.com:6379
- **Connection String:** redis://ai-wb-redis.xfshub.0001.use1.cache.amazonaws.com:6379

---

## 4. Storage

### S3 Buckets

**Sites Bucket**
- **Name:** ai-wb-sites-959545103699
- **Region:** us-east-1
- **Versioning:** Enabled
- **Public Access:** Blocked (all)
- **Purpose:** Store generated website files

**Assets Bucket**
- **Name:** ai-wb-assets-959545103699
- **Region:** us-east-1
- **Versioning:** Disabled
- **Public Access:** Blocked (all)
- **Purpose:** Store user-uploaded assets (images, videos, etc.)

**Templates Bucket**
- **Name:** ai-wb-templates-959545103699
- **Region:** us-east-1
- **Versioning:** Disabled
- **Public Access:** Blocked (all)
- **Purpose:** Store website templates

### DynamoDB Tables

**Page Views Table**
- **Table Name:** ai-wb-page-views
- **Status:** ACTIVE
- **Partition Key:** site_id (String)
- **Sort Key:** timestamp_visitor (String)
- **Billing Mode:** PAY_PER_REQUEST
- **TTL:** Enabled (attribute: ttl)
- **Table ARN:** arn:aws:dynamodb:us-east-1:959545103699:table/ai-wb-page-views
- **Purpose:** Store individual page view events

**Page View Daily Aggregates Table**
- **Table Name:** ai-wb-page-view-daily
- **Status:** ACTIVE
- **Partition Key:** site_id (String)
- **Sort Key:** date_page (String)
- **Billing Mode:** PAY_PER_REQUEST
- **TTL:** Not enabled
- **Table ARN:** arn:aws:dynamodb:us-east-1:959545103699:table/ai-wb-page-view-daily
- **Purpose:** Store daily aggregated page view statistics

---

## 5. Authentication

### Cognito User Pool
- **User Pool ID:** us-east-1_UkKMQIN1R
- **Name:** ai-website-builder-users
- **ARN:** arn:aws:cognito-idp:us-east-1:959545103699:userpool/us-east-1_UkKMQIN1R
- **Username Attributes:** email
- **Auto-Verified Attributes:** email
- **Custom Attributes:** custom:tenant_id (String, Mutable)
- **Password Policy:**
  - Minimum Length: 8
  - Require Uppercase: Yes
  - Require Lowercase: Yes
  - Require Numbers: Yes
  - Require Symbols: No

### Cognito App Client
- **Client ID:** 7kji0ar3m8g81pjr0fnkrpsirb
- **Client Name:** ai-wb-web-client
- **Generate Secret:** No
- **Auth Flows:**
  - ALLOW_USER_PASSWORD_AUTH
  - ALLOW_USER_SRP_AUTH
  - ALLOW_REFRESH_TOKEN_AUTH

---

## 6. DNS & Certificates

### ACM Certificate
- **Certificate ARN:** arn:aws:acm:us-east-1:959545103699:certificate/a511b177-c1c2-4c71-85f3-b148f6b6586e
- **Domain Name:** *.chinabjalex.com
- **Subject Alternative Names:** chinabjalex.com
- **Validation Method:** DNS
- **Status:** ISSUED
- **DNS Validation Record:**
  - Name: _ecdbd79b183f4fec4e9b3cbb399a964f.chinabjalex.com.
  - Type: CNAME
  - Value: _6d89eda2ef9ba271dc7e2b6195ae80b6.mhbtsbpdnt.acm-validations.aws.
  - **Added to Route 53:** Yes

### Route 53 Hosted Zone
- **Hosted Zone ID:** Z07699161LYGXX5HF4BKA
- **Domain Name:** chinabjalex.com

### Route 53 DNS Records
- **www.chinabjalex.com:** A record (alias) → CloudFront distribution d2raj73d783uqn.cloudfront.net
- **api.chinabjalex.com:** Not yet created (will point to ALB after Kubernetes deployment)

---

## 7. CDN

### CloudFront Distribution
- **Distribution ID:** E23RQWEJSVII7S
- **Status:** InProgress (deploying globally)
- **ARN:** arn:aws:cloudfront::959545103699:distribution/E23RQWEJSVII7S
- **Domain Name:** d2raj73d783uqn.cloudfront.net
- **Alternate Domain:** www.chinabjalex.com
- **Origin:** S3 bucket (ai-wb-sites-959545103699)
- **Origin Access Control ID:** E2DRFC44CN47Y2 (ai-wb-s3-oac)
- **SSL Certificate:** ACM certificate (*.chinabjalex.com)
- **SSL Support Method:** SNI
- **Default Root Object:** index.html
- **Custom Error Responses:**
  - 403 → /index.html (200) - for SPA routing
  - 404 → /index.html (200) - for SPA routing
- **Viewer Protocol Policy:** redirect-to-https
- **Compression:** Enabled
- **IPv6:** Enabled
- **Purpose:** Serve platform frontend and user-generated sites

---

## 8. IAM Roles (Pre-existing, Reused)

**EKS Cluster Role**
- **Name:** eksClusterRole
- **ARN:** arn:aws:iam::959545103699:role/eksClusterRole

**EKS Node Role**
- **Name:** eksNodeRole
- **ARN:** arn:aws:iam::959545103699:role/eksNodeRole

---

## 9. Cost Estimates (Monthly)

- **EKS Cluster:** ~$72 (control plane)
- **EKS Nodes (2x t3.large):** ~$120
- **RDS (db.t4g.medium):** ~$60
- **ElastiCache (cache.t4g.micro):** ~$12
- **S3:** Variable (depends on usage)
- **DynamoDB:** Variable (PAY_PER_REQUEST)
- **CloudFront:** Variable (depends on traffic)
- **Data Transfer:** Variable

**Estimated Total:** ~$264/month + variable costs

---

## 10. Next Steps

1. **Configure kubectl access:**
   ```bash
   aws eks update-kubeconfig --name ai-website-builder --region us-east-1
   ```

2. **Deploy Kubernetes resources:**
   - Install AWS Load Balancer Controller
   - Create ALB Ingress for API service
   - Deploy backend services (platform-api, site-generation-api, analytics-api)
   - Deploy frontend application

3. **Create api.chinabjalex.com DNS record:**
   - After ALB is created in Kubernetes, update Route 53 with A record pointing to ALB

4. **Initialize RDS database:**
   - Run Prisma migrations to create database schema
   - Seed initial data (templates, etc.)

5. **Test the platform:**
   - Verify www.chinabjalex.com resolves to CloudFront
   - Test user registration and authentication
   - Create a test website
   - Verify analytics tracking

---

## 11. Notes

- All resources are tagged with `Project=ai-website-builder`
- RDS and Redis are in private subnets and not publicly accessible
- S3 buckets have public access blocked
- Security groups follow least-privilege principle (EKS cluster SG referenced by RDS and Redis)
- ACM certificate uses DNS validation for automatic renewal
- CloudFront managed prefix list (pl-3b927c52) is used for ALB security group
- RDS master username is `dbadmin` (not `admin` which is a reserved word in PostgreSQL)
- Password is stored securely in AWS Secrets Manager
- CloudFront distribution is deploying globally (takes ~15 minutes to reach all edge locations)
- All infrastructure is production-ready and deployed in us-east-1
