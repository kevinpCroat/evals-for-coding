# User Management Application

A simple Flask-based web application and API client for user management.

## Structure

```
starter-code/
├── src/
│   ├── api_client.py    # HTTP API client using requests
│   ├── web_app.py       # Flask web application
│   └── __init__.py
├── tests/
│   ├── test_api_client.py
│   ├── test_web_app.py
│   └── __init__.py
├── requirements.txt     # Dependencies (currently pinned to old versions)
├── KNOWN_ISSUES.md     # List of known security issues
└── README.md           # This file
```

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run all tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## Running the Application

Start the Flask development server:
```bash
python src/web_app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

- `GET /health` - Health check
- `GET /users` - List users (with pagination)
- `GET /users/<id>` - Get user by ID
- `POST /users` - Create new user
- `PUT /users/<id>` - Update user
- `DELETE /users/<id>` - Delete user

## Current State

**WARNING**: This project is using old dependency versions with known security vulnerabilities.
See `KNOWN_ISSUES.md` for details.

The code currently uses some deprecated patterns and features. All tests pass with the current
versions, but the dependencies need to be updated to:
- Fix security vulnerabilities
- Remove deprecation warnings
- Use modern best practices
