"""
Comprehensive test suite for URL Shortener API
Tests all required functionality, edge cases, and error handling
"""

import pytest
import requests
import json
import time
import re
from urllib.parse import urlparse

# Base URL for the API
BASE_URL = "http://localhost:8080"

# Wait for server to be ready
def wait_for_server(max_attempts=30, delay=0.5):
    """Wait for the server to be ready to accept connections"""
    for _ in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/", timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(delay)
    return False

@pytest.fixture(scope="module", autouse=True)
def check_server():
    """Ensure server is running before tests"""
    if not wait_for_server():
        pytest.skip("Server is not running on port 8080")

@pytest.fixture(autouse=True)
def cleanup_urls():
    """Clean up URLs after each test to ensure test independence"""
    yield
    # Try to get all URLs and delete them
    try:
        response = requests.get(f"{BASE_URL}/urls", timeout=2)
        if response.status_code == 200:
            urls = response.json()
            if isinstance(urls, list):
                for url_data in urls:
                    # Try common field names for short code
                    short_code = url_data.get('short_code') or url_data.get('code') or url_data.get('id')
                    if short_code:
                        requests.delete(f"{BASE_URL}/urls/{short_code}", timeout=2)
    except:
        pass  # Cleanup is best-effort


class TestURLCreation:
    """Tests for creating shortened URLs"""

    def test_create_short_url_basic(self):
        """Test creating a basic shortened URL"""
        response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com/test"}
        )
        assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
        data = response.json()

        # Should return a short code
        assert 'short_code' in data or 'code' in data or 'id' in data, "Response should contain short code"
        short_code = data.get('short_code') or data.get('code') or data.get('id')

        # Validate short code format (6-8 alphanumeric characters)
        assert re.match(r'^[a-zA-Z0-9]{6,8}$', short_code), f"Short code {short_code} must be 6-8 alphanumeric chars"

    def test_create_short_url_with_custom_code(self):
        """Test creating a URL with a custom short code"""
        custom_code = "custom1"
        response = requests.post(
            f"{BASE_URL}/urls",
            json={
                "url": "https://www.example.com/custom",
                "custom_code": custom_code
            }
        )
        # Should accept custom code or reject gracefully
        assert response.status_code in [200, 201, 400, 422], "Should handle custom code request"

        if response.status_code in [200, 201]:
            data = response.json()
            returned_code = data.get('short_code') or data.get('code') or data.get('id')
            # If accepted, should use the custom code
            assert returned_code == custom_code, "Should use custom short code when provided"

    def test_create_duplicate_url(self):
        """Test creating the same URL twice"""
        url = "https://www.example.com/duplicate"

        # Create first time
        response1 = requests.post(f"{BASE_URL}/urls", json={"url": url})
        assert response1.status_code in [200, 201]
        code1 = (response1.json().get('short_code') or
                response1.json().get('code') or
                response1.json().get('id'))

        # Create second time
        response2 = requests.post(f"{BASE_URL}/urls", json={"url": url})
        assert response2.status_code in [200, 201]
        code2 = (response2.json().get('short_code') or
                response2.json().get('code') or
                response2.json().get('id'))

        # Either return same code or create new one (both are valid approaches)
        assert code1 and code2, "Both requests should return short codes"

    def test_create_url_invalid_format(self):
        """Test creating URL with invalid format"""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",  # Not HTTP/HTTPS
            "http://",
            "",
            "javascript:alert(1)",
        ]

        for invalid_url in invalid_urls:
            response = requests.post(
                f"{BASE_URL}/urls",
                json={"url": invalid_url}
            )
            assert response.status_code in [400, 422], f"Should reject invalid URL: {invalid_url}"

    def test_create_url_missing_data(self):
        """Test creating URL with missing data"""
        response = requests.post(f"{BASE_URL}/urls", json={})
        assert response.status_code in [400, 422], "Should reject request with missing URL"

    def test_create_url_very_long(self):
        """Test creating a very long URL (>2000 chars)"""
        long_url = "https://www.example.com/" + "a" * 2500
        response = requests.post(f"{BASE_URL}/urls", json={"url": long_url})
        assert response.status_code in [400, 422], "Should reject URLs longer than 2000 characters"

    def test_create_url_with_query_params(self):
        """Test creating URL with query parameters"""
        url = "https://www.example.com/search?q=test&page=1"
        response = requests.post(f"{BASE_URL}/urls", json={"url": url})
        assert response.status_code in [200, 201], "Should accept URLs with query parameters"

    def test_create_url_with_fragment(self):
        """Test creating URL with fragment/anchor"""
        url = "https://www.example.com/page#section"
        response = requests.post(f"{BASE_URL}/urls", json={"url": url})
        assert response.status_code in [200, 201], "Should accept URLs with fragments"

    def test_conflicting_custom_code(self):
        """Test creating URL with conflicting custom code"""
        custom_code = "conflict"

        # Create first URL with custom code
        response1 = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com/first", "custom_code": custom_code}
        )

        if response1.status_code in [200, 201]:
            # Try to create second URL with same custom code
            response2 = requests.post(
                f"{BASE_URL}/urls",
                json={"url": "https://www.example.com/second", "custom_code": custom_code}
            )
            assert response2.status_code in [400, 409, 422], "Should reject conflicting custom code"


