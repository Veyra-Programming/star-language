"""
Unit Tests for Star 1.0 Universal Platform GA
"""

import unittest
import star_engine
from star_runtime.abi import ABI_VERSION
from star_runtime.mobile.abi import MOBILE_ABI_VERSION
from star_backend.mobile.certification import ReleaseCertificationEngine


class TestStar10Universal(unittest.TestCase):
    def test_version_1_0_0(self):
        self.assertTrue(star_engine.__version__.startswith("1."))

    def test_abi_versions_locked_v1(self):
        self.assertEqual(ABI_VERSION, 1)
        self.assertEqual(MOBILE_ABI_VERSION, 1)

    def test_star_1_0_full_certification(self):
        status = ReleaseCertificationEngine.certify("examples/mobile/benchmark.star")
        self.assertEqual(status, 0)


if __name__ == "__main__":
    unittest.main()
