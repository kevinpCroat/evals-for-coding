# Infrastructure as Code (IaC) Benchmark

This benchmark evaluates an AI's ability to write production-quality Infrastructure as Code using Terraform to deploy a containerized web application to AWS.

## Overview

**Skill Tested:** Infrastructure as Code (Terraform)
**Difficulty:** Medium
**Time Estimate:** 45-90 minutes

## What This Tests

This benchmark assesses the ability to:
- Design cloud infrastructure architecture for a real application
- Write clean, maintainable Terraform code
- Implement security best practices (secrets management, least privilege)
- Configure complex AWS services (VPC, ECS, RDS, ALB, IAM)
- Ensure infrastructure is idempotent and reproducible
- Follow IaC best practices and conventions

## The Challenge

You are given a working Flask REST API (Task Management API) and must create all the Terraform infrastructure code needed to deploy it to AWS with:

- **Networking:** VPC with public/private subnets across 2 availability zones
- **Compute:** ECS Fargate for containerized application deployment
- **Database:** RDS PostgreSQL with multi-AZ for high availability
- **Storage:** S3 bucket for file attachments
- **Load Balancing:** Application Load Balancer for traffic distribution
- **Security:** Proper security groups, IAM roles, and secrets management
- **Monitoring:** CloudWatch logs and basic alarms

The infrastructure must be:
- Fully automated (no manual steps)
- Secure (no hardcoded secrets, least privilege access)
- Idempotent (running terraform plan twice shows 0 changes)
- Production-quality (as if deploying to a real environment)

## What Makes This Realistic

Unlike toy IaC exercises, this benchmark:
- Requires orchestrating multiple interconnected AWS services
- Tests security knowledge (secrets management, security groups, IAM)
- Validates that infrastructure actually works (terraform plan must succeed)
- Checks for common mistakes (hardcoded credentials, overly permissive rules)
- Requires understanding dependencies between resources
- Tests idempotency (a critical property of good IaC)

## Files

- `spec.md` - Complete task specification and requirements
- `app_requirements.md` - Detailed infrastructure requirements for the application
- `prompts.txt` - Standardized task prompts for AI agents
- `starter-code/` - Complete Flask application code (ready to deploy)
  - `app.py` - REST API implementation
  - `Dockerfile` - Container definition
  - `requirements.txt` - Python dependencies
  - `README.md` - Application documentation
- `verification/verify.sh` - Automated scoring script

## Scoring

The submission is scored across 4 components:

### 1. IaC Validation (30%)
- Terraform code passes `terraform init`
- Terraform code passes `terraform validate`
- Proper syntax and resource definitions

### 2. Plan Success (40%)
- `terraform plan` executes without errors
- All required AWS resources are defined
- Resource dependencies are correctly configured
- At least 5/6 core resource types present (VPC, ECS, RDS, S3, ALB, Security Groups)

### 3. Idempotency (15%)
- Running `terraform plan` a second time shows 0 changes
- No random or timestamp values in resource names
- Proper use of lifecycle rules where needed

### 4. Security (15%)
- No hardcoded secrets or passwords
- Database credentials stored in AWS Secrets Manager
- Security groups follow principle of least privilege
- IAM roles and policies defined
- S3 bucket encryption enabled

**Pass Threshold:** 70% overall score

## Example Good vs Bad Approaches

### Good Approach
```hcl
# Generate random password
resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Store in Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "task-api-db-password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db_password.result
}

# Reference in RDS
resource "aws_db_instance" "main" {
  password = random_password.db_password.result
  # ... other config
}
```

### Bad Approach
```hcl
# Hardcoded password - SECURITY ISSUE
resource "aws_db_instance" "main" {
  password = "MyPassword123!"  # FAIL: Hardcoded secret
  # ... other config
}

# Overly permissive security group - SECURITY ISSUE
resource "aws_security_group_rule" "allow_all" {
  from_port   = 0
  to_port     = 65535
  cidr_blocks = ["0.0.0.0/0"]  # FAIL: Too permissive
}
```

## Running the Benchmark

### For AI Evaluation

1. Provide the AI with the contents of `prompts.txt` and access to all files
2. The AI should create a `terraform/` directory with all IaC code
3. Run the verification script:
   ```bash
   ./verification/verify.sh
   ```
4. The script outputs JSON scoring data

### For Manual Testing

1. Read `spec.md` for full requirements
2. Read `app_requirements.md` for infrastructure details
3. Review the application in `starter-code/`
4. Create `terraform/` directory with your Terraform code
5. Test locally:
   ```bash
   cd terraform/
   terraform init
   terraform validate
   terraform plan
   terraform plan  # Run again to check idempotency
   ```
6. Run verification:
   ```bash
   cd ..
   ./verification/verify.sh
   ```

## Prerequisites

- Terraform 1.5 or higher installed
- Basic understanding of:
  - Terraform syntax and concepts
  - AWS services (VPC, ECS, RDS, S3, ALB, IAM)
  - Infrastructure as Code principles
  - Container deployment concepts

**Note:** You do NOT need AWS credentials or an actual AWS account. The benchmark only validates and plans - it never runs `terraform apply`.

## Why This Matters

Infrastructure as Code is a critical skill for modern software engineering:
- **Reproducibility:** Infrastructure can be version controlled and recreated
- **Automation:** Eliminates manual configuration and human error
- **Documentation:** The code itself documents the infrastructure
- **Scaling:** Easy to replicate environments (dev, staging, prod)
- **Disaster Recovery:** Infrastructure can be rebuilt from code

This benchmark tests whether an AI can write production-quality IaC that actually works, not just syntactically correct code. The validation ensures:
- Security best practices are followed
- Infrastructure would actually deploy successfully
- Code is maintainable and follows conventions
- Common pitfalls are avoided

## Common Challenges

AIs and humans typically struggle with:
- Getting all the resource dependencies correct
- Properly configuring VPC networking (subnets, route tables, NAT gateway)
- Security group rules (what needs to talk to what)
- IAM roles and policies with correct permissions
- ECS task definitions (container configuration, environment variables)
- Idempotency issues (using timestamps or random values incorrectly)
- Secrets management (avoiding hardcoded passwords)

## Success Criteria

A passing submission demonstrates:
- Strong understanding of AWS architecture
- Ability to write clean, maintainable Terraform code
- Knowledge of security best practices
- Attention to detail in resource configuration
- Understanding of infrastructure dependencies
- Proper use of Terraform features (variables, outputs, dependencies)

## Benchmark Metadata

- **Type:** Infrastructure as Code
- **Domain:** DevOps / Cloud Engineering
- **Technologies:** Terraform, AWS, Docker, ECS
- **Automation Rate:** 100% (fully automated scoring)
- **Reproducibility:** High (deterministic validation)
- **Discrimination:** Good (tests multiple skill levels)

## Future Enhancements

Potential additions to increase difficulty:
- Multi-region deployment
- Auto-scaling policies
- CI/CD pipeline integration
- Custom VPC modules
- Terraform remote state configuration
- Advanced monitoring and alerting
- WAF and DDoS protection
- Cost optimization requirements
