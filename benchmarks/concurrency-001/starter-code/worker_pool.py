"""
Thread-unsafe worker pool with race conditions.

This worker pool has several concurrency issues:
1. Race conditions in task queue management
2. Unsafe state transitions for workers
3. Non-atomic updates to shared state
"""

import time
from typing import Callable, Any, List
from enum import Enum


class WorkerState(Enum):
    IDLE = "idle"
    BUSY = "busy"
    STOPPED = "stopped"


class WorkerPool:
    """A simple worker pool with race conditions."""

    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.task_queue = []  # Not thread-safe
        self.results = []  # Not thread-safe
        self.worker_states = [WorkerState.IDLE] * num_workers
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.active_workers = 0

    def submit_task(self, task: Callable[[], Any]) -> None:
        """Submit a task to the pool."""
        # Race condition: list append is not atomic for our purposes
        self.task_queue.append(task)

    def get_next_task(self, worker_id: int) -> Callable[[], Any]:
        """Get next task from queue."""
        # Race condition: check-then-act pattern
        if len(self.task_queue) == 0:
            return None

        # Race condition: multiple workers might get same task
        # or list might be modified by another thread
        task = self.task_queue[0]
        self.task_queue = self.task_queue[1:]

        # Race condition: state update not synchronized with task removal
        self.worker_states[worker_id] = WorkerState.BUSY
        self.active_workers += 1

        return task

    def execute_task(self, worker_id: int, task: Callable[[], Any]) -> None:
        """Execute a task and store result."""
        try:
            result = task()
            # Race condition: appending to shared list
            self.results.append(result)
            # Race condition: increment not atomic
            self.completed_tasks += 1
        except Exception as e:
            # Race condition: increment not atomic
            self.failed_tasks += 1
            self.results.append(f"Error: {e}")
        finally:
            # Race condition: state updates not atomic
            self.worker_states[worker_id] = WorkerState.IDLE
            self.active_workers -= 1

    def get_pending_count(self) -> int:
        """Get number of pending tasks."""
        # Race condition: list might be modified during len() call
        return len(self.task_queue)

    def get_results(self) -> List[Any]:
        """Get all results."""
        # Race condition: returning reference to mutable shared list
        return self.results

    def get_stats(self) -> dict:
        """Get pool statistics."""
        # Race condition: multiple reads of shared state
        return {
            'pending_tasks': len(self.task_queue),
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'active_workers': self.active_workers,
            'idle_workers': sum(1 for s in self.worker_states if s == WorkerState.IDLE)
        }

    def reset(self) -> None:
        """Reset the pool."""
        self.task_queue = []
        self.results = []
        self.worker_states = [WorkerState.IDLE] * self.num_workers
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.active_workers = 0
