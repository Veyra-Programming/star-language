"""
Unit Tests for iOS Signing and IPA Artifact Verification
"""

import unittest
import os
import shutil
from star_backend.mobile.ios.builder import iOSBuilder
from star_backend.mobile.ios.verify import iOSVerifier
from star_backend.mobile.ios.signing import iOSSigner


class TestiOSSigning(unittest.TestCase):
    def setUp(self):
        self.test_src = "test_ios_verify.star"
        with open(self.test_src, "w", encoding="utf-8") as f:
            f.write("""
use UI
use Mobile

app IOSVerifyApp
    UI.safe_area(
        UI.app_bar("iOS Verify")
    )
end
""")
        self.builder = iOSBuilder()

    def tearDown(self):
        if os.path.exists(self.test_src):
            os.remove(self.test_src)
        if os.path.exists("build/ios"):
            shutil.rmtree("build/ios", ignore_errors=True)

    def test_verify_valid_ipa(self):
        ipa_path = self.builder.build_ipa(self.test_src, release=False)
        result = iOSVerifier.verify(ipa_path)
        self.assertTrue(result.is_valid)
        self.assertTrue(result.checks.get("Info.plist", False))
        self.assertTrue(result.checks.get("Star Bundle", False))
        self.assertTrue(result.checks.get("Code Signature", False))


if __name__ == "__main__":
    unittest.main()
