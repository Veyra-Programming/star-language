"""
Unit Tests for Star Package Registry Workflow
"""

import unittest
import tempfile
import os
import shutil
from star_engine.project import create_project
from star_runtime.registry import PackageRegistry


class TestRegistryWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.proj_dir = create_project("RegistryApp", template="universal", target_dir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_package_and_publish_flow(self):
        old_cwd = os.getcwd()
        os.chdir(self.proj_dir)
        try:
            # 1. Package .starpkg
            pkg_path = PackageRegistry.package(self.proj_dir)
            self.assertTrue(os.path.exists(pkg_path))
            self.assertTrue(pkg_path.endswith(".starpkg"))

            # 2. Publish metadata
            pub_res = PackageRegistry.publish(self.proj_dir)
            self.assertEqual(pub_res["status"], "PUBLISHED")
            self.assertEqual(pub_res["name"], "RegistryApp")
        finally:
            os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
