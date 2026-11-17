"""
Tests for Haven (Heaven) Natural English Syntax in Star
Authoritative Reference: HAVEN-SPEC.md
"""

import unittest
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.analyzer import SemanticAnalyzer
from star_engine.interpreter import Interpreter
from star_engine.types import StarInteger, StarText, StarBoolean, StarNull


class TestHeavenSyntax(unittest.TestCase):
    def run_source(self, code: str):
        tokens = Lexer(code).tokenize()
        parser = Parser(tokens, code)
        ast = parser.parse()
        analyzer = SemanticAnalyzer(code)
        errors, warnings = analyzer.analyze(ast)
        self.assertEqual(len(errors), 0, f"Semantic errors: {errors}")
        output = []
        interpreter = Interpreter(code, output_handler=lambda s: output.append(s))
        result = interpreter.interpret(ast)
        return result, output

    def test_haven_bindings_and_updates(self):
        code = """
        set count to 10
        increase count by 5
        decrease count by 2
        increase count
        decrease count
        say "Final count is {count}"
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["Final count is 13"])

    def test_haven_let_and_remember(self):
        code = """
        let port be 8080
        remember host as "localhost"
        say "Server running at {host}:{port}"
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["Server running at localhost:8080"])

    def test_haven_natural_comparisons(self):
        code = """
        set a to 10
        set b to 20
        
        whenever a is less than b:
            say "less"
        end
        
        whenever b is greater than a:
            say "greater"
        end
        
        whenever a is at most 10:
            say "at most"
        end
        
        whenever b is at least 20:
            say "at least"
        end
        
        whenever a is not equal to b:
            say "not equal"
        end
        
        set c to 10
        whenever a is equal to c:
            say "equal"
        end
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["less", "greater", "at most", "at least", "not equal", "equal"])

    def test_haven_conditionals_whenever_unless_otherwise(self):
        code = """
        set score to 85
        
        whenever score is greater than 90:
            say "A"
        otherwise if score is greater than 80:
            say "B"
        otherwise:
            say "C"
        end
        
        set offline to false
        unless offline:
            say "Connected"
        otherwise:
            say "Disconnected"
        end
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["B", "Connected"])

    def test_haven_repeat_loop_with_iteration(self):
        code = """
        set total to 0
        repeat 4 times:
            increase total by iteration
        end
        say "Total: {total}"
        """
        _, output = self.run_source(code)
        # 1 + 2 + 3 + 4 = 10
        self.assertEqual(output, ["Total: 10"])

    def test_haven_for_each_loop(self):
        code = """
        let peers be ["BLR-01", "DEL-02", "MUM-03"]
        for each peer in peers:
            say "Peer: {peer}"
        end
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["Peer: BLR-01", "Peer: DEL-02", "Peer: MUM-03"])

    def test_haven_functions_define_to_give_back(self):
        code = """
        define add(a, b):
            give back a + b
        end
        
        to greet(name):
            give back "Hello {name}!"
        end
        
        let sum be add(15, 25)
        let msg be greet("Anirudha")
        say "Sum: {sum}"
        say msg
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["Sum: 40", "Hello Anirudha!"])

    def test_haven_pipeline_operator(self):
        code = """
        let processed be "   star continuous runtime   "
            |> trim(_)
            |> uppercase(_)
        say "Result: {processed}"
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["Result: STAR CONTINUOUS RUNTIME"])

    def test_haven_ensure_and_contracts(self):
        code = """
        set quota to 100
        ensure quota is greater than 0 otherwise "Quota exhausted"
        say "Quota valid"
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["Quota valid"])

    def test_haven_try_recover(self):
        code = """
        try:
            ensure 5 is greater than 10 otherwise "Math violation"
        recover as err:
            say "Handled error: {err}"
        end
        """
        _, output = self.run_source(code)
        self.assertEqual(len(output), 1)
        self.assertIn("Math violation", output[0])

    def test_haven_durable_record(self):
        code = """
        durable record TelemetryPacket:
            node_id: String
            rtt_ms: Integer
        end
        
        let packet be TelemetryPacket(node_id: "BLR-Edge", rtt_ms: 12)
        say "Node: {packet.node_id}"
        say "RTT: {packet.rtt_ms}"
        let hash be packet.odcs_hash()
        say "Hash length: {len(hash)}"
        """
        _, output = self.run_source(code)
        self.assertEqual(output[0], "Node: BLR-Edge")
        self.assertEqual(output[1], "RTT: 12")
        self.assertEqual(output[2], "Hash length: 64")

    def test_haven_with_flutter_ui(self):
        code = """
        use Flutter
        
        define build_card(title, count):
            give back Card(
                child: Padding(
                    padding: EdgeInsets.all(16),
                    child: Column(
                        children: [
                            Text(title),
                            Text("Count is {count}")
                        ]
                    )
                )
            )
        end
        
        let my_card be build_card("Counter Card", 42)
        say "Widget built: {my_card.widget_type}"
        """
        _, output = self.run_source(code)
        self.assertEqual(output, ["Widget built: Card"])


if __name__ == "__main__":
    unittest.main()

