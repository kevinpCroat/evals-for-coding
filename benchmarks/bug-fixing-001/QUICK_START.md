# Quick Start Guide

## For AI Agents

1. **Install dependencies:**
   ```bash
   pip install pytest
   ```

2. **Run tests to see the failure:**
   ```bash
   python3 -m pytest tests/ -v
   ```
   You should see: `1 failed, 17 passed`

3. **Read the task:**
   ```bash
   cat prompts.txt
   ```

4. **Fix the bug in src/daterange.py**
   - Look for the off-by-one error in the `get_business_days()` function
   - Change 1 character on line 95

5. **Verify your fix:**
   ```bash
   ./verification/verify.sh
   ```
   Target score: 100

## For Human Evaluators

The bug is intentionally simple to allow for testing AI debugging capabilities:
- **Location:** `src/daterange.py`, line 95
- **Fix:** Change `<` to `<=` in the while loop condition
- **Why:** The function should count days inclusively, but currently excludes end_date

This benchmark tests:
- Code comprehension
- Test interpretation
- Minimal change discipline
- Off-by-one error recognition

## Expected Timeline

- **Fast path:** 1-2 minutes (read test failure, identify issue, fix)
- **Normal path:** 3-5 minutes (explore code, understand logic, fix)
- **Slow path:** 5-10 minutes (multiple attempts, over-thinking)

Scores:
- 100: Bug fixed, all tests pass, minimal changes
- 70: Bug fixed but with regressions or extra changes
- 0-10: Bug not fixed or significant issues
