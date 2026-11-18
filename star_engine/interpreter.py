"""
Star Language Interpreter & Runtime Evaluator
Authoritative Reference: STAR_SPEC.md (Section 7 & Section 8)
"""

from typing import List, Dict, Any, Optional, Callable
from star_engine.tokens import TokenType, SourceLocation
from star_engine.errors import (
    StarRuntimeError, StarTypeError, StarNameError, StarValueError, StarDiagnosticError
)
from star_engine.ast_nodes import (
    ASTNode, ProgramNode, StatementNode, ExpressionNode,
    AppNode, ClassDeclNode, PropertyDeclNode, ComponentDeclNode, StateDeclNode,
    ComputedDeclNode, WatchDeclNode, EventDeclNode, RenderDeclNode, UseStmtNode,
    FunctionDefNode, VarDeclNode, ConstDeclNode,
    AssignNode, ShowNode, ReturnNode, BreakNode, ContinueNode,
    IfNode, WhileNode, RepeatNode, ForNode, TryCatchNode, ExpressionStmtNode,
    LiteralNode, IdentifierNode, SelfNode, BinaryOpNode, UnaryOpNode,
    CallNode, CallArg, IndexNode, MemberAccessNode, ListNode, MapNode,
    EnsureNode
)
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarFunction, StarBuiltinFunction,
    StarClass, StarInstance, StarMethod, StarModule,
    StarComponent, StarComponentInstance, StarReactiveState, StarVirtualNode,
    to_star_value
)
from star_engine.environment import Environment
from star_engine.modules import ModuleManager


class ReturnJump(Exception):
    def __init__(self, value: StarValue):
        self.value = value


class BreakJump(Exception):
    pass


class ContinueJump(Exception):
    pass


