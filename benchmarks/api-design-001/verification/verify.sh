#!/bin/bash
# API Design Benchmark Verification Script
# Tests OpenAPI specification quality and completeness

set -e

BENCHMARK_NAME="api-design-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize scoring components
endpoints_score=0
schema_score=0
rest_score=0
docs_score=0
versioning_score=0

# Change to project directory
cd "$PROJECT_DIR"

echo -e "${YELLOW}Running API Design Benchmark Verification...${NC}" >&2

# 1. CHECK FOR REQUIRED FILES
echo -e "\n${YELLOW}1. Checking for OpenAPI specification file...${NC}" >&2

if [ ! -f "openapi.yaml" ] && [ ! -f "openapi.json" ]; then
    echo -e "${RED}ERROR: No OpenAPI spec file found (openapi.yaml or openapi.json)${NC}" >&2
    cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "error": "No OpenAPI specification file found",
  "components": {
    "required_endpoints": {"score": 0, "weight": 0.30, "details": "No spec file found"},
    "schema_completeness": {"score": 0, "weight": 0.25, "details": "No spec file found"},
    "rest_best_practices": {"score": 0, "weight": 0.25, "details": "No spec file found"},
    "documentation_quality": {"score": 0, "weight": 0.10, "details": "No spec file found"},
    "versioning_strategy": {"score": 0, "weight": 0.10, "details": "No spec file found"}
  },
  "base_score": 0,
  "penalties": {
    "time_penalty": 0,
    "iteration_penalty": 0,
    "error_penalty": 0
  },
  "final_score": 0,
  "passed": false
}
EOF
    exit 1
fi

SPEC_FILE=""
if [ -f "openapi.yaml" ]; then
    SPEC_FILE="openapi.yaml"
    echo -e "${GREEN}Found: openapi.yaml${NC}" >&2
elif [ -f "openapi.json" ]; then
    SPEC_FILE="openapi.json"
    echo -e "${GREEN}Found: openapi.json${NC}" >&2
fi

# 2. INSTALL DEPENDENCIES
echo -e "\n${YELLOW}2. Installing dependencies...${NC}" >&2

# Install Python dependencies for testing
python3 -m pip install --user -q pytest pyyaml 2>/dev/null || true

# Try to install OpenAPI validator (optional but helpful)
python3 -m pip install --user -q openapi-spec-validator 2>/dev/null || {
    echo -e "${YELLOW}Warning: openapi-spec-validator not installed, skipping strict validation${NC}" >&2
}

# 3. VALIDATE SPEC FILE FORMAT
echo -e "\n${YELLOW}3. Validating spec file format...${NC}" >&2

# Try to parse the spec file
if [[ "$SPEC_FILE" == *.yaml ]]; then
    if ! python3 -c "import yaml; yaml.safe_load(open('$SPEC_FILE'))" 2>/dev/null; then
        echo -e "${RED}ERROR: Invalid YAML format${NC}" >&2
        cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "error": "Invalid YAML format in spec file",
  "components": {
    "required_endpoints": {"score": 0, "weight": 0.30, "details": "Invalid YAML"},
    "schema_completeness": {"score": 0, "weight": 0.25, "details": "Invalid YAML"},
    "rest_best_practices": {"score": 0, "weight": 0.25, "details": "Invalid YAML"},
    "documentation_quality": {"score": 0, "weight": 0.10, "details": "Invalid YAML"},
    "versioning_strategy": {"score": 0, "weight": 0.10, "details": "Invalid YAML"}
  },
  "base_score": 0,
  "penalties": {"time_penalty": 0, "iteration_penalty": 0, "error_penalty": 0},
  "final_score": 0,
  "passed": false
}
EOF
        exit 1
    fi
else
    if ! python3 -c "import json; json.load(open('$SPEC_FILE'))" 2>/dev/null; then
        echo -e "${RED}ERROR: Invalid JSON format${NC}" >&2
        cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "error": "Invalid JSON format in spec file",
  "components": {
    "required_endpoints": {"score": 0, "weight": 0.30, "details": "Invalid JSON"},
    "schema_completeness": {"score": 0, "weight": 0.25, "details": "Invalid JSON"},
    "rest_best_practices": {"score": 0, "weight": 0.25, "details": "Invalid JSON"},
    "documentation_quality": {"score": 0, "weight": 0.10, "details": "Invalid JSON"},
    "versioning_strategy": {"score": 0, "weight": 0.10, "details": "Invalid JSON"}
  },
  "base_score": 0,
  "penalties": {"time_penalty": 0, "iteration_penalty": 0, "error_penalty": 0},
  "final_score": 0,
  "passed": false
}
EOF
        exit 1
    fi
