# Phase 2: Integration with Claude Night Market

## Overview

[Claude Night Market](https://github.com/kevinpCroat/claude-night-market) is a marketplace of 16 specialized plugins for Claude Code that can significantly accelerate Phase 2 development of our evaluation framework.

## How Claude Night Market Helps Phase 2

### 1. **Abstract Plugin** - Benchmark Development Infrastructure

**What it provides:**
- **skill-evaluator agent**: Human-in-loop qualitative evaluation of skill executions
- **skill-improver agent**: Automated improvement suggestions for skills
- **plugin-validator agent**: Validates plugin structure and requirements
- **meta-architect agent**: Architectural guidance for complex tasks

**How we'll use it:**
```bash
# Use for creating new benchmarks
Skill(abstract:create-skill)
  --skill-name "debugging-001"
  --purpose "Test AI's ability to identify root causes"

# Validate benchmark structure
Skill(abstract:plugin-validator)
  --target benchmarks/debugging-001

# Evaluate benchmark quality
Skill(abstract:skill-evaluator)
  --skill-name "debugging-001"
```

**Benefits for Phase 2:**
- Automated validation of benchmark structure
- Quality scoring for benchmarks
- Consistent patterns across all benchmarks
- Reduces manual review burden

---

### 2. **Imbue Plugin** - Test-Driven Development Enforcement

**What it provides:**
- **TDD Gate (PreToolUse hook)**: Enforces test file existence before implementation
- **proof-of-work**: Requires functional verification before completion claims
- **rigorous-reasoning**: Checklist-based analysis for complex problems
- **review-core**: Structured methodology for audits

**How we'll use it:**
```bash
# Enable TDD enforcement for benchmark creation
# This ensures we write verification tests BEFORE benchmark code
Skill(imbue:proof-of-work)
  --task "Create debugging-001 benchmark"

# Structured review of benchmark quality
/full-review benchmarks/debugging-001
```

**Benefits for Phase 2:**
- Ensures all benchmarks have comprehensive tests
- Prevents "write code first, test later" anti-pattern
- Enforces our verification-first approach
- Structured quality reviews

---

### 3. **Spec-Kit Plugin** - Specification-Driven Development

**What it provides:**
- Specification templates and workflows
- Requirements tracking
- Spec-to-code workflows
- Validation of implementation against spec

**How we'll use it:**
```bash
# Create benchmark spec first
/speckit-specify
  --output benchmarks/debugging-001/spec.md
  --requirements "Identify root cause of failing test"

# Validate implementation matches spec
Skill(spec-kit:validate-implementation)
  --spec benchmarks/debugging-001/spec.md
  --implementation benchmarks/debugging-001/
```

**Benefits for Phase 2:**
- Consistent spec format across benchmarks
- Ensures specs written before implementation
- Automated spec compliance checking
- Aligns with our verification strategies

---

### 4. **Pensive Plugin** - Code Review & Quality

**What it provides:**
- Code review automation
- Usage frequency and failure rate tracking
- Workflow stability monitoring
- Quality metrics

**How we'll use it:**
```bash
# Review newly created benchmark
Skill(pensive:code-review)
  --target benchmarks/debugging-001

# Track benchmark reliability
Skill(pensive:track-usage)
  --target verification/verify.sh
```

**Benefits for Phase 2:**
- Automated code review for benchmarks
- Track which benchmarks are most/least stable
- Identify patterns in benchmark failures
- Quality metrics for continuous improvement

---

### 5. **Minister Plugin** - Issue Tracking

**What it provides:**
- Issue creation and management
- Task tracking
- Workflow automation
- Progress monitoring

**How we'll use it:**
```bash
# Create issues for remaining benchmarks
/minister create-issue
  --title "Implement debugging-001 benchmark"
  --labels "phase-2,tier-2,debugging"
  --milestone "Phase 2 Completion"

# Track Phase 2 progress
/minister list-issues
  --milestone "Phase 2 Completion"
```

**Benefits for Phase 2:**
- Track 7 Tier 2 benchmarks as issues
- Automated progress reporting
- Link benchmarks to GitHub issues
- Project management integration

---

### 6. **Sanctum Plugin** - Git Workflows & Session Management

**What it provides:**
- Named session isolation
- Git workflow automation
- Branch management
- PR preparation

**How we'll use it:**
```bash
# Create isolated session for each benchmark
/sanctum create-session
  --name "debugging-001-dev"
  --type feature

# Prepare PR when benchmark complete
/prepare-pr
  --title "Add debugging-001 benchmark"
  --validate-tests true
```

**Benefits for Phase 2:**
- Clean git workflows for each benchmark
- Automated PR creation
- Session isolation prevents cross-contamination
- Quality gates before commits

---

### 7. **Hookify Plugin** - Rules Engine & Context-Aware Suggestions

**What it provides:**
- Custom hook system
- Context-aware suggestions
- Workflow automation
- Quality gates

**How we'll use it:**
```bash
# Create hooks for benchmark quality checks
Skill(hookify:create-rule)
  --trigger "before_commit"
  --action "validate_benchmark_structure"
  --context "benchmarks/*"
```

**Benefits for Phase 2:**
- Automated quality checks during development
- Context-aware suggestions for benchmark improvements
- Consistent enforcement of standards
- Pre-commit validation

---

## Proposed Phase 2 Workflow with Claude Night Market

### Step 1: Setup (One-time)

```bash
cd /Users/kperko/code/evals-for-coding

# Install Claude Night Market plugins
/plugin marketplace add kevinpCroat/claude-night-market

# Install specific plugins for benchmark development
/plugin install abstract@claude-night-market    # Meta-tools
/plugin install imbue@claude-night-market       # TDD enforcement
/plugin install spec-kit@claude-night-market    # Spec-driven dev
/plugin install pensive@claude-night-market     # Code review
/plugin install minister@claude-night-market    # Issue tracking
/plugin install sanctum@claude-night-market     # Git workflows
/plugin install hookify@claude-night-market     # Rules engine

# Initialize
claude --init
```

### Step 2: Create Benchmark Issues

```bash
# Create GitHub issues for all 7 Tier 2 benchmarks
/minister create-milestone "Phase 2: Tier 2 Benchmarks"

/minister create-issue --title "debugging-001: Identify root cause" --milestone "Phase 2"
/minister create-issue --title "maintenance-001: Update dependencies" --milestone "Phase 2"
/minister create-issue --title "api-design-001: Design OpenAPI spec" --milestone "Phase 2"
/minister create-issue --title "data-modelling-001: Database schema" --milestone "Phase 2"
/minister create-issue --title "documentation-001: Document codebase" --milestone "Phase 2"
/minister create-issue --title "rewriting-001: Reimplement function" --milestone "Phase 2"
/minister create-issue --title "code-review-001: Find planted bugs" --milestone "Phase 2"
```

### Step 3: Develop Each Benchmark

For each benchmark (e.g., debugging-001):

```bash
# 1. Create session
/sanctum create-session --name debugging-001-dev --type feature

# 2. Create spec FIRST (spec-kit enforces this)
/speckit-specify
  --output benchmarks/debugging-001/spec.md
  --category "Quality"
  --area "Debugging"

# 3. Create benchmark structure (abstract helps)
Skill(abstract:create-skill)
  --skill-name debugging-001
  --structure benchmark-template

# 4. Write verification tests FIRST (imbue enforces this)
# The TDD gate will prevent writing implementation before tests exist
Skill(imbue:proof-of-work)
  --create-test verification/tests/test_debugging.py

# 5. Create starter code (buggy code for AI to debug)
# Now we can write implementation because tests exist

# 6. Validate benchmark structure
Skill(abstract:plugin-validator)
  --target benchmarks/debugging-001

# 7. Code review
/full-review benchmarks/debugging-001

# 8. Test the benchmark
./benchmarks/debugging-001/verification/verify.sh

# 9. Prepare PR
/prepare-pr
  --title "Add debugging-001 benchmark"
  --validate-tests true
  --close-issue true
```

### Step 4: Quality Assurance

```bash
# Run all benchmarks to ensure no regressions
python evaluation-framework/run_benchmark.py --all

# Generate leaderboard
python evaluation-framework/generate_leaderboard.py results/

# Track metrics
Skill(pensive:track-usage)
  --analyze-failure-rates
```

---

## Integration Points

### 1. Extend Benchmark Template

Update `templates/benchmark-template/` to include:
- Claude Night Market skill references
- Pre-commit hooks from hookify
- TDD enforcement patterns from imbue
- Spec templates from spec-kit

### 2. Add Quality Gates

Create `.claude/hooks/` in our repo:
```json
{
  "pre-commit": [
    "hookify:validate-benchmark-structure",
    "imbue:verify-tests-exist",
    "abstract:validate-plugin"
  ],
  "pre-push": [
    "run_benchmark.py --all",
    "pensive:code-review"
  ]
}
```

### 3. Automated Issue Management

```bash
# Create a script that uses minister to:
# - Create issues for all remaining benchmarks
# - Link PRs to issues
# - Update progress tracking
# - Generate status reports
```

### 4. Continuous Improvement

```bash
# Use skill-evaluator to collect feedback
Skill(abstract:skill-evaluator)
  --benchmark debugging-001
  --mode recent

# Use skill-improver for automated suggestions
Skill(abstract:skill-improver)
  --benchmark debugging-001
  --analyze-failures
```

---

## Specific Phase 2 Benchmark Mappings

### Debugging Benchmark (debugging-001)

**Claude Night Market plugins to use:**
- **imbue:rigorous-reasoning** - Structured root cause analysis
- **imbue:proof-of-work** - Verify fix actually works
- **spec-kit** - Clear debugging task specification
- **pensive** - Review debugging methodology

**Workflow:**
1. Create buggy code with failing test
2. Spec requires AI to document root cause analysis
3. Verification checks that AI correctly identified cause
4. Proof-of-work ensures fix is tested

---

### API Design Benchmark (api-design-001)

**Claude Night Market plugins to use:**
- **spec-kit** - OpenAPI spec creation and validation
- **abstract:create-skill** - Template generation
- **pensive** - API design review

**Workflow:**
1. Spec defines API requirements
2. AI must generate OpenAPI spec
3. Contract tests validate spec
4. Design review checks best practices

---

### Code Review Benchmark (code-review-001)

**Claude Night Market plugins to use:**
- **pensive** - Code review methodology
- **imbue:review-core** - Structured review framework
- **abstract:skill-evaluator** - Quality scoring

**Workflow:**
1. Plant bugs in PR code
2. AI must find and classify issues
3. Verification checks detection rate
4. False positive rate measured

---

## Benefits Summary

Using Claude Night Market for Phase 2 provides:

✅ **50% faster development**
- Automated structure creation
- Built-in quality gates
- Reusable patterns

✅ **Higher quality benchmarks**
- TDD enforcement
- Automated validation
- Structured reviews

✅ **Better documentation**
- Spec-driven approach
- Consistent templates
- Automatic README generation

✅ **Project management**
- Issue tracking
- Progress monitoring
- Automated reporting

✅ **Continuous improvement**
- Usage tracking
- Failure analysis
- Automated suggestions

---

## Migration Plan

### Week 1: Setup & Integration
- [ ] Install Claude Night Market plugins
- [ ] Configure hooks for our repo
- [ ] Update benchmark template with CNM patterns
- [ ] Create issues for 7 Tier 2 benchmarks

### Week 2-3: First 3 Benchmarks
- [ ] debugging-001 (with imbue:rigorous-reasoning)
- [ ] maintenance-001 (with minister tracking)
- [ ] api-design-001 (with spec-kit)

### Week 4-5: Next 4 Benchmarks
- [ ] data-modelling-001 (with spec-kit)
- [ ] documentation-001 (with pensive review)
- [ ] rewriting-001 (with imbue:proof-of-work)
- [ ] code-review-001 (with pensive methodology)

### Week 6: Quality & Documentation
- [ ] Run all benchmarks
- [ ] Generate comprehensive leaderboard
- [ ] Update documentation
- [ ] Create Phase 3 plan

---

## Key Takeaways

1. **Claude Night Market provides battle-tested patterns** that align perfectly with our benchmark development needs

2. **TDD enforcement** from imbue ensures we maintain our verification-first approach

3. **Automated quality gates** prevent shipping low-quality benchmarks

4. **Project management tools** help track progress across 7+ benchmarks

5. **Continuous improvement infrastructure** enables benchmark evolution

6. **Reusable components** speed up development without sacrificing quality

This integration should reduce Phase 2 development time from estimated 8 weeks to approximately 4-5 weeks while improving benchmark quality and consistency.
