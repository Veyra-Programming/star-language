"""
Star Language Semantic Analyzer & Static Linter
Authoritative Reference: STAR_SPEC.md (Section 9.2)
"""

from typing import List, Dict, Set, Optional, Tuple
from star_engine.ast_nodes import (
    ASTNode, ProgramNode, StatementNode, ExpressionNode,
    AppNode, ClassDeclNode, PropertyDeclNode, ComponentDeclNode, StateDeclNode,
    ComputedDeclNode, WatchDeclNode, EventDeclNode, RenderDeclNode, UseStmtNode,
    FunctionDefNode, VarDeclNode, ConstDeclNode,
    AssignNode, ShowNode, ReturnNode, BreakNode, ContinueNode,
    IfNode, WhileNode, RepeatNode, ForNode, TryCatchNode, ExpressionStmtNode,
    LiteralNode, IdentifierNode, SelfNode, BinaryOpNode, UnaryOpNode,
    CallNode, IndexNode, MemberAccessNode, ListNode, MapNode,
    EnsureNode, RecordDeclNode
)
from star_engine.errors import (
    StarSyntaxError, StarTypeError, StarNameError, StarWarning
)
from star_engine.tokens import SourceLocation


class ScopeSymbol:
    def __init__(self, name: str, is_constant: bool, type_annotation: Optional[str], location: SourceLocation):
        self.name = name
        self.is_constant = is_constant
        self.type_annotation = type_annotation
        self.location = location
        self.is_used = False