class TestURLRedirection:
    """Tests for URL redirection functionality"""

    def test_redirect_existing_url(self):
        """Test redirecting to an existing shortened URL"""
        # Create a URL first
        create_response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com/redirect-test"}
        )
        assert create_response.status_code in [200, 201]
        short_code = (create_response.json().get('short_code') or
                     create_response.json().get('code') or
                     create_response.json().get('id'))

        # Try to access the short URL
        redirect_response = requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False)

        # Should either redirect (301/302) or return the URL in JSON
        assert redirect_response.status_code in [200, 301, 302], \
            f"Expected redirect or success, got {redirect_response.status_code}"

        if redirect_response.status_code in [301, 302]:
            # Check redirect location
            assert 'Location' in redirect_response.headers, "Redirect should have Location header"
            assert redirect_response.headers['Location'] == "https://www.example.com/redirect-test"

    def test_redirect_nonexistent_url(self):
        """Test accessing a non-existent short code"""
        response = requests.get(f"{BASE_URL}/nonexist", allow_redirects=False)
        assert response.status_code == 404, "Should return 404 for non-existent short code"

    def test_redirect_increments_counter(self):
        """Test that accessing a URL increments its access counter"""
        # Create a URL
        create_response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com/counter-test"}
        )
        short_code = (create_response.json().get('short_code') or
                     create_response.json().get('code') or
                     create_response.json().get('id'))

        # Access it multiple times
        for _ in range(3):
            requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False)

        # Get statistics
        stats_response = requests.get(f"{BASE_URL}/urls/{short_code}/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            access_count = (stats.get('access_count') or stats.get('visits') or
                          stats.get('clicks') or stats.get('count'))
            assert access_count >= 3, "Access count should be at least 3"


class TestURLStatistics:
    """Tests for URL statistics endpoint"""

    def test_get_stats_existing_url(self):
        """Test getting statistics for an existing URL"""
        # Create a URL
        create_response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com/stats-test"}
        )
        short_code = (create_response.json().get('short_code') or
                     create_response.json().get('code') or
                     create_response.json().get('id'))

        # Get statistics
        stats_response = requests.get(f"{BASE_URL}/urls/{short_code}/stats")
        assert stats_response.status_code == 200, "Should return stats for existing URL"

        stats = stats_response.json()

        # Should contain original URL
        assert ('original_url' in stats or 'url' in stats or 'long_url' in stats), \
            "Stats should contain original URL"

        # Should contain access count
        assert ('access_count' in stats or 'visits' in stats or 'clicks' in stats or 'count' in stats), \
            "Stats should contain access count"

        # Should contain creation time
        assert ('created_at' in stats or 'created' in stats or 'timestamp' in stats), \
            "Stats should contain creation timestamp"

    def test_get_stats_nonexistent_url(self):
        """Test getting statistics for a non-existent URL"""
        response = requests.get(f"{BASE_URL}/urls/nonexist/stats")
        assert response.status_code == 404, "Should return 404 for non-existent URL"


