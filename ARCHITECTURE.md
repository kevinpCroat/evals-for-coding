# Architecture Documentation

This document describes the architecture of the AI Coding Evaluation Framework.

---

## System Overview

The framework consists of 20 independent benchmarks, each with a standardized structure, verification system, and scoring mechanism. All benchmarks output JSON for automated analysis and leaderboard generation.

---

## High-Level Architecture

```mermaid
graph TB
    subgraph "Benchmark Suite"
        B1[bug-fixing-001]
        B2[testing-001]
        B3[greenfield-001]
        B4[...]
        B20[porting-001]
    end

    subgraph "Evaluation Framework"
        Runner[run_benchmark.py]
        Leaderboard[generate_leaderboard.py]
    end

    subgraph "Outputs"
        JSON[results/*.json]
        MD[leaderboard.md]
        Stats[statistical_analysis.md]
    end

    B1 --> Runner
    B2 --> Runner
    B3 --> Runner
    B4 --> Runner
    B20 --> Runner

    Runner --> JSON
    JSON --> Leaderboard
    Leaderboard --> MD
    Leaderboard --> Stats

    style B1 fill:#e1f5e1
    style B2 fill:#e1f5e1
    style B3 fill:#e1f5e1
    style B20 fill:#e1f5e1
    style Runner fill:#e3f2fd
    style JSON fill:#fff3e0
```

---

## Benchmark Structure

Each benchmark follows a standardized directory structure:

```
benchmark-name/
├── README.md              # Overview and usage instructions
├── spec.md               # Detailed task specification for AI
├── prompts.txt           # Standardized prompt format
├── starter-code/         # Initial codebase (if applicable)
│   ├── src/             # Source code to modify
│   ├── tests/           # Existing tests (may be incomplete)
│   └── requirements.txt # Dependencies
├── data/                 # Sample data (if applicable)
│   └── sample_data.csv
├── verification/         # Automated verification system
│   ├── verify.sh        # Main verification script
│   ├── tests/           # Comprehensive test suite
│   ├── check_*.py       # Code quality checkers
│   └── reference_output.json
└── reference-solution/   # Hidden from AI during evaluation
    └── solution.py
```

---

## Benchmark Execution Flow

```mermaid
sequenceDiagram
    participant AI as AI Assistant
    participant Bench as Benchmark
    participant Verify as Verification System
    participant Score as Scoring Engine

    AI->>Bench: Read spec.md + prompts.txt
    AI->>Bench: Analyze starter-code/
    AI->>AI: Implement solution
    AI->>Bench: Write/modify code
    AI->>Verify: Execute ./verification/verify.sh

    Verify->>Verify: Run tests
    Verify->>Verify: Check code quality
    Verify->>Verify: Measure performance
    Verify->>Verify: Validate security

    Verify->>Score: Component scores
    Score->>Score: Calculate base_score
    Score->>Score: Apply penalties
    Score->>Score: Compute final_score

    Score->>AI: Return JSON result

    Note over AI,Score: Entire process is automated
```

---

## Verification System Architecture

```mermaid
graph TB
    subgraph "Verification Script (verify.sh)"
        Entry[Entry Point]

        subgraph "Component Scoring"
            C1[Tests Pass?]
            C2[Code Quality?]
            C3[Performance?]
            C4[Security?]
            C5[Custom Checks]
        end

        subgraph "Scoring Engine"
            Base[Calculate Base Score]
            Penalty[Apply Penalties]
            Final[Final Score]
        end

        Entry --> C1
        Entry --> C2
        Entry --> C3
        Entry --> C4
        Entry --> C5

        C1 --> Base
        C2 --> Base
        C3 --> Base
        C4 --> Base
        C5 --> Base

        Base --> Penalty
        Penalty --> Final
    end

    subgraph "Output"
        JSON[JSON Result]
        Pass{Score >= 70?}
    end

    Final --> JSON
    JSON --> Pass

    Pass -->|Yes| Success[passed: true]
    Pass -->|No| Fail[passed: false]

    style C1 fill:#e1f5e1
    style C2 fill:#e1f5e1
    style C3 fill:#e1f5e1
    style C4 fill:#e1f5e1
    style C5 fill:#e1f5e1
    style Success fill:#c8e6c9
    style Fail fill:#ffcdd2
```

---

## Scoring Formula

