# Benchmark Development Prioritization

This document prioritizes which benchmarks to develop first based on automation feasibility, foundational value, and real-world impact.

---

## Prioritization Criteria

Each benchmark is evaluated on:

1. **Automation Feasibility** (1-5): How easy is it to create fully automated, deterministic verification?
2. **Foundation Value** (1-5): Does this benchmark enable or inform development of other benchmarks?
3. **AI Readiness** (1-5): Are current AI coding assistants reasonably capable in this area?
4. **Real-World Impact** (1-5): How frequently do developers encounter this task?
5. **Verification Clarity** (1-5): How unambiguous is success vs failure?

**Total Score:** Sum of criteria (max 25 points)

---

## Tier 1: Start Here (Score: 20-25)

These benchmarks should be developed first due to high automation feasibility, clear success criteria, and foundational value.

### 1. Bug Fixing (Score: 24)
- **Automation:** 5 - Test goes from failing → passing
- **Foundation:** 5 - Core skill, validates debugging too
- **AI Readiness:** 5 - AIs are quite good at this
- **Real-World:** 5 - Extremely common daily task
- **Clarity:** 4 - Clear but fix quality varies

**Why First:** Clearest success metric (failing test passes), high real-world frequency, foundational for other tasks.

**Benchmark Idea:** Provide codebase with failing test, AI must fix the bug to make test pass without breaking others.

---

### 2. Testing (Score: 23)
- **Automation:** 5 - Mutation testing provides objective quality metric
- **Foundation:** 5 - Tests are verification mechanism for other benchmarks
- **AI Readiness:** 4 - Good but test quality varies
- **Real-World:** 5 - Essential development practice
- **Clarity:** 4 - Coverage clear, quality harder

**Why First:** Foundation for verifying many other benchmarks. Mutation testing provides objective quality measurement.

**Benchmark Idea:** Provide untested module, AI must write tests that achieve coverage + high mutation score.

---

### 3. Greenfield (Score: 22)
- **Automation:** 4 - Spec compliance + functional tests
- **Foundation:** 5 - Baseline "can AI build something from scratch"
- **AI Readiness:** 5 - This is what AIs are trained on
- **Real-World:** 4 - Common but less frequent than bug fixing
- **Clarity:** 4 - Spec interpretation can vary

**Why First:** Natural starting point, validates AI can build working code from specifications. Template for Brazil Bench approach.

**Benchmark Idea:** Specification document → AI builds working implementation passing test suite (similar to Brazil Bench).

---

### 4. Refactoring (Score: 22)
- **Automation:** 5 - Behavioral preservation is binary (tests pass/fail)
- **Foundation:** 4 - Tests code transformation without behavior change
- **AI Readiness:** 4 - AIs can do this but cautiously
- **Real-World:** 5 - Constant need in evolving codebases
- **Clarity:** 4 - Behavior preservation clear, improvement quality harder

**Why First:** Perfect test case for "change structure, preserve behavior" - all tests must still pass.

**Benchmark Idea:** Provide code with code smells (long methods, duplicate code), AI must refactor while keeping all tests passing.

---

### 5. Code Migration (Score: 20)
- **Automation:** 5 - Tests pass with new versions, no deprecated APIs
- **Foundation:** 3 - Tests version compatibility handling
- **AI Readiness:** 4 - Good at dependency updates
- **Real-World:** 4 - Regular necessity in maintained codebases
- **Clarity:** 4 - Clear criteria but edge cases exist

**Why First:** Very clear success metrics, common pain point, tests AI's ability to handle breaking changes.

**Benchmark Idea:** Provide codebase on old framework version, AI must migrate to new version with breaking changes.

---

## Tier 2: Next Wave (Score: 16-19)

Develop these after Tier 1 is established. Still highly valuable but may depend on Tier 1 benchmarks or require more setup.

### 6. Debugging (Score: 19)
- **Automation:** 3 - Root cause verification challenging
- **Foundation:** 4 - Precedes bug fixing
- **AI Readiness:** 4 - Decent at hypothesis formation
- **Real-World:** 5 - Daily occurrence
- **Clarity:** 3 - Root cause determination subjective

**Dependencies:** Should be developed after Bug Fixing benchmark to distinguish debugging (finding cause) from fixing (applying solution).

