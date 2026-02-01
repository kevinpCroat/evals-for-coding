# Refactoring Benchmark - Implementation Summary

## Benchmark Details

**Name**: refactoring-001  
**Type**: Code Quality / Refactoring  
**Language**: Python  
**Difficulty**: Intermediate-Advanced

## What It Tests

This benchmark evaluates an AI's ability to:
1. Identify and fix code smells
2. Improve code structure while preserving behavior
3. Apply refactoring patterns (Extract Class, Extract Method, DRY)
4. Maintain backward compatibility with existing tests
5. Reduce measurable complexity metrics

## The Challenge

### Starter Code Characteristics

**order_processor.py** (404 lines):
- 1 god class doing everything (OrderProcessingSystemManager)
- 10 methods with varying complexity
- Average cyclomatic complexity: 6.5 (B grade)
- Longest method: 127 lines
- Code duplication: 10.34%
- Poor variable naming (p, n, pr, s)
- Repeated logic patterns (lookup, validation, formatting)

**test_order_processor.py** (753 lines):
- 59 comprehensive tests
- 100% passing
- Tests all functionality thoroughly
- Must NOT be modified

### Code Smells Present

1. **God Class**: OrderProcessingSystemManager handles inventory, orders, customers, pricing, reports
2. **Long Method**: processOrderAndCalculateEverything is 127 lines
3. **Duplicated Code**: 
   - Order/customer/product lookup repeated 3+ times each
   - Validation patterns duplicated
   - Iteration logic repeated
4. **Poor Naming**: Single-letter variables (p, n, pr, s)
5. **Feature Envy**: Methods accessing data from multiple domains
6. **High Complexity**: Some methods have complexity of 19

## Scoring Components

### 1. Tests Passing (50% weight)
- **Measurement**: Run pytest on refactored code
- **Success**: All 59 tests pass
- **Failure**: Any test fails = 0 points total
- **Rationale**: Behavior preservation is paramount

### 2. Complexity Reduction (30% weight)
- **Measurement**: radon cc (cyclomatic complexity)
- **Baseline**: 6.5 average
- **Target**: <4.0 average (good refactoring)
- **Calculation**: (baseline - refactored) / baseline * 100
- **Rationale**: Simpler code is easier to maintain

### 3. Duplication Reduction (20% weight)
- **Measurement**: Custom duplication detector
- **Baseline**: 10.34%
- **Target**: <3% (minimal duplication)
- **Calculation**: (baseline - refactored) / baseline * 100
- **Rationale**: DRY principle reduces bugs

### Passing Threshold
**70/100** points required to pass

## Expected Refactoring Approaches

### Good Approaches

1. **Extract Classes**:
   ```python
   # Break god class into:
   - InventoryManager (products, stock)
   - CustomerManager (customers, VIP status)
   - OrderProcessor (order creation, cancellation)
   - PricingCalculator (discounts, tax, shipping)
   ```

2. **Extract Methods**:
   ```python
   # Break 127-line method into:
   - _validate_order_data()
   - _validate_inventory()
   - _calculate_prices()
   - _apply_discount()
   - _calculate_shipping()
   - _calculate_tax()
   - _update_inventory()
   - _update_customer()
   ```

3. **Eliminate Duplication**:
   ```python
   # Extract repeated patterns:
   - _find_order(order_id)
   - _find_customer(customer_id)
   - _find_product(product_id)
   - _validate_positive(value, field)
   ```

4. **Improve Naming**:
   ```python
   # Replace: p, n, pr, s
   # With: product_id, name, price, stock
   ```

### Bad Approaches

1. Adding new features (out of scope)
2. Modifying tests (forbidden)
3. Changing public API (breaks tests)
4. Over-engineering (adding unnecessary abstractions)
5. Breaking behavior to improve metrics

## Verification Process

The verify.sh script:

1. **Calculates Baseline**:
   - Runs radon on starter-code/order_processor.py
   - Measures duplication on starter code
   - Stores baseline metrics

