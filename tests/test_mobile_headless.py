"""
End-to-End Headless Mobile Simulation Tests
"""

import unittest
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter
from star_engine.types import StarVirtualNode, StarInteger
from star_backend.mobile.headless import MobileHeadlessRuntime
from star_sdk.mobile.gestures import GestureType


class TestMobileHeadless(unittest.TestCase):
    def test_headless_counter_simulation(self):
        source = """
use UI
use Mobile

variable count = 0

UI.safe_area(
    UI.column(
        UI.title("Counter"),
        UI.button("Increment", function()
            count = count + 1
        end)
    )
)
"""
        lexer = Lexer(source, filename="test_mobile.star")
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename="test_mobile.star")
        program = parser.parse()
        interp = Interpreter(filename="test_mobile.star")
        root_vnode = interp.interpret(program)

        self.assertIsInstance(root_vnode, StarVirtualNode)

        # Initialize headless mobile runtime
        runtime = MobileHeadlessRuntime()
        layout = runtime.mount(root_vnode)

        self.assertEqual(layout.node_type, "safe_area")
        self.assertEqual(runtime.rendered_frames, 1)

        # Find button coordinates
        btn_layout = layout.children[0].children[1]
        self.assertEqual(btn_layout.node_type, "button")

        # Simulate tap on button
        gestures, hit_node = runtime.simulate_tap(btn_layout.x + 10, btn_layout.y + 10)
        self.assertIsNotNone(hit_node)
        self.assertEqual(hit_node.node_type, "button")

        # Verify state mutated
        count_val = interp.globals.get("count")
        self.assertEqual(count_val.value, 1)

    def test_headless_gestures_simulation(self):
        runtime = MobileHeadlessRuntime()
        
        # Test double tap simulation
        dt_gestures = runtime.simulate_double_tap(150.0, 200.0)
        dt_names = [g.name for g in dt_gestures]
        self.assertIn(GestureType.DOUBLE_TAP, dt_names)

        # Test swipe simulation
        swipe_gestures = runtime.simulate_swipe(50.0, 300.0, 250.0, 305.0, duration_ms=80.0)
        swipe_names = [g.name for g in swipe_gestures]
        self.assertIn(GestureType.SWIPE, swipe_names)

    def test_headless_rotation(self):
        runtime = MobileHeadlessRuntime()
        self.assertEqual(runtime.metrics.orientation, "portrait")
        self.assertEqual(runtime.metrics.width_dp, 390.0)

        runtime.rotate_device("landscape")
        self.assertEqual(runtime.metrics.orientation, "landscape")
        self.assertEqual(runtime.metrics.width_dp, 844.0)
        self.assertEqual(runtime.metrics.height_dp, 390.0)


if __name__ == "__main__":
    unittest.main()