class TestListURLs:
    """Tests for listing all URLs"""

    def test_list_urls_empty(self):
        """Test listing URLs when none exist"""
        # Clean up first
        try:
            response = requests.get(f"{BASE_URL}/urls")
            if response.status_code == 200:
                urls = response.json()
                if isinstance(urls, list):
                    for url_data in urls:
                        short_code = (url_data.get('short_code') or
                                    url_data.get('code') or
                                    url_data.get('id'))
                        if short_code:
                            requests.delete(f"{BASE_URL}/urls/{short_code}")
        except:
            pass

        response = requests.get(f"{BASE_URL}/urls")
        assert response.status_code == 200, "Should return 200 for list endpoint"
        data = response.json()
        assert isinstance(data, list), "Should return a list"

    def test_list_urls_with_data(self):
        """Test listing URLs when some exist"""
        # Create a few URLs
        urls_to_create = [
            "https://www.example.com/list1",
            "https://www.example.com/list2",
            "https://www.example.com/list3"
        ]

        for url in urls_to_create:
            requests.post(f"{BASE_URL}/urls", json={"url": url})

        # List all URLs
        response = requests.get(f"{BASE_URL}/urls")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Should return a list"
        assert len(data) >= 3, "Should contain at least 3 URLs"

        # Each item should have required fields
        for item in data:
            assert ('short_code' in item or 'code' in item or 'id' in item), \
                "Each item should have a short code"
            assert ('original_url' in item or 'url' in item or 'long_url' in item), \
                "Each item should have original URL"
            assert ('access_count' in item or 'visits' in item or 'clicks' in item or 'count' in item), \
                "Each item should have access count"
            assert ('created_at' in item or 'created' in item or 'timestamp' in item), \
                "Each item should have creation time"


class TestDeleteURL:
    """Tests for deleting URLs"""

    def test_delete_existing_url(self):
        """Test deleting an existing URL"""
        # Create a URL
        create_response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com/delete-test"}
        )
        short_code = (create_response.json().get('short_code') or
                     create_response.json().get('code') or
                     create_response.json().get('id'))

        # Delete it
        delete_response = requests.delete(f"{BASE_URL}/urls/{short_code}")
        assert delete_response.status_code in [200, 204], "Should successfully delete URL"

        # Verify it's gone
        get_response = requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False)
        assert get_response.status_code == 404, "Deleted URL should return 404"

    def test_delete_nonexistent_url(self):
        """Test deleting a non-existent URL"""
        response = requests.delete(f"{BASE_URL}/urls/nonexist")
        assert response.status_code == 404, "Should return 404 for non-existent URL"


