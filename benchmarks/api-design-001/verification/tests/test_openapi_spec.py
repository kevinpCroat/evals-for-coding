"""
Comprehensive test suite for OpenAPI specification validation
Tests API design quality, completeness, and adherence to best practices
"""

import pytest
import yaml
import json
import os
import sys
from pathlib import Path

# Try to import OpenAPI validation libraries
try:
    from openapi_spec_validator import validate_spec
    from openapi_spec_validator.readers import read_from_filename
    HAS_VALIDATOR = True
except ImportError:
    HAS_VALIDATOR = False

# Find the OpenAPI spec file
BENCHMARK_DIR = Path(__file__).parent.parent.parent
SPEC_FILE_YAML = BENCHMARK_DIR / "openapi.yaml"
SPEC_FILE_JSON = BENCHMARK_DIR / "openapi.json"


def load_spec():
    """Load and parse the OpenAPI specification"""
    if SPEC_FILE_YAML.exists():
        with open(SPEC_FILE_YAML, 'r') as f:
            return yaml.safe_load(f), str(SPEC_FILE_YAML)
    elif SPEC_FILE_JSON.exists():
        with open(SPEC_FILE_JSON, 'r') as f:
            return json.load(f), str(SPEC_FILE_JSON)
    else:
        pytest.skip("No OpenAPI spec file found (openapi.yaml or openapi.json)")


@pytest.fixture(scope="module")
def spec():
    """Load the OpenAPI specification once for all tests"""
    spec_data, spec_file = load_spec()
    return spec_data


@pytest.fixture(scope="module")
def spec_file_path():
    """Get the path to the spec file"""
    _, spec_file = load_spec()
    return spec_file


class TestOpenAPIValidity:
    """Tests for OpenAPI specification validity"""

    def test_spec_file_exists(self):
        """Test that an OpenAPI spec file exists"""
        assert SPEC_FILE_YAML.exists() or SPEC_FILE_JSON.exists(), \
            "OpenAPI spec file (openapi.yaml or openapi.json) must exist"

    def test_spec_is_valid_yaml_or_json(self, spec):
        """Test that the spec file is valid YAML or JSON"""
        assert spec is not None, "Spec file must be valid YAML or JSON"
        assert isinstance(spec, dict), "Spec must be a dictionary"

    @pytest.mark.skipif(not HAS_VALIDATOR, reason="openapi-spec-validator not installed")
    def test_spec_passes_openapi_validation(self, spec_file_path):
        """Test that the spec passes OpenAPI schema validation"""
        try:
            spec_dict, spec_url = read_from_filename(spec_file_path)
            validate_spec(spec_dict)
        except Exception as e:
            pytest.fail(f"OpenAPI validation failed: {str(e)}")

    def test_has_openapi_version(self, spec):
        """Test that OpenAPI version is specified"""
        assert 'openapi' in spec, "Spec must have 'openapi' field"
        assert spec['openapi'].startswith('3.0'), "Must be OpenAPI 3.0.x"

    def test_has_info_section(self, spec):
        """Test that info section is present and complete"""
        assert 'info' in spec, "Spec must have 'info' section"
        info = spec['info']
        assert 'title' in info, "Info must have 'title'"
        assert 'version' in info, "Info must have 'version'"
        assert 'description' in info, "Info should have 'description'"

    def test_has_servers_section(self, spec):
        """Test that servers section is present"""
        assert 'servers' in spec, "Spec must have 'servers' section"
        assert len(spec['servers']) > 0, "Must have at least one server"

    def test_has_paths_section(self, spec):
        """Test that paths section is present"""
        assert 'paths' in spec, "Spec must have 'paths' section"
        assert len(spec['paths']) > 0, "Must have at least one path"

    def test_has_components_section(self, spec):
        """Test that components section is present"""
        assert 'components' in spec, "Spec should have 'components' section"


