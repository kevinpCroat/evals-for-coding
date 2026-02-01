# Verification Strategies by Evaluation Area

This document outlines automated verification mechanisms for each of the 20 software engineering evaluation areas.

---

## Creation

### Greenfield
**Verification Approach:**
- **Functional Tests**: Pre-written test suite that validates core functionality
- **Spec Compliance**: Checklist of required features/endpoints (automated parsing)
- **Build Success**: Project builds/runs without errors
- **Dependency Audit**: Check for appropriate dependencies (no unnecessary bloat)

**Scoring Components:**
- % of tests passing (40%)
- % of spec requirements met (30%)
- Code quality metrics (complexity, duplication) (20%)
- Documentation completeness (10%)

### Prototyping/Spike
**Verification Approach:**
- **Proof of Concept**: Does it demonstrate the key technical question?
- **Time to Working Demo**: Measured from task start event (first tool invocation) to first successful execution of demo script
- **Simplicity Metrics**: LOC count (prefer minimal), dependency count
- **Runnable State**: Can be executed with simple commands

**Scoring Components:**
- Demonstrates key concept (pass/fail)
- Time efficiency (faster = better, measured from task start to runnable artifact)
- Code simplicity (fewer LOC/dependencies = better)
- Working state (pass/fail)

**Note:** Task start is defined as the timestamp of the first tool invocation or command execution, not commit timestamps which can be gamed.

### Architecture
**Verification Approach:**
- **Architecture Decision Records**: AI generates ADRs for key decisions
- **Component Boundaries**: Static analysis of module dependencies (coupling/cohesion metrics)
- **Trade-off Analysis**: AI must document pros/cons of approach taken
- **Diagram Generation**: Can produce architecture diagrams

**Scoring Components:**
- Quality of ADRs (human-reviewed or LLM-as-judge, 30%)
- Coupling metrics (lower = better, 40%)
- Trade-off documentation completeness (automated checklist, 20%)
- Diagram accuracy (LLM-as-judge, 10%)

**Note:** LLM-as-judge components introduce variability across runs due to judge non-determinism. Consider using multiple judge samples and averaging, or human evaluation for ground truth.

### API Design
**Verification Approach:**
- **OpenAPI/Schema Generation**: Valid spec produced
- **Contract Tests**: Pre-written consumer contract tests pass
- **Consistency Checks**: Naming conventions, HTTP semantics
- **Versioning Strategy**: Version present in spec/routes (automated check) + documented approach

**Scoring Components:**
- Valid API spec (pass/fail prerequisite)
- Contract test passage: (passing tests / total tests) × 40
- REST/GraphQL best practices adherence (linter checks): 30%
- Documentation quality (all endpoints documented with examples): 20%
- Versioning presence and strategy: 10%

**Note:** Versioning can be partially automated by checking for version in paths (e.g., `/v1/`, `/api/v2/`) or headers (e.g., `Accept: application/vnd.api+json;version=1`), plus documentation of the versioning approach.

### Data Modelling
**Verification Approach:**
- **Schema Validation**: Generated schema is valid SQL/NoSQL/ORM
- **Migration Tests**: Migrations run successfully
- **Constraint Testing**: Foreign keys, indices, constraints work correctly
- **Query Performance**: Sample queries meet performance targets

**Scoring Components:**
- Schema validity (pass/fail)
- Migration success (pass/fail)
- Constraint correctness (30%)
- Query performance benchmarks (20%)
- Normalization appropriateness (LLM-as-judge, 20%)

---

## Evolution

### Maintenance
**Verification Approach:**
- **Dependency Updates**: Successfully updates outdated dependencies
- **Security Patches**: Identifies and applies CVE fixes
- **Bug Backlog Reduction**: Fixes existing bugs without breaking tests
- **Health Metrics**: No new warnings/errors introduced

**Scoring Components:**
- Dependencies updated successfully (40%)
- Existing tests still pass (40%)
- No new linting/type errors (20%)

### Refactoring
**Verification Approach:**
- **Behavioral Preservation**: All existing tests pass unchanged
- **Code Quality Improvement**: Complexity metrics improve (cyclomatic, cognitive)
- **No Functionality Change**: Integration tests pass
- **Diff Analysis**: No behavior changes, only structure

