"""
Unit Tests for Star Production SDK Bundle & Source Exclusion Gate
"""

import unittest
import tempfile
import os
import shutil
import zipfile
from star_distribution.builder import ProductionDistributionBuilder, SourceExclusionViolationError


class TestProductionBundle(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_production_sdk_source_exclusion_guarantee(self):
        # 1. Build Production SDK
        res = ProductionDistributionBuilder.build_production_sdk(
            version="1.2.0",
            target_platform="windows-x64",
            output_dir=os.path.join(self.temp_dir, "dist")
        )
        archive_path = res["archive_path"]
        self.assertTrue(os.path.exists(archive_path))

        # 2. Inspect archive contents — ZERO .py, .pyc, or __pycache__ allowed
        with zipfile.ZipFile(archive_path, "r") as zf:
            names = zf.namelist()
            self.assertGreater(len(names), 5)
            for n in names:
                self.assertFalse(n.endswith(".py"), f"Found forbidden Python source file in production archive: {n}")
                self.assertFalse(n.endswith(".pyc"), f"Found compiled pyc file in production archive: {n}")
                self.assertNotIn("__pycache__", n, f"Found __pycache__ in production archive: {n}")

    def test_source_exclusion_gate_fails_on_source_files(self):
        bad_dir = os.path.join(self.temp_dir, "bad_staging")
        os.makedirs(bad_dir)
        with open(os.path.join(bad_dir, "leak.py"), "w") as f:
            f.write("# Source leak")

        with self.assertRaises(SourceExclusionViolationError):
            ProductionDistributionBuilder.verify_source_exclusion(bad_dir)


if __name__ == "__main__":
    unittest.main()