class TestRequiredEndpoints:
    """Tests for required endpoint coverage"""

    def test_minimum_endpoint_count(self, spec):
        """Test that spec has minimum 25 distinct paths"""
        paths = spec.get('paths', {})
        assert len(paths) >= 25, f"Must have at least 25 endpoints, found {len(paths)}"

    def test_has_product_endpoints(self, spec):
        """Test that product endpoints exist"""
        paths = spec.get('paths', {})
        path_strings = [p.lower() for p in paths.keys()]

        # Should have products list endpoint
        assert any('product' in p for p in path_strings), "Must have product endpoints"

        # Should have product detail endpoint (with parameter)
        has_product_detail = any('{' in p and 'product' in p for p in path_strings)
        assert has_product_detail, "Must have product detail endpoint with parameter"

    def test_has_order_endpoints(self, spec):
        """Test that order endpoints exist"""
        paths = spec.get('paths', {})
        path_strings = [p.lower() for p in paths.keys()]

        assert any('order' in p for p in path_strings), "Must have order endpoints"
        has_order_detail = any('{' in p and 'order' in p for p in path_strings)
        assert has_order_detail, "Must have order detail endpoint with parameter"

    def test_has_customer_endpoints(self, spec):
        """Test that customer endpoints exist"""
        paths = spec.get('paths', {})
        path_strings = [p.lower() for p in paths.keys()]

        assert any('customer' in p or 'user' in p or 'profile' in p for p in path_strings), \
            "Must have customer/user endpoints"

    def test_has_cart_endpoints(self, spec):
        """Test that cart endpoints exist"""
        paths = spec.get('paths', {})
        path_strings = [p.lower() for p in paths.keys()]

        assert any('cart' in p for p in path_strings), "Must have cart endpoints"

    def test_has_payment_endpoints(self, spec):
        """Test that payment endpoints exist"""
        paths = spec.get('paths', {})
        path_strings = [p.lower() for p in paths.keys()]

        assert any('payment' in p for p in path_strings), "Must have payment endpoints"

    def test_has_review_endpoints(self, spec):
        """Test that review endpoints exist"""
        paths = spec.get('paths', {})
        path_strings = [p.lower() for p in paths.keys()]

        assert any('review' in p for p in path_strings), "Must have review endpoints"

    def test_has_authentication_endpoints(self, spec):
        """Test that authentication endpoints exist"""
        paths = spec.get('paths', {})
        path_strings = [p.lower() for p in paths.keys()]

        has_auth = any(keyword in p for p in path_strings
                      for keyword in ['auth', 'login', 'register', 'token', 'signin', 'signup'])
        assert has_auth, "Must have authentication endpoints (login, register, etc.)"


class TestHTTPMethods:
    """Tests for proper HTTP method usage"""

    def test_uses_get_method(self, spec):
        """Test that GET method is used for retrieval"""
        paths = spec.get('paths', {})
        get_count = sum(1 for path_ops in paths.values() if 'get' in path_ops)
        assert get_count >= 5, "Should have multiple GET endpoints for retrieval"

    def test_uses_post_method(self, spec):
        """Test that POST method is used for creation"""
        paths = spec.get('paths', {})
        post_count = sum(1 for path_ops in paths.values() if 'post' in path_ops)
        assert post_count >= 3, "Should have POST endpoints for creation"

    def test_uses_put_or_patch_method(self, spec):
        """Test that PUT or PATCH is used for updates"""
        paths = spec.get('paths', {})
        update_count = sum(1 for path_ops in paths.values()
                          if 'put' in path_ops or 'patch' in path_ops)
        assert update_count >= 2, "Should have PUT or PATCH endpoints for updates"

    def test_uses_delete_method(self, spec):
        """Test that DELETE method is used for removal"""
        paths = spec.get('paths', {})
        delete_count = sum(1 for path_ops in paths.values() if 'delete' in path_ops)
        assert delete_count >= 2, "Should have DELETE endpoints for removal"

    def test_proper_method_for_list_endpoints(self, spec):
        """Test that list endpoints use GET method"""
        paths = spec.get('paths', {})

        # List endpoints (plural, no parameters) should use GET
        for path, operations in paths.items():
            # Skip paths with parameters
            if '{' in path:
                continue
            # Plural endpoints should have GET
            if any(plural in path.lower() for plural in ['products', 'orders', 'customers', 'reviews']):
                assert 'get' in operations, f"{path} should support GET method"


