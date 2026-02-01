# Planted Vulnerabilities Reference

This document lists all intentionally planted security vulnerabilities in the starter code for verification purposes.

## Total Vulnerabilities: 10

---

## 1. Hardcoded Secret Key and Credentials

**File:** `starter-code/app.py`
**Lines:** 15-18
**Severity:** CRITICAL
**Type:** Sensitive Data Exposure (A02:2021 – Cryptographic Failures)

**Vulnerable Code:**
```python
app.secret_key = "super_secret_key_12345"
DATABASE = "ecommerce.db"
ADMIN_PASSWORD = "admin123"
API_KEY = "hardcoded_api_key_should_be_in_env_12345"  # Vulnerability: hardcoded secret
```

**Risk:** Hardcoded secrets in source code can be exposed through version control, allowing attackers to compromise session security, authentication, and API access.

**Expected Fix:**
- Use environment variables or secure secret management
- Load secrets from .env file or secret manager
- Use `os.environ.get()` or `python-decouple`
- Generate cryptographically secure random session keys

---

## 2. SQL Injection in Login

**File:** `starter-code/app.py`
**Lines:** 66-69
**Severity:** CRITICAL
**Type:** SQL Injection (A03:2021 – Injection)

**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
user = conn.execute(query).fetchone()
```

**Risk:** Attacker can bypass authentication using SQL injection payloads like `admin' --` or extract data using UNION queries.

**Expected Fix:**
- Use parameterized queries with placeholders
- Example: `conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))`

---

## 3. Cross-Site Scripting (XSS)

**File:** `starter-code/app.py`
**Lines:** 100-112
**Severity:** HIGH
**Type:** Cross-Site Scripting (A03:2021 – Injection)

**Vulnerable Code:**
```python
html = f'''
<html>
<body>
    <h2>Search Results for: {query}</h2>
    <form method="get">
        <input type="text" name="q" value="{query}">
        <input type="submit" value="Search">
    </form>
    <p>Showing results for: {query}</p>
</body>
</html>
'''
return render_template_string(html)
```

**Risk:** User input is directly embedded in HTML without escaping, allowing attackers to inject malicious JavaScript.

**Expected Fix:**
- Use Flask's template escaping with Jinja2
- Use `{{ query|e }}` in templates or `escape()` function
- Alternatively, use proper template files instead of `render_template_string`

---

## 4. SQL Injection in Product Search

**File:** `starter-code/app.py`
**Lines:** 123-125
**Severity:** CRITICAL
**Type:** SQL Injection (A03:2021 – Injection)

**Vulnerable Code:**
```python
query = f"SELECT * FROM products WHERE description LIKE '%{category}%'"
products = conn.execute(query).fetchall()
```

**Risk:** Second SQL injection vulnerability allowing data extraction or manipulation through the category parameter.

**Expected Fix:**
- Use parameterized queries: `conn.execute("SELECT * FROM products WHERE description LIKE ?", (f'%{category}%',))`

---

## 5. Path Traversal

**File:** `starter-code/app.py`
**Lines:** 150-160
**Severity:** CRITICAL
**Type:** Path Traversal (A01:2021 – Broken Access Control)

**Vulnerable Code:**
```python
filename = request.args.get('file')
filepath = os.path.join('/var/www/files', filename)

try:
    with open(filepath, 'r') as f:
        content = f.read()
    return content
```

**Risk:** Attacker can access arbitrary files using `../` sequences (e.g., `../../etc/passwd`).

**Expected Fix:**
- Validate and sanitize filename input
- Use `secure_filename()` from werkzeug
- Check that resolved path is within allowed directory
- Use `os.path.abspath()` and validate path prefix

---

## 6. Command Injection

**File:** `starter-code/app.py`
**Lines:** 167-172
**Severity:** CRITICAL
**Type:** Command Injection (A03:2021 – Injection)

