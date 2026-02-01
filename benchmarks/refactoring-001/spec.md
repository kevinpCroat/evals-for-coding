# Code Refactoring - Specification

## Objective

Refactor a working but messy order processing system to improve code structure, reduce complexity, and eliminate duplication while maintaining 100% behavioral compatibility.

## Background

You are provided with a functional order processing system (`starter-code/order_processor.py`) that works correctly and has comprehensive passing tests. However, the code suffers from numerous quality issues:

- **God Class**: `OrderProcessingSystemManager` does everything
- **Long Methods**: Several methods exceed 50-100 lines
- **Code Duplication**: Similar logic repeated in multiple places
- **Poor Naming**: Unclear variable names and inconsistent conventions
- **Feature Envy**: Methods accessing data from other objects excessively
- **Lack of Separation of Concerns**: Mixed responsibilities in single classes

The system includes:
- Product inventory management
- Order processing with discounts and shipping
- Tax calculations
- Customer management with VIP status
- Order cancellation with inventory restoration
- Revenue and inventory reporting

## Requirements

### Functional Requirements

1. **Preserve All Behavior**: Every test in the test suite must continue to pass
2. **Reduce Complexity**: Lower cyclomatic complexity of methods
3. **Eliminate Duplication**: Extract and reuse duplicated code
4. **Improve Structure**: Better class design and separation of concerns
5. **Better Naming**: Use clear, descriptive names for classes, methods, and variables

### Refactoring Opportunities

The code contains these intentional problems to address:

1. **Extract Classes**: Break down the god class into focused classes
   - Separate inventory management
   - Separate order processing
   - Separate customer management
   - Separate pricing/discount calculations

2. **Extract Methods**: Break long methods into smaller, focused ones
   - `processOrderAndCalculateEverything` is >100 lines
   - Extract validation logic
   - Extract calculation logic
   - Extract data transformation logic

3. **Eliminate Duplication**:
   - Order lookup logic repeated 3+ times
   - Customer lookup logic repeated 3+ times
   - Product lookup logic repeated 3+ times
   - Validation patterns duplicated
   - Iteration and formatting patterns duplicated

4. **Improve Naming**:
   - Rename god class to something more specific
   - Remove unclear variable names (p, n, pr, s)
   - Use consistent naming conventions

5. **Simplify Complex Logic**:
   - Reduce nested conditionals
   - Extract complex conditions into named methods
   - Reduce method complexity

### Technical Constraints

- **DO NOT MODIFY THE TESTS**: The test file must remain unchanged
- Use Python 3.7+ features as appropriate
- Maintain the same public API (tests depend on it)
- Keep the same file structure (single module with tests)
- Code must pass Python linting (flake8, pylint)

### Quality Requirements

- All 60+ tests must pass after refactoring
- Code should follow Python best practices (PEP 8)
- Classes should have single responsibilities
- Methods should be focused and concise (<30 lines ideally)
- No code duplication (DRY principle)
- Clear, self-documenting code

## Success Criteria

The refactoring will be considered successful when:

1. **All Tests Pass** (CRITICAL): 100% of tests must pass - this is non-negotiable
2. **Complexity Reduced**: Average cyclomatic complexity per method decreases significantly
3. **Duplication Eliminated**: Measurable reduction in duplicated code blocks
4. **Better Structure**: Clear separation of concerns with focused classes

## Deliverables

1. Refactored `order_processor.py` with improved structure
2. All original tests passing without modification
3. Measurably lower complexity metrics
4. Measurably less code duplication

## Evaluation

Your submission will be scored on:

- **Tests Pass**: 50% - All tests must pass (if any fail, automatic 0)
- **Complexity Reduction**: 30% - Reduction in cyclomatic complexity
- **Duplication Reduction**: 20% - Reduction in duplicated code

See `verification/verify.sh` for automated scoring implementation.

## Measurement Approach

**Before refactoring metrics** (baseline):
- Cyclomatic complexity: Measured with `radon cc`
- Code duplication: Measured with `radon raw` and custom duplication detector
- Test results: All 60+ tests passing

**After refactoring metrics**:
- Same measurements compared against baseline
- Score based on percentage improvement
- CRITICAL: If any test fails, score is 0 regardless of other improvements

The key principle: **Behavior preservation is mandatory; structure improvement is the goal.**
