#!/bin/bash
# Infrastructure-001 Benchmark Verification Script
# Tests Terraform IaC quality for AWS deployment

set -e

BENCHMARK_NAME="infrastructure-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TERRAFORM_DIR="${BENCHMARK_DIR}/terraform"
WORK_DIR=$(pwd)

# Initialize scoring components
validation_score=0
validation_weight=0.30
validation_details=""

plan_success_score=0
plan_success_weight=0.40
plan_success_details=""

idempotency_score=0
idempotency_weight=0.15
idempotency_details=""

security_score=0
security_weight=0.15
security_details=""

# Helper function to check if terraform directory exists
check_terraform_directory() {
    if [ ! -d "$TERRAFORM_DIR" ]; then
        echo "ERROR: terraform/ directory not found at $TERRAFORM_DIR" >&2
        return 1
    fi

    # Check for at least one .tf file
    if ! ls "$TERRAFORM_DIR"/*.tf >/dev/null 2>&1; then
        echo "ERROR: No .tf files found in $TERRAFORM_DIR" >&2
        return 1
    fi

    return 0
}

# Component 1: Terraform Validation (30%)
test_validation() {
    echo "=== Testing Terraform Validation ===" >&2
    local score=0
    local details=""

    cd "$TERRAFORM_DIR"

    # Check for terraform installation
    if ! command -v terraform &> /dev/null; then
        details="Terraform not installed"
        validation_score=0
        validation_details="$details"
        echo "FAIL: Terraform not installed" >&2
        cd "$WORK_DIR"
        return 1
    fi

    # Initialize terraform
    echo "Running terraform init..." >&2
    if terraform init -backend=false > /tmp/tf_init.log 2>&1; then
        score=$((score + 40))
        details="${details}Terraform init: PASS. "
        echo "  terraform init: PASS" >&2
    else
        details="${details}Terraform init: FAIL. "
        echo "  terraform init: FAIL" >&2
        cat /tmp/tf_init.log >&2
        validation_score=$score
        validation_details="$details"
        cd "$WORK_DIR"
        return 1
    fi

    # Validate terraform configuration
    echo "Running terraform validate..." >&2
    if terraform validate > /tmp/tf_validate.log 2>&1; then
        score=$((score + 60))
        details="${details}Terraform validate: PASS."
        echo "  terraform validate: PASS" >&2
    else
        details="${details}Terraform validate: FAIL."
        echo "  terraform validate: FAIL" >&2
        cat /tmp/tf_validate.log >&2
    fi

    validation_score=$score
    validation_details="$details"

    cd "$WORK_DIR"
    return 0
}

# Component 2: Plan Success (40%)
test_plan_success() {
    echo "=== Testing Terraform Plan Success ===" >&2
    local score=0
    local details=""

    cd "$TERRAFORM_DIR"

    # Run terraform plan
    echo "Running terraform plan..." >&2
    if terraform plan -out=/tmp/tfplan > /tmp/tf_plan.log 2>&1; then
        score=$((score + 50))
        details="${details}Plan execution: PASS. "
        echo "  terraform plan: PASS" >&2

        # Check if plan output indicates resources will be created
        local resources_to_add=$(grep -E "Plan:|to add" /tmp/tf_plan.log | grep -oE "[0-9]+ to add" | grep -oE "[0-9]+" || echo "0")

        if [ "$resources_to_add" -gt 0 ]; then
            score=$((score + 25))
            details="${details}Resources defined: $resources_to_add resources. "
            echo "  Resources to create: $resources_to_add" >&2
        else
            details="${details}No resources defined. "
            echo "  WARNING: No resources to create" >&2
        fi

        # Check for required resource types
        local found_count=0
        grep -q "aws_vpc" "$TERRAFORM_DIR"/*.tf 2>/dev/null && found_count=$((found_count + 1))
        grep -q "aws_ecs_cluster" "$TERRAFORM_DIR"/*.tf 2>/dev/null && found_count=$((found_count + 1))
        grep -q "aws_db_instance" "$TERRAFORM_DIR"/*.tf 2>/dev/null && found_count=$((found_count + 1))
        grep -q "aws_s3_bucket" "$TERRAFORM_DIR"/*.tf 2>/dev/null && found_count=$((found_count + 1))
        grep -q "aws_lb" "$TERRAFORM_DIR"/*.tf 2>/dev/null && found_count=$((found_count + 1))
        grep -q "aws_security_group" "$TERRAFORM_DIR"/*.tf 2>/dev/null && found_count=$((found_count + 1))

        if [ $found_count -ge 5 ]; then
            score=$((score + 25))
            details="${details}Required resources: $found_count/6 found."
            echo "  Required resource types: $found_count/6 found" >&2
        else
            details="${details}Required resources: only $found_count/6 found."
            echo "  WARNING: Only $found_count/6 required resource types found" >&2
        fi

    else
        details="${details}Plan execution: FAIL."
        echo "  terraform plan: FAIL" >&2
        cat /tmp/tf_plan.log >&2
    fi

    plan_success_score=$score
    plan_success_details="$details"

    cd "$WORK_DIR"
    return 0
}

# Component 3: Idempotency (15%)
test_idempotency() {
    echo "=== Testing Idempotency ===" >&2
    local score=0
    local details=""

    cd "$TERRAFORM_DIR"

    # First plan should already be done in test_plan_success
    # Run second plan
    echo "Running second terraform plan to check idempotency..." >&2
    if terraform plan > /tmp/tf_plan2.log 2>&1; then
        # Check if plan shows 0 changes
        if grep -q "No changes" /tmp/tf_plan2.log || grep -q "0 to add, 0 to change, 0 to destroy" /tmp/tf_plan2.log; then
            score=100
            details="Second plan shows 0 changes (idempotent)."
            echo "  Idempotency: PASS (0 changes)" >&2
        else
            # Check for non-zero changes
            local changes=$(grep -E "to add|to change|to destroy" /tmp/tf_plan2.log | tail -1)
            details="Second plan shows changes: $changes (not idempotent)."
            echo "  Idempotency: FAIL - $changes" >&2
            score=0
        fi
    else
        details="Second plan failed to execute."
        echo "  Idempotency test: FAIL (plan error)" >&2
        score=0
    fi

    idempotency_score=$score
    idempotency_details="$details"

    cd "$WORK_DIR"
    return 0
}

# Component 4: Security (15%)
test_security() {
    echo "=== Testing Security ===" >&2
    local score=100
    local details=""
    local issues=0

    cd "$TERRAFORM_DIR"

    # Check for hardcoded secrets/passwords
    echo "Checking for hardcoded secrets..." >&2
    if grep -rE "(password|secret|api[_-]?key)\s*=\s*[\"'][^\"'\$]" *.tf 2>/dev/null | grep -v "random_password" | grep -v "aws_secretsmanager" | grep -q .; then
        score=$((score - 30))
        issues=$((issues + 1))
        details="${details}Hardcoded secrets found. "
        echo "  WARNING: Possible hardcoded secrets detected" >&2
    else
        details="${details}No hardcoded secrets. "
        echo "  No hardcoded secrets: PASS" >&2
    fi

    # Check for overly permissive security groups (0.0.0.0/0 on all ports)
    echo "Checking for overly permissive security groups..." >&2
    if grep -rE "cidr_blocks.*=.*\[.*\"0\.0\.0\.0/0\".*\]" *.tf 2>/dev/null | grep -v "443" | grep -v "80" | grep -q .; then
        # Check if it's for ALB (acceptable) or other resources (not acceptable)
        if grep -rE "cidr_blocks.*=.*\[.*\"0\.0\.0\.0/0\".*\]" *.tf 2>/dev/null | grep -v "443" | grep -v "80" | grep -v "alb\|load_balancer" | grep -q .; then
            score=$((score - 25))
            issues=$((issues + 1))
            details="${details}Overly permissive security group rules. "
            echo "  WARNING: Overly permissive security group rules (0.0.0.0/0 on non-HTTP/HTTPS)" >&2
        fi
    fi

    # Check for Secrets Manager usage
    echo "Checking for Secrets Manager..." >&2
    if grep -q "aws_secretsmanager_secret" *.tf 2>/dev/null; then
        details="${details}Secrets Manager used. "
        echo "  Secrets Manager usage: PASS" >&2
    else
        score=$((score - 20))
        issues=$((issues + 1))
        details="${details}Secrets Manager not used. "
        echo "  WARNING: Secrets Manager not found" >&2
    fi

    # Check for S3 encryption
    echo "Checking for S3 encryption..." >&2
    if grep -q "aws_s3_bucket" *.tf 2>/dev/null; then
        if grep -rE "server_side_encryption|sse_algorithm" *.tf 2>/dev/null | grep -q .; then
            details="${details}S3 encryption enabled. "
            echo "  S3 encryption: PASS" >&2
        else
            score=$((score - 15))
            issues=$((issues + 1))
            details="${details}S3 encryption not configured. "
            echo "  WARNING: S3 encryption not found" >&2
        fi
    fi

    # Check for IAM roles (basic check)
    echo "Checking for IAM roles..." >&2
    if grep -q "aws_iam_role" *.tf 2>/dev/null; then
        details="${details}IAM roles defined. "
        echo "  IAM roles: PASS" >&2
    else
        score=$((score - 10))
        issues=$((issues + 1))
        details="${details}IAM roles not found. "
        echo "  WARNING: IAM roles not found" >&2
    fi

    if [ $score -lt 0 ]; then
        score=0
    fi

    security_score=$score
    security_details="${details}Issues found: $issues."

    cd "$WORK_DIR"
    return 0
}

# Main execution
echo "Running verification for ${BENCHMARK_NAME}..." >&2
echo "Benchmark directory: $BENCHMARK_DIR" >&2
echo "Terraform directory: $TERRAFORM_DIR" >&2
echo "" >&2

# Check if terraform directory exists
if ! check_terraform_directory; then
    # Output JSON even on catastrophic failure
    cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "components": {
    "validation": {"score": 0, "weight": 0.30, "details": "Terraform directory or files not found"},
    "plan_success": {"score": 0, "weight": 0.40, "details": "Terraform directory or files not found"},
    "idempotency": {"score": 0, "weight": 0.15, "details": "Terraform directory or files not found"},
    "security": {"score": 0, "weight": 0.15, "details": "Terraform directory or files not found"}
  },
  "base_score": 0,
  "penalties": {
    "time_penalty": 0.0,
    "iteration_penalty": 0.0,
    "error_penalty": 0.0
  },
  "final_score": 0,
  "passed": false
}
EOF
    exit 1
fi

# Run all tests
test_validation
test_plan_success
test_idempotency
test_security

# Calculate base score
base_score=$(echo "$validation_score * $validation_weight + $plan_success_score * $plan_success_weight + $idempotency_score * $idempotency_weight + $security_score * $security_weight" | bc -l)
base_score=$(printf "%.0f" "$base_score")

# Calculate penalties (these would come from execution metadata in real usage)
time_penalty=0
iteration_penalty=0
error_penalty=0

# Calculate final score
penalty_multiplier=$(echo "1.0 - ($time_penalty + $iteration_penalty + $error_penalty)" | bc -l)
final_score=$(echo "$base_score * $penalty_multiplier" | bc -l)
final_score=$(printf "%.0f" "$final_score")

# Determine pass/fail
passed="false"
if [ $final_score -ge 70 ]; then
  passed="true"
fi

# Build JSON output
cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "components": {
    "validation": {
      "score": ${validation_score},
      "weight": ${validation_weight},
      "details": "${validation_details}"
    },
    "plan_success": {
      "score": ${plan_success_score},
      "weight": ${plan_success_weight},
      "details": "${plan_success_details}"
    },
    "idempotency": {
      "score": ${idempotency_score},
      "weight": ${idempotency_weight},
      "details": "${idempotency_details}"
    },
    "security": {
      "score": ${security_score},
      "weight": ${security_weight},
      "details": "${security_details}"
    }
  },
  "base_score": ${base_score},
  "penalties": {
    "time_penalty": ${time_penalty},
    "iteration_penalty": ${iteration_penalty},
    "error_penalty": ${error_penalty}
  },
  "final_score": ${final_score},
  "passed": ${passed}
}
EOF

# Exit with appropriate code
if [ "$passed" = "true" ]; then
  exit 0
else
  exit 1
fi
