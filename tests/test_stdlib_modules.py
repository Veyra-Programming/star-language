"""
Star Language 200+ Standard Library Modules Unit Tests
Tests module resolution, parsing, class instantiation, method calls,
and function exports across all 18 domains in modules/ and lib/.
"""

import os
import glob
import json
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter
from star_engine.types import StarModule, StarInstance, StarInteger, StarDecimal, StarText


class TestStdlibModules(unittest.TestCase):
    def _run(self, code: str):
        output = []
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        program = parser.parse()
        interp = Interpreter(source_code=code, output_handler=lambda s: output.append(s))
        interp.interpret(program)
        return output

    def test_module_count(self):
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        mod_files = glob.glob(os.path.join(repo_root, "modules", "*", "*.star"))
        # Exclude index.star
        mod_files = [f for f in mod_files if not os.path.basename(f) == "index.star"]
        self.assertGreaterEqual(len(mod_files), 200, f"Expected at least 200 modules, found {len(mod_files)}")
        self.assertGreaterEqual(len(mod_files), 235)

        lib_files = glob.glob(os.path.join(repo_root, "lib", "*", "*.star"))
        lib_files = [f for f in lib_files if not os.path.basename(f) == "index.star"]
        self.assertEqual(len(mod_files), len(lib_files))

    def test_import_short_name(self):
        code = """
        use "vector2d"
        variable v = vector2d.create(3.0, 4.0)
        show v.magnitude()
        """
        out = self._run(code)
        self.assertEqual(out, ["5.0"])

    def test_import_category_path(self):
        code = """
        use "math/vector2d"
        variable v1 = vector2d.create(10.0, 20.0)
        variable v2 = vector2d.create(5.0, 5.0)
        variable v3 = vector2d.add(v1, v2)
        show v3.x
        show v3.y
        """
        out = self._run(code)
        self.assertEqual(out, ["15.0", "25.0"])

    def test_import_full_modules_file_path(self):
        code = """
        use "modules/math/vector2d.star"
        variable v = vector2d.create(6.0, 8.0)
        show v.magnitude()
        """
        out = self._run(code)
        self.assertEqual(out, ["10.0"])

    def test_import_full_lib_file_path(self):
        code = """
        use "lib/math/vector2d.star"
        variable v = vector2d.create(9.0, 12.0)
        show v.magnitude()
        """
        out = self._run(code)
        self.assertEqual(out, ["15.0"])

    def test_import_identifier_syntax(self):
        code = """
        use vector2d
        variable v = vector2d.create(1.0, 1.0)
        show vector2d.scale(v, 3.0).x
        """
        out = self._run(code)
        self.assertEqual(out, ["3.0"])

    def test_math_modules(self):
        code = """
        use "matrix"
        use "complex"
        use "geometry"

        variable m = matrix.create(1.0, 2.0, 3.0, 4.0)
        show m.determinant()

        variable c1 = complex.create(2.0, 3.0)
        variable c2 = complex.create(1.0, 4.0)
        variable c3 = complex.add(c1, c2)
        show c3.real
        show c3.imag

        variable r = geometry.Rectangle(width = 5.0, height = 10.0)
        show r.area()
        show r.perimeter()
        """
        out = self._run(code)
        self.assertEqual(out, ["-2.0", "3.0", "7.0", "50.0", "30.0"])

    def test_collections_modules(self):
        code = """
        use "stack"
        use "queue"
        use "circular_buffer"

        variable s = stack.create()
        s.push("alpha")
        s.push("beta")
        show s.size()
        show s.peek()

        variable q = queue.create()
        q.enqueue(100)
        q.enqueue(200)
        show q.size()
        show q.peek()

        variable cb = circular_buffer.create(5)
        show cb.is_empty()
        show cb.capacity
        """
        out = self._run(code)
        self.assertEqual(out, ["2", "beta", "2", "100", "true", "5"])

    def test_ui_and_mobile_modules(self):
        code = """
        use "box_model"
        use "haptic"
        use "battery"

        variable bm = box_model.create()
        show bm.info()

        variable h = haptic.create()
        show h.get_version()

        variable b = battery.create()
        show battery.describe()
        """
        out = self._run(code)
        self.assertEqual(out[0], "box_model v1.0.0")
        self.assertEqual(out[1], "1.0.0")
        self.assertIn("Battery", out[2])

    def test_crypto_and_net_modules(self):
        code = """
        use "uuid"
        use "url"
        use "sha256_lite"

        variable u = uuid.create()
        show u.info()

        variable net_url = url.create()
        show net_url.get_version()

        show sha256_lite.describe()
        """
        out = self._run(code)
        self.assertEqual(out[0], "uuid v1.0.0")
        self.assertEqual(out[1], "1.0.0")
        self.assertIn("SHA-256", out[2])

    def test_ai_game_and_storage_modules(self):
        code = """
        use "neural_net_lite"
        use "game_loop"
        use "key_value_store"

        variable nn = neural_net_lite.create()
        show nn.info()

        variable gl = game_loop.create()
        show gl.get_version()

        variable kv = key_value_store.create()
        show key_value_store.describe()
        """
        out = self._run(code)
        self.assertEqual(out[0], "neural_net_lite v1.0.0")
        self.assertEqual(out[1], "1.0.0")
        self.assertIn("Key-value", out[2])

    def test_all_modules_syntax_valid(self):
        """Validates that every single one of the 235 modules parses cleanly into an AST without any errors."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        mod_files = glob.glob(os.path.join(repo_root, "modules", "*", "*.star"))
        for file_path in mod_files:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            tokens = Lexer(source, filename=file_path).tokenize()
            program = Parser(tokens, source_code=source, filename=file_path).parse()
            self.assertIsNotNone(program)
            self.assertGreater(len(program.statements), 0, f"Module {file_path} had 0 statements.")


    def test_mobile_hardware_module(self):
        code = """
        use "hardware"
        variable info = hardware.get_device_info()
        show info.model
        show info.os
        variable batt = hardware.get_battery()
        show batt.level
        show hardware.vibrate("click")
        """
        out = self._run(code)
        self.assertEqual(len(out), 4)
        self.assertEqual(out[0], "iQOO Z10 Lite 5G")
        self.assertEqual(out[1], "OriginOS 6")
        self.assertEqual(out[2], "100")
        self.assertEqual(out[3], "true")


if __name__ == "__main__":
    unittest.main()

