"""
Star Language Token Definitions
Authoritative Reference: STAR_SPEC.md (Section 3)
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    # Special Tokens
    EOF = auto()
    NEWLINE = auto()
    SEMICOLON = auto()

    # Literals
    INTEGER = auto()
    DECIMAL = auto()
    TEXT = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    # Identifiers & Keywords
    IDENTIFIER = auto()
    APP = auto()
    CLASS = auto()
    PROPERTY = auto()
    COMPONENT = auto()
    STATE = auto()
    COMPUTED = auto()
    WATCH = auto()
    EVENT = auto()
    RENDER = auto()
    USE = auto()
    SELF = auto()
    FUNCTION = auto()
    VARIABLE = auto()
    CONSTANT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    REPEAT = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    SHOW = auto()
    INPUT = auto()
    TRY = auto()
    CATCH = auto()
    END = auto()

    # Haven (Heaven) Natural English Syntax Tokens
    SET = auto()
    TO = auto()
    LET = auto()
    BE = auto()
    REMEMBER = auto()
    AS = auto()
    INCREASE = auto()
    DECREASE = auto()
    BY = auto()
    SAY = auto()
    TIMES = auto()
    WHENEVER = auto()
    UNLESS = auto()
    OTHERWISE = auto()
    UNTIL = auto()
    FOREVER = auto()
    EACH = auto()
    DEFINE = auto()
    GIVE = auto()
    BACK = auto()
    RECOVER = auto()
    ENSURE = auto()
    DURABLE = auto()
    RECORD = auto()
    IS = auto()
    PIPE_GREATER = auto()  # |>

    # Logical Operators
    AND = auto()
    OR = auto()
    NOT = auto()

    # Arithmetic Operators
    PLUS = auto()         # +
    MINUS = auto()        # -
    STAR = auto()         # *
    SLASH = auto()        # /
    PERCENT = auto()      # %

    # Comparison / Relational Operators
    EQUAL_EQUAL = auto()  # ==
    BANG_EQUAL = auto()   # !=
    LESS = auto()         # <
    LESS_EQUAL = auto()   # <=
    GREATER = auto()      # >
    GREATER_EQUAL = auto()# >=

    # Assignment & Punctuation
    EQUAL = auto()        # =
    COLON = auto()        # :
    COMMA = auto()        # ,
    DOT = auto()          # .
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    LBRACE = auto()       # {
    RBRACE = auto()       # }


KEYWORDS = {
    "app": TokenType.APP,
    "class": TokenType.CLASS,
    "property": TokenType.PROPERTY,
    "component": TokenType.COMPONENT,
    "state": TokenType.STATE,
    "computed": TokenType.COMPUTED,
    "watch": TokenType.WATCH,
    "event": TokenType.EVENT,
    "render": TokenType.RENDER,
    "use": TokenType.USE,
    "self": TokenType.SELF,
    "function": TokenType.FUNCTION,
    "variable": TokenType.VARIABLE,
    "constant": TokenType.CONSTANT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "repeat": TokenType.REPEAT,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "return": TokenType.RETURN,
    "show": TokenType.SHOW,
    "input": TokenType.INPUT,
    "try": TokenType.TRY,
    "catch": TokenType.CATCH,
    "end": TokenType.END,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,

    # Haven (Heaven) Natural English Keywords
    "set": TokenType.SET,
    "to": TokenType.TO,
    "let": TokenType.LET,
    "be": TokenType.BE,
    "remember": TokenType.REMEMBER,
    "as": TokenType.AS,
    "increase": TokenType.INCREASE,
    "decrease": TokenType.DECREASE,
    "by": TokenType.BY,
    "say": TokenType.SAY,
    "times": TokenType.TIMES,
    "whenever": TokenType.WHENEVER,
    "unless": TokenType.UNLESS,
    "otherwise": TokenType.OTHERWISE,
    "until": TokenType.UNTIL,
    "forever": TokenType.FOREVER,
    "each": TokenType.EACH,
    "define": TokenType.DEFINE,
    "give": TokenType.GIVE,
    "back": TokenType.BACK,
    "recover": TokenType.RECOVER,
    "ensure": TokenType.ENSURE,
    "durable": TokenType.DURABLE,
    "record": TokenType.RECORD,
    "is": TokenType.IS,
}


@dataclass
class SourceLocation:
    file: str
    line: int
    column: int
    length: int = 1

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"


@dataclass
class Token:
    type: TokenType
    lexeme: str
    value: Any
    location: SourceLocation

    def __str__(self) -> str:
        if self.value is not None and self.value != self.lexeme:
            return f"Token({self.type.name}, '{self.lexeme}', {repr(self.value)}, line={self.location.line}, col={self.location.column})"
        return f"Token({self.type.name}, '{self.lexeme}', line={self.location.line}, col={self.location.column})"
