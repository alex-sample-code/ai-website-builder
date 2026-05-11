# AI Website Builder - Deployment Status

**Date:** 2026-05-11
**Environment:** Production
**Status:** ✅ Deployed Successfully

---

## Deployment Summary

The AI Website Builder has been successfully deployed to Amazon EKS with full integration across all AWS services.

### Infrastructure Deployed

- **EKS Cluster:** ai-website-builder (Kubernetes 1.31)
  - 2x t3.large nodes
  - AWS Load Balancer Controller installed
  - IRSA (IAM Roles for Service Accounts) configured

- **Container Images:**
  - Backend: `959545103699.dkr.ecr.us-east-1.amazonaws.com/ai-website-builder/backend:latest`
  - Frontend: `959545103699.dkr.ecr.us-east-1.amazonaws.com/ai-website-builder/frontend:latest`

- **Kubernetes Resources:**
  - Namespace: `ai-website-builder`
  - Backend Deployment: 2 replicas
  - Frontend Deployment: 2 replicas
  - Services: ClusterIP for internal communication
  - Ingress: ALB for external access

- **Application Load Balancer:**
  - Name: `k8s-aiwebsit-aiwbingr-deb1f97fcf`
  - DNS: `k8s-aiwebsit-aiwbingr-deb1f97fcf-888035372.us-east-1.elb.amazonaws.com`
  - Certificate: ACM wildcard certificate (*.chinabjalex.com)
  - Security Group: sg-0889572eb6e1239a0

---

## DNS Configuration

### Route 53 Records Created

- **api.chinabjalex.com** → ALB (alias record)
- **www.chinabjalex.com** → CloudFront distribution (existing)

---

## Database & Cache

- **PostgreSQL Database:**
  - Tables created via Alembic migration
  - SSL/TLS enabled for secure connections
  - Connection pooling configured

- **Redis Cache:**
  - Connected and accessible from pods
  - Used for session management and caching

---

## Application URLs

- **Frontend:** https://www.chinabjalex.com
- **API:** https://api.chinabjalex.com
- **Health Check:** https://api.chinabjalex.com/health
- **API Docs (dev only):** Disabled in production

---

## Environment Configuration

All environment variables are configured via Kubernetes ConfigMaps and Secrets:

- **ConfigMap:** ai-wb-config
  - AWS region, account ID
  - S3 bucket names
  - DynamoDB table names
  - Cognito pool and client IDs
  - CloudFront distribution ID
  - Bedrock model configuration
  - SES sender email

- **Secret:** ai-wb-secrets
  - PostgreSQL database URL (with SSL)
  - Redis connection URL

---

## IAM Permissions

**Service Account:** ai-wb-service-account
**IAM Role:** Configured via IRSA

