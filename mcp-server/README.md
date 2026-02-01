# Evals for Coding - MCP Server

Model Context Protocol (MCP) server for the AI Coding Evaluation Framework. This server allows AI agents to programmatically interact with the benchmark suite.

## Features

### 8 Available Tools

1. **list_benchmarks** - List all available benchmarks with metadata
   - Filter by category, difficulty, or tier
   - Returns structured metadata for each benchmark

2. **get_benchmark_spec** - Get detailed specification for a benchmark
   - Returns the complete spec.md content
   - Includes requirements, constraints, and success criteria

3. **get_benchmark_prompts** - Get AI instructions for a benchmark
   - Returns the prompts.txt content
   - Standard format for AI evaluation

4. **get_starter_code_structure** - View file structure of starter code
   - Lists all files in starter-code directory
   - Helps understand the codebase before implementation

5. **run_benchmark** - Execute verification and get score
   - Runs the verification script
   - Returns JSON with component scores and final result
   - Configurable timeout

6. **get_results_history** - View historical benchmark results
   - All past runs or filtered by benchmark ID
   - Sorted by timestamp (newest first)

7. **generate_leaderboard** - Create leaderboard from all results
   - Aggregates all results
   - Statistical analysis
   - Markdown and JSON output

8. **get_benchmark_categories** - Get category taxonomy
   - 5 categories, 20 evaluation areas
   - Overview of complete framework

## Installation

```bash
cd mcp-server
npm install
npm run build
```

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "evals-for-coding": {
      "command": "node",
      "args": ["/absolute/path/to/evals-for-coding/mcp-server/dist/index.js"]
    }
  }
}
```

### With Any MCP Client

```bash
# Start the server (stdio mode)
node dist/index.js
```

The server communicates via stdio using the MCP protocol.

## Example Usage

### List All Benchmarks

```typescript
// Request
{
  "tool": "list_benchmarks",
  "arguments": {}
}

// Response
[
  {
    "id": "bug-fixing-001",
    "name": "bug-fixing-001",
    "category": "Quality",
    "difficulty": "Easy",
    "description": "Fix an off-by-one error in date calculation...",
    "estimatedTime": "15-20 minutes",
    "tier": 1,
    "hasStarterCode": true,
    "hasTests": true
  },
  ...
]
```

### Filter Benchmarks by Category

```typescript
// Request
{
  "tool": "list_benchmarks",
  "arguments": {
    "category": "Security"
  }
}

// Returns only security-related benchmarks
```

### Get Benchmark Specification

```typescript
// Request
{
  "tool": "get_benchmark_spec",
  "arguments": {
    "benchmark_id": "security-001"
  }
}

// Response: Full markdown specification
```

### Run a Benchmark

```typescript
// Request
{
  "tool": "run_benchmark",
  "arguments": {
    "benchmark_id": "security-001",
    "timeout_ms": 300000
  }
}

// Response
{
  "benchmark": "security-001",
  "timestamp": "2026-02-01T12:00:00Z",
  "components": {
    "vulnerabilities_fixed": {
      "score": 80,
      "weight": 0.5,
      "details": "8 out of 10 vulnerabilities fixed"
    },
    "sast_improvement": {
      "score": 90,
      "weight": 0.3,
      "details": "Bandit score improved from 12 to 2"
    },
    "tests_written": {
      "score": 70,
      "weight": 0.2,
      "details": "7 security tests written"
    }
  },
  "base_score": 81,
  "penalties": {
    "time_penalty": 0,
    "error_penalty": 0.1
  },
  "final_score": 72.9,
  "passed": true
}
```

## AI Agent Self-Evaluation Workflow

Here's how an AI agent can use this MCP server to evaluate itself:

### 1. Discovery Phase

```typescript
// Get all benchmarks
list_benchmarks({})

// Filter by difficulty
list_benchmarks({ difficulty: "Easy" })

// Understand categories
get_benchmark_categories({})
```

### 2. Preparation Phase

```typescript
// Read the task
get_benchmark_spec({ benchmark_id: "security-001" })

// Get AI instructions
get_benchmark_prompts({ benchmark_id: "security-001" })

// Understand starter code
get_starter_code_structure({ benchmark_id: "security-001" })
```

### 3. Implementation Phase

```typescript
// Agent reads starter code files using file system tools
// Agent implements the solution
// Agent writes/modifies files in starter-code/
```

### 4. Evaluation Phase

```typescript
// Run verification
run_benchmark({
  benchmark_id: "security-001",
  timeout_ms: 300000
})

// Check if passed
// If not, iterate and improve

