# Refactoring Benchmark - Quick Start Guide

## What You're Testing

Can the AI improve code quality while preserving behavior?

## The Task

Refactor `order_processor.py` to:
- Reduce complexity (break down long methods)
- Eliminate duplication (DRY principle)
- Improve naming (clear variable names)
- Better structure (extract classes)

**CRITICAL**: All 59 tests must still pass!

## Quick Start

```bash
# 1. Copy starter code
cp starter-code/order_processor.py .

# 2. Refactor the code (this is what the AI does)
# - Extract classes from god class
# - Break down the 127-line method
# - Eliminate duplicate lookup logic
# - Rename single-letter variables

# 3. Verify tests still pass
pytest test_order_processor.py -v

# 4. Check your score
./verification/verify.sh
```

## Scoring

- **50%** - Tests pass (all or nothing)
- **30%** - Complexity reduction
- **20%** - Duplication reduction
- **70+** - Passing score

## Current Metrics

**Before refactoring:**
- Complexity: 6.5 average
- Duplication: 10.34%
- Longest method: 127 lines

**Good target:**
- Complexity: <4.0 average (40% reduction)
- Duplication: <3% (70% reduction)
- Longest method: <30 lines

## Common Refactorings

### 1. Extract Classes
```python
# From: OrderProcessingSystemManager (does everything)
# To:
- InventoryManager
- CustomerManager  
- OrderProcessor
- PricingCalculator
```

### 2. Extract Methods
```python
# Break processOrderAndCalculateEverything (127 lines) into:
- _validate_order_data()
- _calculate_prices()
- _apply_discount()
- _calculate_shipping()
- _calculate_tax()
```

### 3. Eliminate Duplication
```python
# Extract repeated patterns:
def _find_order(order_id):
    """Used 3+ times in code"""
    
def _find_customer(customer_id):
    """Used 3+ times in code"""
```

### 4. Improve Naming
```python
# Bad: p, n, pr, s
# Good: product_id, name, price, stock
```

## What NOT to Do

- Don't modify test_order_processor.py
- Don't change the public API
- Don't add new features
- Don't break any tests
- Don't over-engineer

## Success Example

```
Running Refactoring Benchmark Verification...
1. Baseline: 6.5 complexity, 10.34% duplication
2. Tests: All 59 passed ✓
3. Complexity: 2.8 (57% reduction) ✓
4. Duplication: 2.1% (80% reduction) ✓
Score: 84/100 - PASSED
```

## Failure Example

```
Running Refactoring Benchmark Verification...
1. Baseline: 6.5 complexity, 10.34% duplication
2. Tests: 55 passed, 4 FAILED ✗
Score: 0/100 - FAILED (tests must pass)
```

## Tips

1. Run tests frequently during refactoring
2. Make small incremental changes
3. Extract methods before extracting classes
4. Use descriptive names
5. Follow the DRY principle
6. Keep the public API unchanged

## Files

- `starter-code/order_processor.py` - The messy code to refactor
- `starter-code/test_order_processor.py` - 59 tests (DO NOT MODIFY)
- `spec.md` - Full specification
- `verification/verify.sh` - Scoring script

## Getting Help

See README.md for full documentation and examples.
