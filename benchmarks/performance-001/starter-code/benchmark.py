"""
Benchmark script to measure performance improvements.

This script times the execution of the data processor and compares
results before and after optimization.
"""

import time
import json
from data_processor import LogProcessor, generate_test_logs


def benchmark_processor(num_users=1000, entries_per_user=5, num_runs=3):
    """
    Benchmark the LogProcessor performance.

    Args:
        num_users: Number of unique users in test data
        entries_per_user: Log entries per user
        num_runs: Number of times to run the benchmark

    Returns:
        Dictionary with timing results and correctness checks
    """
    # Generate test data once
    logs = generate_test_logs(num_users=num_users, entries_per_user=entries_per_user)

    times = []
    results = []

    print(f"Benchmarking with {len(logs)} log entries ({num_users} users, {entries_per_user} entries each)")
    print(f"Running {num_runs} iterations...\n")

    for run in range(num_runs):
        processor = LogProcessor()
        processor.load_logs(logs)

        start = time.time()
        result = processor.process_all()
        elapsed = time.time() - start

        times.append(elapsed)
        results.append(result)

        print(f"Run {run + 1}: {elapsed:.3f} seconds")

    # Calculate statistics
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\nResults:")
    print(f"  Average: {avg_time:.3f}s")
    print(f"  Min:     {min_time:.3f}s")
    print(f"  Max:     {max_time:.3f}s")

    # Verify correctness
    print(f"\nCorrectness checks:")
    print(f"  Duplicates found: {len(results[0]['duplicates'])}")
    print(f"  Unique users in stats: {len(results[0]['stats'])}")
    print(f"  Top user: {results[0]['top_users'][0][0]} with {results[0]['top_users'][0][1]}s")

    # Ensure all runs produced same results
    for i in range(1, len(results)):
        assert len(results[i]['duplicates']) == len(results[0]['duplicates']), "Inconsistent duplicate count"
        assert len(results[i]['stats']) == len(results[0]['stats']), "Inconsistent stats count"

    return {
        'dataset_size': len(logs),
        'num_users': num_users,
        'entries_per_user': entries_per_user,
        'num_runs': num_runs,
        'times': times,
        'avg_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'duplicates_found': len(results[0]['duplicates']),
        'users_in_stats': len(results[0]['stats']),
    }


def save_benchmark_results(results, filename='benchmark_results.json'):
    """Save benchmark results to JSON file."""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {filename}")


if __name__ == "__main__":
    results = benchmark_processor(num_users=1000, entries_per_user=5, num_runs=3)
    save_benchmark_results(results)