**Benchmark Idea:** Provide failing test + codebase, AI must identify root cause before being allowed to fix.

---

### 7. Maintenance (Score: 19)
- **Automation:** 4 - Dependency updates, tests pass
- **Foundation:** 3 - Tests ongoing care
- **AI Readiness:** 4 - Good at routine updates
- **Real-World:** 5 - Constant need
- **Clarity:** 3 - "Maintenance" is broad

**Benchmark Idea:** Provide codebase with outdated dependencies and known CVEs, AI must update without breaking functionality.

---

### 8. API Design (Score: 18)
- **Automation:** 4 - Contract tests provide clear verification
- **Foundation:** 3 - Used in greenfield projects
- **AI Readiness:** 4 - Can generate specs
- **Real-World:** 4 - Common in API development
- **Clarity:** 3 - Design quality subjective

**Benchmark Idea:** Provide requirements, AI must design API with OpenAPI spec that passes consumer contract tests.

---

### 9. Data Modelling (Score: 18)
- **Automation:** 4 - Schema validation, query performance
- **Foundation:** 3 - Used in greenfield + refactoring
- **AI Readiness:** 4 - Good at schema design
- **Real-World:** 4 - Every data-driven app
- **Clarity:** 3 - Normalization choices subjective

**Benchmark Idea:** Provide business requirements, AI must design database schema that passes constraint tests and performance benchmarks.

---

### 10. Documentation (Score: 17)
- **Automation:** 4 - API coverage + example execution
- **Foundation:** 2 - Useful but not foundational
- **AI Readiness:** 5 - AIs excel at this
- **Real-World:** 3 - Important but often neglected
- **Clarity:** 3 - Quality is subjective

**Benchmark Idea:** Provide undocumented codebase, AI must document all public APIs with runnable examples.

---

### 11. Rewriting (Score: 17)
- **Automation:** 4 - Tests pass, performance comparison
- **Foundation:** 3 - Similar to refactoring
- **AI Readiness:** 4 - Can reimplement logic
- **Real-World:** 3 - Less common than refactoring
- **Clarity:** 3 - Implementation approach varies

**Benchmark Idea:** Provide function with tests, AI must rewrite implementation (e.g., iterative → recursive) while tests pass.

---

### 12. Code Review (Score: 17)
- **Automation:** 4 - Planted bugs provide ground truth
- **Foundation:** 2 - Useful validation tool
- **AI Readiness:** 3 - Can find issues but false positives
- **Real-World:** 5 - Constant activity
- **Clarity:** 3 - Severity classification subjective

**Dependencies:** Benefits from having Bug Fixing and Security benchmarks to inform what issues to plant.

**Benchmark Idea:** Provide PR with planted bugs (syntax, logic, security), AI must identify issues with correct severity.

---

## Tier 3: Advanced (Score: 12-15)

More complex benchmarks requiring significant setup or dealing with harder-to-automate aspects.

### 13. Porting (Score: 16)
- **Automation:** 3 - Cross-platform testing complex
- **Foundation:** 2 - Specialized skill
- **AI Readiness:** 3 - Challenging for idioms
- **Real-World:** 3 - Occasional need
- **Clarity:** 4 - Tests pass/fail is clear

**Benchmark Idea:** Provide Python codebase with tests, AI must port to JavaScript/TypeScript with tests passing.

---

### 14. Security (Score: 16)
- **Automation:** 4 - SAST tools + planted vulnerabilities
- **Foundation:** 3 - Important for quality
- **AI Readiness:** 3 - Mixed results
- **Real-World:** 4 - Critical but specialized
- **Clarity:** 2 - Vulnerability types vary

**Benchmark Idea:** Provide code with OWASP Top 10 vulnerabilities, AI must identify and fix them.

---

### 15. Performance Optimisation (Score: 15)
- **Automation:** 4 - Performance benchmarks clear
- **Foundation:** 2 - Specialized optimization skill
- **AI Readiness:** 3 - Hit or miss
- **Real-World:** 3 - Occasional need
- **Clarity:** 3 - Approach quality varies

**Benchmark Idea:** Provide slow implementation with profiler data, AI must optimize to meet performance target.

---

