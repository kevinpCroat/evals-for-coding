# MCP Server Setup Guide

Complete guide to setting up the Evals-for-Coding MCP server for use with Claude Desktop or other MCP clients.

## Prerequisites

- Node.js 18 or higher
- npm or yarn
- Python 3.8+ (for running benchmarks)
- Claude Desktop (for Claude integration) or any MCP client

## Installation Steps

### 1. Install Dependencies

```bash
cd mcp-server
npm install
```

### 2. Build the Server

```bash
npm run build
```

This compiles TypeScript to JavaScript in the `dist/` directory.

### 3. Test the Server

```bash
# Test that it starts
node dist/index.js
# Should output: "Evals-for-Coding MCP Server running on stdio"
# Press Ctrl+C to stop
```

### 4. Configure Claude Desktop

#### macOS

1. **Find your config file location:**
   ```bash
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. **Edit the config file:**
   ```bash
   # Open in your editor
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   # or
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. **Add the MCP server:**
   ```json
   {
     "mcpServers": {
       "evals-for-coding": {
         "command": "node",
         "args": [
           "/Users/YOUR_USERNAME/path/to/evals-for-coding/mcp-server/dist/index.js"
         ]
       }
     }
   }
   ```

   **Important:** Replace `/Users/YOUR_USERNAME/path/to/` with your actual absolute path!

4. **Get absolute path:**
   ```bash
   cd /path/to/evals-for-coding/mcp-server
   pwd
   # Copy this output and use it in the config
   ```

#### Linux

```bash
# Config location
~/.config/Claude/claude_desktop_config.json
```

Follow same steps as macOS.

#### Windows

```bash
# Config location
%APPDATA%\Claude\claude_desktop_config.json
```

Update paths to use Windows format:
```json
{
  "mcpServers": {
    "evals-for-coding": {
      "command": "node",
      "args": [
        "C:\\Users\\YOUR_USERNAME\\path\\to\\evals-for-coding\\mcp-server\\dist\\index.js"
      ]
    }
  }
}
```

### 5. Restart Claude Desktop

After updating the config:
1. Quit Claude Desktop completely
2. Restart Claude Desktop
3. The MCP server should now be available

### 6. Verify Integration

In Claude Desktop, try using the tools:

```
Can you list all available benchmarks?
```

Claude should use the `list_benchmarks` tool and return the list of benchmarks.

## Quick Start Script

Create a setup script to automate installation:

### setup.sh (macOS/Linux)

```bash
#!/bin/bash

echo "Setting up Evals-for-Coding MCP Server..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Build
echo "Building..."
npm run build

# Get absolute path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MCP_PATH="$SCRIPT_DIR/dist/index.js"

echo ""
echo "✅ Build complete!"
echo ""
echo "To use with Claude Desktop, add this to your config:"
echo "File: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo '{
  "mcpServers": {
    "evals-for-coding": {
      "command": "node",
      "args": ["'$MCP_PATH'"]
    }
  }
}'
echo ""
echo "Then restart Claude Desktop."
```

Run it:
```bash
chmod +x setup.sh
./setup.sh
```

## Testing the Server

### Manual Test

```bash
# Start the server
node dist/index.js

# In another terminal, test with stdio
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | node dist/index.js
```

### With Claude Desktop

Once configured, try these prompts:

1. **List benchmarks:**
   ```
   Show me all available benchmarks
   ```

2. **Get a specification:**
   ```
   Get the specification for security-001
   ```

3. **View categories:**
   ```
   What benchmark categories are available?
   ```

4. **Filter benchmarks:**
   ```
   Show me all Easy difficulty benchmarks
   ```

## Troubleshooting

### Server Not Found in Claude

**Problem:** Claude says the tools aren't available

**Solution:**
1. Check config file syntax (valid JSON)
2. Verify absolute path is correct
3. Ensure server was built (`npm run build`)
4. Restart Claude Desktop completely (quit and reopen)
5. Check Claude Desktop logs

### Build Errors

**Problem:** `npm run build` fails

**Solution:**
```bash
# Clean and rebuild
rm -rf node_modules dist
npm install
npm run build
```

