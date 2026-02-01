# Legacy Code Comprehension Benchmark

This benchmark evaluates an AI's ability to analyze and understand complex legacy codebases without documentation.

## Overview

**Difficulty:** Medium-Hard
**Time Estimate:** 30-45 minutes
**Focus Areas:** Code comprehension, dependency analysis, impact analysis

## Task Description

Analyze a legacy Python invoice processing system (450+ lines across 6 modules) and answer 20 questions about its architecture, dependencies, data flow, and business logic.

The codebase is a realistic legacy system with:
- Multiple classes with inheritance
- Complex dependencies between modules
- Technical debt (but functional)
- No documentation
- Realistic business logic

## Directory Structure

```
legacy-comprehension-001/
├── README.md               # This file
├── spec.md                # Detailed task specification
├── prompts.txt            # Standard prompts for AI
├── questions.json         # 20 questions to answer
├── starter-code/          # Legacy invoice processing system
│   ├── invoice.py        # Core models (Invoice, InvoiceItem)
│   ├── tax_calculator.py # Tax calculation logic
│   ├── payment_processor.py # Payment processing
│   ├── database.py       # Data persistence
│   ├── workflow.py       # Business process orchestration
│   └── validators.py     # Validation logic
└── verification/
    ├── test_comprehension.py # Python evaluation script
    └── verify.sh          # Main verification script
```

## Question Categories

The 20 questions cover:

1. **Architecture** (4 questions) - System components, design patterns, structure
2. **Dependencies** (4 questions) - Module relationships, imports, coupling
3. **Data Flow** (4 questions) - How data moves through the system
4. **Change Impact** (4 questions) - What breaks when changes are made
5. **Business Logic** (4 questions) - How features work, validation rules

## Scoring

Your submission is scored on four weighted components:

- **Q&A Accuracy** (40%) - Correctness of answers, keyword matching
- **Dependency Mapping** (30%) - Correctly identifying module relationships
- **Impact Analysis** (20%) - Accurately predicting change effects
- **Analysis Quality** (10%) - Clarity and completeness of explanations

**Passing Score:** 70%
**Partial Credit:** 40-69%
**Fail:** < 40%

## How to Use

1. Read the task in `spec.md`
2. Analyze the codebase in `starter-code/`
3. Read questions in `questions.json`
4. Create `answers.json` with your responses:

```json
{
  "answers": [
    {"id": 1, "answer": "Your detailed answer..."},
    {"id": 2, "answer": "Your detailed answer..."},
    ...
  ]
}
```

5. Run verification: `./verification/verify.sh`

## Answer Quality Guidelines

Good answers should:
- Reference specific class/method/constant names from the code
- Identify both direct and indirect dependencies
- Trace data flows end-to-end
- Consider cascading effects for impact analysis
- Explain the "why" behind design decisions

Avoid:
- Vague generalities without code references
- Missing indirect dependencies
- Incomplete impact analysis
- Assumptions not based on actual code

## Example Questions

**Architecture:** "What are the main components of this invoice processing system?"
**Dependencies:** "Which modules depend on the Invoice class?"
**Data Flow:** "How does tax calculation flow through the system?"
**Change Impact:** "If I change Invoice.STATUS_APPROVED, what breaks?"
**Business Logic:** "How does the auto-approval logic work?"

## Verification

The verification script:
1. Validates `answers.json` format
2. Compares answers to expected answers using fuzzy matching
3. Scores keyword matches and semantic similarity
4. Calculates weighted component scores
5. Outputs detailed results and feedback

Run: `./verification/verify.sh`

## Design Rationale

This benchmark tests critical skills for working with real-world codebases:
- Efficiently exploring unfamiliar code
- Understanding system architecture
- Tracing dependencies and data flows
- Predicting change impacts
- Comprehending business logic

These skills are essential for maintenance, refactoring, debugging, and extending legacy systems.
