#!/bin/bash
# Dependency Maintenance Benchmark Verification Script
# Outputs JSON with scoring details

set -e

BENCHMARK_NAME="maintenance-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER_CODE_DIR="$BENCHMARK_DIR/starter-code"

# Initialize scores
dependencies_updated_score=0
tests_pass_score=0
no_warnings_score=0

# Change to starter code directory
cd "$STARTER_CODE_DIR"

echo "Running verification for ${BENCHMARK_NAME}..." >&2
echo "Benchmark directory: $BENCHMARK_DIR" >&2
echo "Starter code directory: $STARTER_CODE_DIR" >&2

# Create temporary directory for test results
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Component 1: Check if dependencies are updated (40%)
echo "Checking dependency updates..." >&2

dependencies_updated_details=""

if [ ! -f "requirements.txt" ]; then
    dependencies_updated_score=0
    dependencies_updated_details="requirements.txt not found"
else
    # Check for specific minimum versions that fix security issues
    # Flask >= 2.3.0, Werkzeug >= 2.3.0, requests >= 2.31.0, pytest >= 7.0.0

    issues_fixed=0
    total_issues=0

    # Check Flask version
    total_issues=$((total_issues + 1))
    if grep -qE "^Flask==([3-9]\.|2\.[3-9]|2\.[1-9][0-9])" requirements.txt; then
        issues_fixed=$((issues_fixed + 1))
        echo "✓ Flask updated to >= 2.3.0" >&2
    else
        echo "✗ Flask not updated to >= 2.3.0" >&2
    fi

    # Check Werkzeug version
    total_issues=$((total_issues + 1))
    if grep -qE "^Werkzeug==([3-9]\.|2\.[3-9]|2\.[1-9][0-9])" requirements.txt; then
        issues_fixed=$((issues_fixed + 1))
        echo "✓ Werkzeug updated to >= 2.3.0" >&2
    else
        echo "✗ Werkzeug not updated to >= 2.3.0" >&2
    fi

    # Check requests version
    total_issues=$((total_issues + 1))
    if grep -qE "^requests==([3-9]\.|2\.(3[1-9]|[4-9][0-9]))" requirements.txt; then
        issues_fixed=$((issues_fixed + 1))
        echo "✓ requests updated to >= 2.31.0" >&2
    else
        echo "✗ requests not updated to >= 2.31.0" >&2
    fi

    # Check pytest version
    total_issues=$((total_issues + 1))
    if grep -qE "^pytest==([7-9]\.|[1-9][0-9]\.)" requirements.txt; then
        issues_fixed=$((issues_fixed + 1))
        echo "✓ pytest updated to >= 7.0.0" >&2
    else
        echo "✗ pytest not updated to >= 7.0.0" >&2
    fi

    # Calculate score based on percentage of issues fixed
    dependencies_updated_score=$((issues_fixed * 100 / total_issues))
    dependencies_updated_details="$issues_fixed of $total_issues critical dependencies updated"
fi

echo "Dependencies score: $dependencies_updated_score" >&2

# Component 2: Run tests (40%)
echo "Running test suite..." >&2

# First, check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..." >&2
    if ! python3 -m pip install -q -r requirements.txt 2>&1 | tee "$TEMP_DIR/install.log" >&2; then
        tests_pass_score=0
        tests_pass_details="Failed to install dependencies"
        echo "ERROR: Failed to install dependencies" >&2
        cat "$TEMP_DIR/install.log" >&2
    fi
fi

# Check if pytest is available
if ! command -v pytest &> /dev/null && ! python3 -m pytest --version &> /dev/null; then
    echo "ERROR: pytest is not installed after dependency installation" >&2
    tests_pass_score=0
    tests_pass_details="pytest not available"
