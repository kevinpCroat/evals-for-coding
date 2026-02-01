# Greenfield: URL Shortener API - Specification

## Objective

Build a complete REST API for a URL shortening service (like bit.ly or TinyURL) from scratch.

## Background

You are tasked with creating a new URL shortener service that allows users to convert long URLs into short, shareable links. The service should be production-ready with proper error handling, data validation, and comprehensive tests.

This is a greenfield project - you're starting from scratch with no existing codebase. You need to design the architecture, implement all features, and ensure everything is properly tested and documented.

## Requirements

### Functional Requirements

1. **Create Short URL**: Accept a long URL and return a shortened version
   - Generate a unique short code (e.g., "abc123")
   - Store the mapping between short code and original URL
   - Return the short code or full shortened URL

2. **Redirect to Original URL**: Given a short code, redirect to the original URL
   - Look up the original URL by short code
   - Return appropriate response (redirect or error if not found)

3. **Get URL Statistics**: Retrieve information about a shortened URL
   - Show the original URL
   - Track and display the number of times the short URL has been accessed
   - Show when the URL was created

4. **List All URLs**: Return a list of all shortened URLs in the system
   - Should include short code, original URL, access count, and creation time

5. **Delete Short URL**: Remove a shortened URL from the system
   - Validate that the short code exists before deletion

### Technical Constraints

- **Language**: Python with Flask or FastAPI (choose one)
- **Storage**: In-memory data structure (dict/list) - no database required
- **API Format**: RESTful JSON API
- **Short Code**: Must be 6-8 characters, alphanumeric (a-z, A-Z, 0-9)
- **URL Validation**: Validate that submitted URLs are properly formatted
- **Error Handling**: Return appropriate HTTP status codes and error messages
- **Port**: Server should run on port 8080

### Quality Requirements

- Clean, readable code following Python best practices (PEP 8)
- Proper error handling for all edge cases
- Input validation for all endpoints
- Comprehensive test suite covering all functionality
- README with setup instructions and API documentation
- No hardcoded values - use configuration where appropriate

## API Endpoints

Your implementation should provide these endpoints (exact design is up to you):

1. **POST** - Create a new short URL
   - Input: Original URL (and optionally a custom short code)
   - Output: Short code and/or full shortened URL

2. **GET** - Redirect or retrieve original URL
   - Input: Short code
   - Output: Redirect to original URL OR JSON with URL details

3. **GET** - Get statistics for a short URL
   - Input: Short code
   - Output: JSON with original URL, access count, creation timestamp

4. **GET** - List all shortened URLs
   - Output: JSON array of all shortened URLs with their metadata

5. **DELETE** - Remove a shortened URL
   - Input: Short code
   - Output: Confirmation message

## Edge Cases to Handle

- Duplicate URLs (same URL shortened multiple times)
- Invalid URLs (malformed, empty, non-HTTP/HTTPS)
- Conflicting custom short codes
- Accessing non-existent short codes
- Empty or missing request data
- URLs that are already short
- Very long URLs (>2000 characters)

## Success Criteria

The implementation will be considered successful when:

1. All required endpoints are implemented and functional
2. Comprehensive test suite passes with >80% coverage
3. All edge cases are handled gracefully with appropriate error messages
4. Code follows Python best practices and is well-organized
5. README exists with clear setup and usage instructions
6. API returns proper HTTP status codes (200, 201, 404, 400, etc.)

## Deliverables

1. **Source Code**: All Python files implementing the API
2. **Test Suite**: Comprehensive tests for all functionality
3. **README.md**: Documentation including:
   - Setup/installation instructions
   - How to run the server
   - API endpoint documentation with examples
   - How to run tests
4. **requirements.txt**: All Python dependencies
5. **Working Server**: Can be started and tested via HTTP requests

## Evaluation

Your submission will be scored on:

- **Functional Tests Passing**: 40% - All required features work correctly
- **Specification Compliance**: 30% - Meets all requirements in the spec
- **Code Quality**: 20% - Clean code, no duplication, appropriate complexity
- **Documentation**: 10% - README completeness and API documentation

See verification/verify.sh for automated scoring implementation.

## Notes

- You have freedom in exact API design (endpoint paths, request/response formats)
- The spec intentionally leaves some details open - make reasonable decisions
- Focus on getting a working implementation first, then refine
- Consider what would make this production-ready
