# Bug Fixing: Date Range Calculator - Specification

## Objective

Fix a bug in a date range utility library that causes one test to fail.

## Background

You are working on a Python utility library called `daterange` that provides functions for working with date ranges. The library has a comprehensive test suite, but one test is currently failing due to a bug in the implementation.

The failing test indicates that the `get_business_days()` function has an off-by-one error - it's not including the end_date in the calculation when it should be counted inclusively.

## Requirements

### Functional Requirements
1. Identify and fix the bug causing the test failure in `src/daterange.py`
2. Ensure the fix correctly handles all edge cases for business day calculation
3. Do not modify the test suite - the tests are correct

### Technical Constraints
- Python 3.8 or higher
- Must use only Python standard library (no external dependencies)
- Must not change the function signatures or API
- Must not modify the test files

### Quality Requirements
- All existing tests must pass after the fix
- Code must maintain the existing style and structure
- The fix should be minimal - only fix what's broken
- No changes to function behavior except fixing the bug

## Success Criteria

The implementation will be considered successful when:
1. The failing test `test_business_days_one_week_span` passes
2. All other existing tests continue to pass
3. The fix correctly handles the edge case without breaking other functionality
4. No test files or function signatures have been modified

## Deliverables

1. Fixed `src/daterange.py` with the bug corrected
2. All tests passing when running `python -m pytest tests/`

## Evaluation

Your submission will be scored on:
- **Bug Fixed**: 60% - The previously failing test now passes
- **No Regressions**: 30% - All previously passing tests still pass
- **Code Quality**: 10% - The fix is minimal and maintains code style

See verification/verify.sh for automated scoring implementation.
