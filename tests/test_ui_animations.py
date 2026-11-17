"""
Comprehensive Test Suite for Star UI Animation & Motion Suite + Extended UI Components
Verifies:
  - Mathematical Easing Curves & Cubic Bezier Solvers
  - Spring Harmonic Physical Oscillators
  - AnimationController & Tween Systems
  - Virtual Node Generators for All Motion Components
  - Virtual Node Generators for All 15+ New Widgets
  - Desktop Native Window & Layout Runtime Rendering
"""

import unittest
import math
import os
import sys

# Ensure repository root is in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from star_sdk.animation import (
    Curves, SpringSimulation, AnimationController, AnimationStatus,
    Tween, ColorTween, OffsetTween, resolve_curve,
    make_animated_opacity, make_animated_scale, make_animated_slide,
    make_animated_rotation, make_animated_container, make_shimmer,
    make_skeleton, make_pulse, make_bounce, make_shake, make_glow,
    make_marquee, make_confetti, make_ripple, create_animation_module
)
from star_sdk.ui import create_ui_module, UI
from star_engine.types import StarVirtualNode, StarText, StarInteger, StarList, StarMap
from star_backend.desktop.window import DesktopWindow
from star_backend.desktop.runtime import DesktopRuntime


class TestUIAnimationCurves(unittest.TestCase):
    def test_curves_boundaries_and_values(self):
        # Linear
        self.assertAlmostEqual(Curves.linear(0.0), 0.0)
        self.assertAlmostEqual(Curves.linear(0.5), 0.5)
        self.assertAlmostEqual(Curves.linear(1.0), 1.0)

        # Ease In / Out
        self.assertAlmostEqual(Curves.ease_in(0.0), 0.0)
        self.assertAlmostEqual(Curves.ease_in(0.5), 0.25)
        self.assertAlmostEqual(Curves.ease_in(1.0), 1.0)

        self.assertAlmostEqual(Curves.ease_out(0.0), 0.0)
        self.assertAlmostEqual(Curves.ease_out(0.5), 0.75)
        self.assertAlmostEqual(Curves.ease_out(1.0), 1.0)

        # Ease In Out
        self.assertAlmostEqual(Curves.ease_in_out(0.0), 0.0)
        self.assertAlmostEqual(Curves.ease_in_out(0.5), 0.5)
        self.assertAlmostEqual(Curves.ease_in_out(1.0), 1.0)

        # Bounce Out
        self.assertAlmostEqual(Curves.bounce_out(0.0), 0.0)
        self.assertAlmostEqual(Curves.bounce_out(1.0), 1.0)

        # Elastic Out
        self.assertAlmostEqual(Curves.elastic_out(0.0), 0.0)
        self.assertAlmostEqual(Curves.elastic_out(1.0), 1.0)

        # Cubic Bezier Solver
        bezier = Curves.cubic_bezier(0.25, 0.1, 0.25, 1.0)
        self.assertAlmostEqual(bezier(0.0), 0.0, places=2)
        self.assertAlmostEqual(bezier(1.0), 1.0, places=2)
        mid = bezier(0.5)
        self.assertTrue(0.0 <= mid <= 1.0)


class TestSpringSimulation(unittest.TestCase):
    def test_spring_oscillation_and_convergence(self):
        spring = SpringSimulation(mass=1.0, stiffness=180.0, damping=18.0)
        # At start
        pos0, vel0 = spring.evaluate(0.0)
        self.assertEqual(pos0, 0.0)

        # Over time it should approach target 1.0
        pos1, _ = spring.evaluate(1.0)
        self.assertAlmostEqual(pos1, 1.0, places=1)

        # At 3 seconds, should be settled
        self.assertTrue(spring.is_done(3.0, eps=0.05))


