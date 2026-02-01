"""
Thread-safe counter with proper synchronization.

Fixed issues:
1. Added lock to protect all counter operations
2. Made all increments atomic
3. Ensured related counters are updated together
4. Protected read operations for consistency
"""

import time
import threading


class MetricsCounter:
    """A metrics counter with proper thread safety."""

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_processing_time = 0.0
        self.request_count = 0
        self.lock = threading.Lock()

    def record_request(self, success: bool, processing_time: float) -> None:
        """Record a request with its outcome and processing time."""
        with self.lock:
            # All updates are now atomic
            self.total_requests += 1

            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1

            self.total_processing_time += processing_time
            self.request_count += 1

    def get_success_rate(self) -> float:
        """Calculate success rate."""
        with self.lock:
            if self.total_requests == 0:
                return 0.0
            return self.successful_requests / self.total_requests

    def get_average_processing_time(self) -> float:
        """Calculate average processing time."""
        with self.lock:
            if self.request_count == 0:
                return 0.0
            return self.total_processing_time / self.request_count

    def get_stats(self) -> dict:
        """Get all statistics."""
        with self.lock:
            success_rate = self.successful_requests / self.total_requests if self.total_requests > 0 else 0.0
            avg_time = self.total_processing_time / self.request_count if self.request_count > 0 else 0.0
            return {
                'total_requests': self.total_requests,
                'successful_requests': self.successful_requests,
                'failed_requests': self.failed_requests,
                'success_rate': success_rate,
                'avg_processing_time': avg_time
            }

    def increment_simple(self) -> None:
        """Simple increment operation - now thread-safe."""
        with self.lock:
            # The entire read-modify-write is now atomic
            current = self.total_requests
            # Simulate some processing
            time.sleep(0.0001)
            self.total_requests = current + 1

    def reset(self) -> None:
        """Reset all counters."""
        with self.lock:
            self.total_requests = 0
            self.successful_requests = 0
            self.failed_requests = 0
            self.total_processing_time = 0.0
            self.request_count = 0
