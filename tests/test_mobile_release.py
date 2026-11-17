"""
Unit Tests for Unified Mobile Release Manager and Build Provenance
"""

import unittest
import os
import shutil
from star_backend.mobile.release import MobileReleaseManager
from star_backend.mobile.provenance import ProvenanceManager


class TestMobileRelease(unittest.TestCase):
    def setUp(self):
        self.test_src = "test_release_app.star"
        with open(self.test_src, "w", encoding="utf-8") as f:
            f.write("""
use UI
use Mobile

app ReleaseDemo
    UI.safe_area(
        UI.app_bar("Release Demo")
    )
end
""")
        self.manager = MobileReleaseManager()

    def tearDown(self):
        if os.path.exists(self.test_src):
            os.remove(self.test_src)
        if os.path.exists("build"):
            shutil.rmtree("build", ignore_errors=True)

    def test_build_android_suite(self):
        res = self.manager.build_android(self.test_src, profile="debug")
        self.assertTrue(os.path.exists(res["apk"]))
        self.assertTrue(os.path.exists(res["aab"]))
        self.assertTrue(os.path.exists(f"{res['apk']}.sha256"))
        self.assertTrue(os.path.exists(f"{res['aab']}.sha256"))

    def test_build_ios_suite(self):
        res = self.manager.build_ios(self.test_src, profile="development")
        self.assertTrue(os.path.exists(res["ipa"]))
        self.assertTrue(os.path.exists(res["project"]))
        self.assertTrue(os.path.exists(f"{res['ipa']}.sha256"))

    def test_release_mobile_workflow(self):
        status = self.manager.release_mobile(self.test_src, profile="debug")
        self.assertEqual(status, 0)


if __name__ == "__main__":
    unittest.main()
