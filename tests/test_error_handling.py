"""
Unit Tests for Star Error Handling & Diagnostics Engine
Authoritative Reference: STAR_SPEC.md (Section 9) & STAR_SERVER_SPEC.md
"""

import unittest
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter
from star_engine.errors import (
    StarDiagnosticError,
    StarRuntimeError,
    StarTypeError,
    StarNameError,
    StarValueError,
    StarSyntaxError,
)
from star_engine.tokens import SourceLocation
from star_runtime.mobile.isolation import RuntimeFaultBarrier


class TestErrorHandling(unittest.TestCase):
    def _run(self, code: str):
        out = []
        interp = Interpreter(output_handler=lambda s: out.append(s), source_code=code)
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        interp.interpret(ast)
        return out

    def test_try_catch_basic(self):
        code = """
        variable captured = ""
        try:
            variable x = 10 / 0
        catch err:
            set captured to err
        end
        show captured
        """
        out = self._run(code)
        self.assertIn("Division by zero", out[0])

    def test_try_recover_natural_syntax(self):
        code = """
        variable status = "init"
        try:
            fail("Network connection dropped")
        recover as failure:
            set status to failure
        end
        show status
        """
        out = self._run(code)
        self.assertEqual(out, ["Network connection dropped"])

    def test_panic_builtin(self):
        code = """
        variable handled = false
        try:
            panic("Critical hardware failure")
        catch e:
            set handled to true
        end
        show handled
        """
        out = self._run(code)
        self.assertEqual(out, ["true"])

    def test_ensure_precondition_success(self):
        code = """
        variable balance = 100
        ensure balance >= 50 otherwise "Insufficient balance"
        show "Payment approved"
        """
        out = self._run(code)
        self.assertEqual(out, ["Payment approved"])

    def test_ensure_precondition_failure_trapped(self):
        code = """
        variable reason = ""
        try:
            variable balance = 20
            ensure balance >= 50 otherwise "Insufficient balance: required 50"
        recover as err:
            set reason to err
        end
        show reason
        """
        out = self._run(code)
        self.assertEqual(out, ["Insufficient balance: required 50"])

    def test_diagnostic_visual_formatting(self):
        loc = SourceLocation(file="src/main.star", line=1, column=27, length=4)
        err = StarTypeError(
            message="Cannot perform arithmetic on Text and Boolean.",
            location=loc,
            suggestion="Arithmetic subtraction is only defined for Integer and Decimal values.",
            source_code='variable result = "hello" - true',
        )
        formatted = err.format()
        self.assertIn("Star Type Error: Cannot perform arithmetic on Text and Boolean.", formatted)
        self.assertIn("File: src/main.star", formatted)
        self.assertIn("Line: 1, Column: 27", formatted)
        self.assertIn('variable result = "hello" - true', formatted)
        self.assertIn("^^^^", formatted)
        self.assertIn("Suggestion: Arithmetic subtraction is only defined for Integer and Decimal values.", formatted)

    def test_fault_barrier_isolation(self):
        def faulty_task():
            raise StarRuntimeError("Simulated GPU crash")

        # Must not raise to caller, must return fallback
        result = RuntimeFaultBarrier.execute_safely(
            "render_frame",
            faulty_task,
            fallback_val="fallback_frame",
        )
        self.assertEqual(result, "fallback_frame")

    def test_vm_call_stack_unwinding(self):
        from star_engine.compiler import StarCompiler
        from star_engine.vm import StarVM
        code = """
        function level3()
            panic("Error inside deep call stack")
        end

        function level2()
            level3()
        end

        function level1()
            level2()
        end

        variable caught = "none"
        try:
            level1()
        catch e:
            set caught to e
        end
        show caught
        """
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        c = StarCompiler(source_code=code)
        mod = c.compile(ast)
        out = []
        vm = StarVM(mod, output_handler=lambda s: out.append(s))
        vm.run()
        self.assertEqual(out, ["Error inside deep call stack"])


if __name__ == "__main__":
    unittest.main()
