"""
Thread-unsafe counter with race conditions.

This module demonstrates classic race conditions:
1. Non-atomic increment operations
2. Lost updates when multiple threads increment simultaneously
3. Inconsistent state between related counters
"""

import time


class MetricsCounter:
    """A metrics counter with race conditions."""

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_processing_time = 0.0
        self.request_count = 0

    def record_request(self, success: bool, processing_time: float) -> None:
        """Record a request with its outcome and processing time."""
        # Race condition: multiple non-atomic operations
        self.total_requests += 1

        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

        # Race condition: float addition is not atomic
        self.total_processing_time += processing_time
        self.request_count += 1

    def get_success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_requests == 0:
            return 0.0
        # Race condition: total_requests might change during calculation
        return self.successful_requests / self.total_requests

    def get_average_processing_time(self) -> float:
        """Calculate average processing time."""
        if self.request_count == 0:
            return 0.0
        # Race condition: values might be inconsistent
        return self.total_processing_time / self.request_count

    def get_stats(self) -> dict:
        """Get all statistics."""
        return {
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'success_rate': self.get_success_rate(),
            'avg_processing_time': self.get_average_processing_time()
        }

    def increment_simple(self) -> None:
        """Simple increment operation - demonstrates classic race condition."""
        # Classic read-modify-write race condition
        current = self.total_requests
        # Simulate some processing that makes race condition more likely
        time.sleep(0.0001)
        self.total_requests = current + 1

    def reset(self) -> None:
        """Reset all counters."""
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_processing_time = 0.0
        self.request_count = 0
