"""
Star Microsoft Visual Studio & Windows SDK Toolchain Discovery
Authoritative Reference: STAR_DESKTOP.md & STAR_DISTRIBUTION.md
"""

import os
import sys
import subprocess
import shutil
from typing import Optional, Dict, Any, List


class VisualStudioToolchain:
    """
    Discovers and manages Microsoft Visual Studio (MSVC), MSBuild,
    and Windows SDK toolchains on Windows.
    Provides optional native C++/Win32 compilation capabilities while
    allowing Star to remain 100% portable and self-contained by default.
    """
    _instance: Optional["VisualStudioToolchain"] = None

    def __init__(
        self,
        vs_path: Optional[str] = None,
        vs_version: Optional[str] = None,
        cl_path: Optional[str] = None,
        link_path: Optional[str] = None,
        msbuild_path: Optional[str] = None,
        windows_sdk_path: Optional[str] = None,
        windows_sdk_version: Optional[str] = None
    ):
        self.vs_path = vs_path
        self.vs_version = vs_version
        self.cl_path = cl_path
        self.link_path = link_path
        self.msbuild_path = msbuild_path
        self.windows_sdk_path = windows_sdk_path
        self.windows_sdk_version = windows_sdk_version

    @property
    def is_installed(self) -> bool:
        return bool(self.vs_path and os.path.exists(self.vs_path)) or bool(self.cl_path and os.path.exists(self.cl_path))

    @property
    def has_cl(self) -> bool:
        return bool(self.cl_path and os.path.exists(self.cl_path))

    @property
    def has_msbuild(self) -> bool:
        return bool(self.msbuild_path and os.path.exists(self.msbuild_path))

    def get_toolchain_info(self) -> Dict[str, Any]:
        return {
            "is_installed": self.is_installed,
            "vs_version": self.vs_version or "Not Installed (Zero-Dependency Default Active)",
            "vs_path": self.vs_path,
            "cl_path": self.cl_path,
            "msbuild_path": self.msbuild_path,
            "windows_sdk_path": self.windows_sdk_path,
            "windows_sdk_version": self.windows_sdk_version or "None",
            "model": "In-tree Win32 Native Engine (Visual Studio Optional)"
        }

    @classmethod
    def find_toolchain(cls) -> "VisualStudioToolchain":
        """
        Discovers Visual Studio 2022, 2019, 2017 or Build Tools on the host.
        """
        if cls._instance is not None:
            return cls._instance

        if sys.platform != "win32":
            cls._instance = cls()
            return cls._instance

        vs_path = None
        vs_version = None
        cl_path = None
        link_path = None
        msbuild_path = None

        # 1. Try vswhere.exe if present
        vswhere_path = os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft Visual Studio\Installerswhere.exe")
        if os.path.exists(vswhere_path):
            try:
                res = subprocess.run(
                    [vswhere_path, "-latest", "-products", "*", "-property", "installationPath"],
                    capture_output=True, text=True, timeout=2
                )
                p = res.stdout.strip()
                if p and os.path.exists(p):
                    vs_path = p
                    # Get display version
                    ver_res = subprocess.run(
                        [vswhere_path, "-latest", "-products", "*", "-property", "catalog_productDisplayVersion"],
                        capture_output=True, text=True, timeout=2
                    )
                    vs_version = ver_res.stdout.strip() or "Visual Studio"
            except Exception:
                pass

        # 2. Check standard directory paths
        if not vs_path:
            candidates = [
                (r"C:\Program Files\Microsoft Visual Studio2\Community", "Visual Studio 2022 Community"),
                (r"C:\Program Files\Microsoft Visual Studio2\Professional", "Visual Studio 2022 Professional"),
                (r"C:\Program Files\Microsoft Visual Studio2\Enterprise", "Visual Studio 2022 Enterprise"),
                (r"C:\Program Files\Microsoft Visual Studio2\BuildTools", "Visual Studio 2022 Build Tools"),
                (r"C:\Program Files (x86)\Microsoft Visual Studio9\Community", "Visual Studio 2019 Community"),
                (r"C:\Program Files (x86)\Microsoft Visual Studio9\BuildTools", "Visual Studio 2019 Build Tools"),
            ]
            for p, v in candidates:
                if os.path.exists(p):
                    vs_path = p
                    vs_version = v
                    break

        # 3. Search for cl.exe & MSBuild if VS is found
        if vs_path:
            # Look for MSVC tools
            msvc_root = os.path.join(vs_path, "VC", "Tools", "MSVC")
            if os.path.exists(msvc_root):
                try:
                    versions = sorted(os.listdir(msvc_root), reverse=True)
                    if versions:
                        host_bin = os.path.join(msvc_root, versions[0], "bin", "Hostx64", "x64")
                        if os.path.exists(os.path.join(host_bin, "cl.exe")):
                            cl_path = os.path.join(host_bin, "cl.exe")
                            link_path = os.path.join(host_bin, "link.exe")
                except Exception:
                    pass

            # Look for MSBuild
            mb_candidate = os.path.join(vs_path, "MSBuild", "Current", "Bin", "MSBuild.exe")
            if os.path.exists(mb_candidate):
                msbuild_path = mb_candidate

        # 4. Fallback to PATH for cl / msbuild
        if not cl_path:
            cl_in_path = shutil.which("cl")
            if cl_in_path:
                cl_path = cl_in_path
                vs_version = vs_version or "MSVC (PATH)"
        if not msbuild_path:
            msbuild_path = shutil.which("msbuild")

        # 5. Discover Windows SDK
        win_sdk_path = None
        win_sdk_version = None
        for sdk_root in (r"C:\Program Files (x86)\Windows Kits", r"C:\Program Files (x86)\Windows Kits	"):
            include_dir = os.path.join(sdk_root, "Include")
            if os.path.exists(include_dir):
                win_sdk_path = sdk_root
                try:
                    vers = [d for d in os.listdir(include_dir) if d.startswith("10.")]
                    if vers:
                        win_sdk_version = sorted(vers, reverse=True)[0]
                except Exception:
                    pass
                break

        toolchain = cls(
            vs_path=vs_path,
            vs_version=vs_version,
            cl_path=cl_path,
            link_path=link_path,
            msbuild_path=msbuild_path,
            windows_sdk_path=win_sdk_path,
            windows_sdk_version=win_sdk_version
        )
        cls._instance = toolchain
        return toolchain
