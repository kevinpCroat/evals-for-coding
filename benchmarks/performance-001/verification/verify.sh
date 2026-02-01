#!/bin/bash

# Verification script for performance-001 benchmark
# Scores the AI's performance optimization

set -e

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER_CODE_DIR="$BENCHMARK_DIR/starter-code"
VERIFICATION_DIR="$BENCHMARK_DIR/verification"

# Initialize scores
TOTAL_SCORE=0
MAX_SCORE=100

# Score components
PERFORMANCE_SCORE=0
PERFORMANCE_MAX=50

CORRECTNESS_SCORE=0
CORRECTNESS_MAX=30

OPTIMIZATION_SCORE=0
OPTIMIZATION_MAX=20

# Baseline performance (seconds) - measured with slow version
BASELINE_TIME=15.0
TARGET_SPEEDUP=10.0

# --- CHECK IF TESTS PASS (30 points) ---
TEST_PASSED=false
TEST_OUTPUT=""
cd "$STARTER_CODE_DIR"

echo "Running test suite..."

# Run pytest
if command -v pytest &> /dev/null; then
    if pytest test_data_processor.py -v > /tmp/test_output.txt 2>&1; then
        TEST_PASSED=true
        TEST_OUTPUT="All tests passed"
        CORRECTNESS_SCORE=$CORRECTNESS_MAX
        echo "✓ All tests passed"
    else
        TEST_OUTPUT=$(cat /tmp/test_output.txt | tail -30)
        echo "✗ Tests failed"
    fi
else
    # Fallback to python3 -m pytest
    if python3 -m pytest test_data_processor.py -v > /tmp/test_output.txt 2>&1; then
        TEST_PASSED=true
        TEST_OUTPUT="All tests passed"
        CORRECTNESS_SCORE=$CORRECTNESS_MAX
        echo "✓ All tests passed"
    else
        TEST_OUTPUT=$(cat /tmp/test_output.txt | tail -30)
        echo "✗ Tests failed"
    fi
fi

CORRECTNESS_FEEDBACK=""
if [ "$TEST_PASSED" = true ]; then
    CORRECTNESS_FEEDBACK="All tests passed. Behavior correctly preserved."
else
    CORRECTNESS_FEEDBACK="Tests failed. Optimization broke functionality."
fi

# --- MEASURE PERFORMANCE (50 points) ---
PERFORMANCE_FEEDBACK=""
ACTUAL_TIME=0
SPEEDUP=0

if [ "$TEST_PASSED" = true ]; then
    echo ""
    echo "Measuring performance..."

    # Run benchmark with larger dataset for accurate measurement
    cat > /tmp/perf_test.py << 'EOF'
import sys
import time
sys.path.insert(0, '$STARTER_CODE_DIR')

from data_processor import LogProcessor, generate_test_logs

# Generate test data
logs = generate_test_logs(num_users=1000, entries_per_user=5)

# Warm up
processor = LogProcessor()
processor.load_logs(logs)
processor.process_all()

# Measure 3 runs
times = []
for i in range(3):
    processor = LogProcessor()
    processor.load_logs(logs)
    start = time.time()
    result = processor.process_all()
    elapsed = time.time() - start
    times.append(elapsed)

avg_time = sum(times) / len(times)
print(f"{avg_time:.3f}")
EOF

    # Replace $STARTER_CODE_DIR in the script
    sed -i.bak "s|\$STARTER_CODE_DIR|$STARTER_CODE_DIR|g" /tmp/perf_test.py

    # Run performance test
    if ACTUAL_TIME=$(python3 /tmp/perf_test.py 2>/dev/null); then
        SPEEDUP=$(python3 -c "print(f'{$BASELINE_TIME / $ACTUAL_TIME:.2f}')")

        echo "  Baseline: ${BASELINE_TIME}s"
        echo "  Optimized: ${ACTUAL_TIME}s"
        echo "  Speedup: ${SPEEDUP}x"

        # Calculate performance score based on speedup
        # Full points at 10x+, linear scaling from 1x to 10x
        PERFORMANCE_SCORE=$(python3 << PYEOF
import sys
speedup = float($SPEEDUP)
max_score = $PERFORMANCE_MAX
target = $TARGET_SPEEDUP

if speedup >= target:
    score = max_score
elif speedup >= 1.0:
    # Linear interpolation: 0 points at 1x, full points at 10x
    score = int((speedup - 1.0) / (target - 1.0) * max_score)
else:
    score = 0

print(score)
PYEOF
)

        if (( $(python3 -c "print($SPEEDUP >= $TARGET_SPEEDUP)") )); then
            PERFORMANCE_FEEDBACK="Excellent! Achieved ${SPEEDUP}x speedup (target: ${TARGET_SPEEDUP}x)"
        elif (( $(python3 -c "print($SPEEDUP >= 5.0)") )); then
            PERFORMANCE_FEEDBACK="Good speedup of ${SPEEDUP}x but below ${TARGET_SPEEDUP}x target"
        elif (( $(python3 -c "print($SPEEDUP >= 2.0)") )); then
            PERFORMANCE_FEEDBACK="Moderate speedup of ${SPEEDUP}x. Need significant improvements to reach ${TARGET_SPEEDUP}x target"
        else
            PERFORMANCE_FEEDBACK="Minimal speedup of ${SPEEDUP}x. Major optimizations needed"
        fi
    else
        PERFORMANCE_FEEDBACK="Failed to measure performance - code may have runtime errors"
        ACTUAL_TIME=999.0
        SPEEDUP=0.0
    fi
else
    PERFORMANCE_FEEDBACK="Cannot measure performance - tests must pass first"
    ACTUAL_TIME=999.0
    SPEEDUP=0.0
