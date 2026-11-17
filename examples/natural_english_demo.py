"""
Star Programming Language — Natural English AI Compiler Demo
Demonstrates compiling plain English sentences directly into Star Declarative UI and Star Backend.

Author: Star Language Contributors & ODCS Standards Foundation
Version: Star 1.3.0
"""

import sys
import os

# Ensure star_engine is available
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_engine.natural import (
    to_star_ui,
    to_star_backend,
    compile_english,
    run_english,
)


def main():
    print("=" * 78)
    print("🌟 STAR NATURAL-ENGLISH AI COMPILER DEMO (v1.3.0)")
    print("   Translating Real English Sentences into Native Star UI & Backend")
    print("=" * 78)

    # 1. Plain English Input Sentences
    prompt = (
        'Create a screen titled "Star Sovereign Station" with an app bar "Command Center", '
        'a card for "Telemetry Mesh" showing "100% Operational", '
        'a card for "Edge Storage" showing "4.2 GB Merkle WAL", '
        'and a button labeled "Synchronize Node".'
    )
    print(f"\n[1] Input Natural English Prompt:\n    \"{prompt}\"")

    # 2. Compile to Star UI and Star Backend
    print("\n[2] Compiling English prompt to Star Language...")
    bundle = compile_english(prompt)

    print(f"    ✓ Star UI Syntax Valid:       {bundle['is_valid_star']}")
    print(f"    ✓ Star Backend Syntax Valid:  {bundle['is_valid_backend']}")

    # 3. Display Compiled Declarative UI
    print("\n" + "-" * 78)
    print("⭐ COMPILED STAR DECLARATIVE UI (main.star format):")
    print("-" * 78)
    print(bundle["star_ui"])

    # 4. Display Compiled Backend Logic
    print("-" * 78)
    print("🕊️ COMPILED STAR BACKEND & CONTINUITY LOGIC:")
    print("-" * 78)
    print(bundle["star_backend"])

    # 5. Execute Backend Logic in Star VM
    print("-" * 78)
    print("⚡ Executing generated backend logic in Star VM...")
    try:
        from star_engine.lexer import Lexer
        from star_engine.parser import Parser
        from star_engine.compiler import StarCompiler
        from star_engine.vm import StarVM

        tokens = Lexer(bundle["star_backend"]).tokenize()
        program = Parser(tokens, source_code=bundle["star_backend"]).parse()
        module = StarCompiler(source_code=bundle["star_backend"]).compile(program)
        vm = StarVM(module)
        res = vm.run()
        print(f"    ✓ Star VM Execution succeeded with result: {res}")
    except Exception as e:
        print(f"    [Notice] Star VM run: {e}")

    print("\n" + "=" * 78)
    print("🎉 STAR NATURAL-ENGLISH DEMO COMPLETE!")
    print("=" * 78)


if __name__ == "__main__":
    main()
