#!/usr/bin/env python3
"""
Generate leaderboard from benchmark results.

Compares different AI approaches across all benchmarks to create rankings.

Usage:
    python generate_leaderboard.py results/
    python generate_leaderboard.py results/ --format markdown
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime


class LeaderboardGenerator:
    """Generates leaderboards from benchmark results."""

    def __init__(self, results_dir: Path):
        self.results_dir = results_dir

    def load_results(self) -> List[Dict[str, Any]]:
        """Load all result JSON files."""
        results = []
        for filepath in self.results_dir.glob("*.json"):
            try:
                with open(filepath) as f:
                    data = json.load(f)
                    # Handle both single results and batched results
                    if "results" in data:
                        results.extend(data["results"])
                    else:
                        results.append(data)
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")
        return results

    def group_by_benchmark(self, results: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """Group results by benchmark name."""
        grouped = defaultdict(list)
        for result in results:
            benchmark = result.get("benchmark", "unknown")
            grouped[benchmark].append(result)
        return dict(grouped)

    def calculate_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics for a set of results."""
        if not results:
            return {
                "count": 0,
                "avg_score": 0,
                "min_score": 0,
                "max_score": 0,
                "pass_rate": 0
            }

        scores = [r.get("final_score", 0) for r in results]
        passed = sum(1 for r in results if r.get("passed", False))

        return {
            "count": len(results),
            "avg_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "pass_rate": (passed / len(results)) * 100
        }

    def generate_markdown_leaderboard(self, grouped_results: Dict[str, List[Dict]]) -> str:
        """Generate markdown leaderboard."""
        lines = ["# Benchmark Leaderboard\n"]
        lines.append(f"Generated: {datetime.utcnow().isoformat()}Z\n")

        # Overall statistics
        all_results = [r for results in grouped_results.values() for r in results]
        overall = self.calculate_statistics(all_results)

        lines.append("## Overall Statistics\n")
        lines.append(f"- Total Results: {overall['count']}")
        lines.append(f"- Average Score: {overall['avg_score']:.1f}/100")
        lines.append(f"- Pass Rate: {overall['pass_rate']:.1f}%")
        lines.append(f"- Score Range: {overall['min_score']:.0f} - {overall['max_score']:.0f}\n")

        # Per-benchmark results
        lines.append("## Benchmark Results\n")
        lines.append("| Benchmark | Runs | Avg Score | Pass Rate | Min | Max |")
        lines.append("|-----------|------|-----------|-----------|-----|-----|")

        for benchmark in sorted(grouped_results.keys()):
            results = grouped_results[benchmark]
            stats = self.calculate_statistics(results)

            lines.append(
                f"| {benchmark} | {stats['count']} | "
                f"{stats['avg_score']:.1f} | {stats['pass_rate']:.1f}% | "
                f"{stats['min_score']:.0f} | {stats['max_score']:.0f} |"
            )

        lines.append("")

        # Detailed results
        lines.append("## Detailed Results\n")

        for benchmark in sorted(grouped_results.keys()):
            lines.append(f"### {benchmark}\n")

            results = grouped_results[benchmark]
            for i, result in enumerate(results, 1):
                score = result.get("final_score", 0)
                passed = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
                timestamp = result.get("timestamp", "unknown")

                lines.append(f"**Run {i}** ({timestamp}): {passed} - {score}/100")

                # Component breakdown
                components = result.get("components", {})
                if components:
                    lines.append("\nComponent Scores:")
                    for comp_name, comp_data in components.items():
                        if isinstance(comp_data, dict):
                            comp_score = comp_data.get("score", 0)
                            comp_weight = comp_data.get("weight", 0)
                            weighted = comp_score * comp_weight
                            lines.append(f"- {comp_name}: {comp_score}/100 (weight: {comp_weight:.0%}, contribution: {weighted:.1f})")

                lines.append("")

        return "\n".join(lines)

    def generate_json_leaderboard(self, grouped_results: Dict[str, List[Dict]]) -> Dict:
        """Generate JSON leaderboard."""
        all_results = [r for results in grouped_results.values() for r in results]
        overall = self.calculate_statistics(all_results)

        benchmarks = {}
        for benchmark, results in sorted(grouped_results.items()):
            benchmarks[benchmark] = {
                "statistics": self.calculate_statistics(results),
                "runs": results
            }

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "overall_statistics": overall,
            "benchmarks": benchmarks
        }


def main():
    parser = argparse.ArgumentParser(
        description="Generate leaderboard from benchmark results"
    )
    parser.add_argument(
        "results_dir",
        type=Path,
        help="Directory containing result JSON files"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    if not args.results_dir.exists():
        print(f"Error: Results directory not found: {args.results_dir}")
        return 1

    generator = LeaderboardGenerator(args.results_dir)
    results = generator.load_results()

    if not results:
        print(f"Warning: No results found in {args.results_dir}")
        return 1

    grouped = generator.group_by_benchmark(results)

    if args.format == "markdown":
        output = generator.generate_markdown_leaderboard(grouped)
    else:
        output = json.dumps(
            generator.generate_json_leaderboard(grouped),
            indent=2
        )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Leaderboard saved to: {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
