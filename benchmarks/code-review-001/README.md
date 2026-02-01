# Code Review Benchmark (code-review-001)

This benchmark evaluates an AI's ability to perform thorough code review and identify bugs, security vulnerabilities, and code quality issues.

## Overview

The AI is presented with a Pull Request containing a new user management module. The code includes a realistic mix of:
- **11 planted bugs** across different categories
- **Correct implementations** to test for false positives

The AI must identify issues, classify their severity, and provide actionable feedback.

## Directory Structure

```
code-review-001/
├── README.md                      # This file
├── spec.md                        # Task specification given to the AI
├── prompts.txt                    # Standard prompts for the AI
├── starter-code/                  # Code to review
│   ├── user_manager.py           # Python module with planted bugs
│   └── PR_DIFF.md                # Pull request description
└── verification/                  # Scoring scripts
    ├── verify.sh                 # Main verification script
    └── PLANTED_BUGS.md          # Reference list of all bugs
```

## Bug Categories

The benchmark includes realistic bugs that could slip through code review:

### Critical (3 bugs)
- Hardcoded API keys/secrets
- SQL injection vulnerabilities

### High (5 bugs)
- Off-by-one errors
- Resource leaks (file handles, cursors)
- Logic errors (wrong operators)
- Race conditions

### Medium (3 bugs)
- Performance issues (N+1 queries)
- Missing error handling
- Division by zero risks

## Scoring System

Your review is scored on four components:

1. **Bug Detection (40%)**: Percentage of actual bugs found
2. **False Positive Penalty (20%)**: Starting at 40 points, minus 5 per false positive
3. **Severity Accuracy (20%)**: Percentage of bugs with correct severity classification
4. **Feedback Quality (20%)**: Whether suggestions are specific and actionable

Total possible score: 100 points

## Usage

1. Review the code in `starter-code/user_manager.py`
2. Create a review report (as `review.md`, `code_review.md`, or `output.md`)
3. Run verification: `./verification/verify.sh`

## Expected Output Format

Each issue should follow this format:

```markdown
## Issue [N]: [Brief Title]
- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
- **Location**: Line [number]
- **Description**: [What's wrong]
- **Impact**: [What could happen]
- **Suggestion**: [How to fix it]
```

## Verification

The verification script:
- Extracts line numbers mentioned in the review
- Checks which bugs were found
- Counts false positives (flagging correct code)
- Validates severity classifications
- Assesses feedback quality
- Outputs detailed JSON scoring

See `verification/PLANTED_BUGS.md` for the complete list of planted bugs used for verification.
