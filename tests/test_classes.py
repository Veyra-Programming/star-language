"""
Star Language Classes & OOP Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter
from star_engine.errors import StarNameError, StarTypeError


class TestClasses(unittest.TestCase):
    def _run(self, code: str):
        output = []
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        program = parser.parse()
        interp = Interpreter(source_code=code, output_handler=lambda s: output.append(s))
        interp.interpret(program)
        return output

    def test_class_instantiation_and_methods(self):
        code = """
        class Person
            property name
            property age = 0

            function greet()
                return "Hi, I am " + self.name + " (" + self.age + ")"
            end
        end

        variable p1 = Person(name = "Alex", age = 25)
        show p1.greet()
        """
        out = self._run(code)
        self.assertEqual(out, ["Hi, I am Alex (25)"])

    def test_class_property_mutation(self):
        code = """
        class Box
            property width = 10
            property height = 20

            function area()
                return self.width * self.height
            end
        end

        variable b = Box()
        show b.area()
        b.width = 15
        show b.area()
        """
        out = self._run(code)
        self.assertEqual(out, ["200", "300"])

    def test_invalid_property_access_raises_error(self):
        code = """
        class Car
            property model
        end

        variable c = Car(model = "Star Sedan")
        show c.unknownField
        """
        with self.assertRaises(StarNameError):
            self._run(code)

    def test_invalid_property_assignment_raises_error(self):
        code = """
        class Car
            property model
        end

        variable c = Car(model = "Star Sedan")
        c.nonExistent = 10
        """
        with self.assertRaises(StarNameError):
            self._run(code)


if __name__ == "__main__":
    unittest.main()
