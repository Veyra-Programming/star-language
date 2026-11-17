"""
Unit Tests for Star 0.6 Theme SDK
Authoritative Reference: STAR_UI.md
"""

import unittest
from star_sdk.theme import create_theme_module, THEME_PRESETS
from star_engine.types import StarText


class TestStarTheme(unittest.TestCase):
    def test_theme_tokens_and_presets(self):
        theme_mod = create_theme_module()
        self.assertEqual(theme_mod.name, "Theme")
        self.assertIn("primary", theme_mod.exports)
        self.assertIn("background", theme_mod.exports)
        self.assertIn("surface", theme_mod.exports)

    def test_theme_mode_switch(self):
        theme_mod = create_theme_module()
        set_mode_fn = theme_mod.get("set_mode")

        # Switch to light
        set_mode_fn.fn(StarText("light"))
        bg = theme_mod.get("background")
        self.assertEqual(bg.to_string(), THEME_PRESETS["light"]["background"])

        # Switch to cyberpunk
        set_mode_fn.fn(StarText("cyberpunk"))
        primary = theme_mod.get("primary")
        self.assertEqual(primary.to_string(), THEME_PRESETS["cyberpunk"]["primary"])


if __name__ == "__main__":
    unittest.main()
