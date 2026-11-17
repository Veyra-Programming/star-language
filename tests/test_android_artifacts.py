"""
Unit Tests for Android APK and AAB Artifact Verification
"""

import unittest
import os
import shutil
from star_backend.mobile.android.builder import AndroidBuilder
from star_backend.mobile.android.verify import AndroidVerifier


class TestAndroidArtifacts(unittest.TestCase):
    def setUp(self):
        self.test_src = "test_verify_app.star"
        with open(self.test_src, "w", encoding="utf-8") as f:
            f.write("""
use UI
use Mobile

app VerifyApp
    UI.safe_area(
        UI.app_bar("Verify Demo")
    )
end
""")
        self.builder = AndroidBuilder()

    def tearDown(self):
        if os.path.exists(self.test_src):
            os.remove(self.test_src)
        import glob
        for f in glob.glob("build/android/test_verify_app*"):
            if os.path.isfile(f):
                try: os.remove(f)
                except Exception: pass
            elif os.path.isdir(f):
                shutil.rmtree(f, ignore_errors=True)

    def test_verify_valid_apk(self):
        apk_path = self.builder.build_apk(self.test_src, release=False)
        result = AndroidVerifier.verify(apk_path)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.format_type, "apk")
        self.assertTrue(result.checks.get("Manifest", False))
        self.assertTrue(result.checks.get("Star Bundle", False))
        self.assertTrue(result.checks.get("Signature Block", False))

    def test_verify_valid_aab(self):
        aab_path = self.builder.build_aab(self.test_src, release=False)
        result = AndroidVerifier.verify(aab_path)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.format_type, "aab")
        self.assertTrue(result.checks.get("Manifest", False))
        self.assertTrue(result.checks.get("Bundle Config", False))


if __name__ == "__main__":
    unittest.main()
