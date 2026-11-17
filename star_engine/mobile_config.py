"""
Star Mobile Project Configuration Model
Authoritative Reference: STAR_RELEASE.md & STAR_MOBILE.md
"""

import os
import re
from typing import Dict, Any, Optional, List


class MobileConfigError(Exception):
    """Raised when mobile configuration is invalid."""
    pass


class MobileBuildConfig:
    """
    Structured configuration loaded from `star.toml` ([mobile], [mobile.android], [mobile.ios], [android.signing], [ios.signing]).
    """
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        raw = data or {}
        mobile = raw.get("mobile", {})
        android = mobile.get("android", raw.get("android", {}))
        ios = mobile.get("ios", raw.get("ios", {}))
        build = mobile.get("build", raw.get("build", {}))

        # Basic metadata
        self.name: str = mobile.get("name", raw.get("package", {}).get("name", "StarApp"))
        self.package_id: str = mobile.get("package", f"org.starlang.{self.name.lower()}")
        self.version: str = mobile.get("version", raw.get("package", {}).get("version", "0.8.6"))
        self.version_code: int = int(mobile.get("version_code", 1))
        self.orientation: str = mobile.get("orientation", "portrait")

        # Android specific
        self.android_min_sdk: int = int(android.get("min_sdk", 26))
        self.android_target_sdk: int = int(android.get("target_sdk", 35))
        self.android_orientation: str = android.get("orientation", self.orientation)

        # iOS specific
        self.ios_deployment_target: str = str(ios.get("deployment_target", "15.0"))
        self.ios_bundle_id: str = ios.get("bundle_identifier", self.package_id)
        self.ios_device_family: List[str] = ios.get("device_family", ["iphone", "ipad"])

        # Output
        self.output_dir: str = build.get("output", os.path.join("build", "mobile"))

        # Signing profiles
        self.android_signing: Dict[str, Any] = self._resolve_env_secrets(
            raw.get("android.signing", raw.get("android", {}).get("signing", {}))
        )
        self.ios_signing: Dict[str, Any] = self._resolve_env_secrets(
            raw.get("ios.signing", raw.get("ios", {}).get("signing", {}))
        )

    @classmethod
    def _resolve_env_secrets(cls, cfg: Dict[str, Any]) -> Dict[str, Any]:
        """Resolves ${ENV_VAR} expressions securely from the environment."""
        resolved = {}
        for k, v in cfg.items():
            if isinstance(v, dict):
                resolved[k] = cls._resolve_env_secrets(v)
            elif isinstance(v, str):
                match = re.match(r"^\$\{([A-Za-z0-9_]+)\}$", v.strip())
                if match:
                    env_key = match.group(1)
                    resolved[k] = os.getenv(env_key, "")
                else:
                    resolved[k] = v
            else:
                resolved[k] = v
        return resolved

    @classmethod
    def load_from_project_file(cls, toml_path: str = "star.toml") -> "MobileBuildConfig":
        if os.path.exists(toml_path):
            try:
                # Basic TOML parser or dictionary reader
                from star_runtime.packages import PackageManager
                pm = PackageManager()
                raw_cfg = pm.manifest or {}
                return cls(raw_cfg)
            except Exception:
                pass
        return cls({})
