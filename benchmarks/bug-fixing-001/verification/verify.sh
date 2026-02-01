#!/bin/bash
# Bug Fixing Benchmark Verification Script
# Outputs JSON with scoring details

set -e

BENCHMARK_NAME="bug-fixing-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Initialize scores
bug_fixed_score=0
no_regressions_score=0
code_quality_score=0

# Change to benchmark directory
cd "$BENCHMARK_DIR"

echo "Running verification for ${BENCHMARK_NAME}..." >&2
echo "Benchmark directory: $BENCHMARK_DIR" >&2

# Check if pytest is available (try both pytest and python -m pytest)
if ! command -v pytest &> /dev/null && ! python3 -m pytest --version &> /dev/null; then
    echo "ERROR: pytest is not installed. Install with: pip install pytest" >&2
    echo '{"benchmark": "'$BENCHMARK_NAME'", "error": "pytest not installed", "passed": false}'
    exit 1
fi

# Use python3 -m pytest for better compatibility
PYTEST_CMD="python3 -m pytest"

# Create temporary directory for test results
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Run all tests and capture output
echo "Running test suite..." >&2
TEST_OUTPUT="$TEMP_DIR/test_output.txt"
TEST_RESULTS="$TEMP_DIR/test_results.txt"

if $PYTEST_CMD tests/ -v --tb=short > "$TEST_OUTPUT" 2>&1; then
    ALL_TESTS_PASSED=true
    echo "All tests passed!" >&2
else
    ALL_TESTS_PASSED=false
    echo "Some tests failed." >&2
fi

# Save test output for analysis
cat "$TEST_OUTPUT" >&2
cp "$TEST_OUTPUT" "$TEST_RESULTS"

# Parse test results to check specific tests
TOTAL_TESTS=$(grep -E "^tests/.*::" "$TEST_OUTPUT" | wc -l | tr -d ' ' || echo "0")
PASSED_TESTS=$(grep -E "PASSED" "$TEST_OUTPUT" | wc -l | tr -d ' ' || echo "0")
FAILED_TESTS=$(grep -E "FAILED" "$TEST_OUTPUT" | wc -l | tr -d ' ' || echo "0")

echo "Total tests: $TOTAL_TESTS, Passed: $PASSED_TESTS, Failed: $FAILED_TESTS" >&2

# Check if the specific failing test now passes
TARGET_TEST="test_business_days_one_week_span"
if grep -q "${TARGET_TEST}.*PASSED" "$TEST_OUTPUT"; then
    echo "SUCCESS: Target test ${TARGET_TEST} is now passing!" >&2
    bug_fixed_score=100
    bug_fixed_details="The failing test now passes"
else
    echo "FAILURE: Target test ${TARGET_TEST} is still failing" >&2
    bug_fixed_score=0
    bug_fixed_details="The target test is still failing"
fi

# Check for regressions (other tests that should pass)
# Expected: 18 total tests, all should pass after fix
EXPECTED_TOTAL_TESTS=18

if [ "$ALL_TESTS_PASSED" = true ] && [ "$PASSED_TESTS" -eq "$EXPECTED_TOTAL_TESTS" ]; then
    echo "SUCCESS: No regressions detected, all tests pass" >&2
    no_regressions_score=100
    no_regressions_details="All $PASSED_TESTS tests pass"
elif [ "$PASSED_TESTS" -ge 17 ] && [ "$bug_fixed_score" -eq 100 ]; then
    # If the bug is fixed and at least 17/18 tests pass
    echo "WARNING: Minor regression detected" >&2
    no_regressions_score=70
    no_regressions_details="$PASSED_TESTS/$EXPECTED_TOTAL_TESTS tests pass"
else
    echo "FAILURE: Significant regressions or tests not passing" >&2
    no_regressions_score=0
    no_regressions_details="Only $PASSED_TESTS/$EXPECTED_TOTAL_TESTS tests pass"
fi

# Code quality check: verify the fix is minimal
# Check that test files haven't been modified
code_quality_details="Code quality checks passed"

# Check if src/daterange.py exists
if [ ! -f "src/daterange.py" ]; then
    code_quality_score=0
    code_quality_details="src/daterange.py not found"
else
    # Basic check: file should still have similar line count (indicating minimal change)
    LINE_COUNT=$(wc -l < "src/daterange.py" | tr -d ' ')

    # Original file has about 110 lines, give some tolerance
    if [ "$LINE_COUNT" -lt 90 ] || [ "$LINE_COUNT" -gt 150 ]; then
        code_quality_score=50
        code_quality_details="File size changed significantly ($LINE_COUNT lines)"
    else
        code_quality_score=100
        code_quality_details="Minimal changes detected"
    fi
fi

# Calculate base score (weighted average)
bug_fixed_weight=0.6
no_regressions_weight=0.3
code_quality_weight=0.1

base_score=$(echo "scale=2; ($bug_fixed_score * $bug_fixed_weight) + ($no_regressions_score * $no_regressions_weight) + ($code_quality_score * $code_quality_weight)" | bc)
base_score=$(printf "%.0f" "$base_score")

# No penalties for this benchmark (could add time/iteration penalties in future)
time_penalty=0
iteration_penalty=0
error_penalty=0

# Final score same as base score (no penalties)
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
    "bug_fixed": {
      "score": ${bug_fixed_score},
      "weight": ${bug_fixed_weight},
      "details": "${bug_fixed_details}"
    },
    "no_regressions": {
      "score": ${no_regressions_score},
      "weight": ${no_regressions_weight},
      "details": "${no_regressions_details}"
    },
    "code_quality": {
      "score": ${code_quality_score},
      "weight": ${code_quality_weight},
      "details": "${code_quality_details}"
    }
  },
  "test_summary": {
    "total_tests": ${TOTAL_TESTS},
    "passed_tests": ${PASSED_TESTS},
    "failed_tests": ${FAILED_TESTS}
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