class AnalyzerScope:
    def __init__(self, parent: Optional["AnalyzerScope"] = None, is_function: bool = False, is_class: bool = False):
        self.parent = parent
        self.is_function = is_function
        self.is_class = is_class
        self.symbols: Dict[str, ScopeSymbol] = {}

    def define(self, name: str, is_constant: bool, type_annotation: Optional[str], location: SourceLocation):
        self.symbols[name] = ScopeSymbol(name, is_constant, type_annotation, location)

    def lookup(self, name: str) -> Optional[ScopeSymbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def mark_used(self, name: str):
        if name in self.symbols:
            self.symbols[name].is_used = True
        elif self.parent:
            self.parent.mark_used(name)


class SemanticAnalyzer:
    def __init__(self, source_code: str = "", filename: str = "<stdin>"):
        self.source_code = source_code
        self.filename = filename
        self.errors: List[Exception] = []
        self.warnings: List[StarWarning] = []
        self.loop_depth = 0
        self.current_class: Optional[ClassDeclNode] = None

    def analyze(self, program: ProgramNode) -> Tuple[List[Exception], List[StarWarning]]:
        self.errors = []
        self.warnings = []
        global_scope = AnalyzerScope()

        # Builtins
        BUILTIN_NAMES = (
            "show", "type", "len", "str", "num", "Math", "Time", "String", "IO", "System",
            "say", "trim", "uppercase", "lowercase", "seal_hash", "now_ms", "Integer",
            "panic", "fail", "Server", "HTTP", "AI", "Tensor", "Neural", "Agent",
            "Omni", "Fiber", "Grid", "JIT",
            "Platform", "OS", "Web", "DB", "Template", "Security", "Session"
        )
        for b in BUILTIN_NAMES:
            global_scope.define(b, is_constant=True, type_annotation=None, location=program.location)
            global_scope.mark_used(b)

        self._analyze_statements(program.statements, global_scope)
        self._check_unused_symbols(global_scope)

        return self.errors, self.warnings

    def _check_unused_symbols(self, scope: AnalyzerScope):
        BUILTIN_NAMES = (
            "show", "type", "len", "str", "num", "Math", "Time", "String", "IO", "System",
            "say", "trim", "uppercase", "lowercase", "seal_hash", "now_ms", "Integer",
            "panic", "fail", "Server", "HTTP", "AI", "Tensor", "Neural", "Agent",
            "Omni", "Fiber", "Grid", "JIT",
            "Platform", "OS", "Web", "DB", "Template", "Security", "Session"
        )
        for name, sym in scope.symbols.items():
            if not sym.is_used and not name.startswith("_") and name not in BUILTIN_NAMES:
                self.warnings.append(
                    StarWarning(
                        f"Variable '{name}' is declared but never used.",
                        sym.location,
                        f"Remove '{name}' or prefix with an underscore if unused.",
                        self.source_code
                    )
                )

    def _analyze_statements(self, statements: List[StatementNode], scope: AnalyzerScope):
        has_returned = False
        for stmt in statements:
            if has_returned:
                self.warnings.append(
                    StarWarning(
                        "Unreachable code detected.",
                        stmt.location,
                        "Statements after 'return', 'break', or 'continue' will not be executed.",
                        self.source_code
                    )
                )
                break

            self._analyze_statement(stmt, scope)

            if isinstance(stmt, (ReturnNode, BreakNode, ContinueNode)):
                has_returned = True

    def _analyze_statement(self, stmt: StatementNode, scope: AnalyzerScope):
        if isinstance(stmt, AppNode):
            app_scope = AnalyzerScope(parent=scope)
            self._analyze_statements(stmt.body, app_scope)
            self._check_unused_symbols(app_scope)
            return

        if isinstance(stmt, ClassDeclNode):
            scope.define(stmt.name, is_constant=False, type_annotation="Class", location=stmt.location)
            class_scope = AnalyzerScope(parent=scope, is_class=True)
            self.current_class = stmt
            for prop in stmt.properties:
                class_scope.define(prop.name, is_constant=False, type_annotation=prop.type_annotation, location=prop.location)
                if prop.initializer:
                    self._analyze_expression(prop.initializer, class_scope)
            for method in stmt.methods:
                self._analyze_statement(method, class_scope)
            self.current_class = None
            return

        if isinstance(stmt, ComponentDeclNode):
            scope.define(stmt.name, is_constant=False, type_annotation="Component", location=stmt.location)
            comp_scope = AnalyzerScope(parent=scope)
            for st in stmt.states:
                comp_scope.define(st.name, is_constant=False, type_annotation=st.type_annotation, location=st.location)
                if st.initializer:
                    self._analyze_expression(st.initializer, comp_scope)
            for c in stmt.computeds:
                comp_scope.define(c.name, is_constant=True, type_annotation=None, location=c.location)
                self._analyze_expression(c.expression, comp_scope)
            for ev in stmt.events:
                comp_scope.define(ev.name, is_constant=True, type_annotation="Event", location=ev.location)
            for w in stmt.watchers:
                if isinstance(w.handler, FunctionDefNode):
                    w_scope = AnalyzerScope(parent=comp_scope, is_function=True)
                    for p in w.handler.parameters:
                        w_scope.define(p, is_constant=False, type_annotation=None, location=w.location)
                    self._analyze_statements(w.handler.body, w_scope)
            for m in stmt.methods:
                self._analyze_statement(m, comp_scope)
            if stmt.render_decl:
                r_scope = AnalyzerScope(parent=comp_scope)
                self._analyze_statements(stmt.render_decl.body, r_scope)
            return

        if isinstance(stmt, UseStmtNode):
            scope.define(stmt.module_name, is_constant=True, type_annotation="Module", location=stmt.location)
            if stmt.module_name in ("Flutter", "Material", "Cupertino", "Widgets"):
                # Register exported widget symbols for direct un-namespaced invocation
                widget_symbols = [
                    "Scaffold", "AppBar", "MaterialApp", "ElevatedButton", "FilledButton",
                    "FilledTonalButton", "OutlinedButton", "TextButton", "IconButton",
                    "FloatingActionButton", "Card", "ListTile", "TextField", "Checkbox",
                    "Switch", "Slider", "Badge", "Chip", "CircularProgressIndicator",
                    "LinearProgressIndicator", "SnackBar", "AlertDialog", "BottomNavigationBar",
                    "NavigationBar", "NavigationRail", "TabBar", "Container", "Padding",
                    "Center", "Align", "SizedBox", "Expanded", "Spacer", "Row", "Column",
                    "Stack", "Positioned", "Wrap", "ListView", "GridView", "SingleChildScrollView",
                    "Text", "Icon", "Image", "Divider", "GestureDetector", "InkWell",
                    "CustomPaint", "AnimatedContainer", "Hero", "CupertinoApp",
                    "CupertinoPageScaffold", "CupertinoNavigationBar", "CupertinoButton",
                    "CupertinoTextField", "CupertinoSwitch", "CupertinoActivityIndicator",
                    "CupertinoSegmentedControl", "Icons", "Colors", "Catalog", "Widgets",
                    "EdgeInsets", "BorderRadius", "TextStyle", "BoxDecoration"
                ]
                for sym in widget_symbols:
                    if sym not in scope.symbols:
                        scope.define(sym, is_constant=True, type_annotation="Widget", location=stmt.location)
                        scope.mark_used(sym)
            return

        if isinstance(stmt, FunctionDefNode):
            scope.define(stmt.name, is_constant=False, type_annotation="Function", location=stmt.location)
            func_scope = AnalyzerScope(parent=scope, is_function=True)
            for param in stmt.parameters:
                func_scope.define(param, is_constant=False, type_annotation=None, location=stmt.location)
            self._analyze_statements(stmt.body, func_scope)
            self._check_unused_symbols(func_scope)
            return

        if isinstance(stmt, VarDeclNode):
            if stmt.initializer:
                self._analyze_expression(stmt.initializer, scope)
                self._check_type_annotation(stmt.type_annotation, stmt.initializer, stmt.location)
            scope.define(stmt.name, is_constant=False, type_annotation=stmt.type_annotation, location=stmt.location)
            return

        if isinstance(stmt, ConstDeclNode):
            self._analyze_expression(stmt.initializer, scope)
            self._check_type_annotation(stmt.type_annotation, stmt.initializer, stmt.location)
            scope.define(stmt.name, is_constant=True, type_annotation=stmt.type_annotation, location=stmt.location)
            return

        if isinstance(stmt, AssignNode):
            self._analyze_expression(stmt.value, scope)
            if isinstance(stmt.target, IdentifierNode):
                sym = scope.lookup(stmt.target.name)
                if sym and sym.is_constant:
                    self.errors.append(
                        StarNameError(
                            f"Cannot reassign immutable constant '{stmt.target.name}'.",
                            stmt.location,
                            f"'{stmt.target.name}' was declared with 'constant'. Use 'variable' if it needs to change.",
                            self.source_code
                        )
                    )
                elif not sym:
                    scope.define(stmt.target.name, is_constant=False, type_annotation=None, location=stmt.location)
            elif isinstance(stmt.target, MemberAccessNode):
                self._analyze_expression(stmt.target.target, scope)
            elif isinstance(stmt.target, IndexNode):
                self._analyze_expression(stmt.target.target, scope)
                self._analyze_expression(stmt.target.index, scope)
            return

        if isinstance(stmt, ShowNode):
            self._analyze_expression(stmt.expression, scope)
            return

        if isinstance(stmt, ReturnNode):
            if stmt.expression:
                self._analyze_expression(stmt.expression, scope)
            return

        if isinstance(stmt, BreakNode):
            if self.loop_depth == 0:
                self.errors.append(
                    StarSyntaxError(
                        "'break' used outside of any loop.",
                        stmt.location,
                        "Place 'break' inside a while, repeat, or for loop.",
                        self.source_code
                    )
                )
            return

        if isinstance(stmt, ContinueNode):
            if self.loop_depth == 0:
                self.errors.append(
                    StarSyntaxError(
                        "'continue' used outside of any loop.",
                        stmt.location,
                        "Place 'continue' inside a while, repeat, or for loop.",
                        self.source_code
                    )
                )
            return

        if isinstance(stmt, IfNode):
            self._analyze_expression(stmt.condition, scope)
            then_scope = AnalyzerScope(parent=scope)
            self._analyze_statements(stmt.then_body, then_scope)
            self._check_unused_symbols(then_scope)

            for elif_cond, elif_body in stmt.elif_branches:
                self._analyze_expression(elif_cond, scope)
                elif_scope = AnalyzerScope(parent=scope)
                self._analyze_statements(elif_body, elif_scope)
                self._check_unused_symbols(elif_scope)

            if stmt.else_body:
                else_scope = AnalyzerScope(parent=scope)
                self._analyze_statements(stmt.else_body, else_scope)
                self._check_unused_symbols(else_scope)
            return

        if isinstance(stmt, WhileNode):
            self._analyze_expression(stmt.condition, scope)
            self.loop_depth += 1
            loop_scope = AnalyzerScope(parent=scope)
            self._analyze_statements(stmt.body, loop_scope)
            self._check_unused_symbols(loop_scope)
            self.loop_depth -= 1
            return

        if isinstance(stmt, RepeatNode):
            self._analyze_expression(stmt.count, scope)
            self.loop_depth += 1
            loop_scope = AnalyzerScope(parent=scope)
            loop_scope.define("iteration", is_constant=True, type_annotation="Integer", location=stmt.location)
            loop_scope.mark_used("iteration")
            self._analyze_statements(stmt.body, loop_scope)
            self._check_unused_symbols(loop_scope)
            self.loop_depth -= 1
            return

        if isinstance(stmt, ForNode):
            self._analyze_expression(stmt.iterable, scope)
            self.loop_depth += 1
            loop_scope = AnalyzerScope(parent=scope)
            loop_scope.define(stmt.variable_name, is_constant=False, type_annotation=None, location=stmt.location)
            self._analyze_statements(stmt.body, loop_scope)
            self._check_unused_symbols(loop_scope)
            self.loop_depth -= 1
            return

        if isinstance(stmt, TryCatchNode):
            try_scope = AnalyzerScope(parent=scope)
            self._analyze_statements(stmt.try_body, try_scope)
            self._check_unused_symbols(try_scope)

            catch_scope = AnalyzerScope(parent=scope)
            catch_scope.define(stmt.error_variable, is_constant=False, type_annotation="Text", location=stmt.location)
            self._analyze_statements(stmt.catch_body, catch_scope)
            self._check_unused_symbols(catch_scope)
            return

        if isinstance(stmt, EnsureNode):
            self._analyze_expression(stmt.condition, scope)
            if stmt.message:
                self._analyze_expression(stmt.message, scope)
            return

        if isinstance(stmt, RecordDeclNode):
            scope.define(stmt.name, is_constant=False, type_annotation="Record", location=stmt.location)
            return

        if isinstance(stmt, ExpressionStmtNode):
            self._analyze_expression(stmt.expression, scope)

    def _analyze_expression(self, expr: ExpressionNode, scope: AnalyzerScope):
        if isinstance(expr, FunctionDefNode):
            func_scope = AnalyzerScope(parent=scope, is_function=True)
            for param in expr.parameters:
                func_scope.define(param, is_constant=False, type_annotation=None, location=expr.location)
            self._analyze_statements(expr.body, func_scope)
            self._check_unused_symbols(func_scope)
            return

        if isinstance(expr, IdentifierNode):
            scope.mark_used(expr.name)
            return

        if isinstance(expr, SelfNode):
            if not self.current_class:
                self.errors.append(
                    StarSyntaxError(
                        "'self' used outside of a class method.",
                        expr.location,
                        "Use 'self' only inside class methods.",
                        self.source_code
                    )
                )
            return

        if isinstance(expr, BinaryOpNode):
            self._analyze_expression(expr.left, scope)
            self._analyze_expression(expr.right, scope)
            return

        if isinstance(expr, UnaryOpNode):
            self._analyze_expression(expr.operand, scope)
            return

        if isinstance(expr, CallNode):
            self._analyze_expression(expr.callee, scope)
            for arg in expr.arguments:
                self._analyze_expression(arg.value, scope)
            return

        if isinstance(expr, IndexNode):
            self._analyze_expression(expr.target, scope)
            self._analyze_expression(expr.index, scope)
            return

        if isinstance(expr, MemberAccessNode):
            self._analyze_expression(expr.target, scope)
            return

        if isinstance(expr, ListNode):
            for elem in expr.elements:
                self._analyze_expression(elem, scope)
            return

        if isinstance(expr, MapNode):
            for k, v in expr.entries:
                self._analyze_expression(k, scope)
                self._analyze_expression(v, scope)
            return

    def _check_type_annotation(self, type_ann: Optional[str], init_expr: ExpressionNode, location: SourceLocation):
        if not type_ann or not isinstance(init_expr, LiteralNode):
            return
        expected = type_ann
        actual = init_expr.literal_type
        if expected == "Number" and actual in ("Integer", "Decimal"):
            return
        if expected != actual and expected != "Any":
            self.errors.append(
                StarTypeError(
                    f"Variable expects type '{expected}', but initial value is '{actual}'.",
                    location,
                    f"Ensure the assigned value matches type '{expected}'.",
                    self.source_code
                )
            )
