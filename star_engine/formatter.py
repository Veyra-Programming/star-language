"""
Star Language Official Code Formatter
Authoritative Reference: STAR_SPEC.md (Section 10)
"""

from typing import List, Optional
from star_engine.tokens import TokenType
from star_engine.ast_nodes import (
    ProgramNode, StatementNode, ExpressionNode,
    AppNode, ClassDeclNode, PropertyDeclNode, UseStmtNode,
    FunctionDefNode, VarDeclNode, ConstDeclNode,
    AssignNode, ShowNode, ReturnNode, BreakNode, ContinueNode,
    IfNode, WhileNode, RepeatNode, ForNode, TryCatchNode, ExpressionStmtNode,
    LiteralNode, IdentifierNode, SelfNode, BinaryOpNode, UnaryOpNode,
    CallNode, CallArg, IndexNode, MemberAccessNode, ListNode, MapNode,
    ComponentDeclNode, StateDeclNode, ComputedDeclNode, WatchDeclNode, EventDeclNode, RenderDeclNode
)
from star_engine.lexer import Lexer
from star_engine.parser import Parser


class StarFormatter:
    def __init__(self, indent_spaces: int = 4):
        self.indent_spaces = indent_spaces

    def format_code(self, source_code: str, filename: str = "<stdin>") -> str:
        lexer = Lexer(source_code, filename=filename)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source_code, filename=filename)
        program = parser.parse()
        return self.format_program(program)

    def format_program(self, program: ProgramNode) -> str:
        lines: List[str] = []
        for i, stmt in enumerate(program.statements):
            if i > 0 and isinstance(stmt, (ClassDeclNode, FunctionDefNode, AppNode)):
                lines.append("")  # Blank line before major block
            lines.extend(self._format_statement(stmt, depth=0))
            if isinstance(stmt, (ClassDeclNode, FunctionDefNode, AppNode)) and i < len(program.statements) - 1:
                lines.append("")  # Blank line after major block
        return "\n".join(lines) + "\n"

    def _indent(self, depth: int) -> str:
        return " " * (self.indent_spaces * depth)

    def _format_statement(self, stmt: StatementNode, depth: int) -> List[str]:
        ind = self._indent(depth)
        
        if isinstance(stmt, AppNode):
            lines = [f"{ind}app {stmt.name}"]
            for s in stmt.body:
                lines.extend(self._format_statement(s, depth + 1))
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, ClassDeclNode):
            lines = [f"{ind}class {stmt.name}"]
            for p in stmt.properties:
                lines.extend(self._format_statement(p, depth + 1))
            if stmt.properties and stmt.methods:
                lines.append("")
            for m in stmt.methods:
                lines.extend(self._format_statement(m, depth + 1))
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, ComponentDeclNode):
            lines = [f"{ind}component {stmt.name}"]
            for st in stmt.states:
                type_str = f": {st.type_annotation}" if st.type_annotation else ""
                init_str = f" = {self._format_expression(st.initializer)}" if st.initializer else ""
                lines.append(f"{self._indent(depth + 1)}state {st.name}{type_str}{init_str}")
            for c in stmt.computeds:
                lines.append(f"{self._indent(depth + 1)}computed {c.name} = {self._format_expression(c.expression)}")
            for ev in stmt.events:
                p_str = f"({', '.join(ev.parameters)})" if ev.parameters else ""
                lines.append(f"{self._indent(depth + 1)}event {ev.name}{p_str}")
            for w in stmt.watchers:
                lines.append(f"{self._indent(depth + 1)}watch {w.target_state}")
                if isinstance(w.handler, FunctionDefNode):
                    for s in w.handler.body:
                        lines.extend(self._format_statement(s, depth + 2))
                lines.append(f"{self._indent(depth + 1)}end")
            for m in stmt.methods:
                lines.extend(self._format_statement(m, depth + 1))
            if stmt.render_decl:
                lines.append(f"{self._indent(depth + 1)}render")
                for s in stmt.render_decl.body:
                    lines.extend(self._format_statement(s, depth + 2))
                lines.append(f"{self._indent(depth + 1)}end")
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, PropertyDeclNode):
            type_str = f": {stmt.type_annotation}" if stmt.type_annotation else ""
            init_str = f" = {self._format_expression(stmt.initializer)}" if stmt.initializer else ""
            return [f"{ind}property {stmt.name}{type_str}{init_str}"]

        if isinstance(stmt, UseStmtNode):
            target = f'"{stmt.module_name}"' if stmt.is_file else stmt.module_name
            return [f"{ind}use {target}"]

        if isinstance(stmt, FunctionDefNode):
            params_str = ", ".join(stmt.parameters)
            lines = [f"{ind}function {stmt.name}({params_str})"]
            for s in stmt.body:
                lines.extend(self._format_statement(s, depth + 1))
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, VarDeclNode):
            type_str = f": {stmt.type_annotation}" if stmt.type_annotation else ""
            init_str = f" = {self._format_expression(stmt.initializer)}" if stmt.initializer else ""
            return [f"{ind}variable {stmt.name}{type_str}{init_str}"]

        if isinstance(stmt, ConstDeclNode):
            type_str = f": {stmt.type_annotation}" if stmt.type_annotation else ""
            init_str = f" = {self._format_expression(stmt.initializer)}"
            return [f"{ind}constant {stmt.name}{type_str}{init_str}"]

        if isinstance(stmt, AssignNode):
            target_str = self._format_expression(stmt.target)
            val_str = self._format_expression(stmt.value)
            return [f"{ind}{target_str} = {val_str}"]

        if isinstance(stmt, ShowNode):
            return [f"{ind}show {self._format_expression(stmt.expression)}"]

        if isinstance(stmt, ReturnNode):
            if stmt.expression:
                return [f"{ind}return {self._format_expression(stmt.expression)}"]
            return [f"{ind}return"]

        if isinstance(stmt, BreakNode):
            return [f"{ind}break"]

        if isinstance(stmt, ContinueNode):
            return [f"{ind}continue"]

        if isinstance(stmt, IfNode):
            lines = [f"{ind}if {self._format_expression(stmt.condition)}"]
            for s in stmt.then_body:
                lines.extend(self._format_statement(s, depth + 1))
            for elif_cond, elif_body in stmt.elif_branches:
                lines.append(f"{ind}else if {self._format_expression(elif_cond)}")
                for s in elif_body:
                    lines.extend(self._format_statement(s, depth + 1))
            if stmt.else_body:
                lines.append(f"{ind}else")
                for s in stmt.else_body:
                    lines.extend(self._format_statement(s, depth + 1))
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, WhileNode):
            lines = [f"{ind}while {self._format_expression(stmt.condition)}"]
            for s in stmt.body:
                lines.extend(self._format_statement(s, depth + 1))
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, RepeatNode):
            lines = [f"{ind}repeat {self._format_expression(stmt.count)}"]
            for s in stmt.body:
                lines.extend(self._format_statement(s, depth + 1))
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, ForNode):
            lines = [f"{ind}for {stmt.variable_name} in {self._format_expression(stmt.iterable)}"]
            for s in stmt.body:
                lines.extend(self._format_statement(s, depth + 1))
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, TryCatchNode):
            lines = [f"{ind}try"]
            for s in stmt.try_body:
                lines.extend(self._format_statement(s, depth + 1))
            lines.append(f"{ind}catch {stmt.error_variable}")
            for s in stmt.catch_body:
                lines.extend(self._format_statement(s, depth + 1))
            lines.append(f"{ind}end")
            return lines

        if isinstance(stmt, ExpressionStmtNode):
            return [f"{ind}{self._format_expression(stmt.expression)}"]

        return []

    def _format_expression(self, expr: ExpressionNode) -> str:
        if isinstance(expr, LiteralNode):
            if expr.literal_type == "Text":
                escaped = expr.value.replace("\n", "\\n").replace("\t", "\\t").replace('"', '\\"')
                return f'"{escaped}"'
            if expr.literal_type == "Boolean":
                return "true" if expr.value else "false"
            if expr.literal_type == "Null":
                return "null"
            return str(expr.value)

        if isinstance(expr, IdentifierNode):
            return expr.name

        if isinstance(expr, SelfNode):
            return "self"

        if isinstance(expr, BinaryOpNode):
            op_map = {
                TokenType.PLUS: "+",
                TokenType.MINUS: "-",
                TokenType.STAR: "*",
                TokenType.SLASH: "/",
                TokenType.PERCENT: "%",
                TokenType.EQUAL_EQUAL: "==",
                TokenType.BANG_EQUAL: "!=",
                TokenType.LESS: "<",
                TokenType.LESS_EQUAL: "<=",
                TokenType.GREATER: ">",
                TokenType.GREATER_EQUAL: ">=",
                TokenType.AND: "and",
                TokenType.OR: "or",
            }
            op_str = op_map.get(expr.operator, "?")
            return f"{self._format_expression(expr.left)} {op_str} {self._format_expression(expr.right)}"

        if isinstance(expr, UnaryOpNode):
            if expr.operator == TokenType.NOT:
                return f"not {self._format_expression(expr.operand)}"
            if expr.operator == TokenType.MINUS:
                return f"-{self._format_expression(expr.operand)}"
            return f"{expr.operator.name} {self._format_expression(expr.operand)}"

        if isinstance(expr, CallNode):
            args_strs = []
            for arg in expr.arguments:
                if arg.name:
                    args_strs.append(f"{arg.name} = {self._format_expression(arg.value)}")
                else:
                    args_strs.append(self._format_expression(arg.value))
            callee_str = self._format_expression(expr.callee)
            return f"{callee_str}({', '.join(args_strs)})"

        if isinstance(expr, IndexNode):
            return f"{self._format_expression(expr.target)}[{self._format_expression(expr.index)}]"

        if isinstance(expr, MemberAccessNode):
            return f"{self._format_expression(expr.target)}.{expr.member}"

        if isinstance(expr, ListNode):
            elem_strs = [self._format_expression(e) for e in expr.elements]
            return f"[{', '.join(elem_strs)}]"

        if isinstance(expr, MapNode):
            entry_strs = [f"{self._format_expression(k)}: {self._format_expression(v)}" for k, v in expr.entries]
            return "{" + ", ".join(entry_strs) + "}"

        return ""
