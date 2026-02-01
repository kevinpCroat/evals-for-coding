# Bug Fixing Benchmark: Date Range Calculator

## Overview

This benchmark evaluates an AI's ability to identify and fix a bug in a Python library. The task involves fixing an off-by-one error in a date range calculation function.

## Scenario

You are working on a Python utility library called `daterange` that provides functions for working with date ranges and calculating business days. The library has a comprehensive test suite with 18 tests. Currently, 17 tests pass but 1 test fails due to a bug in the `get_business_days()` function.

The failing test is `test_business_days_one_week_span`, which tests the calculation of business days for a date range that spans exactly one week (Monday to Sunday).

## Directory Structure

```
bug-fixing-001/
├── README.md              # This file
├── spec.md               # Detailed task specification
├── prompts.txt           # Standard prompts for AI
├── requirements.txt      # Python dependencies
├── src/                  # Source code
│   ├── __init__.py
│   └── daterange.py      # Main library (contains the bug)
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_daterange.py # Comprehensive tests (1 failing)
└── verification/         # Automated verification
    └── verify.sh         # Verification script
```

## The Bug

The `get_business_days()` function in `src/daterange.py` has an off-by-one error in its loop condition on line 95. The function is supposed to count business days inclusively (including both start and end dates), but it uses `<` instead of `<=`, causing it to exclude the end_date from the count.

This bug is exposed when the end_date is a business day (Monday-Friday). The failing test uses Monday-Friday as a test case, which should return 5 business days but incorrectly returns 4.

**Current (buggy) code (line 95):**
```python
while current_date < end_date:  # BUG: Should be <= to include end_date
```

**Correct code:**
```python
while current_date <= end_date:  # Fixed: Now includes end_date
```

This is a classic off-by-one error - a single character fix that has significant impact on correctness.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests to see the failure:
   ```bash
   python -m pytest tests/ -v
   ```

   Expected output: 17 passed, 1 failed (test_business_days_one_week_span)

## Task

Fix the bug in `src/daterange.py` so that all tests pass. The fix should be minimal - only change what's necessary to fix the bug.

## Verification

Run the verification script to check your solution:

```bash
./verification/verify.sh
```

The script will:
1. Run all tests
2. Verify the previously failing test now passes
3. Verify no other tests broke (no regressions)
4. Check that the fix is minimal
5. Output a JSON score

## Scoring

- **Bug Fixed (60%)**: The failing test `test_business_days_one_week_span` now passes
- **No Regressions (30%)**: All other tests still pass
- **Code Quality (10%)**: The fix is minimal and maintains code style

A score of 70% or higher is required to pass the benchmark.

## Expected Outcome

After fixing the bug:
- All 18 tests should pass
- Only 1 character should be changed in the source code (`<` to `<=` on line 95)
- The function should correctly handle all edge cases for business day calculation
- The verification script should output a score of 100

## Learning Objectives

This benchmark tests:
- Ability to read and understand existing code
- Ability to interpret test failures and identify root cause
- Skill in making minimal, targeted bug fixes
- Understanding of off-by-one errors
- Discipline in not over-engineering the solution

## Notes

- Do not modify the test files
- Do not change function signatures or the public API
- Use only Python standard library (no external dependencies beyond pytest)
- The bug is intentional and realistic - similar issues occur in production code
