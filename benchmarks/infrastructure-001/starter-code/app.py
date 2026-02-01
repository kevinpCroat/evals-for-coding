"""
Task Management API
A simple Flask REST API for managing tasks
"""
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'database': os.environ.get('DB_NAME', 'taskdb'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'password')
}

# S3 configuration
S3_BUCKET = os.environ.get('S3_BUCKET', 'task-attachments')

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize database schema"""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()

        # Create tasks table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                priority VARCHAR(20) DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP
            )
        """)

        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(200) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancer"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200
    else:
        return jsonify({'status': 'unhealthy', 'error': 'database connection failed'}), 503

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 503

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cur.fetchall()
        cur.close()
        conn.close()

        # Convert datetime objects to strings
        for task in tasks:
            for key, value in task.items():
                if isinstance(value, datetime):
                    task[key] = value.isoformat()

        return jsonify({'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 503

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cur.fetchone()
        cur.close()
        conn.close()

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Convert datetime objects to strings
        for key, value in task.items():
            if isinstance(value, datetime):
                task[key] = value.isoformat()

        return jsonify(task), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 503

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            INSERT INTO tasks (title, description, status, priority, due_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                data['title'],
                data.get('description', ''),
                data.get('status', 'pending'),
                data.get('priority', 'medium'),
                data.get('due_date')
            )
        )
        task = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        # Convert datetime objects to strings
        for key, value in task.items():
            if isinstance(value, datetime):
                task[key] = value.isoformat()

        return jsonify(task), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 503

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Build update query dynamically
        update_fields = []
        values = []

        for field in ['title', 'description', 'status', 'priority', 'due_date']:
            if field in data:
                update_fields.append(f"{field} = %s")
                values.append(data[field])

        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400

        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(task_id)

        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
        cur.execute(query, values)
        task = cur.fetchone()

        if not task:
            conn.close()
            return jsonify({'error': 'Task not found'}), 404

        conn.commit()
        cur.close()
        conn.close()

        # Convert datetime objects to strings
        for key, value in task.items():
            if isinstance(value, datetime):
                task[key] = value.isoformat()

        return jsonify(task), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 503

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
        deleted = cur.fetchone()

        if not deleted:
            conn.close()
            return jsonify({'error': 'Task not found'}), 404

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Task Management API',
        'version': '1.0.0',
        'endpoints': [
            'GET /health',
            'GET /tasks',
            'GET /tasks/<id>',
            'POST /tasks',
            'PUT /tasks/<id>',
            'DELETE /tasks/<id>'
        ]
    }), 200

if __name__ == '__main__':
    # Initialize database on startup
    if init_db():
        print("Database initialized successfully")
    else:
        print("Warning: Database initialization failed")

    # Run the application
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