**Permissions Granted:**
- S3: Full access to sites, assets, and templates buckets
- Bedrock: InvokeModel and InvokeModelWithResponseStream
- DynamoDB: Full access to page views tables
- SES: SendEmail and SendRawEmail
- Secrets Manager: GetSecretValue for ai-wb/* secrets
- Cognito: Full access to user pool
- CloudFront: CreateInvalidation, GetInvalidation, ListInvalidations

---

## Security Configuration

- **SSL/TLS:**
  - ALB terminates SSL with ACM certificate
  - Backend pods communicate over HTTP internally
  - RDS connections use SSL (sslmode=require)

- **Network Security:**
  - Backend and frontend in private subnets
  - RDS accessible only from EKS cluster security group
  - Redis accessible only from EKS cluster security group
  - ALB security group allows traffic from CloudFront

- **Application Security:**
  - TrustedHostMiddleware enabled for production
  - CORS configured for specific origins
  - Health check endpoints with proper Host headers

---

## Monitoring & Health Checks

- **Liveness Probe:** /health endpoint (30s delay, 10s period)
- **Readiness Probe:** /health endpoint (10s delay, 5s period)
- **Resource Limits:**
  - Backend: 256Mi-512Mi memory, 250m-500m CPU
  - Frontend: 128Mi-256Mi memory, 100m-250m CPU

---

## Deployment Commands

### View Resources
```bash
kubectl get all -n ai-website-builder
kubectl get ingress -n ai-website-builder
```

### View Logs
```bash
kubectl logs -n ai-website-builder deployment/backend
kubectl logs -n ai-website-builder deployment/frontend
```

### Run Database Migration
```bash
kubectl exec -n ai-website-builder deployment/backend -- alembic upgrade head
```

### Restart Deployments
```bash
kubectl rollout restart deployment/backend -n ai-website-builder
kubectl rollout restart deployment/frontend -n ai-website-builder
```

### Update Docker Images
```bash
# Backend
cd backend
sudo docker build -t ai-website-builder/backend:latest .
sudo docker tag ai-website-builder/backend:latest 959545103699.dkr.ecr.us-east-1.amazonaws.com/ai-website-builder/backend:latest
aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 959545103699.dkr.ecr.us-east-1.amazonaws.com
sudo docker push 959545103699.dkr.ecr.us-east-1.amazonaws.com/ai-website-builder/backend:latest
kubectl rollout restart deployment/backend -n ai-website-builder

# Frontend
cd frontend
sudo docker build --build-arg VITE_API_URL=https://api.chinabjalex.com -t ai-website-builder/frontend:latest .
sudo docker tag ai-website-builder/frontend:latest 959545103699.dkr.ecr.us-east-1.amazonaws.com/ai-website-builder/frontend:latest
sudo docker push 959545103699.dkr.ecr.us-east-1.amazonaws.com/ai-website-builder/frontend:latest
kubectl rollout restart deployment/frontend -n ai-website-builder
```

---

## Verification Steps Completed

✅ EKS cluster accessible
✅ Kubectl configured
✅ ECR repositories created
✅ Docker images built and pushed
✅ Kubernetes namespace created
✅ ConfigMaps and Secrets created
✅ IRSA service account configured
✅ AWS Load Balancer Controller installed
✅ Backend deployment running (2/2 pods)
✅ Frontend deployment running (2/2 pods)
✅ Services created and accessible
✅ Ingress created with ALB
✅ Database migration completed
✅ Route 53 DNS record created
✅ Health checks passing

---

## Next Steps

1. **DNS Propagation:** Wait for api.chinabjalex.com DNS to fully propagate (may take a few minutes)
2. **Frontend Testing:** Access https://www.chinabjalex.com and verify the application loads
3. **API Testing:** Test API endpoints at https://api.chinabjalex.com
4. **User Registration:** Test Cognito authentication flow
5. **Site Creation:** Create a test website and verify S3/CloudFront deployment
6. **Analytics:** Verify DynamoDB analytics tracking
7. **Monitoring:** Set up CloudWatch dashboards for application metrics
8. **Alerts:** Configure CloudWatch alarms for critical metrics

---

## Troubleshooting

### View Pod Status
```bash
kubectl get pods -n ai-website-builder
kubectl describe pod <pod-name> -n ai-website-builder
```

### View Logs
```bash
kubectl logs -f -n ai-website-builder deployment/backend
kubectl logs -f -n ai-website-builder deployment/frontend
```

### Check Ingress
```bash
kubectl describe ingress -n ai-website-builder
```

### Test Health Endpoint
```bash
kubectl exec -n ai-website-builder deployment/backend -- curl http://localhost:8000/health
```

---

## Cost Estimate

**Monthly Costs (Production):**
- EKS Control Plane: ~$72
- EKS Nodes (2x t3.large): ~$120
- ALB: ~$20
- RDS (db.t4g.medium): ~$60
- ElastiCache (cache.t4g.micro): ~$12
- S3 Storage: Variable
- CloudFront Data Transfer: Variable
- DynamoDB (PAY_PER_REQUEST): Variable

**Total Fixed Costs:** ~$284/month + variable

---

## Deployment Complete! 🎉

The AI Website Builder is now live and ready for use.
