"""
Unit Tests for Star Mobile Unified Execution Runtime
"""

import unittest
import os
from star_engine.types import StarVirtualNode
from star_runtime.mobile.abi import MobileRenderOp
from star_backend.mobile.runtime import MobileRuntime
from star_backend.mobile.renderer import MobileHeadlessRenderer, MobileDrawCommand
from star_backend.mobile.packaging import MobilePackager


class TestMobileRuntime(unittest.TestCase):
    def setUp(self):
        self.renderer = MobileHeadlessRenderer()
        self.runtime = MobileRuntime(renderer=self.renderer)

    def test_render_node_generates_command_stream(self):
        vnode = StarVirtualNode("safe_area", children=[
            StarVirtualNode("app_bar", {"title": "Runtime Test"}),
            StarVirtualNode("card", children=[
                StarVirtualNode("title", {"content": "Heading"}),
                StarVirtualNode("button", {"label": "Click Me"}, listeners={"click": lambda: None})
            ])
        ])

        commands = self.runtime.render_node(vnode)
        self.assertGreater(len(commands), 0)
        self.assertEqual(self.runtime.frame_count, 1)

        ops = [cmd.op for cmd in commands]
        self.assertIn(MobileRenderOp.DRAW_APP_BAR, ops)
        self.assertIn(MobileRenderOp.DRAW_CARD, ops)
        self.assertIn(MobileRenderOp.DRAW_TEXT, ops)
        self.assertIn(MobileRenderOp.DRAW_BUTTON, ops)

        # Check renderer recorded frame
        last_frame = self.renderer.last_frame_commands
        self.assertEqual(len(last_frame), len(commands))

    def test_touch_dispatch_and_rotation(self):
        clicked = [False]
        vnode = StarVirtualNode("column", children=[
            StarVirtualNode("button", {"label": "Tap"}, listeners={"click": lambda: clicked.__setitem__(0, True)})
        ])

        self.runtime.render_node(vnode)
        btn_layout = self.runtime.current_layout.children[0]

        # Dispatch touch down & touch up
        self.runtime.dispatch_touch("down", pointer_id=1, x=btn_layout.x + 10, y=btn_layout.y + 10)
        self.runtime.dispatch_touch("up", pointer_id=1, x=btn_layout.x + 10, y=btn_layout.y + 10)

        self.assertTrue(clicked[0])

        # Rotate display
        self.runtime.rotate_display("landscape")
        self.assertEqual(self.runtime.metrics.orientation, "landscape")
        self.assertEqual(self.runtime.metrics.width_dp, 844.0)


if __name__ == "__main__":
    unittest.main()
