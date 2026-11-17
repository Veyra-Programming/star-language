"""
Star Language Formatter Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.formatter import StarFormatter


class TestFormatter(unittest.TestCase):
    def test_formatter_indentation(self):
        unformatted = "app Test\nvariable x=10\nif x>5\nshow x\nend\nend"
        formatter = StarFormatter(indent_spaces=4)
        formatted = formatter.format_code(unformatted)
        expected = "app Test\n    variable x = 10\n    if x > 5\n        show x\n    end\nend\n"
        self.assertEqual(formatted, expected)

    def test_class_formatting(self):
        unformatted = "class User\nproperty name\nproperty age:Integer=20\nfunction greet()\nreturn self.name\nend\nend"
        formatter = StarFormatter(indent_spaces=4)
        formatted = formatter.format_code(unformatted)
        self.assertIn("    property name", formatted)
        self.assertIn("    property age: Integer = 20", formatted)
        self.assertIn("    function greet()", formatted)
        self.assertIn("        return self.name", formatted)


if __name__ == "__main__":
    unittest.main()
