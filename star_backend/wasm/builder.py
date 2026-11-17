"""
Star Web Application Builder & Dev Server
Authoritative Reference: STAR_WEB.md (Section 4)
"""

import os
import shutil
import http.server
import socketserver
import webbrowser
from typing import Optional
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.compiler import StarCompiler
from star_backend.wasm.compiler import WasmCompiler


class WebBuilder:
    def __init__(self, project_dir: Optional[str] = None):
        self.project_dir = os.path.abspath(project_dir or os.getcwd())
        self.build_dir = os.path.join(self.project_dir, "build", "web")

    def build(self, entry_file: Optional[str] = None) -> str:
        entry = entry_file or os.path.join(self.project_dir, "main.star")
        if not os.path.exists(entry):
            raise FileNotFoundError(f"Star entry file not found: '{entry}'")

        os.makedirs(self.build_dir, exist_ok=True)

        # 1. Compile Star Source -> Star IR -> WASM Binary
        with open(entry, "r", encoding="utf-8") as f:
            source = f.read()

        lexer = Lexer(source, filename=entry)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename=entry)
        prog = parser.parse()

        star_compiler = StarCompiler(filename=entry, source_code=source)
        ir_mod = star_compiler.compile(prog)

        wasm_compiler = WasmCompiler(ir_mod)
        wasm_bytes = wasm_compiler.compile()

        wasm_path = os.path.join(self.build_dir, "app.wasm")
        with open(wasm_path, "wb") as f:
            f.write(wasm_bytes)

        # 2. Copy star_runtime.js and styles.css
        wasm_dir = os.path.dirname(__file__)
        shutil.copy(os.path.join(wasm_dir, "runtime.js"), os.path.join(self.build_dir, "star_runtime.js"))
        shutil.copy(os.path.join(wasm_dir, "styles.css"), os.path.join(self.build_dir, "styles.css"))

        # 3. Generate index.html
        from star_engine.project import load_project
        cfg = load_project(self.project_dir)
        app_name = cfg.name if cfg else "Star Web Application"

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="star-app-root" class="star-app-shell">
        <div id="star-ui-container">
            <h1 class="star-title">🌟 {app_name}</h1>
            <p class="star-text">Powered by Star WebAssembly Runtime.</p>
        </div>
        <div id="star-console-output" class="star-console"></div>
    </div>
    <script src="star_runtime.js"></script>
</body>
</html>
"""
        with open(os.path.join(self.build_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

        return self.build_dir

    def serve(self, port: int = 8080):
        os.chdir(self.build_dir)
        handler = http.server.SimpleHTTPRequestHandler
        # Add wasm MIME type
        handler.extensions_map.update({
            '.wasm': 'application/wasm',
        })

        with socketserver.TCPServer(("", port), handler) as httpd:
            url = f"http://localhost:{port}"
            print(f"\n🌟 Star Web Dev Server running at: {url}")
            print("Press Ctrl+C to stop.\n")
            try:
                webbrowser.open(url)
            except Exception:
                pass
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")
