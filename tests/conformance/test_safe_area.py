"""
Cross-Platform Conformance Test: Safe Area Insets Contract
"""

import unittest
from star_sdk.mobile.safe_area import SafeAreaInsets


class TestSafeAreaConformance(unittest.TestCase):
    def test_safe_area_calculations(self):
        insets = SafeAreaInsets(top=59.0, bottom=34.0, left=0.0, right=0.0)
        padded_rect = insets.apply_to_rect(0, 0, 393.0, 852.0)

        self.assertEqual(padded_rect["x"], 0.0)
        self.assertEqual(padded_rect["y"], 59.0)
        self.assertEqual(padded_rect["width"], 393.0)
        self.assertEqual(padded_rect["height"], 852.0 - 59.0 - 34.0)


if __name__ == "__main__":
    unittest.main()
