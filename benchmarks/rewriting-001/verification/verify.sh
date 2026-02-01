#!/bin/bash
# Benchmark Verification Script for rewriting-001
# Tests recursive-to-iterative tree traversal rewrite
# Outputs JSON with scoring details

set -e

BENCHMARK_NAME="rewriting-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER_DIR="${BENCHMARK_DIR}/starter-code"

# Initialize scoring components (using separate variables instead of associative arrays)
tests_passing_score=0
performance_score=0
edge_cases_score=0

tests_passing_weight=0.6
performance_weight=0.2
edge_cases_weight=0.2

# Change to starter directory
cd "${STARTER_DIR}"

echo "Running verification for ${BENCHMARK_NAME}..." >&2
echo "Working directory: ${STARTER_DIR}" >&2

# Component 1: Run all tests (60% weight)
echo "Running all tests..." >&2
if python3 -m pytest test_tree_traversal.py -v --tb=short > /tmp/test_output.txt 2>&1; then
    passed_tests=$(grep -c "PASSED" /tmp/test_output.txt || echo "0")
    total_tests=$(grep -E "[0-9]+ passed" /tmp/test_output.txt | grep -oE "[0-9]+" | head -1 || echo "1")

    if [ "$total_tests" -eq 0 ]; then
        total_tests=1
    fi

    pass_rate=$(echo "scale=2; ($passed_tests / $total_tests) * 100" | bc -l)

    # Score based on pass rate
    if (( $(echo "$pass_rate >= 50" | bc -l) )); then
        tests_passing_score=$(printf "%.0f" "$pass_rate")
    else
        tests_passing_score=0
    fi

    echo "Tests: ${passed_tests}/${total_tests} passed (${pass_rate}%)" >&2
else
    # Tests failed to run or some failed
    if [ -f /tmp/test_output.txt ]; then
        passed_tests=$(grep -c "PASSED" /tmp/test_output.txt || echo "0")
        failed_tests=$(grep -c "FAILED" /tmp/test_output.txt || echo "0")
        total_tests=$((passed_tests + failed_tests))

        if [ "$total_tests" -eq 0 ]; then
            total_tests=1
        fi

        pass_rate=$(echo "scale=2; ($passed_tests / $total_tests) * 100" | bc -l)

        if (( $(echo "$pass_rate >= 50" | bc -l) )); then
            tests_passing_score=$(printf "%.0f" "$pass_rate")
        else
            tests_passing_score=0
        fi

        echo "Tests: ${passed_tests}/${total_tests} passed (${pass_rate}%)" >&2
    else
        tests_passing_score=0
        echo "Tests: Failed to run" >&2
    fi
fi

# Component 2: Performance comparison (20% weight)
echo "Running performance comparison..." >&2

# Create a performance test script
cat > /tmp/perf_test.py << 'PERFTEST'
import time
import sys
from tree_traversal import TreeNode, inorder_traversal, postorder_traversal, max_depth, find_path_sum, collect_leaves, tree_map

def create_balanced_tree(depth, val=1):
    """Create a balanced binary tree of given depth."""
    if depth == 0:
        return None
    node = TreeNode(val)
    node.left = create_balanced_tree(depth - 1, val * 2)
    node.right = create_balanced_tree(depth - 1, val * 2 + 1)
    return node

def create_skewed_tree(depth):
    """Create a left-skewed tree."""
    if depth == 0:
        return None
    root = TreeNode(depth)
    current = root
    for i in range(depth - 1, 0, -1):
        current.left = TreeNode(i)
        current = current.left
    return root

# Test trees
balanced_tree = create_balanced_tree(10)  # 1023 nodes
skewed_tree = create_skewed_tree(100)     # 100 nodes, deep

# Run performance tests
tests = [
    ("inorder_balanced", lambda: inorder_traversal(balanced_tree)),
    ("inorder_skewed", lambda: inorder_traversal(skewed_tree)),
    ("postorder_balanced", lambda: postorder_traversal(balanced_tree)),
    ("max_depth_skewed", lambda: max_depth(skewed_tree)),
    ("find_path_sum", lambda: find_path_sum(balanced_tree, 100)),
    ("collect_leaves", lambda: collect_leaves(balanced_tree)),
    ("tree_map", lambda: tree_map(balanced_tree, lambda x: x * 2)),
]

