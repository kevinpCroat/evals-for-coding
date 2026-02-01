"""
User Management System - Pull Request #142
This module handles user authentication, data retrieval, and session management.
"""

import sqlite3
import hashlib
import os
import time
from datetime import datetime
from threading import Thread

# Configuration
DATABASE_URL = "users.db"
API_KEY = "sk-prod-a8f9d2e1c4b7a3f6"  # Bug: Hardcoded API key

class UserManager:
    def __init__(self, db_path=DATABASE_URL):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cache = {}

    def authenticate_user(self, username, password):
        """Authenticate user with username and password."""
        # Bug: SQL injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return True
        return False

    def get_user_by_id(self, user_id):
        """Retrieve user information by ID."""
        # This is correct - using parameterized query
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    def get_active_users(self):
        """Get all active users from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE is_active = 1")
        users = cursor.fetchall()

        # Bug: Off-by-one error - skips first user
        active_users = []
        for i in range(1, len(users)):
            active_users.append(users[i])

        return active_users

    def hash_password(self, password):
        """Hash password for secure storage."""
        # This is correct - using SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def update_user_status(self, user_id, is_active):
        """Update user active status."""
        # Bug: Resource leak - cursor not closed
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (is_active, user_id))
        self.connection.commit()
        # Missing: cursor.close()

    def batch_process_users(self, user_ids):
        """Process multiple users in batch."""
        # Bug: Inefficient - N+1 query problem
        results = []
        for user_id in user_ids:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            if user:
                results.append(user)
            cursor.close()
        return results

    def export_user_data(self, filename):
        """Export all user data to a file."""
        # Bug: File handle not closed
        file = open(filename, 'w')
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        for user in users:
            file.write(str(user) + '\n')

        cursor.close()
        # Missing: file.close()
        return True

    def calculate_user_score(self, login_count, activity_days):
        """Calculate user engagement score."""
        # Bug: Wrong operator - should use multiplication, not addition
        base_score = login_count + activity_days

        # Bug: Division by zero if login_count is 0
        engagement_ratio = activity_days / login_count

        return base_score * engagement_ratio

    def process_async_task(self, user_id):
        """Process user task asynchronously."""
        # Bug: Race condition - shared cache access without locking
        def update_cache():
            user = self.get_user_by_id(user_id)
            self.cache[user_id] = user
            time.sleep(0.1)  # Simulate processing
            self.cache[user_id] = None

        thread = Thread(target=update_cache)
        thread.start()
        # This is correct - starting a thread properly
        return thread

    def validate_email(self, email):
        """Validate email format."""
        # This is correct - basic email validation
        return '@' in email and '.' in email.split('@')[1]

    def get_user_permissions(self, user_id):
        """Get user permissions from database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT permissions FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        cursor.close()

        # Bug: No error handling - will crash if user not found
        return result[0].split(',')

    def cleanup_old_sessions(self, days_old):
        """Remove sessions older than specified days."""
        # This is correct - proper date handling
        cutoff_date = datetime.now().timestamp() - (days_old * 86400)
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM sessions WHERE created_at < ?", (cutoff_date,))
        self.connection.commit()
        cursor.close()
        return cursor.rowcount

    def search_users(self, search_term):
        """Search for users by name or email."""
        # Bug: SQL injection via string formatting
        query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def __del__(self):
        """Cleanup database connection."""
        # This is correct - closing connection on cleanup
        if hasattr(self, 'connection'):
            self.connection.close()