class TestAnimationControllerAndTweens(unittest.TestCase):
    def test_animation_controller_lifecycle(self):
        ctrl = AnimationController(duration_ms=200.0, lower_bound=0.0, upper_bound=1.0)
        self.assertEqual(ctrl.value, 0.0)
        self.assertEqual(ctrl.status, AnimationStatus.DISMISSED)

        values_recorded = []
        ctrl.add_listener(lambda v: values_recorded.append(v))

        ctrl.forward()
        self.assertTrue(ctrl.is_animating)
        self.assertEqual(ctrl.status, AnimationStatus.FORWARD)

        # Step halfway
        updated = ctrl.tick(100.0)
        self.assertTrue(updated)
        self.assertTrue(len(values_recorded) > 0)
        self.assertTrue(0.0 < ctrl.value <= 1.0)

        # Finish animation
        ctrl.tick(120.0)
        self.assertEqual(ctrl.status, AnimationStatus.COMPLETED)
        self.assertFalse(ctrl.is_animating)
        self.assertAlmostEqual(ctrl.value, 1.0)

    def test_tweens(self):
        t = Tween(begin=100.0, end=200.0)
        self.assertEqual(t.lerp(0.0), 100.0)
        self.assertEqual(t.lerp(0.5), 150.0)
        self.assertEqual(t.lerp(1.0), 200.0)

        ct = ColorTween("#000000", "#ffffff")
        mid_color = ct.lerp(0.5)
        self.assertEqual(mid_color.lower(), "#7f7f7f")

        ot = OffsetTween((10.0, 20.0), (30.0, 60.0))
        ox, oy = ot.lerp(0.5)
        self.assertEqual(ox, 20.0)
        self.assertEqual(oy, 40.0)


class TestDeclarativeMotionVirtualNodes(unittest.TestCase):
    def test_motion_virtual_nodes(self):
        op = make_animated_opacity(0.8, 400, "ease_in")
        self.assertEqual(op.tag, "animated_opacity")
        self.assertEqual(op.props["opacity"], 0.8)
        self.assertEqual(op.props["duration_ms"], 400)

        sc = make_animated_scale(1.2, 300, "overshoot")
        self.assertEqual(sc.tag, "animated_scale")
        self.assertEqual(sc.props["scale"], 1.2)

        sl = make_animated_slide(10.0, -20.0)
        self.assertEqual(sl.tag, "animated_slide")
        self.assertEqual(sl.props["offset_x"], 10.0)
        self.assertEqual(sl.props["offset_y"], -20.0)

        sh = make_shimmer(200, 30)
        self.assertEqual(sh.tag, "shimmer")
        self.assertEqual(sh.props["width"], 200)

        sk = make_skeleton(150, 20)
        self.assertEqual(sk.tag, "skeleton")
        self.assertEqual(sk.props["width"], 150)

        pu = make_pulse(0.9, 1.1)
        self.assertEqual(pu.tag, "pulse")

        bo = make_bounce(15.0)
        self.assertEqual(bo.tag, "bounce")

        shk = make_shake(5.0)
        self.assertEqual(shk.tag, "shake")

        gl = make_glow("#00f0ff", 24)
        self.assertEqual(gl.tag, "glow")
        self.assertEqual(gl.props["color"], "#00f0ff")

        mq = make_marquee("Star Language 2.1 Release", 60)
        self.assertEqual(mq.tag, "marquee")

        cf = make_confetti(100)
        self.assertEqual(cf.tag, "confetti")
        self.assertEqual(cf.props["count"], 100)


