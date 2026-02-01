# Testing the Architecture-001 Benchmark

## Quick Start

### 1. Review the Example Submission

An example high-quality submission is provided in `verification/example-submission/`:

```bash
cd verification/example-submission
ls -la
```

You'll see:
- `architecture.md` - Comprehensive system architecture
- `adrs/` - Three ADRs covering major decisions
- `diagrams/` - Component, deployment, and data flow diagrams
- `trade-offs.md` - Detailed trade-off analysis

### 2. Run Verification (Basic Mode)

Without the Anthropic API, the verification uses fallback structural analysis:

```bash
cd /path/to/benchmarks/architecture-001
./verification/verify.sh verification/example-submission
```

This checks for:
- Required files present
- ADR structure and sections
- Diagram completeness
- Document length and quality indicators

### 3. Run Verification (LLM-as-Judge Mode)

For more accurate scoring, install the Anthropic SDK and set your API key:

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-api-key-here

./verification/verify.sh verification/example-submission
```

The LLM will evaluate:
- Depth of reasoning in ADRs
- Quality of alternatives analysis
- Technical soundness of architecture
- Completeness of trade-off analysis

## Understanding the Scores

### Scoring Components

1. **ADR Quality (30%)**:
   - Format and structure (20 points)
   - Depth of reasoning (40 points)
   - Alternatives analysis (40 points)

2. **Diagram Completeness (20%)**:
   - Presence of required diagrams (60 points)
   - Content quality and detail (40 points)

3. **Trade-off Analysis (25%)**:
   - Breadth of analysis (30 points)
   - Depth of reasoning (40 points)
   - Critical thinking (30 points)

4. **Technical Soundness (25%)**:
   - Requirements coverage (30 points)
   - Technical feasibility (40 points)
   - Completeness (30 points)

### Passing Score

A submission must score **70/100 or higher** to pass.

### Example Output

```json
{
  "benchmark": "architecture-001",
  "components": {
    "adr_quality": {
      "score": 85,
      "weight": 0.3,
      "details": "Strong reasoning with clear alternatives"
    },
    "diagram_completeness": {
      "score": 90,
      "weight": 0.2,
      "details": "All required diagrams present"
    },
    "tradeoff_analysis": {
      "score": 80,
      "weight": 0.25,
      "details": "Thorough analysis of major decisions"
    },
    "technical_soundness": {
      "score": 88,
      "weight": 0.25,
      "details": "Appropriate technology choices"
    }
  },
  "base_score": 85.15,
  "final_score": 85.15,
  "passed": true
}
```

## Testing Different Quality Levels

### Test Case 1: Minimal Submission (Should Fail)

Create a minimal submission to test failure detection:

```bash
mkdir -p test-submission/{adrs,diagrams}
echo "# Architecture" > test-submission/architecture.md
echo "# ADR-001: Test" > test-submission/adrs/ADR-001-test.md
echo "# Component Diagram" > test-submission/diagrams/component-diagram.md
echo "# Deployment Diagram" > test-submission/diagrams/deployment-diagram.md
echo "# Data Flow Diagram" > test-submission/diagrams/data-flow-diagram.md
echo "# Trade-offs" > test-submission/trade-offs.md

./verification/verify.sh test-submission
```

Expected: Low score (<40), fails validation

### Test Case 2: Missing Files (Should Fail)

```bash
mkdir -p test-submission2
echo "# Architecture" > test-submission2/architecture.md

./verification/verify.sh test-submission2
```

Expected: Error message listing missing files

### Test Case 3: Example Submission (Should Pass with LLM)

```bash
./verification/verify.sh verification/example-submission
```

Expected with LLM: Score 80-95, passes validation
Expected without LLM: Score 60-70, may fail (fallback is conservative)

## Manual Evaluation

To manually review a submission:

1. **Check ADRs**: Read each ADR in `adrs/`
   - Are alternatives clearly presented?
   - Is the reasoning sound?
   - Are pros/cons realistic?

2. **Review Diagrams**: Open each diagram in `diagrams/`
   - Do they show key components?
   - Is the architecture clear?
   - Are relationships documented?

3. **Read Trade-offs**: Review `trade-offs.md`
   - Are major decisions covered?
   - Are sacrifices acknowledged?
   - Is the analysis honest?

4. **Evaluate Architecture**: Review `architecture.md`
   - Does it address requirements?
   - Is it implementable?
   - Are technology choices justified?

## Common Issues

### Issue 1: LLM Evaluation Variance

**Symptom**: Same submission gets different scores across runs

**Cause**: LLM-as-judge has inherent variance (±5 points typical)

**Solution**: Run evaluation 3 times, take average. Variance >10 points indicates evaluation prompt may need tuning.

### Issue 2: Fallback Scores Too Low

**Symptom**: Good submissions fail without LLM evaluation

**Cause**: Fallback scoring is conservative, checking only structure

**Solution**: Use LLM evaluation for accurate scoring. Fallback is for basic validation only.

### Issue 3: API Rate Limits

**Symptom**: Evaluation fails with rate limit error

**Cause**: Anthropic API rate limits

**Solution**: Add retry logic with exponential backoff, or reduce evaluation frequency.

## Debugging

### Enable Verbose Output

```bash
# See detailed evaluation output
./verification/verify.sh verification/example-submission 2>&1 | tee evaluation.log
```

### Test Python Evaluator Directly

```bash
cd verification
python3 evaluate_architecture.py example-submission
```

### Check Dependencies

```bash
python3 -c "import anthropic; print('Anthropic SDK installed')"
python3 -c "import json; print('JSON available')"
```

## Performance

- **Without LLM**: <1 second (structural analysis only)
- **With LLM**: 10-30 seconds (4 API calls for evaluation)
- **Cost**: ~$0.10-0.30 per evaluation (Claude API)

## Maintenance

### Updating Evaluation Criteria

Edit `verification/evaluate_architecture.py`:
- Modify prompts in each `evaluate_*` method
- Adjust weights in `evaluate()` method
- Update scoring thresholds

### Adding New Evaluation Dimensions

1. Add new method to `ArchitectureEvaluator` class
2. Call method in `evaluate()`
3. Add weight to components dictionary
4. Update scoring documentation

### Calibration

To calibrate scoring:
1. Create 5-10 reference submissions (poor to excellent)
2. Have human experts score them (0-100)
3. Run LLM evaluation
4. Adjust prompts to align LLM scores with human scores
5. Validate variance is acceptable (±10 points)