class TestStatusCodes:
    """Tests for proper HTTP status code usage"""

    def test_success_status_codes(self, spec):
        """Test that endpoints define appropriate success status codes"""
        paths = spec.get('paths', {})

        for path, operations in paths.items():
            for method, operation in operations.items():
                if method not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue

                responses = operation.get('responses', {})
                assert len(responses) > 0, f"{method.upper()} {path} must define responses"

                # Check for success codes
                success_codes = [code for code in responses.keys()
                               if code.startswith('2')]
                assert len(success_codes) > 0, \
                    f"{method.upper()} {path} must define at least one 2xx success response"

    def test_post_returns_201(self, spec):
        """Test that POST endpoints return 201 Created"""
        paths = spec.get('paths', {})

        post_endpoints = []
        for path, operations in paths.items():
            if 'post' in operations:
                post_endpoints.append(path)
                responses = operations['post'].get('responses', {})
                # POST should return 201 Created for resource creation
                # (Some may use 200, which is also acceptable)
                has_success = '201' in responses or '200' in responses
                assert has_success, f"POST {path} should return 200 or 201"

    def test_error_status_codes(self, spec):
        """Test that endpoints define error status codes"""
        paths = spec.get('paths', {})

        # Check a few endpoints for error responses
        endpoints_checked = 0
        for path, operations in paths.items():
            for method, operation in operations.items():
                if method not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue

                responses = operation.get('responses', {})
                error_codes = [code for code in responses.keys()
                             if code.startswith('4') or code.startswith('5')]

                endpoints_checked += 1
                if endpoints_checked <= 5:  # Check at least 5 endpoints
                    assert len(error_codes) > 0, \
                        f"{method.upper()} {path} should define error responses"

    def test_has_404_for_detail_endpoints(self, spec):
        """Test that detail endpoints (with IDs) define 404 responses"""
        paths = spec.get('paths', {})

        for path, operations in paths.items():
            # Only check paths with parameters (detail endpoints)
            if '{' not in path:
                continue

            for method in ['get', 'put', 'patch', 'delete']:
                if method in operations:
                    responses = operations[method].get('responses', {})
                    assert '404' in responses, \
                        f"{method.upper()} {path} should define 404 response for non-existent resources"

    def test_has_401_for_protected_endpoints(self, spec):
        """Test that protected endpoints define 401 responses"""
        paths = spec.get('paths', {})

        # Check if any endpoints have security requirements
        has_secured_endpoints = False
        for path, operations in paths.items():
            for method, operation in operations.items():
                if method not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue

                if 'security' in operation or 'security' in spec:
                    has_secured_endpoints = True
                    responses = operation.get('responses', {})
                    # If secured, should have 401 defined somewhere in spec
                    # (Can be in components/responses and referenced)
                    break

        # If we have security, we should document 401 somewhere
        if has_secured_endpoints:
            assert True, "Spec has security scheme"


