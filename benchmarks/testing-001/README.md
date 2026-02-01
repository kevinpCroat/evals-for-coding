# Testing-001: Test-Driven Quality Assessment

## Overview

This benchmark evaluates an AI's ability to write high-quality, comprehensive tests for existing code. The AI must write a complete test suite from scratch for a shopping cart module, achieving both high coverage and high mutation scores to demonstrate that the tests actually catch bugs.

## Task Description

The AI is given a `shopping_cart.py` module (approximately 180 lines) that implements a realistic e-commerce shopping cart with:
- Item management (add, remove, update quantities)
- Price calculations with decimal precision
- Discount application (including multiple discounts)
- Tax calculation
- Loyalty points functionality
- Custom exception handling
- Various edge cases and validation logic

**The module has NO existing tests.** The AI must create a comprehensive test suite that:
1. Achieves high code coverage (>90%)
2. Demonstrates test quality through mutation testing (>80% mutation score)
3. Contains independent tests that pass in any order
4. Has meaningful assertions that validate behavior

## Why This Benchmark Matters

Testing is a critical software engineering skill, but writing *good* tests is more challenging than achieving coverage:
- **Coverage is necessary but not sufficient** - 100% coverage doesn't mean tests catch bugs
- **Mutation testing reveals quality** - Only tests that fail when bugs are introduced are truly valuable
- **Edge cases matter** - Good tests handle boundaries, null values, and error conditions
- **Test independence is essential** - Tests must not rely on execution order or shared state

This benchmark uses mutation testing as the key quality metric, ensuring the AI writes tests that actually detect bugs rather than just executing code.

## Directory Structure

```
testing-001/
├── README.md                 # This file
├── spec.md                   # Task specification
├── prompts.txt              # Instructions for AI
├── shopping_cart.py         # Module to test (DO NOT MODIFY)
└── verification/
    └── verify.sh            # Automated verification and scoring
```

## Evaluation Criteria

The benchmark scores submissions on four weighted components:

1. **Coverage (30%)**: Percentage of code coverage achieved
   - Measured using pytest-cov
   - Target: >90% coverage

2. **Mutation Score (40%)**: Percentage of mutants killed
   - Measured using mutmut
   - Target: >80% mutation score
   - This is the most important metric

3. **Test Independence (15%)**: Tests pass in random order
   - Runs tests in random order 3 times
   - All runs must pass

4. **Assertion Quality (15%)**: Meaningful assertions per test
   - Optimal: 1-3 assertions per test on average
   - Too few suggests weak testing
   - Too many suggests unfocused tests

**Passing Score**: 70/100

## Running the Benchmark

### For AI Agents

1. Read `spec.md` and `prompts.txt`
2. Analyze `shopping_cart.py` to understand what needs testing
3. Create `test_shopping_cart.py` with comprehensive tests
4. Run `./verification/verify.sh` to check your score

### For Evaluation

```bash
cd benchmarks/testing-001
./verification/verify.sh
```

The script outputs JSON with detailed scoring:

```json
{
  "benchmark": "testing-001",
  "timestamp": "2026-01-31T12:00:00Z",
  "components": {
    "coverage": {"score": 95, "weight": 0.30, "details": "Coverage: 95.5%"},
    "mutation_score": {"score": 85, "weight": 0.40, "details": "Killed: 85/100 mutants"},
    "independence": {"score": 100, "weight": 0.15, "details": "Passed 3/3 random runs"},
    "assertion_quality": {"score": 100, "weight": 0.15, "details": "Avg: 2.1/test"}
  },
  "base_score": 90.25,
  "final_score": 90,
  "passed": true
}
```

## Key Challenges

This benchmark tests several important capabilities:

1. **Code Understanding**: AI must read and comprehend existing code
2. **Edge Case Identification**: Must identify boundaries, error conditions, and special cases
3. **Test Organization**: Should use fixtures, parametrize, and proper structure
4. **Error Testing**: Must test exception handling correctly
5. **Decimal Precision**: Must handle monetary calculations precisely
6. **Mutation Resistance**: Tests must be specific enough to catch introduced bugs

## Example Test Cases Needed

A strong test suite should include:

- **Item Class**:
  - Valid initialization
  - Invalid inputs (empty ID/name, negative price, zero quantity)
  - Total calculation

- **ShoppingCart Class**:
  - Adding items (new and duplicate)
  - Removing items (existing and non-existent)
  - Updating quantities
  - Empty cart operations
  - Count calculations

- **Calculations**:
  - Subtotal with single/multiple items
  - Single and multiple discounts
  - Tax calculation
  - Final total accuracy
  - Discount capping at subtotal

- **Edge Cases**:
  - Empty cart operations
  - Boundary values (0%, 100% discount)
  - Decimal precision
  - Type validation

## Dependencies

The verification script automatically installs:
- `pytest` - Testing framework
- `pytest-cov` - Coverage measurement
- `pytest-random-order` - Test independence verification
- `mutmut` - Mutation testing

## Expected Time

- Reading and understanding: 5-10 minutes
- Writing comprehensive tests: 20-40 minutes
- Iteration based on verification: 10-20 minutes

Total: 35-70 minutes for a complete solution

## Success Indicators

A successful solution will:
- Have 30-50 well-organized test functions
- Use pytest features appropriately (fixtures, parametrize)
- Test both happy paths and error conditions
- Achieve >90% coverage
- Kill >80% of mutants (showing tests catch bugs)
- Pass all independence checks

## Common Pitfalls

1. **Coverage without quality**: High coverage but low mutation score
2. **Missing edge cases**: Not testing boundaries, empty states, or errors
3. **Weak assertions**: Using `assert True` or not checking actual values
4. **Test dependencies**: Tests that rely on execution order
5. **Poor organization**: All tests in one function or poorly named tests
6. **Type errors**: Not testing type validation
7. **Decimal precision**: Using float comparison instead of Decimal

## Automation Rate

This benchmark is 100% automated:
- Coverage: Measured programmatically
- Mutation score: Measured programmatically
- Independence: Verified automatically
- Assertion quality: Analyzed automatically

## Validation

The benchmark has been validated to ensure:
- Scores are reproducible (±2% variance)
- Different approaches produce different scores
- Mutation testing discriminates between superficial and thorough tests
- The module contains realistic complexity requiring thought
