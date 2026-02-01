# API Design Benchmark (api-design-001)

## Overview

This benchmark evaluates an AI's ability to design a comprehensive REST API using OpenAPI 3.0 specification. It tests understanding of API design principles, REST best practices, and the ability to create production-ready API contracts.

## Task Description

Design a complete OpenAPI 3.0 specification for an e-commerce order management system. The API must support:

- Product catalog management
- Customer accounts and authentication
- Shopping cart operations
- Order processing and tracking
- Payment processing
- Shipment tracking
- Product reviews

## Evaluation Criteria

The benchmark scores submissions across five dimensions:

1. **Required Endpoints (30%)**: Coverage of all necessary API operations
   - Minimum 25 distinct endpoint paths
   - All core resources (products, orders, customers, cart, payments, reviews)
   - CRUD operations where appropriate
   - Authentication endpoints

2. **Schema Completeness (25%)**: Quality and completeness of data schemas
   - Request/response schemas fully defined
   - Proper use of OpenAPI components and $ref
   - Validation constraints (min, max, pattern, enum)
   - Required vs. optional fields clearly marked

3. **REST Best Practices (25%)**: Adherence to REST principles
   - Correct HTTP methods (GET, POST, PUT, PATCH, DELETE)
   - Appropriate status codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 500)
   - Resource-based URL structure
   - Pagination, filtering, and sorting support
   - Proper use of path parameters

4. **Documentation Quality (10%)**: Clarity and completeness of documentation
   - Endpoint descriptions and summaries
   - Parameter descriptions
   - Response descriptions
   - Examples provided

5. **Versioning Strategy (10%)**: API versioning approach
   - Version in URL structure (e.g., /v1/)
   - Versioning strategy documented

**Pass Threshold**: 70/100

## Files and Structure

```
api-design-001/
├── README.md                    # This file
├── requirements.md              # Detailed business requirements
├── spec.md                      # Task specification
├── prompts.txt                  # Prompts to provide to AI
├── verification/
│   ├── tests/
│   │   └── test_openapi_spec.py # Automated test suite
│   └── verify.sh                # Verification script
└── [openapi.yaml/json]          # Your submission (created by AI)
```

## Running the Benchmark

1. **Review the requirements**:
   ```bash
   cat requirements.md
   cat spec.md
   ```

2. **Provide the task to the AI**:
   ```bash
   cat prompts.txt
   ```

3. **Verify the implementation**:
   ```bash
   ./verification/verify.sh
   ```

The verification script will:
- Check for the OpenAPI specification file (openapi.yaml or openapi.json)
- Validate the file format (YAML/JSON parsing)
- Validate against OpenAPI 3.0 schema (if openapi-spec-validator is installed)
- Run comprehensive test suite checking:
  - Endpoint coverage
  - Schema definitions
  - HTTP method usage
  - Status code appropriateness
  - REST best practices
  - Security definitions
  - Documentation quality
- Output a JSON score with component breakdowns

## Expected Output

The verification script outputs JSON with the following structure:

```json
{
  "benchmark": "api-design-001",
  "timestamp": "2026-01-31T12:00:00Z",
  "components": {
    "required_endpoints": {
      "score": 85,
      "weight": 0.30,
      "details": "Passed 8/9 endpoint coverage tests"
    },
    "schema_completeness": {
      "score": 90,
      "weight": 0.25,
      "details": "Passed 9/10 schema completeness tests"
    },
    "rest_best_practices": {
      "score": 88,
      "weight": 0.25,
      "details": "Passed 22/25 REST practice tests"
    },
    "documentation_quality": {
      "score": 75,
      "weight": 0.10,
      "details": "Passed 3/4 documentation tests"
    },
    "versioning_strategy": {
      "score": 100,
      "weight": 0.10,
      "details": "API versioning found in URL paths with documentation"
    }
  },
  "base_score": 87.05,
  "penalties": {
    "time_penalty": 0,
    "iteration_penalty": 0,
    "error_penalty": 0
  },
  "final_score": 87,
  "passed": true
}
```

## What Makes a Good Submission

A high-quality OpenAPI specification should:

1. **Be Complete**: Cover all required resources and operations
2. **Follow Standards**: Adhere to OpenAPI 3.0 specification
3. **Use REST Principles**: Proper HTTP methods, status codes, URL structure
4. **Include Validation**: Define constraints on request data
5. **Handle Errors**: Document error responses comprehensively
6. **Be Secure**: Define authentication and authorization schemes
7. **Be Well-Documented**: Include clear descriptions and examples
8. **Support Evolution**: Include versioning strategy
9. **Be Practical**: Design for real-world use cases
10. **Be Developer-Friendly**: Easy to understand and use

## Common Pitfalls

- Missing required endpoints (cart, reviews, authentication)
- Not using proper HTTP methods (using GET for updates, POST for retrieval)
- Incorrect status codes (returning 200 for all responses)
- Missing error response definitions
- No pagination support for list endpoints
- Missing security definitions
- Incomplete schemas (missing required fields, no validation)
- No API versioning
- Poor or missing documentation
- Not following resource-based URL structure

## Example API Paths

```
Authentication:
POST   /v1/auth/register
POST   /v1/auth/login
POST   /v1/auth/logout
POST   /v1/auth/refresh

Products:
GET    /v1/products
GET    /v1/products/{id}
POST   /v1/products
PUT    /v1/products/{id}
DELETE /v1/products/{id}
GET    /v1/products/{id}/reviews

Orders:
GET    /v1/orders
GET    /v1/orders/{id}
POST   /v1/orders
PATCH  /v1/orders/{id}
DELETE /v1/orders/{id}
GET    /v1/orders/{id}/items

Cart:
GET    /v1/cart
POST   /v1/cart/items
PATCH  /v1/cart/items/{id}
DELETE /v1/cart/items/{id}
DELETE /v1/cart
```

## Skills Tested

- API design and architecture
- REST principles and best practices
- OpenAPI/Swagger specification knowledge
- HTTP protocol understanding
- Data modeling and schema design
- Authentication and authorization patterns
- Error handling and status codes
- API documentation
- Versioning strategies
- Developer experience considerations

## Automation Level

- **95% automated**: All scoring is based on objective criteria
- **5% subjective**: Some design decisions may have multiple valid approaches

## Time Estimate

- Beginner: 2-3 hours
- Intermediate: 1-2 hours
- Expert: 30-60 minutes

## Prerequisites

- Understanding of REST APIs
- Familiarity with OpenAPI/Swagger specification
- Knowledge of HTTP methods and status codes
- Understanding of JSON Schema
- Basic API security concepts

## Dependencies

The verification script requires:
- Python 3.6+
- pytest
- pyyaml
- openapi-spec-validator (optional, for strict validation)

These are automatically installed by the verification script.

## Notes

- This benchmark focuses on API design, not implementation
- The specification should be detailed enough for code generation
- Both YAML and JSON formats are acceptable
- Security details (like JWT secrets) should be described but not hardcoded
- Consider the developer experience when designing the API
- Think about API evolution and backwards compatibility

## Related Benchmarks

- **greenfield-001**: Tests implementation of an API from scratch
- **documentation-001**: Tests API documentation skills
- **maintenance-001**: Tests API evolution and versioning

## Version

Version: 1.0
Created: 2026-01-31
Last Updated: 2026-01-31
