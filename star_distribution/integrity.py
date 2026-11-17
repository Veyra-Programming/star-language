"""
Star Production Integrity & Checksum Verification Subsystem
Authoritative Reference: STAR_DISTRIBUTION.md (Section 3)
"""

import os
import hashlib
import zipfile
from typing import Dict, Any, List, Tuple


class IntegrityError(Exception):
    """Raised when an integrity, checksum, or corrupted package violation occurs."""
    pass


class IntegrityManager:
    """
    Computes cryptographic SHA-256 digests and validates distribution package integrity.
    """

    @classmethod
    def calculate_file_sha256(cls, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found for checksum: '{file_path}'")
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    @classmethod
    def generate_sha256sums(cls, root_dir: str) -> Dict[str, str]:
        checksums = {}
        for dirpath, _, filenames in os.walk(root_dir):
            for fname in sorted(filenames):
                if fname == "SHA256SUMS":
                    continue
                full_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
                checksums[rel_path] = cls.calculate_file_sha256(full_path)
        return checksums

    @classmethod
    def verify_directory_checksums(
        cls,
        root_dir: str,
        expected_checksums: Dict[str, str]
    ) -> Tuple[bool, List[str]]:
        errors = []
        for rel_path, expected_hash in expected_checksums.items():
            full_path = os.path.join(root_dir, rel_path)
            if not os.path.exists(full_path):
                errors.append(f"Missing required file: '{rel_path}'")
                continue
            actual_hash = cls.calculate_file_sha256(full_path)
            if actual_hash != expected_hash:
                errors.append(f"Checksum mismatch for '{rel_path}' (Expected: {expected_hash[:8]}..., Actual: {actual_hash[:8]}...)")

        return (len(errors) == 0, errors)

    @classmethod
    def verify_archive_integrity(cls, archive_path: str) -> Tuple[bool, List[str]]:
        if not os.path.exists(archive_path):
            return (False, [f"Archive file not found: '{archive_path}'"])
        try:
            with zipfile.ZipFile(archive_path, "r") as zf:
                bad_file = zf.testzip()
                if bad_file:
                    return (False, [f"Corrupted entry in archive: '{bad_file}'"])
                return (True, [])
        except Exception as e:
            return (False, [f"Invalid ZIP container: {str(e)}"])
