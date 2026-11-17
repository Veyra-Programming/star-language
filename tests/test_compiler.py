"""
Star Language Compiler & Bytecode Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.compiler import StarCompiler
from star_engine.ir import OpCode


class TestCompiler(unittest.TestCase):
    def _compile(self, code: str):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        prog = parser.parse()
        compiler = StarCompiler(source_code=code)
        return compiler.compile(prog), compiler

    def test_compile_arithmetic(self):
        code = "variable x = 10 + 20 * 2"
        mod, _ = self._compile(code)
        opcodes = [inst.opcode for inst in mod.instructions]
        self.assertIn(OpCode.CONST, opcodes)
        self.assertIn(OpCode.ADD, opcodes)
        self.assertIn(OpCode.MUL, opcodes)
        self.assertIn(OpCode.DEFINE_VAR, opcodes)

    def test_compile_function_and_class(self):
        code = """
        class User
            property name
            function greet()
                return "Hi " + self.name
            end
        end
        """
        mod, _ = self._compile(code)
        self.assertIn("User", mod.classes)
        self.assertIn("greet", mod.classes["User"].methods)

    def test_bytecode_serialization_roundtrip(self):
        code = """
        function add(a, b)
            return a + b
        end
        show add(15, 25)
        """
        mod, compiler = self._compile(code)
        blob = compiler.serialize_bytecode()
        self.assertTrue(blob.startswith(b"STAR"))

        deserialized = StarCompiler.deserialize_bytecode(blob)
        self.assertEqual(len(deserialized.constants), len(mod.constants))
        self.assertIn("add", deserialized.functions)
        self.assertEqual(len(deserialized.instructions), len(mod.instructions))


if __name__ == "__main__":
    unittest.main()
