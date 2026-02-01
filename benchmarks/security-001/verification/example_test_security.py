"""
Example Security Test Suite
This is an EXAMPLE of what a good security test suite might look like.
DO NOT include this in the actual benchmark - it's for reference only.
"""

import pytest
from app import app
import sqlite3


@pytest.fixture
def client():
    """Test client fixture"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_sql_injection_login_prevented(client):
    """Test that SQL injection is prevented in login"""
    # Attempt SQL injection
    response = client.post('/login', data={
        'username': "admin' OR '1'='1",
        'password': "anything"
    })
    # Should not be authenticated
    assert response.status_code == 401 or 'Invalid' in response.data.decode()


def test_xss_in_search_prevented(client):
    """Test that XSS is prevented in search"""
    # Attempt XSS
    xss_payload = '<script>alert("XSS")</script>'
    response = client.get(f'/search?q={xss_payload}')

    # Script tag should be escaped
    assert '<script>' not in response.data.decode()
    assert '&lt;script&gt;' in response.data.decode() or 'escaped' in response.data.decode()


def test_path_traversal_prevented(client):
    """Test that path traversal is prevented"""
    # Attempt path traversal
    response = client.get('/download?file=../../etc/passwd')

    # Should not access file outside allowed directory
    assert response.status_code in [400, 403, 404]


def test_command_injection_prevented(client):
    """Test that command injection is prevented"""
    # Attempt command injection
    response = client.post('/admin/backup', data={
        'backup_name': 'backup.db; rm -rf /'
    })

    # Should not execute injected command
    assert response.status_code in [400, 403] or 'error' in response.data.decode().lower()


def test_no_hardcoded_secrets():
    """Test that secrets are not hardcoded"""
    with open('app.py', 'r') as f:
        content = f.read()

    # Should use environment variables
    assert 'os.environ' in content or 'getenv' in content
    # Should not have hardcoded secret key
    assert 'app.secret_key = "super_secret_key' not in content


def test_debug_mode_disabled():
    """Test that debug mode is disabled"""
    with open('app.py', 'r') as f:
        content = f.read()

    # Debug should be False or from environment
    assert 'debug=True' not in content or 'os.environ' in content


def test_parameterized_queries():
    """Test that queries use parameterization"""
    with open('app.py', 'r') as f:
        content = f.read()

    # Should use parameterized queries
    assert 'execute(' in content
    assert '?' in content  # Parameter placeholder


def test_password_hashing():
    """Test that passwords are hashed"""
    with open('app.py', 'r') as f:
        content = f.read()

    # Should use password hashing
    assert 'bcrypt' in content or 'pbkdf2' in content or 'hashlib' in content