### Node Version Issues

**Problem:** Errors about unsupported features

**Solution:**
```bash
# Check Node version
node --version

# Should be 18 or higher
# Update if needed:
# macOS: brew install node
# Linux: nvm install 18
# Windows: Download from nodejs.org
```

### Path Issues on Windows

**Problem:** Config won't work with forward slashes

**Solution:**
- Use backslashes: `C:\\Users\\...`
- Or use forward slashes: `C:/Users/...` (both work)
- Ensure no trailing slashes

### Permission Errors

**Problem:** Can't write to results directory

**Solution:**
```bash
# Ensure results directory exists and is writable
mkdir -p ../results
chmod 755 ../results
```

## Advanced Configuration

### Custom Environment Variables

```json
{
  "mcpServers": {
    "evals-for-coding": {
      "command": "node",
      "args": ["/path/to/dist/index.js"],
      "env": {
        "RESULTS_DIR": "/custom/results/path",
        "BENCHMARK_TIMEOUT": "600000"
      }
    }
  }
}
```

### Debug Mode

```json
{
  "mcpServers": {
    "evals-for-coding": {
      "command": "node",
      "args": [
        "--inspect",
        "/path/to/dist/index.js"
      ]
    }
  }
}
```

### Multiple Instances

You can run multiple instances with different configurations:

```json
{
  "mcpServers": {
    "evals-for-coding-prod": {
      "command": "node",
      "args": ["/path/to/dist/index.js"]
    },
    "evals-for-coding-dev": {
      "command": "node",
      "args": ["/path/to/dev/dist/index.js"]
    }
  }
}
```

## Development Workflow

### Watch Mode

```bash
# Auto-rebuild on changes
npm run dev
```

### Testing Changes

1. Make changes to `src/index.ts`
2. Rebuild: `npm run build`
3. Restart Claude Desktop
4. Test the changes

### Adding New Tools

1. Add tool definition to `tools` array in `src/index.ts`
2. Implement handler in `CallToolRequestSchema`
3. Rebuild and test
4. Update README.md with examples

## Production Deployment

### Docker (Future)

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY dist ./dist

CMD ["node", "dist/index.js"]
```

### System Service (Linux)

```ini
# /etc/systemd/system/evals-mcp.service
[Unit]
Description=Evals-for-Coding MCP Server
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/path/to/mcp-server
ExecStart=/usr/bin/node /path/to/mcp-server/dist/index.js
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable evals-mcp
sudo systemctl start evals-mcp
```

## Security Notes

### Local Execution

- Server runs benchmarks in local environment
- No sandboxing by default
- Trust the code you're evaluating

### Future: Docker Isolation

- Planned: Docker containerization
- Each benchmark runs in isolated container
- Resource limits enforced

### Access Control

- Currently no authentication
- Intended for local use only
- Do not expose to network

## Performance Tuning

### Benchmark Timeouts

Default: 5 minutes (300000ms)

Adjust per benchmark:
```typescript
run_benchmark({
  benchmark_id: "performance-001",
  timeout_ms: 600000  // 10 minutes
})
```

### Concurrent Execution

Currently sequential. Future enhancement:
- Parallel benchmark execution
- Resource pooling
- Queue management

## Next Steps

1. **Install and test** - Follow steps above
2. **Try the examples** - Use Claude to run benchmarks
3. **Read the API docs** - See README.md for all tools
4. **Customize** - Extend with your own tools
5. **Contribute** - Submit improvements via PR

## Support

- **Issues:** https://github.com/kevinpCroat/evals-for-coding/issues
- **Discussions:** GitHub Discussions
- **MCP Docs:** https://modelcontextprotocol.io

## Success Checklist

- [ ] Node.js 18+ installed
- [ ] Dependencies installed (`npm install`)
- [ ] Server built (`npm run build`)
- [ ] Config file created with absolute path
- [ ] Claude Desktop restarted
- [ ] Tools available in Claude
- [ ] Successfully listed benchmarks
- [ ] Successfully ran a benchmark

If all checked, you're ready to go! 🎉
