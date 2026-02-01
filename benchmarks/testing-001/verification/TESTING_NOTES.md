# Testing Notes for Evaluators

## Mutation Testing Details

The simple_mutate.py script creates the following types of mutations:

1. **Comparison operators**: `<` to `<=`, `>` to `>=`
2. **Arithmetic operators**: `+=` to `-=`, `*` to `/`, `-` to `+`
3. **Boolean values**: `True` to `False` and vice versa
4. **Initial values**: `0` to `1`
5. **Functions**: `min` to `max`, `sum` to `len`

Good tests should catch most of these mutations. A mutation is "killed" when the test suite fails after the mutation is applied.

## Expected Scores for Different Quality Levels

### Minimal Tests (Score: 20-40)
- Basic happy path tests only
- Low coverage (30-50%)
- Low mutation score (20-40%)
- Tests likely have dependencies

### Decent Tests (Score: 50-69 - FAIL)
- Some edge cases covered
- Moderate coverage (60-80%)
- Moderate mutation score (50-70%)
- May have some test dependencies

### Good Tests (Score: 70-85 - PASS)
- Most edge cases covered
- High coverage (85-95%)
- Good mutation score (70-85%)
- Tests are mostly independent
- Good assertion quality

### Excellent Tests (Score: 86-100 - PASS)
- All edge cases covered
- Very high coverage (95-100%)
- Excellent mutation score (85-100%)
- All tests independent
- Excellent assertion quality

## Common Issues

1. **High coverage, low mutation score**: Tests execute code but don't validate behavior
2. **Test dependencies**: Tests share state or depend on execution order
3. **Weak assertions**: Using `assert True` or not checking actual values
4. **Missing edge cases**: Not testing boundaries, empty states, or errors

## Verifying the Benchmark

To verify the benchmark is working:

```bash
# Should fail - no test file
./verification/verify.sh

# Create a minimal test file
echo 'def test_dummy(): assert True' > test_shopping_cart.py

# Should get low score (maybe 15-20)
./verification/verify.sh

# Use reference tests
cp .reference_tests.py test_shopping_cart.py

# Should get 75+ (but independence may fail due to fixture sharing)
./verification/verify.sh
```

## Benchmark Integrity

- shopping_cart.py should never be modified
- The mutation script creates temporary backups
- All temporary files are cleaned up after verification
