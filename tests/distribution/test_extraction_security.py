"""
Security Tests for Zip-Slip and Path-Traversal Prevention in Archive Extractor
"""

import unittest
import tempfile
import os
import shutil
import zipfile
from star_distribution.extractor import SecureExtractor, SecurityViolationError


class TestExtractionSecurity(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.extract_target = os.path.join(self.temp_dir, "safe_target")
        os.makedirs(self.extract_target)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_safe_path_validation(self):
        dest = SecureExtractor.validate_safe_path("bin/star.exe", self.extract_target)
        self.assertTrue(dest.startswith(os.path.abspath(self.extract_target)))

    def test_reject_zip_slip_parent_traversal(self):
        with self.assertRaises(SecurityViolationError):
            SecureExtractor.validate_safe_path("../../Windows/System32/cmd.exe", self.extract_target)

    def test_reject_zip_slip_absolute_path(self):
        with self.assertRaises(SecurityViolationError):
            SecureExtractor.validate_safe_path("/etc/passwd", self.extract_target)

    def test_reject_zip_slip_drive_letter(self):
        with self.assertRaises(SecurityViolationError):
            SecureExtractor.validate_safe_path("C:\\Windows\\System32\\malicious.dll", self.extract_target)

    def test_malicious_archive_unpack_rejection(self):
        malicious_zip = os.path.join(self.temp_dir, "exploit.zip")
        with zipfile.ZipFile(malicious_zip, "w") as zf:
            zf.writestr("../../pwned.txt", "malicious payload")

        with self.assertRaises(SecurityViolationError):
            SecureExtractor.extract_archive(malicious_zip, self.extract_target)

        # Verify nothing was written outside
        escaped_file = os.path.join(self.temp_dir, "pwned.txt")
        self.assertFalse(os.path.exists(escaped_file))


if __name__ == "__main__":
    unittest.main()
