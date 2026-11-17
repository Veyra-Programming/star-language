"""
Unit Tests for Star Mobile Layout Engine, Dimensions & Safe Area
"""

import unittest
from star_engine.types import StarVirtualNode, StarText
from star_sdk.mobile.dimensions import Dimension, DimensionUnit, ScreenMetrics
from star_sdk.mobile.safe_area import SafeAreaInsets
from star_backend.mobile.layout import MobileLayoutEngine, MobileLayoutNode


class TestMobileLayout(unittest.TestCase):
    def setUp(self):
        self.metrics = ScreenMetrics(width_dp=390.0, height_dp=844.0, density_scale=2.0)
        self.insets = SafeAreaInsets(top=47.0, bottom=34.0, left=0.0, right=0.0)
        self.engine = MobileLayoutEngine(self.metrics, self.insets)

    def test_dimension_parsing(self):
        d1 = Dimension.parse("100dp")
        self.assertEqual(d1.value, 100.0)
        self.assertEqual(d1.unit, DimensionUnit.DP)
        self.assertEqual(d1.resolve_to_px(self.metrics), 200.0)

        d2 = Dimension.parse("16sp")
        self.assertEqual(d2.value, 16.0)
        self.assertEqual(d2.unit, DimensionUnit.SP)

        d3 = Dimension.parse("50%")
        self.assertEqual(d3.resolve_to_px(self.metrics, parent_size_px=400.0), 200.0)

    def test_safe_area_bounds_calculation(self):
        safe_x, safe_y, safe_w, safe_h = self.insets.calculate_safe_bounds(self.metrics)
        self.assertEqual(safe_x, 0.0)
        self.assertEqual(safe_y, 47.0)
        self.assertEqual(safe_w, 390.0)
        self.assertEqual(safe_h, 844.0 - 47.0 - 34.0)

    def test_layout_safe_area_node(self):
        vnode = StarVirtualNode("safe_area", children=[
            StarVirtualNode("app_bar", {"title": "Test Bar"}),
            StarVirtualNode("button", {"label": "Click Me"}, listeners={"click": lambda: None})
        ])

        layout = self.engine.compute_layout(vnode)
        self.assertEqual(layout.node_type, "safe_area")
        self.assertEqual(len(layout.children), 2)
        # Child 0 (app_bar) should start at safe_y = 47.0
        self.assertEqual(layout.children[0].y, 47.0)

    def test_accessibility_touch_target_hit_testing(self):
        btn_vnode = StarVirtualNode("button", {"label": "Tap"}, listeners={"click": lambda: None})
        root_vnode = StarVirtualNode("column", children=[btn_vnode])

        layout = self.engine.compute_layout(root_vnode)
        btn_layout = layout.children[0]
        self.assertTrue(btn_layout.is_interactive)

        # Hit bounds should have at least 44x44 DP touch target
        hx, hy, hw, hh = btn_layout.hit_bounds
        self.assertGreaterEqual(hw, 44.0)
        self.assertGreaterEqual(hh, 44.0)

        # Hit test exact button center
        hit = self.engine.hit_test(layout, btn_layout.x + 10, btn_layout.y + 10)
        self.assertIsNotNone(hit)
        self.assertEqual(hit.node_type, "button")


if __name__ == "__main__":
    unittest.main()
