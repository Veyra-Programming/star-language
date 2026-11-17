"""
Hardware Test: Safe Area & Screen Edge Insets
"""

import unittest
from star_sdk.mobile.safe_area import SafeAreaInsets


class TestSafeAreaHardware(unittest.TestCase):
    def test_dynamic_island_insets(self):
        insets = SafeAreaInsets(top=59.0, bottom=34.0, left=0.0, right=0.0)
        rect = insets.apply_to_rect(0, 0, 393.0, 852.0)
        self.assertEqual(rect["y"], 59.0)
        self.assertEqual(rect["height"], 852.0 - 59.0 - 34.0)


if __name__ == "__main__":
    unittest.main()
