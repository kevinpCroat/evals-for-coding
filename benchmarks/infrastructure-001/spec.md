# Infrastructure as Code Benchmark - Specification

## Objective

Write production-quality Terraform code to deploy a containerized Flask application to AWS with all necessary infrastructure including networking, compute, database, storage, and security components.

## Background

You have been given a Task Management API (a simple Flask REST application) that needs to be deployed to AWS. The application code is complete and ready to deploy - your job is to create all the Infrastructure as Code (IaC) needed to run it in production.

This benchmark tests your ability to:
- Design cloud infrastructure architecture
- Write clean, maintainable Terraform code
- Implement security best practices
- Configure networking and load balancing
- Manage secrets and credentials properly
- Ensure high availability and scalability

## Requirements

### Functional Requirements

1. **Review Application Requirements**
   - Read `app_requirements.md` for detailed infrastructure specifications
   - Review `starter-code/` to understand the application architecture

2. **Create Terraform Infrastructure Code**
   - Write Terraform (.tf files) to provision all required AWS resources
   - Organize code into logical modules or files
   - Use Terraform 1.5+ compatible syntax

3. **Implement All Required Components**
   - VPC with public and private subnets across 2 AZs
   - Application Load Balancer for traffic distribution
   - ECS Fargate service for containerized application
   - RDS PostgreSQL database with multi-AZ
   - S3 bucket for static file storage
   - Security groups with least privilege access
   - IAM roles and policies
   - CloudWatch logging and basic alarms
   - Secrets Manager for database credentials

4. **Follow Infrastructure Best Practices**
   - Use variables for configurable values
   - Output important resource identifiers
   - Add proper resource dependencies
   - Tag all resources consistently
   - Use meaningful resource names

### Technical Constraints

- **Provider:** AWS provider only (use us-east-1 region)
- **Terraform Version:** Compatible with Terraform 1.5 or higher
- **No Hardcoded Secrets:** Database passwords and sensitive data must use Secrets Manager
- **No Manual Steps:** All infrastructure must be fully automated
- **Validation Required:** Code must pass `terraform validate`
- **Planning Required:** Code must successfully run `terraform plan`
- **Idempotency:** Running `terraform plan` twice should show zero changes
- **No Deployment:** You do NOT need to run `terraform apply` (validation and planning only)

### Quality Requirements

- Clean, readable Terraform code with proper formatting
- Descriptive variable names and comments where helpful
- Proper use of Terraform resource dependencies
- Security groups following principle of least privilege
- No overly permissive IAM policies (avoid `*` actions or resources where possible)
- Resources organized logically (e.g., separate files for networking, compute, database)

## Success Criteria

The infrastructure code will be considered successful when:

1. **Validation (30%)** - `terraform validate` passes without errors
2. **Planning (40%)** - `terraform plan` executes successfully without errors
3. **Idempotency (15%)** - Second `terraform plan` shows 0 resources to add/change/destroy
4. **Security (15%)** - No hardcoded secrets, proper IAM roles, security group rules follow least privilege

## Deliverables

Create your Terraform code in a `terraform/` directory with the following structure:

```
terraform/
├── main.tf              # Main resource definitions or module composition
├── variables.tf         # Input variable declarations
├── outputs.tf           # Output value definitions
├── providers.tf         # Provider configuration
├── vpc.tf              # VPC and networking resources (optional - can be in main.tf)
├── ecs.tf              # ECS cluster and service (optional - can be in main.tf)
├── rds.tf              # Database resources (optional - can be in main.tf)
├── security.tf         # Security groups and IAM (optional - can be in main.tf)
├── terraform.tfvars    # Variable values (optional)
└── README.md           # Instructions for running the code
```

**Note:** The file organization above is a suggestion. You can organize your Terraform code however you prefer, as long as it's logical and maintainable. You could put everything in `main.tf`, split by service, or use modules - any approach is acceptable.

### Required Resources

Your Terraform code must create these AWS resources (at minimum):

**Networking:**
- VPC with appropriate CIDR block
- Internet Gateway
- NAT Gateway (at least 1)
- Public subnets (2) across 2 AZs
- Private subnets (2) across 2 AZs
- Route tables and associations

