# Debugging Benchmark: LRU Cache Bug

## Objective

Identify and fix a subtle bug in an LRU (Least Recently Used) cache implementation. This benchmark tests your ability to investigate, diagnose the ROOT CAUSE, create a minimal reproduction, and implement a proper fix.

## Background

An LRU cache evicts the least recently used item when it reaches capacity. Items are marked as "recently used" when they are accessed (`get`) or added/updated (`put`).

The implementation in `starter-code/lru_cache.py` has a subtle bug that causes incorrect behavior in a specific edge case.

## Requirements

### Functional Requirements
1. Identify the ROOT CAUSE of the bug (not just symptoms)
2. Create a minimal reproduction case that isolates the bug
3. Document your investigation process and findings
4. Fix the bug in `lru_cache.py`

### Technical Constraints
- Do not change the test file (except to add your minimal reproduction if desired)
- Maintain the existing API of the LRUCache class
- The fix should address the root cause, not work around symptoms

### Quality Requirements
- All existing tests must pass after your fix
- Your root cause explanation must be technically accurate
- Your minimal reproduction should be as simple as possible

## Success Criteria

The implementation will be considered successful when:
1. You correctly identify the root cause of the bug
2. You provide a clear, minimal reproduction case
3. All tests pass after your fix
4. Your fix addresses the root cause (not just the symptom)

## Deliverables

Create a file named `ROOT_CAUSE_ANALYSIS.md` that includes:

1. **Bug Investigation** (20%)
   - Document your investigation process
   - What did you observe from the failing test?
   - What hypotheses did you explore?
   - How did you narrow down the issue?

2. **Root Cause Identification** (60%)
   - What is the ROOT CAUSE of the bug?
   - Why does this cause the observed failure?
   - Explain the logical flaw in the current implementation
   - Be specific about which lines of code are problematic and WHY

3. **Minimal Reproduction** (20%)
   - Provide a minimal code snippet that reproduces JUST this bug
   - Strip away unnecessary complexity
   - Show the exact sequence of operations that triggers the issue

4. **Fix**
   - Provide the corrected code
   - Explain WHY your fix addresses the root cause
   - Ensure all tests pass after your fix

## Important Notes

- We are looking for **root cause analysis**, not just a fix
- The bug is NOT a simple typo or syntax error - it requires understanding the logic
- Focus on explaining WHY the bug occurs, not just WHAT is wrong
- Your minimal reproduction should be as simple as possible while still demonstrating the bug

## Getting Started

1. Run the tests to see the failure:
   ```bash
   pytest test_lru_cache.py -v
   ```

2. Investigate the failing test
3. Analyze the code to understand what's happening
4. Document your findings in `ROOT_CAUSE_ANALYSIS.md`
5. Fix the bug in `lru_cache.py`
6. Verify all tests pass

## Evaluation

Your submission will be scored on:
- **Root Cause Accuracy**: 60% - Correctly identifying the actual cause of the bug
- **Minimal Reproduction**: 20% - Quality and simplicity of reproduction case
- **Investigation Documentation**: 20% - Clarity and thoroughness of analysis

See verification/verify.sh for automated scoring implementation.
