"""
Star Unified Mobile Release Manager
Authoritative Reference: STAR_RELEASE.md & STAR_MOBILE_RUNTIME.md
"""

import os
from typing import Dict, Any, Optional, List, Tuple
from star_engine.mobile_config import MobileBuildConfig
from star_backend.mobile.packaging import MobilePackager
from star_backend.mobile.android.builder import AndroidBuilder
from star_backend.mobile.android.verify import AndroidVerifier, AndroidVerificationResult
from star_backend.mobile.android.signing import AndroidSigner
from star_backend.mobile.ios.builder import iOSBuilder
from star_backend.mobile.ios.verify import iOSVerifier, iOSVerificationResult
from star_backend.mobile.ios.signing import iOSSigner
from star_backend.mobile.provenance import ProvenanceManager
from tests.conformance.runner import run_conformance_matrix


class MobileReleaseManager:
    """
    Automates the full end-to-end mobile release workflow:
    Validation → Conformance → Bundling → Dual Compilation → Signing → Verification → Release Metadata.
    """
    def __init__(self, config: Optional[MobileBuildConfig] = None):
        self.config = config or MobileBuildConfig.load_from_project_file()
        self.packager = MobilePackager()
        self.android_builder = AndroidBuilder()
        self.ios_builder = iOSBuilder()

    def build_android(
        self,
        source_file: str = "main.star",
        profile: str = "debug"
    ) -> Dict[str, str]:
        is_rel = profile in ("release", "distribution")
        signing_cfg = AndroidSigner.resolve_signing_config(
            manifest_signing_dict=self.config.android_signing,
            release=is_rel,
            profile=profile
        )

        apk_path = self.android_builder.build_apk(source_file, release=is_rel, signing_config=signing_cfg)
        aab_path = self.android_builder.build_aab(source_file, release=is_rel, signing_config=signing_cfg)

        apk_prov = ProvenanceManager.generate_provenance(apk_path, "android", source_file, {"profile": profile})
        aab_prov = ProvenanceManager.generate_provenance(aab_path, "android", source_file, {"profile": profile})

        return {
            "apk": apk_path,
            "aab": aab_path,
            "apk_sha256": apk_prov["digest"],
            "aab_sha256": aab_prov["digest"]
        }

    def build_ios(
        self,
        source_file: str = "main.star",
        profile: str = "development"
    ) -> Dict[str, str]:
        is_rel = profile in ("release", "distribution", "appstore")
        project_dir = self.ios_builder.build_project(source_file)
        ipa_path = self.ios_builder.build_ipa(source_file, release=is_rel)

        ipa_prov = ProvenanceManager.generate_provenance(ipa_path, "ios", source_file, {"profile": profile})

        return {
            "project": project_dir,
            "ipa": ipa_path,
            "ipa_sha256": ipa_prov["digest"]
        }

    def build_all(
        self,
        source_file: str = "main.star",
        profile: str = "debug"
    ) -> Dict[str, Any]:
        android_artifacts = self.build_android(source_file, profile)
        ios_artifacts = self.build_ios(source_file, profile)
        return {
            "android": android_artifacts,
            "ios": ios_artifacts
        }

    def verify_artifact(self, artifact_path: str) -> Any:
        if artifact_path.endswith(".apk") or artifact_path.endswith(".aab"):
            return AndroidVerifier.verify(artifact_path)
        elif artifact_path.endswith(".ipa") or artifact_path.endswith(".app"):
            return iOSVerifier.verify(artifact_path)
        else:
            raise ValueError(f"Unsupported mobile artifact format: '{artifact_path}'")

    def release_mobile(
        self,
        source_file: str = "main.star",
        profile: str = "release"
    ) -> int:
        print("=" * 60)
        print(f"🚀 Star Mobile Release Workflow — {source_file} (Profile: {profile.upper()})")
        print("=" * 60)

        # 1. Conformance Matrix
        print("\nStep 1/5: Running Cross-Platform Conformance Verification...")
        conf_res = run_conformance_matrix()
        if conf_res != 0:
            print("\n✗ Release Aborted: Cross-platform conformance check failed.")
            return 1

        # 2. Compile & Produce .starmobile
        print("\nStep 2/5: Packaging Portable .starmobile Bundle...")
        bundle_path = self.packager.build_bundle(source_file)
        ProvenanceManager.generate_provenance(bundle_path, "mobile", source_file, {"profile": profile})
        print(f"✓ Created: {bundle_path}")

        # 3. Build & Sign Android Suite (APK & AAB)
        print("\nStep 3/5: Building & Signing Android Distribution Suite...")
        android_res = self.build_android(source_file, profile=profile)
        print(f"✓ Android APK: {android_res['apk']}")
        print(f"✓ Android AAB: {android_res['aab']}")

        # 4. Build & Sign iOS Suite (Xcode & IPA)
        print("\nStep 4/5: Building & Signing iOS Distribution Suite...")
        ios_res = self.build_ios(source_file, profile=profile)
        print(f"✓ Xcode Project: {ios_res['project']}")
        print(f"✓ iOS IPA:       {ios_res['ipa']}")

        # 5. Verify All Artifacts
        print("\nStep 5/5: Cryptographic Verification of All Release Artifacts...")
        apk_verify = AndroidVerifier.verify(android_res["apk"])
        aab_verify = AndroidVerifier.verify(android_res["aab"])
        ipa_verify = iOSVerifier.verify(ios_res["ipa"])

        all_ok = apk_verify.is_valid and aab_verify.is_valid and ipa_verify.is_valid

        print("=" * 60)
        print("⭐ Star Mobile Release Summary")
        print("=" * 60)
        print(f"Android APK ({os.path.basename(android_res['apk'])}): {'✓ VERIFIED' if apk_verify.is_valid else '✗ FAILED'}")
        print(f"Android AAB ({os.path.basename(android_res['aab'])}): {'✓ VERIFIED' if aab_verify.is_valid else '✗ FAILED'}")
        print(f"iOS IPA     ({os.path.basename(ios_res['ipa'])}): {'✓ VERIFIED' if ipa_verify.is_valid else '✗ FAILED'}")
        print("=" * 60)

        if all_ok:
            print("🚀 MOBILE RELEASE READY FOR DISTRIBUTION")
            return 0
        else:
            print("✗ MOBILE RELEASE VERIFICATION FAILED")
            return 1
