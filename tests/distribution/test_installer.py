"""
Unit Tests for Star Production Installer
"""

import unittest
import tempfile
import os
import shutil
from star_distribution.builder import ProductionDistributionBuilder
from star_distribution.installer import ProductionInstaller


class TestProductionInstaller(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.install_target = os.path.join(self.temp_dir, "StarInstalled")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_end_to_end_sdk_build_and_install(self):
        # 1. Build SDK
        sdk_res = ProductionDistributionBuilder.build_production_sdk(
            version="1.0.1",
            target_platform="windows-x64",
            output_dir=os.path.join(self.temp_dir, "dist")
        )
        archive_path = sdk_res["archive_path"]
        self.assertTrue(os.path.exists(archive_path))

        # 2. Install SDK
        install_res = ProductionInstaller.install(archive_path, self.install_target)
        self.assertEqual(install_res["status"], "SUCCESS")
        self.assertTrue(install_res["manifest_verified"])
        self.assertTrue(os.path.exists(os.path.join(self.install_target, "star.manifest")))


if __name__ == "__main__":
    unittest.main()
