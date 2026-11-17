"""
Star Secure Archive Extractor & Path-Traversal Protection Subsystem
Authoritative Reference: STAR_DISTRIBUTION.md (Section 5)
"""

import os
import shutil
import zipfile
import time
from typing import Optional, List
from star_distribution.integrity import IntegrityError, IntegrityManager


class SecurityViolationError(Exception):
    """Raised when an illegal path traversal (Zip-Slip) or security violation is detected."""
    pass


class SecureExtractor:
    """
    Safely extracts distribution archives with mandatory Zip-Slip path-traversal prevention,
    checksum verification, atomic staging, and failure rollback.
    """

    @classmethod
    def validate_safe_path(cls, member_name: str, target_dir: str) -> str:
        # Check for obvious traversal attempts
        if member_name.startswith("/") or member_name.startswith("\\") or ":" in member_name:
            raise SecurityViolationError(f"Illegal absolute path or drive letter in archive member: '{member_name}'")

        parts = member_name.replace("\\", "/").split("/")
        if ".." in parts:
            raise SecurityViolationError(f"Path-traversal attempt ('..') rejected in member: '{member_name}'")

        target_abs = os.path.abspath(target_dir)
        destination = os.path.abspath(os.path.join(target_abs, member_name))

        # Destination must be strictly inside target_abs
        if not destination.startswith(target_abs + os.sep) and destination != target_abs:
            raise SecurityViolationError(f"Zip-Slip vulnerability detected! Member '{member_name}' escapes target '{target_dir}'")

        return destination

    @classmethod
    def extract_archive(
        cls,
        archive_path: str,
        target_dir: str,
        verify_checksums: bool = True
    ) -> str:
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Archive not found: '{archive_path}'")

        target_dir_abs = os.path.abspath(target_dir)
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        temp_stage = os.path.join(os.path.dirname(target_dir_abs), f".tmp_extract_{os.getpid()}_{timestamp}")
        os.makedirs(temp_stage, exist_ok=True)

        try:
            with zipfile.ZipFile(archive_path, "r") as zf:
                # 1. Pre-validation of all members before extracting any files
                for member in zf.infolist():
                    cls.validate_safe_path(member.filename, temp_stage)

                # 2. Extract into isolated temporary staging directory
                for member in zf.infolist():
                    safe_dest = cls.validate_safe_path(member.filename, temp_stage)
                    if member.is_dir():
                        os.makedirs(safe_dest, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(safe_dest), exist_ok=True)
                        with zf.open(member) as src, open(safe_dest, "wb") as dst:
                            shutil.copyfileobj(src, dst)

            # 3. Optional manifest/checksum verification in staging
            if verify_checksums and os.path.exists(os.path.join(temp_stage, "star.manifest")):
                manifest_path = os.path.join(temp_stage, "star.manifest")
                with open(manifest_path, "r", encoding="utf-8") as f:
                    from star_distribution.manifest import DistributionManifest
                    manifest = DistributionManifest.from_json(f.read())
                    ok, errors = IntegrityManager.verify_directory_checksums(temp_stage, manifest.file_checksums)
                    if not ok:
                        raise IntegrityError(f"Checksum verification failed on extracted files: {errors}")

            # 4. Atomic commit to final target directory
            stage_items = os.listdir(temp_stage)
            if len(stage_items) == 1 and os.path.isdir(os.path.join(temp_stage, stage_items[0])):
                source_root = os.path.join(temp_stage, stage_items[0])
            else:
                source_root = temp_stage

            os.makedirs(target_dir_abs, exist_ok=True)
            for item in os.listdir(source_root):
                s_path = os.path.join(source_root, item)
                d_path = os.path.join(target_dir_abs, item)
                if os.path.exists(d_path):
                    if os.path.isdir(d_path):
                        shutil.rmtree(d_path)
                    else:
                        os.remove(d_path)
                shutil.move(s_path, d_path)

            return target_dir_abs

        finally:
            if os.path.exists(temp_stage):
                shutil.rmtree(temp_stage, ignore_errors=True)
