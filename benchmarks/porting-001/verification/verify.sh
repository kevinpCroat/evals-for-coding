#!/bin/bash
# Porting Benchmark Verification Script
# Scores the ported JavaScript/TypeScript implementation

set -e

BENCHMARK_NAME="porting-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SUBMISSION_DIR="${1:-submission}"

# Initialize scoring variables
tests_passing_score=0
idiomatic_code_score=0
feature_parity_score=0
build_success_score=0

# Component weights
tests_passing_weight=0.50
idiomatic_code_weight=0.20
feature_parity_weight=0.20
build_success_weight=0.10

echo "Running verification for ${BENCHMARK_NAME}..." >&2
echo "Submission directory: ${SUBMISSION_DIR}" >&2

# Check if submission directory exists
if [ ! -d "$SUBMISSION_DIR" ]; then
  echo "Error: Submission directory not found: $SUBMISSION_DIR" >&2

  cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "error": "Submission directory not found",
  "components": {
    "tests_passing": {"score": 0, "weight": ${tests_passing_weight}, "details": "No submission found"},
    "idiomatic_code": {"score": 0, "weight": ${idiomatic_code_weight}, "details": "No submission found"},
    "feature_parity": {"score": 0, "weight": ${feature_parity_weight}, "details": "No submission found"},
    "build_success": {"score": 0, "weight": ${build_success_weight}, "details": "No submission found"}
  },
  "base_score": 0,
  "penalties": {
    "time_penalty": 0,
    "iteration_penalty": 0,
    "error_penalty": 0
  },
  "final_score": 0,
  "passed": false
}
EOF
  exit 1
fi

cd "$SUBMISSION_DIR"

# Component 1: Build Success (10%)
echo "Checking build success..." >&2
build_details="Build not attempted"
if [ -f "package.json" ]; then
  if npm install > /dev/null 2>&1; then
    build_success_score=100
    build_details="npm install successful"
    echo "  ✓ npm install successful" >&2
  else
    build_success_score=0
    build_details="npm install failed"
    echo "  ✗ npm install failed" >&2
  fi
else
  build_success_score=0
  build_details="No package.json found"
  echo "  ✗ No package.json found" >&2
fi

# Component 2: Tests Passing (50%)
echo "Checking tests..." >&2
test_details="Tests not found or not run"
total_tests=0
passed_tests=0

if [ -f "package.json" ] && [ "$build_success_score" -eq 100 ]; then
  # Try to run tests
  if npm test > test_output.txt 2>&1; then
    # Parse Jest output for test results
    if grep -q "Tests:.*passed" test_output.txt; then
      # Extract passed and total tests from Jest output
      passed_tests=$(grep "Tests:" test_output.txt | grep -o "[0-9]* passed" | grep -o "[0-9]*" | head -1 || echo "0")
      total_tests=$(grep "Tests:" test_output.txt | grep -o "[0-9]* total" | grep -o "[0-9]*" || echo "50")

      # If we can't parse, check for test summary
      if [ "$total_tests" = "0" ] || [ -z "$total_tests" ]; then
        total_tests=50  # Expected number of tests
      fi
      if [ "$passed_tests" = "0" ] || [ -z "$passed_tests" ]; then
        passed_tests=$(grep -c "✓" test_output.txt || echo "0")
      fi

      # Calculate score
      if [ "$total_tests" -gt 0 ]; then
        tests_passing_score=$(( (passed_tests * 100) / total_tests ))
      else
        tests_passing_score=100
      fi

      test_details="$passed_tests/$total_tests tests passed"
      echo "  ✓ Tests completed: $test_details" >&2
    else
      tests_passing_score=0
      test_details="Tests ran but results unclear"
      echo "  ⚠ Tests ran but results unclear" >&2
    fi
  else
    # Check if any tests passed even though npm test failed
    if grep -q "passed" test_output.txt 2>/dev/null; then
      passed_tests=$(grep -o "[0-9]* passed" test_output.txt | grep -o "[0-9]*" | head -1 || echo "0")
      failed_tests=$(grep -o "[0-9]* failed" test_output.txt | grep -o "[0-9]*" | head -1 || echo "0")
      total_tests=$((passed_tests + failed_tests))

      if [ "$total_tests" -gt 0 ]; then
        tests_passing_score=$(( (passed_tests * 100) / total_tests ))
        test_details="$passed_tests/$total_tests tests passed (some failures)"
        echo "  ⚠ $test_details" >&2
      fi
    else
      tests_passing_score=0
      test_details="Tests failed to run or all tests failed"
      echo "  ✗ Tests failed" >&2
    fi
  fi

  rm -f test_output.txt
else
  tests_passing_score=0
  test_details="Cannot run tests (build failed or no package.json)"
  echo "  ✗ Cannot run tests" >&2
fi

# Component 3: Feature Parity (20%)
echo "Checking feature parity..." >&2
feature_details="Not checked"
found_features=0
total_features=8

