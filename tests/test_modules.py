"""
Star Language Modules Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter


class TestModules(unittest.TestCase):
    def _run(self, code: str):
        output = []
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        program = parser.parse()
        interp = Interpreter(source_code=code, output_handler=lambda s: output.append(s))
        interp.interpret(program)
        return output

    def test_math_module(self):
        code = """
        use Math
        show Math.sqrt(100)
        show Math.pow(3, 3)
        show Math.floor(4.9)
        show Math.ceil(4.1)
        """
        out = self._run(code)
        self.assertIn(out, [["10", "27", "4", "5"], ["10.0", "27", "4", "5"]])

    def test_string_module(self):
        code = """
        use String
        show String.trim("  hello  ")
        show String.uppercase("star")
        show String.contains("abcdef", "cd")
        """
        out = self._run(code)
        self.assertEqual(out, ["hello", "STAR", "true"])


if __name__ == "__main__":
    unittest.main()