class Interpreter:
    def __init__(self, source_code: str = "", filename: str = "<stdin>", output_handler: Optional[Callable[[str], None]] = None):
        self.source_code = source_code
        self.filename = filename
        self.output_handler = output_handler or print
        self.global_env = Environment()
        self.module_manager = ModuleManager(self)
        self._init_builtins()

    def _init_builtins(self):
        def _builtin_show(*args: StarValue) -> StarValue:
            text_parts = [a.to_string() for a in args]
            self.output_handler(" ".join(text_parts))
            return StarNull()

        def _builtin_type(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Function 'type' expects exactly 1 argument.")
            return StarText(args[0].type_name)

        def _builtin_len(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Function 'len' expects exactly 1 argument.")
            val = args[0]
            if isinstance(val, StarText):
                return StarInteger(len(val.value))
            if isinstance(val, StarList):
                return StarInteger(len(val.elements))
            if isinstance(val, StarMap):
                return StarInteger(len(val.entries))
            raise StarTypeError(f"Cannot get length of type '{val.type_name}'.")

        def _builtin_str(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Function 'str' expects exactly 1 argument.")
            return StarText(args[0].to_string())

        def _builtin_num(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Function 'num' expects exactly 1 argument.")
            val = args[0]
            if isinstance(val, (StarInteger, StarDecimal)):
                return val
            if isinstance(val, StarBoolean):
                return StarInteger(1 if val.value else 0)
            if isinstance(val, StarText):
                try:
                    if "." in val.value:
                        return StarDecimal(float(val.value))
                    return StarInteger(int(val.value))
                except ValueError:
                    raise StarValueError(f"Cannot convert '{val.value}' to a Number.")
            raise StarTypeError(f"Cannot convert type '{val.type_name}' to Number.")

        def _builtin_trim(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Function 'trim' expects exactly 1 argument.")
            return StarText(args[0].to_string().strip())

        def _builtin_uppercase(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Function 'uppercase' expects exactly 1 argument.")
            return StarText(args[0].to_string().upper())

        def _builtin_lowercase(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Function 'lowercase' expects exactly 1 argument.")
            return StarText(args[0].to_string().lower())

        def _builtin_seal_hash(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Function 'seal_hash' expects exactly 1 argument.")
            import hashlib
            data = args[0].to_string().encode("utf-8")
            return StarText(hashlib.sha256(data).hexdigest())

        def _builtin_now_ms(*args: StarValue) -> StarValue:
            import time
            return StarInteger(int(time.time() * 1000))

        def _builtin_panic(*args: StarValue) -> StarValue:
            msg = args[0].to_string() if args else "Explicit panic triggered."
            raise StarRuntimeError(msg, None, "Handle this error using `try: ... catch err: ... end` or check program logic.", self.source_code)

        def _builtin_fail(*args: StarValue) -> StarValue:
            msg = args[0].to_string() if args else "Explicit failure triggered."
            raise StarRuntimeError(msg, None, "Handle this error using `try: ... recover as err: ... end`.", self.source_code)

        def _builtin_append(*args: StarValue) -> StarValue:
            if len(args) != 2:
                raise StarValueError("Function 'append' expects 2 arguments: list, item.")
            val = args[0]
            if not isinstance(val, StarList):
                raise StarTypeError(f"Cannot append to type '{val.type_name}'.")
            val.elements.append(args[1])
            return StarInteger(len(val.elements))

        self.global_env.define("show", StarBuiltinFunction("show", _builtin_show), is_constant=True)
        self.global_env.define("say", StarBuiltinFunction("say", _builtin_show), is_constant=True)
        self.global_env.define("type", StarBuiltinFunction("type", _builtin_type), is_constant=True)
        self.global_env.define("len", StarBuiltinFunction("len", _builtin_len), is_constant=True)
        self.global_env.define("append", StarBuiltinFunction("append", _builtin_append), is_constant=True)
        self.global_env.define("str", StarBuiltinFunction("str", _builtin_str), is_constant=True)
        self.global_env.define("num", StarBuiltinFunction("num", _builtin_num), is_constant=True)
        self.global_env.define("Integer", StarBuiltinFunction("Integer", _builtin_num), is_constant=True)
        self.global_env.define("trim", StarBuiltinFunction("trim", _builtin_trim), is_constant=True)
        self.global_env.define("uppercase", StarBuiltinFunction("uppercase", _builtin_uppercase), is_constant=True)
        self.global_env.define("lowercase", StarBuiltinFunction("lowercase", _builtin_lowercase), is_constant=True)
        self.global_env.define("seal_hash", StarBuiltinFunction("seal_hash", _builtin_seal_hash), is_constant=True)
        self.global_env.define("now_ms", StarBuiltinFunction("now_ms", _builtin_now_ms), is_constant=True)
        self.global_env.define("panic", StarBuiltinFunction("panic", _builtin_panic), is_constant=True)
        self.global_env.define("fail", StarBuiltinFunction("fail", _builtin_fail), is_constant=True)

        # Standard Modules in global scope by default if used
        for mod_name, mod in self.module_manager.loaded_modules.items():
            if mod_name not in self.global_env.bindings:
                self.global_env.define(mod_name, mod, is_constant=True)

    @property
    def globals(self) -> Environment:
        return self.global_env

    def interpret(self, program: ProgramNode) -> StarValue:
        last_value: StarValue = StarNull()
        try:
            for stmt in program.statements:
                last_value = self.execute(stmt, self.global_env)
        except ReturnJump as r:
            last_value = r.value
        except BreakJump:
            raise StarRuntimeError("Invalid 'break' statement outside of a loop.", None, "Place 'break' inside a while, repeat, or for loop.", self.source_code)
        except ContinueJump:
            raise StarRuntimeError("Invalid 'continue' statement outside of a loop.", None, "Place 'continue' inside a while, repeat, or for loop.", self.source_code)
        return last_value

    def execute(self, stmt: StatementNode, env: Environment) -> StarValue:
        if isinstance(stmt, AppNode):
            app_env = Environment(parent=env)
            last_app_val: StarValue = StarNull()
            for s in stmt.body:
                res = self.execute(s, app_env)
                if res is not None and not isinstance(res, StarNull):
                    last_app_val = res
            env.define(stmt.name, last_app_val, is_constant=False, location=stmt.location, source_code=self.source_code)
            return last_app_val

        if isinstance(stmt, ClassDeclNode):
            prop_names: List[str] = []
            prop_defaults: Dict[str, Any] = {}
            for p in stmt.properties:
                prop_names.append(p.name)
                prop_defaults[p.name] = p.initializer

            methods: Dict[str, FunctionDefNode] = {}
            for m in stmt.methods:
                methods[m.name] = m

            is_durable = getattr(stmt, "is_durable", False)
            star_class = StarClass(
                name=stmt.name,
                property_names=prop_names,
                property_defaults=prop_defaults,
                methods=methods,
                closure_env=env,
                is_durable=is_durable
            )
            env.define(stmt.name, star_class, is_constant=False, location=stmt.location, source_code=self.source_code)
            return star_class

        if isinstance(stmt, ComponentDeclNode):
            comp = StarComponent(
                name=stmt.name,
                state_decls=stmt.states,
                computed_decls=stmt.computeds,
                watch_decls=stmt.watchers,
                event_decls=stmt.events,
                methods={m.name: m for m in stmt.methods},
                render_decl=stmt.render_decl,
                closure_env=env
            )
            env.define(stmt.name, comp, is_constant=False, location=stmt.location, source_code=self.source_code)
            return comp

        if isinstance(stmt, UseStmtNode):
            mod = self.module_manager.load_module(stmt.module_name, stmt.is_file, stmt.location)
            if mod.name not in env.bindings:
                env.define(mod.name, mod, is_constant=True, location=stmt.location, source_code=self.source_code)
            if stmt.module_name in ("Flutter", "Material", "Cupertino", "Widgets"):
                for exp_name, exp_val in mod.exports.items():
                    if not exp_name.startswith("_") and exp_name not in env.bindings:
                        env.define(exp_name, exp_val, is_constant=True, location=stmt.location, source_code=self.source_code)
            return mod

        if isinstance(stmt, FunctionDefNode):
            func = StarFunction(
                name=stmt.name,
                parameters=stmt.parameters,
                body=stmt.body,
                closure_env=env
            )
            env.define(stmt.name, func, is_constant=False, location=stmt.location, source_code=self.source_code)
            return func

        if isinstance(stmt, VarDeclNode):
            val: StarValue = StarNull()
            if stmt.initializer:
                val = self.evaluate(stmt.initializer, env)
            env.define(stmt.name, val, is_constant=False, location=stmt.location, source_code=self.source_code)
            return val

        if isinstance(stmt, ConstDeclNode):
            val = self.evaluate(stmt.initializer, env)
            env.define(stmt.name, val, is_constant=True, location=stmt.location, source_code=self.source_code)
            return val

        if isinstance(stmt, AssignNode):
            val = self.evaluate(stmt.value, env)
            if isinstance(stmt.target, IdentifierNode):
                env.assign(stmt.target.name, val, location=stmt.location, source_code=self.source_code)
            elif isinstance(stmt.target, MemberAccessNode):
                target_val = self.evaluate(stmt.target.target, env)
                if isinstance(target_val, StarInstance):
                    try:
                        target_val.set(stmt.target.member, val)
                    except StarNameError as e:
                        e.location = stmt.target.location
                        e.source_code = self.source_code
                        raise e
                elif isinstance(target_val, StarMap):
                    target_val.entries[stmt.target.member] = val
                else:
                    raise StarTypeError(f"Cannot set property '{stmt.target.member}' on type '{target_val.type_name}'.", stmt.target.location, None, self.source_code)
            elif isinstance(stmt.target, IndexNode):
                target_val = self.evaluate(stmt.target.target, env)
                index_val = self.evaluate(stmt.target.index, env)
                if isinstance(target_val, StarList):
                    if not isinstance(index_val, StarInteger):
                        raise StarTypeError("List index must be an Integer.", stmt.target.index.location, None, self.source_code)
                    idx = index_val.value
                    if idx < 0 or idx >= len(target_val.elements):
                        raise StarRuntimeError(f"List index out of bounds: {idx} for length {len(target_val.elements)}.", stmt.target.location, None, self.source_code)
                    target_val.elements[idx] = val
                elif isinstance(target_val, StarMap):
                    key = index_val.value if isinstance(index_val, (StarInteger, StarDecimal, StarText, StarBoolean)) else index_val.to_string()
                    target_val.entries[key] = val
                else:
                    raise StarTypeError(f"Cannot assign by index on type '{target_val.type_name}'.", stmt.target.location, None, self.source_code)
            return val

        if isinstance(stmt, ShowNode):
            val = self.evaluate(stmt.expression, env)
            self.output_handler(val.to_string())
            return val

        if isinstance(stmt, ReturnNode):
            val = self.evaluate(stmt.expression, env) if stmt.expression else StarNull()
            raise ReturnJump(val)

        if isinstance(stmt, BreakNode):
            raise BreakJump()

        if isinstance(stmt, ContinueNode):
            raise ContinueJump()

        if isinstance(stmt, IfNode):
            cond_val = self.evaluate(stmt.condition, env)
            if cond_val.is_truthy():
                block_env = Environment(parent=env)
                for s in stmt.then_body:
                    self.execute(s, block_env)
                return StarNull()

            for elif_cond, elif_body in stmt.elif_branches:
                if self.evaluate(elif_cond, env).is_truthy():
                    block_env = Environment(parent=env)
                    for s in elif_body:
                        self.execute(s, block_env)
                    return StarNull()

            if stmt.else_body:
                block_env = Environment(parent=env)
                for s in stmt.else_body:
                    self.execute(s, block_env)
            return StarNull()

        if isinstance(stmt, WhileNode):
            while self.evaluate(stmt.condition, env).is_truthy():
                block_env = Environment(parent=env)
                try:
                    for s in stmt.body:
                        self.execute(s, block_env)
                except BreakJump:
                    break
                except ContinueJump:
                    continue
            return StarNull()

        if isinstance(stmt, RepeatNode):
            count_val = self.evaluate(stmt.count, env)
            if not isinstance(count_val, StarInteger):
                raise StarTypeError(f"Repeat count must be an Integer, got '{count_val.type_name}'.", stmt.count.location, "Provide an integer count (e.g. `repeat 5`).", self.source_code)
            if count_val.value < 0:
                raise StarValueError(f"Repeat count cannot be negative ({count_val.value}).", stmt.count.location, "Repeat count must be 0 or greater.", self.source_code)
            
            for i in range(count_val.value):
                block_env = Environment(parent=env)
                block_env.define("iteration", StarInteger(i + 1), is_constant=True)
                try:
                    for s in stmt.body:
                        self.execute(s, block_env)
                except BreakJump:
                    break
                except ContinueJump:
                    continue
            return StarNull()

        if isinstance(stmt, EnsureNode):
            cond_val = self.evaluate(stmt.condition, env)
            if not cond_val.is_truthy():
                msg = "Contract failed: condition not met."
                if stmt.message:
                    msg_val = self.evaluate(stmt.message, env)
                    msg = msg_val.to_string()
                raise StarRuntimeError(msg, stmt.location, None, self.source_code)
            return StarNull()

        if isinstance(stmt, ForNode):
            iter_val = self.evaluate(stmt.iterable, env)
            items: List[StarValue] = []
            if isinstance(iter_val, StarList):
                items = iter_val.elements
            elif isinstance(iter_val, StarText):
                items = [StarText(ch) for ch in iter_val.value]
            elif isinstance(iter_val, StarMap):
                items = [StarText(str(k)) for k in iter_val.entries.keys()]
            else:
                raise StarTypeError(f"Type '{iter_val.type_name}' is not iterable.", stmt.iterable.location, "Use a List, Text, or Map to iterate.", self.source_code)

            for item in items:
                block_env = Environment(parent=env)
                block_env.define(stmt.variable_name, item, is_constant=False)
                try:
                    for s in stmt.body:
                        self.execute(s, block_env)
                except BreakJump:
                    break
                except ContinueJump:
                    continue
            return StarNull()

        if isinstance(stmt, TryCatchNode):
            try:
                block_env = Environment(parent=env)
                for s in stmt.try_body:
                    self.execute(s, block_env)
            except (StarDiagnosticError, Exception) as err:
                catch_env = Environment(parent=env)
                err_msg = err.message if isinstance(err, StarDiagnosticError) else str(err)
                catch_env.define(stmt.error_variable, StarText(err_msg), is_constant=False)
                for s in stmt.catch_body:
                    self.execute(s, catch_env)
            return StarNull()

        if isinstance(stmt, ExpressionStmtNode):
            return self.evaluate(stmt.expression, env)

        return StarNull()

    def evaluate(self, expr: ExpressionNode, env: Environment) -> StarValue:
        if isinstance(expr, LiteralNode):
            if expr.literal_type == "Integer":
                return StarInteger(expr.value)
            if expr.literal_type == "Decimal":
                return StarDecimal(expr.value)
            if expr.literal_type == "Text":
                raw_text = expr.value
                if "{" in raw_text and "}" in raw_text:
                    raw_text = self._interpolate_string(raw_text, env)
                return StarText(raw_text)
            if expr.literal_type == "Boolean":
                return StarBoolean(expr.value)
            if expr.literal_type == "Null":
                return StarNull()

        if isinstance(expr, IdentifierNode):
            return env.lookup(expr.name, location=expr.location, source_code=self.source_code)

        if isinstance(expr, SelfNode):
            return env.lookup("self", location=expr.location, source_code=self.source_code)

        if isinstance(expr, ListNode):
            return StarList([self.evaluate(elem, env) for elem in expr.elements])

        if isinstance(expr, FunctionDefNode):
            return StarFunction(
                name=expr.name,
                parameters=expr.parameters,
                body=expr.body,
                closure_env=env
            )

        if isinstance(expr, MapNode):
            entries = {}
            for k_expr, v_expr in expr.entries:
                k_val = self.evaluate(k_expr, env)
                v_val = self.evaluate(v_expr, env)
                key = k_val.value if isinstance(k_val, (StarInteger, StarDecimal, StarText, StarBoolean)) else k_val.to_string()
                entries[key] = v_val
            return StarMap(entries)

        if isinstance(expr, UnaryOpNode):
            operand = self.evaluate(expr.operand, env)
            if expr.operator == TokenType.MINUS:
                if isinstance(operand, StarInteger):
                    return StarInteger(-operand.value)
                if isinstance(operand, StarDecimal):
                    return StarDecimal(-operand.value)
                raise StarTypeError(f"Unary '-' cannot be applied to type '{operand.type_name}'.", expr.location, "Unary '-' is only valid for Integer and Decimal values.", self.source_code)
            if expr.operator == TokenType.NOT:
                return StarBoolean(not operand.is_truthy())

        if isinstance(expr, BinaryOpNode):
            return self._eval_binary(expr, env)

        if isinstance(expr, IndexNode):
            target_val = self.evaluate(expr.target, env)
            idx_val = self.evaluate(expr.index, env)
            if isinstance(target_val, StarList):
                if not isinstance(idx_val, StarInteger):
                    raise StarTypeError(f"List index must be an Integer, got '{idx_val.type_name}'.", expr.index.location, None, self.source_code)
                idx = idx_val.value
                if idx < 0 or idx >= len(target_val.elements):
                    raise StarRuntimeError(f"List index out of bounds: {idx} (length {len(target_val.elements)}).", expr.location, None, self.source_code)
                return target_val.elements[idx]
            if isinstance(target_val, StarText):
                if not isinstance(idx_val, StarInteger):
                    raise StarTypeError(f"Text index must be an Integer, got '{idx_val.type_name}'.", expr.index.location, None, self.source_code)
                idx = idx_val.value
                if idx < 0 or idx >= len(target_val.value):
                    raise StarRuntimeError(f"Text index out of bounds: {idx} (length {len(target_val.value)}).", expr.location, None, self.source_code)
                return StarText(target_val.value[idx])
            if isinstance(target_val, StarMap):
                key = idx_val.value if isinstance(idx_val, (StarInteger, StarDecimal, StarText, StarBoolean)) else idx_val.to_string()
                if key in target_val.entries:
                    return target_val.entries[key]
                return StarNull()
            raise StarTypeError(f"Cannot index into value of type '{target_val.type_name}'.", expr.location, None, self.source_code)

        if isinstance(expr, MemberAccessNode):
            target_val = self.evaluate(expr.target, env)
            if isinstance(target_val, (StarInstance, StarModule)) or (hasattr(target_val, "get") and callable(getattr(target_val, "get")) and not isinstance(target_val, (StarMap, StarList, StarText))):
                try:
                    return target_val.get(expr.member)
                except StarNameError as e:
                    e.location = expr.location
                    e.source_code = self.source_code
                    raise e
            if isinstance(target_val, StarVirtualNode):
                if expr.member == "widget_type":
                    return StarText(target_val.tag.capitalize())
                if expr.member == "tag":
                    return StarText(target_val.tag)
                if expr.member == "props":
                    return StarMap({k: to_star_value(v) for k, v in target_val.props.items()})
                if expr.member in target_val.props:
                    return to_star_value(target_val.props[expr.member])
                if expr.member == "children":
                    return StarList([to_star_value(c) for c in target_val.children])
                return StarNull()
            if isinstance(target_val, StarMap):
                if expr.member in target_val.entries:
                    return target_val.entries[expr.member]
                if expr.member in ("keys",):
                    return StarBuiltinFunction("keys", lambda *a: StarList([StarText(k) for k in target_val.entries.keys()]))
                if expr.member in ("values",):
                    return StarBuiltinFunction("values", lambda *a: StarList(list(target_val.entries.values())))
                if expr.member in ("has", "contains_key"):
                    return StarBuiltinFunction("has", lambda *a: StarBoolean(a[0].to_string() in target_val.entries if a else False))
                if expr.member in ("size", "length"):
                    return StarInteger(len(target_val.entries))
                return StarNull()
            if isinstance(target_val, StarList):
                if expr.member in ("length", "size"):
                    return StarInteger(len(target_val.elements))
                if expr.member == "push":
                    return StarBuiltinFunction("push", lambda *a: target_val.elements.append(a[0]) or a[0] if a else StarNull())
                if expr.member == "pop":
                    return StarBuiltinFunction("pop", lambda *a: target_val.elements.pop() if target_val.elements else StarNull())
                if expr.member == "join":
                    return StarBuiltinFunction("join", lambda *a: StarText((a[0].to_string() if a else "").join([e.to_string() for e in target_val.elements])))
                if expr.member == "contains":
                    return StarBuiltinFunction("contains", lambda *a: StarBoolean(any(e == a[0] for e in target_val.elements) if a else False))
                if expr.member == "reverse":
                    return StarBuiltinFunction("reverse", lambda *a: StarList(list(reversed(target_val.elements))))
            if isinstance(target_val, StarText):
                if expr.member in ("length", "size"):
                    return StarInteger(len(target_val.value))
                if expr.member in ("uppercase", "upper"):
                    return StarBuiltinFunction("uppercase", lambda *a: StarText(target_val.value.upper()))
                if expr.member in ("lowercase", "lower"):
                    return StarBuiltinFunction("lowercase", lambda *a: StarText(target_val.value.lower()))
                if expr.member == "trim":
                    return StarBuiltinFunction("trim", lambda *a: StarText(target_val.value.strip()))
                if expr.member == "split":
                    return StarBuiltinFunction("split", lambda *a: StarList([StarText(p) for p in target_val.value.split(a[0].to_string() if a else " ")]))
                if expr.member == "contains":
                    return StarBuiltinFunction("contains", lambda *a: StarBoolean((a[0].to_string() if a else "") in target_val.value))
                if expr.member == "replace":
                    return StarBuiltinFunction("replace", lambda *a: StarText(target_val.value.replace(a[0].to_string(), a[1].to_string()) if len(a) >= 2 else target_val.value))
                if expr.member == "starts_with":
                    return StarBuiltinFunction("starts_with", lambda *a: StarBoolean(target_val.value.startswith(a[0].to_string() if a else "")))
                if expr.member == "ends_with":
                    return StarBuiltinFunction("ends_with", lambda *a: StarBoolean(target_val.value.endswith(a[0].to_string() if a else "")))
            raise StarTypeError(f"Cannot access property '{expr.member}' on type '{target_val.type_name}'.", expr.location, None, self.source_code)

        if isinstance(expr, CallNode):
            callee_val = self.evaluate(expr.callee, env)

            # 1. Calling a Class (Constructor / Instantiation)
            if isinstance(callee_val, StarClass):
                instance = StarInstance(callee_val)
                # Evaluate default initializers
                for prop_name, init_ast in callee_val.property_defaults.items():
                    if init_ast is not None:
                        instance.fields[prop_name] = self.evaluate(init_ast, callee_val.closure_env)
                    else:
                        instance.fields[prop_name] = StarNull()

                # Process constructor arguments
                pos_idx = 0
                for arg in expr.arguments:
                    if arg.name is not None:
                        if arg.name not in callee_val.property_names:
                            raise StarNameError(f"Unknown property '{arg.name}' on '{callee_val.name}'.", expr.location, f"Available properties: {', '.join(callee_val.property_names)}", self.source_code)
                        instance.fields[arg.name] = self.evaluate(arg.value, env)
                    else:
                        if pos_idx >= len(callee_val.property_names):
                            raise StarTypeError(f"Too many positional arguments to '{callee_val.name}'. Expected up to {len(callee_val.property_names)}.", expr.location, None, self.source_code)
                        prop_name = callee_val.property_names[pos_idx]
                        instance.fields[prop_name] = self.evaluate(arg.value, env)
                        pos_idx += 1
                return instance

            # Calling a Component (Instantiation & Initial Render)
            if isinstance(callee_val, StarComponent):
                props_dict: Dict[str, StarValue] = {}
                pos_idx = 0
                for arg in expr.arguments:
                    val = self.evaluate(arg.value, env)
                    if arg.name:
                        props_dict[arg.name] = val
                    else:
                        props_dict[f"arg_{pos_idx}"] = val
                        pos_idx += 1

                instance = StarComponentInstance(callee_val, props=props_dict)
                comp_env = Environment(parent=callee_val.closure_env)

                # Initialize states
                for s_decl in callee_val.state_decls:
                    init_v = self.evaluate(s_decl.initializer, comp_env) if s_decl.initializer else StarNull()
                    instance.set_state(s_decl.name, init_v)
                    comp_env.define(s_decl.name, init_v, is_constant=False)

                # Define computeds getter
                def _eval_computed(c_decl, c_env):
                    return self.evaluate(c_decl.expression, c_env)

                for c_decl in callee_val.computed_decls:
                    val = _eval_computed(c_decl, comp_env)
                    instance.computed_cache[c_decl.name] = val
                    instance.computed_dirty[c_decl.name] = False
                    comp_env.define(c_decl.name, val, is_constant=False)

                # Define watchers
                for w_decl in callee_val.watch_decls:
                    if w_decl.target_state in instance.state:
                        def _make_watcher(w_node):
                            def _listener(new_v, old_v):
                                w_env = Environment(parent=comp_env)
                                if isinstance(w_node.handler, FunctionDefNode):
                                    if len(w_node.handler.parameters) >= 1:
                                        w_env.define(w_node.handler.parameters[0], new_v)
                                    if len(w_node.handler.parameters) >= 2:
                                        w_env.define(w_node.handler.parameters[1], old_v)
                                    for s in w_node.handler.body:
                                        self.execute(s, w_env)
                            return _listener
                        instance.state[w_decl.target_state].listeners.append(_make_watcher(w_decl))

                # Render
                rendered_node: StarValue = StarNull()
                if callee_val.render_decl:
                    try:
                        for s in callee_val.render_decl.body:
                            res = self.execute(s, comp_env)
                            if res is not None and not isinstance(res, StarNull):
                                rendered_node = res
                    except ReturnJump as r:
                        rendered_node = r.value

                instance.current_vdom = rendered_node if isinstance(rendered_node, StarVirtualNode) else None
                return rendered_node if isinstance(rendered_node, StarVirtualNode) else instance

            # Evaluate arguments for functions/methods (support both positional and named kwargs)
            named_dict: Dict[str, StarValue] = {}
            pos_args: List[StarValue] = []
            for a in expr.arguments:
                val = self.evaluate(a.value, env)
                if a.name:
                    named_dict[a.name] = val
                else:
                    pos_args.append(val)

            # 2. Calling a Built-in Function
            if isinstance(callee_val, StarBuiltinFunction):
                if named_dict:
                    return callee_val.fn(StarMap(named_dict), *pos_args)
                return callee_val.fn(*pos_args)

            # 3. Calling a Bound Class Method
            if isinstance(callee_val, StarMethod):
                method_ast = callee_val.method_ast
                method_env = Environment(parent=callee_val.closure_env)
                method_env.define("self", callee_val.instance, is_constant=True)
                pos_i = 0
                for param_name in method_ast.parameters:
                    if param_name in named_dict:
                        method_env.define(param_name, named_dict[param_name], is_constant=False)
                    elif pos_i < len(pos_args):
                        method_env.define(param_name, pos_args[pos_i], is_constant=False)
                        pos_i += 1
                    else:
                        method_env.define(param_name, StarNull(), is_constant=False)

                try:
                    for s in method_ast.body:
                        self.execute(s, method_env)
                except ReturnJump as r:
                    return r.value
                return StarNull()

            # 4. Calling a First-Class Function
            if isinstance(callee_val, StarFunction):
                func_env = Environment(parent=callee_val.closure_env)
                pos_i = 0
                for param_name in callee_val.parameters:
                    if param_name in named_dict:
                        func_env.define(param_name, named_dict[param_name], is_constant=False)
                    elif pos_i < len(pos_args):
                        func_env.define(param_name, pos_args[pos_i], is_constant=False)
                        pos_i += 1
                    else:
                        func_env.define(param_name, StarNull(), is_constant=False)

                try:
                    for s in callee_val.body:
                        self.execute(s, func_env)
                except ReturnJump as r:
                    return r.value
                return StarNull()

            if hasattr(callee_val, "call") and callable(getattr(callee_val, "call")):
                return callee_val.call(pos_args)
            if callable(callee_val) and not isinstance(callee_val, StarValue):
                return to_star_value(callee_val(*pos_args))

            raise StarTypeError(
                f"Cannot call non-function value of type '{callee_val.type_name}'.",
                expr.location,
                "Make sure you are calling a function, class, or method.",
                self.source_code
            )

        return StarNull()

    def _eval_binary(self, expr: BinaryOpNode, env: Environment) -> StarValue:
        op = expr.operator

        # Short-circuit logical operators
        if op == TokenType.OR:
            left_val = self.evaluate(expr.left, env)
            if left_val.is_truthy():
                return left_val
            return self.evaluate(expr.right, env)

        if op == TokenType.AND:
            left_val = self.evaluate(expr.left, env)
            if not left_val.is_truthy():
                return left_val
            return self.evaluate(expr.right, env)

        left_val = self.evaluate(expr.left, env)
        right_val = self.evaluate(expr.right, env)

        # Equality
        if op == TokenType.EQUAL_EQUAL:
            return StarBoolean(left_val == right_val)
        if op == TokenType.BANG_EQUAL:
            return StarBoolean(left_val != right_val)

        # Addition / Concatenation
        if op == TokenType.PLUS:
            if isinstance(left_val, StarInteger) and isinstance(right_val, StarInteger):
                return StarInteger(left_val.value + right_val.value)
            if isinstance(left_val, (StarInteger, StarDecimal)) and isinstance(right_val, (StarInteger, StarDecimal)):
                return StarDecimal(float(left_val.value) + float(right_val.value))
            if isinstance(left_val, StarText) or isinstance(right_val, StarText):
                return StarText(left_val.to_string() + right_val.to_string())
            raise StarTypeError(
                f"Cannot add types '{left_val.type_name}' and '{right_val.type_name}'.",
                expr.location,
                "The '+' operator is defined for numbers and text concatenation.",
                self.source_code
            )

        # Numeric Operations (-, *, /, %)
        if op in (TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            if not isinstance(left_val, (StarInteger, StarDecimal)) or not isinstance(right_val, (StarInteger, StarDecimal)):
                raise StarTypeError(
                    f"Operator '{op.name}' requires numeric operands, got '{left_val.type_name}' and '{right_val.type_name}'.",
                    expr.location,
                    "Ensure both operands are Integer or Decimal values.",
                    self.source_code
                )
            
            l_num = left_val.value
            r_num = right_val.value

            if op == TokenType.MINUS:
                if isinstance(left_val, StarInteger) and isinstance(right_val, StarInteger):
                    return StarInteger(l_num - r_num)
                return StarDecimal(float(l_num) - float(r_num))

            if op == TokenType.STAR:
                if isinstance(left_val, StarInteger) and isinstance(right_val, StarInteger):
                    return StarInteger(l_num * r_num)
                return StarDecimal(float(l_num) * float(r_num))

            if op == TokenType.SLASH:
                if r_num == 0:
                    raise StarRuntimeError("Division by zero.", expr.location, "Ensure denominator is non-zero.", self.source_code)
                res = float(l_num) / float(r_num)
                if res.is_integer() and isinstance(left_val, StarInteger) and isinstance(right_val, StarInteger):
                    return StarInteger(int(res))
                return StarDecimal(res)

            if op == TokenType.PERCENT:
                if r_num == 0:
                    raise StarRuntimeError("Modulo by zero.", expr.location, "Ensure divisor is non-zero.", self.source_code)
                if isinstance(left_val, StarInteger) and isinstance(right_val, StarInteger):
                    return StarInteger(l_num % r_num)
                return StarDecimal(float(l_num) % float(r_num))

        # Relational Comparisons (<, <=, >, >=)
        if op in (TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            if isinstance(left_val, (StarInteger, StarDecimal)) and isinstance(right_val, (StarInteger, StarDecimal)):
                lv, rv = float(left_val.value), float(right_val.value)
                if op == TokenType.LESS:
                    return StarBoolean(lv < rv)
                if op == TokenType.LESS_EQUAL:
                    return StarBoolean(lv <= rv)
                if op == TokenType.GREATER:
                    return StarBoolean(lv > rv)
                if op == TokenType.GREATER_EQUAL:
                    return StarBoolean(lv >= rv)

            if isinstance(left_val, StarText) and isinstance(right_val, StarText):
                lt, rt = left_val.value, right_val.value
                if op == TokenType.LESS:
                    return StarBoolean(lt < rt)
                if op == TokenType.LESS_EQUAL:
                    return StarBoolean(lt <= rt)
                if op == TokenType.GREATER:
                    return StarBoolean(lt > rt)
                if op == TokenType.GREATER_EQUAL:
                    return StarBoolean(lt >= rt)

            raise StarTypeError(
                f"Cannot compare '{left_val.type_name}' with '{right_val.type_name}'.",
                expr.location,
                "Comparison operators (<, <=, >, >=) are only supported between numbers or between strings.",
                self.source_code
            )

        raise StarRuntimeError(f"Unsupported binary operator: {op}", expr.location, None, self.source_code)

    def _interpolate_string(self, text: str, env: Environment) -> str:
        import re
        def replace_match(match):
            expr_str = match.group(1).strip()
            # 1. Simple identifier e.g. {count} or {name}
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr_str):
                try:
                    val = env.lookup(expr_str)
                    return val.to_string()
                except Exception:
                    return match.group(0)
            # 2. Method call e.g. {packet.odcs_hash()}
            method_call_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\(\)$', expr_str)
            if method_call_match:
                obj_name, method_name = method_call_match.group(1), method_call_match.group(2)
                try:
                    target = env.lookup(obj_name)
                    if isinstance(target, StarInstance):
                        m = target.get(method_name)
                        if isinstance(m, StarBuiltinFunction):
                            return m.call([]).to_string()
                        elif isinstance(m, StarMethod):
                            return self._call_star_function(m.method_ast, [], m.closure_env, target).to_string()
                except Exception:
                    return match.group(0)
            # 3. Simple dot access e.g. {self.title} or {packet.tx_id}
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)+$', expr_str):
                parts = expr_str.split('.')
                try:
                    curr = env.lookup(parts[0])
                    for part in parts[1:]:
                        if isinstance(curr, StarInstance):
                            curr = curr.get(part)
                        elif isinstance(curr, StarVirtualNode):
                            if part == "widget_type":
                                curr = StarText(curr.tag.capitalize())
                            elif part == "tag":
                                curr = StarText(curr.tag)
                            elif part in curr.props:
                                curr = to_star_value(curr.props[part])
                            else:
                                return match.group(0)
                        elif isinstance(curr, StarMap) and part in curr.entries:
                            curr = curr.entries[part]
                        else:
                            return match.group(0)
                    return curr.to_string()
                except Exception:
                    return match.group(0)
            # 4. Map indexing e.g. {receipt['intent_id']} or {receipt["intent_id"]}
            map_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\[[\'"]([^\'"]+)[\'"]\]$', expr_str)
            if map_match:
                map_name, key = map_match.group(1), map_match.group(2)
                try:
                    m = env.lookup(map_name)
                    if isinstance(m, StarMap) and key in m.entries:
                        return m.entries[key].to_string()
                except Exception:
                    return match.group(0)
            # 5. Function call e.g. {len(hash)}
            fn_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\(([a-zA-Z_][a-zA-Z0-9_]*)\)$', expr_str)
            if fn_match:
                fn_name, arg_name = fn_match.group(1), fn_match.group(2)
                try:
                    fn_val = env.lookup(fn_name)
                    arg_val = env.lookup(arg_name)
                    if isinstance(fn_val, StarBuiltinFunction):
                        return fn_val.call([arg_val]).to_string()
                    elif isinstance(fn_val, StarFunction):
                        return self._call_star_function(fn_val, [arg_val], fn_val.closure_env).to_string()
                except Exception:
                    return match.group(0)
            return match.group(0)
        return re.sub(r'\{([^{}]+)\}', replace_match, text)