fi

# --- ANALYZE OPTIMIZATION QUALITY (20 points) ---
OPTIMIZATION_FEEDBACK=""
CODE_CONTENT=$(cat "$STARTER_CODE_DIR/data_processor.py")

# Check for key optimization indicators
USED_CACHING=false
USED_DICT_STRUCTURES=false
USED_BUILTIN_SORT=false
REDUCED_REGEX=false
IMPROVED_ALGORITHM=false

# Check for caching/parsing once
if echo "$CODE_CONTENT" | grep -q -i "cache\|_parsed\|parse.*once"; then
    USED_CACHING=true
    OPTIMIZATION_SCORE=$((OPTIMIZATION_SCORE + 5))
fi

# Check for dict/defaultdict usage
if echo "$CODE_CONTENT" | grep -q "defaultdict\|from collections import"; then
    USED_DICT_STRUCTURES=true
    OPTIMIZATION_SCORE=$((OPTIMIZATION_SCORE + 4))
elif echo "$CODE_CONTENT" | grep -q "dict()\|{}"; then
    USED_DICT_STRUCTURES=true
    OPTIMIZATION_SCORE=$((OPTIMIZATION_SCORE + 3))
fi

# Check for built-in sorting
if echo "$CODE_CONTENT" | grep -q "sorted(\|\.sort("; then
    USED_BUILTIN_SORT=true
    OPTIMIZATION_SCORE=$((OPTIMIZATION_SCORE + 4))
fi

# Check if bubble sort was removed
if ! echo "$CODE_CONTENT" | grep -q "for i in range.*for j in range"; then
    REDUCED_REGEX=true
    OPTIMIZATION_SCORE=$((OPTIMIZATION_SCORE + 4))
fi

# Check for reduced complexity indicators
if echo "$CODE_CONTENT" | grep -q -E "enumerate|items\(\)|\.items|\.keys|\.values"; then
    IMPROVED_ALGORITHM=true
    OPTIMIZATION_SCORE=$((OPTIMIZATION_SCORE + 3))
fi

# Build optimization feedback
OPTIMIZATION_FEEDBACK="Code analysis: "
FOUND_OPTS=""

[ "$USED_CACHING" = true ] && FOUND_OPTS="${FOUND_OPTS}Caching/parsing once ✓ "
[ "$USED_DICT_STRUCTURES" = true ] && FOUND_OPTS="${FOUND_OPTS}Dictionary structures ✓ "
[ "$USED_BUILTIN_SORT" = true ] && FOUND_OPTS="${FOUND_OPTS}Built-in sort ✓ "
[ "$REDUCED_REGEX" = true ] && FOUND_OPTS="${FOUND_OPTS}Removed nested loops ✓ "
[ "$IMPROVED_ALGORITHM" = true ] && FOUND_OPTS="${FOUND_OPTS}Better algorithms ✓ "

if [ -n "$FOUND_OPTS" ]; then
    OPTIMIZATION_FEEDBACK="${OPTIMIZATION_FEEDBACK}${FOUND_OPTS}"
else
    OPTIMIZATION_FEEDBACK="${OPTIMIZATION_FEEDBACK}No clear optimization patterns detected"
fi

# Bonus points if speedup is exceptional
if (( $(python3 -c "print($SPEEDUP >= 20.0)") )); then
    BONUS=5
    OPTIMIZATION_SCORE=$((OPTIMIZATION_SCORE + BONUS))
    OPTIMIZATION_SCORE=$((OPTIMIZATION_SCORE > OPTIMIZATION_MAX ? OPTIMIZATION_MAX : OPTIMIZATION_SCORE))
fi

# Calculate total score
TOTAL_SCORE=$((PERFORMANCE_SCORE + CORRECTNESS_SCORE + OPTIMIZATION_SCORE))

# Output JSON result
cat <<EOF
{
  "score": $TOTAL_SCORE,
  "max_score": $MAX_SCORE,
  "test_passed": $TEST_PASSED,
  "baseline_time": $BASELINE_TIME,
  "optimized_time": $ACTUAL_TIME,
  "speedup": $SPEEDUP,
  "target_speedup": $TARGET_SPEEDUP,
  "details": {
    "performance": {
      "score": $PERFORMANCE_SCORE,
      "max_score": $PERFORMANCE_MAX,
      "feedback": "$PERFORMANCE_FEEDBACK",
      "baseline_seconds": $BASELINE_TIME,
      "optimized_seconds": $ACTUAL_TIME,
      "speedup_factor": $SPEEDUP
    },
    "correctness": {
      "score": $CORRECTNESS_SCORE,
      "max_score": $CORRECTNESS_MAX,
      "feedback": "$CORRECTNESS_FEEDBACK",
      "all_tests_passed": $TEST_PASSED
    },
    "optimization_quality": {
      "score": $OPTIMIZATION_SCORE,
      "max_score": $OPTIMIZATION_MAX,
      "feedback": "$OPTIMIZATION_FEEDBACK",
      "optimizations_found": {
        "used_caching": $USED_CACHING,
        "used_dict_structures": $USED_DICT_STRUCTURES,
        "used_builtin_sort": $USED_BUILTIN_SORT,
        "removed_nested_loops": $REDUCED_REGEX,
        "improved_algorithms": $IMPROVED_ALGORITHM
      }
    },
    "test_results": {
      "passed": $TEST_PASSED,
      "output": $(echo "$TEST_OUTPUT" | python3 -c 'import json, sys; print(json.dumps(sys.stdin.read()))')
    }
  }
}
EOF

exit 0
