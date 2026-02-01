# Documentation-001: HTTP Client Documentation

A benchmark that tests AI's ability to document undocumented production code.

## Overview

This benchmark evaluates an AI's ability to:
- Understand code by reading implementation
- Write clear, comprehensive API documentation
- Create working code examples
- Follow documentation style guidelines
- Ensure documentation accuracy

## Task Description

The AI must document a fully functional but completely undocumented HTTP client library (`http_client.py`). The library contains approximately 180 lines of production-quality Python code with:

- `HTTPClient` class - Main HTTP client with methods for GET, POST, PUT, DELETE, PATCH
- `Response` class - Response wrapper with JSON parsing, status checks
- `RetryConfig` class - Retry configuration with backoff
- `HTTPError` exception - Custom HTTP error handling

The code has **zero documentation** - no docstrings, no comments, no usage examples.

## What Makes This Realistic

Real-world software often lacks documentation:
- Legacy code with missing docs
- Third-party libraries without clear API docs
- Internal tools that need user-facing documentation
- Code written quickly without time for docs

AI must be able to understand code and explain it clearly to users.

## Scoring Components

The benchmark uses automated scoring across four dimensions:

### 1. API Coverage (30%)
- Percentage of public APIs (classes, methods) with docstrings
- Identifies which APIs are missing documentation
- Full credit for 100% coverage

### 2. Example Execution (40%)
- Extracts code examples from docstrings
- Attempts to execute each example
- Scores based on percentage that run without errors
- 10 base points for having examples, 30 points for success rate

### 3. Docs-Code Consistency (20%)
- Checks if documented parameters match actual function signatures
- Verifies return value documentation matches implementation
- Detects parameter mismatches and missing return docs

### 4. Readability (10%)
- Validates Google-style docstring format
- Checks for proper sections (Args, Returns, Raises, Example)
- Evaluates summary line quality and section formatting

## Directory Structure

```
documentation-001/
├── README.md                           # This file
├── spec.md                            # Detailed task specification
├── prompts.txt                        # Standard prompts for AI
├── starter-code/
│   └── http_client.py                # Undocumented HTTP client library
└── verification/
    ├── verify.sh                     # Main verification script
    └── tests/
        ├── check_coverage.py         # API coverage checker
        ├── extract_examples.py       # Code example extractor
        ├── run_examples.py           # Example execution tester
        ├── check_consistency.py      # Signature consistency checker
        └── check_format.py           # Format/style validator
```

## Running the Benchmark

1. Give the AI the task from `prompts.txt`
2. The AI should read and understand `http_client.py`
3. The AI should add comprehensive docstrings to the file
4. Run verification: `./verification/verify.sh`

## Example Output

```json
{
  "score": 85,
  "max_score": 100,
  "test_passed": true,
  "details": {
    "api_coverage": {
      "score": 28,
      "max_score": 30,
      "percentage": 95.0,
      "feedback": "Excellent API coverage (95.0%)..."
    },
    "example_execution": {
      "score": 38,
      "max_score": 40,
      "total_examples": 8,
      "feedback": "Excellent! 8/8 examples execute successfully..."
    },
    "consistency": {
      "score": 18,
      "max_score": 20,
      "percentage": 90.0,
      "feedback": "Excellent consistency between docs and code..."
    },
    "readability": {
      "score": 9,
      "max_score": 10,
      "format_score": 92.5,
      "feedback": "Well-formatted, follows Google style consistently..."
    }
  }
}
```

## Success Criteria

- Score >= 70 to pass
- All public APIs should have docstrings
- Code examples must actually execute
- Documentation must match implementation
- Consistent Google-style format

## What This Tests

- **Code comprehension** - Can the AI understand undocumented code?
- **Technical writing** - Can it explain complex concepts clearly?
- **Example creation** - Can it write realistic, working examples?
- **Accuracy** - Does documentation match reality?
- **Attention to detail** - Proper formatting, complete coverage
