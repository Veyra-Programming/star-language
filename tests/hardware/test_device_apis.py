"""
Hardware Test: Physical Device Hardware Capabilities
"""

import unittest
from star_backend.mobile.hardware.probes import HardwareProbeSuite, ProbeResultStatus


class TestDeviceAPIsHardware(unittest.TestCase):
    def test_run_all_probes(self):
        probes = HardwareProbeSuite.run_all()
        self.assertGreaterEqual(len(probes), 8)
        # All core simulated/hardware probes should complete without uncaught exceptions
        for p in probes:
            self.assertIn(p.status, [ProbeResultStatus.SUPPORTED, ProbeResultStatus.UNAVAILABLE, ProbeResultStatus.PERMISSION_DENIED])


if __name__ == "__main__":
    unittest.main()
