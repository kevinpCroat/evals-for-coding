# Documentation Benchmark: HTTP Client Library

## Objective

Document a fully functional but completely undocumented Python HTTP client library. This benchmark tests your ability to understand code, write clear API documentation, create working examples, and follow documentation best practices.

## Background

The `starter-code/http_client.py` file contains a production-quality HTTP client library with approximately 180 lines of code. The library includes:

- An `HTTPClient` class for making HTTP requests
- A `Response` class for handling HTTP responses
- A `RetryConfig` class for configuring retry behavior
- An `HTTPError` exception class for error handling

The code is fully functional and well-structured, but has **zero documentation** - no docstrings, no comments, no usage examples.

## Requirements

### Functional Requirements
1. **Document all public APIs** - Add comprehensive docstrings to all public classes, methods, and functions
2. **Include working code examples** - Every docstring must include at least one code example that actually executes without errors
3. **Follow Google-style docstrings** - Use consistent formatting throughout (Google Python Style Guide format)
4. **Document parameters and return values** - All parameters, return types, exceptions, and attributes must be documented

### Technical Constraints
- Do not modify the actual implementation code (function bodies)
- Do not change function signatures or class interfaces
- Only add docstrings and documentation - no new functionality
- Code examples in docstrings must be valid Python that can be executed

### Quality Requirements
- Docstrings must accurately reflect what the code actually does
- Parameter descriptions must match the actual parameter types and usage
- Examples must demonstrate realistic use cases
- Documentation must be clear and concise - avoid unnecessary verbosity

## Success Criteria

The documentation will be considered successful when:
1. All public APIs (classes, methods, functions) have comprehensive docstrings
2. All code examples in the docstrings execute successfully
3. Docstrings accurately describe the actual behavior of the code
4. Documentation follows Google-style format consistently

## Deliverables

Update `starter-code/http_client.py` to include:

1. **Class Docstrings** (25% of score)
   - Document `HTTPClient`, `Response`, `RetryConfig`, and `HTTPError`
   - Include class-level description, attributes, and usage examples
   - Explain the purpose and typical use cases

2. **Method Docstrings** (25% of score)
   - Document all public methods
   - Include Args, Returns, Raises sections
   - Describe what each method does and when to use it

3. **Working Code Examples** (30% of score)
   - At least one example per class showing typical usage
   - Examples must execute without errors
   - Demonstrate realistic scenarios (not trivial examples)

4. **Accuracy and Consistency** (20% of score)
   - Docstrings match actual function signatures
   - Parameter types match implementation
   - Return types accurately described
   - Exception documentation matches what code actually raises
   - Consistent format throughout

## Documentation Format

Use Google-style Python docstrings. Example:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief one-line description of the function.

    More detailed description if needed. Explain what the function
    does, when to use it, and any important behavior.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param2 is negative.
        TypeError: When param1 is not a string.

    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    """
    # implementation...
```

## Important Notes

- **Read the code carefully** - Understand what it actually does before documenting
- **Test your examples** - All code examples must work when executed
- **Be accurate** - Documentation that contradicts the code is worse than no documentation
- **Be concise** - Clear and brief is better than verbose
- **Focus on the user** - Write for someone who wants to use the library, not for yourself

## Getting Started

1. Read through `starter-code/http_client.py` to understand the implementation
2. Identify all public APIs (classes, methods, functions)
3. Write docstrings following Google style
4. Include working code examples in docstrings
5. Run verification to check your documentation quality

## Evaluation

Your documentation will be scored on:
- **API Coverage**: 30% - Percentage of public APIs with docstrings
- **Example Execution**: 40% - Whether code examples actually work
- **Docs-Code Consistency**: 20% - Whether docstrings match actual signatures
- **Readability**: 10% - Format consistency and clarity

See `verification/verify.sh` for automated scoring implementation.
