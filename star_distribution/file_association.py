"""
Star Windows File Association and Explorer Integration Subsystem
Authoritative Reference: STAR_ROADMAP.md & STAR_DISTRIBUTION.md
"""

import os
import sys
import platform
import subprocess
from typing import Tuple, Optional


class FileAssociationManager:
    r"""
    Manages automated registration of Star file extensions (.star, .starb, .starmobile)
    in Windows Registry (HKCU\Software\Classes) with custom multi-resolution icons,
    MIME types, and File Explorer context menu actions.
    """

    @classmethod
    def get_star_home(cls) -> str:
        # Determine root Star Language directory
        curr = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(curr)
        return root

    @classmethod
    def is_windows(cls) -> bool:
        return platform.system().lower() == "windows"

    @classmethod
    def notify_shell(cls) -> None:
        """
        Broadcast SHCNE_ASSOCCHANGED to Windows Shell (File Explorer)
        so icon cache and file handlers refresh immediately without reboot.
        """
        if not cls.is_windows():
            return

        try:
            import ctypes
            SHCNE_ASSOCCHANGED = 0x08000000
            SHCNF_IDLIST = 0x0000
            ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
        except Exception:
            pass

        try:
            # Refresh Windows icon cache helper if present
            subprocess.run(["ie4uinit.exe", "-show"], capture_output=True, timeout=3)
        except Exception:
            pass

    @classmethod
    def is_registered(cls) -> bool:
        if not cls.is_windows():
            return False

        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.star") as k:
                val, _ = winreg.QueryValueEx(k, "")
                return val == "Star.SourceFile"
        except Exception:
            return False

    @classmethod
    def register(cls, star_home: Optional[str] = None) -> Tuple[bool, str]:
        """
        Registers .star, .starb, and .starmobile file extensions with Explorer icons and actions.
        """
        if not cls.is_windows():
            return False, "File associations are only supported on Windows."

        import winreg

        home = star_home or cls.get_star_home()
        star_bat = os.path.join(home, "star.bat")
        star_exe = os.path.join(home, "star.exe")
        launcher = star_bat if os.path.exists(star_bat) else (star_exe if os.path.exists(star_exe) else "star")

        icons_dir = os.path.join(home, "assets", "icons")
        if not os.path.exists(icons_dir):
            icons_dir = os.path.join(home, "assets")

        source_ico = os.path.join(icons_dir, "star_source.ico")
        if not os.path.exists(source_ico):
            source_ico = os.path.join(home, "assets", "star_file.ico")

        bytecode_ico = os.path.join(icons_dir, "star_bytecode.ico")
        if not os.path.exists(bytecode_ico):
            bytecode_ico = source_ico

        mobile_ico = os.path.join(icons_dir, "star_mobile.ico")
        if not os.path.exists(mobile_ico):
            mobile_ico = source_ico

        star_ico = os.path.join(icons_dir, "star.ico")
        if not os.path.exists(star_ico):
            star_ico = source_ico

        try:
            # 1. Register .star (Star Source File)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.star", "", "Star.SourceFile")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.star", "Content Type", "text/x-star")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.star", "PerceivedType", "text")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.star\OpenWithProgids", "Star.SourceFile", "")

            prog_key = r"Software\Classes\Star.SourceFile"
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, prog_key, "", "Star Source File")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, prog_key, "FriendlyTypeName", "Star Source File")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\DefaultIcon", "", f"{source_ico},0")

            # Shell actions for .star
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell", "", "open")

            # Open / Run with Star
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\open", "", "Run with Star")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\open", "Icon", source_ico)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\open\\command", "", f'"{launcher}" run "%1" %*')

            # Interactive REPL
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\interactive", "", "Run in Star Interactive Terminal")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\interactive", "Icon", star_ico)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\interactive\\command", "", f'cmd.exe /k ""{launcher}" run "%1""')

            # Compile to bytecode
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\compile", "", "Compile with Star (Bytecode)")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\compile", "Icon", bytecode_ico)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\compile\\command", "", f'cmd.exe /k ""{launcher}" compile "%1""')

            # Check syntax / lint
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\check", "", "Check Syntax with Star Doctor")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\check", "Icon", star_ico)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\check\\command", "", f'cmd.exe /k ""{launcher}" check "%1""')

            # Edit with Notepad
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\edit", "", "Edit with Notepad")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_key}\\shell\\edit\\command", "", 'notepad.exe "%1"')

            # 2. Register .starb (Compiled Bytecode)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.starb", "", "Star.BytecodeFile")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.starb", "PerceivedType", "application")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.starb\OpenWithProgids", "Star.BytecodeFile", "")

            prog_b = r"Software\Classes\Star.BytecodeFile"
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, prog_b, "", "Star Compiled Bytecode")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, prog_b, "FriendlyTypeName", "Star Compiled Bytecode")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_b}\\DefaultIcon", "", f"{bytecode_ico},0")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_b}\\shell", "", "open")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_b}\\shell\\open", "", "Execute with Star VM")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_b}\\shell\\open", "Icon", bytecode_ico)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_b}\\shell\\open\\command", "", f'"{launcher}" run "%1" %*')
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_b}\\shell\\disasm", "", "Disassemble Bytecode (Star IR)")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_b}\\shell\\disasm", "Icon", star_ico)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_b}\\shell\\disasm\\command", "", f'cmd.exe /k ""{launcher}" ir "%1""')

            # 3. Register .starmobile (Mobile App Bundle)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.starmobile", "", "Star.MobileBundle")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.starmobile", "PerceivedType", "application")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, r"Software\Classes\.starmobile\OpenWithProgids", "Star.MobileBundle", "")

            prog_m = r"Software\Classes\Star.MobileBundle"
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, prog_m, "", "Star Mobile Application Bundle")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, prog_m, "FriendlyTypeName", "Star Mobile Application Bundle")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_m}\\DefaultIcon", "", f"{mobile_ico},0")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_m}\\shell", "", "open")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_m}\\shell\\open", "", "Simulate Mobile App")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_m}\\shell\\open", "Icon", mobile_ico)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_m}\\shell\\open\\command", "", f'"{launcher}" simulate mobile "%1"')
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_m}\\shell\\deploy_android", "", "Deploy to Android Device")
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_m}\\shell\\deploy_android", "Icon", mobile_ico)
            cls._set_reg_val(winreg.HKEY_CURRENT_USER, f"{prog_m}\\shell\\deploy_android\\command", "", f'cmd.exe /k ""{launcher}" deploy android "%1""')

            # Broadcast change to Windows Explorer
            cls.notify_shell()
            return True, "Star file associations (.star, .starb, .starmobile) registered successfully."
        except Exception as e:
            return False, f"Failed to register file associations: {e}"

    @classmethod
    def unregister(cls) -> Tuple[bool, str]:
        if not cls.is_windows():
            return False, "File associations are only supported on Windows."

        import winreg

        keys = [
            r"Software\Classes\.star",
            r"Software\Classes\Star.SourceFile",
            r"Software\Classes\.starb",
            r"Software\Classes\Star.BytecodeFile",
            r"Software\Classes\.starmobile",
            r"Software\Classes\Star.MobileBundle",
        ]

        for k in keys:
            cls._delete_reg_key_tree(winreg.HKEY_CURRENT_USER, k)

        cls.notify_shell()
        return True, "Star file associations unregistered successfully."

    @classmethod
    def _set_reg_val(cls, root, subkey: str, name: str, val: str) -> None:
        import winreg
        with winreg.CreateKey(root, subkey) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, val)

    @classmethod
    def _delete_reg_key_tree(cls, root, subkey: str) -> None:
        import winreg
        try:
            with winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
                while True:
                    try:
                        child = winreg.EnumKey(key, 0)
                        cls._delete_reg_key_tree(root, f"{subkey}\\{child}")
                    except OSError:
                        break
            winreg.DeleteKey(root, subkey)
        except OSError:
            pass
