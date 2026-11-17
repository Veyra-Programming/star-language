"""
Star Language Conformance Test Runner
Verifies that Star sample programs and conformance suites execute with 100%
identical behavior across BOTH the Reference Interpreter and the StarVM Bytecode Engine!
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter
from star_engine.compiler import StarCompiler
from star_engine.vm import StarVM


class TestDualEngineConformance(unittest.TestCase):
    def _run_dual(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        lexer = Lexer(source, filename=path)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename=path)
        prog = parser.parse()

        # 1. Reference Interpreter
        ref_output = []
        interp = Interpreter(source_code=source, filename=path, output_handler=lambda s: ref_output.append(s))
        interp.interpret(prog)

        # 2. Star IR Compiler + StarVM
        vm_output = []
        compiler = StarCompiler(filename=path, source_code=source)
        ir_mod = compiler.compile(prog)
        vm = StarVM(ir_mod, output_handler=lambda s: vm_output.append(s))
        vm.run()

        # Assert parity between Reference Engine and Bytecode Engine
        self.assertEqual(
            ref_output,
            vm_output,
            f"Parity failure for '{path}':\nReference: {ref_output}\nStarVM: {vm_output}"
        )
        return vm_output

    def test_example_hello(self):
        out = self._run_dual("examples/hello.star")
        self.assertEqual(out, ["Hello, World!"])

    def test_example_counter(self):
        out = self._run_dual("examples/counter.star")
        self.assertEqual(out[-1], "Final count: 5")

    def test_example_fibonacci(self):
        out = self._run_dual("examples/fibonacci.star")
        self.assertIn("fib(6) = 8", out)
        self.assertIn("fib(10) = 55", out)

    def test_example_functions(self):
        out = self._run_dual("examples/functions.star")
        self.assertEqual(out[0], "Greetings, Commander Alex!")
        self.assertEqual(out[1], "Double 15 = 30")
        self.assertEqual(out[2], "Triple 15 = 45")

    def test_example_collections(self):
        out = self._run_dual("examples/collections.star")
        self.assertIn("First fruit: Apple", out)
        self.assertIn("User: stargazer", out)

    def test_example_classes(self):
        out = self._run_dual("examples/classes.star")
        self.assertIn("Account [Alex Star]: $100.0", out[0])
        self.assertIn("Account [Alex Star]: $120.0", out[-1])

    def test_example_modules_demo(self):
        out = self._run_dual("examples/modules_demo.star")
        self.assertIn("sqrt(144) = 12.0", out)
        self.assertIn("Trimmed: 'star language'", out)
        self.assertIn("Total: $138.0", out)

    def test_conformance_basic_variable(self):
        out = self._run_dual("conformance/variables/basic_variable.star")
        self.assertEqual(out, ["30", "100"])

    def test_conformance_for_loop(self):
        out = self._run_dual("conformance/control_flow/for_loop.star")
        self.assertEqual(out, ["10"])

    def test_conformance_class_basic(self):
        out = self._run_dual("conformance/classes/class_basic.star")
        self.assertEqual(out, ["Hello, World!", "Hello, Star!"])

    def test_conformance_class_state(self):
        out = self._run_dual("conformance/classes/class_state.star")
        self.assertEqual(out, ["3"])

    def test_conformance_use_math(self):
        out = self._run_dual("conformance/modules/use_math.star")
        self.assertEqual(out, ["5.0", "16", "10", "20"])

    def test_conformance_ffi_basic(self):
        out = self._run_dual("conformance/ffi/ffi_basic.star")
        self.assertEqual(out, ["FFI initialized successfully"])

    def test_conformance_desktop_counter(self):
        from star_backend.desktop.builder import DesktopBuilder
        db = DesktopBuilder()
        res = db.run("examples/desktop_counter.star", headless=True)
        self.assertEqual(res, 0)

    def test_conformance_desktop_todo(self):
        from star_backend.desktop.builder import DesktopBuilder
        db = DesktopBuilder()
        res = db.run("examples/desktop_todo.star", headless=True)
        self.assertEqual(res, 0)


if __name__ == "__main__":
    unittest.main()
