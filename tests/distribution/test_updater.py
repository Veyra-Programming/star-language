"""
Unit Tests for Star Self-Updater
"""

import unittest
from star_distribution.updater import SelfUpdater


class TestSelfUpdater(unittest.TestCase):
    def test_check_for_update(self):
        res = SelfUpdater.check_for_update("1.0.0")
        self.assertEqual(res["latest_version"], "1.0.1")
        self.assertTrue(res["update_available"])

    def test_already_up_to_date(self):
        res = SelfUpdater.check_for_update("1.0.1")
        self.assertFalse(res["update_available"])


if __name__ == "__main__":
    unittest.main()
