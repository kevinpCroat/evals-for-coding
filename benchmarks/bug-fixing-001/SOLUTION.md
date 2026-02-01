# Solution for Bug Fixing Benchmark 001

## The Bug

The bug is in `/Users/kperko/code/evals-for-coding/benchmarks/bug-fixing-001/src/daterange.py` at line 95.

The `get_business_days()` function uses `<` instead of `<=` in the while loop condition, causing it to exclude the end_date from the calculation.

## The Fix

Change line 95 from:
```python
while current_date < end_date:  # BUG: Should be <= to include end_date
```

To:
```python
while current_date <= end_date:  # Fixed: Now includes end_date
```

## Why This Fixes It

The function is supposed to count business days **inclusively** - meaning both the start_date and end_date should be included in the count if they are business days.

The original code used `current_date < end_date`, which means the loop stops before checking the end_date. This causes an off-by-one error whenever the end_date is a business day.

For example:
- Monday to Friday (inclusive) should be 5 business days
- With the bug: loop runs for Mon, Tue, Wed, Thu (stops before Fri) = 4 days
- With the fix: loop runs for Mon, Tue, Wed, Thu, Fri = 5 days

The bug was not exposed in tests that ended on weekends because excluding a weekend day from the count didn't change the result. The failing test specifically uses Friday as the end_date to expose this off-by-one error.

## Verification

After making this single-character change, all 18 tests should pass:

```bash
python3 -m pytest tests/ -v
```

Expected output:
```
============================== 18 passed in 0.01s ==============================
```

The verification script will give a score of 100:
```bash
./verification/verify.sh
```
