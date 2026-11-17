"""
Unit Tests for CI/CD Workflow Generation
"""

import unittest
import os
import shutil
from star_backend.mobile.ci import CIPipelineGenerator


class TestCIGenerator(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = "test_ci_out"
        os.makedirs(self.tmp_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_ci_generation_no_hardcoded_secrets(self):
        paths = CIPipelineGenerator.init_all(target_dir=self.tmp_dir)

        self.assertTrue(os.path.exists(paths["github"]))
        self.assertTrue(os.path.exists(paths["gitlab"]))

        with open(paths["github"], "r", encoding="utf-8") as f:
            gh_content = f.read()

        self.assertIn("${{ secrets.STAR_ANDROID_KEYSTORE }}", gh_content)
        self.assertIn("${{ secrets.APPLE_TEAM_ID }}", gh_content)
        self.assertNotIn("password123", gh_content)


if __name__ == "__main__":
    unittest.main()
