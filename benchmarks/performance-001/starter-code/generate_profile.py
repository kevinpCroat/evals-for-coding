"""
Generate profiler output to identify performance bottlenecks.
"""

import cProfile
import pstats
import io
from data_processor import LogProcessor, generate_test_logs


def profile_performance():
    """Profile the data processor performance."""
    # Create profiler
    profiler = cProfile.Profile()

    # Generate test data
    print("Generating test data...")
    logs = generate_test_logs(num_users=1000, entries_per_user=5)
    print(f"Generated {len(logs)} log entries\n")

    # Profile the processing
    processor = LogProcessor()
    processor.load_logs(logs)

    print("Profiling execution...")
    profiler.enable()
    result = processor.process_all()
    profiler.disable()

    # Print results
    print(f"\nProcessing complete!")
    print(f"Found {len(result['duplicates'])} users with duplicate sessions")
    print(f"Top 5 users by session time:")
    for user_id, total_time in result['top_users'][:5]:
        print(f"  {user_id}: {total_time}s")

    # Generate statistics
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')

    print("\n" + "=" * 80)
    print("PROFILER OUTPUT - Top 20 functions by cumulative time")
    print("=" * 80 + "\n")

    stats.print_stats(20)
    profile_output = s.getvalue()
    print(profile_output)

    # Also save to file
    with open('/Users/kperko/code/evals-for-coding/benchmarks/performance-001/starter-code/profiler_output.txt', 'w') as f:
        f.write("PROFILER OUTPUT - Performance Analysis\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Dataset: {len(logs)} log entries ({1000} users, 5 entries each)\n\n")
        f.write("Top 20 functions by cumulative time:\n")
        f.write("=" * 80 + "\n")
        f.write(profile_output)

    print("\nProfile saved to profiler_output.txt")


if __name__ == "__main__":
    profile_performance()
