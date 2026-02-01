"""
API Client for fetching user data from a REST API.

This module uses requests library to interact with external APIs.
"""

import requests
import json
from typing import Dict, List, Optional


class APIClient:
    """Client for interacting with the User API."""

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def get_user(self, user_id: int) -> Optional[Dict]:
        """
        Fetch user by ID.

        Args:
            user_id: The user ID to fetch

        Returns:
            User data dictionary or None if not found
        """
        url = f'{self.base_url}/users/{user_id}'

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Failed to fetch user {user_id}: {e}")

    def list_users(self, page: int = 1, per_page: int = 10) -> List[Dict]:
        """
        List users with pagination.

        Args:
            page: Page number (1-indexed)
            per_page: Number of users per page

        Returns:
            List of user dictionaries
        """
        url = f'{self.base_url}/users'
        params = {'page': page, 'per_page': per_page}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('users', [])
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Failed to list users: {e}")

    def create_user(self, user_data: Dict) -> Dict:
        """
        Create a new user.

        Args:
            user_data: User data to create

        Returns:
            Created user data
        """
        url = f'{self.base_url}/users'

        try:
            response = self.session.post(url, json=user_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Failed to create user: {e}")

    def update_user(self, user_id: int, user_data: Dict) -> Dict:
        """
        Update an existing user.

        Args:
            user_id: The user ID to update
            user_data: Updated user data

        Returns:
            Updated user data
        """
        url = f'{self.base_url}/users/{user_id}'

        try:
            response = self.session.put(url, json=user_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Failed to update user {user_id}: {e}")

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: The user ID to delete

        Returns:
            True if deleted successfully
        """
        url = f'{self.base_url}/users/{user_id}'

        try:
            response = self.session.delete(url, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise APIClientError(f"Failed to delete user {user_id}: {e}")

    def close(self):
        """Close the session."""
        self.session.close()


class APIClientError(Exception):
    """Exception raised for API client errors."""
    pass
