"""
Unit Tests for Star 0.6 Component Model
Authoritative Reference: STAR_COMPONENTS.md
"""

import unittest
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.compiler import StarCompiler
from star_engine.interpreter import Interpreter
from star_engine.types import StarComponent, StarComponentInstance, StarVirtualNode, StarInteger, StarText


class TestStarComponents(unittest.TestCase):
    def test_component_parsing(self):
        source = """
component Counter
    state count = 0
    computed is_even = (count % 2 == 0)
    event onClicked()

    render
        UI.column(
            UI.text("Count: " + count)
        )
    end
end
"""
        lexer = Lexer(source, filename="test.star")
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename="test.star")
        program = parser.parse()

        self.assertEqual(len(program.statements), 1)
        comp_node = program.statements[0]
        self.assertEqual(comp_node.name, "Counter")
        self.assertEqual(len(comp_node.states), 1)
        self.assertEqual(comp_node.states[0].name, "count")
        self.assertEqual(len(comp_node.computeds), 1)
        self.assertEqual(comp_node.computeds[0].name, "is_even")
        self.assertEqual(len(comp_node.events), 1)
        self.assertEqual(comp_node.events[0].name, "onClicked")
        self.assertIsNotNone(comp_node.render_decl)

    def test_component_compilation_to_ir(self):
        source = """
component Header
    state title_text = "Hello Star"
    render
        UI.title(title_text)
    end
end
"""
        lexer = Lexer(source, filename="test.star")
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename="test.star")
        program = parser.parse()

        compiler = StarCompiler(filename="test.star", source_code=source)
        ir_mod = compiler.compile(program)

        self.assertIn("Header", ir_mod.components)
        ir_comp = ir_mod.components["Header"]
        self.assertEqual(ir_comp.name, "Header")
        self.assertIn("title_text", ir_comp.states)
        self.assertIsNotNone(ir_comp.render)

    def test_component_execution_and_vdom_creation(self):
        source = """
use UI

component CardBox
    state count = 10
    render
        UI.card(
            UI.title("Card Title"),
            UI.text("Value: " + count)
        )
    end
end

CardBox()
"""
        interp = Interpreter(source_code=source, filename="test.star")
        lexer = Lexer(source, filename="test.star")
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename="test.star")
        program = parser.parse()

        res = None
        for s in program.statements:
            res = interp.execute(s, interp.global_env)

        self.assertIsInstance(res, StarVirtualNode)
        self.assertEqual(res.tag, "card")
        self.assertEqual(len(res.children), 2)
        self.assertEqual(res.children[0].tag, "title")
    def test_extended_ui_components_and_styling(self):
        source = """
use UI

component ModernDashboard
    render
        UI.column(
            UI.stack(
                UI.icon("bell", 24, "#f59e0b"),
                UI.badge("3", "danger")
            ),
            UI.grid(
                2,
                UI.card(UI.text("Card 1")),
                UI.card(UI.text("Card 2"))
            ),
            UI.row(
                UI.avatar("AK", 40),
                UI.tabs(["Tab 1", "Tab 2"], 0, null)
            ),
            UI.toast("Saved successfully", "success"),
            UI.spinner(24, "#6366f1"),
            UI.styled("box", {"bg": "#1e293b", "radius": 12}, UI.text("Styled Content"))
        )
    end
end

ModernDashboard()
"""
        interp = Interpreter(source_code=source, filename="test_modern.star")
        lexer = Lexer(source, filename="test_modern.star")
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source, filename="test_modern.star")
        program = parser.parse()

        res = None
        for s in program.statements:
            res = interp.execute(s, interp.global_env)

        self.assertIsInstance(res, StarVirtualNode)
        self.assertEqual(res.tag, "column")
        self.assertEqual(len(res.children), 6)
        self.assertEqual(res.children[0].tag, "stack")
        self.assertEqual(res.children[1].tag, "grid")
        self.assertEqual(res.children[2].tag, "row")
        self.assertEqual(res.children[3].tag, "toast")
        self.assertEqual(res.children[4].tag, "spinner")
        self.assertEqual(res.children[5].tag, "box")
        self.assertEqual(res.children[5].props["style"]["bg"], "#1e293b")


if __name__ == "__main__":
    unittest.main()
