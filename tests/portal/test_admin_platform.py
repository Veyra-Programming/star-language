"""
Unit Tests for Star 1.2 Developer Portal & Admin Console Assets
"""

import unittest
import os


class TestAdminPlatform(unittest.TestCase):
    def setUp(self):
        self.portal_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "web", "portal"))

    def test_portal_html_structure(self):
        index_path = os.path.join(self.portal_dir, "index.html")
        self.assertTrue(os.path.exists(index_path))
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("v1.2.0", content)
        self.assertIn("admin-modal", content)
        self.assertIn("Star Doctor Web Dashboard", content)
        self.assertIn("The Star Book: 20-Chapter Curriculum", content)
        self.assertIn("Explore What Star Can Build", content)

    def test_portal_app_js_data_integrity(self):
        app_js_path = os.path.join(self.portal_dir, "app.js")
        self.assertTrue(os.path.exists(app_js_path))
        with open(app_js_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("PLAYGROUND_SNIPPETS", content)
        self.assertIn("STAR_BOOK_CHAPTERS", content)
        self.assertIn("EXAMPLES_GALLERY", content)
        self.assertIn("PACKAGES_CATALOG", content)
        self.assertIn("DOWNLOAD_RELEASES", content)


if __name__ == "__main__":
    unittest.main()
