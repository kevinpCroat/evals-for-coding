#!/usr/bin/env python3
"""
Benchmark runner utility for executing individual benchmarks and collecting results.

Usage:
    python run_benchmark.py benchmark-name
    python run_benchmark.py bug-fixing-001
    python run_benchmark.py --all
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class BenchmarkRunner:
    """Runs benchmarks and collects results."""

    def __init__(self, benchmarks_dir: Path, results_dir: Path):
        self.benchmarks_dir = benchmarks_dir
        self.results_dir = results_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def list_benchmarks(self) -> list[str]:
        """List all available benchmarks."""
        benchmarks = []
        for path in self.benchmarks_dir.iterdir():
            if path.is_dir() and (path / "verification" / "verify.sh").exists():
                benchmarks.append(path.name)
        return sorted(benchmarks)

    def run_benchmark(self, benchmark_name: str) -> Dict[str, Any]:
        """Run a single benchmark and return results."""
        benchmark_path = self.benchmarks_dir / benchmark_name
        verify_script = benchmark_path / "verification" / "verify.sh"

        if not verify_script.exists():
            return {
                "benchmark": benchmark_name,
                "error": "verify.sh not found",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

        print(f"Running benchmark: {benchmark_name}")
        print(f"Path: {benchmark_path}")

        try:
            result = subprocess.run(
                [str(verify_script)],
                cwd=benchmark_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            # Try to parse JSON from stdout
            try:
                output = json.loads(result.stdout)
            except json.JSONDecodeError:
                # If not JSON, capture the raw output
                output = {
                    "benchmark": benchmark_name,
                    "error": "Invalid JSON output",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }

            # Add metadata
            output["exit_code"] = result.returncode
            output["execution_time_ms"] = None  # Could add timing

            return output

        except subprocess.TimeoutExpired:
            return {
                "benchmark": benchmark_name,
                "error": "Execution timeout (300s)",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        except Exception as e:
            return {
                "benchmark": benchmark_name,
                "error": f"Execution failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

    def save_result(self, result: Dict[str, Any]) -> Path:
        """Save benchmark result to file."""
        benchmark_name = result.get("benchmark", "unknown")
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{benchmark_name}_{timestamp}.json"
        filepath = self.results_dir / filename

        with open(filepath, "w") as f:
            json.dump(result, f, indent=2)

        return filepath

    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all available benchmarks."""
        benchmarks = self.list_benchmarks()
        results = {
            "run_timestamp": datetime.utcnow().isoformat() + "Z",
            "total_benchmarks": len(benchmarks),
            "results": []
        }

        for benchmark in benchmarks:
            result = self.run_benchmark(benchmark)
            results["results"].append(result)

            # Print summary
            passed = result.get("passed", False)
            score = result.get("final_score", 0)
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {status} - Score: {score}/100")

        return results


def main():
    parser = argparse.ArgumentParser(
        description="Run software engineering benchmarks for AI evaluation"
    )
    parser.add_argument(
        "benchmark",
        nargs="?",
        help="Benchmark name to run (e.g., bug-fixing-001)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all available benchmarks"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available benchmarks"
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results"),
        help="Directory to save results (default: results/)"
    )

    args = parser.parse_args()

    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    benchmarks_dir = project_root / "benchmarks"

    runner = BenchmarkRunner(benchmarks_dir, args.results_dir)

    # List benchmarks
    if args.list:
        benchmarks = runner.list_benchmarks()
        print(f"Available benchmarks ({len(benchmarks)}):")
        for benchmark in benchmarks:
            print(f"  - {benchmark}")
        return 0

    # Run all benchmarks
    if args.all:
        results = runner.run_all_benchmarks()

        # Save combined results
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filepath = args.results_dir / f"all_benchmarks_{timestamp}.json"
        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\nResults saved to: {filepath}")

        # Print summary
        passed = sum(1 for r in results["results"] if r.get("passed", False))
        total = results["total_benchmarks"]
        print(f"\nSummary: {passed}/{total} benchmarks passed")

        return 0 if passed == total else 1

    # Run single benchmark
    if args.benchmark:
        result = runner.run_benchmark(args.benchmark)
        filepath = runner.save_result(result)

        print(f"\nResults saved to: {filepath}")
        print(json.dumps(result, indent=2))

        return 0 if result.get("passed", False) else 1

    # No arguments provided
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
