# Example Solution

This file demonstrates what a well-documented version of the HTTP client would look like.

## What Good Documentation Includes

For each class:
- Clear description of purpose
- List of important attributes
- Usage example that actually works

For each method:
- Brief description
- Args section with all parameters
- Returns section
- Raises section (if applicable)
- Example section showing usage

## Example Class Documentation

```python
class HTTPClient:
    """A simple HTTP client for making web requests.

    This client supports common HTTP methods (GET, POST, PUT, DELETE, PATCH)
    with optional retry logic and custom headers.

    Attributes:
        base_url: Base URL prepended to all requests.
        default_headers: Headers included in every request.
        timeout: Request timeout in seconds.
        retry_config: Retry configuration (optional).

    Example:
        Basic usage:

        client = HTTPClient(base_url="https://api.example.com")
        response = client.get("/users/123")
        print(response.status_code)
    """
```

## Example Method Documentation

```python
def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None) -> 'Response':
    """Send a GET request to the specified endpoint.

    Args:
        endpoint: URL path or full URL to request.
        params: Query parameters to include in URL.
        headers: Additional headers for this request.

    Returns:
        Response object containing the server's response.

    Raises:
        HTTPError: If the request fails or returns an error status.

    Example:
        Get user data with query parameters:

        client = HTTPClient(base_url="https://api.example.com")
        response = client.get("/users", params={"page": 1})
        users = response.json()
    """
```

## Scoring Breakdown

A perfect solution would score:

1. **API Coverage (30/30)**: All 4 classes and 15+ methods documented
2. **Example Execution (40/40)**: All examples run successfully
3. **Consistency (20/20)**: All parameter docs match signatures
4. **Readability (10/10)**: Consistent Google-style format

Total: 100/100
