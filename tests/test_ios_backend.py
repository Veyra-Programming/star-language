"""
Unit Tests for Star iOS Native Backend Subsystem
"""

import unittest
import os
import shutil
import zipfile
from star_backend.mobile.ios.touch_bridge import iOSTouchBridge, iOSUITouchPhase
from star_backend.mobile.ios.metal_renderer import iOSMetalRenderer
from star_backend.mobile.ios.view_controller import StarViewController
from star_backend.mobile.ios.device_bridge import iOSDeviceBridge
from star_backend.mobile.ios.swift_bridge import SwiftNativeBridge
from star_backend.mobile.ios.xcode_generator import XcodeProjectGenerator
from star_backend.mobile.ios.builder import iOSBuilder
from star_runtime.mobile.abi import MobileRenderOp
from star_backend.mobile.renderer import MobileDrawCommand


class TestiOSBackend(unittest.TestCase):
    def setUp(self):
        self.test_src = "test_ios_app.star"
        with open(self.test_src, "w", encoding="utf-8") as f:
            f.write("""
use UI
use Mobile

app IOSTest
    variable count = 0
    UI.safe_area(
        UI.app_bar("iOS Demo"),
        UI.card(
            UI.title("Testing iOS Backend"),
            UI.button("+ Tap", function()
                count = count + 1
                Mobile.Vibrate()
            end)
        )
    )
end
""")
        self.builder = iOSBuilder()

    def tearDown(self):
        if os.path.exists(self.test_src):
            try:
                os.remove(self.test_src)
            except OSError:
                pass
        if os.path.exists("build/ios"):
            shutil.rmtree("build/ios", ignore_errors=True)

    def test_swift_bridge_generation(self):
        c_header = SwiftNativeBridge.generate_c_header()
        self.assertIn("star_ios_init_runtime", c_header)
        self.assertIn("star_ios_render_frame", c_header)

        swift_src = SwiftNativeBridge.generate_swift_bridge_source()
        self.assertIn("class StarNativeBridge", swift_src)
        self.assertIn("initRuntime", swift_src)

    def test_ios_touch_event_translation(self):
        bridge = iOSTouchBridge()

        # Touch Began
        bridge.handle_ui_touch(iOSUITouchPhase.BEGAN, touch_id=1, x=150.0, y=200.0)
        # Touch Ended
        gestures = bridge.handle_ui_touch(iOSUITouchPhase.ENDED, touch_id=1, x=152.0, y=201.0)

        self.assertEqual(len(gestures), 1)
        self.assertEqual(gestures[0].name, "Tap")

    def test_ios_view_controller_lifecycle(self):
        vc = StarViewController(app_name="TestApp")
        self.assertEqual(vc.state, "initialized")

        vc.view_did_load()
        self.assertEqual(vc.state, "loaded")

        vc.view_did_appear()
        self.assertEqual(vc.state, "resumed")
        self.assertTrue(vc.is_active)

        vc.view_did_disappear()
        self.assertEqual(vc.state, "paused")
        self.assertFalse(vc.is_active)

        vc.view_will_terminate()
        self.assertEqual(vc.state, "detached")

    def test_ios_metal_renderer(self):
        renderer = iOSMetalRenderer()
        renderer.begin_frame(393.0, 852.0)

        cmd1 = MobileDrawCommand(MobileRenderOp.DRAW_APP_BAR, 0, 0, 393, 56, {"title": "App"})
        cmd2 = MobileDrawCommand(MobileRenderOp.DRAW_BUTTON, 20, 100, 350, 48, {"label": "Click"})

        renderer.execute_command(cmd1)
        renderer.execute_command(cmd2)
        renderer.end_frame()

        self.assertEqual(len(renderer.rendered_frames), 1)
        self.assertEqual(len(renderer.rendered_frames[0]), 2)

    def test_ios_device_bridge(self):
        device = iOSDeviceBridge()
        device.vibrate("heavy")
        self.assertEqual(len(device._haptics_log), 1)

        device.storage_set("token", "ios_keychain_sec_456")
        self.assertEqual(device.storage_get("token"), "ios_keychain_sec_456")

        battery = device.get_battery_info()
        self.assertGreater(battery["level"], 0.0)

    def test_build_xcode_project_and_ipa(self):
        ipa_path = self.builder.build_ipa(self.test_src)
        self.assertTrue(os.path.exists(ipa_path))
        self.assertTrue(ipa_path.endswith(".ipa"))

        # Verify IPA archive contents
        with zipfile.ZipFile(ipa_path, "r") as ipa_zf:
            namelist = ipa_zf.namelist()
            self.assertIn("Payload/Iostest.app/Info.plist", namelist)
            self.assertIn("Payload/Iostest.app/app.starmobile", namelist)
            self.assertIn("Payload/Iostest.app/Iostest", namelist)
            self.assertIn("Payload/Iostest.app/_CodeSignature/CodeResources", namelist)

        # Verify generated Xcode project
        proj_dir = os.path.join("build", "ios", "project")
        self.assertTrue(os.path.exists(os.path.join(proj_dir, "Iostest.xcodeproj", "project.pbxproj")))
        self.assertTrue(os.path.exists(os.path.join(proj_dir, "Iostest", "AppDelegate.swift")))
        self.assertTrue(os.path.exists(os.path.join(proj_dir, "Iostest", "StarViewController.swift")))
        self.assertTrue(os.path.exists(os.path.join(proj_dir, "Iostest", "StarMetalView.swift")))

    def test_run_ios_simulation(self):
        res = self.builder.run_ios(self.test_src)
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()
