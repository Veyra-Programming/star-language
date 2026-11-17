"""
Unit Tests for Mobile Signing Subsystem (Android & iOS)
"""

import unittest
import os
from star_backend.mobile.android.signing import AndroidSigner, AndroidSigningConfig, AndroidSigningError
from star_backend.mobile.ios.signing import iOSSigner, iOSSigningConfig, iOSSigningError


class TestMobileSigning(unittest.TestCase):
    def test_android_debug_signing_auto_keystore(self):
        cfg = AndroidSigner.resolve_signing_config(release=False, profile="debug")
        self.assertTrue(cfg.is_debug)
        self.assertEqual(cfg.alias, "androiddebugkey")
        self.assertTrue(os.path.exists(cfg.keystore_path))

    def test_android_release_signing_requires_keystore(self):
        # Should raise AndroidSigningError if no production keystore is configured
        with self.assertRaises(AndroidSigningError):
            AndroidSigner.resolve_signing_config(manifest_signing_dict={}, release=True, profile="release")

    def test_ios_development_signing_defaults(self):
        cfg = iOSSigner.resolve_signing_config(release=False, profile="development")
        self.assertEqual(cfg.profile, "development")
        self.assertIsNotNone(cfg.team_id)

    def test_ios_distribution_signing_requires_credentials(self):
        # Should raise iOSSigningError if no distribution identity is configured
        with self.assertRaises(iOSSigningError):
            iOSSigner.resolve_signing_config(manifest_signing_dict={}, release=True, profile="distribution")


if __name__ == "__main__":
    unittest.main()
