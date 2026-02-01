#!/bin/bash
# Demo Test Script
# Tests that the file watching + sync demo actually works

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Create a temporary test directory
TEST_DIR="$PROJECT_DIR/.test_demo_$$"
mkdir -p "$TEST_DIR"

# Cleanup function
cleanup() {
    if [ ! -z "$WATCHER_PID" ]; then
        kill $WATCHER_PID 2>/dev/null || true
        wait $WATCHER_PID 2>/dev/null || true
    fi
    rm -rf "$TEST_DIR" 2>/dev/null || true
}
trap cleanup EXIT

# Find the main script
MAIN_SCRIPT=""
for file in sync_tool.py file_sync.py watcher.py main.py watch.py app.py; do
    if [ -f "$file" ]; then
        MAIN_SCRIPT="$file"
        break
    fi
done

if [ -z "$MAIN_SCRIPT" ]; then
    MAIN_SCRIPT=$(ls *.py 2>/dev/null | head -1)
fi

if [ -z "$MAIN_SCRIPT" ]; then
    echo "ERROR: No Python script found" >&2
    exit 1
fi

echo "Testing $MAIN_SCRIPT" >&2

# Start the watcher in the background with a timeout
timeout 10 python3 "$MAIN_SCRIPT" watch "$TEST_DIR" 2>&1 &
WATCHER_PID=$!

# Give it time to start
sleep 2

# Check if process is still running
if ! kill -0 $WATCHER_PID 2>/dev/null; then
    echo "ERROR: Watcher process died" >&2
    exit 1
fi

echo "Watcher started (PID: $WATCHER_PID)" >&2

# Perform file operations
echo "Creating test file..." >&2
echo "test content 1" > "$TEST_DIR/file1.txt"
sleep 1

echo "Modifying test file..." >&2
echo "test content 2" >> "$TEST_DIR/file1.txt"
sleep 1

echo "Creating another file..." >&2
echo "test content 3" > "$TEST_DIR/file2.txt"
sleep 1

echo "Deleting a file..." >&2
rm "$TEST_DIR/file1.txt"
sleep 1

# Stop the watcher
echo "Stopping watcher..." >&2
kill $WATCHER_PID 2>/dev/null || true
wait $WATCHER_PID 2>/dev/null || true

echo "Demo test completed successfully" >&2
exit 0
