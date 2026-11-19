"""
Star Platform Independence & Abstraction Layer (PAL)
Authoritative Reference: STAR_PLATFORM_SPEC.md

Provides unified cross-platform primitives across Windows, Linux, macOS,
Android, iOS, Raspberry Pi, Docker, and WebAssembly (WASM).
"""

import os
import sys
import platform
import tempfile
import subprocess
from typing import Dict, Any, Optional, List


class Platform:
    """Universal Platform Abstraction Layer for Star Language."""

    @classmethod
    def os_name(cls) -> str:
        """Normalized OS name: 'windows', 'linux', 'macos', 'android', 'ios', 'web'."""
        if "ANDROID_ROOT" in os.environ or "ANDROID_DATA" in os.environ:
            return "android"
        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        if system.startswith("win"):
            return "windows"
        if "linux" in system:
            return "linux"
        return system

    @classmethod
    def arch(cls) -> str:
        """Normalized architecture: 'x64', 'arm64', 'x86', 'arm'."""
        machine = platform.machine().lower()
        if machine in ("amd64", "x86_64", "x64"):
            return "x64"
        if machine in ("aarch64", "arm64"):
            return "arm64"
        if machine in ("i386", "i686", "x86"):
            return "x86"
        return machine

    @classmethod
    def is_windows(cls) -> bool:
        return cls.os_name() == "windows"

    @classmethod
    def is_linux(cls) -> bool:
        return cls.os_name() == "linux"

    @classmethod
    def is_macos(cls) -> bool:
        return cls.os_name() == "macos"

    @classmethod
    def is_android(cls) -> bool:
        return cls.os_name() == "android"

    @classmethod
    def is_posix(cls) -> bool:
        return os.name == "posix"

    @classmethod
    def is_64bit(cls) -> bool:
        return sys.maxsize > 2**32

    @classmethod
    def cpu_count(cls) -> int:
        return os.cpu_count() or 1

    @classmethod
    def endian(cls) -> str:
        return sys.byteorder  # 'little' or 'big'

    @classmethod
    def path_separator(cls) -> str:
        return os.sep

    @classmethod
    def line_separator(cls) -> str:
        return os.linesep

    @classmethod
    def normalize_path(cls, p: str) -> str:
        """Converts mixed backslashes/slashes into canonical system-independent normalized path."""
        if not p:
            return ""
        return os.path.normpath(os.path.expanduser(p))

    @classmethod
    def to_posix_path(cls, p: str) -> str:
        """Converts path to POSIX forward-slash format for web and cross-platform URLs."""
        return cls.normalize_path(p).replace("\\", "/")

    @classmethod
    def home_dir(cls) -> str:
        return os.path.expanduser("~")

    @classmethod
    def temp_dir(cls) -> str:
        return tempfile.gettempdir()

    @classmethod
    def app_data_dir(cls, app_name: str = "Star") -> str:
        """Returns standard per-platform application data directory."""
        os_n = cls.os_name()
        if os_n == "windows":
            base = os.environ.get("APPDATA", cls.home_dir())
            path = os.path.join(base, app_name)
        elif os_n == "macos":
            path = os.path.join(cls.home_dir(), "Library", "Application Support", app_name)
        else:
            base = os.environ.get("XDG_DATA_HOME", os.path.join(cls.home_dir(), ".local", "share"))
            path = os.path.join(base, app_name.lower())
        os.makedirs(path, exist_ok=True)
        return path

    @classmethod
    def cwd(cls) -> str:
        return os.getcwd()

    @classmethod
    def get_env(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.environ.get(key, default)

    @classmethod
    def set_env(cls, key: str, value: str):
        os.environ[key] = str(value)

    @classmethod
    def run_command(cls, cmd: str, timeout: Optional[float] = None) -> Dict[str, Any]:
        """Runs a system command portably across platforms."""
        try:
            res = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding="utf-8",
                errors="replace"
            )
            return {
                "exit_code": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "success": res.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"exit_code": -1, "stdout": "", "stderr": "Command timed out", "success": False}
        except Exception as e:
            return {"exit_code": -1, "stdout": "", "stderr": str(e), "success": False}

    @classmethod
    def platform_info(cls) -> Dict[str, Any]:
        """Returns comprehensive diagnostic information about the runtime host."""
        return {
            "os": cls.os_name(),
            "arch": cls.arch(),
            "is_64bit": cls.is_64bit(),
            "endian": cls.endian(),
            "cpus": cls.cpu_count(),
            "platform_release": platform.release(),
            "python_version": platform.python_version(),
            "home_dir": cls.home_dir(),
            "temp_dir": cls.temp_dir(),
            "cwd": cls.cwd(),
            "path_sep": cls.path_separator(),
        }