total_time = 0
for name, test_func in tests:
    start = time.perf_counter()
    for _ in range(100):  # Run 100 iterations
        test_func()
    elapsed = time.perf_counter() - start
    total_time += elapsed

print(f"{total_time:.6f}")
PERFTEST

# Run performance test (set PYTHONPATH so imports work)
if PYTHONPATH="${STARTER_DIR}:${PYTHONPATH}" python3 /tmp/perf_test.py > /tmp/perf_result.txt 2>&1; then
    actual_time=$(cat /tmp/perf_result.txt)

    # Baseline time (approximate expected time for iterative version)
    # This is based on the recursive implementation performance
    # Iterative should be within 120% of this
    baseline_time="0.1"  # seconds for all tests

    # Calculate performance ratio
    ratio=$(echo "scale=2; $actual_time / $baseline_time" | bc -l)

    echo "Performance: ${actual_time}s (baseline: ${baseline_time}s, ratio: ${ratio}x)" >&2

    # Score based on performance
    if (( $(echo "$ratio <= 1.1" | bc -l) )); then
        performance_score=100
    elif (( $(echo "$ratio <= 1.2" | bc -l) )); then
        performance_score=75
    elif (( $(echo "$ratio <= 1.5" | bc -l) )); then
        performance_score=50
    else
        performance_score=0
    fi
else
    performance_score=0
    echo "Performance: Test failed to run" >&2
fi

# Component 3: Edge case tests (20% weight)
echo "Running edge case tests..." >&2

edge_case_score=0

# Test 1: Deep recursion test (10 points = 50% of edge case score)
if python3 -m pytest test_tree_traversal.py::TestEdgeCases::test_deep_recursion_inorder -v > /tmp/edge1.txt 2>&1; then
    edge_case_score=$((edge_case_score + 50))
    echo "Edge case 1 (deep recursion inorder): PASSED" >&2
else
    echo "Edge case 1 (deep recursion inorder): FAILED" >&2
fi

# Test 2: Deep max_depth test (5 points = 25% of edge case score)
if python3 -m pytest test_tree_traversal.py::TestEdgeCases::test_deep_recursion_max_depth -v > /tmp/edge2.txt 2>&1; then
    edge_case_score=$((edge_case_score + 25))
    echo "Edge case 2 (deep max_depth): PASSED" >&2
else
    echo "Edge case 2 (deep max_depth): FAILED" >&2
fi

# Test 3: Path sum with zero (5 points = 25% of edge case score)
if python3 -m pytest test_tree_traversal.py::TestEdgeCases::test_path_sum_with_zero -v > /tmp/edge3.txt 2>&1; then
    edge_case_score=$((edge_case_score + 25))
    echo "Edge case 3 (path sum with zero): PASSED" >&2
else
    echo "Edge case 3 (path sum with zero): FAILED" >&2
fi

edge_cases_score=$edge_case_score

# Calculate base score (weighted sum)
tests_weighted=$(echo "$tests_passing_score * $tests_passing_weight" | bc -l)
performance_weighted=$(echo "$performance_score * $performance_weight" | bc -l)
edge_cases_weighted=$(echo "$edge_cases_score * $edge_cases_weight" | bc -l)

base_score=$(echo "$tests_weighted + $performance_weighted + $edge_cases_weighted" | bc -l)
base_score=$(printf "%.0f" "$base_score")

# Calculate penalties (none for this benchmark)
time_penalty=0
iteration_penalty=0
error_penalty=0

# Calculate final score
penalty_multiplier=$(echo "1.0 - ($time_penalty + $iteration_penalty + $error_penalty)" | bc -l)
final_score=$(echo "$base_score * $penalty_multiplier" | bc -l)
final_score=$(printf "%.0f" "$final_score")

# Determine pass/fail
passed="false"
if (( final_score >= 70 )); then
    passed="true"
fi

echo "Final score: ${final_score}/100" >&2

# Output JSON
cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "components": {
    "tests_passing": {
      "score": ${tests_passing_score},
      "weight": ${tests_passing_weight},
      "description": "Percentage of tests passing"
    },
    "performance": {
      "score": ${performance_score},
      "weight": ${performance_weight},
      "description": "Performance compared to baseline"
    },
    "edge_cases": {
      "score": ${edge_cases_score},
      "weight": ${edge_cases_weight},
      "description": "Edge case test handling"
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

# Exit with appropriate code
if [ "$passed" = "true" ]; then
    exit 0
else
    exit 1
fi
