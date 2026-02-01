"""
E-commerce Web Application
A simple Flask-based e-commerce platform for managing products and users.
"""
import os
import pickle
import sqlite3
import subprocess
from flask import Flask, request, render_template_string, session, redirect, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret key and credentials
app.secret_key = "super_secret_key_12345"
DATABASE = "ecommerce.db"
ADMIN_PASSWORD = "admin123"  # Hardcoded admin password
API_KEY = "hardcoded_api_key_should_be_in_env_12345"  # Vulnerability: hardcoded secret

# VULNERABILITY 2: Insecure upload directory without validation
UPLOAD_FOLDER = "/var/www/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            stock INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    """Home page"""
    return '''
    <html>
    <body>
        <h1>Welcome to SecureShop</h1>
        <ul>
            <li><a href="/login">Login</a></li>
            <li><a href="/products">Products</a></li>
            <li><a href="/search">Search</a></li>
            <li><a href="/admin">Admin Panel</a></li>
        </ul>
    </body>
    </html>
    '''


# VULNERABILITY 3: SQL Injection in login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        # SQL Injection vulnerability - unsanitized input
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 401

    return '''
    <html>
    <body>
        <h2>Login</h2>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    '''


# VULNERABILITY 4: Cross-Site Scripting (XSS)
@app.route('/search')
def search():
    """Product search with XSS vulnerability"""
    query = request.args.get('q', '')

    # XSS vulnerability - unescaped user input in HTML
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


# VULNERABILITY 5: SQL Injection in product search
@app.route('/products')
def products():
    """List products with optional filter"""
    category = request.args.get('category', '')

    conn = get_db_connection()
    if category:
        # SQL Injection vulnerability
        query = f"SELECT * FROM products WHERE description LIKE '%{category}%'"
        products = conn.execute(query).fetchall()
    else:
        products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    product_list = "<ul>"
    for product in products:
        product_list += f"<li>{product['name']} - ${product['price']}</li>"
    product_list += "</ul>"

    return f'''
    <html>
    <body>
        <h2>Products</h2>
        <form method="get">
            Filter by category: <input type="text" name="category">
            <input type="submit" value="Filter">
        </form>
        {product_list}
    </body>
    </html>
    '''


# VULNERABILITY 6: Path Traversal
@app.route('/download')
def download():
    """Download files - path traversal vulnerability"""
    filename = request.args.get('file')

    # Path traversal vulnerability - no validation
    filepath = os.path.join('/var/www/files', filename)

    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error: {str(e)}", 404


# VULNERABILITY 7: Command Injection
@app.route('/admin/backup', methods=['POST'])
def backup_database():
    """Backup database - command injection vulnerability"""
    backup_name = request.form.get('backup_name', 'backup.db')

    # Command injection vulnerability
    command = f"cp {DATABASE} /backups/{backup_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    return jsonify({
        'status': 'success',
        'output': result.stdout,
        'error': result.stderr
    })


# VULNERABILITY 8: Insecure Deserialization
@app.route('/api/import', methods=['POST'])
def import_data():
    """Import user data from pickle file"""
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    # Insecure deserialization vulnerability
    try:
        data = pickle.loads(file.read())
        return jsonify({'status': 'success', 'imported': len(data)})
    except Exception as e:
        return f"Error importing data: {str(e)}", 500


# VULNERABILITY 9: Broken Authentication - No session timeout, weak password check
@app.route('/admin')
def admin_panel():
    """Admin panel with broken authentication"""
    # Weak authentication check
    if 'role' in session and session['role'] == 'admin':
        return '''
        <html>
        <body>
            <h2>Admin Panel</h2>
            <p>Welcome, administrator!</p>
            <a href="/admin/users">Manage Users</a>
        </body>
        </html>
        '''

    # Check for admin override parameter (authentication bypass)
    if request.args.get('override') == 'true':
        session['role'] = 'admin'
        return redirect('/admin')

    return "Access denied", 403


@app.route('/admin/users')
def manage_users():
    """Manage users - requires admin access"""
    if 'role' not in session or session['role'] != 'admin':
        return "Access denied", 403

    conn = get_db_connection()
    users = conn.execute("SELECT id, username, email, role FROM users").fetchall()
    conn.close()

    user_list = "<ul>"
    for user in users:
        user_list += f"<li>{user['username']} ({user['role']})</li>"
    user_list += "</ul>"

    return f'''
    <html>
    <body>
        <h2>User Management</h2>
        {user_list}
    </body>
    </html>
    '''


# CORRECT CODE: Proper input validation example
@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    """Get product by ID - properly parameterized query"""
    conn = get_db_connection()
    # This is CORRECT - using parameterized query
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()

    if product:
        return jsonify({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'description': product['description']
        })
    return jsonify({'error': 'Product not found'}), 404


# CORRECT CODE: Proper password hashing (example)
def hash_password(password):
    """
    Example of proper password hashing approach.
    In production, use bcrypt or argon2.
    """
    import hashlib
    # This is a simplified example - use proper libraries in production
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key


# CORRECT CODE: Proper file upload validation
@app.route('/upload/avatar', methods=['POST'])
def upload_avatar():
    """Upload user avatar with proper validation"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    # Proper validation
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Validate file extension
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' not in file.filename:
        return jsonify({'error': 'Invalid file'}), 400

    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'File type not allowed'}), 400

    # Use secure_filename
    filename = secure_filename(file.filename)

    # Validate file size (e.g., max 5MB)
    file.seek(0, os.SEEK_END)
    size = file.tell()
    if size > 5 * 1024 * 1024:
        return jsonify({'error': 'File too large'}), 400

    file.seek(0)

    # Save file
    filepath = os.path.join('/var/www/avatars', filename)
    file.save(filepath)

    return jsonify({'status': 'success', 'filename': filename})


@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        return redirect('/login')

    return f'''
    <html>
    <body>
        <h2>Dashboard</h2>
        <p>Welcome, {session.get('username')}!</p>
        <a href="/logout">Logout</a>
    </body>
    </html>
    '''


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    init_db()
    # VULNERABILITY 10: Debug mode enabled in production
    app.run(debug=True, host='0.0.0.0', port=5000)
