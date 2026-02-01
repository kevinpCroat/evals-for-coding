#!/usr/bin/env node

/**
 * MCP Server for AI Coding Evaluation Framework
 *
 * Provides tools for AI agents to interact with the benchmark suite:
 * - List available benchmarks
 * - Get benchmark specifications
 * - Run benchmarks
 * - Submit solutions
 * - View results
 * - Generate leaderboards
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import { execSync } from 'child_process';
import { readFileSync, readdirSync, existsSync, writeFileSync } from 'fs';
import { join, resolve } from 'path';

// Get the repository root (assumes MCP server is in mcp-server/ subdirectory)
const REPO_ROOT = resolve(process.cwd(), '..');
const BENCHMARKS_DIR = join(REPO_ROOT, 'benchmarks');
const RESULTS_DIR = join(REPO_ROOT, 'results');

/**
 * Benchmark metadata interface
 */
interface BenchmarkMetadata {
  id: string;
  name: string;
  category: string;
  difficulty: string;
  description: string;
  estimatedTime: string;
  tier: number;
  hasStarterCode: boolean;
  hasTests: boolean;
}

/**
 * Benchmark result interface
 */
interface BenchmarkResult {
  benchmark: string;
  timestamp: string;
  components: Record<string, {
    score: number;
    weight: number;
    details: string;
  }>;
  base_score: number;
  penalties: Record<string, number>;
  final_score: number;
  passed: boolean;
}

/**
 * Get all available benchmarks
 */
function listBenchmarks(): BenchmarkMetadata[] {
  const benchmarks: BenchmarkMetadata[] = [];

  const benchmarkDirs = readdirSync(BENCHMARKS_DIR, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name)
    .filter(name => name.endsWith('-001'));

  for (const benchmarkId of benchmarkDirs) {
    const benchmarkPath = join(BENCHMARKS_DIR, benchmarkId);
    const readmePath = join(benchmarkPath, 'README.md');

    if (!existsSync(readmePath)) continue;

    const readme = readFileSync(readmePath, 'utf-8');

    // Extract metadata from README
    const metadata: BenchmarkMetadata = {
      id: benchmarkId,
      name: benchmarkId,
      category: extractCategory(readme),
      difficulty: extractDifficulty(readme),
      description: extractDescription(readme),
      estimatedTime: extractEstimatedTime(readme),
      tier: determineTier(benchmarkId),
      hasStarterCode: existsSync(join(benchmarkPath, 'starter-code')),
      hasTests: existsSync(join(benchmarkPath, 'verification')),
    };

    benchmarks.push(metadata);
  }

  return benchmarks.sort((a, b) => a.id.localeCompare(b.id));
}

/**
 * Get benchmark specification
 */
function getBenchmarkSpec(benchmarkId: string): string {
  const specPath = join(BENCHMARKS_DIR, benchmarkId, 'spec.md');

  if (!existsSync(specPath)) {
    throw new Error(`Benchmark ${benchmarkId} not found or missing spec.md`);
  }

  return readFileSync(specPath, 'utf-8');
}

/**
 * Get benchmark prompts
 */
function getBenchmarkPrompts(benchmarkId: string): string {
  const promptsPath = join(BENCHMARKS_DIR, benchmarkId, 'prompts.txt');

  if (!existsSync(promptsPath)) {
    throw new Error(`Benchmark ${benchmarkId} not found or missing prompts.txt`);
  }

  return readFileSync(promptsPath, 'utf-8');
}

/**
 * Get benchmark starter code structure
 */
function getStarterCodeStructure(benchmarkId: string): string {
  const starterCodePath = join(BENCHMARKS_DIR, benchmarkId, 'starter-code');

  if (!existsSync(starterCodePath)) {
    return 'No starter code available for this benchmark.';
  }

  try {
    const tree = execSync(`cd "${starterCodePath}" && find . -type f | sort`, {
      encoding: 'utf-8',
      maxBuffer: 10 * 1024 * 1024,
    });

    return `Starter code structure:\n${tree}`;
  } catch (error) {
    return `Error reading starter code: ${error}`;
  }
}

/**
 * Run a benchmark
 */
