# Testing-001 Benchmark Example

## What You'll See

When running this benchmark, the AI will be given:

1. **shopping_cart.py** - A 180-line Python module with no tests
2. **spec.md** - Requirements for writing comprehensive tests
3. **prompts.txt** - Instructions on what to test

## Expected AI Behavior

The AI should:

1. Read and understand the shopping_cart module
2. Identify all testable functions and edge cases
3. Create test_shopping_cart.py with comprehensive tests
4. Run tests iteratively, improving coverage and quality

## Sample Interaction

**AI**: "I'll analyze the shopping cart module and create comprehensive tests."

**AI**: *Reads shopping_cart.py*

**AI**: "I've identified the following areas to test:
- Item class validation
- Cart operations (add, remove, update)
- Price calculations (subtotal, discounts, tax)
- Edge cases (empty cart, negative values, etc.)
- Error handling

Creating test suite..."

**AI**: *Creates test_shopping_cart.py*

**AI**: *Runs ./verification/verify.sh*

**Output**:
```json
{
  "final_score": 85,
  "components": {
    "coverage": {"score": 95},
    "mutation_score": {"score": 83},
    "independence": {"score": 100},
    "assertion_quality": {"score": 100}
  },
  "passed": true
}
```

## Scoring Breakdown

- **30%** Coverage - Did tests execute the code?
- **40%** Mutation Score - Do tests catch actual bugs?
- **15%** Independence - Can tests run in any order?
- **15%** Assertion Quality - Are assertions meaningful?

**Passing**: 70+ points

## Key Success Factors

1. **Read the code carefully** - Understand what each function does
2. **Test edge cases** - Empty, zero, negative, boundary values  
3. **Test errors** - All exception paths
4. **Use good assertions** - Check actual values, not just execution
5. **Keep tests independent** - No shared state between tests

## Common Pitfalls

- Writing tests that just execute code without assertions
- Missing error/exception tests
- Tests that depend on execution order
- Not testing boundary conditions
- Focusing only on happy paths