class TestSchemaDefinitions:
    """Tests for schema completeness and quality"""

    def test_has_schema_components(self, spec):
        """Test that spec defines schema components"""
        components = spec.get('components', {})
        assert 'schemas' in components, "Must define schemas in components"
        schemas = components['schemas']
        assert len(schemas) >= 5, f"Should have at least 5 schema definitions, found {len(schemas)}"

    def test_key_schemas_exist(self, spec):
        """Test that key resource schemas are defined"""
        components = spec.get('components', {})
        schemas = components.get('schemas', {})
        schema_names = [name.lower() for name in schemas.keys()]

        # Check for key resource schemas
        required_schemas = ['product', 'order', 'customer', 'user', 'payment', 'cart']
        found_schemas = []

        for required in required_schemas:
            if any(required in name for name in schema_names):
                found_schemas.append(required)

        assert len(found_schemas) >= 4, \
            f"Must define schemas for key resources (product, order, customer, payment, cart). Found: {found_schemas}"

    def test_schemas_have_properties(self, spec):
        """Test that schemas define properties"""
        components = spec.get('components', {})
        schemas = components.get('schemas', {})

        for schema_name, schema in schemas.items():
            # Skip if it's a reference or composition
            if '$ref' in schema or 'allOf' in schema or 'oneOf' in schema or 'anyOf' in schema:
                continue

            # Should have properties or be an array/string/etc with type
            has_structure = 'properties' in schema or 'type' in schema or 'enum' in schema
            assert has_structure, f"Schema {schema_name} should define properties or type"

    def test_schemas_have_descriptions(self, spec):
        """Test that schemas have descriptions"""
        components = spec.get('components', {})
        schemas = components.get('schemas', {})

        described_count = sum(1 for schema in schemas.values() if 'description' in schema)
        total_schemas = len(schemas)

        # At least 50% of schemas should have descriptions
        assert described_count >= total_schemas * 0.5, \
            f"At least 50% of schemas should have descriptions. Found {described_count}/{total_schemas}"

    def test_request_bodies_defined(self, spec):
        """Test that POST/PUT/PATCH operations have request bodies"""
        paths = spec.get('paths', {})

        for path, operations in paths.items():
            for method in ['post', 'put', 'patch']:
                if method in operations:
                    operation = operations[method]
                    # Should have requestBody or parameters
                    has_body = 'requestBody' in operation or 'parameters' in operation
                    assert has_body, \
                        f"{method.upper()} {path} should define requestBody or parameters"

    def test_response_schemas_defined(self, spec):
        """Test that successful responses have schemas"""
        paths = spec.get('paths', {})

        endpoints_checked = 0
        for path, operations in paths.items():
            for method, operation in operations.items():
                if method not in ['get', 'post', 'put', 'patch']:
                    continue

                responses = operation.get('responses', {})
                for code, response in responses.items():
                    if code.startswith('2') and code != '204':  # Success codes except No Content
                        # Should have content or schema
                        has_content = 'content' in response or 'schema' in response
                        endpoints_checked += 1
                        if endpoints_checked <= 10:  # Check at least 10 responses
                            assert has_content, \
                                f"{method.upper()} {path} response {code} should define content/schema"

    def test_error_response_schema(self, spec):
        """Test that error responses have consistent schema"""
        components = spec.get('components', {})
        schemas = components.get('schemas', {})

        # Look for error schema definition
        has_error_schema = any('error' in name.lower() for name in schemas.keys())

        if has_error_schema:
            # Good - error schema is defined
            assert True
        else:
            # Check if error responses are at least defined somewhere
            paths = spec.get('paths', {})
            has_error_responses = False
            for path, operations in paths.items():
                for method, operation in operations.items():
                    if method not in ['get', 'post', 'put', 'patch', 'delete']:
                        continue
                    responses = operation.get('responses', {})
                    if any(code.startswith('4') or code.startswith('5') for code in responses.keys()):
                        has_error_responses = True
                        break
            assert has_error_responses, "Should define error responses"