**Vulnerable Code:**
```python
backup_name = request.form.get('backup_name', 'backup.db')
command = f"cp {DATABASE} /backups/{backup_name}"
result = subprocess.run(command, shell=True, capture_output=True, text=True)
```

**Risk:** Attacker can inject shell commands through backup_name parameter (e.g., `backup.db; rm -rf /`).

**Expected Fix:**
- Never use `shell=True` with user input
- Use subprocess with array arguments: `subprocess.run(['cp', DATABASE, f'/backups/{backup_name}'])`
- Validate input against allowed patterns
- Use Python's `shutil.copy()` instead

---

## 7. Insecure Deserialization

**File:** `starter-code/app.py`
**Lines:** 181-189
**Severity:** CRITICAL
**Type:** Insecure Deserialization (A08:2021 – Software and Data Integrity Failures)

**Vulnerable Code:**
```python
data = pickle.loads(file.read())
```

**Risk:** Pickle deserialization can execute arbitrary code. Attacker can craft malicious pickle payloads for remote code execution.

**Expected Fix:**
- Never use pickle with untrusted data
- Use safe serialization formats (JSON, YAML with safe_load)
- Implement strict input validation
- Use `json.loads()` instead

---

## 8. Broken Authentication - Authentication Bypass

**File:** `starter-code/app.py`
**Lines:** 203-206
**Severity:** CRITICAL
**Type:** Broken Authentication (A07:2021 – Identification and Authentication Failures)

**Vulnerable Code:**
```python
if request.args.get('override') == 'true':
    session['role'] = 'admin'
    return redirect('/admin')
```

**Risk:** Anyone can gain admin access by adding `?override=true` to the URL, bypassing authentication entirely.

**Expected Fix:**
- Remove authentication bypass mechanism
- Implement proper authentication checks
- Require valid credentials for privilege escalation
- Add session timeout and security controls

---

## 9. Weak Password Storage

**File:** `starter-code/app.py`
**Lines:** 66-69 (context)
**Severity:** HIGH
**Type:** Cryptographic Failures (A02:2021)

**Vulnerable Code:**
```python
# Passwords stored/compared in plaintext in SQL query
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

**Risk:** Passwords are compared directly without hashing, implying plaintext storage in database.

**Expected Fix:**
- Hash passwords using bcrypt, argon2, or PBKDF2
- Never store plaintext passwords
- Use `bcrypt.hashpw()` and `bcrypt.checkpw()`
- Update login to hash input and compare hashes

---

## 10. Debug Mode Enabled

**File:** `starter-code/app.py`
**Lines:** 295-297
**Severity:** HIGH
**Type:** Security Misconfiguration (A05:2021)

**Vulnerable Code:**
```python
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Risk:** Debug mode exposes sensitive information through error pages, enables code execution via debugger, and allows reloading on code changes.

**Expected Fix:**
- Set `debug=False` in production
- Use environment variables for configuration
- Bind to localhost (127.0.0.1) unless intentionally exposing
- Use proper production WSGI server (gunicorn, uwsgi)

---

## CORRECT Code (Should NOT be flagged)

The following code is correctly implemented and should NOT be reported as vulnerabilities:

1. **Lines 226-241:** `get_product(product_id)` - Uses parameterized query correctly
2. **Lines 245-251:** `hash_password()` - Demonstrates proper password hashing concept
3. **Lines 255-292:** `upload_avatar()` - Proper file upload validation with:
   - File type validation
   - Extension whitelist
   - `secure_filename()` usage
   - File size limits

---

## Scoring Guidelines

### Vulnerability Detection (50%)
- 1 point per correctly identified vulnerability (10 total)
- Must identify type, location, and general risk
- Partial credit for identifying vulnerability without complete details

### SAST Improvement (30%)
- Measure bandit score before and after fixes
- Compare high/medium/low severity counts
- Score = (vulnerabilities_fixed / total_bandit_findings) * 30

### Security Testing (20%)
- Quality of test cases created
- Coverage of vulnerability fixes
- Validation methods used
- 5 points for basic tests, 20 points for comprehensive suite
