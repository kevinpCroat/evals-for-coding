# Greenfield-001: URL Shortener API

A benchmark that tests an AI's ability to build a complete REST API from scratch with no existing codebase.

## Overview

This benchmark evaluates whether an AI can:
- Design and implement a complete API architecture from scratch
- Make reasonable decisions when faced with underspecified requirements
- Write production-quality code with proper error handling
- Create comprehensive tests for their implementation
- Document their work clearly

The task is to build a URL shortener service (like bit.ly) with full CRUD operations, statistics tracking, and proper validation.

## Task Description

Build a complete URL shortening REST API in Python (Flask or FastAPI) with:
- URL creation with auto-generated or custom short codes
- Redirection from short codes to original URLs
- Statistics tracking (access counts, creation time)
- List all URLs functionality
- Delete URLs
- Comprehensive error handling and validation

See `spec.md` for complete requirements.

## Difficulty

**Medium** - Should take an experienced AI 15-30 minutes to complete.

Challenges:
- Greenfield project requires making architectural decisions
- Spec has deliberate ambiguities (e.g., exact endpoint paths, response formats)
- Must balance completeness with good design
- Requires proper testing strategy
- Need to document from scratch

## Evaluation Components

The benchmark scores submissions on:

1. **Functional Tests (40%)**: Comprehensive pytest test suite validates all features
2. **Spec Compliance (30%)**: Automated checks verify all requirements are met
3. **Code Quality (20%)**: Complexity analysis, no duplication, error handling, validation
4. **Documentation (10%)**: README completeness, API docs, setup instructions

Pass threshold: 70/100

## Directory Structure

```
greenfield-001/
├── README.md              # This file
├── spec.md               # Complete task specification
├── prompts.txt           # Task description for AI
├── data/                 # Sample URLs for reference
│   └── sample_urls.json
└── verification/
    ├── tests/
    │   └── test_api.py   # Comprehensive API test suite
    └── verify.sh         # Automated scoring script
```

## Running the Benchmark

1. Give the AI the task from `prompts.txt`
2. Let the AI implement the solution in the benchmark directory
3. Run verification:
   ```bash
   cd greenfield-001
   ./verification/verify.sh
   ```

The script will:
- Install dependencies
- Start the API server on port 8080
- Run comprehensive functional tests
- Check specification compliance
- Analyze code quality
- Verify documentation
- Output JSON scoring results

## Example JSON Output

```json
{
  "benchmark": "greenfield-001",
  "timestamp": "2026-01-31T15:00:00Z",
  "components": {
    "functional_tests": {"score": 85, "weight": 0.40, "details": "Passed: 42, Failed: 3 (93.3%)"},
    "spec_compliance": {"score": 90, "weight": 0.30, "details": "Passed 9/10 specification checks"},
    "code_quality": {"score": 80, "weight": 0.20, "details": "Passed 4/5 quality checks"},
    "documentation": {"score": 100, "weight": 0.10, "details": "Passed 5/5 documentation checks"}
  },
  "base_score": 87.5,
  "penalties": {
    "time_penalty": 0,
    "iteration_penalty": 0,
    "error_penalty": 0
  },
  "final_score": 87,
  "passed": true
}
```

## Design Philosophy

This benchmark follows the "Brazil Bench" approach:
- Deliberate ambiguities test decision-making (e.g., exact field names, endpoint paths)
- Multiple valid solutions exist
- Tests are flexible but verify core requirements
- Rewards production-ready code over quick hacks

## Success Criteria

A good implementation should:
- Work correctly for all core features
- Handle edge cases gracefully (invalid URLs, missing data, duplicates)
- Use appropriate HTTP status codes
- Have clean, maintainable code structure
- Include proper error handling and validation
- Be well-documented with clear setup instructions
- Pass >80% of functional tests

## Common Pitfalls

- Forgetting to validate URL format
- Not handling missing/null data in requests
- Using wrong HTTP status codes
- Insufficient error messages
- Missing documentation
- Not tracking access counts properly
- Short codes that don't meet spec (must be 6-8 alphanumeric)
- Server not running on port 8080

## Benchmark Metadata

- **Category**: Greenfield Development
- **Language**: Python
- **Framework**: Flask or FastAPI
- **Estimated Time**: 15-30 minutes
- **Automation Rate**: ~95% (fully automated scoring)
- **Pass Threshold**: 70/100