// View improvement over time
get_results_history({ benchmark_id: "security-001" })
```

### 5. Comparison Phase

```typescript
// Generate leaderboard to compare against other models
generate_leaderboard({})
```

## Use Cases

### For AI Models

**Self-Evaluation:**
```typescript
// Run all easy benchmarks
const benchmarks = list_benchmarks({ difficulty: "Easy" });
for (const benchmark of benchmarks) {
  const result = run_benchmark({ benchmark_id: benchmark.id });
  console.log(`${benchmark.id}: ${result.passed ? 'PASS' : 'FAIL'} (${result.final_score})`);
}
```

**Progress Tracking:**
```typescript
// Track improvement on a specific benchmark
const history = get_results_history({ benchmark_id: "security-001" });
// Analyze trend over time
```

**Capability Mapping:**
```typescript
// Test all categories to identify strengths/weaknesses
const categories = ["Creation", "Evolution", "Quality", "Knowledge", "Operations"];
for (const category of categories) {
  const benchmarks = list_benchmarks({ category });
  // Run and analyze results per category
}
```

### For Researchers

**Model Comparison:**
```typescript
// Run benchmark suite on multiple models
// Compare results using leaderboard
generate_leaderboard({})
```

**Ablation Studies:**
```typescript
// Test model variants on specific benchmarks
// Track performance differences
```

### For Development Teams

**CI/CD Integration:**
```typescript
// Automated regression testing
// Run benchmarks before/after model updates
// Ensure no capability regression
```

**Quality Gates:**
```typescript
// Require passing specific benchmarks before deployment
const criticalBenchmarks = list_benchmarks({ category: "Security" });
// All must pass before release
```

## API Reference

### list_benchmarks

**Arguments:**
- `category` (optional): Filter by category
- `difficulty` (optional): Filter by difficulty
- `tier` (optional): Filter by tier (1, 2, or 3)

**Returns:** Array of BenchmarkMetadata objects

### get_benchmark_spec

**Arguments:**
- `benchmark_id` (required): Benchmark identifier

**Returns:** Markdown specification text

### get_benchmark_prompts

**Arguments:**
- `benchmark_id` (required): Benchmark identifier

**Returns:** Prompts text

### get_starter_code_structure

**Arguments:**
- `benchmark_id` (required): Benchmark identifier

**Returns:** File tree listing

### run_benchmark

**Arguments:**
- `benchmark_id` (required): Benchmark identifier
- `timeout_ms` (optional): Timeout in milliseconds (default: 300000)

**Returns:** BenchmarkResult object

### get_results_history

**Arguments:**
- `benchmark_id` (optional): Filter by specific benchmark

**Returns:** Array of BenchmarkResult objects

### generate_leaderboard

**Arguments:** None

**Returns:** Leaderboard markdown/JSON

### get_benchmark_categories

**Arguments:** None

**Returns:** Category taxonomy object

## Architecture

```
MCP Server (stdio)
├── Tools (8 total)
│   ├── list_benchmarks
│   ├── get_benchmark_spec
│   ├── get_benchmark_prompts
│   ├── get_starter_code_structure
│   ├── run_benchmark
│   ├── get_results_history
│   ├── generate_leaderboard
│   └── get_benchmark_categories
│
├── File System Access
│   ├── benchmarks/ (read specs, prompts)
│   ├── results/ (read/write results)
│   └── starter-code/ (agent modifies)
│
└── Process Execution
    ├── ./verification/verify.sh
    └── generate_leaderboard.py
```

## Development

### Build

```bash
npm run build
```

### Watch Mode

```bash
npm run dev
```

### Testing

```bash
# Start the server
npm start

# Test with MCP client or Claude Desktop
```

## Requirements

- Node.js 18+
- Python 3.8+ (for running benchmarks)
- All benchmark dependencies installed

## Security Considerations

**Sandbox Execution:**
- Currently runs benchmarks in local environment
- Future: Docker containerization for isolation
- Be cautious when running untrusted code

**Resource Limits:**
- Configurable timeouts per benchmark
- Default: 5 minutes (300000ms)
- Prevents infinite loops/hangs

**File System Access:**
- Read-only access to benchmark specs
- Write access to starter-code/ for solutions
- Write access to results/ for outputs

## Troubleshooting

### Server won't start

```bash
# Check Node.js version
node --version  # Should be 18+

# Rebuild
npm run build

# Check for errors
node dist/index.js
```

### Benchmarks fail to run

```bash
# Verify Python is available
python3 --version

# Check benchmark dependencies
cd benchmarks/security-001
pip install -r requirements.txt

# Test verification manually
./verification/verify.sh
```

### Results not saving

```bash
# Ensure results directory exists
mkdir -p results

# Check permissions
ls -la results/
```

## Future Enhancements

- [ ] Docker containerization for isolated execution
- [ ] Streaming results for long-running benchmarks
- [ ] Benchmark submission queue
- [ ] Real-time leaderboard updates
- [ ] WebSocket support for live progress
- [ ] Multi-model parallel evaluation
- [ ] Statistical significance testing
- [ ] Automated regression detection

## Contributing

Contributions welcome! To add new tools:

1. Add tool definition to `tools` array
2. Implement handler in `CallToolRequestSchema`
3. Update README with examples
4. Test with MCP client

## License

MIT

## Links

- [Main Repository](https://github.com/kevinpCroat/evals-for-coding)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Benchmark Suite Documentation](../README.md)
