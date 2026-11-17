"""
Unit Tests for Star Flutter Framework, Material 3, Cupertino, and 60,000+ UI Component Catalog
Authoritative Reference: STAR_FLUTTER.md
"""

import unittest
import os
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.analyzer import SemanticAnalyzer
from star_engine.interpreter import Interpreter
from star_sdk.flutter import (
    create_flutter_module, create_material_module, create_cupertino_module,
    create_widgets_module, create_catalog_module, CATALOG
)
from star_engine.types import StarVirtualNode, StarInteger


class TestStarFlutter(unittest.TestCase):
    def setUp(self):
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_catalog_component_count_exceeds_60000(self):
        """Verify that the Component Catalog registers at least 60,000 UI components."""
        self.assertGreaterEqual(CATALOG.total_count, 60000, "Catalog must register 60,000+ UI components")
        self.assertGreaterEqual(len(CATALOG._categories), 10, "Must support at least 10 categories")

    def test_catalog_search_and_inspect(self):
        """Verify searching and inspecting components from the catalog."""
        results = CATALOG.search("button", limit=10)
        self.assertGreater(len(results), 0)
        first = results[0]
        info = CATALOG.inspect(first)
        self.assertIsNotNone(info)
        self.assertIn("category", info)
        self.assertIn("theme", info)

        # Render component
        vnode = CATALOG.render_component(first)
        self.assertIsInstance(vnode, StarVirtualNode)

    def test_flutter_module_exports(self):
        """Verify that create_flutter_module exports core Flutter primitives."""
        fl = create_flutter_module()
        self.assertIn("Scaffold", fl.exports)
        self.assertIn("AppBar", fl.exports)
        self.assertIn("Container", fl.exports)
        self.assertIn("Row", fl.exports)
        self.assertIn("Column", fl.exports)
        self.assertIn("Center", fl.exports)
        self.assertIn("ElevatedButton", fl.exports)
        self.assertIn("CupertinoButton", fl.exports)
        self.assertIn("Icons", fl.exports)
        self.assertIn("Colors", fl.exports)
        self.assertIn("Catalog", fl.exports)
        self.assertGreaterEqual(fl.exports["component_count"].value, 60000)

    def test_material_module_widgets(self):
        """Verify Material 3 widget node construction."""
        mat = create_material_module()
        scaffold = mat.exports["Scaffold"].fn()
        self.assertIsInstance(scaffold, StarVirtualNode)
        self.assertEqual(scaffold.tag, "scaffold")

        btn = mat.exports["ElevatedButton"].fn()
        self.assertIsInstance(btn, StarVirtualNode)
        self.assertEqual(btn.tag, "button")

    def test_cupertino_module_widgets(self):
        """Verify Cupertino iOS widget node construction."""
        cup = create_cupertino_module()
        c_btn = cup.exports["CupertinoButton"].fn()
        self.assertIsInstance(c_btn, StarVirtualNode)
        self.assertEqual(c_btn.tag, "button")
        self.assertEqual(c_btn.props.get("variant"), "cupertino")

    def test_named_arguments_with_colon(self):
        """Verify Dart/Flutter style named arguments in Star syntax."""
        src = """
        use Flutter
        use Material

        constant my_ui = Scaffold(
            appBar: AppBar(title: "Dart Style"),
            body: Center(child: Text("Hello Flutter"))
        )
        """
        lexer = Lexer(src)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=src)
        program = parser.parse()
        analyzer = SemanticAnalyzer(source_code=src)
        errors, warnings = analyzer.analyze(program)
        self.assertEqual(len(errors), 0, f"Analyzer errors: {errors}")

        interp = Interpreter(source_code=src)
        interp.interpret(program)
        self.assertIn("my_ui", interp.global_env.bindings)
        app_node = interp.global_env.bindings["my_ui"][0]
        self.assertIsInstance(app_node, StarVirtualNode)
        self.assertEqual(app_node.tag, "scaffold")

    def test_flutter_counter_example_execution(self):
        """Verify examples/flutter_counter.star runs and produces a valid UI tree."""
        fpath = os.path.join(self.repo_root, "examples", "flutter_counter.star")
        with open(fpath, "r", encoding="utf-8") as f:
            src = f.read()

        lexer = Lexer(src, filename=fpath)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=src, filename=fpath)
        prog = parser.parse()
        analyzer = SemanticAnalyzer(source_code=src)
        errors, _ = analyzer.analyze(prog)
        self.assertEqual(len(errors), 0, f"Analyzer errors: {errors}")

        interp = Interpreter(source_code=src, filename=fpath)
        interp.interpret(prog)
        self.assertIn("CounterApp", interp.global_env.bindings)

    def test_flutter_showcase_example_execution(self):
        """Verify examples/flutter_showcase.star runs with 60,000+ catalog widgets."""
        fpath = os.path.join(self.repo_root, "examples", "flutter_showcase.star")
        with open(fpath, "r", encoding="utf-8") as f:
            src = f.read()

        lexer = Lexer(src, filename=fpath)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=src, filename=fpath)
        prog = parser.parse()
        analyzer = SemanticAnalyzer(source_code=src)
        errors, _ = analyzer.analyze(prog)
        self.assertEqual(len(errors), 0, f"Analyzer errors: {errors}")

        interp = Interpreter(source_code=src, filename=fpath)
        interp.interpret(prog)
        self.assertIn("StudioApp", interp.global_env.bindings)


if __name__ == "__main__":
    unittest.main()
