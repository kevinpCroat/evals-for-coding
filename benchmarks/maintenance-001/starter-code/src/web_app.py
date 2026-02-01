"""
Simple Flask web application for managing users.

This uses Flask with some older patterns that may generate deprecation warnings.
"""

from flask import Flask, request, jsonify
import json
from typing import Dict, List
import os


# Create Flask app - this pattern works but may show deprecation warnings in newer versions
app = Flask(__name__)

# In-memory user storage (for demo purposes)
users_db: Dict[int, Dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}
next_user_id = 3


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route('/users', methods=['GET'])
def list_users():
    """List all users with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Simple pagination
    all_users = list(users_db.values())
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = all_users[start:end]

    return jsonify({
        "users": paginated_users,
        "page": page,
        "per_page": per_page,
        "total": len(all_users)
    }), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID."""
    user = users_db.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    global next_user_id

    if not request.json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = {
        "id": next_user_id,
        "name": data['name'],
        "email": data['email']
    }
    users_db[next_user_id] = user
    next_user_id += 1

    return jsonify(user), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user."""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404

    if not request.json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json
    user = users_db[user_id]

    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']

    return jsonify(user), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404

    del users_db[user_id]
    return '', 204


def create_app(config=None):
    """Application factory pattern."""
    if config:
        app.config.update(config)
    return app


if __name__ == '__main__':
    # This pattern may show deprecation warnings in newer Flask versions
    app.run(debug=True, host='0.0.0.0', port=5000)
