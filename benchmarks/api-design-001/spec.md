# API Design - Specification

## Objective

Design a comprehensive OpenAPI 3.0 specification for an e-commerce order management REST API following industry best practices.

## Background

You are the API architect for a growing e-commerce platform. The company needs a well-designed REST API to support their web and mobile applications. The API must handle the complete order lifecycle, from product browsing to order fulfillment and tracking.

Your task is to create a detailed OpenAPI 3.0 specification that will serve as the contract between frontend and backend teams. This specification must be complete, unambiguous, and follow REST best practices.

## Requirements

### Functional Requirements

1. **Complete OpenAPI 3.0 Specification**
   - Valid OpenAPI 3.0.x format (YAML or JSON)
   - All required OpenAPI fields properly defined
   - Parseable by OpenAPI validation tools

2. **Resource Coverage**
   - Products (with variants, categories, inventory)
   - Customers (with authentication and addresses)
   - Orders (with items, status tracking)
   - Payments (with multiple payment methods)
   - Shipments (with tracking)
   - Shopping Cart
   - Reviews (with ratings)

3. **Complete CRUD Operations**
   - All necessary endpoints for each resource
   - Proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
   - Appropriate status codes for success and error cases

4. **Request/Response Schemas**
   - Complete JSON schema definitions for all request bodies
   - Complete JSON schema definitions for all responses
   - Reusable schema components
   - Proper data types and validations
   - Required vs. optional fields clearly marked

5. **Error Handling**
   - Standard error response schema
   - Error responses documented for each endpoint
   - Appropriate HTTP status codes (400, 401, 403, 404, 409, 422, 500)
   - Meaningful error messages and codes

6. **Authentication & Authorization**
   - Security scheme defined (JWT recommended)
   - Authentication requirements specified per endpoint
   - Role-based access control considerations

### Technical Constraints

- **Format**: OpenAPI 3.0.x specification (YAML preferred, JSON acceptable)
- **File Name**: `openapi.yaml` or `openapi.json`
- **Validation**: Must pass OpenAPI schema validation
- **Completeness**: Must include all sections (info, servers, paths, components, security)

### REST Best Practices

1. **URL Structure**
   - Use plural nouns for collections (e.g., `/products`, `/orders`)
   - Use resource hierarchy for relationships (e.g., `/orders/{orderId}/items`)
   - Include API versioning (e.g., `/v1/products`)
   - Use kebab-case or snake_case consistently

2. **HTTP Methods**
   - GET for retrieval (idempotent, cacheable)
   - POST for creation (non-idempotent)
   - PUT for full replacement (idempotent)
   - PATCH for partial updates (idempotent)
   - DELETE for removal (idempotent)

3. **HTTP Status Codes**
   - 200 OK: Successful GET, PUT, PATCH, DELETE
   - 201 Created: Successful POST (resource created)
   - 204 No Content: Successful DELETE with no response body
   - 400 Bad Request: Malformed request
   - 401 Unauthorized: Missing or invalid authentication
   - 403 Forbidden: Insufficient permissions
   - 404 Not Found: Resource does not exist
   - 409 Conflict: Resource conflict (e.g., duplicate)
   - 422 Unprocessable Entity: Validation errors
   - 500 Internal Server Error: Server error

4. **Query Parameters**
   - Pagination: `page`, `limit`, `offset`
   - Filtering: Field-specific filters
   - Sorting: `sort`, `order`
   - Searching: `q` or `search`
   - Field selection: `fields`

5. **Response Patterns**
   - Consistent response structure
   - Include metadata (pagination, timestamps)
   - Use envelopes for lists (array wrapped in object with metadata)
   - Include links/HATEOAS where appropriate

### Quality Requirements

1. **Schema Completeness (25% weight)**
   - All request/response schemas fully defined
   - Proper use of schema composition ($ref, allOf, oneOf)
   - Validation constraints (min, max, pattern, enum)
   - Clear descriptions for all fields
   - Examples provided

2. **REST Best Practices (25% weight)**
   - Correct HTTP methods for operations
   - Appropriate status codes
   - Proper URL structure and naming
   - Idempotent operations properly designed
   - Query parameters for filtering/pagination

3. **Required Endpoints (30% weight)**
   - All core resources have CRUD operations
   - Business logic endpoints (checkout, payment processing)
   - Search and filter capabilities
   - Authentication endpoints
   - Minimum 25 distinct endpoint paths

4. **Documentation Quality (10% weight)**
   - Clear endpoint descriptions
   - Parameter descriptions
   - Response descriptions
   - Example requests/responses
   - Security requirements documented

5. **Versioning Strategy (10% weight)**
   - API versioning approach defined
   - Version included in URL structure
   - Deprecation strategy described (in description or notes)

## Success Criteria

The API specification will be considered successful when:

1. **Valid OpenAPI Format**: Passes OpenAPI 3.0 schema validation
2. **Complete Coverage**: All required resources and operations are defined
3. **Best Practices**: Follows REST conventions and HTTP standards
4. **Production Ready**: Includes error handling, authentication, and validation
5. **Well Documented**: Clear descriptions and examples throughout

## Deliverables

1. **OpenAPI Specification File**: `openapi.yaml` or `openapi.json`
   - Place in the root of the benchmark directory
   - Must be valid OpenAPI 3.0.x format
   - Should be complete and ready for code generation

2. **API Documentation** (Optional but recommended): `API.md`
   - High-level API overview
   - Authentication guide
   - Common use cases and workflows
   - Any design decisions or trade-offs

## Evaluation

Your submission will be scored on:

- **Required Endpoints**: 30% - Coverage of all necessary operations
- **Schema Completeness**: 25% - Request/response schemas fully defined
- **REST Best Practices**: 25% - Proper HTTP methods, status codes, URL structure
- **Documentation Quality**: 10% - Descriptions, examples, clarity
- **Versioning Strategy**: 10% - Clear versioning approach

See `verification/verify.sh` for automated scoring implementation.

## Example Resources to Consider

### Products
```
GET    /v1/products                    - List products (with filtering, pagination)
GET    /v1/products/{productId}        - Get product details
POST   /v1/products                    - Create product (admin)
PUT    /v1/products/{productId}        - Update product (admin)
DELETE /v1/products/{productId}        - Delete product (admin)
GET    /v1/products/{productId}/reviews - Get product reviews
```

### Orders
```
GET    /v1/orders                      - List customer orders
GET    /v1/orders/{orderId}            - Get order details
POST   /v1/orders                      - Create order (checkout)
PATCH  /v1/orders/{orderId}            - Update order status
DELETE /v1/orders/{orderId}            - Cancel order
GET    /v1/orders/{orderId}/items      - Get order items
```

### Cart
```
GET    /v1/cart                        - Get current cart
POST   /v1/cart/items                  - Add item to cart
PATCH  /v1/cart/items/{itemId}         - Update cart item
DELETE /v1/cart/items/{itemId}         - Remove item from cart
DELETE /v1/cart                        - Clear cart
```

## Notes

- Focus on creating a realistic, production-ready API design
- Consider the developer experience when designing the API
- Think about API evolution and backwards compatibility
- Error responses should be helpful for debugging
- Include rate limiting and security considerations
- The specification should be detailed enough for automatic code generation
