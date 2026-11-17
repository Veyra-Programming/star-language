"""
Star Production Distribution Manifest Subsystem
Authoritative Reference: STAR_DISTRIBUTION.md (Section 2)
"""

import json
import time
from typing import Dict, Any, List, Optional


class DistributionManifest:
    """
    Descriptor capturing SDK version, target platform, binary executables,
    standard library assets, and file checksums for production releases.
    """
    def __init__(
        self,
        name: str = "Star-SDK",
        version: str = "1.0.1",
        target_platform: str = "windows-x64",
        core_abi: int = 1,
        mobile_abi: int = 1,
        binaries: Optional[List[str]] = None,
        file_checksums: Optional[Dict[str, str]] = None,
        build_timestamp: Optional[str] = None
    ):
        self.name = name
        self.version = version
        self.target_platform = target_platform
        self.core_abi = core_abi
        self.mobile_abi = mobile_abi
        self.binaries = binaries or ["bin/star.exe", "bin/starc.exe", "bin/star-runtime.exe"]
        self.file_checksums = file_checksums or {}
        self.build_timestamp = build_timestamp or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "target_platform": self.target_platform,
            "core_abi": self.core_abi,
            "mobile_abi": self.mobile_abi,
            "binaries": self.binaries,
            "build_timestamp": self.build_timestamp,
            "file_checksums": self.file_checksums,
            "source_distribution": False,
            "integrity_verified": True
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DistributionManifest":
        return cls(
            name=data.get("name", "Star-SDK"),
            version=data.get("version", "1.0.1"),
            target_platform=data.get("target_platform", "windows-x64"),
            core_abi=data.get("core_abi", 1),
            mobile_abi=data.get("mobile_abi", 1),
            binaries=data.get("binaries", []),
            file_checksums=data.get("file_checksums", {}),
            build_timestamp=data.get("build_timestamp")
        )

    @classmethod
    def from_json(cls, json_str: str) -> "DistributionManifest":
        return cls.from_dict(json.loads(json_str))
