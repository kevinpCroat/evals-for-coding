#!/bin/bash

# Security Vulnerability Assessment Verification Script
# This script scores the AI's security audit and fixes

set -e

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER_DIR="$BENCHMARK_DIR/starter-code"
VERIFICATION_DIR="$BENCHMARK_DIR/verification"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize scores
total_score=0
vulnerability_score=0
sast_score=0
test_score=0
vulnerabilities_found=0
fixes_applied=0

echo "======================================"
echo "Security Assessment Verification"
echo "======================================"
echo ""

# Check if required files exist
echo -e "${YELLOW}Checking for required deliverables...${NC}"

if [ ! -f "$BENCHMARK_DIR/SECURITY_AUDIT.md" ]; then
    echo -e "${RED}ERROR: SECURITY_AUDIT.md not found${NC}"
    AUDIT_EXISTS=false
else
    echo -e "${GREEN}✓ SECURITY_AUDIT.md found${NC}"
    AUDIT_EXISTS=true
fi

if [ ! -f "$STARTER_DIR/app.py" ]; then
    echo -e "${RED}ERROR: starter-code/app.py not found${NC}"
    exit 1
else
    echo -e "${GREEN}✓ app.py found${NC}"
fi

echo ""

# Install bandit if not present
bandit_available=true
if ! command -v bandit &> /dev/null; then
    echo -e "${YELLOW}Installing bandit...${NC}"
    if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
        (pip install bandit -q || pip3 install bandit -q) 2>/dev/null || bandit_available=false
    else
        echo -e "${YELLOW}Warning: pip not found, skipping bandit installation${NC}"
        bandit_available=false
    fi
fi

# Run bandit on current code
bandit_high=0
bandit_medium=0
bandit_low=0

if [ "$bandit_available" = true ] && command -v bandit &> /dev/null; then
    echo -e "${YELLOW}Running SAST analysis with bandit...${NC}"
    bandit -r "$STARTER_DIR" -f json -o "$VERIFICATION_DIR/bandit_current.json" 2>/dev/null || true
    echo -e "${GREEN}✓ Bandit analysis complete${NC}"
    echo ""

    # Parse bandit results
    if [ -f "$VERIFICATION_DIR/bandit_current.json" ]; then
        if command -v jq &> /dev/null; then
            bandit_high=$(jq '[.results[] | select(.issue_severity=="HIGH")] | length' "$VERIFICATION_DIR/bandit_current.json" 2>/dev/null || echo "0")
            bandit_medium=$(jq '[.results[] | select(.issue_severity=="MEDIUM")] | length' "$VERIFICATION_DIR/bandit_current.json" 2>/dev/null || echo "0")
            bandit_low=$(jq '[.results[] | select(.issue_severity=="LOW")] | length' "$VERIFICATION_DIR/bandit_current.json" 2>/dev/null || echo "0")
        else
            # Fallback if jq not available - estimate from bandit output
            bandit_high=$(grep -c '"issue_severity": "HIGH"' "$VERIFICATION_DIR/bandit_current.json" 2>/dev/null || echo "0")
            bandit_medium=$(grep -c '"issue_severity": "MEDIUM"' "$VERIFICATION_DIR/bandit_current.json" 2>/dev/null || echo "0")
            bandit_low=$(grep -c '"issue_severity": "LOW"' "$VERIFICATION_DIR/bandit_current.json" 2>/dev/null || echo "0")
        fi

        echo "Bandit Results (Current Code):"
        echo "  High Severity: $bandit_high"
        echo "  Medium Severity: $bandit_medium"
        echo "  Low Severity: $bandit_low"
        echo ""
    fi
else
    echo -e "${YELLOW}Warning: Bandit not available, SAST analysis skipped${NC}"
    echo ""
fi

# Score 1: Vulnerability Detection Rate (50%)
echo "======================================"
echo "1. Vulnerability Detection (50%)"
echo "======================================"

