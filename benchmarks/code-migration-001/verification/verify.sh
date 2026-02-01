#!/bin/bash

# Code Migration Benchmark - Verification Script
# Tests SQLAlchemy 1.4 to 2.0 migration

set -e

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER_CODE_DIR="$BENCHMARK_DIR/starter-code"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize scores
TESTS_SCORE=0
TESTS_WEIGHT=0.60
DEPRECATION_SCORE=0
DEPRECATION_WEIGHT=0.20
BUILD_SCORE=0
BUILD_WEIGHT=0.20

# Details for each component
TESTS_DETAILS=""
DEPRECATION_DETAILS=""
BUILD_DETAILS=""

echo -e "${YELLOW}=== Code Migration Benchmark: SQLAlchemy 1.4 to 2.0 ===${NC}" >&2
echo "" >&2

# Change to starter-code directory
cd "$STARTER_CODE_DIR"

# Component 1: Build/Installation Check (20% weight)
echo -e "${YELLOW}[1/3] Checking build and installation...${NC}" >&2

# Create a virtual environment for testing
TEMP_VENV=$(mktemp -d)/venv
python3 -m venv "$TEMP_VENV" 2>/dev/null

# Activate virtual environment
source "$TEMP_VENV/bin/activate"

# Try to install requirements
if pip install -q -r requirements.txt 2>/dev/null; then
    # Check if SQLAlchemy 2.0+ is installed
    SQLALCHEMY_VERSION=$(python -c "import sqlalchemy; print(sqlalchemy.__version__)" 2>/dev/null || echo "0.0.0")
    MAJOR_VERSION=$(echo "$SQLALCHEMY_VERSION" | cut -d. -f1)
    MINOR_VERSION=$(echo "$SQLALCHEMY_VERSION" | cut -d. -f2)

    if [ "$MAJOR_VERSION" -ge 2 ]; then
        BUILD_SCORE=100
        BUILD_DETAILS="Installation successful. SQLAlchemy version: $SQLALCHEMY_VERSION (2.0+)"
        echo -e "${GREEN}✓ Build successful - SQLAlchemy $SQLALCHEMY_VERSION${NC}" >&2
    else
        BUILD_SCORE=0
        BUILD_DETAILS="Wrong SQLAlchemy version: $SQLALCHEMY_VERSION (expected 2.0+)"
        echo -e "${RED}✗ Wrong SQLAlchemy version: $SQLALCHEMY_VERSION${NC}" >&2
    fi
else
    BUILD_SCORE=0
    BUILD_DETAILS="Failed to install requirements"
    echo -e "${RED}✗ Installation failed${NC}" >&2
fi

# Component 2: Test Suite (60% weight)
echo -e "${YELLOW}[2/3] Running test suite...${NC}" >&2

if [ "$BUILD_SCORE" -eq 100 ]; then
    # Run tests and capture output
    if pytest test_database.py -v --tb=short > /tmp/test_output.txt 2>&1; then
        # All tests passed
        PASSED_TESTS=$(grep -c "PASSED" /tmp/test_output.txt || echo "0")
        TOTAL_TESTS=$(grep -E "passed|failed" /tmp/test_output.txt | tail -1 | grep -oE "[0-9]+ passed" | grep -oE "[0-9]+" || echo "0")

        if [ "$TOTAL_TESTS" -gt 0 ]; then
            TESTS_SCORE=100
            TESTS_DETAILS="All $TOTAL_TESTS tests passed"
            echo -e "${GREEN}✓ All tests passed ($TOTAL_TESTS/$TOTAL_TESTS)${NC}" >&2
        else
            TESTS_SCORE=0
            TESTS_DETAILS="No tests found or executed"
            echo -e "${RED}✗ No tests executed${NC}" >&2
        fi
    else
        # Some tests failed
        PASSED_TESTS=$(grep -c "PASSED" /tmp/test_output.txt || echo "0")
        FAILED_TESTS=$(grep -c "FAILED" /tmp/test_output.txt || echo "0")
        TOTAL_TESTS=$((PASSED_TESTS + FAILED_TESTS))

        if [ "$TOTAL_TESTS" -gt 0 ]; then
            TESTS_SCORE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
            TESTS_DETAILS="$PASSED_TESTS/$TOTAL_TESTS tests passed, $FAILED_TESTS failed"
            echo -e "${RED}✗ Tests failed ($PASSED_TESTS/$TOTAL_TESTS passed)${NC}" >&2
        else
            TESTS_SCORE=0
            TESTS_DETAILS="Tests crashed or could not run"
            echo -e "${RED}✗ Tests could not run${NC}" >&2
        fi
    fi
