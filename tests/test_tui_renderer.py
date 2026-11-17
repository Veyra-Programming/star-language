"""
Unit Tests for Star Terminal UI (TUI) TrueColor Renderer
Authoritative Reference: STAR_UI.md
"""

import unittest
from star_backend.tui.renderer import TUIRenderer, strip_ansi, visible_len
from star_engine.types import StarVirtualNode


class TestTUIRenderer(unittest.TestCase):
    def test_strip_ansi_and_visible_len(self):
        colored_text = "\x1b[38;2;99;102;241m\x1b[1mHello Star\x1b[0m"
        self.assertEqual(strip_ansi(colored_text), "Hello Star")
        self.assertEqual(visible_len(colored_text), 10)

    def test_tui_render_title_badge_card(self):
        vnode = StarVirtualNode("card", children=[
            StarVirtualNode("title", props={"content": "Terminal Dashboard", "level": 1}),
            StarVirtualNode("text", props={"content": "Rendering in TrueColor ANSI"}),
            StarVirtualNode("badge", props={"label": "Production", "variant": "success"}),
            StarVirtualNode("button", props={"label": "Deploy"}),
            StarVirtualNode("switch", props={"value": True}),
            StarVirtualNode("progress", props={"value": 75, "max": 100})
        ])

        renderer = TUIRenderer(theme_mode="dark", max_width=60)
        output = renderer.render(vnode)

        clean_output = strip_ansi(output)
        self.assertIn("╭", clean_output)
        self.assertIn("╯", clean_output)
        self.assertIn("Terminal Dashboard", clean_output)
        self.assertIn("Production", clean_output)
        self.assertIn("Deploy", clean_output)
        self.assertIn("ON", clean_output)
        self.assertIn("75%", clean_output)

    def test_tui_render_grid_and_row(self):
        vnode = StarVirtualNode("grid", props={"columns": 2}, children=[
            StarVirtualNode("card", children=[StarVirtualNode("text", props={"content": "Card A"})]),
            StarVirtualNode("card", children=[StarVirtualNode("text", props={"content": "Card B"})])
        ])

        renderer = TUIRenderer(theme_mode="midnight", max_width=70)
        output = renderer.render(vnode)
        clean_output = strip_ansi(output)
        self.assertIn("Card A", clean_output)
        self.assertIn("Card B", clean_output)


if __name__ == "__main__":
    unittest.main()