if [ "$AUDIT_EXISTS" = true ]; then
    # Check for each expected vulnerability in the audit
    if grep -qi "secret\|credential\|hardcoded\|api.key" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ Hardcoded secrets detected${NC}"
    fi

    if grep -qi "sql.*injection\|injection.*login\|login.*sql" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ SQL Injection (login) detected${NC}"
    fi

    if grep -qi "xss\|cross.site.scripting\|script.*injection" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ XSS vulnerability detected${NC}"
    fi

    if grep -qi "sql.*injection.*product\|product.*sql\|category.*injection" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ SQL Injection (products) detected${NC}"
    fi

    if grep -qi "path.traversal\|directory.traversal\|file.*traversal" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ Path traversal detected${NC}"
    fi

    if grep -qi "command.injection\|os.*injection\|shell.*injection" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ Command injection detected${NC}"
    fi

    if grep -qi "deserialization\|pickle\|unsafe.*load" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ Insecure deserialization detected${NC}"
    fi

    if grep -qi "auth.*bypass\|authentication.*bypass\|broken.*auth" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ Authentication bypass detected${NC}"
    fi

    if grep -qi "plaintext.*password\|password.*hash\|unhashed.*password" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ Plaintext password issue detected${NC}"
    fi

    if grep -qi "debug.*mode\|debug.*true\|production.*debug" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
        vulnerabilities_found=$((vulnerabilities_found + 1))
        echo -e "${GREEN}✓ Debug mode issue detected${NC}"
    fi

    echo ""
    echo "Vulnerabilities detected: $vulnerabilities_found / 10"
    vulnerability_score=$(echo "scale=2; ($vulnerabilities_found / 10) * 50" | bc)
else
    echo -e "${RED}Cannot score - SECURITY_AUDIT.md not found${NC}"
    vulnerability_score=0
fi

echo "Vulnerability Detection Score: $vulnerability_score / 50"
echo ""

# Score 2: SAST Score Improvement (30%)
echo "======================================"
echo "2. SAST Score Improvement (30%)"
echo "======================================"

# Check if code has been modified to fix vulnerabilities
code_fixed=false

# Check for common fixes in app.py
if grep -q "execute.*\?.*\?" "$STARTER_DIR/app.py" 2>/dev/null; then
    echo -e "${GREEN}✓ Found parameterized queries${NC}"
    code_fixed=true
fi

if grep -q "os\.environ\|getenv" "$STARTER_DIR/app.py" 2>/dev/null; then
    echo -e "${GREEN}✓ Found environment variable usage${NC}"
    code_fixed=true
fi

if ! grep -q "shell=True" "$STARTER_DIR/app.py" 2>/dev/null; then
    echo -e "${GREEN}✓ Shell command execution removed/fixed${NC}"
    code_fixed=true
fi

if ! grep -q "pickle\.loads" "$STARTER_DIR/app.py" 2>/dev/null; then
    echo -e "${GREEN}✓ Insecure deserialization removed${NC}"
    code_fixed=true
fi

if grep -q "escape\|safe_join\|secure_filename" "$STARTER_DIR/app.py" 2>/dev/null; then
    echo -e "${GREEN}✓ Found security functions (escape, safe_join, etc.)${NC}"
    code_fixed=true
fi

# Calculate SAST improvement score
if [ "$code_fixed" = true ]; then
    # Count fixed vulnerabilities by comparing current vs expected

    # Check each vulnerability is fixed
    if ! grep -q 'app\.secret_key = "' "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    if grep -q "execute.*\?" "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    if grep -q "escape\|\{\{.*|e\}\}" "$STARTER_DIR/app.py" 2>/dev/null || ! grep -q "render_template_string" "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    if ! grep -q "shell=True" "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    if ! grep -q "pickle\.loads" "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    if grep -q "secure_filename\|safe_join\|abspath.*startswith" "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    if ! grep -q "override.*admin" "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    if grep -q "bcrypt\|hashlib\.pbkdf2\|werkzeug\.security" "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    if ! grep -q "debug=True" "$STARTER_DIR/app.py" 2>/dev/null; then
        fixes_applied=$((fixes_applied + 1))
    fi

    echo ""
    echo "Fixes applied: $fixes_applied / 10"
    sast_score=$(echo "scale=2; ($fixes_applied / 10) * 30" | bc)
