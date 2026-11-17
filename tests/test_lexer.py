"""
Star Language Lexer Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.tokens import TokenType
from star_engine.lexer import Lexer
from star_engine.errors import StarSyntaxError


class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        source = 'variable x = 42\nconstant PI = 3.14\nshow "Hello"'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertEqual(
            types,
            [
                TokenType.VARIABLE, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.INTEGER, TokenType.NEWLINE,
                TokenType.CONSTANT, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.DECIMAL, TokenType.NEWLINE,
                TokenType.SHOW, TokenType.TEXT, TokenType.EOF
            ]
        )

    def test_operators(self):
        source = "+ - * / % == != < <= > >= and or not ="
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertEqual(
            types,
            [
                TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
                TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL,
                TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.AND, TokenType.OR, TokenType.NOT,
                TokenType.EQUAL, TokenType.EOF
            ]
        )

    def test_keywords_and_blocks(self):
        source = "app MyApp\nfunction test(a, b)\nif true\nelse if false\nelse\nend\nrepeat 3\nwhile x\nfor i in list\nbreak\ncontinue\nreturn\ntry\ncatch err\nend"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        kw_types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF, TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.RPAREN, TokenType.COMMA, TokenType.INTEGER)]
        self.assertIn(TokenType.APP, kw_types)
        self.assertIn(TokenType.FUNCTION, kw_types)
        self.assertIn(TokenType.IF, kw_types)
        self.assertIn(TokenType.REPEAT, kw_types)
        self.assertIn(TokenType.FOR, kw_types)
        self.assertIn(TokenType.BREAK, kw_types)
        self.assertIn(TokenType.CONTINUE, kw_types)
        self.assertIn(TokenType.TRY, kw_types)
        self.assertIn(TokenType.CATCH, kw_types)

    def test_string_escapes(self):
        source = r'"Line 1\nLine 2\t\"Quotes\""'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.TEXT)
        self.assertEqual(tokens[0].value, 'Line 1\nLine 2\t"Quotes"')

    def test_unterminated_string_error(self):
        source = '"unterminated string'
        lexer = Lexer(source)
        with self.assertRaises(StarSyntaxError):
            lexer.tokenize()


if __name__ == "__main__":
    unittest.main()