fi

echo -e "${GREEN}Spec file format is valid${NC}" >&2

# 4. RUN AUTOMATED TESTS
echo -e "\n${YELLOW}4. Running automated tests...${NC}" >&2

# Run pytest and capture results
if python3 -m pytest "$SCRIPT_DIR/tests/test_openapi_spec.py" -v --tb=short > test_results.txt 2>&1; then
    all_tests_passed=true
else
    all_tests_passed=false
fi

# Parse test results
total_tests=$(grep -c "PASSED\|FAILED" test_results.txt || echo "0")
passed_tests=$(grep -c "PASSED" test_results.txt || echo "0")
failed_tests=$(grep -c "FAILED" test_results.txt || echo "0")

echo -e "${GREEN}Tests completed: ${passed_tests} passed, ${failed_tests} failed${NC}" >&2

# 5. CALCULATE COMPONENT SCORES

# Score based on test categories
# We'll parse the test results to get scores per category

# Helper function to count tests in a class
count_tests_for_class() {
    local class_name=$1
    local passed=$(grep "test_openapi_spec.py::${class_name}" test_results.txt | grep -c "PASSED" || echo "0")
    local total=$(grep -c "test_openapi_spec.py::${class_name}" test_results.txt || echo "0")
    if [ $total -eq 0 ]; then
        echo "0"
    else
        python3 -c "print(int(($passed / $total) * 100))"
    fi
}

# REQUIRED ENDPOINTS (30% weight)
echo -e "\n${YELLOW}5. Scoring required endpoints...${NC}" >&2

endpoints_passed=$(grep "TestRequiredEndpoints" test_results.txt | grep -c "PASSED")
endpoints_total=$(grep "TestRequiredEndpoints" test_results.txt | grep -c -E "PASSED|FAILED")
if [ -z "$endpoints_total" ] || [ "$endpoints_total" -eq 0 ]; then
    endpoints_score=0
    endpoints_total=0
else
    endpoints_score=$(python3 -c "print(int(($endpoints_passed / $endpoints_total) * 100))")
fi
endpoints_details="Passed ${endpoints_passed}/${endpoints_total} endpoint coverage tests"

echo "  Required Endpoints: ${endpoints_score}/100 (${endpoints_passed}/${endpoints_total} tests)" >&2

# SCHEMA COMPLETENESS (25% weight)
echo -e "\n${YELLOW}6. Scoring schema completeness...${NC}" >&2

schema_passed=$(grep "TestSchemaDefinitions" test_results.txt | grep -c "PASSED")
schema_total=$(grep "TestSchemaDefinitions" test_results.txt | grep -c -E "PASSED|FAILED")
if [ -z "$schema_total" ] || [ "$schema_total" -eq 0 ]; then
    schema_score=0
    schema_total=0
else
    schema_score=$(python3 -c "print(int(($schema_passed / $schema_total) * 100))")
fi
schema_details="Passed ${schema_passed}/${schema_total} schema completeness tests"

echo "  Schema Completeness: ${schema_score}/100 (${schema_passed}/${schema_total} tests)" >&2

# REST BEST PRACTICES (25% weight)
echo -e "\n${YELLOW}7. Scoring REST best practices...${NC}" >&2

# Combine HTTP methods, status codes, and best practices tests
methods_passed=$(grep "TestHTTPMethods" test_results.txt | grep -c "PASSED")
methods_total=$(grep "TestHTTPMethods" test_results.txt | grep -c -E "PASSED|FAILED")

status_passed=$(grep "TestStatusCodes" test_results.txt | grep -c "PASSED")
status_total=$(grep "TestStatusCodes" test_results.txt | grep -c -E "PASSED|FAILED")

practices_passed=$(grep "TestRESTBestPractices" test_results.txt | grep -c "PASSED")
practices_total=$(grep "TestRESTBestPractices" test_results.txt | grep -c -E "PASSED|FAILED")

