#!/bin/bash
# Testing Benchmark Verification Script
# Measures test quality through coverage, mutation testing, independence, and assertion quality

set -e

BENCHMARK_NAME="testing-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize scoring components
coverage_score=0
mutation_score=0
independence_score=0
assertion_score=0

# Change to project directory
cd "$PROJECT_DIR"

echo -e "${YELLOW}Running Testing Benchmark Verification...${NC}" >&2

# Check if test file exists
if [ ! -f "test_shopping_cart.py" ]; then
    echo -e "${RED}ERROR: test_shopping_cart.py not found${NC}" >&2
    cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "error": "test_shopping_cart.py not found",
  "components": {
    "coverage": {"score": 0, "weight": 0.30, "details": "Test file not found"},
    "mutation_score": {"score": 0, "weight": 0.40, "details": "Test file not found"},
    "independence": {"score": 0, "weight": 0.15, "details": "Test file not found"},
    "assertion_quality": {"score": 0, "weight": 0.15, "details": "Test file not found"}
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

# Install required packages if not present
echo "Checking dependencies..." >&2
python3 -m pip install --user -q pytest pytest-cov pytest-random-order 2>/dev/null || true

# 1. RUN TESTS AND MEASURE COVERAGE (30% weight)
echo -e "\n${YELLOW}1. Running tests and measuring coverage...${NC}" >&2

coverage_details="Tests failed or error occurred"
if python3 -m pytest test_shopping_cart.py --cov=shopping_cart --cov-report=term --cov-report=json -v > test_output.txt 2>&1; then
    tests_passed=true

    # Extract coverage percentage from coverage.json if it exists
    if [ -f "coverage.json" ]; then
        coverage_percent=$(python3 -c "
import json
with open('coverage.json') as f:
    data = json.load(f)
    print(data['totals']['percent_covered'])
" 2>/dev/null || echo "0")

        coverage_score=$(python3 -c "print(min(100, int($coverage_percent)))")
        coverage_details="Coverage: ${coverage_percent}% (Score: ${coverage_score}/100)"
        echo -e "${GREEN}Coverage: ${coverage_percent}%${NC}" >&2
    else
        coverage_score=0
        coverage_details="Coverage data not available"
    fi
else
    tests_passed=false
    coverage_score=0
    coverage_details="Tests failed - see output for details"
    echo -e "${RED}Tests failed${NC}" >&2
    cat test_output.txt >&2
fi

# 2. MUTATION TESTING (40% weight)
echo -e "\n${YELLOW}2. Running mutation testing...${NC}" >&2

mutation_details="Mutation testing not run"
if [ "$tests_passed" = true ]; then
    # Run simple mutation testing
    echo "Running mutation testing (this may take a while)..." >&2

    # Run our simple mutation tester
    mutation_stats=$(python3 "$SCRIPT_DIR/simple_mutate.py" 2>&1)
    mutation_output=$(echo "$mutation_stats" | tail -1)

    # Parse results (format: killed,survived,timeout,suspicious)
    IFS=',' read -r killed survived timeout suspicious <<< "$mutation_output"

    total_mutants=$((killed + survived + timeout + suspicious))

    if [ $total_mutants -gt 0 ]; then
        mutation_percent=$(python3 -c "print(round(($killed / $total_mutants) * 100, 2))")
        mutation_score=$(python3 -c "print(min(100, int($mutation_percent)))")
        mutation_details="Killed: ${killed}/${total_mutants} mutants (${mutation_percent}%)"
        echo -e "${GREEN}Mutation score: ${mutation_percent}% (${killed}/${total_mutants})${NC}" >&2
    else
        mutation_score=0
        mutation_details="No mutants generated or parsed"
        echo -e "${YELLOW}No mutants generated or parsed${NC}" >&2
    fi
else
    mutation_score=0
    mutation_details="Skipped due to test failures"
    echo -e "${YELLOW}Mutation testing skipped (tests didn't pass)${NC}" >&2
fi

# 3. TEST INDEPENDENCE (15% weight)
echo -e "\n${YELLOW}3. Testing independence (random order)...${NC}" >&2

independence_details="Tests failed"
if [ "$tests_passed" = true ]; then
    # Run tests in random order multiple times
    independence_runs=3
    independence_passed=0

    for i in $(seq 1 $independence_runs); do
        if python3 -m pytest test_shopping_cart.py -p no:randomly --random-order -q > /dev/null 2>&1; then
            independence_passed=$((independence_passed + 1))
        fi
    done

    independence_score=$(python3 -c "print(int(($independence_passed / $independence_runs) * 100))")
    independence_details="Passed ${independence_passed}/${independence_runs} random order runs"
    echo -e "${GREEN}Independence: ${independence_passed}/${independence_runs} runs passed${NC}" >&2
else
    independence_score=0
    independence_details="Skipped due to test failures"
fi

# 4. ASSERTION QUALITY (15% weight)
echo -e "\n${YELLOW}4. Analyzing assertion quality...${NC}" >&2

assertion_details="Analysis failed"
if [ -f "test_shopping_cart.py" ]; then
    # Count assertions in test file
    total_assertions=$(grep -o "assert " test_shopping_cart.py | wc -l | tr -d ' ')

    # Count test functions
    test_functions=$(grep -c "def test_" test_shopping_cart.py 2>/dev/null || echo "1")

    # Calculate assertions per test
    if [ $test_functions -gt 0 ]; then
        assertions_per_test=$(python3 -c "print(round($total_assertions / $test_functions, 2))")

        # Score based on assertion density
        # Good tests have 1-3 assertions per test on average
        # Score: 100 if 1-3, degrading outside that range
        assertion_score=$(python3 -c "
apt = $assertions_per_test
if apt >= 1 and apt <= 3:
    score = 100
elif apt < 1:
    score = int(apt * 100)
else:
    # Degrade for too many assertions (probably not focused tests)
    score = max(0, int(100 - (apt - 3) * 10))
print(min(100, max(0, score)))
")
        assertion_details="Total assertions: ${total_assertions}, Tests: ${test_functions}, Avg: ${assertions_per_test}/test"
        echo -e "${GREEN}Assertions: ${assertions_per_test} per test on average${NC}" >&2
    else
        assertion_score=0
        assertion_details="No test functions found"
    fi
else
    assertion_score=0
    assertion_details="Test file not found"
fi

# Calculate base score (weighted sum)
base_score=$(python3 -c "
coverage = $coverage_score * 0.30
mutation = $mutation_score * 0.40
independence = $independence_score * 0.15
assertion = $assertion_score * 0.15
total = coverage + mutation + independence + assertion
print(round(total, 2))
")

# No penalties in this benchmark (could be added based on metadata)
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

# Output JSON
cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "components": {
    "coverage": {
      "score": ${coverage_score},
      "weight": 0.30,
      "details": "${coverage_details}"
    },
    "mutation_score": {
      "score": ${mutation_score},
      "weight": 0.40,
      "details": "${mutation_details}"
    },
    "independence": {
      "score": ${independence_score},
      "weight": 0.15,
      "details": "${independence_details}"
    },
    "assertion_quality": {
      "score": ${assertion_score},
      "weight": 0.15,
      "details": "${assertion_details}"
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
rm -f test_output.txt coverage.json .coverage shopping_cart.py.bak 2>/dev/null || true

# Exit with appropriate code
if [ "$passed" = "true" ]; then
    exit 0
else
    exit 1
fi
