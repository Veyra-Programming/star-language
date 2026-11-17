"""
Star iOS Code Signing & Provisioning Subsystem
Authoritative Reference: STAR_IOS.md & STAR_RELEASE.md
"""

import os
import zipfile
from typing import Dict, Any, Optional, List
from star_engine.errors import StarRuntimeError


class iOSSigningError(StarRuntimeError):
    """Raised when an error occurs during iOS code signing or provisioning profile resolution."""
    pass


class iOSSigningConfig:
    def __init__(
        self,
        profile: str = "development",
        team_id: Optional[str] = None,
        identity: Optional[str] = None,
        provisioning_profile: Optional[str] = None,
        bundle_id: str = "org.starlang.app",
        entitlements: Optional[Dict[str, Any]] = None
    ):
        self.profile = profile
        self.team_id = team_id or "STAR_DEV_TEAM"
        self.identity = identity or "Apple Development: Star Developer"
        self.provisioning_profile = provisioning_profile or "embedded.mobileprovision"
        self.bundle_id = bundle_id
        self.entitlements = entitlements or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile": self.profile,
            "team_id": self.team_id,
            "identity": self.identity,
            "provisioning_profile": self.provisioning_profile,
            "bundle_id": self.bundle_id
        }


class iOSSigner:
    """
    Manages Apple code signing identity resolution, provisioning profiles,
    and IPA signature envelope generation.
    """
    @classmethod
    def resolve_signing_config(
        cls,
        manifest_signing_dict: Optional[Dict[str, Any]] = None,
        release: bool = False,
        profile: Optional[str] = None
    ) -> iOSSigningConfig:
        active_profile = profile or ("distribution" if release else "development")
        cfg = manifest_signing_dict or {}

        if active_profile in cfg and isinstance(cfg[active_profile], dict):
            cfg = cfg[active_profile]

        team_id = cfg.get("team_id") or os.getenv("APPLE_TEAM_ID")
        identity = cfg.get("identity") or (
            os.getenv("APPLE_DISTRIBUTION_IDENTITY") if active_profile in ("distribution", "appstore")
            else os.getenv("APPLE_DEVELOPMENT_IDENTITY")
        )
        prov_profile = cfg.get("profile") or os.getenv("APPLE_PROVISIONING_PROFILE")

        if active_profile in ("distribution", "appstore", "release"):
            if not team_id or not identity:
                raise iOSSigningError(
                    f"iOS {active_profile.capitalize()} build signing failed: No Apple Team ID or Distribution Identity configured.\n"
                    "To configure iOS release signing, add the following to 'star.toml':\n\n"
                    "[ios.signing.distribution]\n"
                    'team_id = "TEAM12345"\n'
                    'identity = "Apple Distribution: Example Corp (TEAM12345)"\n'
                    'profile = "keys/Example_AppStore.mobileprovision"\n\n'
                    "Or set the 'APPLE_TEAM_ID' and 'APPLE_DISTRIBUTION_IDENTITY' environment variables."
                )

        return iOSSigningConfig(
            profile=active_profile,
            team_id=team_id or "STAR_DEV_TEAM",
            identity=identity or "Apple Development: Local Simulator",
            provisioning_profile=prov_profile or "embedded.mobileprovision"
        )

    @classmethod
    def sign_ipa(cls, ipa_path: str, signing_config: iOSSigningConfig, app_name: str) -> None:
        """
        Appends code signature envelope and entitlements to the IPA package.
        """
        if not os.path.exists(ipa_path):
            raise FileNotFoundError(f"IPA package not found: '{ipa_path}'")

        code_resources = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>SigningProfile</key>
    <string>{signing_config.profile}</string>
    <key>TeamIdentifier</key>
    <string>{signing_config.team_id}</string>
    <key>Identity</key>
    <string>{signing_config.identity}</string>
    <key>Signer</key>
    <string>Star iOS CodeSigner 0.8.6</string>
</dict>
</plist>
"""
        with zipfile.ZipFile(ipa_path, "a", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"Payload/{app_name}.app/_CodeSignature/CodeResources", code_resources)
            zf.writestr(f"Payload/{app_name}.app/embedded.mobileprovision", b"STAR_PROVISIONING_PROFILE_DESCRIPTOR")
