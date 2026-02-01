"""Tests for the API client module."""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from src.api_client import APIClient, APIClientError


class TestAPIClient:
    """Test suite for APIClient class."""

    @pytest.fixture
    def client(self):
        """Create an API client instance for testing."""
        return APIClient("https://api.example.com", "test-api-key")

    @pytest.fixture
    def mock_response(self):
        """Create a mock response object."""
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {"id": 1, "name": "Test User"}
        return mock

    def test_init(self, client):
        """Test client initialization."""
        assert client.base_url == "https://api.example.com"
        assert client.api_key == "test-api-key"
        assert isinstance(client.session, requests.Session)
        assert client.session.headers['Authorization'] == 'Bearer test-api-key'

    def test_base_url_trailing_slash_removed(self):
        """Test that trailing slash is removed from base URL."""
        client = APIClient("https://api.example.com/", "key")
        assert client.base_url == "https://api.example.com"

    @patch('src.api_client.requests.Session.get')
    def test_get_user_success(self, mock_get, client, mock_response):
        """Test successful user retrieval."""
        mock_get.return_value = mock_response

        result = client.get_user(1)

        assert result == {"id": 1, "name": "Test User"}
        mock_get.assert_called_once_with(
            'https://api.example.com/users/1',
            timeout=10
        )

    @patch('src.api_client.requests.Session.get')
    def test_get_user_not_found(self, mock_get, client):
        """Test user not found returns None."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        result = client.get_user(999)

        assert result is None

    @patch('src.api_client.requests.Session.get')
    def test_get_user_server_error(self, mock_get, client):
        """Test server error raises exception."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            client.get_user(1)

    @patch('src.api_client.requests.Session.get')
    def test_list_users_success(self, mock_get, client):
        """Test successful user listing."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "users": [{"id": 1}, {"id": 2}],
            "total": 2
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = client.list_users(page=1, per_page=10)

        assert result == [{"id": 1}, {"id": 2}]
        mock_get.assert_called_once()

    @patch('src.api_client.requests.Session.post')
    def test_create_user_success(self, mock_post, client, mock_response):
        """Test successful user creation."""
        user_data = {"name": "New User", "email": "new@example.com"}
        mock_post.return_value = mock_response

        result = client.create_user(user_data)

        assert result == {"id": 1, "name": "Test User"}
        mock_post.assert_called_once_with(
            'https://api.example.com/users',
            json=user_data,
            timeout=10
        )

    @patch('src.api_client.requests.Session.put')
    def test_update_user_success(self, mock_put, client, mock_response):
        """Test successful user update."""
        user_data = {"name": "Updated User"}
        mock_put.return_value = mock_response

        result = client.update_user(1, user_data)

        assert result == {"id": 1, "name": "Test User"}
        mock_put.assert_called_once_with(
            'https://api.example.com/users/1',
            json=user_data,
            timeout=10
        )

    @patch('src.api_client.requests.Session.delete')
    def test_delete_user_success(self, mock_delete, client):
        """Test successful user deletion."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response

        result = client.delete_user(1)

        assert result is True
        mock_delete.assert_called_once_with(
            'https://api.example.com/users/1',
            timeout=10
        )

    def test_close(self, client):
        """Test session close."""
        with patch.object(client.session, 'close') as mock_close:
            client.close()
            mock_close.assert_called_once()

    @patch('src.api_client.requests.Session.get')
    def test_request_exception_handling(self, mock_get, client):
        """Test that request exceptions are properly handled."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with pytest.raises(APIClientError) as exc_info:
            client.get_user(1)

        assert "Failed to fetch user 1" in str(exc_info.value)
