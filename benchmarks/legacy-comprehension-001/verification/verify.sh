#!/bin/bash

# Legacy Code Comprehension Benchmark - Verification Script
# Evaluates AI's ability to understand complex legacy codebases

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCHMARK_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Score tracking
TOTAL_SCORE=0
MAX_SCORE=100

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Legacy Code Comprehension - Verification${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if answers.json exists
if [ ! -f "$BENCHMARK_DIR/answers.json" ]; then
    echo -e "${RED}Error: answers.json not found!${NC}"
    echo "Expected location: $BENCHMARK_DIR/answers.json"
    echo ""
    echo "Please create answers.json with your answers in the following format:"
    echo '{'
    echo '  "answers": ['
    echo '    {"id": 1, "answer": "Your answer..."},'
    echo '    {"id": 2, "answer": "Your answer..."},'
    echo '    ...'
    echo '  ]'
    echo '}'
    echo ""
    exit 1
fi

# Validate answers.json is valid JSON
if ! python3 -c "import json; json.load(open('$BENCHMARK_DIR/answers.json'))" 2>/dev/null; then
    echo -e "${RED}Error: answers.json is not valid JSON!${NC}"
    echo "Please check your JSON syntax."
    echo ""
    exit 1
fi

# Check if Python test script exists
if [ ! -f "$SCRIPT_DIR/test_comprehension.py" ]; then
    echo -e "${RED}Error: test_comprehension.py not found!${NC}"
    exit 1
fi

# Check if questions.json exists
if [ ! -f "$BENCHMARK_DIR/questions.json" ]; then
    echo -e "${RED}Error: questions.json not found!${NC}"
    exit 1
fi

echo -e "${BLUE}Running comprehension analysis...${NC}"
echo ""

# Run the Python test script and capture output
TEST_OUTPUT=$(python3 "$SCRIPT_DIR/test_comprehension.py" \
    "$BENCHMARK_DIR/questions.json" \
    "$BENCHMARK_DIR/answers.json")

# Extract the JSON output (everything after the summary)
JSON_OUTPUT=$(echo "$TEST_OUTPUT" | sed -n '/{/,$p')

# Parse scores from JSON output
QA_ACCURACY=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['components']['qa_accuracy']['score'])")
DEP_MAPPING=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['components']['dependency_mapping']['score'])")
IMPACT_ANALYSIS=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['components']['impact_analysis']['score'])")
ANALYSIS_QUALITY=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['components']['analysis_quality']['score'])")
FINAL_SCORE=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['score'])")
PASSED=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['passed'])")

# Get summary stats
TOTAL_QUESTIONS=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['summary']['total_questions'])")
ANSWERED=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['summary']['answered'])")
CORRECT=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['summary']['correct'])")
PARTIAL=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['summary']['partial'])")
INCORRECT=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['summary']['incorrect'])")
UNANSWERED=$(echo "$JSON_OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['summary']['unanswered'])")

# Display summary
echo -e "${BLUE}Evaluation Results:${NC}"
echo "----------------------------------------"
echo -e "Total Questions:    $TOTAL_QUESTIONS"
echo -e "Answered:           $ANSWERED"
echo -e "Correct:            ${GREEN}$CORRECT${NC}"
echo -e "Partial Credit:     ${YELLOW}$PARTIAL${NC}"
echo -e "Incorrect:          ${RED}$INCORRECT${NC}"
echo -e "Unanswered:         ${RED}$UNANSWERED${NC}"
echo ""

# Display component scores
echo -e "${BLUE}Component Scores:${NC}"
echo "----------------------------------------"

# Function to display score with color
display_score() {
    local score=$1
    local label=$2
    local weight=$3

    if (( $(echo "$score >= 70" | bc -l) )); then
        color=$GREEN
    elif (( $(echo "$score >= 40" | bc -l) )); then
        color=$YELLOW
    else
        color=$RED
    fi

    printf "%-30s ${color}%6.2f/100${NC} (weight: %d%%)\n" "$label:" "$score" "$weight"
}

display_score "$QA_ACCURACY" "Q&A Accuracy" 40
display_score "$DEP_MAPPING" "Dependency Mapping" 30
display_score "$IMPACT_ANALYSIS" "Impact Analysis" 20
display_score "$ANALYSIS_QUALITY" "Analysis Quality" 10

