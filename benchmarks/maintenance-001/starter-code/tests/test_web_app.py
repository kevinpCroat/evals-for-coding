"""Tests for the Flask web application."""

import pytest
import json
from src.web_app import create_app, users_db


@pytest.fixture
def app():
    """Create a test Flask application."""
    app = create_app({'TESTING': True})
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the in-memory database before each test."""
    users_db.clear()
    users_db.update({
        1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
        2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
    })
    # Reset the next_user_id in the module
    import src.web_app
    src.web_app.next_user_id = 3


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns healthy status."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestListUsers:
    """Tests for listing users endpoint."""

    def test_list_users_default_pagination(self, client):
        """Test listing users with default pagination."""
        response = client.get('/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['users']) == 2
        assert data['page'] == 1
        assert data['per_page'] == 10
        assert data['total'] == 2

    def test_list_users_custom_pagination(self, client):
        """Test listing users with custom pagination."""
        response = client.get('/users?page=1&per_page=1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['users']) == 1
        assert data['per_page'] == 1

    def test_list_users_empty_page(self, client):
        """Test listing users on empty page."""
        response = client.get('/users?page=10&per_page=10')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['users']) == 0


class TestGetUser:
    """Tests for getting a single user."""

    def test_get_existing_user(self, client):
        """Test getting an existing user."""
        response = client.get('/users/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == 1
        assert data['name'] == 'Alice'
        assert data['email'] == 'alice@example.com'

    def test_get_nonexistent_user(self, client):
        """Test getting a non-existent user."""
        response = client.get('/users/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data


class TestCreateUser:
    """Tests for creating users."""

    def test_create_user_success(self, client):
        """Test successfully creating a user."""
        new_user = {
            "name": "Charlie",
            "email": "charlie@example.com"
        }
        response = client.post('/users',
                                data=json.dumps(new_user),
                                content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['id'] == 3
        assert data['name'] == 'Charlie'
        assert data['email'] == 'charlie@example.com'

    def test_create_user_missing_fields(self, client):
        """Test creating user with missing required fields."""
        incomplete_user = {"name": "Charlie"}
        response = client.post('/users',
                                data=json.dumps(incomplete_user),
                                content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_user_not_json(self, client):
        """Test creating user without JSON content type."""
        response = client.post('/users', data="not json")
        # Flask 1.x returns 400, Flask 2.x+ returns 415 (Unsupported Media Type)
        assert response.status_code in [400, 415]


class TestUpdateUser:
    """Tests for updating users."""

    def test_update_user_success(self, client):
        """Test successfully updating a user."""
        updates = {"name": "Alice Updated"}
        response = client.put('/users/1',
                               data=json.dumps(updates),
                               content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Alice Updated'
        assert data['email'] == 'alice@example.com'  # unchanged

    def test_update_nonexistent_user(self, client):
        """Test updating a non-existent user."""
        updates = {"name": "Nobody"}
        response = client.put('/users/999',
                               data=json.dumps(updates),
                               content_type='application/json')
        assert response.status_code == 404

    def test_update_user_not_json(self, client):
        """Test updating user without JSON content type."""
        response = client.put('/users/1', data="not json")
        # Flask 1.x returns 400, Flask 2.x+ returns 415 (Unsupported Media Type)
        assert response.status_code in [400, 415]


class TestDeleteUser:
    """Tests for deleting users."""

    def test_delete_user_success(self, client):
        """Test successfully deleting a user."""
        response = client.delete('/users/1')
        assert response.status_code == 204

        # Verify user is deleted
        get_response = client.get('/users/1')
        assert get_response.status_code == 404

    def test_delete_nonexistent_user(self, client):
        """Test deleting a non-existent user."""
        response = client.delete('/users/999')
        assert response.status_code == 404


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_full_user_lifecycle(self, client):
        """Test creating, reading, updating, and deleting a user."""
        # Create
        new_user = {"name": "Dave", "email": "dave@example.com"}
        create_response = client.post('/users',
                                       data=json.dumps(new_user),
                                       content_type='application/json')
        assert create_response.status_code == 201
        created_user = json.loads(create_response.data)
        user_id = created_user['id']

        # Read
        read_response = client.get(f'/users/{user_id}')
        assert read_response.status_code == 200
        assert json.loads(read_response.data)['name'] == 'Dave'

        # Update
        update_response = client.put(f'/users/{user_id}',
                                       data=json.dumps({"name": "Dave Updated"}),
                                       content_type='application/json')
        assert update_response.status_code == 200
        assert json.loads(update_response.data)['name'] == 'Dave Updated'

        # Delete
        delete_response = client.delete(f'/users/{user_id}')
        assert delete_response.status_code == 204

        # Verify deletion
        verify_response = client.get(f'/users/{user_id}')
        assert verify_response.status_code == 404
