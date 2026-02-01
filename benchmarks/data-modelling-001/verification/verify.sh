#!/bin/bash

# Verification script for data-modelling-001 benchmark
# Scores the AI's database schema design

set -e

BENCHMARK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERIFICATION_DIR="$BENCHMARK_DIR/verification"
TESTS_DIR="$VERIFICATION_DIR/tests"

# Initialize scores
TOTAL_SCORE=0
MAX_SCORE=100

# Score components
SCHEMA_VALIDITY_SCORE=0
SCHEMA_VALIDITY_MAX=30

RELATIONSHIPS_SCORE=0
RELATIONSHIPS_MAX=25

CONSTRAINTS_SCORE=0
CONSTRAINTS_MAX=20

MIGRATIONS_SCORE=0
MIGRATIONS_MAX=15

INDEXES_SCORE=0
INDEXES_MAX=10

# Change to benchmark directory
cd "$BENCHMARK_DIR"

# Check if models.py exists
if [ ! -f "$BENCHMARK_DIR/models.py" ]; then
    echo "Error: models.py not found" >&2
    cat <<EOF
{
  "score": 0,
  "max_score": $MAX_SCORE,
  "test_passed": false,
  "details": {
    "error": "Missing models.py file",
    "schema_validity": {
      "score": 0,
      "max_score": $SCHEMA_VALIDITY_MAX,
      "feedback": "Required file models.py not found"
    },
    "relationships": {
      "score": 0,
      "max_score": $RELATIONSHIPS_MAX,
      "feedback": "Cannot test without models.py"
    },
    "constraints": {
      "score": 0,
      "max_score": $CONSTRAINTS_MAX,
      "feedback": "Cannot test without models.py"
    },
    "migrations": {
      "score": 0,
      "max_score": $MIGRATIONS_MAX,
      "feedback": "Cannot test without models.py"
    },
    "indexes": {
      "score": 0,
      "max_score": $INDEXES_MAX,
      "feedback": "Cannot test without models.py"
    }
  }
}
EOF
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "$BENCHMARK_DIR/requirements.txt" ]; then
    pip install -q -r "$BENCHMARK_DIR/requirements.txt" > /dev/null 2>&1 || true
fi

# Function to run pytest and capture results
run_test_suite() {
    local test_file=$1
    local output_file=$(mktemp)

    if python3 -m pytest "$test_file" -v --tb=short > "$output_file" 2>&1; then
        echo "passed"
    else
        echo "failed"
    fi

    cat "$output_file"
    rm "$output_file"
}

# --- TEST SCHEMA VALIDITY (30 points) ---
echo "Testing schema validity..." >&2
SCHEMA_OUTPUT=$(mktemp)
if python3 -m pytest "$TESTS_DIR/test_schema.py" -v --tb=short > "$SCHEMA_OUTPUT" 2>&1; then
    SCHEMA_VALIDITY_SCORE=$SCHEMA_VALIDITY_MAX
    SCHEMA_FEEDBACK="All schema tests passed. Models are well-defined."
else
    # Count passed vs failed tests
    PASSED=$(grep -c "PASSED" "$SCHEMA_OUTPUT" || echo "0")
    FAILED=$(grep -c "FAILED" "$SCHEMA_OUTPUT" || echo "0")
    TOTAL_TESTS=$((PASSED + FAILED))

    if [ $TOTAL_TESTS -gt 0 ]; then
        SCHEMA_VALIDITY_SCORE=$(echo "scale=0; $SCHEMA_VALIDITY_MAX * $PASSED / $TOTAL_TESTS" | bc)
    fi

    SCHEMA_FEEDBACK="Schema tests: $PASSED passed, $FAILED failed. Check model definitions."
fi

