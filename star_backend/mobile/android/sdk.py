"""
Star Android SDK Integration & Environment Discovery
Authoritative Reference: STAR_ANDROID.md (Section 6 & 8)
"""

import os
import sys
import subprocess
from typing import Optional, Dict, Any, List


class AndroidSDK:
    """
    Discovers, validates, and manages the Android SDK environment.
    Provides direct access to Android build tools (aapt2, zipalign, apksigner),
    platform JARs (android.jar), ADB device bridge, and Gradle integration.
    """
    _instance: Optional["AndroidSDK"] = None

    def __init__(self, sdk_dir: str):
        self.sdk_dir = os.path.abspath(sdk_dir)
        self.platform_tools_dir = os.path.join(self.sdk_dir, "platform-tools")
        self.build_tools_root = os.path.join(self.sdk_dir, "build-tools")
        self.platforms_root = os.path.join(self.sdk_dir, "platforms")
        
        self.platforms = self._discover_platforms()
        self.build_tools_versions = self._discover_build_tools()
        
        # Determine best available target platform (prefer 34 for Google Play GA compliance)
        self.target_platform = "android-34" if "android-34" in self.platforms else (self.platforms[-1] if self.platforms else "android-34")

        exe_ext = ".exe" if sys.platform == "win32" else ""
        cmd_ext = ".bat" if sys.platform == "win32" else ""

        # Determine best build tools version that has necessary binaries
        self.build_tools_version = "35.0.0" if "35.0.0" in self.build_tools_versions else (self.build_tools_versions[-1] if self.build_tools_versions else "34.0.0")
        for bt in reversed(self.build_tools_versions):
            bt_dir_candidate = os.path.join(self.build_tools_root, bt)
            if os.path.exists(os.path.join(bt_dir_candidate, f"aapt2{exe_ext}")) and os.path.exists(os.path.join(bt_dir_candidate, f"zipalign{exe_ext}")):
                self.build_tools_version = bt
                break

        # Tool paths
        direct_adb = os.path.join(self.sdk_dir, f"adb{exe_ext}")
        if os.path.exists(direct_adb):
            self.adb_path = direct_adb
            self.platform_tools_dir = self.sdk_dir
        else:
            self.adb_path = os.path.join(self.platform_tools_dir, f"adb{exe_ext}")
        bt_dir = os.path.join(self.build_tools_root, self.build_tools_version) if self.build_tools_versions else ""
        self.aapt2_path = os.path.join(bt_dir, f"aapt2{exe_ext}") if bt_dir else None
        self.zipalign_path = os.path.join(bt_dir, f"zipalign{exe_ext}") if bt_dir else None
        self.apksigner_path = os.path.join(bt_dir, f"apksigner{cmd_ext}") if bt_dir else None
        self.d8_path = os.path.join(bt_dir, f"d8{cmd_ext}") if bt_dir else None
        
        self.android_jar_path = os.path.join(self.platforms_root, self.target_platform, "android.jar")

        # JDK tool paths (javac, keytool)
        import shutil
        java_home = os.environ.get("JAVA_HOME", "")
        javac_candidate = os.path.join(java_home, "bin", f"javac{exe_ext}") if java_home else ""
        self.javac_path = javac_candidate if (javac_candidate and os.path.exists(javac_candidate)) else shutil.which("javac")

        keytool_candidate = os.path.join(java_home, "bin", f"keytool{exe_ext}") if java_home else ""
        self.keytool_path = keytool_candidate if (keytool_candidate and os.path.exists(keytool_candidate)) else shutil.which("keytool")

    def _discover_platforms(self) -> List[str]:
        if not os.path.exists(self.platforms_root):
            return []
        try:
            return sorted([d for d in os.listdir(self.platforms_root) if os.path.isdir(os.path.join(self.platforms_root, d)) and d.startswith("android-")])
        except Exception:
            return []

    def _discover_build_tools(self) -> List[str]:
        if not os.path.exists(self.build_tools_root):
            return []
        try:
            return sorted([d for d in os.listdir(self.build_tools_root) if os.path.isdir(os.path.join(self.build_tools_root, d))])
        except Exception:
            return []

    @property
    def is_valid(self) -> bool:
        return os.path.exists(self.sdk_dir) and (bool(self.platforms) or os.path.exists(self.platform_tools_dir))

    @property
    def has_build_tools(self) -> bool:
        return bool(self.build_tools_versions) and bool(self.zipalign_path and os.path.exists(self.zipalign_path)) and bool(self.aapt2_path and os.path.exists(self.aapt2_path))

    @property
    def has_compiler(self) -> bool:
        return bool(self.has_build_tools and self.javac_path and os.path.exists(self.javac_path) and self.android_jar_path and os.path.exists(self.android_jar_path))

    @property
    def has_adb(self) -> bool:
        return bool(self.adb_path and os.path.exists(self.adb_path))

    def generate_local_properties(self, project_dir: str) -> str:
        """
        Generates standard local.properties with escaped sdk.dir for Gradle.
        """
        os.makedirs(project_dir, exist_ok=True)
        props_path = os.path.join(project_dir, "local.properties")
        escaped_sdk = self.sdk_dir.replace("\\", "/").replace(":", "\\:")
        with open(props_path, "w", encoding="utf-8") as f:
            f.write(f"## Auto-generated by Star Language Android Toolchain\n")
            f.write(f"sdk.dir={escaped_sdk}\n")
        return props_path

    def get_sdk_info(self) -> Dict[str, Any]:
        return {
            "sdk_dir": self.sdk_dir,
            "target_platform": self.target_platform,
            "build_tools_version": self.build_tools_version,
            "has_adb": self.has_adb,
            "has_build_tools": self.has_build_tools,
            "has_compiler": self.has_compiler,
            "platforms": self.platforms,
            "build_tools": self.build_tools_versions
        }

    @classmethod
    def find_sdk(cls) -> Optional["AndroidSDK"]:
        """
        Detects the Android SDK from environment variables or standard OS paths.
        Prioritizes full SDK installations containing build-tools and platforms over bare ADB stubs.
        """
        if cls._instance is not None:
            return cls._instance

        import shutil
        candidates = []
        # 1. Environment variables
        for env_var in ("ANDROID_HOME", "ANDROID_SDK_ROOT"):
            val = os.environ.get(env_var)
            if val and os.path.exists(val):
                candidates.append(val)

        # 2. Standard platform SDK directories
        if sys.platform == "win32":
            local_appdata = os.environ.get("LOCALAPPDATA", "")
            if local_appdata:
                candidates.append(os.path.join(local_appdata, "Android", "Sdk"))
                candidates.append(os.path.join(local_appdata, "Android", "sdk"))
            user_profile = os.environ.get("USERPROFILE", "")
            if user_profile:
                candidates.append(os.path.join(user_profile, "AppData", "Local", "Android", "Sdk"))
                candidates.append(os.path.join(user_profile, "AppData", "Local", "Android", "sdk"))
            for drive in ("C:", "D:", "E:"):
                candidates.append(os.path.join(drive, "\\Android", "Sdk"))
                candidates.append(os.path.join(drive, "\\Android", "sdk"))
        elif sys.platform == "darwin":
            home = os.path.expanduser("~")
            candidates.append(os.path.join(home, "Library", "Android", "sdk"))
        else:
            home = os.path.expanduser("~")
            candidates.append(os.path.join(home, "Android", "Sdk"))
            candidates.append("/usr/lib/android-sdk")
            candidates.append("/opt/android-sdk")

        # 3. Check shutil.which for active adb in PATH
        adb_in_path = shutil.which("adb")
        if adb_in_path:
            pt_dir = os.path.dirname(os.path.abspath(adb_in_path))
            candidates.append(os.path.dirname(pt_dir))
            candidates.append(pt_dir)

        # 4. Check common Windows standalone Android platform-tools locations
        if sys.platform == "win32":
            for drive in ("C:", "D:", "E:"):
                candidates.append(os.path.join(drive, "\\platform-tools-latest-windows", "platform-tools"))
                candidates.append(os.path.join(drive, "\\platform-tools-latest-windows"))
                candidates.append(os.path.join(drive, "\\platform-tools"))

        valid_sdks = []
        for c in candidates:
            if c and os.path.exists(c) and os.path.isdir(c):
                try:
                    sdk = cls(c)
                    if sdk.is_valid:
                        # Full SDK with compiler found, prioritize immediately!
                        if sdk.has_compiler:
                            cls._instance = sdk
                            return sdk
                        valid_sdks.append(sdk)
                except Exception:
                    continue

        for sdk in valid_sdks:
            if sdk.has_build_tools:
                cls._instance = sdk
                return sdk

        if valid_sdks:
            cls._instance = valid_sdks[0]
            return valid_sdks[0]

        return None
