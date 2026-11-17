"""
Star Cross-Platform PATH & Environment Management Subsystem
Authoritative Reference: STAR_DISTRIBUTION.md (Section 3 & 7)
"""

import os
import sys
import platform
from typing import Dict, Any, Optional, List, Tuple


class PathManager:
    """
    Manages automated registration and verification of Star binary directories in system and user PATH.
    """

    @classmethod
    def get_default_install_dir(cls) -> str:
        sys_name = platform.system().lower()
        if sys_name == "windows":
            prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
            return os.path.join(prog_files, "Star")
        elif sys_name == "darwin":
            return "/opt/star"
        else: # Linux
            return "/usr/local/star"

    @classmethod
    def get_bin_dir(cls, install_dir: Optional[str] = None) -> str:
        base = install_dir or cls.get_default_install_dir()
        return os.path.join(base, "bin")

    @classmethod
    def is_in_path(cls, bin_dir: Optional[str] = None) -> bool:
        target = bin_dir or cls.get_bin_dir()
        target_norm = os.path.normpath(target).lower()
        current_paths = [os.path.normpath(p).lower() for p in os.environ.get("PATH", "").split(os.pathsep) if p]
        return target_norm in current_paths

    @classmethod
    def add_to_windows_path(cls, bin_dir: str) -> bool:
        if platform.system().lower() != "windows":
            return False

        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except WindowsError:
                current_path = ""

            paths = current_path.split(";") if current_path else []
            norm_target = os.path.normpath(bin_dir)
            if not any(os.path.normpath(p) == norm_target for p in paths if p):
                paths.append(norm_target)
                new_path = ";".join(paths)
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                cls.broadcast_windows_environment_change()

            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    @classmethod
    def broadcast_windows_environment_change(cls) -> None:
        if platform.system().lower() == "windows":
            try:
                import ctypes
                HWND_BROADCAST = 0xFFFF
                WM_SETTINGCHANGE = 0x001A
                SMTO_ABORTIFHUNG = 0x0002
                result = ctypes.c_long()
                ctypes.windll.user32.SendMessageTimeoutW(
                    HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
                    SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
                )
            except Exception:
                pass

    @classmethod
    def add_to_unix_path(cls, bin_dir: str) -> bool:
        home = os.path.expanduser("~")
        rc_files = [os.path.join(home, ".bashrc"), os.path.join(home, ".zshrc"), os.path.join(home, ".profile")]
        export_line = f'\nexport PATH="{bin_dir}:$PATH"\n'

        updated = False
        for rc in rc_files:
            if os.path.exists(rc):
                with open(rc, "r", encoding="utf-8") as f:
                    content = f.read()
                if bin_dir not in content:
                    with open(rc, "a", encoding="utf-8") as f:
                        f.write(export_line)
                    updated = True
        return updated

    @classmethod
    def add_to_path(cls, bin_dir: Optional[str] = None) -> Tuple[bool, str]:
        target = bin_dir or cls.get_bin_dir()
        if cls.is_in_path(target):
            return True, f"'{target}' is already present in PATH."
        sys_name = platform.system().lower()
        if sys_name == "windows":
            ok = cls.add_to_windows_path(target)
        else:
            ok = cls.add_to_unix_path(target)
        if ok:
            return True, f"Successfully added '{target}' to PATH."
        return False, f"Could not automatically add '{target}' to PATH."

    @classmethod
    def configure_path(cls, install_dir: Optional[str] = None) -> Dict[str, Any]:
        bin_dir = cls.get_bin_dir(install_dir)
        sys_name = platform.system().lower()

        if sys_name == "windows":
            ok = cls.add_to_windows_path(bin_dir)
        else:
            ok = cls.add_to_unix_path(bin_dir)

        return {
            "bin_dir": bin_dir,
            "status": "CONFIGURED" if ok else "SKIPPED",
            "is_in_path": cls.is_in_path(bin_dir) or ok
        }
