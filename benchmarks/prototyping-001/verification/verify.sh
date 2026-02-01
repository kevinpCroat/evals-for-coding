#!/bin/bash
# Prototyping Benchmark Verification Script
# Tests a proof-of-concept file watching + cloud sync CLI tool

set -e

BENCHMARK_NAME="prototyping-001"
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize scoring components
demo_score=0
feasibility_score=0
simplicity_score=0
time_score=0

# Change to project directory
cd "$PROJECT_DIR"

echo -e "${YELLOW}Running Prototyping Benchmark Verification...${NC}" >&2

# 1. CHECK FOR REQUIRED FILES
echo -e "\n${YELLOW}1. Checking for required files...${NC}" >&2

required_files_found=true
missing_files=""

# Check for Python files
if ! ls *.py > /dev/null 2>&1; then
    required_files_found=false
    missing_files="${missing_files}\n  - No Python files found"
fi

# Check for README
if [ ! -f "README.md" ] && [ ! -f "readme.md" ] && [ ! -f "README.txt" ]; then
    required_files_found=false
    missing_files="${missing_files}\n  - README.md"
fi

if [ "$required_files_found" = false ]; then
    echo -e "${RED}ERROR: Missing required files:${missing_files}${NC}" >&2
    cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "error": "Missing required files: ${missing_files}",
  "components": {
    "demo_works": {"score": 0, "weight": 0.40, "details": "Required files missing"},
    "answers_question": {"score": 0, "weight": 0.30, "details": "Required files missing"},
    "simplicity": {"score": 0, "weight": 0.20, "details": "Required files missing"},
    "time_bonus": {"score": 0, "weight": 0.10, "details": "Required files missing"}
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

echo -e "${GREEN}Required files found${NC}" >&2

# 2. INSTALL DEPENDENCIES
echo -e "\n${YELLOW}2. Installing dependencies...${NC}" >&2

if [ -f "requirements.txt" ]; then
    if python3 -m pip install --user -q -r requirements.txt 2>&1 | grep -v "already satisfied" | head -5 >&2; then
        echo -e "${YELLOW}Dependencies installed${NC}" >&2
    fi
else
    echo "No requirements.txt found, assuming standard library only" >&2
fi

# 3. RUN DEMO TEST (40% weight)
echo -e "\n${YELLOW}3. Testing demo functionality...${NC}" >&2

demo_checks_passed=0
demo_checks_total=8

# Create test directory
TEST_DIR="$PROJECT_DIR/test_watch_dir_$$"
mkdir -p "$TEST_DIR"

# Find main script
MAIN_SCRIPT=""
for file in sync_tool.py file_sync.py watcher.py main.py watch.py app.py; do
    if [ -f "$file" ]; then
        MAIN_SCRIPT="$file"
        break
    fi
done

if [ -z "$MAIN_SCRIPT" ]; then
    # Try to find any Python file
    MAIN_SCRIPT=$(ls *.py 2>/dev/null | head -1)
fi

if [ -z "$MAIN_SCRIPT" ]; then
    echo -e "${RED}ERROR: Could not find main Python script${NC}" >&2
    demo_score=0
    demo_details="No main script found"
else
    echo "Found main script: $MAIN_SCRIPT" >&2

    # Check 1: Script is executable/runnable
    if python3 "$MAIN_SCRIPT" --help > /dev/null 2>&1 || python3 "$MAIN_SCRIPT" -h > /dev/null 2>&1 || python3 "$MAIN_SCRIPT" > /dev/null 2>&1; then
        demo_checks_passed=$((demo_checks_passed + 1))
        echo "  ✓ Script is executable" >&2
    else
        echo "  ✗ Script not executable or has errors" >&2
    fi

    # Check 2: Can start watching (run test_demo.sh)
    if [ -f "$SCRIPT_DIR/test_demo.sh" ]; then
        if bash "$SCRIPT_DIR/test_demo.sh" > demo_test.log 2>&1; then
            demo_checks_passed=$((demo_checks_passed + 3))
            echo "  ✓ Demo test passed (file watching works)" >&2

            # Check if output shows expected behavior
            if grep -qiE "(watching|monitor|sync|upload|created|modified)" demo_test.log; then
                demo_checks_passed=$((demo_checks_passed + 1))
                echo "  ✓ Output shows file watching activity" >&2
            else
                echo "  ✗ Output doesn't show expected activity" >&2
            fi

            if grep -qiE "(sync|upload|cloud|backup)" demo_test.log; then
                demo_checks_passed=$((demo_checks_passed + 1))
                echo "  ✓ Output shows sync operations" >&2
            else
                echo "  ✗ Output doesn't show sync operations" >&2
            fi
        else
            echo "  ✗ Demo test failed (check demo_test.log)" >&2
            tail -20 demo_test.log >&2 || true
        fi
    else
        echo "  ⚠ test_demo.sh not found, running basic test" >&2

        # Basic test: start watcher in background, make changes, check output
        timeout 5 python3 "$MAIN_SCRIPT" watch "$TEST_DIR" > watcher_output.log 2>&1 &
        WATCHER_PID=$!
        sleep 2

        # Make a test file
        echo "test content" > "$TEST_DIR/test_file.txt"
        sleep 1

        # Check if watcher detected it
        if grep -qiE "(test_file|created|sync|upload)" watcher_output.log; then
            demo_checks_passed=$((demo_checks_passed + 2))
            echo "  ✓ Detected file creation" >&2
        else
            echo "  ✗ Did not detect file creation" >&2
        fi

        kill $WATCHER_PID 2>/dev/null || true
    fi

    # Check 3: Code structure suggests file watching
    if grep -qiE "(watch|observer|monitor|poll)" "$MAIN_SCRIPT"; then
        demo_checks_passed=$((demo_checks_passed + 1))
        echo "  ✓ Code contains file watching logic" >&2
    else
        echo "  ✗ No file watching logic found" >&2
    fi

    # Check 4: Code suggests sync operations
    if grep -qiE "(sync|upload|cloud|copy|backup)" "$MAIN_SCRIPT"; then
        demo_checks_passed=$((demo_checks_passed + 1))
        echo "  ✓ Code contains sync operations" >&2
    else
        echo "  ✗ No sync operations found" >&2
    fi

    demo_score=$(python3 -c "print(int(($demo_checks_passed / $demo_checks_total) * 100))")
    demo_details="Passed ${demo_checks_passed}/${demo_checks_total} demo checks"
    echo -e "${GREEN}Demo functionality: ${demo_checks_passed}/${demo_checks_total}${NC}" >&2
fi

# Cleanup test directory
rm -rf "$TEST_DIR" 2>/dev/null || true

# 4. CHECK IF IT ANSWERS THE FEASIBILITY QUESTION (30% weight)
echo -e "\n${YELLOW}4. Checking if prototype answers feasibility question...${NC}" >&2

feasibility_checks_passed=0
feasibility_checks_total=6

# Check 1: Implements file watching
if grep -qiE "(watchdog|Observer|inotify|kqueue|watch.*event|FileSystemEventHandler)" "$MAIN_SCRIPT" *.py 2>/dev/null; then
    feasibility_checks_passed=$((feasibility_checks_passed + 1))
    echo "  ✓ Uses proper file watching mechanism" >&2
elif grep -qiE "(os\.stat|os\.listdir|time\.sleep.*while)" "$MAIN_SCRIPT" *.py 2>/dev/null; then
    feasibility_checks_passed=$((feasibility_checks_passed + 1))
    echo "  ✓ Uses polling-based file watching" >&2
else
    echo "  ✗ No clear file watching implementation" >&2
fi

# Check 2: Has sync mechanism (even if mocked)
if grep -qiE "(def.*sync|class.*Sync|upload|cloud|backend)" "$MAIN_SCRIPT" *.py 2>/dev/null; then
    feasibility_checks_passed=$((feasibility_checks_passed + 1))
    echo "  ✓ Has sync mechanism implemented" >&2
else
    echo "  ✗ No sync mechanism found" >&2
fi

# Check 3: CLI interface exists
if grep -qiE "(argparse|sys\.argv|click|if __name__|def main)" "$MAIN_SCRIPT" *.py 2>/dev/null; then
    feasibility_checks_passed=$((feasibility_checks_passed + 1))
    echo "  ✓ Has CLI interface" >&2
else
    echo "  ✗ No CLI interface found" >&2
fi

# Check 4: Status/logging output
if grep -qiE "(print\(|logging\.|logger\.|sys\.stdout)" "$MAIN_SCRIPT" *.py 2>/dev/null; then
    feasibility_checks_passed=$((feasibility_checks_passed + 1))
    echo "  ✓ Has status output" >&2
else
    echo "  ✗ No status output found" >&2
fi

# Check 5: README explains what it demonstrates
README_FILE=$(ls README.md readme.md README.txt 2>/dev/null | head -1)
if [ ! -z "$README_FILE" ] && grep -qiE "(demo|prototype|feasibility|proof|concept)" "$README_FILE"; then
    feasibility_checks_passed=$((feasibility_checks_passed + 1))
    echo "  ✓ README explains prototype purpose" >&2
else
    echo "  ✗ README doesn't explain prototype purpose" >&2
fi

# Check 6: README has usage instructions
if [ ! -z "$README_FILE" ] && grep -qiE "(usage|how to|run|example|demo)" "$README_FILE"; then
    feasibility_checks_passed=$((feasibility_checks_passed + 1))
    echo "  ✓ README has usage instructions" >&2
else
    echo "  ✗ README missing usage instructions" >&2
fi

feasibility_score=$(python3 -c "print(int(($feasibility_checks_passed / $feasibility_checks_total) * 100))")
feasibility_details="Passed ${feasibility_checks_passed}/${feasibility_checks_total} feasibility checks"
echo -e "${GREEN}Feasibility demonstration: ${feasibility_checks_passed}/${feasibility_checks_total}${NC}" >&2

# 5. CHECK SIMPLICITY (20% weight)
echo -e "\n${YELLOW}5. Analyzing simplicity...${NC}" >&2

simplicity_checks_passed=0
simplicity_checks_total=5

# Count total lines of code (excluding comments and blank lines)
TOTAL_LOC=$(find . -name "*.py" -not -path "./verification/*" -exec grep -vE "^\s*#|^\s*$" {} \; 2>/dev/null | wc -l | tr -d ' ')

# Check 1: Low line count (under 200 lines is excellent for a prototype)
if [ "$TOTAL_LOC" -lt 100 ]; then
    simplicity_checks_passed=$((simplicity_checks_passed + 2))
    echo "  ✓ Very simple implementation ($TOTAL_LOC LOC)" >&2
elif [ "$TOTAL_LOC" -lt 200 ]; then
    simplicity_checks_passed=$((simplicity_checks_passed + 1))
    echo "  ✓ Simple implementation ($TOTAL_LOC LOC)" >&2
else
    echo "  ⚠ Somewhat complex implementation ($TOTAL_LOC LOC)" >&2
fi

# Check 2: Minimal dependencies
if [ -f "requirements.txt" ]; then
    DEP_COUNT=$(grep -vE "^\s*#|^\s*$" requirements.txt | wc -l | tr -d ' ')
    if [ "$DEP_COUNT" -le 2 ]; then
        simplicity_checks_passed=$((simplicity_checks_passed + 1))
        echo "  ✓ Minimal dependencies ($DEP_COUNT)" >&2
    else
        echo "  ⚠ Several dependencies ($DEP_COUNT)" >&2
    fi
else
    simplicity_checks_passed=$((simplicity_checks_passed + 1))
    echo "  ✓ No external dependencies" >&2
fi

# Check 3: Single or few files
FILE_COUNT=$(find . -name "*.py" -not -path "./verification/*" | wc -l | tr -d ' ')
if [ "$FILE_COUNT" -le 2 ]; then
    simplicity_checks_passed=$((simplicity_checks_passed + 1))
    echo "  ✓ Few Python files ($FILE_COUNT)" >&2
else
    echo "  ⚠ Multiple Python files ($FILE_COUNT)" >&2
fi

# Check 4: No complex abstractions
if ! grep -qE "(abstract|metaclass|@decorator|Protocol|TypeVar)" *.py 2>/dev/null; then
    simplicity_checks_passed=$((simplicity_checks_passed + 1))
    echo "  ✓ No complex abstractions" >&2
else
    echo "  ⚠ Uses complex abstractions" >&2
fi

simplicity_score=$(python3 -c "print(int(($simplicity_checks_passed / $simplicity_checks_total) * 100))")
simplicity_details="Passed ${simplicity_checks_passed}/${simplicity_checks_total} simplicity checks (${TOTAL_LOC} LOC)"
echo -e "${GREEN}Simplicity: ${simplicity_checks_passed}/${simplicity_checks_total}${NC}" >&2

# 6. TIME BONUS (10% weight)
echo -e "\n${YELLOW}6. Evaluating development approach...${NC}" >&2

time_checks_passed=0
time_checks_total=2

# This is hard to measure automatically, so we use proxies:
# - Simple code suggests fast development
# - Working demo suggests iterative approach

# Check 1: Simple enough to build quickly (based on LOC)
if [ "$TOTAL_LOC" -lt 150 ]; then
    time_checks_passed=$((time_checks_passed + 1))
    echo "  ✓ Code size suggests quick development" >&2
else
    echo "  ⚠ Code size suggests longer development" >&2
fi

# Check 2: Working demo suggests successful iteration
if [ "$demo_checks_passed" -ge 4 ]; then
    time_checks_passed=$((time_checks_passed + 1))
    echo "  ✓ Working demo suggests iterative development" >&2
else
    echo "  ⚠ Demo functionality incomplete" >&2
fi

time_score=$(python3 -c "print(int(($time_checks_passed / $time_checks_total) * 100))")
time_details="Passed ${time_checks_passed}/${time_checks_total} time checks"
echo -e "${GREEN}Time/iteration: ${time_checks_passed}/${time_checks_total}${NC}" >&2

# Calculate base score (weighted sum)
base_score=$(python3 -c "
demo = $demo_score * 0.40
feasibility = $feasibility_score * 0.30
simplicity = $simplicity_score * 0.20
time = $time_score * 0.10
total = demo + feasibility + simplicity + time
print(round(total, 2))
")

# No penalties in this benchmark (it's about rapid prototyping)
time_penalty=0
iteration_penalty=0
error_penalty=0

final_score=$(python3 -c "print(int($base_score))")

# Determine pass/fail (60% threshold for prototypes - lower bar than production code)
if (( final_score >= 60 )); then
    passed="true"
    echo -e "\n${GREEN}PASSED${NC} - Score: ${final_score}/100" >&2
else
    passed="false"
    echo -e "\n${RED}FAILED${NC} - Score: ${final_score}/100 (need 60+)" >&2
fi

# Output JSON
cat <<EOF
{
  "benchmark": "${BENCHMARK_NAME}",
  "timestamp": "${START_TIME}",
  "components": {
    "demo_works": {
      "score": ${demo_score},
      "weight": 0.40,
      "details": "${demo_details}"
    },
    "answers_question": {
      "score": ${feasibility_score},
      "weight": 0.30,
      "details": "${feasibility_details}"
    },
    "simplicity": {
      "score": ${simplicity_score},
      "weight": 0.20,
      "details": "${simplicity_details}"
    },
    "time_bonus": {
      "score": ${time_score},
      "weight": 0.10,
      "details": "${time_details}"
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

# Cleanup
rm -f demo_test.log watcher_output.log 2>/dev/null || true

# Exit with appropriate code
if [ "$passed" = "true" ]; then
    exit 0
else
    exit 1
fi
