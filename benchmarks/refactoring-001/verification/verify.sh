#!/bin/bash
# Refactoring Benchmark Verification Script
# Measures code quality improvement through tests, complexity reduction, and duplication elimination

set -e

BENCHMARK_NAME="refactoring-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
STARTER_DIR="$PROJECT_DIR/starter-code"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize scoring components
tests_score=0
complexity_score=0
duplication_score=0

# Change to project directory
cd "$PROJECT_DIR"

echo -e "${YELLOW}Running Refactoring Benchmark Verification...${NC}" >&2

# Check if refactored file exists
if [ ! -f "order_processor.py" ]; then
    echo -e "${RED}ERROR: order_processor.py not found in project root${NC}" >&2
    cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "error": "order_processor.py not found - expected in project root",
  "components": {
    "tests": {"score": 0, "weight": 0.50, "details": "Refactored file not found"},
    "complexity": {"score": 0, "weight": 0.30, "details": "Refactored file not found"},
    "duplication": {"score": 0, "weight": 0.20, "details": "Refactored file not found"}
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

# Install required packages
echo "Installing dependencies..." >&2
python3 -m pip install --user -q pytest radon 2>/dev/null || true

# Copy test file to project root
cp "$STARTER_DIR/test_order_processor.py" . 2>/dev/null || true

# 1. BASELINE METRICS (from starter code)
echo -e "\n${YELLOW}1. Calculating baseline metrics from starter code...${NC}" >&2

cd "$STARTER_DIR"

# Baseline complexity
baseline_complexity=$(python3 -m radon cc order_processor.py -a -s | grep "Average complexity:" | awk '{print $NF}' | tr -d '()' || echo "10.0")
echo "Baseline complexity: $baseline_complexity" >&2

# Baseline duplication (count repeated code blocks)
baseline_duplication=$(python3 "$SCRIPT_DIR/measure_duplication.py" order_processor.py 2>/dev/null || echo "100")
echo "Baseline duplication: $baseline_duplication" >&2

# 2. RUN TESTS ON REFACTORED CODE (50% weight - ALL OR NOTHING)
echo -e "\n${YELLOW}2. Running tests on refactored code...${NC}" >&2

cd "$PROJECT_DIR"

tests_details="Tests failed or error occurred"
if python3 -m pytest test_order_processor.py -v --tb=short > test_output.txt 2>&1; then
    tests_passed=true
    tests_score=100

    # Count passing tests
    passed_count=$(grep -c "PASSED" test_output.txt || echo "0")
    tests_details="All $passed_count tests passed"
    echo -e "${GREEN}All tests passed ($passed_count tests)${NC}" >&2
else
    tests_passed=false
    tests_score=0

    # Count failures
    failed_count=$(grep -c "FAILED" test_output.txt || echo "unknown")
    tests_details="Tests failed (${failed_count} failures) - see output"
    echo -e "${RED}Tests failed (${failed_count} failures)${NC}" >&2
    cat test_output.txt >&2
fi

# 3. COMPLEXITY REDUCTION (30% weight)
echo -e "\n${YELLOW}3. Measuring complexity reduction...${NC}" >&2

complexity_details="Complexity analysis failed"
if [ "$tests_passed" = true ]; then
    # Measure refactored complexity
    refactored_complexity=$(python3 -m radon cc order_processor.py -a -s | grep "Average complexity:" | awk '{print $NF}' | tr -d '()' || echo "10.0")
    echo "Refactored complexity: $refactored_complexity" >&2

    # Calculate reduction percentage
    complexity_reduction=$(python3 -c "
baseline = float($baseline_complexity)
refactored = float($refactored_complexity)
if baseline > 0:
    reduction = ((baseline - refactored) / baseline) * 100
    # Cap at 100% improvement
    reduction = max(0, min(100, reduction))
    print(round(reduction, 2))
else:
    print(0)
" 2>/dev/null || echo "0")

    complexity_score=$(python3 -c "print(int(float($complexity_reduction)))")
    complexity_details="Reduced from ${baseline_complexity} to ${refactored_complexity} (${complexity_reduction}% improvement)"
    echo -e "${GREEN}Complexity reduction: ${complexity_reduction}%${NC}" >&2
else
    complexity_score=0
    complexity_details="Skipped due to test failures"
    echo -e "${YELLOW}Complexity analysis skipped (tests failed)${NC}" >&2
fi

# 4. DUPLICATION REDUCTION (20% weight)
echo -e "\n${YELLOW}4. Measuring code duplication reduction...${NC}" >&2

duplication_details="Duplication analysis failed"
if [ "$tests_passed" = true ]; then
    # Measure refactored duplication
    refactored_duplication=$(python3 "$SCRIPT_DIR/measure_duplication.py" order_processor.py 2>/dev/null || echo "100")
    echo "Refactored duplication: $refactored_duplication" >&2

    # Calculate reduction percentage
    duplication_reduction=$(python3 -c "
baseline = float($baseline_duplication)
refactored = float($refactored_duplication)
if baseline > 0:
    reduction = ((baseline - refactored) / baseline) * 100
    # Cap at 100% improvement
    reduction = max(0, min(100, reduction))
    print(round(reduction, 2))
else:
    print(0)
" 2>/dev/null || echo "0")

    duplication_score=$(python3 -c "print(int(float($duplication_reduction)))")
    duplication_details="Reduced from ${baseline_duplication} to ${refactored_duplication} (${duplication_reduction}% improvement)"
    echo -e "${GREEN}Duplication reduction: ${duplication_reduction}%${NC}" >&2
else
    duplication_score=0
    duplication_details="Skipped due to test failures"
    echo -e "${YELLOW}Duplication analysis skipped (tests failed)${NC}" >&2
fi

# Calculate base score (weighted sum)
base_score=$(python3 -c "
tests = $tests_score * 0.50
complexity = $complexity_score * 0.30
duplication = $duplication_score * 0.20
total = tests + complexity + duplication
print(round(total, 2))
")

# No penalties in this benchmark
time_penalty=0
iteration_penalty=0
error_penalty=0

final_score=$(python3 -c "print(int($base_score))")

# Determine pass/fail (70% threshold, but must pass tests)
if [ "$tests_passed" = true ] && (( final_score >= 70 )); then
    passed="true"
    echo -e "\n${GREEN}PASSED${NC} - Score: ${final_score}/100" >&2
elif [ "$tests_passed" = false ]; then
    passed="false"
    echo -e "\n${RED}FAILED${NC} - Tests must pass (score: 0/100)" >&2
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
    "tests": {
      "score": ${tests_score},
      "weight": 0.50,
      "details": "${tests_details}"
    },
    "complexity": {
      "score": ${complexity_score},
      "weight": 0.30,
      "details": "${complexity_details}",
      "baseline": ${baseline_complexity},
      "refactored": ${refactored_complexity:-0}
    },
    "duplication": {
      "score": ${duplication_score},
      "weight": 0.20,
      "details": "${duplication_details}",
      "baseline": ${baseline_duplication},
      "refactored": ${refactored_duplication:-0}
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
rm -f test_output.txt test_order_processor.py 2>/dev/null || true

# Exit with appropriate code
if [ "$passed" = "true" ]; then
    exit 0
else
    exit 1
fi
