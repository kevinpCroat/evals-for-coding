#!/bin/bash

# Code Review Benchmark Verification Script
# Scores AI's ability to find bugs during code review
# Compatible with Bash 3.2+

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCHMARK_DIR="$(dirname "$SCRIPT_DIR")"

# Expected bugs - line_num:severity:description
BUGS="
15:CRITICAL:Hardcoded API key
26:CRITICAL:SQL injection in authenticate_user
49:HIGH:Off-by-one error skipping first user
63:HIGH:Resource leak - cursor not closed
71:MEDIUM:N+1 query performance issue
84:HIGH:File handle not closed
99:HIGH:Wrong operator (addition instead of multiplication)
102:MEDIUM:Division by zero risk
109:HIGH:Race condition on shared cache
133:MEDIUM:Missing null check / error handling
148:CRITICAL:SQL injection in search_users
"

# Correct code sections that should NOT be flagged
# get_user_by_id (38-40), hash_password (57-59), validate_email (122-124),
# cleanup_old_sessions (137-143), __del__ (157-159), thread.start (117)
CORRECT_LINES="38 39 40 57 58 59 117 122 123 124 137 138 139 140 141 142 143 157 158 159"

# Read the AI's review output
REVIEW_FILE=""
if [ -f "$BENCHMARK_DIR/review.md" ]; then
    REVIEW_FILE="$BENCHMARK_DIR/review.md"
elif [ -f "$BENCHMARK_DIR/code_review.md" ]; then
    REVIEW_FILE="$BENCHMARK_DIR/code_review.md"
elif [ -f "$BENCHMARK_DIR/output.md" ]; then
    REVIEW_FILE="$BENCHMARK_DIR/output.md"
else
    echo '{"score": 0, "max_score": 100, "status": "error", "message": "No review file found. Expected review.md, code_review.md, or output.md"}'
    exit 1
fi

# Extract line numbers mentioned in the review
FOUND_LINES=$(grep -oE "(Line|line|LINE) *:? *[0-9]+" "$REVIEW_FILE" | grep -oE "[0-9]+" | sort -u || true)

# Extract severity text for checking
SEVERITIES_TEXT=$(grep -iE "severity.*:.*\b(critical|high|medium|low)\b" "$REVIEW_FILE" || true)

# Count total bugs
TOTAL_BUGS=$(echo "$BUGS" | grep -c ":" || echo 0)

# Calculate bug detection
BUGS_FOUND=0
CORRECT_SEVERITY=0
FOUND_BUG_LINES=""

for line_num in $FOUND_LINES; do
    # Check if this line matches a known bug
    bug_info=$(echo "$BUGS" | grep "^${line_num}:" || true)
    if [ -n "$bug_info" ]; then
        BUGS_FOUND=$((BUGS_FOUND + 1))
        FOUND_BUG_LINES="$FOUND_BUG_LINES $line_num"

        # Check if severity matches
        expected_severity=$(echo "$bug_info" | cut -d: -f2)
        # Look for the severity near this line number (severity usually comes before line)
        if grep -B2 -i "line.*$line_num" "$REVIEW_FILE" | grep -qi "severity.*$expected_severity"; then
            CORRECT_SEVERITY=$((CORRECT_SEVERITY + 1))
        fi
    fi
done

# Calculate scores
if [ $TOTAL_BUGS -gt 0 ]; then
    DETECTION_RATE=$(awk "BEGIN {printf \"%.2f\", ($BUGS_FOUND * 100) / $TOTAL_BUGS}")
    DETECTION_SCORE=$(awk "BEGIN {printf \"%.2f\", ($BUGS_FOUND * 40) / $TOTAL_BUGS}")
else
    DETECTION_RATE="0.00"
    DETECTION_SCORE="0.00"
fi

# Calculate false positives
FALSE_POSITIVES=0
for line_num in $FOUND_LINES; do
    # Check if this is a correct line
    is_correct=0
    for correct_line in $CORRECT_LINES; do
        if [ "$line_num" = "$correct_line" ]; then
            is_correct=1
            break
        fi
    done

    # Check if this is a known bug
    is_bug=0
    if echo " $FOUND_BUG_LINES " | grep -q " $line_num "; then
        is_bug=1
    fi

    # If flagged a correct line OR flagged a line that's not a known bug
    if [ $is_correct -eq 1 ] || [ $is_bug -eq 0 ]; then
        # Check if it's near a bug (within 2 lines)
        has_nearby_bug=0
        for bug_line in $FOUND_BUG_LINES; do
            diff=$((line_num - bug_line))
            if [ $diff -gt -3 ] && [ $diff -lt 3 ] && [ $diff -ne 0 ]; then
                has_nearby_bug=1
                break
            fi
        done

        if [ $has_nearby_bug -eq 0 ]; then
            FALSE_POSITIVES=$((FALSE_POSITIVES + 1))
        fi
    fi
