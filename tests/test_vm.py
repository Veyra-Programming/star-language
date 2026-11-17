"""
Star Bytecode Virtual Machine (StarVM) Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.compiler import StarCompiler
from star_engine.vm import StarVM


class TestVM(unittest.TestCase):
    def _run_vm(self, code: str):
        output = []
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        prog = parser.parse()
        compiler = StarCompiler(source_code=code)
        mod = compiler.compile(prog)
        vm = StarVM(mod, output_handler=lambda s: output.append(s))
        vm.run()
        return output

    def test_vm_basic_arithmetic(self):
        code = "show (10 + 20) * 3 - 10 / 2"
        out = self._run_vm(code)
        self.assertEqual(out, ["85"])

    def test_vm_control_flow(self):
        code = """
        variable x = 15
        if x > 20
            show "big"
        else if x > 10
            show "medium"
        else
            show "small"
        end
        """
        out = self._run_vm(code)
        self.assertEqual(out, ["medium"])

    def test_vm_loops(self):
        code = """
        variable count = 0
        repeat 3
            count = count + 1
        end
        show count
        """
        out = self._run_vm(code)
        self.assertEqual(out, ["3"])

    def test_vm_classes_and_methods(self):
        code = """
        class Point
            property x = 0
            property y = 0

            function move(dx, dy)
                self.x = self.x + dx
                self.y = self.y + dy
            end

            function pos()
                return "(" + self.x + ", " + self.y + ")"
            end
        end

        variable p = Point(x = 10, y = 20)
        p.move(5, -5)
        show p.pos()
        """
        out = self._run_vm(code)
        self.assertEqual(out, ["(15, 15)"])

    def test_vm_modules(self):
        code = """
        use Math
        show Math.sqrt(64)
        """
        out = self._run_vm(code)
        self.assertEqual(out, ["8.0"])


if __name__ == "__main__":
    unittest.main()
