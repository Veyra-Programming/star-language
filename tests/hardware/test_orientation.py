"""
Hardware Test: Screen Orientation Locking & Dynamic Layout
"""

import unittest
from star_sdk.mobile.device_apis import OrientationAPI, ScreenAPI


class TestOrientationHardware(unittest.TestCase):
    def test_orientation_transitions(self):
        initial = OrientationAPI.current()
        OrientationAPI.lock("landscape")
        self.assertEqual(OrientationAPI.current(), "landscape")
        OrientationAPI.unlock()
        self.assertIsNotNone(OrientationAPI.current())


if __name__ == "__main__":
    unittest.main()