class TestEdgeCases:
    """Tests for various edge cases"""

    def test_url_with_special_characters(self):
        """Test URL with special characters in query params"""
        url = "https://www.example.com/search?q=hello%20world&filter=new"
        response = requests.post(f"{BASE_URL}/urls", json={"url": url})
        assert response.status_code in [200, 201], "Should handle URLs with encoded characters"

    def test_https_url(self):
        """Test that HTTPS URLs are accepted"""
        response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://secure.example.com"}
        )
        assert response.status_code in [200, 201], "Should accept HTTPS URLs"

    def test_http_url(self):
        """Test that HTTP URLs are accepted"""
        response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "http://example.com"}
        )
        assert response.status_code in [200, 201], "Should accept HTTP URLs"

    def test_url_with_port(self):
        """Test URL with explicit port number"""
        url = "https://www.example.com:8443/path"
        response = requests.post(f"{BASE_URL}/urls", json={"url": url})
        assert response.status_code in [200, 201], "Should accept URLs with port numbers"

    def test_url_with_subdomain(self):
        """Test URL with subdomain"""
        url = "https://api.example.com/v1/endpoint"
        response = requests.post(f"{BASE_URL}/urls", json={"url": url})
        assert response.status_code in [200, 201], "Should accept URLs with subdomains"

    def test_international_domain(self):
        """Test URL with international characters"""
        url = "https://example.com/café"
        response = requests.post(f"{BASE_URL}/urls", json={"url": url})
        # Should either accept or reject gracefully
        assert response.status_code in [200, 201, 400, 422], "Should handle international URLs"

    def test_null_url(self):
        """Test sending null URL"""
        response = requests.post(f"{BASE_URL}/urls", json={"url": None})
        assert response.status_code in [400, 422], "Should reject null URL"

    def test_empty_string_url(self):
        """Test sending empty string URL"""
        response = requests.post(f"{BASE_URL}/urls", json={"url": ""})
        assert response.status_code in [400, 422], "Should reject empty URL"

    def test_whitespace_url(self):
        """Test URL that is just whitespace"""
        response = requests.post(f"{BASE_URL}/urls", json={"url": "   "})
        assert response.status_code in [400, 422], "Should reject whitespace-only URL"

    def test_malformed_json(self):
        """Test sending malformed JSON"""
        response = requests.post(
            f"{BASE_URL}/urls",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422], "Should reject malformed JSON"

    def test_url_already_short(self):
        """Test shortening a URL that is already short"""
        url = "https://bit.ly/abc123"
        response = requests.post(f"{BASE_URL}/urls", json={"url": url})
        # Should either accept or reject - both are valid
        assert response.status_code in [200, 201, 400, 422], "Should handle already-short URLs"


class TestHTTPMethods:
    """Tests for proper HTTP method handling"""

    def test_post_to_create(self):
        """Test that POST is used for creating URLs"""
        response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com"}
        )
        assert response.status_code in [200, 201], "POST should create new URL"

    def test_get_to_list(self):
        """Test that GET is used for listing URLs"""
        response = requests.get(f"{BASE_URL}/urls")
        assert response.status_code == 200, "GET should list URLs"

    def test_delete_to_remove(self):
        """Test that DELETE is used for removing URLs"""
        # Create a URL first
        create_response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com/method-test"}
        )
        short_code = (create_response.json().get('short_code') or
                     create_response.json().get('code') or
                     create_response.json().get('id'))

        # Delete it
        response = requests.delete(f"{BASE_URL}/urls/{short_code}")
        assert response.status_code in [200, 204], "DELETE should remove URL"


class TestResponseFormats:
    """Tests for proper response formats"""

    def test_json_response_on_create(self):
        """Test that creating URL returns JSON"""
        response = requests.post(
            f"{BASE_URL}/urls",
            json={"url": "https://www.example.com/json-test"}
        )
        assert 'application/json' in response.headers.get('Content-Type', ''), \
            "Should return JSON response"
        assert isinstance(response.json(), dict), "Response should be JSON object"

    def test_json_response_on_list(self):
        """Test that listing URLs returns JSON"""
        response = requests.get(f"{BASE_URL}/urls")
        assert 'application/json' in response.headers.get('Content-Type', ''), \
            "Should return JSON response"
        assert isinstance(response.json(), list), "Response should be JSON array"

    def test_error_response_format(self):
        """Test that errors return proper JSON"""
        response = requests.post(f"{BASE_URL}/urls", json={"url": "invalid"})
        assert response.status_code in [400, 422]
        # Error response should be JSON
        try:
            error_data = response.json()
            assert isinstance(error_data, dict), "Error should be JSON object"
        except:
            pytest.fail("Error response should be valid JSON")