function runBenchmark(benchmarkId: string, timeout: number = 300000): BenchmarkResult {
  const benchmarkPath = join(BENCHMARKS_DIR, benchmarkId);
  const verifyScript = join(benchmarkPath, 'verification', 'verify.sh');

  if (!existsSync(verifyScript)) {
    throw new Error(`Benchmark ${benchmarkId} not found or missing verification script`);
  }

  try {
    const output = execSync(`cd "${benchmarkPath}" && ./verification/verify.sh`, {
      encoding: 'utf-8',
      timeout: timeout,
      maxBuffer: 10 * 1024 * 1024,
    });

    // Extract JSON from output (last JSON object)
    const jsonMatch = output.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No JSON output found from verification script');
    }

    return JSON.parse(jsonMatch[0]) as BenchmarkResult;
  } catch (error: any) {
    if (error.killed) {
      throw new Error(`Benchmark timed out after ${timeout}ms`);
    }
    throw new Error(`Benchmark execution failed: ${error.message}`);
  }
}

/**
 * Get results history
 */
function getResultsHistory(benchmarkId?: string): BenchmarkResult[] {
  if (!existsSync(RESULTS_DIR)) {
    return [];
  }

  const resultFiles = readdirSync(RESULTS_DIR)
    .filter(f => f.endsWith('.json'))
    .filter(f => !benchmarkId || f.startsWith(benchmarkId));

  const results: BenchmarkResult[] = [];

  for (const file of resultFiles) {
    try {
      const content = readFileSync(join(RESULTS_DIR, file), 'utf-8');
      results.push(JSON.parse(content));
    } catch (error) {
      // Skip invalid JSON files
    }
  }

  return results.sort((a, b) =>
    new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  );
}

/**
 * Generate leaderboard
 */
function generateLeaderboard(): string {
  try {
    const output = execSync(
      `cd "${REPO_ROOT}/evaluation-framework" && python3 generate_leaderboard.py "${RESULTS_DIR}"`,
      { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 }
    );
    return output;
  } catch (error: any) {
    throw new Error(`Failed to generate leaderboard: ${error.message}`);
  }
}

/**
 * Helper functions for metadata extraction
 */
function extractCategory(readme: string): string {
  const match = readme.match(/\*\*Category:\*\*\s*(.+)/i);
  return match ? match[1].trim() : 'Unknown';
}

function extractDifficulty(readme: string): string {
  const match = readme.match(/\*\*Difficulty:\*\*\s*(.+)/i);
  return match ? match[1].trim() : 'Unknown';
}

