# Application Deployment Requirements

## Application Overview

You are deploying a **Task Management API** - a RESTful web service built with Python Flask that allows users to create, read, update, and delete tasks. The application needs to be deployed to AWS with proper infrastructure.

## Application Details

**Technology Stack:**
- Backend: Python 3.11 with Flask
- Database: PostgreSQL
- Static Assets: User profile images and task attachments

**Application Components:**
- `app.py` - Main Flask application with REST API endpoints
- `requirements.txt` - Python dependencies
- Database schema for tasks and users

## Infrastructure Requirements

### 1. Compute

**Primary Application Server:**
- Deploy the Flask application as a containerized service
- Use AWS ECS with Fargate (serverless containers)
- Minimum 2 tasks for high availability
- Auto-scaling: 2-10 tasks based on CPU utilization (target 70%)
- Container specs: 512 MB memory, 0.25 vCPU per task

**Alternative:** EC2 instances are acceptable but ECS/Fargate preferred for simplicity

### 2. Database

**PostgreSQL Database:**
- AWS RDS PostgreSQL 15.x
- Instance class: db.t3.micro (for development/testing)
- Storage: 20 GB general purpose SSD (gp3)
- Multi-AZ deployment for high availability
- Automated backups: 7-day retention
- Database name: `taskdb`
- Port: 5432

**Security:**
- Database credentials must NOT be hardcoded
- Use AWS Secrets Manager or Parameter Store for database password
- Database should only be accessible from application security group

### 3. Storage

**S3 Bucket for Static Assets:**
- Bucket for user uploads (profile images, task attachments)
- Versioning enabled
- Server-side encryption (AES-256)
- Lifecycle policy: Delete objects after 90 days in "archived" prefix
- Block public access (application accesses via IAM role)

### 4. Networking

**VPC Configuration:**
- VPC CIDR: 10.0.0.0/16
- Two public subnets (for ALB): 10.0.1.0/24, 10.0.2.0/24
- Two private subnets (for app/database): 10.0.10.0/24, 10.0.11.0/24
- Subnets should span 2 availability zones
- Internet Gateway for public subnets
- NAT Gateway for private subnet outbound access
- Proper route tables for public and private subnets

**Application Load Balancer:**
- Internet-facing ALB in public subnets
- HTTPS listener on port 443 (with HTTP redirect from port 80)
- Health check: GET /health endpoint (expect 200 OK)
- Target group pointing to ECS service

**Security Groups:**
- ALB Security Group: Allow inbound 80/443 from 0.0.0.0/0, outbound to app SG
- Application Security Group: Allow inbound from ALB SG on container port (8000), outbound to DB SG
- Database Security Group: Allow inbound 5432 from app SG only
- All security groups should have descriptive names and follow principle of least privilege

### 5. Security & IAM

**IAM Roles:**
- ECS Task Execution Role: For pulling container images from ECR
- ECS Task Role: For application to access S3 and Secrets Manager
- Both roles should follow principle of least privilege

**Secrets Management:**
- Database password stored in AWS Secrets Manager
- Application retrieves credentials at runtime
- No credentials in environment variables or code

### 6. Monitoring & Logging

**CloudWatch:**
- Log group for ECS container logs
- Log retention: 7 days
- Alarms for:
  - RDS CPU > 80%
  - ECS service task count < 2
  - ALB 5xx errors > 10 per 5 minutes

### 7. Additional Requirements

**DNS (Optional but Recommended):**
- Route 53 hosted zone (if implementing)
- A record pointing to ALB

**SSL Certificate:**
- Use AWS ACM for SSL certificate
- Can use self-signed for this exercise or reference a domain

**Tags:**
- All resources should be tagged with:
  - Environment: "development"
  - Project: "task-management-api"
  - ManagedBy: "terraform"

## Deployment Constraints

1. **No Manual Steps:** All infrastructure must be fully automated via IaC
2. **Region:** Use `us-east-1` as the default AWS region
3. **State Management:** Terraform state can be local (no S3 backend required for this exercise)
4. **Cost Optimization:** Use smallest instance types and free tier where possible
5. **Idempotency:** Running terraform apply twice should result in no changes

## Success Criteria

The infrastructure is complete when:
1. `terraform validate` passes
2. `terraform plan` executes without errors
3. All resources are defined with proper dependencies
4. No secrets are hardcoded in the code
5. Security groups follow least privilege principle
6. High availability is configured (multi-AZ, multiple tasks)
7. Running `terraform plan` a second time shows 0 changes to apply

## Out of Scope

- **No Actual Deployment:** You do NOT need to run `terraform apply` or deploy to real AWS
- **No Container Registry:** You do NOT need to push Docker images to ECR
- **No Domain Registration:** Mock/placeholder domain names are acceptable
- **No CI/CD Pipeline:** Infrastructure code only, no deployment automation

## Notes

- Focus on infrastructure quality over application complexity
- The application code is provided - you focus on Terraform
- Assume the Docker image exists in ECR (use placeholder ARN)
- This is about Infrastructure as Code best practices, not application development