echo ""
echo -e "${BLUE}----------------------------------------${NC}"

# Final score with color
if (( $(echo "$FINAL_SCORE >= 70" | bc -l) )); then
    SCORE_COLOR=$GREEN
    STATUS="PASSED"
    STATUS_COLOR=$GREEN
elif (( $(echo "$FINAL_SCORE >= 40" | bc -l) )); then
    SCORE_COLOR=$YELLOW
    STATUS="PARTIAL"
    STATUS_COLOR=$YELLOW
else
    SCORE_COLOR=$RED
    STATUS="FAILED"
    STATUS_COLOR=$RED
fi

printf "%-30s ${SCORE_COLOR}%6.2f/100${NC}\n" "FINAL SCORE:" "$FINAL_SCORE"
echo -e "Status:                        ${STATUS_COLOR}${STATUS}${NC}"
echo ""

# Grading scale
echo -e "${BLUE}Grading Scale:${NC}"
echo "  >= 70%: Pass"
echo "  40-69%: Partial Credit"
echo "  < 40%:  Fail"
echo ""

# Category-specific feedback
echo -e "${BLUE}Detailed Feedback:${NC}"
echo "----------------------------------------"

if (( $(echo "$QA_ACCURACY < 70" | bc -l) )); then
    echo -e "${YELLOW}Q&A Accuracy is low.${NC} Review your answers for:"
    echo "  - Specific class/method names from the code"
    echo "  - All relevant keywords for each question"
    echo "  - Technical accuracy based on actual code"
fi

if (( $(echo "$DEP_MAPPING < 70" | bc -l) )); then
    echo -e "${YELLOW}Dependency Mapping needs improvement.${NC} Make sure to:"
    echo "  - Identify both direct and indirect dependencies"
    echo "  - Trace import statements carefully"
    echo "  - Note runtime dependencies (e.g., via parameters)"
fi

if (( $(echo "$IMPACT_ANALYSIS < 70" | bc -l) )); then
    echo -e "${YELLOW}Impact Analysis needs work.${NC} Remember to:"
    echo "  - Trace all uses of changed components"
    echo "  - Consider cascading effects"
    echo "  - Think about data flow and state changes"
fi

if (( $(echo "$ANALYSIS_QUALITY < 70" | bc -l) )); then
    echo -e "${YELLOW}Analysis Quality could be better.${NC} Try to:"
    echo "  - Provide clearer explanations"
    echo "  - Include more specific examples"
    echo "  - Explain the 'why' behind the design"
fi

if (( $(echo "$FINAL_SCORE >= 70" | bc -l) )); then
    echo -e "${GREEN}Excellent work!${NC} You demonstrated strong code comprehension skills."
fi

echo ""

# Generate JSON output for CI/CD
cat > "$BENCHMARK_DIR/verification_result.json" <<EOF
{
  "benchmark": "legacy-comprehension-001",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "passed": $(echo "$PASSED" | tr '[:upper:]' '[:lower:]'),
  "score": $FINAL_SCORE,
  "max_score": 100,
  "components": {
    "qa_accuracy": {
      "score": $QA_ACCURACY,
      "weight": 40,
      "weighted_score": $(echo "$QA_ACCURACY * 0.4" | bc -l)
    },
    "dependency_mapping": {
      "score": $DEP_MAPPING,
      "weight": 30,
      "weighted_score": $(echo "$DEP_MAPPING * 0.3" | bc -l)
    },
    "impact_analysis": {
      "score": $IMPACT_ANALYSIS,
      "weight": 20,
      "weighted_score": $(echo "$IMPACT_ANALYSIS * 0.2" | bc -l)
    },
    "analysis_quality": {
      "score": $ANALYSIS_QUALITY,
      "weight": 10,
      "weighted_score": $(echo "$ANALYSIS_QUALITY * 0.1" | bc -l)
    }
  },
  "summary": {
    "total_questions": $TOTAL_QUESTIONS,
    "answered": $ANSWERED,
    "correct": $CORRECT,
    "partial": $PARTIAL,
    "incorrect": $INCORRECT,
    "unanswered": $UNANSWERED
  }
}
EOF

echo -e "${GREEN}Results saved to verification_result.json${NC}"
echo ""

# Exit with appropriate code
if [ "$PASSED" = "True" ]; then
    exit 0
else
    exit 1
fi