class TestExtendedUIWidgets(unittest.TestCase):
    def setUp(self):
        self.ui = create_ui_module()

    def test_new_widgets_virtual_nodes(self):
        # Modal
        modal_fn = self.ui.exports["modal"]
        m_node = modal_fn(StarText("Confirm Exit"), StarInteger(1))
        self.assertEqual(m_node.tag, "modal")
        self.assertEqual(m_node.props["title"], "Confirm Exit")
        self.assertTrue(m_node.props["open"])

        # Dialog
        dialog_fn = self.ui.exports["dialog"]
        d_node = dialog_fn(StarText("Alert"), StarText("Action Completed"))
        self.assertEqual(d_node.tag, "dialog")
        self.assertEqual(d_node.props["title"], "Alert")

        # Drawer
        drawer_fn = self.ui.exports["drawer"]
        dr_node = drawer_fn(StarInteger(1), StarText("left"))
        self.assertEqual(dr_node.tag, "drawer")
        self.assertEqual(dr_node.props["side"], "left")

        # Accordion
        acc_fn = self.ui.exports["accordion"]
        acc_node = acc_fn(StarText("FAQ Section"), StarInteger(0))
        self.assertEqual(acc_node.tag, "accordion")
        self.assertEqual(acc_node.props["title"], "FAQ Section")
        self.assertFalse(acc_node.props["expanded"])

        # Dropdown
        dd_fn = self.ui.exports["dropdown"]
        items = StarList([StarText("Alpha"), StarText("Beta")])
        dd_node = dd_fn(items, StarInteger(0))
        self.assertEqual(dd_node.tag, "dropdown")
        self.assertEqual(dd_node.props["items"], ["Alpha", "Beta"])

        # Breadcrumbs
        bc_fn = self.ui.exports["breadcrumbs"]
        bc_node = bc_fn(StarList([StarText("Home"), StarText("Docs"), StarText("UI")]))
        self.assertEqual(bc_node.tag, "breadcrumbs")
        self.assertEqual(len(bc_node.props["items"]), 3)

        # Pagination
        pg_fn = self.ui.exports["pagination"]
        pg_node = pg_fn(StarInteger(10), StarInteger(2))
        self.assertEqual(pg_node.tag, "pagination")
        self.assertEqual(pg_node.props["total"], 10)
        self.assertEqual(pg_node.props["current"], 2)

        # Table
        tbl_fn = self.ui.exports["table"]
        hdrs = StarList([StarText("Name"), StarText("Role")])
        rows = StarList([StarList([StarText("Alice"), StarText("Architect")])])
        tbl_node = tbl_fn(hdrs, rows)
        self.assertEqual(tbl_node.tag, "table")
        self.assertEqual(tbl_node.props["headers"], ["Name", "Role"])
        self.assertEqual(tbl_node.props["rows"], [["Alice", "Architect"]])

        # Code Block
        cb_fn = self.ui.exports["code_block"]
        cb_node = cb_fn(StarText("use UI\nUI.title('Hello')"), StarText("star"))
        self.assertEqual(cb_node.tag, "code_block")
        self.assertEqual(cb_node.props["language"], "star")

        # Segmented Control
        sc_fn = self.ui.exports["segmented_control"]
        sc_node = sc_fn(StarList([StarText("Day"), StarText("Night")]), StarInteger(1))
        self.assertEqual(sc_node.tag, "segmented_control")
        self.assertEqual(sc_node.props["selected"], 1)

        # Stepper
        st_fn = self.ui.exports["stepper"]
        st_node = st_fn(StarList([StarText("Cart"), StarText("Billing"), StarText("Finish")]), StarInteger(1))
        self.assertEqual(st_node.tag, "stepper")
        self.assertEqual(st_node.props["current"], 1)

        # Rating
        rt_fn = self.ui.exports["rating"]
        rt_node = rt_fn(StarInteger(4), StarInteger(5))
        self.assertEqual(rt_node.tag, "rating")
        self.assertEqual(rt_node.props["value"], 4.0)

        # FAB
        fab_fn = self.ui.exports["fab"]
        fab_node = fab_fn(StarText("Add"))
        self.assertEqual(fab_node.tag, "fab")
        self.assertEqual(fab_node.props["label"], "Add")

        # Bottom Sheet
        bs_fn = self.ui.exports["bottom_sheet"]
        bs_node = bs_fn(StarInteger(1))
        self.assertEqual(bs_node.tag, "bottom_sheet")
        self.assertTrue(bs_node.props["open"])


class TestDesktopRuntimeAndWindowRendering(unittest.TestCase):
    def test_headless_desktop_render_with_motion_and_widgets(self):
        window = DesktopWindow(title="Test Animated Window", width=800, height=600, headless=True)
        runtime = DesktopRuntime(window=window, headless=True)

        tree = StarVirtualNode("column", children=[
            StarVirtualNode("title", {"content": "Motion Demo", "level": 1}),
            make_shimmer(width=300, height=24),
            make_skeleton(width=200, height=20),
            make_pulse(child=StarVirtualNode("button", {"label": "Pulsing Button"})),
            make_glow("#00f0ff", 20, child=StarVirtualNode("card", children=[
                StarVirtualNode("text", {"content": "Glowing Card"})
            ])),
            StarVirtualNode("segmented_control", {"items": ["Tab 1", "Tab 2", "Tab 3"], "selected": 0}),
            StarVirtualNode("stepper", {"steps": ["Step 1", "Step 2"], "current": 0}),
            StarVirtualNode("rating", {"value": 4.5, "max": 5}),
            StarVirtualNode("code_block", {"code": "print('hello')", "language": "star"}),
            StarVirtualNode("table", {
                "headers": ["Col 1", "Col 2"],
                "rows": [["Val A", "Val B"]]
            }),
            StarVirtualNode("marquee", {"text": "Breaking News"}),
            StarVirtualNode("confetti", {"count": 25})
        ])

        runtime.mount(tree)
        self.assertTrue(len(window.draw_commands) > 10)

        # Trigger animation tick
        runtime._on_anim_tick(0.016)
        self.assertTrue(runtime.anim_phase > 0.0)


if __name__ == "__main__":
    unittest.main()