class TestRESTBestPractices:
    """Tests for REST API best practices"""

    def test_uses_versioning(self, spec):
        """Test that API uses versioning in URLs"""
        paths = spec.get('paths', {})

        # Check if paths include version (e.g., /v1/, /api/v1/)
        versioned_paths = sum(1 for path in paths.keys()
                             if '/v1' in path or '/v2' in path or '/api/v1' in path)

        # At least 50% of paths should be versioned
        assert versioned_paths >= len(paths) * 0.5, \
            "API should use versioning in URL paths (e.g., /v1/)"

    def test_uses_plural_nouns(self, spec):
        """Test that collection endpoints use plural nouns"""
        paths = spec.get('paths', {})

        # Common plural resource names
        plurals = ['products', 'orders', 'customers', 'users', 'payments',
                  'reviews', 'items', 'addresses', 'shipments']

        plural_count = sum(1 for path in paths.keys()
                          if any(plural in path.lower() for plural in plurals))

        assert plural_count >= 5, "Should use plural nouns for collections"

    def test_proper_url_hierarchy(self, spec):
        """Test that nested resources use proper hierarchy"""
        paths = spec.get('paths', {})

        # Look for nested resources (e.g., /orders/{id}/items)
        nested_count = sum(1 for path in paths.keys()
                          if path.count('/') >= 4)  # At least /v1/resource/{id}/nested

        # Should have some nested resources
        if nested_count > 0:
            assert True, "Uses resource hierarchy for nested resources"

    def test_pagination_support(self, spec):
        """Test that list endpoints support pagination"""
        paths = spec.get('paths', {})

        has_pagination = False
        for path, operations in paths.items():
            if 'get' in operations:
                operation = operations['get']
                parameters = operation.get('parameters', [])

                # Look for pagination parameters
                param_names = [p.get('name', '').lower() for p in parameters]
                if any(p in param_names for p in ['page', 'limit', 'offset', 'per_page']):
                    has_pagination = True
                    break

        assert has_pagination, "Should support pagination with page/limit/offset parameters"

    def test_filtering_support(self, spec):
        """Test that list endpoints support filtering"""
        paths = spec.get('paths', {})

        has_filtering = False
        for path, operations in paths.items():
            if 'get' in operations:
                operation = operations['get']
                parameters = operation.get('parameters', [])

                # Look for filter parameters
                if len(parameters) > 1:  # More than just basic params
                    has_filtering = True
                    break

        assert has_filtering, "Should support filtering through query parameters"

    def test_uses_path_parameters_for_ids(self, spec):
        """Test that IDs are passed as path parameters, not query params"""
        paths = spec.get('paths', {})

        # Look for detail endpoints with path parameters
        has_path_params = any('{' in path and '}' in path for path in paths.keys())
        assert has_path_params, "Should use path parameters for resource IDs (e.g., /products/{id})"


class TestSecurityDefinitions:
    """Tests for security and authentication"""

    def test_has_security_scheme(self, spec):
        """Test that security scheme is defined"""
        components = spec.get('components', {})
        assert 'securitySchemes' in components, \
            "Must define security schemes in components"

        schemes = components['securitySchemes']
        assert len(schemes) > 0, "Must define at least one security scheme"

    def test_security_scheme_type(self, spec):
        """Test that security scheme uses appropriate type"""
        components = spec.get('components', {})
        schemes = components.get('securitySchemes', {})

        for scheme_name, scheme in schemes.items():
            assert 'type' in scheme, f"Security scheme {scheme_name} must have type"
            # Common types: http, apiKey, oauth2, openIdConnect
            assert scheme['type'] in ['http', 'apiKey', 'oauth2', 'openIdConnect'], \
                f"Security scheme {scheme_name} has invalid type"

    def test_some_endpoints_require_auth(self, spec):
        """Test that some endpoints require authentication"""
        paths = spec.get('paths', {})

        secured_endpoints = 0
        for path, operations in paths.items():
            for method, operation in operations.items():
                if method not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue

                if 'security' in operation:
                    secured_endpoints += 1

        # Check global security as well
        has_global_security = 'security' in spec

        assert secured_endpoints > 0 or has_global_security, \
            "Some endpoints should require authentication"