# --- TEST RELATIONSHIPS (25 points) ---
echo "Testing relationships..." >&2
RELATIONSHIPS_OUTPUT=$(mktemp)
if python3 -m pytest "$TESTS_DIR/test_relationships.py" -v --tb=short > "$RELATIONSHIPS_OUTPUT" 2>&1; then
    RELATIONSHIPS_SCORE=$RELATIONSHIPS_MAX
    RELATIONSHIPS_FEEDBACK="All relationship tests passed. Bidirectional relationships work correctly."
else
    PASSED=$(grep -c "PASSED" "$RELATIONSHIPS_OUTPUT" || echo "0")
    FAILED=$(grep -c "FAILED" "$RELATIONSHIPS_OUTPUT" || echo "0")
    TOTAL_TESTS=$((PASSED + FAILED))

    if [ $TOTAL_TESTS -gt 0 ]; then
        RELATIONSHIPS_SCORE=$(echo "scale=0; $RELATIONSHIPS_MAX * $PASSED / $TOTAL_TESTS" | bc)
    fi

    RELATIONSHIPS_FEEDBACK="Relationship tests: $PASSED passed, $FAILED failed. Check relationship definitions."
fi

# --- TEST CONSTRAINTS (20 points) ---
echo "Testing constraints..." >&2
CONSTRAINTS_OUTPUT=$(mktemp)
if python3 -m pytest "$TESTS_DIR/test_constraints.py" -v --tb=short > "$CONSTRAINTS_OUTPUT" 2>&1; then
    CONSTRAINTS_SCORE=$CONSTRAINTS_MAX
    CONSTRAINTS_FEEDBACK="All constraint tests passed. Data integrity is properly enforced."
else
    PASSED=$(grep -c "PASSED" "$CONSTRAINTS_OUTPUT" || echo "0")
    FAILED=$(grep -c "FAILED" "$CONSTRAINTS_OUTPUT" || echo "0")
    TOTAL_TESTS=$((PASSED + FAILED))

    if [ $TOTAL_TESTS -gt 0 ]; then
        CONSTRAINTS_SCORE=$(echo "scale=0; $CONSTRAINTS_MAX * $PASSED / $TOTAL_TESTS" | bc)
    fi

    CONSTRAINTS_FEEDBACK="Constraint tests: $PASSED passed, $FAILED failed. Check unique/not-null/FK constraints."
fi

# --- TEST MIGRATIONS (15 points) ---
echo "Testing migrations..." >&2
MIGRATIONS_OUTPUT=$(mktemp)
if python3 -m pytest "$TESTS_DIR/test_migrations.py" -v --tb=short > "$MIGRATIONS_OUTPUT" 2>&1; then
    MIGRATIONS_SCORE=$MIGRATIONS_MAX
    MIGRATIONS_FEEDBACK="All migration tests passed. Alembic setup is correct."
else
    PASSED=$(grep -c "PASSED" "$MIGRATIONS_OUTPUT" || echo "0")
    FAILED=$(grep -c "FAILED" "$MIGRATIONS_OUTPUT" || echo "0")
    SKIPPED=$(grep -c "SKIPPED" "$MIGRATIONS_OUTPUT" || echo "0")
    TOTAL_TESTS=$((PASSED + FAILED))

    if [ $TOTAL_TESTS -gt 0 ]; then
        MIGRATIONS_SCORE=$(echo "scale=0; $MIGRATIONS_MAX * $PASSED / $TOTAL_TESTS" | bc)
    fi

    MIGRATIONS_FEEDBACK="Migration tests: $PASSED passed, $FAILED failed, $SKIPPED skipped. Check Alembic configuration."
fi

# --- TEST INDEXES (10 points) ---
echo "Testing indexes..." >&2
INDEXES_OUTPUT=$(mktemp)
if python3 -m pytest "$TESTS_DIR/test_indexes.py" -v --tb=short > "$INDEXES_OUTPUT" 2>&1; then
    INDEXES_SCORE=$INDEXES_MAX
    INDEXES_FEEDBACK="All index tests passed. Query performance is optimized."