**Compute:**
- ECS Cluster
- ECS Task Definition (Fargate)
- ECS Service with desired count of 2
- Application Load Balancer
- ALB Target Group
- ALB Listener(s)

**Database:**
- RDS PostgreSQL instance
- RDS subnet group
- Random password generation for database (stored in Secrets Manager)

**Storage:**
- S3 bucket with versioning and encryption

**Security:**
- Security group for ALB
- Security group for ECS tasks
- Security group for RDS
- IAM role for ECS task execution
- IAM role for ECS tasks
- Secrets Manager secret for database credentials

**Monitoring:**
- CloudWatch log group for ECS
- CloudWatch alarms (at least 2-3 basic alarms)

**Optional but Recommended:**
- Route53 zone and records (if implementing DNS)
- ACM certificate (can be mocked/placeholder)
- Additional CloudWatch alarms
- Auto-scaling policies for ECS

### terraform/README.md

Include a README with:

```markdown
# Task Management API - Terraform Infrastructure

## Overview
Brief description of what this Terraform code deploys.

## Prerequisites
- Terraform 1.5+
- AWS CLI configured (for actual deployment, not required for this exercise)

## Usage

### Initialize Terraform
\`\`\`bash
terraform init
\`\`\`

### Validate Configuration
\`\`\`bash
terraform validate
\`\`\`

### Plan Infrastructure
\`\`\`bash
terraform plan
\`\`\`

### Apply (DO NOT RUN for this exercise)
\`\`\`bash
terraform apply
\`\`\`

## Architecture
Brief description of the infrastructure architecture.

## Variables
List of important variables and their defaults.

## Outputs
List of outputs provided after apply.
```

## Evaluation

Your submission will be scored on:

- **IaC Validation (30%)**:
  - `terraform validate` passes
  - Proper syntax and resource definitions
  - Correct provider configuration

- **Plan Success (40%)**:
  - `terraform plan` executes without errors
  - All required resources are defined
  - Dependencies are correctly configured
  - Resource attributes are valid

- **Idempotency (15%)**:
  - Running `terraform plan` a second time shows 0 changes
  - No random or timestamp values in resource names
  - Proper use of lifecycle rules where needed

- **Security (15%)**:
  - No hardcoded secrets or passwords
  - Database credentials in Secrets Manager
  - Security groups use specific ports and sources (not 0.0.0.0/0 for everything)
  - IAM policies avoid overly broad permissions
  - S3 bucket has encryption enabled
  - Resources follow principle of least privilege

See `verification/verify.sh` for automated scoring implementation.

## Important Notes

- **No Actual Deployment Required:** You do NOT need to run `terraform apply` or deploy to real AWS
- **Placeholder Values:** You can use placeholder ECR image ARNs, domain names, etc.
- **Focus on Quality:** Write production-quality code as if this will be used by a real team
- **Security Matters:** Treat this as production infrastructure - no shortcuts on security
- **Documentation:** Add comments where helpful, especially for complex logic
- **Testing:** Run `terraform validate` and `terraform plan` locally before submitting

## Getting Started

1. Read `app_requirements.md` to understand all infrastructure requirements
2. Review the application code in `starter-code/` to understand what it needs
3. Create a `terraform/` directory for your infrastructure code
4. Start with basic structure (providers, VPC, basic compute)
5. Add database, storage, security, and monitoring incrementally
6. Test with `terraform validate` and `terraform plan` frequently
7. Ensure idempotency by running plan twice
8. Run `./verification/verify.sh` to check your score

## Common Pitfalls to Avoid

- Hardcoding sensitive values (use Secrets Manager)
- Overly permissive security groups (0.0.0.0/0 for all ports)
- Missing resource dependencies (e.g., ALB depends on subnets)
- Non-idempotent resource names (using timestamps)
- Missing required tags
- Incorrect subnet types (public vs private)
- Forgetting NAT Gateway for private subnet internet access
- Not specifying container port mappings in ECS task definition

## Verification

Run the verification script to check your implementation:

```bash
cd /path/to/infrastructure-001
./verification/verify.sh
```

The script will:
1. Check that terraform code exists
2. Run `terraform init` and `terraform validate`
3. Run `terraform plan` and check for errors
4. Run `terraform plan` again to verify idempotency
5. Scan code for security issues (hardcoded secrets, overly permissive rules)
6. Output a JSON score report
