"""
Star Deterministic Archive Packaging Subsystem
Authoritative Reference: STAR_DISTRIBUTION.md (Section 4)
"""

import os
import zipfile
import time
from typing import Optional, List


class ArchiveEngine:
    """
    Creates deterministic, reproducible ZIP and .starpkg distribution archives
    with normalized timestamps, directory preservation, and UTF-8 encoding.
    """

    # Deterministic epoch timestamp (2026-01-01 00:00:00)
    DETERMINISTIC_TIMESTAMP = (2026, 1, 1, 0, 0, 0)

    @classmethod
    def create_deterministic_zip(
        cls,
        source_dir: str,
        output_zip: str,
        base_folder: Optional[str] = None
    ) -> str:
        os.makedirs(os.path.dirname(os.path.abspath(output_zip)), exist_ok=True)

        files_to_pack: List[str] = []
        for root, dirs, files in os.walk(source_dir):
            dirs.sort()
            for f in sorted(files):
                full_path = os.path.join(root, f)
                files_to_pack.append(full_path)

        with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for full_path in sorted(files_to_pack):
                rel_path = os.path.relpath(full_path, source_dir).replace("\\", "/")
                arcname = f"{base_folder}/{rel_path}" if base_folder else rel_path

                with open(full_path, "rb") as f:
                    data = f.read()

                zinfo = zipfile.ZipInfo(arcname, cls.DETERMINISTIC_TIMESTAMP)
                zinfo.external_attr = 0o755 << 16 if full_path.endswith(".exe") or "/bin/" in full_path else 0o644 << 16
                zf.writestr(zinfo, data)

        return output_zip

    @classmethod
    def package_project(cls, project_dir: str = ".", output_name: Optional[str] = None) -> str:
        manifest_path = os.path.join(project_dir, "star.toml")
        app_name = "MyApp"
        version = "1.0.0"

        if os.path.exists(manifest_path):
            from star_runtime.packages import PackageManager
            pm = PackageManager()
            manifest = pm.load_manifest()
            if manifest:
                app_name = manifest.name
                version = manifest.version

        pkg_name = output_name or f"{app_name}-{version}.starpkg"
        out_path = os.path.join(project_dir, pkg_name)
        return cls.create_deterministic_zip(project_dir, out_path)