else
    PASSED=$(grep -c "PASSED" "$INDEXES_OUTPUT" || echo "0")
    FAILED=$(grep -c "FAILED" "$INDEXES_OUTPUT" || echo "0")
    SKIPPED=$(grep -c "SKIPPED" "$INDEXES_OUTPUT" || echo "0")
    TOTAL_TESTS=$((PASSED + FAILED))

    if [ $TOTAL_TESTS -gt 0 ]; then
        INDEXES_SCORE=$(echo "scale=0; $INDEXES_MAX * $PASSED / $TOTAL_TESTS" | bc)
    fi

    INDEXES_FEEDBACK="Index tests: $PASSED passed, $FAILED failed, $SKIPPED skipped. Add indexes for common queries."
fi

# Calculate total score
TOTAL_SCORE=$((SCHEMA_VALIDITY_SCORE + RELATIONSHIPS_SCORE + CONSTRAINTS_SCORE + MIGRATIONS_SCORE + INDEXES_SCORE))

# Determine pass/fail
TEST_PASSED="false"
if [ $TOTAL_SCORE -ge 70 ]; then
    TEST_PASSED="true"
fi

# Clean up temp files
rm -f "$SCHEMA_OUTPUT" "$RELATIONSHIPS_OUTPUT" "$CONSTRAINTS_OUTPUT" "$MIGRATIONS_OUTPUT" "$INDEXES_OUTPUT"

# Get detailed test output for JSON
SCHEMA_TESTS=$(python3 -m pytest "$TESTS_DIR/test_schema.py" -v --tb=line 2>&1 | tail -30 | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g' || echo "Error running tests")
RELATIONSHIP_TESTS=$(python3 -m pytest "$TESTS_DIR/test_relationships.py" -v --tb=line 2>&1 | tail -30 | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g' || echo "Error running tests")
CONSTRAINT_TESTS=$(python3 -m pytest "$TESTS_DIR/test_constraints.py" -v --tb=line 2>&1 | tail -30 | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g' || echo "Error running tests")
MIGRATION_TESTS=$(python3 -m pytest "$TESTS_DIR/test_migrations.py" -v --tb=line 2>&1 | tail -30 | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g' || echo "Error running tests")
INDEX_TESTS=$(python3 -m pytest "$TESTS_DIR/test_indexes.py" -v --tb=line 2>&1 | tail -30 | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g' || echo "Error running tests")

# Output JSON result
cat <<EOF
{
  "score": $TOTAL_SCORE,
  "max_score": $MAX_SCORE,
  "test_passed": $TEST_PASSED,
  "details": {
    "schema_validity": {
      "score": $SCHEMA_VALIDITY_SCORE,
      "max_score": $SCHEMA_VALIDITY_MAX,
      "feedback": "$SCHEMA_FEEDBACK",
      "test_output": "$SCHEMA_TESTS"
    },
    "relationships": {
      "score": $RELATIONSHIPS_SCORE,
      "max_score": $RELATIONSHIPS_MAX,
      "feedback": "$RELATIONSHIPS_FEEDBACK",
      "test_output": "$RELATIONSHIP_TESTS"
    },
    "constraints": {
      "score": $CONSTRAINTS_SCORE,
      "max_score": $CONSTRAINTS_MAX,
      "feedback": "$CONSTRAINTS_FEEDBACK",
      "test_output": "$CONSTRAINT_TESTS"
    },
    "migrations": {
      "score": $MIGRATIONS_SCORE,
      "max_score": $MIGRATIONS_MAX,
      "feedback": "$MIGRATIONS_FEEDBACK",
      "test_output": "$MIGRATION_TESTS"
    },
    "indexes": {
      "score": $INDEXES_SCORE,
      "max_score": $INDEXES_MAX,
      "feedback": "$INDEXES_FEEDBACK",
      "test_output": "$INDEX_TESTS"
    }
  }
}
EOF

exit 0
