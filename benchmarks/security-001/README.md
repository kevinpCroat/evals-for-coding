# Security-001: Security Vulnerability Assessment

This benchmark evaluates an AI's ability to identify and fix security vulnerabilities in a web application, following OWASP Top 10 best practices.

## Overview

The AI is given a Flask-based e-commerce web application that was developed quickly without proper security considerations. The application contains 10 intentionally planted security vulnerabilities spanning the OWASP Top 10 categories. The AI must:

1. Identify all security vulnerabilities
2. Document each with type, location, severity, and exploitation scenario
3. Fix all vulnerabilities following security best practices
4. Run SAST tools (bandit) to measure improvement
5. Optionally create security tests to validate fixes

## Vulnerabilities Planted

The starter code contains the following realistic vulnerabilities:

1. **Hardcoded Secrets** (Critical) - Secret keys, credentials, and API keys in source code
2. **SQL Injection - Login** (Critical) - Unsanitized user input in authentication query
3. **Cross-Site Scripting (XSS)** (High) - Unescaped user input rendered in HTML
4. **SQL Injection - Products** (Critical) - Second SQL injection in product search
5. **Path Traversal** (Critical) - Unvalidated file path allowing directory traversal
6. **Command Injection** (Critical) - Shell command execution with user input
7. **Insecure Deserialization** (Critical) - Pickle deserialization of untrusted data
8. **Authentication Bypass** (Critical) - Backdoor allowing admin access without credentials
9. **Weak Password Storage** (High) - Plaintext password comparison
10. **Debug Mode Enabled** (High) - Flask debug mode in production configuration

The application also includes **correctly implemented** security features that should NOT be flagged as vulnerabilities, testing for false positives.

## Directory Structure

```
security-001/
├── README.md                      # This file
├── spec.md                        # Detailed task specification
├── prompts.txt                    # Standard prompts for AI
├── starter-code/
│   ├── app.py                     # Flask application with vulnerabilities
│   ├── requirements.txt           # Python dependencies
│   └── README.md                  # Application documentation
└── verification/
    ├── verify.sh                  # Automated scoring script
    └── VULNERABILITIES.md         # Reference list of all vulnerabilities
```

## Scoring

The benchmark uses a weighted scoring system:

### 1. Vulnerability Detection Rate (50%)
- Points awarded for each correctly identified vulnerability
- Must identify type, location, and general security risk
- Partial credit for identifying vulnerability without complete details
- **10 vulnerabilities total** = 5 points each

### 2. SAST Score Improvement (30%)
- Measures actual code fixes applied
- Checks for proper security implementations:
  - Parameterized queries instead of string concatenation
  - Environment variables instead of hardcoded secrets
  - Secure functions (escape, secure_filename, safe_join)
  - Removal of dangerous patterns (shell=True, pickle.loads)
  - Password hashing implementation
  - Debug mode disabled
- **10 fixes expected** = 3 points each

### 3. Security Test Quality (20%)
- Awards points for creating security-focused tests
- Checks for test file existence and coverage
- Looks for specific vulnerability tests (SQL injection, XSS, etc.)
- **Basic tests** = 10 points, **Comprehensive suite** = 20 points

**Passing Score:** 70/100

## Usage

### Running the Benchmark

1. Provide the AI with the contents of `prompts.txt`
2. Give access to `starter-code/` directory
3. Allow the AI to analyze, document, and fix vulnerabilities
4. Run verification:

```bash
./verification/verify.sh
```

### Expected Deliverables

1. **SECURITY_AUDIT.md** - Documentation of all vulnerabilities found with:
   - Vulnerability type and location (file, line numbers)
   - Severity level (Critical, High, Medium, Low)
   - Description of the security risk
   - Exploitation scenario
   - Fix applied

2. **Fixed app.py** - Remediated version with all vulnerabilities fixed

3. **SAST Analysis** - Bandit output before and after fixes:
   ```bash
   bandit -r starter-code/ -f json -o bandit_before.json
   # After fixes
   bandit -r starter-code/ -f json -o bandit_after.json
   ```

4. **Security Tests** (Optional) - Test cases validating fixes

## Evaluation Criteria

### What Makes a Good Response

- **Comprehensive Detection:** Identifies all 10 vulnerabilities
- **Accurate Classification:** Correctly categorizes vulnerability types
- **Proper Fixes:** Implements industry-standard security controls
- **No False Positives:** Doesn't flag correctly implemented security code
- **OWASP Alignment:** Fixes follow OWASP recommendations
- **Testing:** Includes validation that fixes work correctly

### Common Pitfalls to Avoid

- Missing vulnerabilities (especially subtle ones)
- Overly generic fixes that don't actually solve the problem
- Breaking application functionality while fixing security issues
- Introducing new vulnerabilities while fixing others
- Flagging secure code as vulnerable (false positives)
- Not using proper security libraries (bcrypt, parameterized queries, etc.)

## Verification Output

The `verify.sh` script outputs JSON with detailed scoring:

```json
{
  "benchmark": "security-001",
  "timestamp": "2026-01-31T...",
  "scores": {
    "vulnerability_detection": {
      "score": 45.00,
      "max": 50,
      "details": {
        "vulnerabilities_found": 9,
        "total_vulnerabilities": 10
      }
    },
    "sast_improvement": {
      "score": 27.00,
      "max": 30,
      "details": {
        "fixes_applied": 9,
        "total_fixes_needed": 10,
        "bandit_high": 2,
        "bandit_medium": 3,
        "bandit_low": 1
      }
    },
    "security_tests": {
      "score": 20,
      "max": 20,
      "details": {
        "test_file_exists": true,
        "test_count": 8
      }
    },
    "total": {
      "score": 92.00,
      "max": 100,
      "percentage": 92.00
    }
  },
  "vulnerabilities": {
    "expected": 10,
    "detected": 9,
    "detection_rate": 0.9000
  },
  "pass": true
}
```

## Benchmark Characteristics

- **Automation Rate:** ~90% (all scoring is deterministic)
- **Difficulty:** Advanced
- **Time Estimate:** 30-60 minutes for human expert
- **Skills Tested:**
  - Security vulnerability identification
  - OWASP Top 10 knowledge
  - Secure coding practices
  - SAST tool usage
  - Security testing
  - Python/Flask security

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Bandit SAST Tool](https://bandit.readthedocs.io/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)

## License

This benchmark is part of the software engineering evaluation suite.
