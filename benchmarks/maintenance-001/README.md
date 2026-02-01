# Dependency Maintenance Benchmark (maintenance-001)

This benchmark tests an AI's ability to update project dependencies, fix security vulnerabilities, handle breaking changes, and ensure tests continue to pass.

## Overview

**Task Type**: Dependency Maintenance & Security Updates
**Difficulty**: Medium
**Time Estimate**: 15-30 minutes
**Key Skills Tested**:
- Dependency management
- Security vulnerability remediation
- Handling breaking changes in libraries
- Backward compatibility maintenance
- Debugging test failures after updates
- Addressing deprecation warnings

## Scenario

You are given a Python Flask web application that has been running in production since 2021. The dependencies haven't been updated in years and now have known security vulnerabilities (CVEs). Your task is to update all dependencies to their latest stable versions while ensuring the application continues to work correctly.

## What's Included

### starter-code/
The initial codebase with old dependencies:
- **requirements.txt**: Pinned to old versions from 2021
  - Flask 1.1.2 (has CVE-2023-30861)
  - Werkzeug 1.0.1 (has CVE-2023-25577)
  - requests 2.25.0 (has CVE-2023-32681)
  - Other outdated dependencies
- **src/web_app.py**: Flask web application with REST API
- **src/api_client.py**: HTTP client using requests library
- **tests/**: Comprehensive test suite (all tests currently pass with old versions)
- **KNOWN_ISSUES.md**: Documentation of security vulnerabilities

### verification/
Automated scoring system:
- **verify.sh**: Checks dependencies updated, tests pass, no warnings

## Task Description

Update all dependencies to latest stable versions and ensure:
1. All security vulnerabilities are fixed (minimum versions specified)
2. All existing tests continue to pass
3. No deprecation warnings when running the code
4. Application functionality is preserved

See `spec.md` for detailed requirements and `prompts.txt` for the standard task prompt.

## Evaluation Criteria

The benchmark scores on three components:

1. **Dependencies Updated (40%)**
   - Flask updated to >= 2.3.0
   - Werkzeug updated to >= 2.3.0
   - requests updated to >= 2.31.0
   - pytest updated to >= 7.0.0

2. **Tests Pass (40%)**
   - All existing tests pass with new dependencies
   - At least 16 tests should pass
   - No regressions in functionality

3. **No Warnings (20%)**
   - No deprecation warnings when running tests
   - Code runs cleanly with `-W default` flag

**Passing Score**: 70%

## Running the Benchmark

1. Give the AI the task from `prompts.txt`
2. Point it to the `starter-code/` directory
3. Let it update dependencies and fix any issues
4. Run verification: `./verification/verify.sh`

## Example Solution Approach

A successful solution typically:
1. Reviews KNOWN_ISSUES.md to understand security vulnerabilities
2. Updates requirements.txt with latest stable versions
3. Installs new dependencies and runs tests
4. Fixes any breaking changes (e.g., Flask 2.x API changes)
5. Addresses deprecation warnings
6. Verifies all tests pass cleanly

## Common Challenges

- **Flask 1.x → 2.x migration**: Some APIs changed between major versions
- **Test fixtures**: May need updates for new pytest versions
- **Import changes**: Werkzeug moved some imports in 2.x
- **Deprecation warnings**: Need to update deprecated patterns in code

## Key Learning Outcomes

This benchmark tests whether an AI can:
- Understand security vulnerability reports
- Plan a dependency update strategy
- Handle breaking changes in dependencies
- Debug test failures after updates
- Clean up deprecation warnings
- Maintain backward compatibility

## Verification Details

The verification script:
1. Checks `requirements.txt` for minimum required versions
2. Installs dependencies and runs test suite
3. Re-runs tests with warnings enabled to check for deprecations
4. Outputs JSON with detailed scoring breakdown

## Files Structure

```
maintenance-001/
├── README.md                      # This file
├── spec.md                        # Detailed task specification
├── prompts.txt                    # Standard prompts for AI
├── starter-code/
│   ├── requirements.txt           # Old dependencies (to be updated)
│   ├── KNOWN_ISSUES.md           # Security vulnerability documentation
│   ├── README.md                 # Project documentation
│   ├── src/
│   │   ├── __init__.py
│   │   ├── api_client.py         # HTTP client code
│   │   └── web_app.py            # Flask application
│   └── tests/
│       ├── __init__.py
│       ├── test_api_client.py    # API client tests
│       └── test_web_app.py       # Flask app tests
└── verification/
    └── verify.sh                  # Automated verification script
```

## Notes

- This benchmark simulates a realistic maintenance task
- The security vulnerabilities are based on real CVEs
- Tests are designed to work with both old and new versions (if code is updated properly)
- The task requires both technical skills and careful attention to detail
