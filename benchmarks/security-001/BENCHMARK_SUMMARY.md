# Security-001 Benchmark Summary

## Quick Overview

This benchmark tests an AI's ability to identify and fix security vulnerabilities in a realistic Flask web application.

**Difficulty:** Advanced
**Time Estimate:** 30-60 minutes
**Automation Rate:** 90%
**Passing Score:** 70/100

## What's Been Built

### 1. Vulnerable Application (`starter-code/app.py`)
A realistic Flask e-commerce application with 10 intentionally planted vulnerabilities:

- **Critical Severity (7):**
  1. Hardcoded secrets and credentials
  2. SQL Injection in login
  3. SQL Injection in product search
  4. Path traversal
  5. Command injection
  6. Insecure deserialization
  7. Authentication bypass

- **High Severity (3):**
  8. Cross-Site Scripting (XSS)
  9. Plaintext password storage
  10. Debug mode enabled in production

**Key Feature:** Includes correctly implemented security code to test for false positives.

### 2. Documentation

- **spec.md** - Complete task specification with requirements and success criteria
- **prompts.txt** - Standard prompts formatted for AI consumption
- **README.md** - Comprehensive benchmark documentation
- **verification/VULNERABILITIES.md** - Reference guide listing all vulnerabilities with:
  - Exact line numbers
  - Severity levels
  - Exploitation scenarios
  - Expected fixes

### 3. Verification System (`verification/verify.sh`)

Automated scoring script that:
- Checks for SECURITY_AUDIT.md deliverable
- Analyzes vulnerability detection (50%)
- Measures code fixes applied (30%)
- Evaluates security test quality (20%)
- Runs SAST analysis with Bandit (when available)
- Outputs JSON results

**Scoring Breakdown:**
- 50% - Vulnerability Detection: 5 points per vulnerability found (10 total)
- 30% - SAST Improvement: 3 points per fix applied (10 total)
- 20% - Security Tests: Based on test file quality and coverage

### 4. Example Resources

- **verification/example_test_security.py** - Example security test suite (for reference only)
- **starter-code/README.md** - Application documentation

## File Structure

```
security-001/
├── README.md                          # Main documentation
├── spec.md                            # Task specification
├── prompts.txt                        # AI prompts
├── BENCHMARK_SUMMARY.md               # This file
├── starter-code/
│   ├── app.py                         # Vulnerable Flask app (297 lines)
│   ├── requirements.txt               # Python dependencies
│   └── README.md                      # App documentation
└── verification/
    ├── verify.sh                      # Scoring script (378 lines)
    ├── VULNERABILITIES.md             # Reference vulnerabilities
    └── example_test_security.py       # Example tests (reference)
```

## How It Works

1. **AI receives** prompts.txt and access to starter-code/
2. **AI must:**
   - Audit the code for security vulnerabilities
   - Create SECURITY_AUDIT.md documenting findings
   - Fix all vulnerabilities in app.py
   - Optionally create security tests
3. **Verification runs** and scores based on:
   - How many vulnerabilities were correctly identified
   - How many were actually fixed in the code
   - Quality of security tests created

## Testing the Benchmark

The benchmark has been validated to ensure:
- ✅ All vulnerabilities are realistic OWASP Top 10 issues
- ✅ Verification script runs on macOS/Linux (bash 3.2+)
- ✅ Scoring is deterministic and reproducible
- ✅ JSON output is properly formatted
- ✅ False positive testing (secure code included)
- ✅ Handles missing dependencies gracefully

## Expected AI Deliverables

1. **SECURITY_AUDIT.md** with:
   - List of vulnerabilities found
   - Type, location, severity for each
   - Exploitation scenarios
   - Fixes applied

2. **Fixed app.py** with security remediations

3. **Bandit analysis** (before/after)

4. **Security tests** (optional, for full score)

## Scoring Examples

**Perfect Score (100):**
- All 10 vulnerabilities identified and documented
- All 10 vulnerabilities fixed with proper security controls
- Comprehensive security test suite created

**Good Score (85):**
- 9/10 vulnerabilities identified
- 9/10 vulnerabilities fixed
- Basic security tests created

**Passing Score (70):**
- 7/10 vulnerabilities identified
- 7/10 vulnerabilities fixed
- Testing mentioned in audit but no dedicated tests

**Failing Score (45):**
- 5/10 vulnerabilities identified
- 4/10 vulnerabilities fixed
- No security tests

## Validation

The benchmark has been tested with:
- ✅ Empty SECURITY_AUDIT.md (scores 0 on detection)
- ✅ Unfixed vulnerable code (scores based on secure examples present)
- ✅ Missing dependencies (bandit, jq) - handles gracefully
- ✅ JSON output format validation

## Next Steps for Usage

To use this benchmark:

1. Copy prompts.txt content to AI
2. Provide access to starter-code/
3. Let AI analyze and fix
4. Run: `./verification/verify.sh`
5. Review results.json

## Notes

- Bandit SAST tool is optional but recommended
- Script works without jq (uses grep fallback)
- Compatible with bash 3.2+ (macOS default)
- All scoring is deterministic
- No network access required
