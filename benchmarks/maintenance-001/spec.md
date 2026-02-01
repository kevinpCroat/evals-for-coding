# Dependency Maintenance: Security Updates - Specification

## Objective

Update all project dependencies to their latest stable versions, fix security vulnerabilities, handle breaking changes, and ensure all tests continue to pass.

## Background

You have inherited a Python web application that has been running in production for several years. The project uses Flask for the web framework and the requests library for HTTP client functionality. However, the dependencies have not been updated since 2021 and now have known security vulnerabilities.

The codebase includes:
- A Flask web application (`src/web_app.py`)
- An HTTP API client (`src/api_client.py`)
- Comprehensive test suite (`tests/`)
- Documentation of known security issues (`KNOWN_ISSUES.md`)

All tests currently pass with the old dependency versions, but you need to update everything to modern, secure versions while maintaining functionality.

## Requirements

### Functional Requirements
1. Update all dependencies in `requirements.txt` to latest stable versions
2. Ensure the application remains functional after updates
3. Fix any code that breaks due to dependency updates
4. Address all deprecation warnings
5. All existing tests must continue to pass

### Technical Constraints
- Must use Python 3.8 or higher
- Cannot modify test files - they define the expected behavior
- Must maintain backward compatibility with existing API
- Must use only well-established, actively maintained packages
- No new dependencies should be added (only update existing ones)

### Security Requirements
- Address all security vulnerabilities listed in `KNOWN_ISSUES.md`
- Update Flask to version >= 2.3.0 (fixes CVE-2023-30861)
- Update Werkzeug to version >= 2.3.0 (fixes CVE-2023-25577)
- Update requests to version >= 2.31.0 (fixes CVE-2023-32681)
- No new security vulnerabilities should be introduced

### Quality Requirements
- All existing tests must pass
- No deprecation warnings when running tests
- Code must run cleanly without warnings
- Maintain existing code style and structure
- Update only what is necessary to support new dependencies

## Success Criteria

The implementation will be considered successful when:

1. **All dependencies are updated** - `requirements.txt` contains latest stable versions
2. **All tests pass** - Running `pytest tests/ -v` shows 100% pass rate
3. **No deprecation warnings** - Running tests with `-W default` flag shows no warnings
4. **Security vulnerabilities fixed** - All CVEs mentioned in `KNOWN_ISSUES.md` are resolved
5. **Application functionality preserved** - No regression in features or behavior

## Deliverables

1. Updated `requirements.txt` with new dependency versions
2. Modified source code (if needed) to work with new dependencies
3. All tests passing with new dependency versions
4. Clean test run with no deprecation warnings

## Evaluation

Your submission will be scored on:

- **Dependencies Updated**: 40% - All dependencies updated to latest stable versions that fix security issues
- **Tests Pass**: 40% - All existing tests pass with new dependency versions
- **No Warnings**: 20% - Code runs cleanly without deprecation warnings

See verification/verify.sh for automated scoring implementation.

## Getting Started

1. Review `KNOWN_ISSUES.md` to understand the security vulnerabilities
2. Check current dependency versions in `requirements.txt`
3. Research the latest stable versions of each dependency
4. Create a plan for updating dependencies (recommended order provided in KNOWN_ISSUES.md)
5. Update `requirements.txt` and install new versions
6. Run tests and fix any breaking changes
7. Address deprecation warnings
8. Verify all tests pass cleanly

## Tips

- Update dependencies incrementally rather than all at once
- Run tests after each update to isolate issues
- Pay attention to major version changes (e.g., Flask 1.x → 2.x)
- Use `pytest -W default` to see deprecation warnings
- Check the official migration guides for each package
- Flask and Werkzeug should be updated together (they're tightly coupled)
