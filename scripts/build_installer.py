"""
Star Inno Setup Windows Installer Builder
Locates ISCC.exe and compiles installer.iss into Star-1.2.0-Windows-x64-Setup.exe
"""

import os
import sys
import subprocess
import shutil
import hashlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def find_iscc() -> str:
    # 1. Check PATH
    which_iscc = shutil.which("iscc")
    if which_iscc:
        return which_iscc

    # 2. Check standard Inno Setup installation paths
    candidates = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c

    # 3. Check environment variable
    custom = os.environ.get("INNO_SETUP_HOME")
    if custom:
        cand = os.path.join(custom, "ISCC.exe")
        if os.path.exists(cand):
            return cand

    return ""


def build_installer():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    iss_file = os.path.join(repo_root, "installer.iss")

    if not os.path.exists(iss_file):
        print(f"Error: Inno script not found at '{iss_file}'", file=sys.stderr)
        return 1

    iscc_exe = find_iscc()
    if not iscc_exe:
        print("=" * 65)
        print("ℹ Inno Setup Compiler (ISCC.exe) not detected on this machine.")
        print("=" * 65)
        print("Star Inno Setup script created and ready at:")
        print(f"  --> {iss_file}")
        print("\nTo compile the standalone Windows Setup executable:")
        print("  1. Install Inno Setup (via winget: 'winget install JRSoftware.InnoSetup')")
        print("     or download from: https://jrsoftware.org/isdl.php")
        print(f"  2. Run: iscc \"{iss_file}\"")
        print("=" * 65)
        return 0

    print(f"🔨 Compiling Inno Setup Windows Installer using: {iscc_exe}...")
    res = subprocess.run([iscc_exe, iss_file], cwd=repo_root, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("Error compiling installer:", res.stderr, file=sys.stderr)
        return res.returncode

    out_exe = os.path.join(repo_root, "dist", "Star-1.2.0-Windows-x64-Setup.exe")
    if os.path.exists(out_exe):
        sha256 = hashlib.sha256()
        with open(out_exe, "rb") as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        print("=" * 65)
        print("✓ Star Windows Installer built successfully!")
        print(f"Installer: {out_exe}")
        print(f"Size:      {os.path.getsize(out_exe)} bytes")
        print(f"SHA-256:   {sha256.hexdigest()}")
        print("=" * 65)
    return 0


if __name__ == "__main__":
    sys.exit(build_installer())
