"""
Tests that expose race conditions in the concurrent code.

These tests are designed to fail intermittently with the buggy code
and pass consistently with properly synchronized code.
"""

import threading
import time
import random
from cache import SimpleCache
from counter import MetricsCounter
from worker_pool import WorkerPool


def test_cache_concurrent_access():
    """Test cache with concurrent reads and writes."""
    cache = SimpleCache(max_size=50)
    errors = []
    num_threads = 10
    operations_per_thread = 1000

    def worker(thread_id):
        try:
            for i in range(operations_per_thread):
                key = f"key_{i % 100}"
                value = f"value_{thread_id}_{i}"

                # Mix of reads and writes
                if i % 3 == 0:
                    cache.put(key, value)
                else:
                    cache.get(key)

        except Exception as e:
            errors.append(f"Thread {thread_id}: {e}")

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Check for errors
    assert len(errors) == 0, f"Encountered errors: {errors}"

    # Verify cache stats are consistent
    stats = cache.get_stats()
    # Only get() operations count in stats (2 out of 3 operations are gets)
    expected_get_operations = num_threads * operations_per_thread * 2 // 3
    # Allow some tolerance for the division
    actual_total = stats['hits'] + stats['misses']
    assert abs(actual_total - expected_get_operations) <= num_threads, \
        f"Stats inconsistent: hits={stats['hits']}, misses={stats['misses']}, expected ~{expected_get_operations}, got {actual_total}"

    print(f"Cache test passed: {stats}")


def test_counter_concurrent_increments():
    """Test counter with concurrent increments."""
    counter = MetricsCounter()
    num_threads = 20
    increments_per_thread = 1000
    expected_total = num_threads * increments_per_thread

    def worker():
        for _ in range(increments_per_thread):
            # Simulate request recording
            success = random.random() > 0.1  # 90% success rate
            processing_time = random.uniform(0.001, 0.1)
            counter.record_request(success, processing_time)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Verify counts are correct
    stats = counter.get_stats()
    assert stats['total_requests'] == expected_total, \
        f"Expected {expected_total} total requests, got {stats['total_requests']}"

    assert stats['successful_requests'] + stats['failed_requests'] == expected_total, \
        f"Success + failed ({stats['successful_requests']} + {stats['failed_requests']}) != total ({expected_total})"

    # Verify success rate is reasonable (should be around 90%)
    success_rate = stats['success_rate']
    assert 0.85 < success_rate < 0.95, \
        f"Success rate {success_rate} outside expected range (0.85-0.95)"

    print(f"Counter test passed: {stats}")


def test_counter_simple_increment():
    """Test simple counter increment - demonstrates classic race condition."""
    counter = MetricsCounter()
    num_threads = 50
    increments_per_thread = 100
    expected_total = num_threads * increments_per_thread

    def worker():
        for _ in range(increments_per_thread):
            counter.increment_simple()

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert counter.total_requests == expected_total, \
        f"Expected {expected_total} total requests, got {counter.total_requests}"

    print(f"Simple increment test passed: {counter.total_requests}")


def test_worker_pool_concurrent_tasks():
    """Test worker pool with concurrent task submission and execution."""
    pool = WorkerPool(num_workers=4)
    num_task_submitters = 5
    tasks_per_submitter = 200
    total_tasks = num_task_submitters * tasks_per_submitter

    def sample_task():
        """A simple task that returns a value."""
        time.sleep(0.0001)  # Simulate work
        return random.randint(1, 100)

    def task_submitter():
        """Submit tasks to the pool."""
        for _ in range(tasks_per_submitter):
            pool.submit_task(sample_task)

    def task_executor(worker_id):
        """Execute tasks from the pool."""
        # Execute tasks until queue is empty
        while True:
            task = pool.get_next_task(worker_id)
            if task:
                pool.execute_task(worker_id, task)
            else:
                # Check if there are really no more tasks
                if pool.get_pending_count() == 0:
                    # Double-check after a short wait
                    time.sleep(0.01)
                    if pool.get_pending_count() == 0:
                        break
                time.sleep(0.001)  # Wait for more tasks

    # Start task submitters
    submitter_threads = []
    for i in range(num_task_submitters):
        t = threading.Thread(target=task_submitter)
        submitter_threads.append(t)
        t.start()

    # Wait for submissions to complete
    for t in submitter_threads:
        t.join()

    # Start task executors
    executor_threads = []
    for i in range(pool.num_workers):
        t = threading.Thread(target=task_executor, args=(i,))
        executor_threads.append(t)
        t.start()

    # Wait for execution to complete
    for t in executor_threads:
        t.join()

    # Verify all tasks were completed
    stats = pool.get_stats()
    results = pool.get_results()

    assert stats['completed_tasks'] == total_tasks, \
        f"Expected {total_tasks} completed tasks, got {stats['completed_tasks']}"

    assert len(results) == total_tasks, \
        f"Expected {total_tasks} results, got {len(results)}"

    assert stats['pending_tasks'] == 0, \
        f"Expected 0 pending tasks, got {stats['pending_tasks']}"

    print(f"Worker pool test passed: {stats}")


def test_all():
    """Run all tests."""
    print("Running cache concurrent access test...")
    test_cache_concurrent_access()

    print("\nRunning counter concurrent increments test...")
    test_counter_concurrent_increments()

    print("\nRunning counter simple increment test...")
    test_counter_simple_increment()

    print("\nRunning worker pool concurrent tasks test...")
    test_worker_pool_concurrent_tasks()

    print("\n✓ All tests passed!")


if __name__ == "__main__":
    test_all()
