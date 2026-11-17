"""
Star Programming Language
Reference, Bytecode, WebAssembly, Native Desktop, Android & iOS Universal Engine
Version 1.3.0 (Official Developer Platform & Ecosystem Release)
"""

__version__ = "1.3.0"




__author__ = "Star Language Contributors"

from star_engine.tokens import TokenType, Token, SourceLocation
from star_engine.errors import (
    StarDiagnosticError,
    StarSyntaxError,
    StarRuntimeError,
    StarTypeError,
    StarNameError,
    StarValueError,
    StarInternalError,
    StarWarning
)
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.analyzer import SemanticAnalyzer
from star_engine.formatter import StarFormatter
from star_engine.ir import OpCode, Instruction, IRModule, IRFunction, IRClass
from star_engine.compiler import StarCompiler
from star_engine.vm import StarVM
from star_engine.modules import ModuleManager
from star_engine.project import create_project, init_project, load_project
from star_engine.types import StarValue, StarClass, StarInstance, StarMethod, StarModule, to_star_value
from star_engine.interpreter import Interpreter
from star_engine.natural import to_star_ui, to_star_backend, compile_english, run_english
