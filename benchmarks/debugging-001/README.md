# Debugging-001: Root Cause Analysis

This benchmark evaluates an AI's ability to identify the ROOT CAUSE of a subtle bug, not just fix it.

## Overview

**Skill Tested:** Debugging and Root Cause Analysis

**Task:** Investigate a failing test in an LRU cache implementation, identify the root cause of the bug, document the analysis process, create a minimal reproduction case, and fix the bug.

**Difficulty:** Medium

**Time Estimate:** 20-30 minutes for a human developer

## What Makes This Benchmark Unique

Unlike benchmarks that just test if an AI can fix code, this benchmark evaluates:

1. **Investigation Skills** - Can the AI methodically explore the problem?
2. **Root Cause Identification** - Can the AI identify WHY the bug occurs, not just WHAT is broken?
3. **Minimal Reproduction** - Can the AI distill the problem to its essence?
4. **Documentation** - Can the AI clearly communicate their findings?

## The Bug

The LRU cache implementation has a subtle logic error in its eviction mechanism. When the cache is at capacity and needs to evict an item:

- The code gets the LRU (least recently used) key correctly
- **BUG**: It then overwrites that key's value instead of deleting the entry and adding the new key
- This causes the new key to never actually be added (unless it's the same as the LRU key)

This is a realistic production-level bug that requires understanding the code flow, not just pattern matching error messages.

## Scoring Components

The verification script scores three components:

1. **Root Cause Analysis (60 points)**
   - Correctly identifies that LRU key is being reused/overwritten (15 pts)
   - Explains that value is assigned to wrong key (15 pts)
   - Mentions need to delete old entry (10 pts)
   - References specific lines of code (10 pts)
   - Understands that new entry is never added (10 pts)

2. **Minimal Reproduction (20 points)**
   - Provides a minimal reproduction case (5 pts)
   - Shows the basic pattern (5 pts)
   - Uses small capacity (1-2) for simplicity (5 pts)
   - Demonstrates the wrong behavior (5 pts)

3. **Investigation Documentation (20 points)**
   - Documents investigation process (5 pts)
   - Describes test failure observation (5 pts)
   - Shows hypothesis exploration (5 pts)
   - Demonstrates code analysis (5 pts)

**Penalty:** If tests don't pass after the fix, all scores are halved.

## Directory Structure

```
debugging-001/
├── README.md              # This file
├── spec.md               # Task specification for AI
├── prompts.txt           # Standard prompts
├── starter-code/
│   ├── lru_cache.py      # Buggy LRU cache implementation
│   └── test_lru_cache.py # Test suite (5 tests fail)
└── verification/
    ├── SOLUTION.md       # Reference solution for scoring
    └── verify.sh         # Automated scoring script
```

## Expected AI Workflow

1. Run tests to see failures
2. Examine failing test `test_evict_and_readd_same_key`
3. Read and analyze the `put()` method in `lru_cache.py`
4. Identify that lines 47-50 overwrite the LRU key instead of deleting it
5. Create minimal reproduction case
6. Document findings in `ROOT_CAUSE_ANALYSIS.md`
7. Fix the bug by replacing the eviction logic
8. Verify all tests pass

## Common Pitfalls

- **Surface-level fix**: Just making tests pass without understanding why
- **No minimal repro**: Not distilling the problem to its simplest form
- **Vague explanation**: Saying "there's a bug in put()" without explaining the logic flaw
- **Missing investigation**: Not documenting the thought process

## Verification

Run the verification script:
```bash
./verification/verify.sh
```

This will:
1. Check for `ROOT_CAUSE_ANALYSIS.md` in starter-code/
2. Score the root cause explanation using pattern matching
3. Score the minimal reproduction
4. Score the investigation documentation
5. Run tests to verify the fix works
6. Output JSON with detailed scoring breakdown

## Success Criteria

- **Excellent (90-100)**: Identifies all key concepts, provides clear minimal repro, documents investigation thoroughly, all tests pass
- **Good (70-89)**: Identifies most key concepts, has minimal repro, some documentation, all tests pass
- **Acceptable (50-69)**: Identifies some key concepts or tests pass but analysis is weak
- **Poor (<50)**: Misses root cause or tests still fail

## Example Output

```json
{
  "score": 95,
  "max_score": 100,
  "test_passed": true,
  "details": {
    "root_cause_analysis": {
      "score": 60,
      "max_score": 60,
      "feedback": "Excellent identification of the bug.",
      "found_key_concepts": {
        "lru_key_reuse": true,
        "wrong_key_assignment": true,
        "should_delete": true,
        "line_reference": true,
        "overwrites_instead_of_adding": true
      }
    },
    "minimal_reproduction": {
      "score": 20,
      "max_score": 20,
      "feedback": "Minimal reproduction provided."
    },
    "investigation": {
      "score": 15,
      "max_score": 20,
      "feedback": "Investigation documented but could be more detailed."
    }
  }
}
```
