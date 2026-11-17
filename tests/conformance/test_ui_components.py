"""
Cross-Platform Conformance Test: Declarative UI Component Tree Contract
"""

import unittest
from star_sdk.ui import UI
from star_engine.types import StarVirtualNode


class TestUIComponentsConformance(unittest.TestCase):
    def test_mobile_ui_component_node_generation(self):
        app_bar = UI.app_bar("Title")
        self.assertIsInstance(app_bar, StarVirtualNode)
        self.assertEqual(app_bar.tag, "mobile_app_bar")

        button = UI.button("Click", None)
        self.assertIsInstance(button, StarVirtualNode)
        self.assertEqual(button.tag, "button")

        sw = UI.switch(True, None)
        self.assertIsInstance(sw, StarVirtualNode)
        self.assertEqual(sw.tag, "mobile_switch")

        sl = UI.slider(50.0, 0.0, 100.0, None)
        self.assertIsInstance(sl, StarVirtualNode)
        self.assertEqual(sl.tag, "mobile_slider")


if __name__ == "__main__":
    unittest.main()