# Check for required functions/exports
if [ -f "textAnalyzer.ts" ] || [ -f "textAnalyzer.js" ]; then
  impl_file="textAnalyzer.ts"
  [ ! -f "$impl_file" ] && impl_file="textAnalyzer.js"

  # Check for TextAnalyzer class
  grep -q "class TextAnalyzer" "$impl_file" && found_features=$((found_features + 1))

  # Check for required functions
  grep -q "tokenize" "$impl_file" && found_features=$((found_features + 1))
  grep -q "charFrequencyAnalysis\|char_frequency_analysis" "$impl_file" && found_features=$((found_features + 1))
  grep -q "findPalindromes\|find_palindromes" "$impl_file" && found_features=$((found_features + 1))
  grep -q "groupByLength\|group_by_length" "$impl_file" && found_features=$((found_features + 1))
  grep -q "calculateReadingMetrics\|calculate_reading_metrics" "$impl_file" && found_features=$((found_features + 1))
  grep -q "extractAcronyms\|extract_acronyms" "$impl_file" && found_features=$((found_features + 1))
  grep -q "titleCaseSpecial\|title_case_special" "$impl_file" && found_features=$((found_features + 1))

  feature_parity_score=$(( (found_features * 100) / total_features ))
  feature_details="$found_features/$total_features required features found"
  echo "  ✓ Feature parity: $feature_details" >&2
else
  feature_parity_score=0
  feature_details="Implementation file not found (textAnalyzer.ts or textAnalyzer.js)"
  echo "  ✗ $feature_details" >&2
fi

# Component 4: Idiomatic Code (20%)
echo "Checking code quality..." >&2
quality_details="Not checked"
quality_checks=0
total_quality_checks=5

if [ -f "textAnalyzer.ts" ] || [ -f "textAnalyzer.js" ]; then
  impl_file="textAnalyzer.ts"
  [ ! -f "$impl_file" ] && impl_file="textAnalyzer.js"

  # Check 1: Uses camelCase (no snake_case in function names)
  if ! grep -q "function [a-z_]*_[a-z_]*\|const [a-z_]*_[a-z_]* =" "$impl_file"; then
    quality_checks=$((quality_checks + 1))
    echo "  ✓ Uses camelCase naming" >&2
  else
    echo "  ✗ Found snake_case naming" >&2
  fi

  # Check 2: Uses const/let (no var)
  if ! grep -q "var " "$impl_file"; then
    quality_checks=$((quality_checks + 1))
    echo "  ✓ No 'var' usage" >&2
  else
    echo "  ✗ Found 'var' usage" >&2
  fi

  # Check 3: Uses modern array methods (map, filter, reduce)
  if grep -q "\.map(\|\.filter(\|\.reduce(" "$impl_file"; then
    quality_checks=$((quality_checks + 1))
    echo "  ✓ Uses array methods" >&2
  else
    echo "  ✗ Doesn't use array methods" >&2
  fi

  # Check 4: Uses arrow functions
  if grep -q "=>" "$impl_file"; then
    quality_checks=$((quality_checks + 1))
    echo "  ✓ Uses arrow functions" >&2
  else
    echo "  ✗ Doesn't use arrow functions" >&2
  fi

  # Check 5: Run ESLint if config exists
  if [ -f ".eslintrc.json" ] || [ -f ".eslintrc.js" ] || [ -f "eslint.config.js" ]; then
    if npx eslint "$impl_file" > /dev/null 2>&1; then
      quality_checks=$((quality_checks + 1))
      echo "  ✓ ESLint passes" >&2
    else
      echo "  ⚠ ESLint has warnings/errors" >&2
    fi
  else
    # Give partial credit if no eslint config
    quality_checks=$((quality_checks + 1))
    echo "  ⚠ No ESLint config (giving benefit of doubt)" >&2
  fi

  idiomatic_code_score=$(( (quality_checks * 100) / total_quality_checks ))
  quality_details="$quality_checks/$total_quality_checks quality checks passed"
else
  idiomatic_code_score=0
  quality_details="No implementation file to check"
fi

# Calculate base score using bc for floating point
base_score=$(echo "$tests_passing_score * $tests_passing_weight + \
                   $idiomatic_code_score * $idiomatic_code_weight + \
                   $feature_parity_score * $feature_parity_weight + \
                   $build_success_score * $build_success_weight" | bc -l)
base_score=$(printf "%.0f" "$base_score")

# Calculate penalties (would come from execution metadata in real scenario)
time_penalty=0
iteration_penalty=0
error_penalty=0

# Calculate final score
penalty_multiplier=$(echo "1.0 - ($time_penalty + $iteration_penalty + $error_penalty)" | bc -l)
final_score=$(echo "$base_score * $penalty_multiplier" | bc -l)
final_score=$(printf "%.0f" "$final_score")

# Determine pass/fail (70% threshold)
passed="false"
if [ "$final_score" -ge 70 ]; then
  passed="true"
fi

echo "" >&2
echo "Final Score: $final_score/100" >&2
echo "Status: $([ "$passed" = "true" ] && echo "PASSED" || echo "FAILED")" >&2

# Output JSON
cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "components": {
    "tests_passing": {
      "score": ${tests_passing_score},
      "weight": ${tests_passing_weight},
      "details": "$test_details"
    },
    "idiomatic_code": {
      "score": ${idiomatic_code_score},
      "weight": ${idiomatic_code_weight},
      "details": "$quality_details"
    },
    "feature_parity": {
      "score": ${feature_parity_score},
      "weight": ${feature_parity_weight},
      "details": "$feature_details"
    },
    "build_success": {
      "score": ${build_success_score},
      "weight": ${build_success_weight},
      "details": "$build_details"
    }
  },
  "base_score": ${base_score},
  "penalties": {
    "time_penalty": ${time_penalty},
    "iteration_penalty": ${iteration_penalty},
    "error_penalty": ${error_penalty}
  },
  "final_score": ${final_score},
  "passed": ${passed}
}
EOF

# Exit with appropriate code
if [ "$passed" = "true" ]; then
  exit 0
else
  exit 1
fi
