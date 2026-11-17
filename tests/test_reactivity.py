"""
Unit Tests for Star 0.6 Reactive State System
Authoritative Reference: STAR_COMPONENTS.md
"""

import unittest
from star_engine.types import StarReactiveState, StarInteger, StarComponent, StarComponentInstance, StarVirtualNode


class TestReactivity(unittest.TestCase):
    def test_reactive_state_listener(self):
        state = StarReactiveState("count", StarInteger(0))
        history = []

        def _on_change(new_val, old_val):
            history.append((new_val.value, old_val.value))

        state.listeners.append(_on_change)
        state.set_value(StarInteger(1))
        state.set_value(StarInteger(2))

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], (1, 0))
        self.assertEqual(history[1], (2, 1))

    def test_component_state_mutation_triggers_reconciliation(self):
        comp = StarComponent(
            name="Counter",
            state_decls=[],
            computed_decls=[],
            watch_decls=[],
            event_decls=[],
            methods={},
            render_decl=None,
            closure_env=None
        )
        instance = StarComponentInstance(comp)
        instance.set_state("count", StarInteger(0))

        reconciled = []

        def _on_reconcile(inst, old_vdom):
            reconciled.append(inst.get_state("count").value)

        instance.on_reconcile = _on_reconcile
        instance.set_state("count", StarInteger(5))
        instance.set_state("count", StarInteger(10))

        self.assertEqual(len(reconciled), 2)
        self.assertEqual(reconciled, [5, 10])


if __name__ == "__main__":
    unittest.main()