else
    PYTEST_CMD="python3 -m pytest"

    # Run tests
    TEST_OUTPUT="$TEMP_DIR/test_output.txt"

    if $PYTEST_CMD tests/ -v --tb=short > "$TEST_OUTPUT" 2>&1; then
        ALL_TESTS_PASSED=true
        echo "All tests passed!" >&2
    else
        ALL_TESTS_PASSED=false
        echo "Some tests failed." >&2
    fi

    # Show test output
    cat "$TEST_OUTPUT" >&2

    # Parse test results
    TOTAL_TESTS=$(grep -oE "[0-9]+ passed" "$TEST_OUTPUT" | head -1 | grep -oE "[0-9]+" || echo "0")
    FAILED_TESTS=$(grep -oE "[0-9]+ failed" "$TEST_OUTPUT" | head -1 | grep -oE "[0-9]+" || echo "0")

    # Expected: at least 16 tests (2 test files with comprehensive coverage)
    if [ "$ALL_TESTS_PASSED" = true ] && [ "$TOTAL_TESTS" -ge 16 ]; then
        tests_pass_score=100
        tests_pass_details="All $TOTAL_TESTS tests pass"
    elif [ "$TOTAL_TESTS" -ge 14 ]; then
        tests_pass_score=70
        tests_pass_details="$TOTAL_TESTS tests pass, $FAILED_TESTS failed"
    else
        tests_pass_score=0
        tests_pass_details="Only $TOTAL_TESTS tests pass, $FAILED_TESTS failed"
    fi
fi

echo "Tests score: $tests_pass_score" >&2

# Component 3: Check for deprecation warnings (20%)
echo "Checking for deprecation warnings..." >&2

if [ "$tests_pass_score" -gt 0 ]; then
    WARNING_OUTPUT="$TEMP_DIR/warning_output.txt"

    # Run tests with all warnings enabled
    if $PYTEST_CMD tests/ -W default --tb=short > "$WARNING_OUTPUT" 2>&1; then
        WARNINGS_FOUND=false
    else
        WARNINGS_FOUND=false  # Test failures handled separately
    fi

    # Check for deprecation warnings
    if grep -qiE "(DeprecationWarning|PendingDeprecationWarning|FutureWarning)" "$WARNING_OUTPUT"; then
        WARNING_COUNT=$(grep -icE "(DeprecationWarning|PendingDeprecationWarning|FutureWarning)" "$WARNING_OUTPUT" || echo "0")
        echo "Found $WARNING_COUNT deprecation warnings:" >&2
        grep -iE "(DeprecationWarning|PendingDeprecationWarning|FutureWarning)" "$WARNING_OUTPUT" >&2 || true

        if [ "$WARNING_COUNT" -le 2 ]; then
            no_warnings_score=60
            no_warnings_details="$WARNING_COUNT minor warnings found"
        else
            no_warnings_score=0
            no_warnings_details="$WARNING_COUNT warnings found"
        fi
    else
        no_warnings_score=100
        no_warnings_details="No deprecation warnings"
        echo "✓ No deprecation warnings found" >&2
    fi
else
    no_warnings_score=0
    no_warnings_details="Cannot check warnings (tests failed)"
fi

echo "Warnings score: $no_warnings_score" >&2

# Calculate base score (weighted average)
dependencies_weight=0.40
tests_weight=0.40
warnings_weight=0.20

base_score=$(echo "scale=2; ($dependencies_updated_score * $dependencies_weight) + ($tests_pass_score * $tests_weight) + ($no_warnings_score * $warnings_weight)" | bc)
base_score=$(printf "%.0f" "$base_score")

# No penalties for this benchmark
time_penalty=0
iteration_penalty=0
error_penalty=0

# Final score same as base score
final_score=$base_score

# Determine pass/fail (need at least 70% to pass)
passed="false"
if (( final_score >= 70 )); then
  passed="true"
fi

# Output JSON
cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "components": {
    "dependencies_updated": {
      "score": ${dependencies_updated_score},
      "weight": ${dependencies_weight},
      "details": "${dependencies_updated_details}"
    },
    "tests_pass": {
      "score": ${tests_pass_score},
      "weight": ${tests_weight},
      "details": "${tests_pass_details}"
    },
    "no_warnings": {
      "score": ${no_warnings_score},
      "weight": ${warnings_weight},
      "details": "${no_warnings_details}"
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
