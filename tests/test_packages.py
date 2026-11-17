"""
Star Language Package Manager Unit Tests
"""

import unittest
import sys
import os
import shutil
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_runtime.packages import PackageManager
from star_engine.project import create_project


class TestPackageManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="star_pkg_test_")
        create_project("test_app", self.test_dir)
        self.app_dir = os.path.join(self.test_dir, "test_app")
        self.pm = PackageManager(self.app_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_add_and_remove_package(self):
        self.pm.add_package("math_utils", "0.2.0")
        lock_file = os.path.join(self.app_dir, "star.lock")
        self.assertTrue(os.path.exists(lock_file))

        with open(lock_file, "r", encoding="utf-8") as f:
            lock_content = f.read()
        self.assertIn('name = "math_utils"', lock_content)
        self.assertIn('version = "0.2.0"', lock_content)

        # Remove package
        self.pm.remove_package("math_utils")
        with open(lock_file, "r", encoding="utf-8") as f:
            lock_content_after = f.read()
        self.assertNotIn('name = "math_utils"', lock_content_after)

    def test_pack_project(self):
        archive_path = self.pm.pack()
        self.assertTrue(os.path.exists(archive_path))
        self.assertTrue(archive_path.endswith(".starpkg"))


if __name__ == "__main__":
    unittest.main()
