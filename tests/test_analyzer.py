"""
Star Language Semantic Analyzer & Linter Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.analyzer import SemanticAnalyzer


class TestAnalyzer(unittest.TestCase):
    def _analyze(self, code: str):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        program = parser.parse()
        analyzer = SemanticAnalyzer(source_code=code)
        return analyzer.analyze(program)

    def test_unreachable_code_warning(self):
        code = """
        function test()
            return 42
            show "Unreachable"
        end
        """
        errors, warnings = self._analyze(code)
        self.assertEqual(len(errors), 0)
        self.assertTrue(any("Unreachable" in w.message for w in warnings))

    def test_unused_variable_warning(self):
        code = """
        variable unusedVar = 100
        show "done"
        """
        errors, warnings = self._analyze(code)
        self.assertEqual(len(errors), 0)
        self.assertTrue(any("unusedVar" in w.message for w in warnings))

    def test_break_outside_loop_error(self):
        code = """
        show "hello"
        break
        """
        errors, warnings = self._analyze(code)
        self.assertTrue(len(errors) > 0)
        self.assertIn("break", errors[0].message)

    def test_type_annotation_mismatch_error(self):
        code = """
        variable age: Integer = "twenty"
        """
        errors, warnings = self._analyze(code)
        self.assertTrue(len(errors) > 0)
        self.assertIn("type", errors[0].message.lower())


if __name__ == "__main__":
    unittest.main()
