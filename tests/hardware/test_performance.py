"""
Hardware Test: Frame Rendering Performance & Jitter Profiler
"""

import unittest
import time
from star_backend.mobile.hardware.metrics import PerformanceProfiler


class TestPerformanceHardware(unittest.TestCase):
    def test_frame_metrics_calculation(self):
        profiler = PerformanceProfiler()
        for _ in range(100):
            profiler.record_frame(16.6)

        metrics = profiler.calculate_metrics()
        self.assertGreaterEqual(metrics.avg_fps, 58.0)
        self.assertEqual(metrics.dropped_frames, 0)


if __name__ == "__main__":
    unittest.main()
