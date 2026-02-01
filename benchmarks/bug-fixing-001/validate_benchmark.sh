#!/bin/bash
# Validation script to ensure benchmark is properly configured
# Run this to verify the benchmark is in the correct initial state

echo "======================================"
echo "Benchmark Validation Script"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found"
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check pytest
if ! python3 -m pytest --version &> /dev/null; then
    echo "ERROR: pytest not installed. Run: pip install pytest"
    exit 1
fi
echo "✓ pytest found: $(python3 -m pytest --version | head -1)"

# Check file structure
echo ""
echo "Checking file structure..."
required_files=(
    "README.md"
    "spec.md"
    "prompts.txt"
    "requirements.txt"
    "src/__init__.py"
    "src/daterange.py"
    "tests/__init__.py"
    "tests/test_daterange.py"
    "verification/verify.sh"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Missing required file: $file"
        exit 1
    fi
done
echo "✓ All required files present"

# Check that exactly 1 test fails
echo ""
echo "Running test suite..."
TEST_OUTPUT=$(python3 -m pytest tests/ -v 2>&1)

# Look for the summary line like "1 failed, 17 passed"
SUMMARY=$(echo "$TEST_OUTPUT" | grep "failed.*passed" | tail -1)
if ! echo "$SUMMARY" | grep -q "1 failed, 17 passed"; then
    echo "ERROR: Expected '1 failed, 17 passed' in output"
    echo "Actual summary: $SUMMARY"
    exit 1
fi

echo "✓ Test suite: 17 passed, 1 failed (as expected)"

# Check that the specific test fails
if ! echo "$TEST_OUTPUT" | grep -q "FAILED.*test_business_days_one_week_span"; then
    echo "ERROR: Expected test_business_days_one_week_span to fail"
    exit 1
fi
echo "✓ Correct test is failing: test_business_days_one_week_span"

# Check verification script
echo ""
echo "Checking verification script..."
if [ ! -x "verification/verify.sh" ]; then
    echo "ERROR: verification/verify.sh is not executable"
    chmod +x verification/verify.sh
    echo "  Fixed: made verification/verify.sh executable"
fi
echo "✓ Verification script is executable"

# Run verification (should fail with score ~10)
VERIFY_OUTPUT=$(./verification/verify.sh 2>/dev/null || true)
SCORE=$(echo "$VERIFY_OUTPUT" | grep '"final_score"' | grep -o '[0-9]\+')

if [ "$SCORE" -gt 20 ]; then
    echo "ERROR: Expected low score (<20) in buggy state, got $SCORE"
    exit 1
fi
echo "✓ Verification script works (score: $SCORE, as expected)"

# Check that bug is on correct line
if ! grep -n "while current_date < end_date:" src/daterange.py | grep -q "95:"; then
    echo "WARNING: Bug might not be on line 95 as documented"
fi

echo ""
echo "======================================"
echo "✓ Benchmark validation PASSED"
echo "======================================"
echo ""
echo "Benchmark is ready to use!"
echo "Next steps:"
echo "  1. Read prompts.txt for the task"
echo "  2. Fix the bug in src/daterange.py"
echo "  3. Run ./verification/verify.sh to check"
echo ""
