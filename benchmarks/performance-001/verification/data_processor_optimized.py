"""
Optimized Data Processor - Reference Solution

This is the optimized version that should be 10x+ faster.

Key optimizations:
1. Parse logs once and cache results (avoid repeated regex matching)
2. Use dict/defaultdict for O(1) lookups instead of O(n) linear searches
3. Use built-in sorted() instead of bubble sort O(n log n) vs O(n²)
4. Eliminate redundant iterations
"""

import re
from typing import List, Dict, Tuple
from collections import defaultdict


class LogProcessor:
    """Optimized LogProcessor with better algorithms and data structures."""

    def __init__(self):
        self.logs = []
        self._parsed_logs = None

    def load_logs(self, log_entries: List[str]) -> None:
        """Load log entries for processing."""
        self.logs = log_entries
        # Invalidate cache when new logs are loaded
        self._parsed_logs = None

    def _parse_logs_once(self) -> List[Tuple[str, int]]:
        """
        Parse all logs once and cache the results.

        Returns:
            List of (user_id, duration) tuples
        """
        if self._parsed_logs is not None:
            return self._parsed_logs

        parsed = []
        for log in self.logs:
            # Parse both user_id and duration in one pass
            user_match = re.search(r'user_id=(\w+)', log)
            duration_match = re.search(r'duration=(\d+)', log)

            if user_match and duration_match:
                user_id = user_match.group(1)
                duration = int(duration_match.group(1))
                parsed.append((user_id, duration))

        self._parsed_logs = parsed
        return parsed

    def find_duplicate_sessions(self) -> List[Tuple[str, List[int]]]:
        """
        Find all duplicate user sessions in the logs.

        Optimized to O(n) using a hash map instead of O(n²) nested loops.

        Returns:
            List of tuples (user_id, [line_numbers]) for users with duplicate sessions
        """
        # Parse logs once
        parsed_logs = self._parse_logs_once()

        # Build index of user_id -> list of line numbers (O(n) single pass)
        user_indices = defaultdict(list)
        for i, (user_id, _) in enumerate(parsed_logs):
            user_indices[user_id].append(i)

        # Filter for users with duplicates (more than one entry)
        duplicates = [
            (user_id, line_nums)
            for user_id, line_nums in user_indices.items()
            if len(line_nums) > 1
        ]

        return duplicates

    def compute_session_stats(self) -> Dict[str, int]:
        """
        Compute session duration statistics for each user.

        Optimized to parse logs once and use O(1) dict operations.

        Returns:
            Dictionary mapping user_id to total session time in seconds
        """
        # Parse logs once
        parsed_logs = self._parse_logs_once()

        # Aggregate durations using defaultdict (O(n) single pass)
        stats = defaultdict(int)
        for user_id, duration in parsed_logs:
            stats[user_id] += duration

        return dict(stats)

    def get_top_users(self, stats: Dict[str, int], n: int = 10) -> List[Tuple[str, int]]:
        """
        Get top N users by session time.

        Optimized to use built-in sorted() which is O(n log n) instead of
        bubble sort which is O(n²).

        Args:
            stats: Dictionary of user_id -> total_time
            n: Number of top users to return

        Returns:
            List of (user_id, total_time) tuples, sorted by time descending
        """
        # Use built-in sorted with key parameter (O(n log n))
        sorted_items = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:n]

    def process_all(self) -> Dict:
        """
        Run full analysis pipeline.

        Returns:
            Dictionary with duplicates and top users
        """
        # Parse logs once at the start
        self._parse_logs_once()

        # All methods now use the cached parsed data
        duplicates = self.find_duplicate_sessions()
        stats = self.compute_session_stats()
        top_users = self.get_top_users(stats)

        return {
            'duplicates': duplicates,
            'stats': stats,
            'top_users': top_users
        }


def generate_test_logs(num_users: int = 1000, entries_per_user: int = 5) -> List[str]:
    """Generate test log data."""
    logs = []
    for user_num in range(num_users):
        user_id = f"user{user_num:04d}"
        for entry_num in range(entries_per_user):
            duration = (user_num + entry_num) % 100 + 10
            logs.append(
                f"[2024-01-{(entry_num % 28) + 1:02d}] session_start user_id={user_id} duration={duration}s status=active"
            )
    return logs


if __name__ == "__main__":
    # Demo usage
    processor = LogProcessor()
    logs = generate_test_logs(num_users=1000, entries_per_user=5)
    processor.load_logs(logs)

    print("Processing logs...")
    import time
    start = time.time()
    result = processor.process_all()
    elapsed = time.time() - start

    print(f"\nProcessed {len(logs)} log entries in {elapsed:.2f} seconds")
    print(f"Found {len(result['duplicates'])} users with duplicate sessions")
    print(f"\nTop 5 users by session time:")
    for user_id, total_time in result['top_users'][:5]:
        print(f"  {user_id}: {total_time}s")
