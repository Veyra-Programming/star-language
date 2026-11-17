"""
Unit Tests for Star 0.6 Desktop Backend & Runtime
Authoritative Reference: STAR_DESKTOP.md
"""

import unittest
from star_backend.desktop.window import DesktopWindow
from star_backend.desktop.runtime import DesktopRuntime
from star_backend.desktop.compiler import DesktopCompiler
from star_backend.desktop.builder import DesktopBuilder
from star_engine.types import StarVirtualNode


class TestDesktopBackend(unittest.TestCase):
    def test_desktop_window_headless(self):
        win = DesktopWindow(title="Test Window", width=400, height=300, headless=True)
        win.draw_rect(10, 10, 100, 50, fill="#ffffff")
        win.draw_text(20, 20, "Hello Desktop")
        self.assertEqual(len(win.draw_commands), 2)
        self.assertEqual(win.draw_commands[0]["type"], "rect")
        self.assertEqual(win.draw_commands[1]["type"], "text")

    def test_desktop_runtime_layout_and_hit_testing(self):
        vnode = StarVirtualNode("column", children=[
            StarVirtualNode("title", props={"content": "App Title"}),
            StarVirtualNode("card", children=[
                StarVirtualNode("text", props={"content": "Card Content"}),
                StarVirtualNode("button", props={"label": "Click Me"}, listeners={"click": lambda: clicked.append(True)})
            ])
        ])

        clicked = []
        runtime = DesktopRuntime(headless=True)
        runtime.mount(vnode)

        self.assertIsNotNone(runtime.layout_root)
        self.assertEqual(runtime.layout_root.vnode.tag, "column")
        self.assertTrue(len(runtime.interactive_elements) > 0)

        # Simulate click on button
        success = runtime.simulate_click("Click Me")
        self.assertTrue(success)
        self.assertEqual(len(clicked), 1)

    def test_desktop_compiler_and_bundle(self):
        source = """
use UI
app TestApp
    UI.title("Compiled Desktop App")
end
"""
        compiler = DesktopCompiler(source_code=source, filename="app.star")
        bundle = compiler.compile()
        self.assertEqual(bundle["target"], "desktop")
        self.assertEqual(bundle["version"], "0.6.0")
        self.assertIn("bytecode_hex", bundle)

    def test_desktop_builder_build_and_run(self):
        builder = DesktopBuilder(project_dir=".")
        # Test running desktop counter example headless
        exit_code = builder.run("examples/desktop_counter.star", headless=True)
        self.assertEqual(exit_code, 0)

        # Test running desktop todo example headless
        exit_code = builder.run("examples/desktop_todo.star", headless=True)
        self.assertEqual(exit_code, 0)

        # Test running ui_showcase example headless
        exit_code = builder.run("examples/ui_showcase.star", headless=True)
        self.assertEqual(exit_code, 0)

    def test_desktop_window_advanced_draw_commands(self):
        win = DesktopWindow(title="Advanced Window", width=600, height=400, headless=True)
        win.draw_rect(10, 10, 100, 50, fill="#1e293b", corner_radius=12)
        win.draw_gradient_rect(10, 70, 100, 50, "#6366f1", "#a855f7", corner_radius=8)
        win.draw_shadow(10, 130, 100, 50, corner_radius=8, elevation=2)
        win.draw_switch(10, 190, 48, 26, active=True)
        win.draw_slider(10, 230, 100, 24, value=75.0, min_v=0.0, max_v=100.0)
        win.draw_tabs(10, 270, 200, 36, tabs=["Tab A", "Tab B"], active_idx=0)
        win.draw_toast(10, 320, 200, 40, "Test notification", variant="success")
        win.draw_icon(250, 20, "star", size=24, fill="#38bdf8")
        win.draw_avatar(250, 60, size=36, label="ST")

        types = [cmd["type"] for cmd in win.draw_commands]
        self.assertIn("rect", types)
        self.assertIn("gradient_rect", types)
        self.assertIn("shadow", types)
        self.assertIn("switch", types)
        self.assertIn("slider", types)
        self.assertIn("tabs", types)
        self.assertIn("toast", types)
        self.assertIn("icon", types)

    def test_desktop_runtime_extended_controls_hit_testing(self):
        state = {"switched": False, "tab": 0, "checked": False}
        vnode = StarVirtualNode("column", children=[
            StarVirtualNode("switch", props={"value": False}, listeners={"change": lambda: state.update({"switched": True})}),
            StarVirtualNode("tabs", props={"items": ["Home", "Settings"], "active": 0}, listeners={"select": lambda: state.update({"tab": 1})}),
            StarVirtualNode("checkbox", props={"label": "Agree", "checked": False}, listeners={"change": lambda: state.update({"checked": True})})
        ])

        runtime = DesktopRuntime(headless=True)
        runtime.mount(vnode)
        self.assertEqual(len(runtime.interactive_elements), 4)  # 1 switch + 2 tabs + 1 checkbox

        # Simulate switch toggle
        sw_tag = [tag for *_, tag in runtime.interactive_elements if tag.startswith("switch:")][0]
        self.assertTrue(runtime.simulate_click(sw_tag))
        self.assertTrue(state["switched"])

        # Simulate checkbox toggle
        cb_tag = [tag for *_, tag in runtime.interactive_elements if tag.startswith("checkbox:")][0]
        self.assertTrue(runtime.simulate_click(cb_tag))
        self.assertTrue(state["checked"])


if __name__ == "__main__":
    unittest.main()

