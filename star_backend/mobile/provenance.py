"""
Star Mobile Build Provenance & Deterministic Metadata Manager
Authoritative Reference: STAR_RELEASE.md & STAR_RUNTIME.md
"""

import os
import json
import hashlib
import time
from typing import Dict, Any, Optional


class ProvenanceManager:
    """
    Generates cryptographic checksums and build provenance descriptors (.build.json, .sha256)
    for reproducible mobile build artifacts.
    """
    @classmethod
    def calculate_sha256(cls, file_path: str) -> str:
        if not os.path.exists(file_path):
            return ""
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    @classmethod
    def generate_provenance(
        cls,
        artifact_path: str,
        target_platform: str,
        source_file: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        if not os.path.exists(artifact_path):
            raise FileNotFoundError(f"Artifact not found: '{artifact_path}'")

        artifact_sha256 = cls.calculate_sha256(artifact_path)
        source_sha256 = cls.calculate_sha256(source_file) if source_file and os.path.exists(source_file) else ""

        base_dir = os.path.dirname(artifact_path)
        base_name = os.path.basename(artifact_path)
        root_name = os.path.splitext(base_name)[0]

        # 1. Write .sha256 file
        sha256_file_path = f"{artifact_path}.sha256"
        with open(sha256_file_path, "w", encoding="utf-8") as f:
            f.write(f"{artifact_sha256}  {base_name}\n")

        # 2. Write .build.json descriptor
        build_json_path = os.path.join(base_dir, f"{root_name}.build.json")
        provenance_data = {
            "star_version": "0.8.6",
            "mobile_abi_version": 1,
            "target": target_platform,
            "artifact_file": base_name,
            "artifact_sha256": artifact_sha256,
            "source_file": os.path.basename(source_file) if source_file else "",
            "source_sha256": source_sha256,
            "build_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "deterministic_reproducible": True
        }
        if extra_metadata:
            provenance_data.update(extra_metadata)

        with open(build_json_path, "w", encoding="utf-8") as f:
            json.dump(provenance_data, f, indent=2)

        return {
            "sha256_file": sha256_file_path,
            "build_json": build_json_path,
            "digest": artifact_sha256
        }