else
    TESTS_SCORE=0
    TESTS_DETAILS="Skipped due to build failure"
    echo -e "${YELLOW}⊘ Tests skipped (build failed)${NC}" >&2
fi

# Component 3: Deprecation Warnings Check (20% weight)
echo -e "${YELLOW}[3/3] Checking for deprecation warnings...${NC}" >&2

if [ "$BUILD_SCORE" -eq 100 ]; then
    # Run tests with deprecation warnings
    if pytest test_database.py -v -W default::DeprecationWarning 2>&1 | tee /tmp/deprecation_output.txt | grep -i "deprecationwarning" > /dev/null; then
        # Found deprecation warnings
        WARNING_COUNT=$(grep -ci "deprecationwarning" /tmp/deprecation_output.txt || echo "0")

        # Check specifically for SQLAlchemy deprecation warnings
        SQLALCHEMY_WARNINGS=$(grep -i "sqlalchemy.*deprecat" /tmp/deprecation_output.txt | wc -l || echo "0")

        if [ "$SQLALCHEMY_WARNINGS" -gt 0 ]; then
            DEPRECATION_SCORE=0
            DEPRECATION_DETAILS="Found $SQLALCHEMY_WARNINGS SQLAlchemy deprecation warnings"
            echo -e "${RED}✗ Found SQLAlchemy deprecation warnings ($SQLALCHEMY_WARNINGS)${NC}" >&2
        else
            # Non-SQLAlchemy warnings (might be from other libraries)
            DEPRECATION_SCORE=80
            DEPRECATION_DETAILS="Found $WARNING_COUNT deprecation warnings (not SQLAlchemy specific)"
            echo -e "${YELLOW}⚠ Found deprecation warnings, but not SQLAlchemy specific${NC}" >&2
        fi
    else
        # No deprecation warnings
        DEPRECATION_SCORE=100
        DEPRECATION_DETAILS="No deprecation warnings detected"
        echo -e "${GREEN}✓ No deprecation warnings${NC}" >&2
    fi
else
    DEPRECATION_SCORE=0
    DEPRECATION_DETAILS="Skipped due to build failure"
    echo -e "${YELLOW}⊘ Deprecation check skipped (build failed)${NC}" >&2
fi

# Deactivate and cleanup virtual environment
deactivate
rm -rf "$(dirname "$TEMP_VENV")"

# Calculate final score
BASE_SCORE=$(echo "scale=2; ($TESTS_SCORE * $TESTS_WEIGHT) + ($DEPRECATION_SCORE * $DEPRECATION_WEIGHT) + ($BUILD_SCORE * $BUILD_WEIGHT)" | bc)
FINAL_SCORE=$(printf "%.0f" "$BASE_SCORE")

# Determine pass/fail (need at least 70%)
if [ "$FINAL_SCORE" -ge 70 ]; then
    PASSED=true
    PASS_TEXT="${GREEN}PASSED${NC}"
else
    PASSED=false
    PASS_TEXT="${RED}FAILED${NC}"
fi

echo "" >&2
echo -e "${YELLOW}=== Results ===${NC}" >&2
echo -e "Tests:        $TESTS_SCORE/100 (weight: $TESTS_WEIGHT)" >&2
echo -e "Deprecation:  $DEPRECATION_SCORE/100 (weight: $DEPRECATION_WEIGHT)" >&2
echo -e "Build:        $BUILD_SCORE/100 (weight: $BUILD_WEIGHT)" >&2
echo -e "Final Score:  $FINAL_SCORE/100" >&2
echo -e "Status:       $PASS_TEXT" >&2
echo "" >&2

# Output JSON results
cat << EOF
{
  "benchmark": "code-migration-001",
  "timestamp": "$TIMESTAMP",
  "components": {
    "tests": {
      "score": $TESTS_SCORE,
      "weight": $TESTS_WEIGHT,
      "details": "$TESTS_DETAILS"
    },
    "deprecation_warnings": {
      "score": $DEPRECATION_SCORE,
      "weight": $DEPRECATION_WEIGHT,
      "details": "$DEPRECATION_DETAILS"
    },
    "build": {
      "score": $BUILD_SCORE,
      "weight": $BUILD_WEIGHT,
      "details": "$BUILD_DETAILS"
    }
  },
  "base_score": $BASE_SCORE,
  "final_score": $FINAL_SCORE,
  "passed": $PASSED
}
EOF

# Exit with appropriate code
if [ "$PASSED" = true ]; then
    exit 0
else
    exit 1
fi
