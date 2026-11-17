"""
Star Web / WebAssembly Backend Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.compiler import StarCompiler
from star_backend.wasm.compiler import WasmCompiler
from star_backend.wasm.emitter import WasmEmitter


class TestWasmBackend(unittest.TestCase):
    def test_wasm_emitter_magic_header(self):
        emitter = WasmEmitter()
        blob = emitter.emit_binary()
        self.assertTrue(blob.startswith(b"\x00asm\x01\x00\x00\x00"))

    def test_wasm_compile_star_program(self):
        code = """
        show "Hello WASM!"
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=code)
        prog = parser.parse()

        star_compiler = StarCompiler(source_code=code)
        ir_mod = star_compiler.compile(prog)

        wasm_compiler = WasmCompiler(ir_mod)
        wasm_bytes = wasm_compiler.compile()

        self.assertTrue(len(wasm_bytes) > 0)
        self.assertTrue(wasm_bytes.startswith(b"\x00asm\x01\x00\x00\x00"))


if __name__ == "__main__":
    unittest.main()
