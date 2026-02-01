"""
Test suite for LogProcessor

These tests verify correctness of the log processing functionality.
All tests must continue to pass after optimization.
"""

import pytest
from data_processor import LogProcessor, generate_test_logs


class TestLogProcessor:
    """Test cases for LogProcessor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.processor = LogProcessor()

    def test_load_logs(self):
        """Test loading logs into processor."""
        logs = ["log1", "log2", "log3"]
        self.processor.load_logs(logs)
        assert self.processor.logs == logs

    def test_find_duplicate_sessions_no_duplicates(self):
        """Test finding duplicates when there are none."""
        logs = [
            "[2024-01-01] session_start user_id=user001 duration=10s status=active",
            "[2024-01-02] session_start user_id=user002 duration=20s status=active",
            "[2024-01-03] session_start user_id=user003 duration=30s status=active",
        ]
        self.processor.load_logs(logs)
        duplicates = self.processor.find_duplicate_sessions()
        assert len(duplicates) == 0

    def test_find_duplicate_sessions_with_duplicates(self):
        """Test finding duplicate sessions."""
        logs = [
            "[2024-01-01] session_start user_id=user001 duration=10s status=active",
            "[2024-01-02] session_start user_id=user002 duration=20s status=active",
            "[2024-01-03] session_start user_id=user001 duration=15s status=active",
            "[2024-01-04] session_start user_id=user003 duration=30s status=active",
            "[2024-01-05] session_start user_id=user002 duration=25s status=active",
        ]
        self.processor.load_logs(logs)
        duplicates = self.processor.find_duplicate_sessions()

        # Should find user001 and user002 as duplicates
        assert len(duplicates) == 2

        # Convert to dict for easier checking
        dup_dict = {user_id: lines for user_id, lines in duplicates}

        assert "user001" in dup_dict
        assert "user002" in dup_dict
        assert sorted(dup_dict["user001"]) == [0, 2]
        assert sorted(dup_dict["user002"]) == [1, 4]

    def test_compute_session_stats_empty(self):
        """Test computing stats with no logs."""
        self.processor.load_logs([])
        stats = self.processor.compute_session_stats()
        assert stats == {}

    def test_compute_session_stats_single_user(self):
        """Test computing stats for a single user."""
        logs = [
            "[2024-01-01] session_start user_id=user001 duration=10s status=active",
            "[2024-01-02] session_start user_id=user001 duration=20s status=active",
            "[2024-01-03] session_start user_id=user001 duration=30s status=active",
        ]
        self.processor.load_logs(logs)
        stats = self.processor.compute_session_stats()

        assert len(stats) == 1
        assert stats["user001"] == 60

    def test_compute_session_stats_multiple_users(self):
        """Test computing stats for multiple users."""
        logs = [
            "[2024-01-01] session_start user_id=user001 duration=10s status=active",
            "[2024-01-02] session_start user_id=user002 duration=20s status=active",
            "[2024-01-03] session_start user_id=user001 duration=15s status=active",
            "[2024-01-04] session_start user_id=user003 duration=30s status=active",
            "[2024-01-05] session_start user_id=user002 duration=25s status=active",
        ]
        self.processor.load_logs(logs)
        stats = self.processor.compute_session_stats()

        assert len(stats) == 3
        assert stats["user001"] == 25  # 10 + 15
        assert stats["user002"] == 45  # 20 + 25
        assert stats["user003"] == 30

    def test_get_top_users_empty(self):
        """Test getting top users with empty stats."""
        top = self.processor.get_top_users({}, n=5)
        assert top == []

    def test_get_top_users_sorted_correctly(self):
        """Test that top users are sorted by session time descending."""
        stats = {
            "user001": 100,
            "user002": 50,
            "user003": 200,
            "user004": 75,
            "user005": 150,
        }
        top = self.processor.get_top_users(stats, n=3)

        assert len(top) == 3
        assert top[0] == ("user003", 200)
        assert top[1] == ("user005", 150)
        assert top[2] == ("user001", 100)

    def test_get_top_users_limit_respected(self):
        """Test that n parameter limits results."""
        stats = {f"user{i:03d}": i * 10 for i in range(20)}
        top = self.processor.get_top_users(stats, n=5)

        assert len(top) == 5
        # Should be in descending order
        for i in range(len(top) - 1):
            assert top[i][1] >= top[i + 1][1]

    def test_process_all_integration(self):
        """Integration test for full processing pipeline."""
        logs = [
            "[2024-01-01] session_start user_id=user001 duration=10s status=active",
            "[2024-01-02] session_start user_id=user002 duration=20s status=active",
            "[2024-01-03] session_start user_id=user001 duration=15s status=active",
            "[2024-01-04] session_start user_id=user003 duration=30s status=active",
            "[2024-01-05] session_start user_id=user002 duration=25s status=active",
        ]
        self.processor.load_logs(logs)
        result = self.processor.process_all()

        # Check structure
        assert "duplicates" in result
        assert "stats" in result
        assert "top_users" in result

        # Check duplicates
        assert len(result["duplicates"]) == 2

        # Check stats
        assert result["stats"]["user001"] == 25
        assert result["stats"]["user002"] == 45
        assert result["stats"]["user003"] == 30

        # Check top users
        assert result["top_users"][0][0] == "user002"
        assert result["top_users"][0][1] == 45

    def test_large_dataset_correctness(self):
        """Test correctness with larger dataset."""
        logs = generate_test_logs(num_users=100, entries_per_user=3)
        self.processor.load_logs(logs)
        result = self.processor.process_all()

        # All users should have duplicates (3 entries each)
        assert len(result["duplicates"]) == 100

        # Each user should have exactly 3 entries
        for user_id, line_nums in result["duplicates"]:
            assert len(line_nums) == 3

        # Stats should exist for all users
        assert len(result["stats"]) == 100

    def test_generate_test_logs(self):
        """Test the test data generator."""
        logs = generate_test_logs(num_users=10, entries_per_user=5)

        assert len(logs) == 50  # 10 users * 5 entries

        # Check format
        for log in logs:
            assert "user_id=" in log
            assert "duration=" in log
            assert "status=" in log


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
