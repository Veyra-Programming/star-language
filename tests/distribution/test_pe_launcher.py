"""
Unit Tests for Star Native Windows PE Launchers & Dual 64/32-Bit Architecture Compatibility
Authoritative Reference: STAR_DISTRIBUTION.md & STAR_COMPATIBILITY.md
"""

import unittest
import os
import subprocess
import sys
from star_distribution.pe_launcher import PELauncherCompiler
from star_engine import __version__


class TestPELauncher(unittest.TestCase):
    def setUp(self):
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    def test_root_launchers_pe_headers(self):
        """Verify that root star.exe, starc.exe, and star-runtime.exe have authentic PE headers."""
        launchers = ["star.exe", "starc.exe", "star-runtime.exe"]
        for bname in launchers:
            exe_path = os.path.join(self.repo_root, bname)
            self.assertTrue(os.path.exists(exe_path), f"Launcher {bname} does not exist in repo root")

            info = PELauncherCompiler.verify_pe_header(exe_path)
            self.assertTrue(info["valid"], f"Launcher {bname} failed PE validation: {info.get('error')}")
            self.assertEqual(info["dos_header"], "MZ")
            self.assertEqual(info["pe_signature"], "PE\\0\\0")
            self.assertGreater(info["size_bytes"], 1024, "File size must be greater than dummy byte file")

    def test_distribution_launchers_pe_headers(self):
        """Verify that distribution staging bin directory contains verified PE executables."""
        dist_bin = os.path.join(self.repo_root, "dist", "Star-1.2.0-Windows-x64", "bin")
        if not os.path.exists(dist_bin):
            self.skipTest("Distribution staging directory not yet generated")

        launchers = ["star.exe", "starc.exe", "star-runtime.exe"]
        for bname in launchers:
            exe_path = os.path.join(dist_bin, bname)
            self.assertTrue(os.path.exists(exe_path), f"Launcher {bname} missing from dist bin")

            info = PELauncherCompiler.verify_pe_header(exe_path)
            self.assertTrue(info["valid"], f"Launcher {bname} in dist failed PE validation: {info.get('error')}")
            self.assertEqual(info["dos_header"], "MZ")
            self.assertEqual(info["pe_signature"], "PE\\0\\0")

    def test_native_star_exe_execution_version(self):
        """Verify that star.exe runs natively and reports architecture and version without error."""
        star_exe = os.path.join(self.repo_root, "star.exe")
        try:
            res = subprocess.run([star_exe, "--version"], cwd=self.repo_root, capture_output=True, text=True, encoding="utf-8", errors="replace")
        except PermissionError:
            self.skipTest("Application Control policy restricts local executable execution")
        except OSError as e:
            if "blocked" in str(e).lower() or getattr(e, 'winerror', None) == 1260:
                self.skipTest("Application Control policy restricts local executable execution")
            raise
        if res.returncode != 0 and ("blocked" in res.stderr.lower() or "application control policy" in res.stderr.lower()):
            self.skipTest("Application Control policy restricts local executable execution")
        self.assertEqual(res.returncode, 0, f"star.exe --version failed: {res.stderr}")
        self.assertIn("Star Programming Language", res.stdout)
        self.assertIn(__version__, res.stdout)
        self.assertIn("Architecture:", res.stdout)
        self.assertIn("Dual x64 / x86 Compatibility", res.stdout)

    def test_native_compile_and_run_pipeline(self):
        """Verify compiling a source file with starc.exe and executing bytecode with star-runtime.exe."""
        starc_exe = os.path.join(self.repo_root, "starc.exe")
        star_runtime_exe = os.path.join(self.repo_root, "star-runtime.exe")
        hello_src = os.path.join(self.repo_root, "examples", "hello.star")
        hello_byte = os.path.join(self.repo_root, "examples", "hello.starb")

        # 1. Compile
        try:
            compile_res = subprocess.run([starc_exe, hello_src], cwd=self.repo_root, capture_output=True, text=True, encoding="utf-8", errors="replace")
        except PermissionError:
            self.skipTest("Application Control policy restricts local executable execution")
        except OSError as e:
            if "blocked" in str(e).lower() or getattr(e, 'winerror', None) == 1260:
                self.skipTest("Application Control policy restricts local executable execution")
            raise
        if compile_res.returncode != 0 and ("blocked" in compile_res.stderr.lower() or "application control policy" in compile_res.stderr.lower()):
            self.skipTest("Application Control policy restricts local executable execution")
        self.assertEqual(compile_res.returncode, 0, f"starc.exe compilation failed: {compile_res.stderr}")
        self.assertTrue(os.path.exists(hello_byte))

        # 2. Run
        try:
            run_res = subprocess.run([star_runtime_exe, hello_byte], cwd=self.repo_root, capture_output=True, text=True, encoding="utf-8", errors="replace")
        except PermissionError:
            self.skipTest("Application Control policy restricts local executable execution")
        except OSError as e:
            if "blocked" in str(e).lower() or getattr(e, 'winerror', None) == 1260:
                self.skipTest("Application Control policy restricts local executable execution")
            raise
        if run_res.returncode != 0 and ("blocked" in run_res.stderr.lower() or "application control policy" in run_res.stderr.lower()):
            self.skipTest("Application Control policy restricts local executable execution")
        self.assertEqual(run_res.returncode, 0, f"star-runtime.exe failed: {run_res.stderr}")
        self.assertIn("Hello, World!", run_res.stdout)

    def test_doctor_production_architecture_matrix(self):
        """Verify that star doctor --production reports Architecture & Launchers validation."""
        star_exe = os.path.join(self.repo_root, "star.exe")
        try:
            res = subprocess.run([star_exe, "doctor", "--production"], cwd=self.repo_root, capture_output=True, text=True, encoding="utf-8", errors="replace")
        except PermissionError:
            self.skipTest("Application Control policy restricts local executable execution")
        except OSError as e:
            if "blocked" in str(e).lower() or getattr(e, 'winerror', None) == 1260:
                self.skipTest("Application Control policy restricts local executable execution")
            raise
        if res.returncode != 0 and ("blocked" in res.stderr.lower() or "application control policy" in res.stderr.lower()):
            self.skipTest("Application Control policy restricts local executable execution")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Architecture & Launchers:", res.stdout)
        self.assertIn("16-Bit Shield:", res.stdout)
        self.assertIn("PE Launcher Standard:", res.stdout)


if __name__ == "__main__":
    unittest.main()