else
    echo -e "${YELLOW}No significant code fixes detected${NC}"
    sast_score=0
fi

echo "SAST Improvement Score: $sast_score / 30"
echo ""

# Score 3: Security Test Quality (20%)
echo "======================================"
echo "3. Security Test Quality (20%)"
echo "======================================"

test_score=0

# Check for security tests
if [ -f "$BENCHMARK_DIR/test_security.py" ]; then
    echo -e "${GREEN}✓ Security test file found${NC}"
    test_score=10

    # Check test quality
    test_count=$(grep -c "def test_" "$BENCHMARK_DIR/test_security.py" 2>/dev/null || echo "0")
    echo "  Test cases found: $test_count"

    if [ "$test_count" -ge 5 ]; then
        echo -e "${GREEN}✓ Good test coverage${NC}"
        test_score=20
    fi

    # Check for specific security test patterns
    if grep -qi "sql.*injection\|' OR\|--" "$BENCHMARK_DIR/test_security.py" 2>/dev/null; then
        echo -e "${GREEN}✓ SQL injection tests found${NC}"
    fi

    if grep -qi "xss\|<script>\|javascript:" "$BENCHMARK_DIR/test_security.py" 2>/dev/null; then
        echo -e "${GREEN}✓ XSS tests found${NC}"
    fi
elif grep -qi "test\|validation\|security" "$BENCHMARK_DIR/SECURITY_AUDIT.md" 2>/dev/null; then
    echo -e "${YELLOW}No dedicated test file, but testing mentioned in audit${NC}"
    test_score=5
else
    echo -e "${YELLOW}No security tests found${NC}"
    test_score=0
fi

echo "Security Test Score: $test_score / 20"
echo ""

# Calculate total score
total_score=$(echo "scale=2; $vulnerability_score + $sast_score + $test_score" | bc)

echo "======================================"
echo "Final Score"
echo "======================================"
echo "Vulnerability Detection: $vulnerability_score / 50"
echo "SAST Improvement: $sast_score / 30"
echo "Security Tests: $test_score / 20"
echo "--------------------------------------"
echo "TOTAL SCORE: $total_score / 100"
echo "======================================"
echo ""

# Generate JSON output
cat > "$VERIFICATION_DIR/results.json" << EOF
{
  "benchmark": "security-001",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "scores": {
    "vulnerability_detection": {
      "score": $vulnerability_score,
      "max": 50,
      "details": {
        "vulnerabilities_found": $vulnerabilities_found,
        "total_vulnerabilities": 10
      }
    },
    "sast_improvement": {
      "score": $sast_score,
      "max": 30,
      "details": {
        "fixes_applied": ${fixes_applied:-0},
        "total_fixes_needed": 10,
        "bandit_high": ${bandit_high:-0},
        "bandit_medium": ${bandit_medium:-0},
        "bandit_low": ${bandit_low:-0}
      }
    },
    "security_tests": {
      "score": $test_score,
      "max": 20,
      "details": {
        "test_file_exists": $([ -f "$BENCHMARK_DIR/test_security.py" ] && echo "true" || echo "false"),
        "test_count": ${test_count:-0}
      }
    },
    "total": {
      "score": $total_score,
      "max": 100,
      "percentage": $(echo "scale=2; $total_score" | bc)
    }
  },
  "vulnerabilities": {
    "expected": 10,
    "detected": $vulnerabilities_found,
    "detection_rate": $(echo "scale=4; $vulnerabilities_found / 10" | bc)
  },
  "pass": $([ $(echo "$total_score >= 70" | bc) -eq 1 ] && echo "true" || echo "false")
}
EOF

echo "Results saved to: $VERIFICATION_DIR/results.json"

# Exit with appropriate code
if [ $(echo "$total_score >= 70" | bc) -eq 1 ]; then
    echo -e "${GREEN}✓ PASS - Score meets threshold (70+)${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ INCOMPLETE - Score below threshold (<70)${NC}"
    exit 1
fi