2. **Tests Refactored Code**:
   - Copies test file to project root
   - Runs pytest on refactored order_processor.py
   - Counts passing/failing tests

3. **Measures Improvements**:
   - Runs radon on refactored code
   - Measures duplication on refactored code
   - Calculates percentage improvements

4. **Calculates Score**:
   - Tests: 100 if all pass, 0 if any fail
   - Complexity: % reduction from baseline
   - Duplication: % reduction from baseline
   - Weighted sum: 50% + 30% + 20%

5. **Outputs JSON**:
   ```json
   {
     "benchmark": "refactoring-001",
     "components": {...},
     "base_score": 85.5,
     "final_score": 85,
     "passed": true
   }
   ```

## Tools Used

- **pytest**: Test runner
- **radon**: Cyclomatic complexity analyzer
- **measure_duplication.py**: Custom duplication detector
  - Finds repeated code blocks (3-5 lines)
  - Normalizes whitespace and comments
  - Counts duplicate instances

## Example Scoring Scenarios

### Scenario 1: No Refactoring
```
Tests: 100 (59/59 pass)
Complexity: 0 (6.5 → 6.5)
Duplication: 0 (10.34 → 10.34)
Final: 50/100 - FAIL
```

### Scenario 2: Good Refactoring
```
Tests: 100 (59/59 pass)
Complexity: 60 (6.5 → 2.6, 60% reduction)
Duplication: 80 (10.34 → 2.07, 80% reduction)
Final: 50 + 18 + 16 = 84/100 - PASS
```

### Scenario 3: Broke Tests
```
Tests: 0 (55/59 pass, 4 fail)
Complexity: 100 (6.5 → 0, impossible but hypothetical)
Duplication: 100 (10.34 → 0, impossible but hypothetical)
Final: 0/100 - FAIL (tests must pass)
```

## Files Manifest

```
refactoring-001/
├── README.md                     # User-facing documentation
├── spec.md                       # Detailed specification
├── prompts.txt                   # Task prompt for AI
├── SUMMARY.md                    # This file
├── starter-code/
│   ├── order_processor.py        # Messy code (404 lines)
│   └── test_order_processor.py   # Tests (753 lines, 59 tests)
└── verification/
    ├── verify.sh                 # Scoring script (bash)
    └── measure_duplication.py    # Duplication detector (python)
```

## Key Design Decisions

1. **50% weight on tests**: Behavior preservation is critical
2. **Python**: Easy to measure complexity with radon
3. **Real code smells**: Not artificial, reflects real-world problems
4. **Measurable metrics**: Objective scoring reduces subjectivity
5. **Comprehensive tests**: 59 tests ensure behavior preservation
6. **No penalties**: Focus on quality improvement, not speed

## Validation

✅ All 59 tests pass on starter code  
✅ Baseline metrics are measurable  
✅ Verification script outputs valid JSON  
✅ Unrefactored code scores 50/100  
✅ Code has genuine refactoring opportunities  
✅ Tests are comprehensive and independent  
✅ Public API is stable and testable  

## Usage

```bash
# For AI agent
cd /path/to/refactoring-001
cp starter-code/order_processor.py .
# ... refactor the code ...
./verification/verify.sh

# For manual testing
cp starter-code/order_processor.py .
pytest test_order_processor.py -v
python3 -m radon cc order_processor.py -a
```

## Expected Difficulty

- **Beginner AI**: May struggle to maintain tests (0-40 points)
- **Intermediate AI**: Can refactor without breaking tests (50-70 points)
- **Advanced AI**: Significantly improves structure (70-90 points)
- **Expert AI**: Optimal refactoring with best practices (90-100 points)

## Learning Value

This benchmark teaches:
- Safe refactoring practices
- Code smell recognition
- Test-driven refactoring
- Complexity measurement
- DRY principle application
- Backward compatibility maintenance
