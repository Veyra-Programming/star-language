"""
Hardware Test: Hardware Verification Test Runner & Dashboard
"""

import unittest
from star_backend.mobile.hardware.runner import HardwareTestRunner


class TestHardwareRunner(unittest.TestCase):
    def test_run_hardware_suite(self):
        exit_code = HardwareTestRunner.run_hardware_suite()
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