### 16. Legacy Code Comprehension (Score: 15)
- **Automation:** 3 - Q&A verification challenging
- **Foundation:** 3 - Needed for many tasks
- **AI Readiness:** 4 - Good at code understanding
- **Real-World:** 4 - Common pain point
- **Clarity:** 1 - Understanding is hard to measure

**Benchmark Idea:** Provide complex legacy codebase, AI must answer questions about architecture, dependencies, and change impact.

---

### 17. Concurrency (Score: 14)
- **Automation:** 3 - Flakiness vs real issues
- **Foundation:** 2 - Specialized skill
- **AI Readiness:** 2 - Often struggles
- **Real-World:** 3 - Important but specialized
- **Clarity:** 4 - Race detectors help

**Benchmark Idea:** Provide code with race conditions, AI must make it thread-safe using proper synchronization.

---

### 18. Prototyping/Spike (Score: 14)
- **Automation:** 2 - "Demonstrates concept" is subjective
- **Foundation:** 2 - Specialized use case
- **AI Readiness:** 4 - Can build quick demos
- **Real-World:** 3 - Common in research phase
- **Clarity:** 3 - Success criteria fuzzy

**Benchmark Idea:** Provide technical question (e.g., "Can we stream video with WebRTC?"), AI must build minimal proof of concept.

---

### 19. Architecture (Score: 13)
- **Automation:** 2 - Heavy LLM-as-judge dependency
- **Foundation:** 4 - Important for greenfield
- **AI Readiness:** 3 - Can generate but quality varies
- **Real-World:** 4 - Critical for large projects
- **Clarity:** 2 - Many valid approaches

**Benchmark Idea:** Provide high-level requirements, AI must produce ADRs, component diagrams, and justify trade-offs.

---

### 20. Infrastructure (Score: 13)
- **Automation:** 3 - Deployment environments complex
- **Foundation:** 1 - Orthogonal to most tasks
- **AI Readiness:** 3 - Can generate IaC
- **Real-World:** 3 - Important but specialized
- **Clarity:** 4 - Deployment success clear

**Benchmark Idea:** Provide app requirements, AI must create Terraform/CloudFormation that deploys successfully to cloud.

---

## Recommended Development Roadmap

### Phase 1 (Months 1-2): Core Foundation
1. **Bug Fixing** - Establish test-based verification pattern
2. **Testing** - Create mutation testing framework for benchmark verification
3. **Greenfield** - Adapt Brazil Bench template approach

**Deliverable:** 3 working benchmarks with automated scoring, initial leaderboard comparing AI approaches.

---

### Phase 2 (Months 3-4): Evolution & Quality
4. **Refactoring** - Test behavioral preservation
5. **Code Migration** - Test version upgrade handling
6. **Debugging** - Test root cause identification
7. **Maintenance** - Test ongoing codebase care

**Deliverable:** 7 total benchmarks covering creation + evolution + critical quality tasks.

---

### Phase 3 (Months 5-6): Broader Coverage
8. **API Design** - Contract testing pattern
9. **Data Modelling** - Schema validation pattern
10. **Documentation** - Code-docs consistency checks
11. **Code Review** - Planted bug detection

**Deliverable:** 11 benchmarks covering most common development tasks.

---

### Phase 4 (Months 7-8): Advanced Capabilities
12. **Security** - Vulnerability detection
13. **Performance Optimisation** - Benchmark-driven optimization
14. **Porting** - Cross-language/platform testing
15. **Legacy Code Comprehension** - Understanding evaluation

**Deliverable:** 15 benchmarks including specialized/advanced areas.

---

### Phase 5 (Months 9-10): Specialized Areas
16. **Concurrency** - Race detection and thread safety
17. **Rewriting** - Implementation transformation
18. **Architecture** - Design quality evaluation
19. **Infrastructure** - IaC and deployment
20. **Prototyping/Spike** - Rapid exploration

**Deliverable:** Complete suite of 20 benchmarks across all evaluation areas.

---

## Success Metrics for Prioritization

For each phase, validate:
- **Automation Rate**: % of scoring that is fully automated (target: >70%)
- **Reproducibility**: Same AI + same benchmark = same score ±5%
- **Discrimination**: Different AI approaches produce different scores
- **Face Validity**: Scores align with human judgment of AI capability

If any benchmark fails these metrics, refactor before proceeding to next phase.