```mermaid
graph LR
    subgraph "Component Scores"
        C1[Component 1<br/>Score × Weight]
        C2[Component 2<br/>Score × Weight]
        C3[Component 3<br/>Score × Weight]
        CN[Component N<br/>Score × Weight]
    end

    subgraph "Base Score"
        Sum[Σ Weighted<br/>Scores]
    end

    subgraph "Penalties"
        Time[Time Penalty]
        Iter[Iteration Penalty]
        Error[Error Penalty]
        Mult[Penalty<br/>Multiplier]
    end

    subgraph "Final Score"
        Final[max 0,<br/>Base × Multiplier]
        Pass{>= 70?}
    end

    C1 --> Sum
    C2 --> Sum
    C3 --> Sum
    CN --> Sum

    Time --> Mult
    Iter --> Mult
    Error --> Mult

    Sum --> Final
    Mult --> Final
    Final --> Pass

    style Sum fill:#e3f2fd
    style Final fill:#fff3e0
```

**Formula:**
```
Base Score = Σ(Component Score × Component Weight)
Penalty Multiplier = 1.0 - (time_penalty + iteration_penalty + error_penalty)
Final Score = max(0, Base Score × Penalty Multiplier)
Passed = Final Score >= 70
```

---

## Benchmark Categories & Coverage

```mermaid
mindmap
  root((AI Coding<br/>Evaluation))
    Creation
      Greenfield
      Prototyping
      Architecture
      API Design
      Data Modelling
    Evolution
      Maintenance
      Refactoring
      Rewriting
      Porting
      Code Migration
    Quality
      Debugging
      Bug Fixing
      Testing
      Code Review
      Performance
      Security
      Concurrency
    Knowledge
      Documentation
      Legacy Comprehension
    Operations
      Infrastructure
```

---

## Example: security-001 Architecture

```mermaid
graph TB
    subgraph "Input: Vulnerable Code"
        App[app.py<br/>366 lines<br/>10 vulnerabilities]

        V1[SQL Injection]
        V2[XSS]
        V3[Hardcoded Secrets]
        V4[Command Injection]
        V5[Path Traversal]
        V6[Insecure Deserialization]
        V7[Auth Bypass]
        V8[Weak Passwords]
        V9[Debug Mode]
        V10[Missing Validation]
    end

    subgraph "AI Task"
        Read[Read VULNERABILITIES.md]
        Analyze[Analyze vulnerable code]
        Fix[Apply security fixes]
    end

    subgraph "Verification"
        Tests[Run security tests]
        Bandit[Bandit SAST scan]
        Manual[Manual review checklist]
    end

    subgraph "Scoring"
        S1[Vulnerabilities Fixed<br/>50% weight]
        S2[SAST Improvement<br/>30% weight]
        S3[Tests Written<br/>20% weight]
        Score[Final Score]
    end

    App --> Read
    Read --> Analyze
    Analyze --> Fix

    Fix --> Tests
    Fix --> Bandit
    Fix --> Manual

    Tests --> S1
    Bandit --> S2
    Manual --> S3

    S1 --> Score
    S2 --> Score
    S3 --> Score

    style V1 fill:#ffcdd2
    style V2 fill:#ffcdd2
    style V3 fill:#ffcdd2
    style V4 fill:#ffcdd2
    style Score fill:#c8e6c9
```

---

## Example: performance-001 Architecture

```mermaid
graph TB
    subgraph "Input"
        Code[Slow Code<br/>O n² complexity<br/>15 second runtime]
        Profile[cProfile Output<br/>Identifies bottlenecks]
    end

    subgraph "AI Task"
        Analyze[Analyze profiler data]
        Identify[Identify bottlenecks]
        Optimize[Apply optimizations]
    end

    subgraph "Verification"
        Correct[Correctness Tests<br/>All must pass]
        Perf[Performance Tests<br/>Measure speedup]
    end

    subgraph "Scoring"
        S1[Tests Pass<br/>30% weight]
        S2[Performance Gain<br/>50% weight]
        S3[Code Quality<br/>20% weight]
        Score[Final Score]
    end

    Code --> Analyze
    Profile --> Analyze
    Analyze --> Identify
    Identify --> Optimize

    Optimize --> Correct
    Optimize --> Perf

    Correct --> S1
    Perf --> S2
    Optimize --> S3

    S1 --> Score
    S2 --> Score
    S3 --> Score

    style Code fill:#ffcdd2
    style Correct fill:#c8e6c9
    style Perf fill:#c8e6c9
```

