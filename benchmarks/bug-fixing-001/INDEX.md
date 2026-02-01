# Bug-Fixing-001 Benchmark Index

## Quick Links

- **[README.md](README.md)** - Complete documentation and overview
- **[prompts.txt](prompts.txt)** - Task prompt to give to AI (START HERE for AI)
- **[spec.md](spec.md)** - Formal specification
- **[QUICK_START.md](QUICK_START.md)** - Quick reference guide
- **[SOLUTION.md](SOLUTION.md)** - Solution and explanation
- **[BENCHMARK_SUMMARY.md](BENCHMARK_SUMMARY.md)** - Comprehensive benchmark details

## For AI Agents

1. Read: [prompts.txt](prompts.txt)
2. Fix: `src/daterange.py`
3. Verify: Run `./verification/verify.sh`

## For Humans

Run `./validate_benchmark.sh` to confirm benchmark is properly set up.

## Directory Structure

```
bug-fixing-001/
├── Documentation
│   ├── README.md              - Main documentation
│   ├── spec.md               - Task specification
│   ├── prompts.txt           - AI task prompt
│   ├── SOLUTION.md           - Solution guide
│   ├── QUICK_START.md        - Quick reference
│   ├── BENCHMARK_SUMMARY.md  - Detailed metrics
│   └── INDEX.md              - This file
│
├── Source Code
│   ├── src/
│   │   ├── __init__.py       - Package init
│   │   └── daterange.py      - Library with bug (FIX THIS)
│   └── tests/
│       ├── __init__.py       - Test package init
│       └── test_daterange.py - Test suite (18 tests)
│
├── Verification
│   └── verification/
│       └── verify.sh         - Automated scoring
│
├── Utilities
│   ├── validate_benchmark.sh - Benchmark validation
│   ├── requirements.txt      - Python dependencies
│   └── .gitignore           - Git ignore patterns
│
└── Current State
    └── 1 failing test, 17 passing (ready for AI)
```

## Key Metrics

- **Language:** Python 3.8+
- **Tests:** 18 total (1 failing initially)
- **Fix:** 1 character change
- **Difficulty:** Easy
- **Time:** 2-5 minutes expected
- **Pass Score:** 70+
- **Perfect Score:** 100

## Benchmark Quality

- ✓ 100% automated scoring
- ✓ 100% reproducible
- ✓ Realistic bug (off-by-one error)
- ✓ Comprehensive tests
- ✓ Clear success criteria
- ✓ No manual review needed
