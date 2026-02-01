#!/bin/bash

# Verification script for documentation-001 benchmark
# Scores the AI's documentation of the HTTP client library

set -e

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER_CODE_DIR="$BENCHMARK_DIR/starter-code"
VERIFICATION_DIR="$BENCHMARK_DIR/verification"
TESTS_DIR="$VERIFICATION_DIR/tests"

# Initialize scores
TOTAL_SCORE=0
MAX_SCORE=100

# Score components
API_COVERAGE_SCORE=0
API_COVERAGE_MAX=30

EXAMPLE_EXECUTION_SCORE=0
EXAMPLE_EXECUTION_MAX=40

CONSISTENCY_SCORE=0
CONSISTENCY_MAX=20

READABILITY_SCORE=0
READABILITY_MAX=10

# Check if http_client.py exists
if [ ! -f "$STARTER_CODE_DIR/http_client.py" ]; then
    echo "Error: http_client.py not found in starter-code/" >&2
    cat <<EOF
{
  "score": 0,
  "max_score": $MAX_SCORE,
  "test_passed": false,
  "details": {
    "error": "Missing http_client.py file",
    "api_coverage": {
      "score": 0,
      "max_score": $API_COVERAGE_MAX,
      "feedback": "Required file http_client.py not found"
    },
    "example_execution": {
      "score": 0,
      "max_score": $EXAMPLE_EXECUTION_MAX,
      "feedback": "No file to test"
    },
    "consistency": {
      "score": 0,
      "max_score": $CONSISTENCY_MAX,
      "feedback": "No file to test"
    },
    "readability": {
      "score": 0,
      "max_score": $READABILITY_MAX,
      "feedback": "No file to test"
    }
  }
}
EOF
    exit 1
fi

