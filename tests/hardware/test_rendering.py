"""
Hardware Test: Render Command Stream Consumption
"""

import unittest
from star_backend.mobile.renderer import MobileDrawCommand
from star_runtime.mobile.abi import MobileRenderOp
from star_backend.mobile.android.surface_renderer import AndroidSurfaceRenderer
from star_backend.mobile.ios.metal_renderer import iOSMetalRenderer


class TestRenderingHardware(unittest.TestCase):
    def test_dual_renderer_command_consumption(self):
        cmd = MobileDrawCommand(MobileRenderOp.DRAW_CARD, 10, 20, 300, 150, {"elevation": 2})

        android_renderer = AndroidSurfaceRenderer()
        android_renderer.begin_frame(390.0, 844.0)
        android_renderer.execute_command(cmd)
        android_renderer.end_frame()
        self.assertEqual(len(android_renderer.rendered_frames), 1)

        ios_renderer = iOSMetalRenderer()
        ios_renderer.begin_frame(393.0, 852.0)
        ios_renderer.execute_command(cmd)
        ios_renderer.end_frame()
        self.assertEqual(len(ios_renderer.rendered_frames), 1)


if __name__ == "__main__":
    unittest.main()
