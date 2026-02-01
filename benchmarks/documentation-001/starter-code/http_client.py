import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional, Union
from http.client import HTTPResponse
import time


class HTTPError(Exception):
    def __init__(self, status_code: int, message: str, response_body: Optional[str] = None):
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(f"HTTP {status_code}: {message}")


class RetryConfig:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0,
                 retry_statuses: Optional[list] = None):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.retry_statuses = retry_statuses or [500, 502, 503, 504]


class HTTPClient:
    def __init__(self, base_url: str = "", default_headers: Optional[Dict[str, str]] = None,
                 timeout: int = 30, retry_config: Optional[RetryConfig] = None):
        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {}
        self.timeout = timeout
        self.retry_config = retry_config

    def _build_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            url = endpoint
        else:
            endpoint = endpoint.lstrip('/')
            url = f"{self.base_url}/{endpoint}" if self.base_url else endpoint

        if params:
            query_string = urllib.parse.urlencode(params)
            separator = '&' if '?' in url else '?'
            url = f"{url}{separator}{query_string}"

        return url

    def _prepare_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        merged_headers = self.default_headers.copy()
        if headers:
            merged_headers.update(headers)
        return merged_headers

    def _prepare_body(self, data: Optional[Union[Dict, str]] = None,
                     json_data: Optional[Dict] = None) -> Optional[bytes]:
        if json_data is not None:
            return json.dumps(json_data).encode('utf-8')
        elif isinstance(data, dict):
            return urllib.parse.urlencode(data).encode('utf-8')
        elif isinstance(data, str):
            return data.encode('utf-8')
        return None

    def _execute_request(self, method: str, url: str, headers: Dict[str, str],
                        body: Optional[bytes] = None) -> HTTPResponse:
        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            response = urllib.request.urlopen(req, timeout=self.timeout)
            return response
        except urllib.error.HTTPError as e:
            response_body = e.read().decode('utf-8', errors='ignore') if e.fp else None
            raise HTTPError(e.code, e.reason, response_body)
        except urllib.error.URLError as e:
            raise HTTPError(0, str(e.reason))

    def _should_retry(self, error: HTTPError, attempt: int) -> bool:
        if not self.retry_config or attempt >= self.retry_config.max_retries:
            return False
        return error.status_code in self.retry_config.retry_statuses

    def _calculate_backoff(self, attempt: int) -> float:
        if not self.retry_config:
            return 0
        return self.retry_config.backoff_factor * (2 ** attempt)

    def request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None, data: Optional[Union[Dict, str]] = None,
                json_data: Optional[Dict] = None) -> 'Response':
        url = self._build_url(endpoint, params)
        merged_headers = self._prepare_headers(headers)

        if json_data is not None and 'Content-Type' not in merged_headers:
            merged_headers['Content-Type'] = 'application/json'
        elif isinstance(data, dict) and 'Content-Type' not in merged_headers:
            merged_headers['Content-Type'] = 'application/x-www-form-urlencoded'

        body = self._prepare_body(data, json_data)

        attempt = 0
        last_error = None

        while attempt <= (self.retry_config.max_retries if self.retry_config else 0):
            try:
                http_response = self._execute_request(method, url, merged_headers, body)
                return Response(http_response)
            except HTTPError as e:
                last_error = e
                if self._should_retry(e, attempt):
                    backoff = self._calculate_backoff(attempt)
                    time.sleep(backoff)
                    attempt += 1
                else:
                    raise

        raise last_error

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> 'Response':
        return self.request('GET', endpoint, params=params, headers=headers)

    def post(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
             json_data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> 'Response':
        return self.request('POST', endpoint, headers=headers, data=data, json_data=json_data)

    def put(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
            json_data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> 'Response':
        return self.request('PUT', endpoint, headers=headers, data=data, json_data=json_data)

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> 'Response':
        return self.request('DELETE', endpoint, headers=headers)

    def patch(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
              json_data: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> 'Response':
        return self.request('PATCH', endpoint, headers=headers, data=data, json_data=json_data)


class Response:
    def __init__(self, http_response: HTTPResponse):
        self._response = http_response
        self._content = None
        self._text = None
        self._json_data = None

    @property
    def status_code(self) -> int:
        return self._response.status

    @property
    def headers(self) -> Dict[str, str]:
        return dict(self._response.headers)

    @property
    def content(self) -> bytes:
        if self._content is None:
            self._content = self._response.read()
        return self._content

    @property
    def text(self) -> str:
        if self._text is None:
            charset = self._get_charset()
            self._text = self.content.decode(charset, errors='replace')
        return self._text

    def _get_charset(self) -> str:
        content_type = self._response.headers.get('Content-Type', '')
        if 'charset=' in content_type:
            return content_type.split('charset=')[-1].split(';')[0].strip()
        return 'utf-8'

    def json(self) -> Union[Dict, list]:
        if self._json_data is None:
            self._json_data = json.loads(self.text)
        return self._json_data

    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    def is_redirect(self) -> bool:
        return 300 <= self.status_code < 400

    def is_client_error(self) -> bool:
        return 400 <= self.status_code < 500

    def is_server_error(self) -> bool:
        return 500 <= self.status_code < 600