# --- SCORE API COVERAGE (30 points) ---
echo "Checking API coverage..." >&2
COVERAGE_RESULT=$(python3 "$TESTS_DIR/check_coverage.py" "$STARTER_CODE_DIR/http_client.py")
COVERAGE_PCT=$(echo "$COVERAGE_RESULT" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(data["coverage_percentage"])')

# Convert coverage percentage to score (0-30)
API_COVERAGE_SCORE=$(python3 -c "print(int($COVERAGE_PCT * $API_COVERAGE_MAX / 100))")

COVERAGE_FEEDBACK=""
if (( $(echo "$COVERAGE_PCT >= 90" | bc -l) )); then
    COVERAGE_FEEDBACK="Excellent API coverage (${COVERAGE_PCT}%). "
elif (( $(echo "$COVERAGE_PCT >= 70" | bc -l) )); then
    COVERAGE_FEEDBACK="Good API coverage (${COVERAGE_PCT}%), but some APIs missing documentation. "
elif (( $(echo "$COVERAGE_PCT >= 50" | bc -l) )); then
    COVERAGE_FEEDBACK="Fair API coverage (${COVERAGE_PCT}%), many APIs still undocumented. "
else
    COVERAGE_FEEDBACK="Poor API coverage (${COVERAGE_PCT}%), most APIs lack documentation. "
fi

# Get missing APIs
MISSING_CLASSES=$(echo "$COVERAGE_RESULT" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(", ".join(data["details"]["classes"]["missing"]) if data["details"]["classes"]["missing"] else "None")')
MISSING_METHODS=$(echo "$COVERAGE_RESULT" | python3 -c 'import sys, json; data=json.load(sys.stdin); missing=data["details"]["methods"]["missing"]; print(", ".join(missing[:5]) + ("..." if len(missing) > 5 else "") if missing else "None")')

if [ "$MISSING_CLASSES" != "None" ]; then
    COVERAGE_FEEDBACK+="Missing class docs: $MISSING_CLASSES. "
fi
if [ "$MISSING_METHODS" != "None" ]; then
    COVERAGE_FEEDBACK+="Missing method docs: $MISSING_METHODS. "
fi

# --- SCORE EXAMPLE EXECUTION (40 points) ---
echo "Extracting code examples..." >&2
python3 "$TESTS_DIR/extract_examples.py" "$STARTER_CODE_DIR/http_client.py" > /tmp/examples.json

EXAMPLE_COUNT=$(python3 -c 'import json; data=json.load(open("/tmp/examples.json")); print(len(data))')

EXAMPLE_FEEDBACK=""
if [ "$EXAMPLE_COUNT" -eq 0 ]; then
    EXAMPLE_EXECUTION_SCORE=0
    EXAMPLE_FEEDBACK="No code examples found in docstrings. "
else
    echo "Running $EXAMPLE_COUNT code examples..." >&2
    EXAMPLE_RESULTS=$(python3 "$TESTS_DIR/run_examples.py" "$STARTER_CODE_DIR/http_client.py" /tmp/examples.json)

    SUCCESSFUL_EXAMPLES=$(echo "$EXAMPLE_RESULTS" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(sum(1 for ex in data if ex["success"]))')
    FAILED_EXAMPLES=$(echo "$EXAMPLE_RESULTS" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(sum(1 for ex in data if not ex["success"]))')

    SUCCESS_RATE=$(python3 -c "print($SUCCESSFUL_EXAMPLES / $EXAMPLE_COUNT * 100 if $EXAMPLE_COUNT > 0 else 0)")

    # Score: Base points for having examples + points for success rate
    BASE_POINTS=10
    SUCCESS_POINTS=$((EXAMPLE_EXECUTION_MAX - BASE_POINTS))
    EXAMPLE_EXECUTION_SCORE=$(python3 -c "print(int($BASE_POINTS + $SUCCESS_RATE * $SUCCESS_POINTS / 100))")

    if (( $(echo "$SUCCESS_RATE >= 90" | bc -l) )); then
        EXAMPLE_FEEDBACK="Excellent! ${SUCCESSFUL_EXAMPLES}/${EXAMPLE_COUNT} examples execute successfully (${SUCCESS_RATE}%). "
    elif (( $(echo "$SUCCESS_RATE >= 70" | bc -l) )); then
        EXAMPLE_FEEDBACK="Good. ${SUCCESSFUL_EXAMPLES}/${EXAMPLE_COUNT} examples execute successfully (${SUCCESS_RATE}%). "
    elif (( $(echo "$SUCCESS_RATE >= 50" | bc -l) )); then
        EXAMPLE_FEEDBACK="Fair. ${SUCCESSFUL_EXAMPLES}/${EXAMPLE_COUNT} examples execute (${SUCCESS_RATE}%), but many fail. "
    else
        EXAMPLE_FEEDBACK="Poor. Only ${SUCCESSFUL_EXAMPLES}/${EXAMPLE_COUNT} examples execute (${SUCCESS_RATE}%). "
    fi

    if [ "$FAILED_EXAMPLES" -gt 0 ]; then
        FIRST_ERROR=$(echo "$EXAMPLE_RESULTS" | python3 -c 'import sys, json; data=json.load(sys.stdin); failed=[ex for ex in data if not ex["success"]]; print(failed[0]["error"][:100] + "..." if failed and failed[0]["error"] else "") if failed else ""')
        if [ -n "$FIRST_ERROR" ]; then
            EXAMPLE_FEEDBACK+="Example error: $FIRST_ERROR "
        fi
    fi
fi

# --- SCORE CONSISTENCY (20 points) ---
echo "Checking documentation consistency..." >&2
CONSISTENCY_RESULT=$(python3 "$TESTS_DIR/check_consistency.py" "$STARTER_CODE_DIR/http_client.py")
CONSISTENCY_PCT=$(echo "$CONSISTENCY_RESULT" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(data["consistency_percentage"])')

# Convert consistency percentage to score (0-20)
CONSISTENCY_SCORE=$(python3 -c "print(int($CONSISTENCY_PCT * $CONSISTENCY_MAX / 100))")

CONSISTENCY_FEEDBACK=""
ISSUE_COUNT=$(echo "$CONSISTENCY_RESULT" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(len(data["issues"]))')

if (( $(echo "$CONSISTENCY_PCT >= 90" | bc -l) )); then
    CONSISTENCY_FEEDBACK="Excellent consistency between docs and code. "
elif (( $(echo "$CONSISTENCY_PCT >= 70" | bc -l) )); then
    CONSISTENCY_FEEDBACK="Good consistency, minor issues found ($ISSUE_COUNT issues). "
else
    CONSISTENCY_FEEDBACK="Poor consistency, documentation doesn't match code ($ISSUE_COUNT issues). "
fi

if [ "$ISSUE_COUNT" -gt 0 ]; then
    FIRST_ISSUE=$(echo "$CONSISTENCY_RESULT" | python3 -c 'import sys, json; data=json.load(sys.stdin); issues=data["issues"]; print(f"{issues[0][\"function\"]}: {issues[0][\"type\"]}") if issues else ""')
    if [ -n "$FIRST_ISSUE" ]; then
        CONSISTENCY_FEEDBACK+="Example: $FIRST_ISSUE. "
    fi
fi

# --- SCORE READABILITY (10 points) ---
echo "Checking documentation format..." >&2
FORMAT_RESULT=$(python3 "$TESTS_DIR/check_format.py" "$STARTER_CODE_DIR/http_client.py")
FORMAT_SCORE=$(echo "$FORMAT_RESULT" | python3 -c 'import sys, json; data=json.load(sys.stdin); print(data["average_format_score"])')

# Convert format score to readability score (0-10)
READABILITY_SCORE=$(python3 -c "print(int($FORMAT_SCORE * $READABILITY_MAX / 100))")

READABILITY_FEEDBACK=""
if (( $(echo "$FORMAT_SCORE >= 90" | bc -l) )); then
    READABILITY_FEEDBACK="Well-formatted, follows Google style consistently. "
elif (( $(echo "$FORMAT_SCORE >= 70" | bc -l) )); then
    READABILITY_FEEDBACK="Generally well-formatted, minor style issues. "
else
    READABILITY_FEEDBACK="Formatting needs improvement, inconsistent style. "
fi

# Calculate total score
TOTAL_SCORE=$((API_COVERAGE_SCORE + EXAMPLE_EXECUTION_SCORE + CONSISTENCY_SCORE + READABILITY_SCORE))

# Determine overall test status
TEST_PASSED=false
if [ "$TOTAL_SCORE" -ge 70 ]; then
    TEST_PASSED=true
fi

# Build detailed results JSON
cat <<EOF
{
  "score": $TOTAL_SCORE,
  "max_score": $MAX_SCORE,
  "test_passed": $TEST_PASSED,
  "details": {
    "api_coverage": {
      "score": $API_COVERAGE_SCORE,
      "max_score": $API_COVERAGE_MAX,
      "percentage": $COVERAGE_PCT,
      "feedback": "$COVERAGE_FEEDBACK",
      "coverage_details": $COVERAGE_RESULT
    },
    "example_execution": {
      "score": $EXAMPLE_EXECUTION_SCORE,
      "max_score": $EXAMPLE_EXECUTION_MAX,
      "total_examples": $EXAMPLE_COUNT,
      "feedback": "$EXAMPLE_FEEDBACK"
    },
    "consistency": {
      "score": $CONSISTENCY_SCORE,
      "max_score": $CONSISTENCY_MAX,
      "percentage": $CONSISTENCY_PCT,
      "feedback": "$CONSISTENCY_FEEDBACK",
      "consistency_details": $CONSISTENCY_RESULT
    },
    "readability": {
      "score": $READABILITY_SCORE,
      "max_score": $READABILITY_MAX,
      "format_score": $FORMAT_SCORE,
      "feedback": "$READABILITY_FEEDBACK",
      "format_details": $FORMAT_RESULT
    }
  }
}
EOF

exit 0
