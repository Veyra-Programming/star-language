"""
Star Language Interpreter Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter
from star_engine.errors import StarNameError, StarRuntimeError, StarTypeError


class TestInterpreter(unittest.TestCase):
    def _run(self, code: str):
        output = []
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        program = parser.parse()
        interp = Interpreter(source_code=code, output_handler=lambda s: output.append(s))
        interp.interpret(program)
        return output

    def test_basic_arithmetic_and_show(self):
        code = "show 10 + 20 * 2"
        out = self._run(code)
        self.assertEqual(out, ["50"])

    def test_variables_and_reassignment(self):
        code = """
        variable x = 5
        x = x + 10
        show x
        """
        out = self._run(code)
        self.assertEqual(out, ["15"])

    def test_constant_immutability(self):
        code = """
        constant MAX = 100
        MAX = 200
        """
        with self.assertRaises(StarNameError):
            self._run(code)

    def test_lexical_scoping(self):
        code = """
        variable x = "outer"
        if true
            variable x = "inner"
            show x
        end
        show x
        """
        out = self._run(code)
        self.assertEqual(out, ["inner", "outer"])

    def test_functions_and_recursion(self):
        code = """
        function fact(n)
            if n <= 1
                return 1
            end
            return n * fact(n - 1)
        end
        show fact(5)
        """
        out = self._run(code)
        self.assertEqual(out, ["120"])

    def test_closures(self):
        code = """
        function makeCounter()
            variable count = 0
            function inc()
                count = count + 1
                return count
            end
            return inc
        end

        variable c = makeCounter()
        show c()
        show c()
        show c()
        """
        out = self._run(code)
        self.assertEqual(out, ["1", "2", "3"])

    def test_repeat_loop(self):
        code = """
        variable count = 0
        repeat 4
            count = count + 1
        end
        show count
        """
        out = self._run(code)
        self.assertEqual(out, ["4"])

    def test_for_in_loop(self):
        code = """
        variable sum = 0
        for n in [10, 20, 30]
            sum = sum + n
        end
        show sum
        """
        out = self._run(code)
        self.assertEqual(out, ["60"])

    def test_break_and_continue(self):
        code = """
        variable count = 0
        while count < 10
            count = count + 1
            if count == 2
                continue
            end
            if count == 4
                break
            end
            show count
        end
        """
        out = self._run(code)
        self.assertEqual(out, ["1", "3"])

    def test_collections_and_indexing(self):
        code = """
        variable list = [10, 20, 30]
        list[1] = 99
        show list[1]
        show len(list)

        variable map = {"key": "val"}
        map["key"] = "new_val"
        show map["key"]
        """
        out = self._run(code)
        self.assertEqual(out, ["99", "3", "new_val"])

    def test_try_catch(self):
        code = """
        try
            variable err = 10 / 0
        catch e
            show "Caught error!"
        end
        """
        out = self._run(code)
        self.assertEqual(out, ["Caught error!"])


if __name__ == "__main__":
    unittest.main()
