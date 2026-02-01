#!/bin/bash

# Concurrency-001 Verification Script
# This script verifies that race conditions have been fixed and code is thread-safe

set -euo pipefail

# Detect timeout command (macOS vs Linux)
TIMEOUT_CMD=""
if command -v timeout &> /dev/null; then
    TIMEOUT_CMD="timeout"
elif command -v gtimeout &> /dev/null; then
    TIMEOUT_CMD="gtimeout"
fi

# Function to run command with timeout
run_with_timeout() {
    local timeout_seconds=$1
    shift
    if [ -n "$TIMEOUT_CMD" ]; then
        $TIMEOUT_CMD "${timeout_seconds}s" "$@"
    else
        # No timeout available, just run the command
        "$@"
    fi
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCHMARK_DIR="$(dirname "$SCRIPT_DIR")"
STARTER_CODE_DIR="$BENCHMARK_DIR/starter-code"

# Output JSON result
output_json() {
    local score=$1
    local max_score=$2
    local status=$3
    local message=$4

    cat <<EOF
{
  "score": $score,
  "max_score": $max_score,
  "status": "$status",
  "message": "$message"
}
EOF
}

# Check if we're verifying starter-code or a submission
if [ "${1:-}" = "--starter-code" ]; then
    SUBMISSION_DIR="$STARTER_CODE_DIR"
else
    SUBMISSION_DIR="${1:-$STARTER_CODE_DIR}"
fi

cd "$SUBMISSION_DIR"

# Check required files exist
if [ ! -f "cache.py" ] || [ ! -f "counter.py" ] || [ ! -f "worker_pool.py" ] || [ ! -f "test_concurrency.py" ]; then
    output_json 0 100 "error" "Missing required files"
    exit 1
fi

# Initialize scoring
total_score=0
max_score=100
details=""

echo "========================================" >&2
echo "Concurrency-001 Verification" >&2
echo "========================================" >&2
echo "" >&2

# =============================================================================
# TEST 1: Race Condition Tests (40 points)
# Run tests 100 times, all must pass
# =============================================================================
echo "TEST 1: Race Condition Tests (40 points)" >&2
echo "Running test suite 100 times..." >&2

race_condition_score=0
max_race_condition_score=40

test_failures=0
test_successes=0
timeout_failures=0

for i in $(seq 1 100); do
    if [ $((i % 10)) -eq 0 ]; then
        echo "  Progress: $i/100 runs..." >&2
    fi

    # Run with timeout to detect deadlocks
    if run_with_timeout 10 python3 test_concurrency.py > /dev/null 2>&1; then
        ((test_successes++)) || true
    else
        exit_code=$?
        # 124 = timeout (GNU), 127 = command not found, treat both as potential timeout
        if [ $exit_code -eq 124 ] || [ $exit_code -eq 143 ]; then
            ((timeout_failures++)) || true
            echo "  Run $i: TIMEOUT (possible deadlock)" >&2
        else
            ((test_failures++)) || true
            if [ $((i % 10)) -eq 1 ] || [ $i -le 3 ]; then
                echo "  Run $i: FAILED" >&2
            fi
        fi
    fi
done

echo "  Results: $test_successes/100 passed, $test_failures failed, $timeout_failures timeouts" >&2

if [ $test_successes -eq 100 ]; then
    race_condition_score=$max_race_condition_score
    echo "  ✓ All 100 runs passed" >&2
elif [ $test_successes -ge 95 ]; then
    race_condition_score=$((max_race_condition_score * 3 / 4))
    echo "  ~ Most runs passed ($test_successes/100)" >&2
elif [ $test_successes -ge 80 ]; then
    race_condition_score=$((max_race_condition_score / 2))
    echo "  ~ Some runs passed ($test_successes/100)" >&2
elif [ $test_successes -ge 50 ]; then
    race_condition_score=$((max_race_condition_score / 4))
    echo "  ✗ Many failures ($test_failures/100 failed, $timeout_failures/100 timeout)" >&2
else
    race_condition_score=0
    echo "  ✗ Most runs failed" >&2
fi

total_score=$((total_score + race_condition_score))
details="${details}Race Condition Tests: $race_condition_score/$max_race_condition_score points ($test_successes/100 passed). "

# =============================================================================
# TEST 2: Deadlock Freedom (30 points)
# Check for proper lock usage and no deadlocks
# =============================================================================
echo "" >&2
echo "TEST 2: Deadlock Freedom (30 points)" >&2

deadlock_score=0
max_deadlock_score=30

# Check if code completes in reasonable time (run 10 more tests with longer timeout)
echo "  Checking for deadlocks..." >&2
deadlock_detected=0

for i in $(seq 1 10); do
    if ! run_with_timeout 15 python3 test_concurrency.py > /dev/null 2>&1; then
        exit_code=$?
        if [ $exit_code -eq 124 ] || [ $exit_code -eq 143 ]; then
            deadlock_detected=1
            echo "  ✗ Timeout detected on run $i (possible deadlock)" >&2
            break
        fi
    fi
done

if [ $deadlock_detected -eq 0 ] && [ $timeout_failures -eq 0 ]; then
    deadlock_score=$max_deadlock_score
    echo "  ✓ No deadlocks detected" >&2
elif [ $timeout_failures -lt 5 ]; then
    deadlock_score=$((max_deadlock_score / 2))
    echo "  ~ Some timeouts detected (possible intermittent deadlock)" >&2
else
    deadlock_score=0
    echo "  ✗ Deadlocks detected" >&2
fi

total_score=$((total_score + deadlock_score))
details="${details}Deadlock Freedom: $deadlock_score/$max_deadlock_score points. "

# =============================================================================
# TEST 3: Synchronization Correctness (20 points)
# Check for proper use of synchronization primitives
# =============================================================================
echo "" >&2
echo "TEST 3: Synchronization Correctness (20 points)" >&2

sync_score=0
max_sync_score=20

# Check for proper lock usage
echo "  Checking for synchronization primitives..." >&2

has_lock_in_cache=0
has_lock_in_counter=0
has_queue_or_lock_in_pool=0

if grep -q "threading.Lock\|threading.RLock" cache.py && grep -q "with.*lock" cache.py; then
    has_lock_in_cache=1
    echo "  ✓ cache.py uses locks" >&2
else
    echo "  ✗ cache.py missing proper lock usage" >&2
fi

if grep -q "threading.Lock\|threading.RLock" counter.py && grep -q "with.*lock" counter.py; then
    has_lock_in_counter=1
    echo "  ✓ counter.py uses locks" >&2
else
    echo "  ✗ counter.py missing proper lock usage" >&2
fi

if grep -q "queue.Queue\|threading.Lock\|threading.RLock" worker_pool.py; then
    has_queue_or_lock_in_pool=1
    echo "  ✓ worker_pool.py uses thread-safe primitives" >&2
else
    echo "  ✗ worker_pool.py missing thread-safe primitives" >&2
fi

# Check for anti-patterns (check-then-act without locks)
echo "  Checking for common anti-patterns..." >&2

has_antipatterns=0

# Look for check-then-act patterns outside of lock context
# This is a simple heuristic - not perfect but catches obvious issues
if grep -A 2 "if.*in self\." cache.py counter.py worker_pool.py 2>/dev/null | grep -v "with\|lock" | grep -q "self\."; then
    # Check if there are any if statements that might be check-then-act
    # without proper context (this is an approximation)
    echo "  ⚠ Possible check-then-act patterns detected" >&2
    has_antipatterns=1
fi

# Calculate synchronization score
sync_components=0
if [ $has_lock_in_cache -eq 1 ]; then
    sync_components=$((sync_components + 1))
fi
if [ $has_lock_in_counter -eq 1 ]; then
    sync_components=$((sync_components + 1))
fi
if [ $has_queue_or_lock_in_pool -eq 1 ]; then
    sync_components=$((sync_components + 1))
fi

sync_score=$((max_sync_score * sync_components / 3))

if [ $has_antipatterns -eq 1 ]; then
    sync_score=$((sync_score * 3 / 4))
fi

total_score=$((total_score + sync_score))
details="${details}Synchronization Correctness: $sync_score/$max_sync_score points. "

# =============================================================================
# TEST 4: Performance (10 points)
# Code should not be excessively slow from over-locking
# =============================================================================
echo "" >&2
echo "TEST 4: Performance (10 points)" >&2

performance_score=0
max_performance_score=10

echo "  Measuring execution time..." >&2

# Run tests and measure time
start_time=$(date +%s)
if run_with_timeout 60 python3 test_concurrency.py > /dev/null 2>&1; then
    end_time=$(date +%s)
    elapsed=$((end_time - start_time))

    echo "  Execution time: ${elapsed}s" >&2

    # Good: < 5 seconds (full points)
    # Acceptable: 5-15 seconds (3/4 points)
    # Slow: 15-30 seconds (1/2 points)
    # Very slow: > 30 seconds (1/4 points)

    if [ $elapsed -lt 5 ]; then
        performance_score=$max_performance_score
        echo "  ✓ Excellent performance" >&2
    elif [ $elapsed -lt 15 ]; then
        performance_score=$((max_performance_score * 3 / 4))
        echo "  ✓ Good performance" >&2
    elif [ $elapsed -lt 30 ]; then
        performance_score=$((max_performance_score / 2))
        echo "  ~ Acceptable performance" >&2
    else
        performance_score=$((max_performance_score / 4))
        echo "  ~ Slow performance (possible over-locking)" >&2
    fi
else
    performance_score=0
    echo "  ✗ Timeout or failure" >&2
fi

total_score=$((total_score + performance_score))
details="${details}Performance: $performance_score/$max_performance_score points. "

# =============================================================================
# Final Results
# =============================================================================
echo "" >&2
echo "========================================" >&2
echo "Final Score: $total_score/$max_score" >&2
echo "========================================" >&2

if [ $total_score -ge 90 ]; then
    status="pass"
    message="Excellent! All race conditions fixed. ${details}"
elif [ $total_score -ge 70 ]; then
    status="partial"
    message="Good progress, but some issues remain. ${details}"
elif [ $total_score -ge 40 ]; then
    status="partial"
    message="Race conditions partially fixed. ${details}"
else
    status="fail"
    message="Significant race conditions remain. ${details}"
fi

output_json "$total_score" "$max_score" "$status" "$message"
