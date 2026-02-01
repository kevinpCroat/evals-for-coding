# Test-Driven Quality Assessment - Specification

## Objective

Write comprehensive tests for an existing shopping cart module to achieve high coverage and demonstrate test quality through mutation testing.

## Background

You are provided with a `shopping_cart.py` module that implements a realistic e-commerce shopping cart system. The module has NO existing tests. Your task is to write a complete test suite that thoroughly validates the module's behavior, handles edge cases, and can detect real bugs through mutation testing.

The module includes:
- `Item` class: Represents products with ID, name, price, and quantity
- `ShoppingCart` class: Manages cart operations, discounts, tax calculations, and loyalty points
- Custom exceptions for validation errors
- Edge cases around pricing, quantities, discounts, and tax calculations

## Requirements

### Functional Requirements

1. Create a comprehensive test suite in `test_shopping_cart.py`
2. Test all public methods and classes in the module
3. Cover normal cases, edge cases, and error conditions
4. Use proper test organization (test classes, descriptive names, etc.)
5. Include assertions that validate behavior, not just execution

### Testing Coverage Requirements

You must test:
- Item class initialization with valid and invalid inputs
- Adding, removing, and updating items in the cart
- Quantity calculations (total items, unique items)
- Price calculations (subtotal, discounts, tax, final total)
- Edge cases: empty cart, negative values, boundary conditions
- Discount logic including multiple discounts
- Tax calculation accuracy
- Loyalty points functionality
- Error handling for all custom exceptions
- Type validation for inputs

### Technical Constraints

- Use `pytest` as the testing framework
- Follow pytest naming conventions (test files start with `test_`)
- Use descriptive test function names that explain what is being tested
- Each test should test one specific behavior
- Tests must be independent (no shared state between tests)
- Use appropriate pytest features (fixtures, parametrize, etc.) where beneficial

### Quality Requirements

- Tests must be executable and pass
- Code must follow Python best practices
- No test duplication - use parametrize for similar test cases
- Assertions must check actual behavior, not just execution
- Tests must be maintainable and readable

## Success Criteria

The implementation will be considered successful when:

1. **Coverage**: Achieve >90% code coverage on the shopping_cart.py module
2. **Mutation Score**: Kill >80% of mutations (showing tests detect actual bugs)
3. **Test Independence**: All tests pass when run individually and in any order
4. **Assertion Quality**: Tests have meaningful assertions that would catch bugs

## Deliverables

1. `test_shopping_cart.py` - Complete test suite for the shopping cart module
2. All tests must pass when run with `pytest test_shopping_cart.py`
3. Tests should work with `pytest-cov` for coverage measurement
4. Tests should work with `mutmut` for mutation testing

## Evaluation

Your submission will be scored on:

- **Coverage Increase**: 30% - Percentage of code coverage achieved
- **Mutation Score**: 40% - Percentage of mutants killed by your tests
- **Test Independence**: 15% - Tests pass in isolation and don't depend on execution order
- **Assertion Quality**: 15% - Tests have meaningful assertions that validate behavior

See verification/verify.sh for automated scoring implementation.

The mutation score is the most important metric - it ensures your tests actually catch bugs, not just execute code.
