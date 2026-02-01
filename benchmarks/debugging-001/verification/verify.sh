#!/bin/bash

# Verification script for debugging-001 benchmark
# Scores the AI's root cause analysis and bug fix

set -e

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER_CODE_DIR="$BENCHMARK_DIR/starter-code"
VERIFICATION_DIR="$BENCHMARK_DIR/verification"

# Initialize scores
TOTAL_SCORE=0
MAX_SCORE=100

# Score components
ROOT_CAUSE_SCORE=0
ROOT_CAUSE_MAX=60

MINIMAL_REPRO_SCORE=0
MINIMAL_REPRO_MAX=20

INVESTIGATION_SCORE=0
INVESTIGATION_MAX=20

# Check if ROOT_CAUSE_ANALYSIS.md exists
if [ ! -f "$STARTER_CODE_DIR/ROOT_CAUSE_ANALYSIS.md" ]; then
    echo "Error: ROOT_CAUSE_ANALYSIS.md not found in starter-code/" >&2
    cat <<EOF
{
  "score": 0,
  "max_score": $MAX_SCORE,
  "test_passed": false,
  "details": {
    "error": "Missing ROOT_CAUSE_ANALYSIS.md file",
    "root_cause_analysis": {
      "score": 0,
      "max_score": $ROOT_CAUSE_MAX,
      "feedback": "Required file ROOT_CAUSE_ANALYSIS.md not found"
    },
    "minimal_reproduction": {
      "score": 0,
      "max_score": $MINIMAL_REPRO_MAX,
      "feedback": "No analysis document provided"
    },
    "investigation": {
      "score": 0,
      "max_score": $INVESTIGATION_MAX,
      "feedback": "No analysis document provided"
    }
  }
}
EOF
    exit 1
fi

# Read the analysis file
ANALYSIS_FILE="$STARTER_CODE_DIR/ROOT_CAUSE_ANALYSIS.md"
ANALYSIS_CONTENT=$(cat "$ANALYSIS_FILE")

# Function to check if text contains key concepts (case insensitive)
contains_concept() {
    local text="$1"
    local pattern="$2"
    echo "$text" | grep -iq "$pattern"
    return $?
}

# --- SCORE ROOT CAUSE ANALYSIS (60 points) ---
ROOT_CAUSE_FEEDBACK=""

# Check for key concepts in root cause identification
FOUND_KEY_REUSE=false
FOUND_WRONG_KEY=false
FOUND_SHOULD_DELETE=false
FOUND_LINE_REFERENCE=false
FOUND_OVERWRITES=false

# Look for understanding that the LRU key is being reused/overwritten
if contains_concept "$ANALYSIS_CONTENT" "lru.*key.*reuse\|reuse.*lru.*key\|overwrit.*lru\|lru.*overwrit\|replac.*lru.*key\|lru.*key.*replac"; then
    FOUND_KEY_REUSE=true
    ROOT_CAUSE_SCORE=$((ROOT_CAUSE_SCORE + 15))
fi

# Look for understanding that value is assigned to wrong key
if contains_concept "$ANALYSIS_CONTENT" "wrong.*key\|incorrect.*key\|assigns.*to.*lru\|lru_key.*=.*value\|cache\[lru_key\].*=.*value"; then
    FOUND_WRONG_KEY=true
    ROOT_CAUSE_SCORE=$((ROOT_CAUSE_SCORE + 15))
fi

# Look for understanding that the old key should be deleted/removed
if contains_concept "$ANALYSIS_CONTENT" "delete\|delet\|remove\|remov\|pop\|should.*del\|need.*del\|must.*del"; then
    FOUND_SHOULD_DELETE=true
    ROOT_CAUSE_SCORE=$((ROOT_CAUSE_SCORE + 10))
fi

# Look for specific line/code reference
if contains_concept "$ANALYSIS_CONTENT" "line.*4[0-9]\|line.*5[0-9]\|self._cache\[lru_key\].*=.*value"; then
    FOUND_LINE_REFERENCE=true
    ROOT_CAUSE_SCORE=$((ROOT_CAUSE_SCORE + 10))
fi

# Look for understanding about overwriting instead of adding new entry
if contains_concept "$ANALYSIS_CONTENT" "never.*add\|not.*add\|doesn't.*add\|fails.*to.*add\|overwrit.*instead\|modif.*existing\|modif.*old"; then
    FOUND_OVERWRITES=true
    ROOT_CAUSE_SCORE=$((ROOT_CAUSE_SCORE + 10))
fi

# Build feedback for root cause
ROOT_CAUSE_FEEDBACK="Root cause analysis: "
if [ $ROOT_CAUSE_SCORE -ge 50 ]; then
    ROOT_CAUSE_FEEDBACK+="Excellent identification of the bug. "
elif [ $ROOT_CAUSE_SCORE -ge 30 ]; then
    ROOT_CAUSE_FEEDBACK+="Good understanding, but missing some key details. "
else
    ROOT_CAUSE_FEEDBACK+="Root cause not correctly identified. "
fi

if [ "$FOUND_KEY_REUSE" = false ]; then
    ROOT_CAUSE_FEEDBACK+="Did not identify that LRU key is being reused/overwritten. "
fi
if [ "$FOUND_WRONG_KEY" = false ]; then
    ROOT_CAUSE_FEEDBACK+="Did not explain that value is assigned to wrong key. "
fi
if [ "$FOUND_SHOULD_DELETE" = false ]; then
    ROOT_CAUSE_FEEDBACK+="Did not mention need to delete/remove old entry. "
fi

# --- SCORE MINIMAL REPRODUCTION (20 points) ---
MINIMAL_REPRO_FEEDBACK=""

