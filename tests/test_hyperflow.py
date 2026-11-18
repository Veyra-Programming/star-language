"""
Unit Tests for Star HyperFlow Engine, ChronoState, Reactive Mesh & Actor Mesh
Authoritative Reference: STAR_SERVER_SPEC.md
"""

import unittest
import time
import json
from star_engine.hyperflow.router import HyperRouter
from star_engine.hyperflow.chrono import ChronoStore
from star_engine.hyperflow.reactive_mesh import ReactiveStore, ReactivePatch
from star_engine.hyperflow.actor import ActorMesh
from star_engine.hyperflow.server import ServerApp, Request, Response
from star_sdk.server import create_server_module
from star_engine.interpreter import Interpreter
from star_engine.lexer import Lexer
from star_engine.parser import Parser


class TestHyperRouter(unittest.TestCase):
    def setUp(self):
        self.router = HyperRouter()

    def test_exact_route(self):
        self.router.add_route("GET", "/api/v1/health", "health_handler")
        match = self.router.match("GET", "/api/v1/health")
        self.assertIsNotNone(match)
        self.assertEqual(match.handler, "health_handler")
        self.assertEqual(match.params, {})

    def test_parameter_extraction(self):
        self.router.add_route("GET", "/users/:id/profile", "profile_handler")
        match = self.router.match("GET", "/users/alex123/profile")
        self.assertIsNotNone(match)
        self.assertEqual(match.handler, "profile_handler")
        self.assertEqual(match.params.get("id"), "alex123")

    def test_wildcard_route(self):
        self.router.add_route("GET", "/static/*filepath", "static_handler")
        match = self.router.match("GET", "/static/css/theme/dark.css")
        self.assertIsNotNone(match)
        self.assertEqual(match.handler, "static_handler")
        self.assertEqual(match.params.get("filepath"), "css/theme/dark.css")

    def test_route_not_found(self):
        self.router.add_route("GET", "/ping", "ping_handler")
        match = self.router.match("POST", "/ping")
        self.assertIsNone(match)
        match2 = self.router.match("GET", "/unknown")
        self.assertIsNone(match2)


class TestChronoState(unittest.TestCase):
    def setUp(self):
        self.store = ChronoStore("test_bank", {"balance": 1000, "status": "active"})

    def test_state_mutation_and_ticks(self):
        self.assertEqual(self.store.get("balance"), 1000)
        self.store.set("balance", 1200)
        self.assertEqual(self.store.get("balance"), 1200)
        self.assertGreater(self.store.current_tick, 0)

    def test_checkpoint_and_rewind(self):
        self.store.set("balance", 500)
        cp = self.store.checkpoint("savepoint_1")
        self.store.set("balance", 100)
        self.assertEqual(self.store.get("balance"), 100)

        # Rewind back to savepoint
        ok = self.store.rewind(cp)
        self.assertTrue(ok)
        self.assertEqual(self.store.get("balance"), 500)

    def test_diff_and_history(self):
        cp1 = self.store.checkpoint("cp1")
        self.store.set("balance", 2000)
        self.store.set("new_field", "created")
        cp2 = self.store.checkpoint("cp2")

        diff = self.store.diff("cp1", "cp2")
        self.assertIn("balance", diff["changed"])
        self.assertIn("new_field", diff["added"])
        self.assertGreater(len(self.store.history()), 0)

    def test_atomic_run_rollback_on_error(self):
        def _failing_op():
            self.store.set("balance", 0)
            raise ValueError("Simulated network timeout")

        with self.assertRaises(ValueError):
            self.store.atomic_run(_failing_op)

        # Balance was restored because of atomic rollback!
        self.assertEqual(self.store.get("balance"), 1000)


class TestReactiveMesh(unittest.TestCase):
    def test_delta_patch_notification(self):
        store = ReactiveStore("telemetry", {"active": 1})
        patches_received = []

        store.subscribe(lambda patch, state: patches_received.append(patch))
        store.set("active", 10)
        store.push("users", "alex")

        self.assertEqual(len(patches_received), 2)
        self.assertEqual(patches_received[0].op, "replace")
        self.assertEqual(patches_received[0].path, "/active")
        self.assertEqual(patches_received[1].op, "add")
        self.assertEqual(patches_received[1].path, "/users/0")

    def test_sse_frame_generation(self):
        patch = ReactivePatch(op="replace", path="/temperature", value=24.5)
        sse_text = patch.to_sse_frame("sensor")
        self.assertTrue(sse_text.startswith("event: sensor\n"))
        self.assertIn('"value": 24.5', sse_text)


class TestActorMesh(unittest.TestCase):
    def test_actor_spawn_send_and_ask(self):
        mesh = ActorMesh()
        actor = mesh.spawn("calculator", lambda msg: msg.get("a", 0) + msg.get("b", 0))

        # Test request-reply ask
        result = actor.ask({"a": 15, "b": 27}, timeout=2.0)
        self.assertEqual(result, 42)
        self.assertEqual(actor.processed_count, 1)

        # Test fire-and-forget send
        actor.send({"a": 1, "b": 2})
        time.sleep(0.1)
        self.assertEqual(actor.processed_count, 2)
        mesh.stop_all()


class TestServerModuleIntegration(unittest.TestCase):
    def test_jwt_sign_and_verify(self):
        mod = create_server_module()
        jwt_sign = mod.get("jwt_sign")
        jwt_verify = mod.get("jwt_verify")

        from star_engine.types import StarMap, StarText
        payload = StarMap({"sub": StarText("12345"), "name": StarText("Alice")})
        secret = StarText("super-star-secret")

        token = jwt_sign.fn(payload, secret)
        self.assertTrue(token.to_string().count(".") == 2)

        verified = jwt_verify.fn(token, secret)
        self.assertIsNotNone(verified)
        self.assertEqual(verified.get("name").to_string(), "Alice")

    def test_password_hash_and_verify(self):
        mod = create_server_module()
        h_fn = mod.get("hash_password")
        v_fn = mod.get("verify_password")

        from star_engine.types import StarText
        pwd = StarText("SecurePassword2026!")
        hashed = h_fn.fn(pwd)

        is_valid = v_fn.fn(pwd, hashed)
        self.assertTrue(is_valid.value)

        wrong_pwd = StarText("WrongPassword")
        is_invalid = v_fn.fn(wrong_pwd, hashed)
        self.assertFalse(is_invalid.value)

    def test_star_script_methods(self):
        source = """use Server
constant txt = "  hello world  "
constant clean = txt.trim().uppercase()
constant list_data = [1, 2, 3]
list_data.push(4)
constant reversed_list = list_data.reverse()
constant map_data = {"a": 1, "b": 2}
constant map_keys = map_data.keys()
"""
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), source_code=source)
        prog = parser.parse()
        interp = Interpreter(source_code=source)
        interp.interpret(prog)

        clean_val = interp.global_env.lookup("clean")
        self.assertEqual(clean_val.to_string(), "HELLO WORLD")

        list_val = interp.global_env.lookup("list_data")
        self.assertEqual(len(list_val.elements), 4)

        keys_val = interp.global_env.lookup("map_keys")
        self.assertEqual(len(keys_val.elements), 2)


if __name__ == "__main__":
    unittest.main()