**Performance Scoring:**
- Baseline: 15 seconds
- Target: 10x speedup (1.5 seconds)
- Reference: 3,750x speedup (4ms)

---

## Leaderboard Generation Architecture

```mermaid
graph TB
    subgraph "Input: Individual Results"
        R1[bug-fixing-001.json]
        R2[testing-001.json]
        R3[...]
        R20[porting-001.json]
    end

    subgraph "Analysis Engine"
        Parse[Parse JSON files]
        Aggregate[Aggregate scores]
        Stats[Calculate statistics]
        Rank[Rank AI models]
    end

    subgraph "Output Formats"
        MD[leaderboard.md<br/>Human-readable]
        JSON[leaderboard.json<br/>Machine-readable]
        Charts[charts/<br/>Visualizations]
    end

    R1 --> Parse
    R2 --> Parse
    R3 --> Parse
    R20 --> Parse

    Parse --> Aggregate
    Aggregate --> Stats
    Stats --> Rank

    Rank --> MD
    Rank --> JSON
    Rank --> Charts

    style MD fill:#e3f2fd
    style JSON fill:#fff3e0
    style Charts fill:#f3e5f5
```

**Leaderboard Metrics:**
- Average score across all benchmarks
- Pass rate (% of benchmarks passed)
- Category breakdowns (Creation, Evolution, Quality, etc.)
- Difficulty breakdowns (Easy, Medium, Hard)
- Per-benchmark scores

---

## Development Workflow

```mermaid
graph TB
    subgraph "Phase 1: Planning"
        Taxonomy[Define 20<br/>Evaluation Areas]
        Strategy[Design Verification<br/>Strategies]
        Template[Create Benchmark<br/>Template]
    end

    subgraph "Phase 2: Implementation"
        Tier1[Build Tier 1<br/>5 benchmarks<br/>Sequential]
        Tier2[Build Tier 2<br/>7 benchmarks<br/>Parallel]
        Tier3[Build Tier 3<br/>8 benchmarks<br/>Max Parallel]
    end

    subgraph "Phase 3: Validation"
        Test[Test with buggy code<br/>should fail]
        Verify[Test with correct code<br/>should pass]
        Document[Write documentation]
    end

    subgraph "Phase 4: Deployment"
        Git[Git commit & push]
        Release[GitHub release]
        Announce[Community announcement]
    end

    Taxonomy --> Strategy
    Strategy --> Template
    Template --> Tier1

    Tier1 --> Tier2
    Tier2 --> Tier3

    Tier1 --> Test
    Tier2 --> Test
    Tier3 --> Test

    Test --> Verify
    Verify --> Document
    Document --> Git
    Git --> Release
    Release --> Announce

    style Tier1 fill:#e1f5e1
    style Tier2 fill:#e1f5e1
    style Tier3 fill:#e1f5e1
    style Announce fill:#c8e6c9
```

**Timeline:**
- Phase 1: 45 minutes
- Phase 2: 6 hours (4h Tier 1, 2h Tier 2+3)
- Phase 3: 1 hour
- Phase 4: 15 minutes
- **Total:** ~8 hours

---

## Sub-Agent Parallelization

```mermaid
graph TB
    subgraph "Main Agent"
        Main[Main Coordinator]
        Plan[Create Benchmark Plan]
    end

    subgraph "Sub-Agents (Parallel Execution)"
        A1[Agent 1<br/>security-001]
        A2[Agent 2<br/>performance-001]
        A3[Agent 3<br/>concurrency-001]
        A4[Agent 4<br/>architecture-001]
    end

    subgraph "Per-Agent Tasks"
        T1[Write spec.md]
        T2[Create starter code]
        T3[Build tests]
        T4[Write verify.sh]
        T5[Create docs]
    end

    subgraph "Integration"
        Collect[Collect Results]
        Validate[Validate All Benchmarks]
        Commit[Git Commit]
    end

    Main --> Plan
    Plan --> A1
    Plan --> A2
    Plan --> A3
    Plan --> A4

    A1 --> T1
    A2 --> T1
    A3 --> T1
    A4 --> T1

    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> T5

    T5 --> Collect
    Collect --> Validate
    Validate --> Commit

    style A1 fill:#e3f2fd
    style A2 fill:#e3f2fd
    style A3 fill:#e3f2fd
    style A4 fill:#e3f2fd
```

