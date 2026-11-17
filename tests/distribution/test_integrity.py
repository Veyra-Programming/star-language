"""
Unit Tests for Star Production Integrity & Checksums
"""

import unittest
import tempfile
import os
import shutil
from star_distribution.integrity import IntegrityManager


class TestIntegrityManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_checksum_generation_and_verification(self):
        file1 = os.path.join(self.test_dir, "test1.txt")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("Star Language 1.0.1")

        csums = IntegrityManager.generate_sha256sums(self.test_dir)
        self.assertIn("test1.txt", csums)

        ok, errors = IntegrityManager.verify_directory_checksums(self.test_dir, csums)
        self.assertTrue(ok)
        self.assertEqual(len(errors), 0)

        # Mutate file and ensure failure
        with open(file1, "w", encoding="utf-8") as f:
            f.write("Corrupted content")

        ok, errors = IntegrityManager.verify_directory_checksums(self.test_dir, csums)
        self.assertFalse(ok)
        self.assertGreaterEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
