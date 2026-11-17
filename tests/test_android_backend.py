"""
Unit Tests for Star Android Native Backend Subsystem & Signing Management
"""

import unittest
import os
import shutil
import zipfile
from star_backend.mobile.android.input_bridge import AndroidInputBridge, AndroidMotionEventAction
from star_backend.mobile.android.surface_renderer import AndroidSurfaceRenderer
from star_backend.mobile.android.activity import StarActivity
from star_backend.mobile.android.device_bridge import AndroidDeviceBridge
from star_backend.mobile.android.project_generator import AndroidProjectGenerator
from star_backend.mobile.android.signing import AndroidSigner, AndroidSigningConfig, AndroidSigningError
from star_backend.mobile.android.builder import AndroidBuilder
from star_backend.mobile.packaging import MobilePackager
from star_runtime.mobile.abi import MobileRenderOp
from star_backend.mobile.renderer import MobileDrawCommand


class TestAndroidBackend(unittest.TestCase):
    def setUp(self):
        self.test_src = "test_android_app.star"
        with open(self.test_src, "w", encoding="utf-8") as f:
            f.write("""
use UI
use Mobile

app AndroidTest
    variable count = 0
    UI.safe_area(
        UI.app_bar("Android Demo"),
        UI.card(
            UI.title("Testing Android Backend"),
            UI.button("+ Tap", function()
                count = count + 1
                Mobile.Vibrate()
            end)
        )
    )
end
""")
        self.builder = AndroidBuilder()

    def tearDown(self):
        if os.path.exists(self.test_src):
            os.remove(self.test_src)
        if os.path.exists("build/android"):
            shutil.rmtree("build/android", ignore_errors=True)

    def test_android_motion_event_translation(self):
        bridge = AndroidInputBridge()

        # Action Down
        bridge.handle_motion_event(AndroidMotionEventAction.ACTION_DOWN, pointer_id=1, x=150.0, y=200.0)
        # Action Up
        gestures = bridge.handle_motion_event(AndroidMotionEventAction.ACTION_UP, pointer_id=1, x=152.0, y=201.0)

        self.assertEqual(len(gestures), 1)
        self.assertEqual(gestures[0].name, "Tap")

    def test_android_activity_lifecycle(self):
        activity = StarActivity(package_name="org.starlang.test")
        self.assertEqual(activity.state, "initialized")

        activity.on_create()
        self.assertEqual(activity.state, "created")

        activity.on_start()
        self.assertEqual(activity.state, "started")

        activity.on_resume()
        self.assertEqual(activity.state, "resumed")
        self.assertTrue(activity.is_active)

        activity.on_pause()
        self.assertEqual(activity.state, "paused")
        self.assertFalse(activity.is_active)

        activity.on_destroy()
        self.assertEqual(activity.state, "destroyed")

    def test_android_surface_renderer(self):
        renderer = AndroidSurfaceRenderer()
        renderer.begin_frame(390.0, 844.0)

        cmd1 = MobileDrawCommand(MobileRenderOp.DRAW_APP_BAR, 0, 0, 390, 56, {"title": "App"})
        cmd2 = MobileDrawCommand(MobileRenderOp.DRAW_BUTTON, 20, 100, 350, 48, {"label": "Click"})

        renderer.execute_command(cmd1)
        renderer.execute_command(cmd2)
        renderer.end_frame()

        self.assertEqual(len(renderer.rendered_frames), 1)
        self.assertEqual(len(renderer.rendered_frames[0]), 2)

    def test_android_device_bridge(self):
        device = AndroidDeviceBridge()
        device.vibrate(pattern=[0, 100, 50, 100])
        self.assertEqual(len(device._vibration_log), 1)

        device.storage_set("token", "android_sec_123")
        self.assertEqual(device.storage_get("token"), "android_sec_123")

        battery = device.get_battery_info()
        self.assertGreater(battery["level"], 0.0)

    def test_debug_keystore_provisioning_and_signing(self):
        debug_cfg = AndroidSigner.get_or_create_debug_keystore()
        self.assertTrue(os.path.exists(debug_cfg.keystore_path))
        self.assertEqual(debug_cfg.alias, "androiddebugkey")
        self.assertTrue(debug_cfg.is_debug)

    def test_build_apk_with_signing(self):
        apk_path = self.builder.build_apk(self.test_src)
        self.assertTrue(os.path.exists(apk_path))
        self.assertTrue(apk_path.endswith(".apk"))

        # Verify APK archive contents & signature block
        with zipfile.ZipFile(apk_path, "r") as apk_zf:
            namelist = apk_zf.namelist()
            self.assertIn("AndroidManifest.xml", namelist)
            self.assertIn("assets/app.starmobile", namelist)
            self.assertIn("classes.dex", namelist)
            self.assertIn("lib/arm64-v8a/libstarnative.so", namelist)
            self.assertIn("META-INF/MANIFEST.MF", namelist)
            self.assertIn("META-INF/CERT.SF", namelist)
            self.assertIn("META-INF/CERT.RSA", namelist)

    def test_build_aab_app_bundle(self):
        aab_path = self.builder.build_aab(self.test_src)
        self.assertTrue(os.path.exists(aab_path))
        self.assertTrue(aab_path.endswith(".aab"))

        with zipfile.ZipFile(aab_path, "r") as aab_zf:
            namelist = aab_zf.namelist()
            self.assertIn("base/manifest/AndroidManifest.xml", namelist)
            self.assertIn("base/assets/app.starmobile", namelist)
            self.assertIn("base/dex/classes.dex", namelist)
            self.assertIn("base/lib/arm64-v8a/libstarnative.so", namelist)
            self.assertIn("BundleConfig.pb", namelist)
            self.assertIn("META-INF/MANIFEST.MF", namelist)

    def test_build_android_complete_suite(self):
        apk_path, aab_path = self.builder.build_android(self.test_src)
        self.assertTrue(os.path.exists(apk_path))
        self.assertTrue(os.path.exists(aab_path))

    def test_release_mode_requires_configured_key(self):
        # Building release without configuring keystore should raise AndroidSigningError
        with self.assertRaises(AndroidSigningError):
            self.builder.build_apk(self.test_src, release=True)

    def test_run_android_simulation(self):
        res = self.builder.run_android(self.test_src)
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()