**Efficiency Gains:**
- Phase 1 (Sequential): 48 min/benchmark
- Phase 2 (2-3 parallel): 17 min/benchmark (2.8x faster)
- Phase 3 (4+ parallel): 15 min/benchmark (3.2x faster)

---

## Technology Stack

```mermaid
graph TB
    subgraph "Languages"
        Python[Python<br/>18 benchmarks]
        JS[JavaScript/TypeScript<br/>2 benchmarks]
        TF[Terraform<br/>1 benchmark]
        SQL[SQL<br/>Multiple]
        Bash[Bash<br/>All verify scripts]
    end

    subgraph "Testing Frameworks"
        Pytest[pytest]
        Jest[jest]
        Mutation[mutpy]
        Stress[Custom stress tests]
    end

    subgraph "Web Frameworks"
        Flask[Flask]
        FastAPI[FastAPI]
        Express[Express.js]
    end

    subgraph "Database"
        SQLAlchemy[SQLAlchemy ORM]
        Postgres[PostgreSQL]
        SQLite[SQLite]
        Alembic[Alembic migrations]
    end

    subgraph "Code Quality"
        Bandit[Bandit SAST]
        ESLint[ESLint]
        Radon[Radon complexity]
        Profiler[cProfile]
    end

    subgraph "Infrastructure"
        Terraform2[Terraform]
        AWS[AWS Provider]
        Docker[Docker future]
    end

    Python --> Pytest
    Python --> Flask
    Python --> SQLAlchemy
    Python --> Bandit

    JS --> Jest
    JS --> Express
    JS --> ESLint

    TF --> Terraform2
    Terraform2 --> AWS

    style Python fill:#4caf50
    style JS fill:#ffc107
    style TF fill:#9c27b0
```

---

## Data Flow

```mermaid
sequenceDiagram
    participant User as User/AI Model
    participant Bench as Benchmark
    participant Verify as Verification
    participant File as File System
    participant Output as JSON Output

    User->>Bench: 1. Read spec.md, prompts.txt
    Bench->>User: Task description

    User->>File: 2. Implement solution
    File->>User: Code written

    User->>Verify: 3. Run ./verification/verify.sh

    Verify->>File: 4a. Read solution code
    Verify->>Verify: 4b. Run tests
    Verify->>Verify: 4c. Check quality
    Verify->>Verify: 4d. Measure performance

    Verify->>Verify: 5. Calculate scores
    Verify->>Output: 6. Write JSON
    Output->>User: 7. Return result

    Note over User,Output: Fully automated pipeline
```

---

## Future Architecture Enhancements

```mermaid
graph TB
    subgraph "Current State"
        Current[20 Benchmarks<br/>Local Execution<br/>Manual Analysis]
    end

    subgraph "Phase 1: Containerization"
        Docker[Docker Containers]
        Isolation[Complete Isolation]
        Reproducible[Reproducible Env]
    end

    subgraph "Phase 2: CI/CD"
        GH[GitHub Actions]
        Auto[Automated Testing]
        Regression[Regression Detection]
    end

    subgraph "Phase 3: Analytics"
        DB[Results Database]
        Dashboard[Web Dashboard]
        Charts[Visualization]
        API[Public API]
    end

    subgraph "Phase 4: Expansion"
        MultiLang[More Languages]
        Domain[Domain-Specific]
        Difficulty[Difficulty Variants]
        Collaborative[Multi-Agent]
    end

    Current --> Docker
    Docker --> Isolation
    Isolation --> Reproducible

    Reproducible --> GH
    GH --> Auto
    Auto --> Regression

    Regression --> DB
    DB --> Dashboard
    Dashboard --> Charts
    Charts --> API

    API --> MultiLang
    MultiLang --> Domain
    Domain --> Difficulty
    Difficulty --> Collaborative

    style Current fill:#e3f2fd
    style Collaborative fill:#c8e6c9
```

---

## Security Considerations

