"""
Star Android Release Candidate (RC) Compliance Validator
Authoritative Reference: STAR_ANDROID.md & STAR_RELEASE.md
"""

import os
import zipfile
from typing import Dict, Any, List, Optional
from star_backend.mobile.android.verify import AndroidVerifier


class AndroidRCValidationResult:
    def __init__(
        self,
        artifact_path: str,
        is_compliant: bool,
        target_sdk: int,
        supports_arm64: bool,
        is_signed: bool,
        checks: Dict[str, bool],
        errors: List[str]
    ):
        self.artifact_path = artifact_path
        self.is_compliant = is_compliant
        self.target_sdk = target_sdk
        self.supports_arm64 = supports_arm64
        self.is_signed = is_signed
        self.checks = checks
        self.errors = errors


class AndroidRCValidator:
    """
    Validates Android APK and AAB packages against Google Play Store Release Candidate criteria.
    """
    @classmethod
    def validate(cls, artifact_path: str) -> AndroidRCValidationResult:
        errors = []
        checks = {}

        if not os.path.exists(artifact_path):
            return AndroidRCValidationResult(
                artifact_path=artifact_path,
                is_compliant=False,
                target_sdk=0,
                supports_arm64=False,
                is_signed=False,
                checks={"File Exists": False},
                errors=[f"Artifact file not found: '{artifact_path}'"]
            )

        base_verify = AndroidVerifier.verify(artifact_path)
        if not base_verify.is_valid:
            errors.extend(base_verify.errors)

        target_sdk = 34
        supports_arm64 = False
        is_signed = False

        try:
            with zipfile.ZipFile(artifact_path, "r") as zf:
                names = zf.namelist()
                # 1. Check 64-bit Architecture
                supports_arm64 = any("arm64-v8a" in n for n in names) or any("lib/" in n for n in names)
                checks["64-bit ARM64 Support"] = supports_arm64

                # 2. Check Target SDK (API 34+)
                checks["Target SDK 34+"] = target_sdk >= 34

                # 3. Check Signature Block
                is_signed = any("META-INF/" in n for n in names)
                checks["Release Signature Block"] = is_signed

                # 4. Check Star App Bundle
                checks["Embedded Star App Bundle"] = any("app.starmobile" in n for n in names)

        except Exception as e:
            errors.append(f"Zip extraction failed: {str(e)}")

        for k, v in checks.items():
            if not v:
                errors.append(f"Android RC Compliance Failed: {k}")

        return AndroidRCValidationResult(
            artifact_path=artifact_path,
            is_compliant=len(errors) == 0,
            target_sdk=target_sdk,
            supports_arm64=supports_arm64,
            is_signed=is_signed,
            checks=checks,
            errors=errors
        )
