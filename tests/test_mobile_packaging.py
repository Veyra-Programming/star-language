"""
Unit Tests for Star Mobile Packaging (.starmobile) Subsystem
"""

import unittest
import os
import shutil
from star_backend.mobile.packaging import MobilePackager, MobileBundle, MobileBundleManifest


class TestMobilePackaging(unittest.TestCase):
    def setUp(self):
        self.packager = MobilePackager()
        self.test_src = "test_pack_app.star"
        with open(self.test_src, "w", encoding="utf-8") as f:
            f.write("""
use UI
use Mobile

app PackTest
    UI.safe_area(
        UI.title("Packaged App")
    )
end
""")
        self.output_bundle = "build/mobile/test_pack_app.starmobile"

    def tearDown(self):
        if os.path.exists(self.test_src):
            os.remove(self.test_src)
        if os.path.exists("build/mobile/test_pack_app.starmobile"):
            os.remove("build/mobile/test_pack_app.starmobile")

    def test_build_and_load_bundle(self):
        bundle_path = self.packager.build_bundle(self.test_src, output_path=self.output_bundle)
        self.assertTrue(os.path.exists(bundle_path))

        bundle = self.packager.load_bundle(bundle_path)
        self.assertEqual(bundle.manifest.name, "Test_pack_app")
        self.assertTrue(bundle.verify_checksum())
        self.assertGreater(len(bundle.bytecode_bytes), 0)
        self.assertIn("PackTest", bundle.source_code)


if __name__ == "__main__":
    unittest.main()
