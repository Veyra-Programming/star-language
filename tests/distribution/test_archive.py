"""
Unit Tests for Star Deterministic Archive Engine
"""

import unittest
import tempfile
import os
import shutil
from star_distribution.archive import ArchiveEngine
from star_distribution.integrity import IntegrityManager


class TestArchiveEngine(unittest.TestCase):
    def setUp(self):
        self.src_dir = tempfile.mkdtemp()
        self.out_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.src_dir, ignore_errors=True)
        shutil.rmtree(self.out_dir, ignore_errors=True)

    def test_deterministic_zip_reproducibility(self):
        # Create identical files
        with open(os.path.join(self.src_dir, "b.txt"), "w", encoding="utf-8") as f:
            f.write("Second file")
        with open(os.path.join(self.src_dir, "a.txt"), "w", encoding="utf-8") as f:
            f.write("First file")

        zip1 = os.path.join(self.out_dir, "test1.zip")
        zip2 = os.path.join(self.out_dir, "test2.zip")

        ArchiveEngine.create_deterministic_zip(self.src_dir, zip1)
        ArchiveEngine.create_deterministic_zip(self.src_dir, zip2)

        hash1 = IntegrityManager.calculate_file_sha256(zip1)
        hash2 = IntegrityManager.calculate_file_sha256(zip2)

        self.assertEqual(hash1, hash2, "Deterministic ZIPs must yield byte-identical hashes")


if __name__ == "__main__":
    unittest.main()
