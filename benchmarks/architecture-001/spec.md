# Architecture Design Benchmark - Specification

## Objective

Design a comprehensive system architecture for a real-time collaborative document editing platform based on the provided requirements. You must create detailed architectural documentation including Architecture Decision Records (ADRs), diagrams, and trade-off analysis.

## Background

You are the lead architect for a startup building a collaborative document editing platform. The business team has provided high-level requirements (see `requirements.md`), but many technical decisions are yours to make. Your architecture will guide the engineering team's implementation over the next 12 months.

The architecture must balance multiple concerns: real-time performance, scalability, cost, development velocity, and operational complexity. There is no single "correct" solution - multiple valid architectural approaches exist, each with different trade-offs.

## Requirements

### Functional Requirements

1. Design a complete system architecture addressing all requirements in `requirements.md`
2. Create Architecture Decision Records (ADRs) for major technical decisions
3. Produce architectural diagrams showing system components and interactions
4. Document trade-offs and alternatives considered
5. Justify technology and design choices with clear reasoning

### Technical Constraints

- Must support 100,000 concurrent users at peak
- Must achieve <100ms P95 latency for same-region real-time edits
- Must provide 99.9% availability
- Must be cloud-native and horizontally scalable
- Must comply with SOC 2, GDPR, CCPA requirements
- Must support multi-region deployment

### Quality Requirements

- ADRs must follow a consistent format with clear reasoning
- Diagrams must be readable and show key components and data flows
- Trade-off analysis must consider at least 2-3 alternatives per major decision
- Architecture must be technically sound and feasible
- All claims and design choices must be justified

## Success Criteria

The architecture will be considered successful when:

1. All major architectural decisions are documented with clear rationale
2. Diagrams clearly communicate system structure and interactions
3. Trade-offs are explicitly analyzed with pros/cons of alternatives
4. Technology choices are appropriate for stated requirements
5. The architecture is feasible, scalable, and addresses all requirements

## Deliverables

Create the following files in the working directory:

### 1. architecture.md
A comprehensive architecture overview document containing:
- Executive summary of architectural approach
- High-level system overview
- Component breakdown with responsibilities
- Data flow descriptions
- Technology stack with justifications
- Scalability strategy
- Security and compliance approach
- Operational considerations (monitoring, deployment, disaster recovery)
- Migration and rollout strategy

### 2. adrs/ directory
Create 3-5 Architecture Decision Records in `adrs/` directory. Each ADR should follow this format:

```markdown
# ADR-XXX: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue we're trying to solve? What are the constraints?]

## Decision
[What did we decide? Be specific and concrete.]

## Consequences
[What are the positive and negative consequences of this decision?]

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

## Alternatives Considered
[What other options did we evaluate? Why did we reject them?]

### Alternative 1: [Name]
- Description: [Brief description]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Reason for rejection: [Why we didn't choose this]

### Alternative 2: [Name]
- Description: [Brief description]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Reason for rejection: [Why we didn't choose this]
```

Suggested ADR topics (choose 3-5 most critical):
- Real-time collaboration strategy (OT vs CRDT)
- Database selection for document storage
- Real-time communication protocol
- Multi-region deployment strategy
- Microservices vs monolith architecture
- Caching strategy
- Search infrastructure approach
- Authentication and authorization approach

### 3. diagrams/ directory
Create text-based diagrams (Mermaid, PlantUML, or ASCII art) in `diagrams/` directory:

**Required diagrams:**
- `component-diagram.md` - High-level component architecture showing major services/components and their relationships
- `deployment-diagram.md` - Deployment architecture showing how components are deployed across infrastructure (regions, availability zones, etc.)
- `data-flow-diagram.md` - How data flows through the system for key use cases (e.g., real-time edit, document load)

**Optional diagrams:**
- Sequence diagrams for critical operations
- Database schema or data model
- Network architecture
- Authentication flow

### 4. trade-offs.md
A document analyzing key architectural trade-offs:
- Summary of major trade-offs in the architecture
- For each significant decision, document:
  - What alternatives were considered
  - Criteria used to evaluate alternatives
  - Why the chosen approach was selected
  - What we're sacrificing and what we're gaining
  - Risk mitigation for the chosen approach
  - Potential future re-evaluation triggers

## Evaluation

Your submission will be scored on:

- **ADR Quality (30%)**: Clarity of reasoning, consideration of alternatives, proper format, technical accuracy
- **Diagram Completeness (20%)**: Coverage of key components, readability, appropriate level of detail
- **Trade-off Analysis (25%)**: Depth of analysis, consideration of alternatives, realistic assessment of pros/cons
- **Technical Soundness (25%)**: Feasibility of architecture, appropriate technology choices, addresses all requirements, scalability and reliability considerations

See `verification/verify.sh` for automated scoring implementation.

## Important Notes

- There is no single "correct" architecture - multiple valid solutions exist
- Focus on explaining your reasoning and trade-offs clearly
- Be specific and concrete in your decisions - avoid vague statements
- Consider real-world constraints: cost, complexity, time-to-market, team expertise
- Your architecture should be implementable by a real engineering team
- Don't over-engineer, but don't under-estimate complexity either

## Getting Started

1. Read `requirements.md` carefully to understand business and technical requirements
2. Identify the most critical architectural decisions that need to be made
3. Research options and trade-offs for each decision area
4. Create ADRs for your major decisions
5. Design the overall system architecture
6. Create diagrams to visualize your architecture
7. Document trade-offs and rationale
8. Review for completeness and technical soundness