**Scoring Components:**
- All tests pass (50% - critical)
- Complexity reduction % (30%)
- Code duplication reduction % (20%)

### Rewriting
**Verification Approach:**
- **Test Preservation**: Same test suite passes
- **API Compatibility**: Public interface unchanged
- **Performance Comparison**: New implementation meets/exceeds old benchmarks
- **Edge Case Handling**: Pre-defined edge case test suite (null handling, boundary values, error conditions)

**Scoring Components:**
- Test passage (60%)
- Performance comparison (20%)
- Edge case handling: (edge case tests passing / total edge case tests) × 20

**Note:** Edge cases must be explicitly defined as a fixed test set (e.g., null inputs, empty arrays, max values, error conditions) to make this automatable. Without explicit tests, this metric cannot be measured.

### Porting
**Verification Approach:**
- **Cross-Platform Tests**: Tests pass in target environment
- **Feature Parity**: All features from source platform work
- **Idiomatic Code**: Uses target platform conventions (linter rules)
- **Build Process**: Clean build in target environment

**Scoring Components:**
- Tests pass in new environment (50%)
- Idiomatic code (static analysis, 20%)
- Build success (20%)
- Documentation for platform differences (10%)

### Code Migration
**Verification Approach:**
- **Version Compatibility**: Works with new dependency versions
- **Deprecated API Removal**: No use of deprecated APIs
- **Test Suite Passes**: All tests work with new versions
- **Build Pipeline**: CI/CD runs successfully

**Scoring Components:**
- Tests pass with new versions (60%)
- No deprecated API usage (20%)
- Build/CI success (20%)

---

## Quality

### Debugging
**Verification Approach:**
- **Root Cause Identified**: AI must document the actual cause (verified by applying fix and checking tests)
- **Minimal Reproduction**: Creates minimal test case reproducing bug
- **Trace Analysis**: Correctly interprets stack traces/logs
- **Hypothesis Testing**: Documents investigation process

**Scoring Components:**
- Root cause accuracy (verified by fix success): 60%
- Minimal repro provided (test compiles and reproduces bug): 20%
- Investigation documentation quality (LLM-as-judge): 20%

**Note:** Root cause accuracy is primarily verified by whether the proposed fix (based on the stated cause) actually resolves the bug. Direct verification of causal claims is only possible when the stated cause can be tested independently (e.g., "race condition in line X" → fix line X → bug disappears). Otherwise, this requires LLM or human judgment of the reasoning quality.

### Bug Fixing
**Verification Approach:**
- **Bug Test Passes**: Previously failing test now passes
- **No Regressions**: All other tests still pass
- **Edge Cases**: Fix handles related edge cases
- **Root Cause Addressed**: Fix targets actual cause, not symptoms

**Scoring Components:**
- Bug test passes (40%)
- No regressions (40%)
- Edge case coverage (10%)
- Fix quality (code review metrics, 10%)

### Testing
**Verification Approach:**
- **Test Coverage**: Coverage increases for target code
- **Test Quality**: Tests detect intentional bugs (mutation testing)
- **Test Independence**: Tests can run in isolation
- **Assertions**: Meaningful assertions (not just "does not throw")

**Scoring Components:**
- Coverage increase % (30%)
- Mutation score (40% - critical)
- Test independence (15%)
- Assertion quality (15%)

### Code Review
**Verification Approach:**
- **Issue Detection**: Identifies planted bugs/anti-patterns
- **False Positive Rate**: Doesn't flag correct code
- **Severity Classification**: Correctly prioritizes issues
- **Actionable Feedback**: Provides specific improvement suggestions

**Scoring Components:**
- Bug detection rate: (bugs found / bugs planted) × 40
- False positive penalty: max(0, 40 - (false positives × 4))
- Severity accuracy: (correctly classified / total issues) × 20
- Feedback quality (LLM-as-judge): 0-20 points

**Note:** False positive scoring inverts the typical component structure - each false positive reduces the score by 4 points from a base of 40, ensuring higher FP rates decrease the overall score.

### Performance Optimisation
**Verification Approach:**
- **Benchmark Improvement**: Performance metrics improve
- **Profiling Evidence**: Uses profiler data to guide optimization
- **No Functionality Change**: Tests still pass
- **Resource Usage**: Memory/CPU usage decreases

**Scoring Components:**
- Performance improvement % (50%)
- Tests still pass (30%)
- Optimization approach quality (profiling-based vs guessing, 20%)

