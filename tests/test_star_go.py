"""
Unit Tests for Star Go Universal Companion (Expo Go Architecture) & QR Code Subsystem
"""

import unittest
import os
import time
import json
import urllib.request
from star_backend.mobile.android.qr import QRCode
from star_backend.mobile.android.go_server import StarGoServer
from star_backend.mobile.android.builder import AndroidBuilder


class TestStarGo(unittest.TestCase):
    def test_qr_code_generation(self):
        text = "star://192.168.1.5:8088"
        qr = QRCode.encode(text)
        self.assertGreaterEqual(qr.size, 21)
        self.assertEqual(len(qr.matrix), qr.size)
        self.assertEqual(len(qr.matrix[0]), qr.size)

        # Check finder pattern in top-left
        self.assertEqual(qr.matrix[0][0], 1)
        self.assertEqual(qr.matrix[0][6], 1)
        self.assertEqual(qr.matrix[6][0], 1)

        # Terminal & SVG export
        term = qr.to_terminal()
        self.assertIn("\033[40m", term)

        term_compact = qr.to_terminal_compact()
        self.assertIn("█", term_compact)

        svg = qr.to_svg()
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)

    def test_star_go_server_endpoints(self):
        source_file = "examples/hello.star"
        if not os.path.exists(source_file):
            source_file = "examples/ui_motion_showcase.star"

        port = 8123
        server = StarGoServer(source_file, port=port)
        server.start(interactive=False)

        try:
            base_url = f"http://127.0.0.1:{port}"

            # 1. Test status endpoint
            with urllib.request.urlopen(f"{base_url}/status", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(data["status"], "online")

            # 2. Test manifest endpoint
            with urllib.request.urlopen(f"{base_url}/manifest.json", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                manifest = json.loads(resp.read().decode("utf-8"))
                self.assertIn("bundle_size", manifest)
                self.assertGreater(manifest["bundle_size"], 0)

            # 3. Test bundle download endpoint
            with urllib.request.urlopen(f"{base_url}/bundle.starmobile", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                bundle_bytes = resp.read()
                self.assertGreater(len(bundle_bytes), 0)

            # 4. Test QR SVG endpoint
            with urllib.request.urlopen(f"{base_url}/qr.svg", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                svg_data = resp.read().decode("utf-8")
                self.assertIn("<svg", svg_data)

            # 5. Test dashboard HTML
            with urllib.request.urlopen(f"{base_url}/", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                html = resp.read().decode("utf-8")
                self.assertIn("Star Go", html)

        finally:
            server.stop()

    def test_android_go_directory_structure(self):
        android_dir = "android"
        self.assertTrue(os.path.isdir(android_dir))

        # Project Gradle & wrapper files
        self.assertTrue(os.path.exists(os.path.join(android_dir, "build.gradle")))
        self.assertTrue(os.path.exists(os.path.join(android_dir, "settings.gradle")))
        self.assertTrue(os.path.exists(os.path.join(android_dir, "gradlew.bat")))
        self.assertTrue(os.path.exists(os.path.join(android_dir, "gradlew")))
        self.assertTrue(os.path.exists(os.path.join(android_dir, "gradle", "wrapper", "gradle-wrapper.properties")))

        # App sources
        app_dir = os.path.join(android_dir, "app")
        manifest_path = os.path.join(app_dir, "src", "main", "AndroidManifest.xml")
        self.assertTrue(os.path.exists(manifest_path))

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_content = f.read()
            self.assertIn("org.starlang.go", manifest_content)
            self.assertIn("QRScannerActivity", manifest_content)
            self.assertIn('android:scheme="star"', manifest_content)

        # Java class sources
        go_pkg = os.path.join(app_dir, "src", "main", "java", "org", "starlang", "go")
        self.assertTrue(os.path.exists(os.path.join(go_pkg, "MainActivity.java")))
        self.assertTrue(os.path.exists(os.path.join(go_pkg, "QRScannerActivity.java")))
        self.assertTrue(os.path.exists(os.path.join(go_pkg, "BundleDownloader.java")))
        self.assertTrue(os.path.exists(os.path.join(go_pkg, "DevMenuBottomSheet.java")))
        self.assertTrue(os.path.exists(os.path.join(go_pkg, "PerformanceOverlay.java")))

        # Native C++ JNI bridge
        cpp_dir = os.path.join(app_dir, "src", "main", "cpp")
        self.assertTrue(os.path.exists(os.path.join(cpp_dir, "CMakeLists.txt")))
        self.assertTrue(os.path.exists(os.path.join(cpp_dir, "star_jni_bridge.cpp")))

    def test_run_star_go_simulation(self):
        builder = AndroidBuilder()
        star_go_file = "examples/star_go.star"
        self.assertTrue(os.path.exists(star_go_file))
        res = builder.run_android(star_go_file)
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()

