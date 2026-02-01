# Benchmark Summary: Bug Fixing 001

## Overview
- **Name:** bug-fixing-001
- **Type:** Bug Fixing
- **Difficulty:** Easy
- **Language:** Python 3.8+
- **Domain:** Date/Time Utilities

## Characteristics

### Bug Details
- **Type:** Off-by-one error
- **Location:** Single line (src/daterange.py:95)
- **Fix complexity:** Single character change (`<` to `<=`)
- **Root cause:** Incorrect loop boundary condition

### Test Suite
- **Total tests:** 18
- **Failing initially:** 1
- **Passing after fix:** 18
- **Test framework:** pytest

### Scoring Components
1. **Bug Fixed (60%):** Target test now passes
2. **No Regressions (30%):** All other tests still pass
3. **Code Quality (10%):** Minimal changes maintained

## Quality Metrics

### Automation Rate
- **Score:** 100%
- All scoring is deterministic and automated

### Reproducibility
- **Score:** 100%
- Same fix always produces same score
- No random elements

### Discrimination
- **Good:** Distinguishes between:
  - Complete fix vs partial fix
  - Minimal change vs over-engineering
  - Understanding vs guessing

### Face Validity
- **Score:** High
- Bug is realistic (common in production code)
- Test suite is comprehensive and realistic
- Fix requires understanding, not just trial and error

## Usage Instructions

### Setup
```bash
cd /Users/kperko/code/evals-for-coding/benchmarks/bug-fixing-001
pip install -r requirements.txt
```

### Running
```bash
# See the failure
python3 -m pytest tests/ -v

# Fix the bug in src/daterange.py

# Verify the fix
./verification/verify.sh
```

### Expected Outputs

**Before fix:**
```
1 failed, 17 passed
Score: 10 (failed)
```

**After fix:**
```
18 passed
Score: 100 (passed)
```

## Success Criteria

- Score >= 70 to pass
- Perfect score (100) requires:
  - Target test passes
  - All other tests pass
  - File size unchanged significantly (minimal edit)

## Learning Objectives

This benchmark evaluates:
1. **Code Reading:** Understanding existing code structure
2. **Test Interpretation:** Using test failures to locate bugs
3. **Debugging:** Identifying root cause of off-by-one errors
4. **Discipline:** Making minimal, targeted changes
5. **Verification:** Confirming fix doesn't break anything

## Extensibility

This benchmark serves as a template for future bug-fixing benchmarks:
- Clear bug location
- Single point of failure
- Comprehensive test coverage
- Automated verification
- Realistic scenario

## Files Reference

```
bug-fixing-001/
├── README.md              - Full documentation
├── spec.md               - Task specification
├── prompts.txt           - AI prompts
├── SOLUTION.md           - Solution explanation
├── QUICK_START.md        - Quick reference
├── BENCHMARK_SUMMARY.md  - This file
├── requirements.txt      - Dependencies
├── .gitignore           - Git ignore rules
├── src/
│   ├── __init__.py      - Package init
│   └── daterange.py     - Main library (contains bug)
├── tests/
│   ├── __init__.py      - Test package init
│   └── test_daterange.py - Test suite (18 tests)
└── verification/
    └── verify.sh        - Automated scoring script
```

## Maintenance

### Updating
- If Python API changes, update imports
- If pytest changes, update test commands
- Keep tests comprehensive but focused

### Validation
- Run `./verification/verify.sh` before committing
- Ensure exactly 1 test fails initially
- Ensure all tests pass with documented fix

## Notes

- Bug is intentionally simple for baseline evaluation
- Can be used to compare different AI models
- Suitable for automated evaluation pipelines
- No external dependencies beyond pytest
