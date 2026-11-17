"""
Star Language Parser Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.tokens import TokenType
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.ast_nodes import (
    ProgramNode, AppNode, FunctionDefNode, VarDeclNode,
    ConstDeclNode, IfNode, RepeatNode, WhileNode, ForNode,
    BinaryOpNode, LiteralNode, IdentifierNode
)
from star_engine.errors import StarSyntaxError


class TestParser(unittest.TestCase):
    def _parse(self, code: str) -> ProgramNode:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        return parser.parse()

    def test_var_and_const_decls(self):
        code = "variable a = 10\nconstant B = 20"
        prog = self._parse(code)
        self.assertEqual(len(prog.statements), 2)
        self.assertIsInstance(prog.statements[0], VarDeclNode)
        self.assertEqual(prog.statements[0].name, "a")
        self.assertIsInstance(prog.statements[1], ConstDeclNode)
        self.assertEqual(prog.statements[1].name, "B")

    def test_function_decl(self):
        code = "function add(x, y)\nreturn x + y\nend"
        prog = self._parse(code)
        self.assertEqual(len(prog.statements), 1)
        fn = prog.statements[0]
        self.assertIsInstance(fn, FunctionDefNode)
        self.assertEqual(fn.name, "add")
        self.assertEqual(fn.parameters, ["x", "y"])
        self.assertEqual(len(fn.body), 1)

    def test_expression_precedence(self):
        code = "variable x = 2 + 3 * 4"
        prog = self._parse(code)
        decl = prog.statements[0]
        self.assertIsInstance(decl.initializer, BinaryOpNode)
        # Should be +(2, *(3, 4))
        self.assertEqual(decl.initializer.operator, TokenType.PLUS)
        self.assertEqual(decl.initializer.right.operator, TokenType.STAR)

    def test_control_flow(self):
        code = """
        if x > 0
            show "positive"
        else if x == 0
            show "zero"
        else
            show "negative"
        end
        """
        prog = self._parse(code)
        self.assertEqual(len(prog.statements), 1)
        if_node = prog.statements[0]
        self.assertIsInstance(if_node, IfNode)
        self.assertEqual(len(if_node.elif_branches), 1)
        self.assertIsNotNone(if_node.else_body)

    def test_loops(self):
        code = """
        repeat 5
            show "hi"
        end
        while true
            break
        end
        for item in items
            continue
        end
        """
        prog = self._parse(code)
        self.assertEqual(len(prog.statements), 3)
        self.assertIsInstance(prog.statements[0], RepeatNode)
        self.assertIsInstance(prog.statements[1], WhileNode)
        self.assertIsInstance(prog.statements[2], ForNode)

    def test_missing_end_error(self):
        code = "function broken()\nshow 1"
        with self.assertRaises(StarSyntaxError):
            self._parse(code)


if __name__ == "__main__":
    unittest.main()