```mermaid
graph TB
    subgraph "Threat Model"
        T1[Malicious AI<br/>Code Execution]
        T2[Resource Exhaustion]
        T3[Data Leakage]
        T4[Evaluation Gaming]
    end

    subgraph "Mitigations"
        M1[Sandboxed Execution<br/>Future: Docker]
        M2[Resource Limits<br/>Timeouts, Memory]
        M3[No Sensitive Data<br/>All public]
        M4[Anti-Gaming<br/>Hidden tests]
    end

    subgraph "Current Status"
        S1[Local Execution<br/>User responsibility]
        S2[5-min timeouts<br/>Implemented]
        S3[Public data only<br/>Implemented]
        S4[Reference solutions<br/>Hidden]
    end

    T1 --> M1
    T2 --> M2
    T3 --> M3
    T4 --> M4

    M1 --> S1
    M2 --> S2
    M3 --> S3
    M4 --> S4

    style T1 fill:#ffcdd2
    style T2 fill:#ffcdd2
    style M1 fill:#fff9c4
    style S1 fill:#fff9c4
```

**Current Security Posture:**
- ⚠️ Local execution (user responsibility for sandboxing)
- ✅ Timeouts prevent infinite loops
- ✅ No sensitive data in benchmarks
- ✅ Reference solutions hidden from AI

**Future Improvements:**
- Docker containerization for isolation
- Resource quotas (CPU, memory, disk)
- Network isolation for security benchmarks
- Automated security scanning of submissions

---

## Extensibility

The architecture is designed for extensibility:

### Adding New Benchmarks
1. Copy `templates/benchmark-template/`
2. Customize spec.md, prompts.txt
3. Implement verification logic
4. Add to `benchmarks/` directory
5. Update documentation

### Adding New Languages
1. Create language-specific verification scripts
2. Add tooling (linters, test frameworks)
3. Update template with language examples
4. Document language-specific guidelines

### Adding New Evaluation Metrics
1. Implement metric calculation in verify.sh
2. Add component to JSON output
3. Update scoring formula if needed
4. Document metric rationale

### Integration with External Tools
- CI/CD: GitHub Actions, Jenkins
- Databases: PostgreSQL, MongoDB for results
- Dashboards: Grafana, custom web UI
- APIs: REST endpoints for submission/results

---

## Performance Characteristics

| Component | Time | Scalability |
|-----------|------|-------------|
| Single Benchmark | 1-5 min | O(1) |
| All 20 Benchmarks | 20-100 min | O(n) |
| Leaderboard Gen | <1 min | O(n×m) models |
| Sub-agent Build | 15 min | O(1) per agent |

**Bottlenecks:**
- Test execution (most time-consuming)
- Performance benchmarks (actual timing)
- LLM-as-judge (API latency)

**Optimizations:**
- Parallel test execution
- Cached results for unchanged code
- Async LLM evaluation
- Incremental verification

---

## Comparison with Other Benchmarks

```mermaid
graph TB
    subgraph "HumanEval"
        HE[164 Problems<br/>Function Writing<br/>Pass@k Metric]
    end

    subgraph "MBPP"
        MBPP[974 Problems<br/>Python Only<br/>Text Match]
    end

    subgraph "Brazil Bench"
        BB[Realistic Tasks<br/>Automated Verify<br/>Web Dev Focus]
    end

    subgraph "This Framework"
        TF[20 Benchmarks<br/>Full Lifecycle<br/>Multi-Language<br/>90% Automation<br/>Production Quality]
    end

    HE --> Narrow[Narrow Scope]
    MBPP --> Narrow
    BB --> Focused[Domain Focused]

    TF --> Comprehensive[Comprehensive<br/>Coverage]

    style TF fill:#c8e6c9
    style Comprehensive fill:#4caf50
```

**Our Differentiators:**
1. **Full lifecycle coverage** (20 areas vs narrow focus)
2. **Production quality** (realistic complexity)
3. **High automation** (>90% deterministic)
4. **Multi-language** (Python, JS/TS, Terraform)
5. **Comprehensive docs** (90+ markdown files)

---

## Conclusion

This architecture enables:
- ✅ Comprehensive AI evaluation across 20 areas
- ✅ Automated, reproducible scoring
- ✅ Extensible framework for future benchmarks
- ✅ Production-ready quality and documentation
- ✅ Rapid development (8 hours for 20 benchmarks)

The modular design, standardized structure, and automation-first approach make this the most comprehensive AI coding evaluation framework available.
