# Known Issues with Current Dependencies

This document lists known security vulnerabilities and issues with the current dependency versions.

## Security Vulnerabilities

### Flask 1.1.2 (CVE-2023-30861)
- **Severity**: High
- **Issue**: Flask before 2.2.5 has a security vulnerability where the application can fail to properly sanitize session cookie values
- **Impact**: Potential for session manipulation attacks
- **Fix**: Update to Flask >= 2.3.0

### Werkzeug 1.0.1 (CVE-2023-25577)
- **Severity**: High
- **Issue**: Werkzeug versions before 2.2.3 have a security vulnerability in the debugger pin
- **Impact**: Unauthorized access to debugger in production environments
- **Fix**: Update to Werkzeug >= 2.3.0

### requests 2.25.0 (CVE-2023-32681)
- **Severity**: Medium
- **Issue**: Requests library before 2.31.0 has an improper verification of SSL certificates vulnerability
- **Impact**: Potential for man-in-the-middle attacks
- **Fix**: Update to requests >= 2.31.0

## Deprecated Features

### Flask
- The `app.run()` method used in development is deprecated in favor of using the Flask CLI
- Direct use of `app.config.update()` in application factory should use environment-specific configs

### Click 7.1.2
- Some parameter types have been deprecated in favor of newer equivalents
- Old-style command decorators may show warnings

## Breaking Changes to Watch For

When updating dependencies, be aware of these potential breaking changes:

### Flask 1.x → 2.x → 3.x
- Flask 2.0+ requires Python 3.7+
- `flask.json` module changes in Flask 2.2+
- Some Werkzeug imports may need to be updated
- Test client API changes

### requests 2.25.0 → 2.31.0+
- Minor API improvements, mostly backward compatible
- Better type hints and error messages

### pytest 6.x → 7.x → 8.x
- pytest 7.0+ requires Python 3.7+
- Some internal APIs may have changed
- Plugin compatibility may need verification

## Recommended Update Path

1. Update to latest pytest first (tests should continue to work)
2. Update requests (minimal breaking changes)
3. Update Flask and Werkzeug together (they're closely related)
4. Update click last
5. Run full test suite after each update
6. Address any deprecation warnings

## Testing After Updates

After updating dependencies:
1. Run `pytest tests/ -v` - all tests must pass
2. Run with warnings enabled: `pytest tests/ -v -W default` - fix any DeprecationWarnings
3. Check for security vulnerabilities: `pip list --outdated`
4. Verify the application still runs correctly
