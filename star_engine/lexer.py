"""
Star Language Lexer / Scanner
Authoritative Reference: STAR_SPEC.md (Section 3)
"""

from typing import List, Optional
from star_engine.tokens import TokenType, Token, SourceLocation, KEYWORDS
from star_engine.errors import StarSyntaxError


class Lexer:
    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source = source
        self.filename = filename
        self.length = len(source)
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.token_start_col = 1
        self.tokens: List[Token] = []
        self.paren_depth = 0

    def tokenize(self) -> List[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.token_start_col = self.column
            self._scan_token()

        # Append final EOF token
        loc = SourceLocation(
            file=self.filename,
            line=self.line,
            column=self.column,
            length=1
        )
        self.tokens.append(Token(TokenType.EOF, "", None, loc))
        return self.tokens

    def _is_at_end(self) -> bool:
        return self.current >= self.length

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= self.length:
            return "\0"
        return self.source[self.current + 1]

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _add_token(self, token_type: TokenType, value: any = None):
        lexeme = self.source[self.start:self.current]
        loc = SourceLocation(
            file=self.filename,
            line=self.line,
            column=self.token_start_col,
            length=max(1, len(lexeme))
        )
        self.tokens.append(Token(token_type, lexeme, value, loc))

    def _scan_token(self):
        c = self._advance()

        # Whitespace
        if c in (" ", "\t", "\r"):
            return

        # Newline
        if c == "\n":
            self.line += 1
            self.column = 1
            # If we are inside parentheses/brackets, suppress newline tokens
            if self.paren_depth == 0:
                # Suppress consecutive newline tokens
                if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
                    self._add_token(TokenType.NEWLINE, "\n")
            return

        # Comments (# or //)
        if c == "#" or (c == "/" and self._peek() == "/"):
            while self._peek() != "\n" and not self._is_at_end():
                self._advance()
            return

        # Punctuation & Delimiters
        if c == "(":
            self.paren_depth += 1
            self._add_token(TokenType.LPAREN)
        elif c == ")":
            if self.paren_depth > 0:
                self.paren_depth -= 1
            self._add_token(TokenType.RPAREN)
        elif c == "[":
            self.paren_depth += 1
            self._add_token(TokenType.LBRACKET)
        elif c == "]":
            if self.paren_depth > 0:
                self.paren_depth -= 1
            self._add_token(TokenType.RBRACKET)
        elif c == "{":
            self.paren_depth += 1
            self._add_token(TokenType.LBRACE)
        elif c == "}":
            if self.paren_depth > 0:
                self.paren_depth -= 1
            self._add_token(TokenType.RBRACE)
        elif c == ",":
            self._add_token(TokenType.COMMA)
        elif c == ":":
            self._add_token(TokenType.COLON)
        elif c == ";":
            self._add_token(TokenType.SEMICOLON)
        elif c == ".":
            self._add_token(TokenType.DOT)

        # Arithmetic Operators
        elif c == "+":
            self._add_token(TokenType.PLUS)
        elif c == "-":
            self._add_token(TokenType.MINUS)
        elif c == "*":
            self._add_token(TokenType.STAR)
        elif c == "/":
            self._add_token(TokenType.SLASH)
        elif c == "%":
            self._add_token(TokenType.PERCENT)
        elif c == "|":
            if self._match(">"):
                self._add_token(TokenType.PIPE_GREATER)
            else:
                self._add_token(TokenType.OR)

        # Comparison & Assignment
        elif c == "=":
            if self._match("="):
                self._add_token(TokenType.EQUAL_EQUAL)
            else:
                self._add_token(TokenType.EQUAL)
        elif c == "!":
            if self._match("="):
                self._add_token(TokenType.BANG_EQUAL)
            else:
                loc = SourceLocation(self.filename, self.line, self.token_start_col, 1)
                raise StarSyntaxError(
                    "Unexpected character '!'",
                    loc,
                    "In Star, inequality is written as '!=' and logical negation is written as 'not'.",
                    self.source
                )
        elif c == "<":
            if self._match("="):
                self._add_token(TokenType.LESS_EQUAL)
            else:
                self._add_token(TokenType.LESS)
        elif c == ">":
            if self._match("="):
                self._add_token(TokenType.GREATER_EQUAL)
            else:
                self._add_token(TokenType.GREATER)

        # String Literals
        elif c == '"':
            self._string()

        # Numbers
        elif c.isdigit():
            self._number()

        # Identifiers & Keywords
        elif c.isalpha() or c == "_":
            self._identifier()

        else:
            loc = SourceLocation(self.filename, self.line, self.token_start_col, 1)
            raise StarSyntaxError(
                f"Unexpected character '{c}'",
                loc,
                "Remove this character or verify valid Star syntax.",
                self.source
            )

    def _string(self):
        chars = []
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
                self.column = 1
            
            c = self._advance()
            if c == "\\":
                if self._is_at_end():
                    break
                esc = self._advance()
                if esc == "n":
                    chars.append("\n")
                elif esc == "t":
                    chars.append("\t")
                elif esc == "r":
                    chars.append("\r")
                elif esc == '"':
                    chars.append('"')
                elif esc == "\\":
                    chars.append("\\")
                else:
                    chars.append(esc)
            else:
                chars.append(c)

        if self._is_at_end():
            loc = SourceLocation(self.filename, self.line, self.token_start_col, max(1, self.current - self.start))
            raise StarSyntaxError(
                "Unterminated string literal.",
                loc,
                'Add a closing quote `"` at the end of the text literal.',
                self.source
            )

        # Consume closing quote
        self._advance()
        value = "".join(chars)
        self._add_token(TokenType.TEXT, value)

    def _number(self):
        while self._peek().isdigit():
            self._advance()

        # Look for fractional part
        if self._peek() == "." and self._peek_next().isdigit():
            # Consume '.'
            self._advance()
            while self._peek().isdigit():
                self._advance()
            text = self.source[self.start:self.current]
            self._add_token(TokenType.DECIMAL, float(text))
        else:
            text = self.source[self.start:self.current]
            self._add_token(TokenType.INTEGER, int(text))

    def _identifier(self):
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        if token_type == TokenType.TRUE:
            self._add_token(token_type, True)
        elif token_type == TokenType.FALSE:
            self._add_token(token_type, False)
        elif token_type == TokenType.NULL:
            self._add_token(token_type, None)
        else:
            self._add_token(token_type, text)
