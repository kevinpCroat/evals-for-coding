# Prototyping: File Sync CLI Tool - Specification

## Objective

Build a minimal working proof-of-concept CLI tool that demonstrates real-time file watching and cloud synchronization capabilities.

## Background

You need to answer the technical feasibility question: "Can we build a CLI tool that watches local files and syncs them to cloud storage in real-time?"

This is a prototyping exercise, not production development. The goal is to quickly build a working demo that proves the concept is technically viable. Focus on:
- **Speed**: Get something working quickly
- **Simplicity**: Minimal code, minimal dependencies
- **Demonstrability**: It must actually run and show the concept working

## Requirements

### Functional Requirements

1. **File Watching**: Monitor a directory for changes
   - Detect when files are created
   - Detect when files are modified
   - Detect when files are deleted

2. **Simulated Cloud Sync**: Mock cloud storage operations
   - Simulate uploading files to cloud
   - Simulate deleting files from cloud
   - Track sync state (what's in "cloud")
   - Can use local directory, JSON file, or in-memory structure to simulate cloud

3. **CLI Interface**: Command-line tool to control the watcher
   - Start watching a directory: `sync-tool watch <directory>`
   - Show current status: `sync-tool status`
   - Stop gracefully with Ctrl+C

4. **Status Reporting**: Show what's happening
   - Print when files change
   - Print when sync operations occur
   - Show success/failure for each operation

### Technical Constraints

- **Language**: Python (any version 3.7+)
- **Dependencies**: Prefer standard library; minimal external dependencies are OK
- **Platform**: Must work on Unix-like systems (Linux/macOS)
- **Scope**: Proof-of-concept quality, not production-ready
- **Time**: Should be buildable in 20-30 minutes

### Out of Scope (Don't Build These)

- Real cloud API integration
- Conflict resolution
- File versioning
- Database persistence
- Authentication/security
- Multi-user support
- Configuration files
- Comprehensive error recovery

## Success Criteria

Your prototype will be considered successful when:

1. **It Runs**: The tool can be executed and demonstrates the concept
2. **It Watches**: File changes are actually detected in real-time
3. **It Syncs**: Some form of sync operation happens (even if mocked)
4. **It's Simple**: Code is straightforward and easy to understand
5. **It Answers the Question**: Demonstrates that file watching + sync is feasible

## Deliverables

1. **Python Script(s)**: The CLI tool implementation
   - Can be single file or multiple files
   - Should have a clear entry point

2. **README.md**: Brief documentation with:
   - How to run the tool
   - What it demonstrates
   - Example usage
   - Any dependencies to install

3. **Demo Instructions**: How to see it working
   - What commands to run
   - What to expect to see

4. **requirements.txt**: Any Python dependencies (if needed)

## Example Usage

Your tool should work something like this:

```bash
# Install dependencies (if any)
pip install -r requirements.txt

# Start watching a directory
python sync_tool.py watch ./test_folder

# In another terminal, make changes:
echo "hello" > ./test_folder/newfile.txt
# Tool should detect and "sync" this

# Stop with Ctrl+C
```

## Evaluation

Your submission will be scored on:

- **Demo Works**: 40% - Can execute and demonstrates file watching + sync
- **Answers Question**: 30% - Proves the concept is feasible
- **Simplicity**: 20% - Low lines of code, minimal complexity
- **Time to Working**: 10% - Bonus for quick, iterative development

This is not about perfect code or comprehensive features. It's about quickly validating technical feasibility.

## Tips

- Start with the simplest possible implementation
- Use existing libraries for file watching (e.g., `watchdog`)
- Mock the cloud backend with a local directory or simple data structure
- Focus on making it runnable and demonstrable
- Don't over-engineer - this is a prototype
- It's OK if it's rough around the edges
- Prefer fewer lines of code over more features

See verification/verify.sh for automated scoring implementation.
