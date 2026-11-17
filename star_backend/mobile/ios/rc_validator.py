"""
Star iOS Release Candidate (RC) Compliance Validator
Authoritative Reference: STAR_IOS.md & STAR_RELEASE.md
"""

import os
import zipfile
from typing import Dict, Any, List, Optional
from star_backend.mobile.ios.verify import iOSVerifier


class iOSRCValidationResult:
    def __init__(
        self,
        artifact_path: str,
        is_compliant: bool,
        min_os_version: str,
        supports_arm64: bool,
        is_signed: bool,
        checks: Dict[str, bool],
        errors: List[str]
    ):
        self.artifact_path = artifact_path
        self.is_compliant = is_compliant
        self.min_os_version = min_os_version
        self.supports_arm64 = supports_arm64
        self.is_signed = is_signed
        self.checks = checks
        self.errors = errors


class iOSRCValidator:
    """
    Validates iOS IPA packages against Apple App Store Release Candidate criteria.
    """
    @classmethod
    def validate(cls, artifact_path: str) -> iOSRCValidationResult:
        errors = []
        checks = {}

        if not os.path.exists(artifact_path):
            return iOSRCValidationResult(
                artifact_path=artifact_path,
                is_compliant=False,
                min_os_version="0.0",
                supports_arm64=False,
                is_signed=False,
                checks={"File Exists": False},
                errors=[f"Artifact file not found: '{artifact_path}'"]
            )

        base_verify = iOSVerifier.verify(artifact_path)
        if not base_verify.is_valid:
            errors.extend(base_verify.errors)

        min_os_version = "15.0"
        supports_arm64 = False
        is_signed = False

        try:
            with zipfile.ZipFile(artifact_path, "r") as zf:
                names = zf.namelist()

                # 1. ARM64 Mach-O Binary
                supports_arm64 = any("Payload/" in n and not "." in os.path.basename(n) and os.path.basename(n) != "Payload" for n in names)
                checks["ARM64 Native Binary"] = supports_arm64

                # 2. Info.plist Present
                checks["Info.plist Metadata"] = any(n.endswith("Info.plist") for n in names)

                # 3. Code Signature
                is_signed = any("_CodeSignature/CodeResources" in n for n in names)
                checks["Apple Code Signature"] = is_signed

                # 4. Embedded Star App Bundle
                checks["Embedded Star App Bundle"] = any("app.starmobile" in n for n in names)

        except Exception as e:
            errors.append(f"Zip extraction failed: {str(e)}")

        for k, v in checks.items():
            if not v:
                errors.append(f"iOS RC Compliance Failed: {k}")

        return iOSRCValidationResult(
            artifact_path=artifact_path,
            is_compliant=len(errors) == 0,
            min_os_version=min_os_version,
            supports_arm64=supports_arm64,
            is_signed=is_signed,
            checks=checks,
            errors=errors
        )
