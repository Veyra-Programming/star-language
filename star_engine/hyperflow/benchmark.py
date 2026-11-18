"""
Star HyperFlow Engine — Built-In HTTP Performance & Scalability Benchmarking Suite
Authoritative Reference: STAR_BENCHMARK_SPEC.md

Usage:
  star server:bench http://localhost:8080/api/users --requests 1000 --concurrency 20
"""

import time
import urllib.request
import urllib.error
import threading
from typing import Dict, Any, List


class BenchmarkResult:
    def __init__(self):
        self.total_requests = 0
        self.completed = 0
        self.failed = 0
        self.latencies: List[float] = []
        self.status_codes: Dict[int, int] = {}
        self.total_bytes = 0
        self.start_time = 0.0
        self.end_time = 0.0
        self._lock = threading.Lock()

    def record_success(self, latency_ms: float, status_code: int, byte_len: int):
        with self._lock:
            self.completed += 1
            self.latencies.append(latency_ms)
            self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1
            self.total_bytes += byte_len

    def record_failure(self):
        with self._lock:
            self.failed += 1

    def print_report(self, url: str, concurrency: int):
        duration = max(self.end_time - self.start_time, 0.001)
        rps = self.completed / duration
        sorted_lats = sorted(self.latencies) if self.latencies else [0.0]
        n = len(sorted_lats)
        
        def pct(p: float) -> float:
            idx = int(n * (p / 100.0))
            return sorted_lats[min(idx, n - 1)]

        avg_lat = sum(sorted_lats) / n if n > 0 else 0.0
        mb_transferred = self.total_bytes / (1024 * 1024)
        throughput_mb_s = mb_transferred / duration

        print("\n" + "=" * 65)
        print("⚡ STAR HYPERFLOW BENCHMARK REPORT")
        print("=" * 65)
        print(f"Target URL:            {url}")
        print(f"Concurrency Level:     {concurrency} worker threads")
        print(f"Total Requests:        {self.total_requests}")
        print(f"Completed Requests:    {self.completed} ({(self.completed/max(self.total_requests,1))*100:.1f}%)")
        print(f"Failed Requests:       {self.failed}")
        print(f"Total Time Taken:      {duration:.3f} seconds")
        print(f"Throughput (RPS):      {rps:.2f} requests/sec")
        print(f"Transfer Rate:         {throughput_mb_s:.2f} MB/sec ({self.total_bytes / 1024:.1f} KB total)")
        print("\nLatency Percentiles (Response Time):")
        print(f"  Fastest (Min):       {sorted_lats[0]:.2f} ms")
        print(f"  50% Median (p50):    {pct(50):.2f} ms")
        print(f"  90% Tail   (p90):    {pct(90):.2f} ms")
        print(f"  95% High   (p95):    {pct(95):.2f} ms")
        print(f"  99% Peak   (p99):    {pct(99):.2f} ms")
        print(f"  Slowest (Max):       {sorted_lats[-1]:.2f} ms")
        print(f"  Average:             {avg_lat:.2f} ms")
        print("\nStatus Codes Distribution:")
        for code, count in sorted(self.status_codes.items()):
            print(f"  HTTP {code}:            {count} responses")
        print("=" * 65)
        if self.failed == 0 and rps > 100:
            print("🚀 STATUS: OPTIMAL & SMOOTH PERFORMANCE CERTIFIED")
        else:
            print("✓ STATUS: BENCHMARK RUN COMPLETED")
        print("=" * 65 + "\n")


def run_benchmark(url: str, requests: int = 500, concurrency: int = 10) -> BenchmarkResult:
    result = BenchmarkResult()
    result.total_requests = requests
    reqs_per_worker = requests // concurrency
    rem = requests % concurrency

    print(f"🚀 Benchmarking {url} with {requests} requests across {concurrency} threads...")
    result.start_time = time.time()

    def _worker(count: int):
        for _ in range(count):
            t0 = time.time()
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "StarHyperFlow-Bench/1.3.0"})
                with urllib.request.urlopen(req, timeout=5.0) as resp:
                    data = resp.read()
                    lat = (time.time() - t0) * 1000.0
                    result.record_success(lat, resp.status, len(data))
            except urllib.error.HTTPError as e:
                lat = (time.time() - t0) * 1000.0
                result.record_success(lat, e.code, 0)
            except Exception:
                result.record_failure()

    threads = []
    for i in range(concurrency):
        c = reqs_per_worker + (1 if i < rem else 0)
        t = threading.Thread(target=_worker, args=(c,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    result.end_time = time.time()
    result.print_report(url, concurrency)
    return result