rest_total=$((methods_total + status_total + practices_total))
rest_passed=$((methods_passed + status_passed + practices_passed))

if [ -z "$rest_total" ] || [ "$rest_total" -eq 0 ]; then
    rest_score=0
    rest_total=0
else
    rest_score=$(python3 -c "print(int(($rest_passed / $rest_total) * 100))")
fi

rest_details="Passed ${rest_passed}/${rest_total} REST practice tests (methods: ${methods_passed}/${methods_total}, status: ${status_passed}/${status_total}, practices: ${practices_passed}/${practices_total})"

echo "  REST Best Practices: ${rest_score}/100 (${rest_passed}/${rest_total} tests)" >&2

# DOCUMENTATION QUALITY (10% weight)
echo -e "\n${YELLOW}8. Scoring documentation quality...${NC}" >&2

docs_passed=$(grep "TestDocumentationQuality" test_results.txt | grep -c "PASSED")
docs_total=$(grep "TestDocumentationQuality" test_results.txt | grep -c -E "PASSED|FAILED")
if [ -z "$docs_total" ] || [ "$docs_total" -eq 0 ]; then
    docs_score=0
    docs_total=0
else
    docs_score=$(python3 -c "print(int(($docs_passed / $docs_total) * 100))")
fi
docs_details="Passed ${docs_passed}/${docs_total} documentation tests"

echo "  Documentation Quality: ${docs_score}/100 (${docs_passed}/${docs_total} tests)" >&2

# VERSIONING STRATEGY (10% weight)
echo -e "\n${YELLOW}9. Scoring versioning strategy...${NC}" >&2

# Check for versioning in the spec
if grep -qE "(/v1/|/v2/|/api/v1/)" "$SPEC_FILE"; then
    versioning_score=100
    versioning_details="API versioning found in URL paths"
    echo "  ✓ API uses versioning" >&2
else
    versioning_score=0
    versioning_details="No API versioning found in URL paths"
    echo "  ✗ API does not use versioning" >&2
fi

# Check if description mentions versioning strategy
if grep -qiE "(version|deprecat|backward.compatib)" "$SPEC_FILE"; then
    if [ $versioning_score -eq 0 ]; then
        versioning_score=50
        versioning_details="Versioning mentioned in description but not in URLs"
    else
        versioning_details="$versioning_details with documentation"
    fi
fi

echo "  Versioning Strategy: ${versioning_score}/100" >&2

# Calculate base score (weighted sum)
base_score=$(python3 -c "
endpoints = $endpoints_score * 0.30
schema = $schema_score * 0.25
rest = $rest_score * 0.25
docs = $docs_score * 0.10
versioning = $versioning_score * 0.10
total = endpoints + schema + rest + docs + versioning
print(round(total, 2))
")

# No penalties in this benchmark
time_penalty=0
iteration_penalty=0
error_penalty=0

final_score=$(python3 -c "print(int($base_score))")

# Determine pass/fail (70% threshold)
if (( final_score >= 70 )); then
    passed="true"
    echo -e "\n${GREEN}PASSED${NC} - Score: ${final_score}/100" >&2
else
    passed="false"
    echo -e "\n${RED}FAILED${NC} - Score: ${final_score}/100 (need 70+)" >&2
fi

# Show some failed tests for debugging
if [ "$all_tests_passed" = false ]; then
    echo -e "\n${YELLOW}Failed tests (first 10):${NC}" >&2
    grep "FAILED" test_results.txt | head -10 >&2 || true
fi

# Output JSON
cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "components": {
    "required_endpoints": {
      "score": ${endpoints_score},
      "weight": 0.30,
      "details": "${endpoints_details}"
    },
    "schema_completeness": {
      "score": ${schema_score},
      "weight": 0.25,
      "details": "${schema_details}"
    },
    "rest_best_practices": {
      "score": ${rest_score},
      "weight": 0.25,
      "details": "${rest_details}"
    },
    "documentation_quality": {
      "score": ${docs_score},
      "weight": 0.10,
      "details": "${docs_details}"
    },
    "versioning_strategy": {
      "score": ${versioning_score},
      "weight": 0.10,
      "details": "${versioning_details}"
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

# Cleanup
rm -f test_results.txt 2>/dev/null || true

# Exit with appropriate code
if [ "$passed" = "true" ]; then
    exit 0
else
    exit 1
fi
