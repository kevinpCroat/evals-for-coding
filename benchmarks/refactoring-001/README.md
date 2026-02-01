# Refactoring Benchmark

## Overview

This benchmark tests an AI's ability to improve code structure while maintaining 100% behavioral compatibility. The task involves refactoring a working but messy order processing system that suffers from multiple code smells.

## Challenge

The starter code (`starter-code/order_processor.py`) works perfectly and has 59 passing tests, but it has intentional quality issues:

- **God Class**: Single class doing too much
- **Long Methods**: Methods over 100 lines
- **Code Duplication**: ~10% duplicate code blocks
- **Poor Naming**: Unclear variable names
- **High Complexity**: Average cyclomatic complexity of 6.5

The AI must refactor this code to improve structure while keeping all tests passing.

## Baseline Metrics

**Before refactoring:**
- Tests: 59 passing
- Average cyclomatic complexity: 6.5 (B grade)
- Code duplication: 10.34%
- Longest method: 127 lines (processOrderAndCalculateEverything)

## Scoring

The benchmark measures three components:

1. **Tests Passing (50%)**: All-or-nothing - if any test fails, score is 0
2. **Complexity Reduction (30%)**: Percentage reduction in average cyclomatic complexity
3. **Duplication Reduction (20%)**: Percentage reduction in duplicated code blocks

**Passing threshold**: 70/100 points

## Key Test

The fundamental challenge is: **Can the AI improve code quality while preserving behavior?**

This tests:
- Understanding of refactoring patterns
- Ability to maintain APIs while restructuring internals
- Test-driven refactoring discipline
- Code smell recognition and remediation

## Files

```
refactoring-001/
├── README.md                          # This file
├── spec.md                            # Detailed specification
├── prompts.txt                        # Task prompt for AI
├── starter-code/
│   ├── order_processor.py             # Messy but working code
│   └── test_order_processor.py        # 59 comprehensive tests
└── verification/
    ├── verify.sh                      # Scoring script
    └── measure_duplication.py         # Duplication detector
```

## Running the Benchmark

1. Copy the starter code to work on:
   ```bash
   cp starter-code/order_processor.py .
   ```

2. Refactor the code while keeping tests passing:
   ```bash
   pytest test_order_processor.py -v
   ```

3. Verify your solution:
   ```bash
   ./verification/verify.sh
   ```

## Example Refactorings

Good refactorings would include:

- **Extract Classes**: Break god class into:
  - InventoryManager
  - OrderProcessor
  - CustomerManager
  - PricingCalculator

- **Extract Methods**: Break 127-line method into:
  - Validation methods
  - Calculation methods
  - Update methods

- **DRY Principle**: Eliminate repeated:
  - Product/customer/order lookups
  - Validation patterns
  - Calculation logic

- **Improve Naming**: Replace unclear names:
  - `p, n, pr, s` → `product_id, name, price, stock`
  - Better method names

## Success Criteria

A successful refactoring will:

1. Pass all 59 tests (mandatory)
2. Reduce average complexity from 6.5 to <4.0 (ideally)
3. Reduce duplication from 10% to <3%
4. Have better class/method organization
5. Use clear, self-documenting names

## Learning Objectives

This benchmark teaches:

- Safe refactoring with test coverage
- Identifying and fixing code smells
- Maintaining backward compatibility
- Measuring code quality objectively
- Test-driven development practices

## Notes

- The test file must NOT be modified
- The public API must remain the same (tests depend on it)
- Focus on structural improvements, not feature additions
- Behavior preservation is paramount