function extractDescription(readme: string): string {
  const match = readme.match(/##\s*Overview\s+(.+?)(?=\n##|\n\*\*|$)/s);
  if (match) {
    return match[1].trim().replace(/\n/g, ' ').substring(0, 200);
  }
  return 'No description available';
}

function extractEstimatedTime(readme: string): string {
  const match = readme.match(/\*\*Estimated Time:\*\*\s*(.+)/i);
  return match ? match[1].trim() : 'Unknown';
}

function determineTier(benchmarkId: string): number {
  const tier1 = ['bug-fixing-001', 'testing-001', 'greenfield-001', 'refactoring-001', 'code-migration-001'];
  const tier2 = ['debugging-001', 'maintenance-001', 'documentation-001', 'rewriting-001', 'code-review-001', 'api-design-001', 'data-modelling-001'];

  if (tier1.includes(benchmarkId)) return 1;
  if (tier2.includes(benchmarkId)) return 2;
  return 3;
}

/**
 * MCP Server Setup
 */
const server = new Server(
  {
    name: 'evals-for-coding',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Define available tools
 */
const tools: Tool[] = [
  {
    name: 'list_benchmarks',
    description: 'List all available benchmarks with metadata (category, difficulty, tier, description)',
    inputSchema: {
      type: 'object',
      properties: {
        category: {
          type: 'string',
          description: 'Filter by category (Creation, Evolution, Quality, Knowledge, Operations)',
          enum: ['Creation', 'Evolution', 'Quality', 'Knowledge', 'Operations'],
        },
        difficulty: {
          type: 'string',
          description: 'Filter by difficulty level',
          enum: ['Easy', 'Medium', 'Medium-Hard', 'Hard'],
        },
        tier: {
          type: 'number',
          description: 'Filter by tier (1, 2, or 3)',
          enum: [1, 2, 3],
        },
      },
    },
  },
  {
    name: 'get_benchmark_spec',
    description: 'Get the detailed specification for a specific benchmark',
    inputSchema: {
      type: 'object',
      properties: {
        benchmark_id: {
          type: 'string',
          description: 'The benchmark ID (e.g., "security-001")',
        },
      },
      required: ['benchmark_id'],
    },
  },
  {
    name: 'get_benchmark_prompts',
    description: 'Get the AI prompts/instructions for a specific benchmark',
    inputSchema: {
      type: 'object',
      properties: {
        benchmark_id: {
          type: 'string',
          description: 'The benchmark ID (e.g., "security-001")',
        },
      },
      required: ['benchmark_id'],
    },
  },
  {
    name: 'get_starter_code_structure',
    description: 'Get the file structure of the starter code for a benchmark',
    inputSchema: {
      type: 'object',
      properties: {
        benchmark_id: {
          type: 'string',
          description: 'The benchmark ID (e.g., "security-001")',
        },
      },
      required: ['benchmark_id'],
    },
  },
  {
    name: 'run_benchmark',
    description: 'Run the verification script for a benchmark and get the score. The benchmark code must already be completed.',
    inputSchema: {
      type: 'object',
      properties: {
        benchmark_id: {
          type: 'string',
          description: 'The benchmark ID (e.g., "security-001")',
        },
        timeout_ms: {
          type: 'number',
          description: 'Timeout in milliseconds (default: 300000 = 5 minutes)',
          default: 300000,
        },
      },
      required: ['benchmark_id'],
    },
  },
  {
    name: 'get_results_history',
    description: 'Get historical results for benchmarks',
    inputSchema: {
      type: 'object',
      properties: {
        benchmark_id: {
          type: 'string',
          description: 'Optional: Filter by specific benchmark ID',
        },
      },
    },
  },
  {
    name: 'generate_leaderboard',
    description: 'Generate a leaderboard from all results in the results directory',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'get_benchmark_categories',
    description: 'Get information about the 5 evaluation categories and 20 areas',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
];

/**
 * Handle list_tools request
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

/**
 * Handle call_tool request
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'list_benchmarks': {
        let benchmarks = listBenchmarks();

        // Apply filters
        if (args?.category) {
          benchmarks = benchmarks.filter(b => b.category === args.category);
        }
        if (args?.difficulty) {
          benchmarks = benchmarks.filter(b => b.difficulty === args.difficulty);
        }
        if (args?.tier) {
          benchmarks = benchmarks.filter(b => b.tier === args.tier);
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(benchmarks, null, 2),
            },
          ],
        };
      }

      case 'get_benchmark_spec': {
        const spec = getBenchmarkSpec(args.benchmark_id as string);
        return {
          content: [
            {
              type: 'text',
              text: spec,
            },
          ],
        };
      }

      case 'get_benchmark_prompts': {
        const prompts = getBenchmarkPrompts(args.benchmark_id as string);
        return {
          content: [
            {
              type: 'text',
              text: prompts,
            },
          ],
        };
      }

      case 'get_starter_code_structure': {
        const structure = getStarterCodeStructure(args.benchmark_id as string);
        return {
          content: [
            {
              type: 'text',
              text: structure,
            },
          ],
        };
      }

      case 'run_benchmark': {
        const result = runBenchmark(
          args.benchmark_id as string,
          args.timeout_ms as number | undefined
        );
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2),
            },
          ],
        };
      }

      case 'get_results_history': {
        const results = getResultsHistory(args?.benchmark_id as string | undefined);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(results, null, 2),
            },
          ],
        };
      }

      case 'generate_leaderboard': {
        const leaderboard = generateLeaderboard();
        return {
          content: [
            {
              type: 'text',
              text: leaderboard,
            },
          ],
        };
      }

      case 'get_benchmark_categories': {
        const categories = {
          categories: [
            {
              name: 'Creation',
              count: 5,
              areas: ['Greenfield', 'Prototyping', 'Architecture', 'API Design', 'Data Modelling'],
            },
            {
              name: 'Evolution',
              count: 5,
              areas: ['Maintenance', 'Refactoring', 'Rewriting', 'Porting', 'Code Migration'],
            },
            {
              name: 'Quality',
              count: 7,
              areas: ['Debugging', 'Bug Fixing', 'Testing', 'Code Review', 'Performance', 'Security', 'Concurrency'],
            },
            {
              name: 'Knowledge',
              count: 2,
              areas: ['Documentation', 'Legacy Code Comprehension'],
            },
            {
              name: 'Operations',
              count: 1,
              areas: ['Infrastructure'],
            },
          ],
          total_areas: 20,
        };
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(categories, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

/**
 * Start the server
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Evals-for-Coding MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
