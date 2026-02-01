# Prototyping-001: File Sync CLI Tool

This benchmark evaluates an AI's ability to quickly build proof-of-concept prototypes to validate technical feasibility.

## Objective

Build a minimal working CLI tool that demonstrates real-time file watching and cloud synchronization capabilities. This tests the AI's ability to:
- Rapidly build working demos
- Answer technical feasibility questions through code
- Keep implementations simple and focused
- Prioritize demonstration over production quality

## Technical Question

**Can we build a CLI tool that watches local files and syncs them to cloud storage in real-time?**

The AI must create a working prototype that proves this concept is technically feasible.

## What Makes This Challenging

Unlike production coding tasks, prototyping requires different skills:
- **Speed over perfection**: Quick iterations, not comprehensive features
- **Demonstration over documentation**: Show it works, don't over-document
- **Simplicity over architecture**: Minimal code, minimal abstractions
- **Feasibility over completeness**: Prove the concept, don't build everything

## Task Requirements

The AI must build:

1. **File Watching**: Monitor a directory for file changes (create, modify, delete)
2. **Simulated Cloud Sync**: Mock cloud storage operations (no real API needed)
3. **CLI Interface**: Command-line tool to start/stop watching
4. **Status Output**: Show what's happening in real-time

### Constraints

- Python 3.7+
- Minimal dependencies (prefer standard library)
- Works on Unix-like systems
- Should be buildable in 20-30 minutes
- Can mock/simulate the cloud backend

## Deliverables

1. Python script(s) implementing the tool
2. README.md with usage instructions
3. requirements.txt (if dependencies needed)
4. Working demo that can be executed

## Evaluation Criteria

The submission is scored on:

- **Demo Works** (40%): Can execute and demonstrates file watching + sync
- **Answers Question** (30%): Proves the concept is technically feasible
- **Simplicity** (20%): Low lines of code, minimal complexity
- **Time to Working** (10%): Bonus for quick, iterative development

### Scoring Details

**Demo Works (40%)**:
- Script is executable
- File watching actually works
- Sync operations occur (even if mocked)
- Output shows activity
- Code contains expected functionality

**Answers Question (30%)**:
- Implements file watching mechanism (watchdog library or polling)
- Has sync mechanism (even if mocked)
- CLI interface exists
- Status output is present
- README explains the prototype
- README has usage instructions

**Simplicity (20%)**:
- Low line count (< 100 LOC is excellent, < 200 is good)
- Minimal dependencies (≤ 2 is best)
- Few Python files (≤ 2 files)
- No complex abstractions

**Time Bonus (10%)**:
- Code size suggests quick development
- Working demo suggests successful iteration

### Pass Threshold

- **60% or higher** to pass
- Lower threshold than production benchmarks (prototypes are rough!)

## Running Verification

```bash
cd /Users/kperko/code/evals-for-coding/benchmarks/prototyping-001
./verification/verify.sh
```

The verification script:
1. Checks for required files
2. Installs dependencies
3. Tests demo functionality
4. Validates feasibility demonstration
5. Analyzes code simplicity
6. Outputs JSON scoring

## Example Success

A successful prototype might:
- Use `watchdog` library for file monitoring
- Store "synced" files in a local directory to simulate cloud
- Print status messages when files change
- Be ~80 lines of simple Python code
- Take 15-20 minutes to build

## Common Pitfalls

- **Over-engineering**: Building too many features
- **Over-documentation**: Spending time on docs instead of code
- **Complexity**: Using advanced patterns when simple code works
- **No demo**: Code exists but doesn't actually run
- **Missing the point**: Building perfect code instead of proving feasibility

## Philosophy

This benchmark tests rapid prototyping skills, not production engineering. The goal is to quickly answer "Can this be done?" with a working demo, not to build a production-ready system.

Think of it as a technical spike or proof-of-concept, not a feature release.

## Files

- `technical_question.md`: The feasibility question to answer
- `spec.md`: Detailed task specification
- `prompts.txt`: Standard prompts for AI agents
- `verification/verify.sh`: Automated scoring script
- `verification/test_demo.sh`: Demo functionality test
