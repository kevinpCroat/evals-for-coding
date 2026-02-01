# Software Engineering Evals for AI Coding Assistants

A comprehensive benchmark suite for evaluating AI coding assistants across 20 software engineering evaluation areas.

## Overview

This repository contains automated, verifiable benchmarks that test AI's ability to complete real-world software development tasks. Each benchmark provides:
- Clear task specifications
- Automated scoring with objective metrics
- Reproducible evaluation results
- JSON output for analysis

## Current Benchmarks

### Tier 1: Core Capabilities (5/5 Complete)

| Benchmark | Category | Description | Status |
|-----------|----------|-------------|--------|
| [bug-fixing-001](benchmarks/bug-fixing-001/) | Quality | Fix off-by-one error in date calculation | ✅ Complete |
| [testing-001](benchmarks/testing-001/) | Quality | Write comprehensive tests with mutation testing | ✅ Complete |
| [greenfield-001](benchmarks/greenfield-001/) | Creation | Build URL shortener REST API from scratch | ✅ Complete |
| [refactoring-001](benchmarks/refactoring-001/) | Evolution | Improve code structure while preserving behavior | ✅ Complete |
| [code-migration-001](benchmarks/code-migration-001/) | Evolution | Migrate SQLAlchemy 1.4 → 2.0 | ✅ Complete |

### Tier 2: Next Wave (0/7 Planned)

- **Debugging** - Identify root cause of failing tests
- **Maintenance** - Update dependencies and fix CVEs
- **API Design** - Design REST API with OpenAPI spec
- **Data Modelling** - Design database schema
- **Documentation** - Document undocumented codebase
- **Rewriting** - Reimplement with different approach
- **Code Review** - Identify planted bugs

### Tier 3: Advanced (0/8 Planned)

See [benchmark-prioritization.md](benchmark-prioritization.md) for full roadmap.

## Quick Start

### Running a Single Benchmark

```bash
# Navigate to a benchmark directory
cd benchmarks/bug-fixing-001

# Read the task specification
cat spec.md

# Read the prompt for AI
cat prompts.txt

# Complete the task (e.g., fix the bug)
# ...

# Run verification
./verification/verify.sh
```

### Verification Output

Each benchmark outputs JSON with scoring details:

```json
{
  "benchmark": "bug-fixing-001",
  "timestamp": "2026-02-01T00:00:00Z",
  "components": {
    "bug_fixed": {"score": 100, "weight": 0.6, "details": "..."},
    "no_regressions": {"score": 100, "weight": 0.3, "details": "..."},
    "code_quality": {"score": 100, "weight": 0.1, "details": "..."}
  },
  "base_score": 100,
  "penalties": {
    "time_penalty": 0,
    "iteration_penalty": 0,
    "error_penalty": 0
  },
  "final_score": 100,
  "passed": true
}
```

## Benchmark Structure

Each benchmark follows a standard structure:

```
benchmark-name/
├── README.md              # Benchmark-specific documentation
├── spec.md               # Task specification for AI
├── prompts.txt           # Standard prompt format
├── starter-code/         # Initial codebase (if applicable)
│   └── ...
├── data/                 # Sample data (if applicable)
│   └── ...
├── verification/         # Automated verification
│   ├── verify.sh        # Main verification script
│   └── tests/           # Test suite
└── reference-solution/   # Reference implementation (hidden from AI)
    └── ...
```

## Evaluation Criteria

Benchmarks are scored on:
- **Automation Rate**: >70% of scoring is deterministic
- **Reproducibility**: Same AI produces same score ±5%
- **Discrimination**: Different approaches produce different scores
- **Face Validity**: Scores align with human judgment

## Development

### Creating a New Benchmark

```bash
# Copy the template
cp -r templates/benchmark-template benchmarks/your-benchmark-name

# Update the files
# - spec.md: Task specification
# - prompts.txt: AI instructions
# - verification/verify.sh: Scoring logic
# - verification/tests/: Test suite

# Test the benchmark
cd benchmarks/your-benchmark-name
./verification/verify.sh
```

See [templates/benchmark-template/README.md](templates/benchmark-template/README.md) for detailed guidelines.

## Documentation

- [Evaluation Areas](software-engineering-evaluation-areas.md) - 20 areas across 5 categories
- [Verification Strategies](verification-strategies.md) - Detailed verification approach for each area
- [Benchmark Prioritization](benchmark-prioritization.md) - Development roadmap and priorities
- [Template Guide](templates/benchmark-template/README.md) - How to create new benchmarks

## Scoring Framework

Each benchmark produces a score from 0-100:

```
Base Score = Σ(Component Score × Component Weight)
Penalty Multiplier = 1.0 - (time_penalty + iteration_penalty + error_penalty)
Final Score = max(0, Base Score × Penalty Multiplier)
```

**Pass Threshold**: Typically 70/100

## Languages & Technologies

Current benchmarks use:
- **Python** (4 benchmarks): pytest, SQLAlchemy, Flask/FastAPI
- **Language-agnostic** (1 benchmark): REST API design

Future benchmarks will include JavaScript/TypeScript, Go, Rust, and other popular languages.

## Contributing

Contributions welcome! To add a new benchmark:

1. Choose an evaluation area from [evaluation areas](software-engineering-evaluation-areas.md)
2. Follow the [benchmark template](templates/benchmark-template/)
3. Ensure >70% automation rate
4. Validate reproducibility
5. Submit a PR

## License

[To be determined]

## Acknowledgments

Inspired by [Brazil Bench](https://github.com/brazil-bench) and their approach to automated benchmark evaluation.
