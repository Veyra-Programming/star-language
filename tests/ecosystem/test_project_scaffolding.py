"""
Unit Tests for Star 1.1 Multi-Template Project Scaffolding
"""

import unittest
import tempfile
import os
import shutil
from star_engine.project import create_project, load_project, TEMPLATES


class TestProjectScaffolding(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_scaffold_all_six_templates(self):
        for tmpl in ["cli", "web", "desktop", "android", "ios", "universal"]:
            app_name = f"Test_{tmpl}_App"
            proj_path = create_project(app_name, template=tmpl, target_dir=self.temp_dir)
            self.assertTrue(os.path.exists(proj_path))
            self.assertTrue(os.path.exists(os.path.join(proj_path, "star.toml")))
            self.assertTrue(os.path.exists(os.path.join(proj_path, "src", "main.star")))
            self.assertTrue(os.path.exists(os.path.join(proj_path, "tests", "test_main.star")))
            self.assertTrue(os.path.exists(os.path.join(proj_path, "README.md")))
            self.assertTrue(os.path.exists(os.path.join(proj_path, ".gitignore")))

            cfg = load_project(proj_path)
            self.assertIsNotNone(cfg)
            self.assertEqual(cfg.name, app_name)
            self.assertEqual(cfg.target, TEMPLATES[tmpl]["target"])


if __name__ == "__main__":
    unittest.main()
