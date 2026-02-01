#!/bin/bash
# Architecture Benchmark Verification Script
# Outputs JSON with scoring details using LLM-as-judge evaluation

set -e

BENCHMARK_NAME="architecture-001"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBMISSION_DIR="${1:-.}"

echo "Running verification for ${BENCHMARK_NAME}..." >&2
echo "Submission directory: ${SUBMISSION_DIR}" >&2

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not found" >&2
    exit 1
fi

# Check if required files exist (basic validation)
echo "Checking required files..." >&2

required_files=(
    "architecture.md"
    "trade-offs.md"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "${SUBMISSION_DIR}/${file}" ]; then
        missing_files+=("$file")
    fi
done

required_dirs=(
    "adrs"
    "diagrams"
)

for dir in "${required_dirs[@]}"; do
    if [ ! -d "${SUBMISSION_DIR}/${dir}" ]; then
        missing_files+=("$dir/")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "Error: Missing required files/directories:" >&2
    printf '  - %s\n' "${missing_files[@]}" >&2
    echo "" >&2
    echo "Required deliverables:" >&2
    echo "  - architecture.md" >&2
    echo "  - adrs/ directory with ADR files" >&2
    echo "  - diagrams/ directory with diagram files" >&2
    echo "  - trade-offs.md" >&2

    # Output minimal JSON for failure
    cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "components": {
    "adr_quality": {"score": 0, "weight": 0.30, "details": "ADRs directory missing or empty"},
    "diagram_completeness": {"score": 0, "weight": 0.20, "details": "Diagrams directory missing"},
    "tradeoff_analysis": {"score": 0, "weight": 0.25, "details": "trade-offs.md missing"},
    "technical_soundness": {"score": 0, "weight": 0.25, "details": "architecture.md missing"}
  },
  "base_score": 0,
  "penalties": {
    "time_penalty": 0.0,
    "iteration_penalty": 0.0,
    "error_penalty": 0.0
  },
  "final_score": 0,
  "passed": false
}
EOF
    exit 1
fi

echo "All required files/directories present" >&2

# Check for Python dependencies (anthropic package)
echo "Checking Python dependencies..." >&2
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo "Warning: anthropic package not installed. Install with: pip install anthropic" >&2
    echo "Evaluation will use fallback scoring without LLM judge." >&2
fi

# Run the Python evaluation script
echo "Running LLM-as-judge evaluation..." >&2
python3 "${SCRIPT_DIR}/evaluate_architecture.py" "${SUBMISSION_DIR}"
