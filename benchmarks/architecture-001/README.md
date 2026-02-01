# Architecture Design Benchmark (architecture-001)

This benchmark evaluates an AI agent's ability to design comprehensive system architecture, make well-reasoned architectural decisions, and clearly document trade-offs and alternatives.

## Overview

**Task**: Design a complete system architecture for a real-time collaborative document editing platform (similar to Google Docs or Notion).

**Challenge**: The AI must make critical architectural decisions with incomplete information, consider multiple alternatives, justify choices with clear reasoning, and document trade-offs. This tests the AI's ability to think architecturally, not just write code.

**Key Difficulty**: Unlike code-based benchmarks with deterministic test results, architecture design is inherently subjective. Multiple valid solutions exist, requiring evaluation of reasoning quality rather than correctness of a single answer.

## What This Benchmark Tests

1. **Architectural Thinking**: Can the AI identify key architectural decisions and understand their implications?
2. **Trade-off Analysis**: Does the AI consider alternatives and understand the pros/cons of each approach?
3. **Documentation Skills**: Can the AI clearly communicate complex technical decisions through ADRs and diagrams?
4. **Technical Breadth**: Does the AI demonstrate knowledge across databases, distributed systems, scalability, security, and operations?
5. **Practical Judgment**: Does the AI make realistic, implementable decisions considering real-world constraints (cost, complexity, team expertise)?

## Requirements

The AI must design architecture for a system with:
- 100,000 concurrent users at peak
- <100ms P95 latency for real-time edits
- 99.9% availability with zero data loss
- Multi-region deployment capability
- SOC 2, GDPR, CCPA compliance

Key ambiguous decisions left to the AI:
- Real-time collaboration approach (OT vs CRDT)
- Database technology selection
- Microservices vs monolith
- Multi-region strategy
- Caching and search infrastructure

See `requirements.md` for complete requirements.

## Deliverables

The AI must create:

1. **architecture.md** - Comprehensive system architecture overview
2. **adrs/** - 3-5 Architecture Decision Records documenting major decisions
3. **diagrams/** - Text-based diagrams (Mermaid/PlantUML/ASCII):
   - Component diagram
   - Deployment diagram
   - Data flow diagram
4. **trade-offs.md** - Analysis of key architectural trade-offs

## Evaluation Methodology

This benchmark uses an **LLM-as-judge** approach since architecture quality is subjective.

### Scoring Components

- **ADR Quality (30%)**: Format, reasoning depth, alternatives analysis
- **Diagram Completeness (20%)**: Coverage of key components, readability
- **Trade-off Analysis (25%)**: Consideration of alternatives, realistic assessment
- **Technical Soundness (25%)**: Feasibility, appropriate technology choices, requirements coverage

### Scoring Process

1. **Basic validation**: Check for required files and minimum content
2. **Structural analysis**: Verify ADR format, diagram presence, document structure
3. **LLM evaluation**: Claude API evaluates reasoning quality, technical soundness, and depth of analysis
4. **Weighted scoring**: Combine component scores with weights

### Pass Threshold

**70/100** - The architecture must demonstrate solid technical reasoning and cover all major requirements.

### Fallback Scoring

If the Anthropic API is unavailable, the script falls back to structural analysis (checking for required sections, keywords, content length). This provides basic scoring but is less reliable than LLM-based evaluation.

## Running the Benchmark

```bash
# Run verification on a submission
cd /path/to/submission
../verification/verify.sh

# Or specify submission directory
../verification/verify.sh /path/to/submission

# Requires: python3 and anthropic package
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY=your-api-key
```

## Example JSON Output

```json
{
  "benchmark": "architecture-001",
  "timestamp": "2026-01-31T21:00:00Z",
  "components": {
    "adr_quality": {
      "score": 85,
      "weight": 0.30,
      "details": "Strong reasoning with clear alternatives"
    },
    "diagram_completeness": {
      "score": 90,
      "weight": 0.20,
      "details": "All required diagrams present (3500 chars total)"
    },
    "tradeoff_analysis": {
      "score": 80,
      "weight": 0.25,
      "details": "Thorough analysis of major decisions"
    },
    "technical_soundness": {
      "score": 88,
      "weight": 0.25,
      "details": "Appropriate technology choices for requirements"
    }
  },
  "base_score": 85.15,
  "penalties": {
    "time_penalty": 0.0,
    "iteration_penalty": 0.0,
    "error_penalty": 0.0
  },
  "final_score": 85.15,
  "passed": true
}
```

## Design Notes

### Why LLM-as-Judge?

Architecture design cannot be evaluated with deterministic tests. A human architect would evaluate:
- Is the reasoning sound?
- Are trade-offs realistic?
- Are alternatives properly considered?
- Is the architecture implementable?

LLMs can approximate this human judgment at scale.

### Evaluation Reliability

- **Consistency**: Same submission should score within ±5 points across evaluations
- **Discrimination**: Different quality levels should produce different scores
- **Face validity**: Scores should align with expert human judgment
- **Transparency**: Evaluation prompts are explicit about criteria

### Known Limitations

1. **Subjectivity**: Architecture has no single right answer
2. **LLM bias**: Evaluator may favor certain architectural styles
3. **Cost**: API calls required for evaluation
4. **Version sensitivity**: Different Claude versions may score differently

These are acceptable trade-offs for evaluating complex architectural thinking.

## Benchmark Metadata

- **Category**: Software Design
- **Difficulty**: Advanced
- **Time estimate**: 45-90 minutes for human architect
- **Automation level**: 70% (structure checks) + 30% (LLM judgment)
- **Evaluation cost**: ~$0.10-0.30 per submission (Claude API)

## Files

```
architecture-001/
├── README.md                          # This file
├── spec.md                           # Task specification for AI
├── prompts.txt                       # Standard prompts
├── requirements.md                   # System requirements
└── verification/
    ├── verify.sh                     # Main verification script
    └── evaluate_architecture.py      # LLM-as-judge evaluator
```