### Security
**Verification Approach:**
- **Vulnerability Detection**: Identifies planted security issues
- **OWASP Top 10**: Checks for common vulnerabilities
- **Static Analysis**: SAST tools show improvement
- **Security Test Creation**: Creates security-focused tests

**Scoring Components:**
- Vulnerability detection rate (50%)
- SAST score improvement (30%)
- Security test quality (20%)

### Concurrency
**Verification Approach:**
- **Race Condition Tests**: Stress tests pass consistently over N runs (e.g., 100 runs)
- **Deadlock Detection**: Static analysis shows no potential deadlocks
- **Thread Safety**: Concurrent execution tests pass consistently
- **Performance Under Load**: Maintains performance with concurrent users

**Scoring Components:**
- Race condition test passage: (successful runs / total runs) × 40
- Deadlock freedom (static analysis + runtime detection): pass/fail × 30
- Load test performance (throughput under concurrency): 20%
- Code review for concurrency patterns (proper synchronization primitives): 10%

**Note:** Test flakiness can stem from code issues (logical races) or environment issues (resource limits, timeouts). Tests should run in controlled environments with adequate resources. Consider using race detection tools (e.g., ThreadSanitizer, Go race detector) to distinguish logical errors from environmental factors.

---

## Knowledge

### Documentation
**Verification Approach:**
- **Completeness**: All public APIs documented
- **Accuracy**: Code examples run successfully
- **Up-to-Date**: Docs match current code state
- **Clarity**: Readability metrics (reading level, structure)

**Scoring Components:**
- API coverage % (30%)
- Example execution success (40%)
- Docs-code consistency (20%)
- Readability score (10%)

### Legacy Code Comprehension
**Verification Approach:**
- **Q&A Accuracy**: Answers questions about codebase correctly
- **Dependency Mapping**: Correctly identifies component relationships
- **Change Impact Analysis**: Predicts which tests will break from a change
- **Summary Quality**: Generates accurate architectural summaries

**Scoring Components:**
- Q&A accuracy % (40%)
- Dependency map correctness (30%)
- Impact analysis accuracy (20%)
- Summary quality (LLM-as-judge, 10%)

---

## Operations

### Infrastructure
**Verification Approach:**
- **IaC Validation**: Terraform/CloudFormation validates and plans successfully
- **Deployment Success**: Code deploys to target environment
- **Idempotency**: Second run shows no unexpected changes (plan shows 0 changes, or only expected drift)
- **Security Best Practices**: No hardcoded secrets, proper IAM policies

**Scoring Components:**
- IaC validation (terraform validate / plan succeeds): 30%
- Successful deployment (apply succeeds, health checks pass): 40%
- Idempotency (second plan shows 0 changes or only documented expected changes): 15%
- Security scan pass (no secrets, least-privilege IAM): 15%

**Note:** Idempotency in practice means "no unexpected changes on re-run." Some resources may have acceptable drift (e.g., timestamps, auto-scaling counts). The benchmark should define what changes are acceptable vs unexpected.

---

## General Scoring Framework

Each benchmark produces a score from 0-100 using the weighted components above.

**Additional Metrics Tracked Across All Areas:**
- Time to completion
- Number of AI iterations/attempts
- Code churn (lines added/deleted)
- Tool usage patterns (which capabilities were used)
- Error recovery (how many failures before success)

**Composite Benchmark Score:**
```
Base Score = Σ(Component Score × Component Weight)
Penalty Multiplier = 1.0 - (time_penalty + iteration_penalty + error_penalty)
Final Score = max(0, Base Score × Penalty Multiplier)

Where:
- time_penalty = min(0.3, (time_taken - target_time) / target_time × 0.1)
- iteration_penalty = min(0.2, failed_attempts × 0.05)
- error_penalty = min(0.2, unrecovered_errors × 0.1)
```

**Score Bounds:** Final scores are clamped to [0, 100] range. Penalties are multiplicative rather than additive to ensure scores cannot go negative and to preserve relative component weights.

**Penalty Philosophy:** Penalties reduce the base score proportionally, meaning poor time/iteration/error performance affects the final score but cannot produce negative or nonsensical results.

This allows comparison both within an area (different AI approaches) and across areas (which tasks are hardest for AI).