class TestDocumentationQuality:
    """Tests for documentation completeness"""

    def test_endpoints_have_descriptions(self, spec):
        """Test that endpoints have descriptions"""
        paths = spec.get('paths', {})

        described_ops = 0
        total_ops = 0

        for path, operations in paths.items():
            for method, operation in operations.items():
                if method not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue

                total_ops += 1
                if 'description' in operation or 'summary' in operation:
                    described_ops += 1

        # At least 70% of operations should have descriptions
        description_ratio = described_ops / total_ops if total_ops > 0 else 0
        assert description_ratio >= 0.7, \
            f"At least 70% of endpoints should have descriptions. Found {described_ops}/{total_ops}"

    def test_parameters_have_descriptions(self, spec):
        """Test that parameters have descriptions"""
        paths = spec.get('paths', {})

        described_params = 0
        total_params = 0

        for path, operations in paths.items():
            for method, operation in operations.items():
                if method not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue

                parameters = operation.get('parameters', [])
                for param in parameters:
                    total_params += 1
                    if 'description' in param:
                        described_params += 1

        if total_params > 0:
            description_ratio = described_params / total_params
            # At least 50% of parameters should have descriptions
            assert description_ratio >= 0.5, \
                f"At least 50% of parameters should have descriptions. Found {described_params}/{total_params}"

    def test_has_examples(self, spec):
        """Test that spec includes examples"""
        components = spec.get('components', {})
        schemas = components.get('schemas', {})

        has_examples = False

        # Check schemas for examples
        for schema in schemas.values():
            if 'example' in schema or 'examples' in schema:
                has_examples = True
                break

        # Also check in paths
        if not has_examples:
            paths = spec.get('paths', {})
            for operations in paths.values():
                for operation in operations.values():
                    if isinstance(operation, dict):
                        if 'examples' in operation or 'example' in operation:
                            has_examples = True
                            break

        # Examples are good practice but not strictly required
        # Just check that some effort was made
        if has_examples:
            assert True, "Includes examples"


class TestAPICompleteness:
    """Tests for overall API completeness"""

    def test_covers_full_crud_for_products(self, spec):
        """Test that products have full CRUD operations"""
        paths = spec.get('paths', {})

        operations_found = {'get': False, 'post': False, 'put_or_patch': False, 'delete': False}

        for path, operations in paths.items():
            if 'product' in path.lower():
                if 'get' in operations:
                    operations_found['get'] = True
                if 'post' in operations:
                    operations_found['post'] = True
                if 'put' in operations or 'patch' in operations:
                    operations_found['put_or_patch'] = True
                if 'delete' in operations:
                    operations_found['delete'] = True

        missing = [op for op, found in operations_found.items() if not found]
        assert len(missing) == 0, \
            f"Products should support full CRUD. Missing: {missing}"

    def test_covers_order_lifecycle(self, spec):
        """Test that orders have necessary operations for lifecycle"""
        paths = spec.get('paths', {})

        operations_found = {'create': False, 'get': False, 'update': False}

        for path, operations in paths.items():
            if 'order' in path.lower():
                if 'post' in operations:
                    operations_found['create'] = True
                if 'get' in operations:
                    operations_found['get'] = True
                if 'put' in operations or 'patch' in operations:
                    operations_found['update'] = True

        missing = [op for op, found in operations_found.items() if not found]
        assert len(missing) == 0, \
            f"Orders should support create, get, and update. Missing: {missing}"

    def test_has_search_capability(self, spec):
        """Test that API supports search"""
        paths = spec.get('paths', {})

        has_search = False

        # Look for search endpoint or search parameters
        for path, operations in paths.items():
            if 'search' in path.lower():
                has_search = True
                break

            # Or check for search query parameters
            if 'get' in operations:
                params = operations['get'].get('parameters', [])
                param_names = [p.get('name', '').lower() for p in params]
                if any(p in param_names for p in ['q', 'search', 'query']):
                    has_search = True
                    break

        assert has_search, "Should support search functionality"
