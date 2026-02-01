# Rewriting-001: Recursive to Iterative Tree Traversal

## Objective

Rewrite recursive binary tree operations to use iterative implementations with explicit stacks while preserving exact behavior and maintaining comparable performance.

## Background

Recursive tree algorithms are elegant and easy to understand, but they have limitations:
- Stack overflow risk with deep trees (recursion depth limits)
- Higher memory overhead from call stack frames
- Difficult to control execution flow (pause/resume)

Iterative implementations using explicit stacks address these issues while maintaining the same algorithmic behavior. This benchmark tests the ability to transform recursive patterns into iterative equivalents.

## Requirements

### Functional Requirements

1. **Rewrite all functions in `tree_traversal.py` from recursive to iterative**:
   - `inorder_traversal()` - Use explicit stack for in-order traversal
   - `postorder_traversal()` - Use explicit stack for post-order traversal
   - `max_depth()` - Use level-order traversal or iterative depth tracking
   - `find_path_sum()` - Use stack to track paths and running sums
   - `collect_leaves()` - Use iterative traversal to collect leaf nodes
   - `tree_map()` - Use stack to build new tree iteratively

2. **Preserve exact behavior**:
   - All functions must return identical results to the original recursive versions
   - Edge cases must be handled identically (empty trees, single nodes, etc.)
   - Order of traversal must be preserved (e.g., left-to-right for leaves)

3. **Maintain or improve performance**:
   - Iterative versions should not be significantly slower than recursive versions
   - Should handle deeper trees without stack overflow
   - Memory usage should be reasonable (explicit stack size)

### Technical Constraints

- Must use Python 3.7+
- Cannot modify the `TreeNode` class definition
- Cannot modify function signatures (names, parameters, return types)
- Must use explicit data structures (lists/deque as stacks) instead of recursion
- Cannot use helper functions that are themselves recursive
- All type hints must be preserved

### Quality Requirements

- All 40+ existing tests must pass
- Code must be readable and well-commented
- Stack operations should be clearly documented
- Performance should not degrade more than 20% on average

## Success Criteria

The implementation will be considered successful when:

1. **All unit tests pass (100%)** - Every test in `test_tree_traversal.py` must pass
2. **Edge case tests pass** - Specifically:
   - Deep recursion test (100+ level tree) passes without stack overflow
   - Large tree tests complete in reasonable time
   - Zero/negative value edge cases handled correctly
3. **Performance is comparable** - Iterative versions complete within 120% of recursive baseline time
4. **Code quality** - Functions are clearly written with appropriate comments explaining stack usage

## Deliverables

1. Modified `tree_traversal.py` with all functions rewritten iteratively
2. All functions must maintain the same signatures and behavior
3. Clear comments explaining the stack-based approach for each function

## Evaluation

Your submission will be scored on:

- **Tests Passing**: 60% - All original tests must pass
  - 60 points: All tests pass
  - Proportional points: Percentage of tests passing
  - 0 points: Less than 50% of tests passing

- **Performance Comparison**: 20% - Execution time vs baseline
  - 20 points: Within 110% of baseline
  - 15 points: Within 120% of baseline
  - 10 points: Within 150% of baseline
  - 0 points: Slower than 150% of baseline

- **Edge Cases**: 20% - Explicit edge case test handling
  - Deep recursion test (100+ levels): 10 points
  - Large tree test: 5 points
  - Special value tests (zero, negative): 5 points

**Minimum passing score: 70/100**

See `verification/verify.sh` for automated scoring implementation.

## Notes

- The recursive implementations are provided as a reference
- You may want to study iterative tree traversal patterns before starting
- Common approach: Use a stack (list) and process nodes in specific order
- For `tree_map`, consider using two stacks (one for old tree, one for new tree)
- Test your implementation incrementally - one function at a time
