# Benchmark Template

This template provides the standard structure for creating new benchmarks in the software engineering evaluation suite.

## Directory Structure

```
benchmark-name/
├── README.md           # Benchmark description and instructions
├── spec.md            # Task specification given to the AI
├── prompts.txt        # Standard prompts to provide to AI
├── starter-code/      # Initial codebase (if applicable)
├── verification/      # Automated verification scripts
│   ├── tests/        # Test suite
│   └── verify.sh     # Main verification script
└── expected-output/   # Reference implementation or expected behavior
```

## Required Files

### spec.md
Clear, unambiguous specification of what the AI must accomplish. Should include:
- Task description
- Success criteria
- Constraints and requirements
- What deliverables are expected

### prompts.txt
Standard prompts to give the AI agent. Format:
```
=== TASK ===
[Main task description]

=== CONTEXT ===
[Any additional context]

=== DELIVERABLES ===
[What should be produced]
```

### verification/verify.sh
Automated script that:
1. Runs all verification checks
2. Outputs JSON with scoring components
3. Returns exit code 0 on success, non-zero on failure

Expected JSON output format:
```json
{
  "benchmark": "benchmark-name",
  "timestamp": "2025-01-31T15:00:00Z",
  "components": {
    "component1_name": {"score": 0-100, "weight": 0.0-1.0, "details": "..."},
    "component2_name": {"score": 0-100, "weight": 0.0-1.0, "details": "..."}
  },
  "base_score": 0-100,
  "penalties": {
    "time_penalty": 0.0-0.3,
    "iteration_penalty": 0.0-0.2,
    "error_penalty": 0.0-0.2
  },
  "final_score": 0-100,
  "passed": true/false
}
```

## Creating a New Benchmark

1. Copy this template directory: `cp -r templates/benchmark-template benchmarks/your-benchmark-name`
2. Update README.md with benchmark-specific information
3. Write spec.md with clear task requirements
4. Create prompts.txt with standard task description
5. Add starter-code/ if the benchmark requires existing code
6. Implement verification/tests/ with comprehensive test suite
7. Write verification/verify.sh to automate scoring
8. Test the benchmark with multiple AI approaches
9. Validate that scores are reproducible and discriminating

## Testing Your Benchmark

Before considering a benchmark complete:
- [ ] Automation Rate: >70% of scoring is deterministic
- [ ] Reproducibility: Same AI produces same score ±5%
- [ ] Discrimination: Different AI approaches produce different scores
- [ ] Face Validity: Scores align with human judgment
- [ ] Clear Pass/Fail: Success criteria are unambiguous