# Check if there's a minimal reproduction section
if contains_concept "$ANALYSIS_CONTENT" "minimal.*repro\|reproduction\|reproduce\|repro.*case\|simple.*example"; then
    MINIMAL_REPRO_SCORE=$((MINIMAL_REPRO_SCORE + 5))

    # Check if it shows the basic pattern (create cache, add items, demonstrate bug)
    if contains_concept "$ANALYSIS_CONTENT" "LRUCache\|cache.*put\|cache\.put"; then
        MINIMAL_REPRO_SCORE=$((MINIMAL_REPRO_SCORE + 5))
    fi

    # Check if it's actually minimal (not just copying the full test)
    if contains_concept "$ANALYSIS_CONTENT" "capacity.*[12]\|LRUCache(1)\|LRUCache(2)"; then
        MINIMAL_REPRO_SCORE=$((MINIMAL_REPRO_SCORE + 5))
    fi

    # Check if it demonstrates the wrong behavior
    if contains_concept "$ANALYSIS_CONTENT" "get.*None\|returns.*None\|should.*be.*None\|expected\|actual"; then
        MINIMAL_REPRO_SCORE=$((MINIMAL_REPRO_SCORE + 5))
    fi

    MINIMAL_REPRO_FEEDBACK="Minimal reproduction provided. "
else
    MINIMAL_REPRO_FEEDBACK="No minimal reproduction case found. "
fi

# --- SCORE INVESTIGATION DOCUMENTATION (20 points) ---
INVESTIGATION_FEEDBACK=""

# Check for investigation process documentation
if contains_concept "$ANALYSIS_CONTENT" "investigation\|process\|steps\|approach\|method\|how.*debug"; then
    INVESTIGATION_SCORE=$((INVESTIGATION_SCORE + 5))
fi

# Check for observation of test failure
if contains_concept "$ANALYSIS_CONTENT" "failing.*test\|test.*fail\|observed\|error\|assertion"; then
    INVESTIGATION_SCORE=$((INVESTIGATION_SCORE + 5))
fi

# Check for hypothesis exploration
if contains_concept "$ANALYSIS_CONTENT" "hypothesis\|hypothes\|thought\|considered\|explored\|tried\|checked"; then
    INVESTIGATION_SCORE=$((INVESTIGATION_SCORE + 5))
fi

# Check for code analysis
if contains_concept "$ANALYSIS_CONTENT" "code.*review\|analyzed.*code\|examined\|inspected\|traced\|follow.*flow"; then
    INVESTIGATION_SCORE=$((INVESTIGATION_SCORE + 5))
fi

if [ $INVESTIGATION_SCORE -ge 15 ]; then
    INVESTIGATION_FEEDBACK="Well-documented investigation process. "
elif [ $INVESTIGATION_SCORE -ge 10 ]; then
    INVESTIGATION_FEEDBACK="Investigation documented but could be more detailed. "
else
    INVESTIGATION_FEEDBACK="Investigation process not well documented. "
fi

# --- CHECK IF TESTS PASS ---
TEST_PASSED=false
TEST_OUTPUT=""
cd "$STARTER_CODE_DIR"

# Run pytest
if command -v pytest &> /dev/null; then
    if pytest test_lru_cache.py -v > /tmp/test_output.txt 2>&1; then
        TEST_PASSED=true
        TEST_OUTPUT="All tests passed"
    else
        TEST_OUTPUT=$(cat /tmp/test_output.txt | tail -20)
    fi
else
    # Fallback to python3 -m pytest
    if python3 -m pytest test_lru_cache.py -v > /tmp/test_output.txt 2>&1; then
        TEST_PASSED=true
        TEST_OUTPUT="All tests passed"
    else
        TEST_OUTPUT=$(cat /tmp/test_output.txt | tail -20)
    fi
fi

# If tests don't pass, penalize scores
if [ "$TEST_PASSED" = false ]; then
    ROOT_CAUSE_SCORE=$((ROOT_CAUSE_SCORE / 2))
    MINIMAL_REPRO_SCORE=$((MINIMAL_REPRO_SCORE / 2))
    INVESTIGATION_SCORE=$((INVESTIGATION_SCORE / 2))
fi

# Calculate total score
TOTAL_SCORE=$((ROOT_CAUSE_SCORE + MINIMAL_REPRO_SCORE + INVESTIGATION_SCORE))

# Output JSON result
cat <<EOF
{
  "score": $TOTAL_SCORE,
  "max_score": $MAX_SCORE,
  "test_passed": $TEST_PASSED,
  "details": {
    "root_cause_analysis": {
      "score": $ROOT_CAUSE_SCORE,
      "max_score": $ROOT_CAUSE_MAX,
      "feedback": "$ROOT_CAUSE_FEEDBACK",
      "found_key_concepts": {
        "lru_key_reuse": $FOUND_KEY_REUSE,
        "wrong_key_assignment": $FOUND_WRONG_KEY,
        "should_delete": $FOUND_SHOULD_DELETE,
        "line_reference": $FOUND_LINE_REFERENCE,
        "overwrites_instead_of_adding": $FOUND_OVERWRITES
      }
    },
    "minimal_reproduction": {
      "score": $MINIMAL_REPRO_SCORE,
      "max_score": $MINIMAL_REPRO_MAX,
      "feedback": "$MINIMAL_REPRO_FEEDBACK"
    },
    "investigation": {
      "score": $INVESTIGATION_SCORE,
      "max_score": $INVESTIGATION_MAX,
      "feedback": "$INVESTIGATION_FEEDBACK"
    },
    "test_results": {
      "passed": $TEST_PASSED,
      "output": $(echo "$TEST_OUTPUT" | python3 -c 'import json, sys; print(json.dumps(sys.stdin.read()))')
    }
  }
}
EOF

exit 0