done

# False positive score
FP_SCORE=$(awk "BEGIN {score = 40 - ($FALSE_POSITIVES * 5); printf \"%.2f\", (score < 0) ? 0 : score}")

# Severity accuracy
if [ $BUGS_FOUND -gt 0 ]; then
    SEVERITY_ACCURACY=$(awk "BEGIN {printf \"%.2f\", ($CORRECT_SEVERITY * 100) / $BUGS_FOUND}")
    SEVERITY_SCORE=$(awk "BEGIN {printf \"%.2f\", ($CORRECT_SEVERITY * 20) / $BUGS_FOUND}")
else
    SEVERITY_ACCURACY="0.00"
    SEVERITY_SCORE="0.00"
fi

# Feedback quality
HAS_DESCRIPTIONS=$(grep -ci "description\|what.*wrong\|issue\|problem" "$REVIEW_FILE" || echo 0)
HAS_IMPACTS=$(grep -ci "impact\|consequence\|could\|risk\|result" "$REVIEW_FILE" || echo 0)
HAS_SUGGESTIONS=$(grep -ci "suggest\|fix\|should\|recommend\|instead" "$REVIEW_FILE" || echo 0)

FEEDBACK_QUALITY=0
[ $HAS_DESCRIPTIONS -ge 5 ] && FEEDBACK_QUALITY=$((FEEDBACK_QUALITY + 7))
[ $HAS_IMPACTS -ge 3 ] && FEEDBACK_QUALITY=$((FEEDBACK_QUALITY + 7))
[ $HAS_SUGGESTIONS -ge 5 ] && FEEDBACK_QUALITY=$((FEEDBACK_QUALITY + 6))

# Total score
TOTAL_SCORE=$(awk "BEGIN {printf \"%.2f\", $DETECTION_SCORE + $FP_SCORE + $SEVERITY_SCORE + $FEEDBACK_QUALITY}")

# Build feedback message
FEEDBACK="Bug Detection: Found $BUGS_FOUND/$TOTAL_BUGS bugs (${DETECTION_RATE}%). "
FEEDBACK="${FEEDBACK}False Positives: $FALSE_POSITIVES flagged. "
FEEDBACK="${FEEDBACK}Severity Accuracy: $CORRECT_SEVERITY/$BUGS_FOUND correct (${SEVERITY_ACCURACY}%)."

# List missed bugs
MISSED_COUNT=0
MISSED_LIST=""
while IFS=: read -r line_num severity description; do
    [ -z "$line_num" ] && continue
    if ! echo " $FOUND_BUG_LINES " | grep -q " $line_num "; then
        MISSED_COUNT=$((MISSED_COUNT + 1))
        MISSED_LIST="${MISSED_LIST}\n  - Line $line_num: $description"
    fi
done <<< "$BUGS"

if [ $MISSED_COUNT -gt 0 ]; then
    FEEDBACK="${FEEDBACK} Missed $MISSED_COUNT bugs:$MISSED_LIST"
fi

# Determine boolean values for JSON
DESC_BOOL=$([ $HAS_DESCRIPTIONS -ge 5 ] && echo "true" || echo "false")
IMP_BOOL=$([ $HAS_IMPACTS -ge 3 ] && echo "true" || echo "false")
SUG_BOOL=$([ $HAS_SUGGESTIONS -ge 5 ] && echo "true" || echo "false")

# Output JSON
cat <<EOF
{
    "score": $TOTAL_SCORE,
    "max_score": 100,
    "status": "completed",
    "message": "$FEEDBACK",
    "breakdown": {
        "bug_detection": {
            "score": $DETECTION_SCORE,
            "max_score": 40,
            "bugs_found": $BUGS_FOUND,
            "total_bugs": $TOTAL_BUGS,
            "detection_rate": "${DETECTION_RATE}%"
        },
        "false_positives": {
            "score": $FP_SCORE,
            "max_score": 40,
            "false_positives": $FALSE_POSITIVES,
            "penalty_per_fp": 5
        },
        "severity_accuracy": {
            "score": $SEVERITY_SCORE,
            "max_score": 20,
            "correct": $CORRECT_SEVERITY,
            "total_found": $BUGS_FOUND,
            "accuracy": "${SEVERITY_ACCURACY}%"
        },
        "feedback_quality": {
            "score": $FEEDBACK_QUALITY,
            "max_score": 20,
            "has_descriptions": $DESC_BOOL,
            "has_impacts": $IMP_BOOL,
            "has_suggestions": $SUG_BOOL
        }
    }
}
EOF
