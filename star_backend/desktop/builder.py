"""
Star Desktop Application Builder & Runner
Authoritative Reference: STAR_DESKTOP.md
"""

import os
import sys
from typing import Optional
from star_engine.project import load_project
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter
from star_engine.types import StarComponent, StarVirtualNode, StarComponentInstance
from star_backend.desktop.compiler import DesktopCompiler
from star_backend.desktop.runtime import DesktopRuntime
from star_backend.desktop.window import DesktopWindow


class DesktopBuilder:
    def __init__(self, project_dir: str = "."):
        self.project_dir = os.path.abspath(project_dir)

    def _resolve_entry(self, target_file: Optional[str] = None) -> str:
        if target_file:
            if os.path.isabs(target_file):
                return target_file
            return os.path.join(self.project_dir, target_file)
        
        proj = load_project(self.project_dir)
        if proj and proj.entry:
            return os.path.join(self.project_dir, proj.entry)
        
        # Check standard entry files
        for candidate in ("src/main.star", "main.star", "app.star"):
            p = os.path.join(self.project_dir, candidate)
            if os.path.exists(p):
                return p
        return os.path.join(self.project_dir, "main.star")

    def build(self, target_file: Optional[str] = None, out_dir: Optional[str] = None) -> str:
        entry_path = self._resolve_entry(target_file)
        if not os.path.exists(entry_path):
            raise FileNotFoundError(f"Entry file not found: {entry_path}")

        if not out_dir:
            out_dir = os.path.join(self.project_dir, "build", "desktop")

        with open(entry_path, "r", encoding="utf-8") as f:
            source = f.read()

        compiler = DesktopCompiler(source_code=source, filename=entry_path)
        bundle_path = compiler.emit_bundle(out_dir)
        return out_dir

    def run(self, target_file: Optional[str] = None, headless: bool = False) -> int:
        entry_path = self._resolve_entry(target_file)
        if not os.path.exists(entry_path):
            print(f"Error: Entry file not found: '{entry_path}'", file=sys.stderr)
            return 1

        with open(entry_path, "r", encoding="utf-8") as f:
            source = f.read()

        lexer = Lexer(source, filename=entry_path)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename=entry_path)
        program = parser.parse()

        interp = Interpreter(source_code=source, filename=entry_path)
        last_val = None
        for stmt in program.statements:
            res = interp.execute(stmt, interp.global_env)
            if res is not None:
                last_val = res

        # Check if a component or UI tree was returned or instantiated
        mounted_node = None
        if isinstance(last_val, (StarVirtualNode, StarComponentInstance)):
            mounted_node = last_val
        else:
            # Check global env for App or Component
            for name, (val, _) in interp.global_env.bindings.items():
                if isinstance(val, (StarVirtualNode, StarComponentInstance)):
                    mounted_node = val
                    break
                if isinstance(val, StarComponent):
                    # Instantiate default
                    mounted_node = val

        if mounted_node:
            runtime = DesktopRuntime(headless=headless)
            runtime.mount(mounted_node)
            if not headless:
                runtime.window.run()
        else:
            print("✓ Desktop application executed cleanly.")

        return 0
