"""
Star Desktop Compiler & Package Emitter
Authoritative Reference: STAR_DESKTOP.md
"""

import os
import json
from typing import Optional, Dict, Any
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.compiler import StarCompiler
from star_engine.ir import IRModule


class DesktopCompiler:
    def __init__(self, source_code: str = "", filename: str = "<stdin>"):
        self.source_code = source_code
        self.filename = filename

    def compile(self) -> Dict[str, Any]:
        lexer = Lexer(self.source_code, filename=self.filename)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=self.source_code, filename=self.filename)
        program = parser.parse()

        compiler = StarCompiler(filename=self.filename, source_code=self.source_code)
        ir_module = compiler.compile(program)
        bytecode = compiler.serialize_bytecode()

        bundle = {
            "target": "desktop",
            "version": "0.6.0",
            "entry": self.filename,
            "bytecode_hex": bytecode.hex(),
            "window": {
                "title": "Star Application",
                "width": 800,
                "height": 600,
                "resizable": True
            }
        }
        return bundle

    def emit_bundle(self, out_dir: str) -> str:
        os.makedirs(out_dir, exist_ok=True)
        bundle = self.compile()
        bundle_path = os.path.join(out_dir, "app.stardesktop")
        with open(bundle_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2)
        return bundle_path
