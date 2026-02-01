"""
Thread-safe worker pool with proper synchronization.

Fixed issues:
1. Replaced list with thread-safe queue.Queue
2. Added lock to protect worker state and statistics
3. Made result collection thread-safe
4. Protected all state transitions
"""

import time
import queue
import threading
from typing import Callable, Any, List
from enum import Enum


class WorkerState(Enum):
    IDLE = "idle"
    BUSY = "busy"
    STOPPED = "stopped"


class WorkerPool:
    """A simple worker pool with proper thread safety."""

    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.task_queue = queue.Queue()  # Thread-safe queue
        self.results = []
        self.worker_states = [WorkerState.IDLE] * num_workers
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.active_workers = 0
        self.lock = threading.Lock()  # Protect state and statistics

    def submit_task(self, task: Callable[[], Any]) -> None:
        """Submit a task to the pool."""
        # Queue is thread-safe, no lock needed
        self.task_queue.put(task)

    def get_next_task(self, worker_id: int) -> Callable[[], Any]:
        """Get next task from queue."""
        try:
            # Queue is thread-safe with timeout
            task = self.task_queue.get(timeout=0.001)

            # Update worker state atomically
            with self.lock:
                self.worker_states[worker_id] = WorkerState.BUSY
                self.active_workers += 1

            return task
        except queue.Empty:
            return None

    def execute_task(self, worker_id: int, task: Callable[[], Any]) -> None:
        """Execute a task and store result."""
        try:
            result = task()

            # Update results and statistics atomically
            with self.lock:
                self.results.append(result)
                self.completed_tasks += 1

        except Exception as e:
            with self.lock:
                self.failed_tasks += 1
                self.results.append(f"Error: {e}")

        finally:
            # Update worker state atomically
            with self.lock:
                self.worker_states[worker_id] = WorkerState.IDLE
                self.active_workers -= 1

    def get_pending_count(self) -> int:
        """Get number of pending tasks."""
        # Queue.qsize() is thread-safe
        return self.task_queue.qsize()

    def get_results(self) -> List[Any]:
        """Get all results."""
        with self.lock:
            # Return a copy to avoid external modification
            return self.results.copy()

    def get_stats(self) -> dict:
        """Get pool statistics."""
        with self.lock:
            return {
                'pending_tasks': self.task_queue.qsize(),
                'completed_tasks': self.completed_tasks,
                'failed_tasks': self.failed_tasks,
                'active_workers': self.active_workers,
                'idle_workers': sum(1 for s in self.worker_states if s == WorkerState.IDLE)
            }

    def reset(self) -> None:
        """Reset the pool."""
        with self.lock:
            # Clear the queue
            while not self.task_queue.empty():
                try:
                    self.task_queue.get_nowait()
                except queue.Empty:
                    break

            self.results = []
            self.worker_states = [WorkerState.IDLE] * self.num_workers
            self.completed_tasks = 0
            self.failed_tasks = 0
            self.active_workers = 0
