# Solution Guide for Concurrency-001

This document explains the race conditions in the starter code and how to fix them.

## Overview of Race Conditions

The starter code contains three modules with realistic concurrency bugs that cause intermittent test failures. All bugs stem from accessing shared mutable state without proper synchronization.

## Module 1: cache.py

### Problems

1. **Check-then-act race condition in get()**
   ```python
   if key in self.cache:
       self.hits += 1  # Race condition!
       return self.cache[key]
   ```
   Thread A checks `key in self.cache` (true), but before it can increment hits, Thread B deletes the key. Thread A crashes or returns None.

2. **Non-atomic statistics updates**
   ```python
   self.hits += 1  # Read-modify-write is NOT atomic
   ```
   If two threads execute this simultaneously, updates can be lost.

3. **Unsafe eviction logic**
   ```python
   if len(self.cache) >= self.max_size:  # Check
       first_key = next(iter(self.cache))
       del self.cache[first_key]  # Act - not atomic with check!
   self.cache[key] = value
   ```

### Solution

Add a `threading.Lock` and protect all critical sections:

```python
def __init__(self, max_size: int = 100):
    self.cache = {}
    self.max_size = max_size
    self.hits = 0
    self.misses = 0
    self.lock = threading.Lock()  # Add lock

def get(self, key: str) -> Optional[Any]:
    with self.lock:  # Protect entire operation
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None

def put(self, key: str, value: Any) -> None:
    with self.lock:  # Make eviction and insertion atomic
        if len(self.cache) >= self.max_size and key not in self.cache:
            if self.cache:
                first_key = next(iter(self.cache))
                del self.cache[first_key]
        self.cache[key] = value
```

## Module 2: counter.py

### Problems

1. **Non-atomic increment operations**
   ```python
   self.total_requests += 1  # NOT atomic!
   ```
   The `+=` operator is actually three operations: read, add, write. Two threads can both read 5, add 1, and write 6 (losing one increment).

2. **Inconsistent state between related counters**
   ```python
   self.total_requests += 1
   if success:
       self.successful_requests += 1
   else:
       self.failed_requests += 1
   ```
   If another thread reads between these lines, it sees inconsistent state.

3. **Classic read-modify-write race**
   ```python
   current = self.total_requests
   time.sleep(0.0001)  # Makes the bug obvious
   self.total_requests = current + 1  # Lost updates!
   ```

### Solution

Add a `threading.Lock` to protect all counter operations:

```python
def __init__(self):
    self.total_requests = 0
    self.successful_requests = 0
    self.failed_requests = 0
    self.total_processing_time = 0.0
    self.request_count = 0
    self.lock = threading.Lock()  # Add lock

def record_request(self, success: bool, processing_time: float) -> None:
    with self.lock:  # Make all updates atomic
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        self.total_processing_time += processing_time
        self.request_count += 1

def get_stats(self) -> dict:
    with self.lock:  # Ensure consistent snapshot
        success_rate = self.successful_requests / self.total_requests if self.total_requests > 0 else 0.0
        avg_time = self.total_processing_time / self.request_count if self.request_count > 0 else 0.0
        return {
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'success_rate': success_rate,
            'avg_processing_time': avg_time
        }
```

## Module 3: worker_pool.py

### Problems

1. **Unsafe list-based task queue**
   ```python
   if len(self.task_queue) == 0:  # Check
       return None
   task = self.task_queue[0]  # Act - race condition!
   self.task_queue = self.task_queue[1:]
   ```
   Two workers can both check (queue not empty), then both try to get task[0].

2. **Non-atomic state updates**
   ```python
   self.worker_states[worker_id] = WorkerState.BUSY
   self.active_workers += 1  # Not atomic with above
   ```

3. **Unsafe result collection**
   ```python
   self.results.append(result)  # List operations aren't always thread-safe
   ```

### Solution

Use `queue.Queue` (thread-safe) for tasks and a lock for state:

```python
import queue  # Thread-safe queue
import threading

def __init__(self, num_workers: int = 4):
    self.num_workers = num_workers
    self.task_queue = queue.Queue()  # Thread-safe queue!
    self.results = []
    self.worker_states = [WorkerState.IDLE] * num_workers
    self.completed_tasks = 0
    self.failed_tasks = 0
    self.active_workers = 0
    self.lock = threading.Lock()  # Protect state

def submit_task(self, task: Callable[[], Any]) -> None:
    self.task_queue.put(task)  # Queue is thread-safe

def get_next_task(self, worker_id: int) -> Callable[[], Any]:
    try:
        task = self.task_queue.get(timeout=0.001)  # Thread-safe get
        with self.lock:  # Protect state update
            self.worker_states[worker_id] = WorkerState.BUSY
            self.active_workers += 1
        return task
    except queue.Empty:
        return None

def execute_task(self, worker_id: int, task: Callable[[], Any]) -> None:
    try:
        result = task()
        with self.lock:  # Atomic result storage
            self.results.append(result)
            self.completed_tasks += 1
    except Exception as e:
        with self.lock:
            self.failed_tasks += 1
            self.results.append(f"Error: {e}")
    finally:
        with self.lock:  # Atomic state update
            self.worker_states[worker_id] = WorkerState.IDLE
            self.active_workers -= 1
```

## Key Principles

1. **Identify Shared Mutable State**: Any variable accessed by multiple threads
2. **Use Locks for Critical Sections**: Operations that must be atomic
3. **Avoid Check-Then-Act**: Always hold the lock from check to act
4. **Make Related Updates Atomic**: Update related variables together
5. **Use Thread-Safe Data Structures**: Like `queue.Queue` for queues
6. **Use Context Managers**: `with lock:` ensures proper lock release

## Common Mistakes to Avoid

1. **Locking too little**: Only protecting part of a critical section
2. **Locking too much**: Holding locks longer than needed
3. **Deadlocks**: Acquiring multiple locks in different order
4. **Assuming `+=` is atomic**: It's not!
5. **Reading without locks**: Even reads need protection for consistency

## Testing

The fixed code should pass all tests 100 times consecutively:

```bash
cd reference-solution
for i in {1..100}; do python3 test_concurrency.py || break; done
```

All 100 runs should complete without errors.
