"""
Unit Tests for Star OmniEngine 2.0 GN Subsystem
Authoritative Reference: STAR_OMNI_SPEC.md
"""

import unittest
import time
from star_engine.omni.jit import TieredJITEngine, HotspotProfile
from star_engine.omni.fiber import FiberScheduler, OmniFiber, OmniChannel, FiberState
from star_engine.omni.memory import ArenaAllocator, BorrowedBuffer
from star_engine.omni.grid import OmniCluster, OmniNode
from star_engine.omni.ffi import PolyglotFFIEngine
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter


class TestOmniEngine(unittest.TestCase):
    def setUp(self):
        self.scheduler = FiberScheduler(num_workers=2)
        self.jit = TieredJITEngine(hotspot_threshold=10)
        self.arena = ArenaAllocator(capacity_bytes=64 * 1024)
        self.cluster = OmniCluster("test-cluster")
        self.ffi = PolyglotFFIEngine()

    def tearDown(self):
        self.scheduler.shutdown()

    # 1. JIT Subsystem
    def test_jit_profile_and_compilation(self):
        def sample_workload(x, y):
            return x * y + 42

        prof = self.jit.get_profile("sample")
        self.assertFalse(prof.is_compiled)

        for _ in range(9):
            self.assertFalse(prof.record_call())
        # 10th call reaches threshold
        self.assertTrue(prof.record_call())

        compiled = self.jit.compile_function("sample", sample_workload)
        res = compiled(3, 4)
        self.assertEqual(res, 54)
        self.assertTrue(prof.is_compiled)

    def test_jit_benchmark_speedup(self):
        def dummy_calc():
            total = 0
            for i in range(20):
                total += i
            return total

        bench = self.jit.benchmark_speedup("dummy", dummy_calc, iterations=1000)
        self.assertEqual(bench["workload"], "dummy")
        self.assertIn("speedup_factor", bench)

    # 2. Parallel Fibers & Scheduler
    def test_fiber_spawn_and_join(self):
        def compute_square(n):
            return n * n

        fiber = self.scheduler.spawn(compute_square, 9)
        result = fiber.join(timeout=2.0)
        self.assertEqual(result, 81)
        self.assertEqual(fiber.state, FiberState.COMPLETED)
        self.assertGreater(fiber.duration_ms, 0.0)

    def test_fiber_channels_csp(self):
        chan = OmniChannel(capacity=2)
        self.assertTrue(chan.send("packet-A"))
        self.assertTrue(chan.send("packet-B"))
        self.assertEqual(chan.size, 2)

        val1 = chan.recv()
        val2 = chan.recv()
        self.assertEqual(val1, "packet-A")
        self.assertEqual(val2, "packet-B")

        chan.close()
        self.assertTrue(chan.is_closed)

    def test_fiber_parallel_map(self):
        items = [1, 2, 3, 4, 5]
        results = self.scheduler.parallel_map(lambda x: x * 10, items, timeout=2.0)
        self.assertEqual(results, [10, 20, 30, 40, 50])

    # 3. Memory Arena & Borrowed Buffer
    def test_arena_bump_pointer_allocation(self):
        buf1 = self.arena.alloc_text("Hello Star OmniEngine!")
        self.assertEqual(buf1.to_text(), "Hello Star OmniEngine!")
        self.assertEqual(len(buf1), 22)

        # Sub-slicing without copying
        sub = buf1.slice(6, 10)
        self.assertEqual(sub.to_text(), "Star")

        # Stats verification
        st = self.arena.stats()
        self.assertGreater(st["used_bytes"], 0)
        self.assertEqual(st["allocations"], 1)

        # O(1) instant reset
        self.arena.reset()
        st_reset = self.arena.stats()
        self.assertEqual(st_reset["used_bytes"], 0)
        self.assertEqual(st_reset["allocations"], 0)

    # 4. Global Network (GN) Cluster
    def test_grid_cluster_load_balancing_and_scatter_gather(self):
        node_a = OmniNode("node-a", "127.0.0.1", 7001, capabilities=["cpu"])
        node_b = OmniNode("node-b", "127.0.0.1", 7002, capabilities=["cpu", "gpu"])
        self.cluster.register_node(node_a)
        self.cluster.register_node(node_b)

        st = self.cluster.cluster_status()
        self.assertEqual(st["total_nodes"], 3)  # Local + 2 peers

        dataset = [10, 20, 30]
        results = self.cluster.scatter_gather(dataset, lambda x: x * 2)
        self.assertEqual(results, [20, 40, 60])
        self.assertEqual(len(self.cluster.task_history), 3)

    # 5. Polyglot FFI Engine
    def test_polyglot_ffi(self):
        stats = self.ffi.stats()
        self.assertIn("loaded_libraries", stats)
        self.assertIn("platform", stats)

    # 6. Star Language SDK Integration (use Omni)
    def test_omni_star_sdk_execution(self):
        code = """
        use Omni

        variable arena = Omni.arena(64)
        variable text_buf = arena.alloc_text("OmniEngine 2.0 GN")
        variable txt = text_buf.to_text()
        show txt

        variable chan = Omni.channel(2)
        chan.send("event-alpha")
        variable received = chan.recv()
        show received
        """
        out = []
        interp = Interpreter(output_handler=lambda s: out.append(s), source_code=code)
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        interp.interpret(ast)

        self.assertEqual(out, ["OmniEngine 2.0 GN", "event-alpha"])


if __name__ == "__main__":
    unittest.main()
