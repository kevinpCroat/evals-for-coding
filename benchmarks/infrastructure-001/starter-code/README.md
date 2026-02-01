# Task Management API - Starter Code

This directory contains a simple Flask-based REST API for task management. Your job is to create the Terraform infrastructure to deploy this application to AWS.

## Application Details

**Technology:** Python Flask REST API

**Endpoints:**
- `GET /health` - Health check endpoint
- `GET /tasks` - List all tasks
- `GET /tasks/<id>` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task

**Dependencies:**
- PostgreSQL database for data storage
- S3 bucket for file attachments (referenced in code but not fully implemented)
- Environment variables for configuration

## Environment Variables

The application expects these environment variables:

```bash
DB_HOST=<RDS endpoint>
DB_PORT=5432
DB_NAME=taskdb
DB_USER=postgres
DB_PASSWORD=<from Secrets Manager>
S3_BUCKET=<bucket name>
PORT=8000
```

## Docker Image

The Dockerfile is provided. You can reference it in your Terraform code.

**Note:** For this exercise, you do NOT need to actually build or push the Docker image. You can use a placeholder ECR repository ARN in your Terraform code like:

```hcl
image = "123456789012.dkr.ecr.us-east-1.amazonaws.com/task-api:latest"
```

## Database Schema

The application automatically creates the following tables on startup:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Your Task

Create Terraform infrastructure code to deploy this application according to the requirements in `app_requirements.md`.

You do NOT need to modify this application code - it's ready to deploy. Focus on creating high-quality Infrastructure as Code.
