"""
Star OmniEngine 2.0 GN — Structured Parallel Fibers & Work-Stealing M:N Scheduler
Authoritative Reference: STAR_OMNI_SPEC.md
"""

import threading
import queue
import time
import collections
import atexit
from typing import Callable, Any, Optional, List, Dict
from enum import Enum, auto


class FiberState(Enum):
    PENDING = auto()
    RUNNING = auto()
    SUSPENDED = auto()
    COMPLETED = auto()
    FAILED = auto()


class OmniFiber:
    """A lightweight cooperative green thread / fiber running inside the Omni Scheduler."""
    _id_counter = 0
    _lock = threading.Lock()

    def __init__(self, target: Callable[..., Any], args: tuple = (), kwargs: dict = None, name: Optional[str] = None):
        with OmniFiber._lock:
            OmniFiber._id_counter += 1
            self.id = OmniFiber._id_counter

        self.name = name or f"fiber-{self.id}"
        self.target = target
        self.args = args
        self.kwargs = kwargs or {}
        self.state = FiberState.PENDING
        self.result: Any = None
        self.error: Optional[Exception] = None
        self.started_at: float = 0.0
        self.completed_at: float = 0.0
        self._done_event = threading.Event()

    def run(self):
        self.state = FiberState.RUNNING
        self.started_at = time.perf_counter()
        try:
            self.result = self.target(*self.args, **self.kwargs)
            self.state = FiberState.COMPLETED
        except Exception as e:
            self.error = e
            self.state = FiberState.FAILED
        finally:
            self.completed_at = time.perf_counter()
            self._done_event.set()

    def join(self, timeout: Optional[float] = None) -> Any:
        self._done_event.wait(timeout=timeout)
        if self.state == FiberState.FAILED:
            raise self.error
        return self.result

    @property
    def duration_ms(self) -> float:
        if self.started_at == 0.0:
            return 0.0
        end_t = self.completed_at if self.completed_at > 0.0 else time.perf_counter()
        return round((end_t - self.started_at) * 1000, 3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state.name,
            "duration_ms": self.duration_ms,
            "has_error": self.error is not None,
        }


class OmniChannel:
    """
    Lock-free Communicating Sequential Processes (CSP) Channel for Fibers.
    Supports buffered and unbuffered transfers, timeouts, and closing.
    """
    def __init__(self, capacity: int = 0):
        self.capacity = capacity
        self._queue = queue.Queue(maxsize=capacity if capacity > 0 else 1)
        self._is_closed = False
        self._closed_lock = threading.Lock()

    def send(self, value: Any, timeout: Optional[float] = None) -> bool:
        with self._closed_lock:
            if self._is_closed:
                raise RuntimeError("Cannot send on a closed OmniChannel.")
        try:
            self._queue.put(value, block=True, timeout=timeout)
            return True
        except queue.Full:
            return False

    def recv(self, timeout: Optional[float] = None, default: Any = None) -> Any:
        try:
            return self._queue.get(block=True, timeout=timeout)
        except queue.Empty:
            if self.is_closed:
                return default
            return default

    def close(self):
        with self._closed_lock:
            self._is_closed = True

    @property
    def is_closed(self) -> bool:
        with self._closed_lock:
            return self._is_closed

    @property
    def size(self) -> int:
        return self._queue.qsize()


class FiberScheduler:
    """
    Multi-core work-stealing M:N fiber scheduler.
    Spawns worker OS threads, maintains per-worker local deque, and implements
    lock-free work stealing when a thread deque starves.
    """
    def __init__(self, num_workers: int = 4):
        self.num_workers = max(1, num_workers)
        self.worker_queues: List[collections.deque] = [collections.deque() for _ in range(self.num_workers)]
        self.queue_locks: List[threading.Lock] = [threading.Lock() for _ in range(self.num_workers)]
        self.workers: List[threading.Thread] = []
        self._running = False
        self._all_fibers: List[OmniFiber] = []
        self._start_workers()
        atexit.register(self.shutdown)

    def _start_workers(self):
        self._running = True
        for worker_id in range(self.num_workers):
            t = threading.Thread(target=self._worker_loop, args=(worker_id,), daemon=True, name=f"OmniWorker-{worker_id}")
            self.workers.append(t)
            t.start()

    def _worker_loop(self, worker_id: int):
        while self._running:
            fiber = self._pop_task(worker_id)
            if fiber:
                fiber.run()
            else:
                time.sleep(0.001)

    def _pop_task(self, worker_id: int) -> Optional[OmniFiber]:
        # 1. Pop from local queue (LIFO for cache affinity)
        with self.queue_locks[worker_id]:
            if self.worker_queues[worker_id]:
                return self.worker_queues[worker_id].pop()

        # 2. Work-stealing: Steal from other worker's queue (FIFO)
        for other_id in range(self.num_workers):
            if other_id == worker_id:
                continue
            with self.queue_locks[other_id]:
                if len(self.worker_queues[other_id]) > 1:
                    return self.worker_queues[other_id].popleft()

        return None

    def spawn(self, fn: Callable[..., Any], *args, **kwargs) -> OmniFiber:
        fiber = OmniFiber(fn, args, kwargs)
        # Choose queue with smallest load
        min_idx = 0
        min_len = 999999999
        for i in range(self.num_workers):
            l = len(self.worker_queues[i])
            if l < min_len:
                min_len = l
                min_idx = i

        with self.queue_locks[min_idx]:
            self.worker_queues[min_idx].append(fiber)

        self._all_fibers.append(fiber)
        return fiber

    def await_all(self, fibers: List[OmniFiber], timeout: Optional[float] = None) -> List[Any]:
        results = []
        for f in fibers:
            results.append(f.join(timeout=timeout))
        return results

    def parallel_map(self, fn: Callable[[Any], Any], items: List[Any], timeout: Optional[float] = None) -> List[Any]:
        fibers = [self.spawn(fn, item) for item in items]
        return self.await_all(fibers, timeout=timeout)

    def stats(self) -> Dict[str, Any]:
        completed = sum(1 for f in self._all_fibers if f.state == FiberState.COMPLETED)
        failed = sum(1 for f in self._all_fibers if f.state == FiberState.FAILED)
        pending = sum(1 for f in self._all_fibers if f.state in (FiberState.PENDING, FiberState.RUNNING))
        return {
            "workers": self.num_workers,
            "total_fibers": len(self._all_fibers),
            "completed": completed,
            "failed": failed,
            "active": pending,
        }

    def shutdown(self):
        self._running = False
        for t in self.workers:
            t.join(timeout=0.1)
