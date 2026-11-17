"""
Star Language AST to Star IR Compiler & Bytecode Serializer
Authoritative Reference: STAR_IR.md
"""

import struct
import json
from typing import List, Dict, Any, Optional, Tuple
from star_engine.tokens import TokenType, SourceLocation
from star_engine.ast_nodes import (
    ProgramNode, StatementNode, ExpressionNode,
    AppNode, ClassDeclNode, PropertyDeclNode, ComponentDeclNode, StateDeclNode,
    ComputedDeclNode, WatchDeclNode, EventDeclNode, RenderDeclNode, UseStmtNode,
    FunctionDefNode, VarDeclNode, ConstDeclNode,
    AssignNode, ShowNode, ReturnNode, BreakNode, ContinueNode,
    IfNode, WhileNode, RepeatNode, ForNode, TryCatchNode, ExpressionStmtNode,
    LiteralNode, IdentifierNode, SelfNode, BinaryOpNode, UnaryOpNode,
    CallNode, CallArg, IndexNode, MemberAccessNode, ListNode, MapNode
)
from star_engine.ir import (
    OpCode, Instruction, IRFunction, IRClass, IRComponent, IRModule
)
from star_engine.errors import StarSyntaxError


class LoopContext:
    def __init__(self, start_ip: int):
        self.start_ip = start_ip
        self.break_jumps: List[int] = []
        self.continue_ip: int = start_ip


class StarCompiler:
    def __init__(self, filename: str = "<stdin>", source_code: str = ""):
        self.filename = filename
        self.source_code = source_code
        self.module = IRModule(filename=filename)
        self.current_instructions: List[Instruction] = []
        self.loop_stack: List[LoopContext] = []

    def compile(self, program: ProgramNode) -> IRModule:
        self.current_instructions = []
        for stmt in program.statements:
            self._compile_statement(stmt)

        # End of main code
        self._emit(OpCode.RETURN_NULL, location=program.location)
        self.module.instructions = self.current_instructions
        return self.module

    def _emit(self, opcode: OpCode, *operands: Any, location: Optional[SourceLocation] = None) -> int:
        idx = len(self.current_instructions)
        self.current_instructions.append(Instruction(opcode, list(operands), location))
        return idx

    def _patch_jump(self, jump_ip: int, target_ip: int):
        self.current_instructions[jump_ip].operands = [target_ip]

    # ---------------- Statement Compilation ----------------

    def _compile_statement(self, stmt: StatementNode):
        if isinstance(stmt, AppNode):
            for s in stmt.body:
                self._compile_statement(s)
            return

        if isinstance(stmt, ClassDeclNode):
            self._compile_class(stmt)
            return

        if isinstance(stmt, ComponentDeclNode):
            self._compile_component(stmt)
            return

        if isinstance(stmt, FunctionDefNode):
            self._compile_function(stmt)
            return

        if isinstance(stmt, UseStmtNode):
            name_idx = self.module.add_constant(stmt.module_name)
            self._emit(OpCode.USE_MODULE, name_idx, 1 if stmt.is_file else 0, location=stmt.location)
            return

        if isinstance(stmt, VarDeclNode):
            name_idx = self.module.add_constant(stmt.name)
            if stmt.initializer:
                self._compile_expression(stmt.initializer)
            else:
                const_null = self.module.add_constant(None)
                self._emit(OpCode.CONST, const_null, location=stmt.location)
            self._emit(OpCode.DEFINE_VAR, name_idx, location=stmt.location)
            return

        if isinstance(stmt, ConstDeclNode):
            name_idx = self.module.add_constant(stmt.name)
            self._compile_expression(stmt.initializer)
            self._emit(OpCode.DEFINE_CONST, name_idx, location=stmt.location)
            return

        if isinstance(stmt, AssignNode):
            self._compile_assignment(stmt)
            return

        if isinstance(stmt, ShowNode):
            self._compile_expression(stmt.expression)
            show_name_idx = self.module.add_constant("show")
            self._emit(OpCode.CALL_BUILTIN, show_name_idx, 1, location=stmt.location)
            self._emit(OpCode.POP, location=stmt.location)
            return

        if isinstance(stmt, ReturnNode):
            if stmt.expression:
                self._compile_expression(stmt.expression)
                self._emit(OpCode.RETURN_VAL, location=stmt.location)
            else:
                self._emit(OpCode.RETURN_NULL, location=stmt.location)
            return

        if isinstance(stmt, BreakNode):
            if not self.loop_stack:
                raise StarSyntaxError("'break' outside loop.", stmt.location, None, self.source_code)
            jump_ip = self._emit(OpCode.JUMP, 0, location=stmt.location)
            self.loop_stack[-1].break_jumps.append(jump_ip)
            return

        if isinstance(stmt, ContinueNode):
            if not self.loop_stack:
                raise StarSyntaxError("'continue' outside loop.", stmt.location, None, self.source_code)
            self._emit(OpCode.JUMP, self.loop_stack[-1].continue_ip, location=stmt.location)
            return

        if isinstance(stmt, IfNode):
            self._compile_if(stmt)
            return

        if isinstance(stmt, WhileNode):
            self._compile_while(stmt)
            return

        if isinstance(stmt, RepeatNode):
            self._compile_repeat(stmt)
            return

        if isinstance(stmt, ForNode):
            self._compile_for(stmt)
            return

        if isinstance(stmt, TryCatchNode):
            self._compile_try_catch(stmt)
            return

        if isinstance(stmt, ExpressionStmtNode):
            self._compile_expression(stmt.expression)
            self._emit(OpCode.POP, location=stmt.location)

    def _compile_class(self, stmt: ClassDeclNode):
        prop_names = [p.name for p in stmt.properties]
        defaults = {}
        for p in stmt.properties:
            if p.initializer and isinstance(p.initializer, LiteralNode):
                defaults[p.name] = p.initializer.value
        ir_class = IRClass(name=stmt.name, properties=prop_names, defaults=defaults)

        # Compile methods
        saved_instructions = self.current_instructions
        for m in stmt.methods:
            self.current_instructions = []
            for s in m.body:
                self._compile_statement(s)
            self._emit(OpCode.RETURN_NULL, location=m.location)
            ir_fn = IRFunction(name=m.name, parameters=m.parameters, instructions=self.current_instructions)
            ir_class.methods[m.name] = ir_fn

        self.current_instructions = saved_instructions
        self.module.classes[stmt.name] = ir_class

        class_name_idx = self.module.add_constant(stmt.name)
        self._emit(OpCode.MAKE_CLASS, class_name_idx, location=stmt.location)

    def _compile_component(self, stmt: ComponentDeclNode):
        states = [s.name for s in stmt.states]
        events = [e.name for e in stmt.events]
        ir_comp = IRComponent(name=stmt.name, states=states, events=events)

        saved_instructions = self.current_instructions

        # Compile computeds
        for c in stmt.computeds:
            self.current_instructions = []
            self._compile_expression(c.expression)
            self._emit(OpCode.RETURN_VAL, location=c.location)
            ir_comp.computeds[c.name] = IRFunction(name=c.name, parameters=[], instructions=self.current_instructions)

        # Compile watchers
        for w in stmt.watchers:
            self.current_instructions = []
            if isinstance(w.handler, FunctionDefNode):
                for s in w.handler.body:
                    self._compile_statement(s)
            self._emit(OpCode.RETURN_NULL, location=w.location)
            ir_comp.watchers[w.target_state] = IRFunction(name=w.target_state, parameters=["new_val", "old_val"], instructions=self.current_instructions)

        # Compile methods
        for m in stmt.methods:
            self.current_instructions = []
            for s in m.body:
                self._compile_statement(s)
            self._emit(OpCode.RETURN_NULL, location=m.location)
            ir_comp.methods[m.name] = IRFunction(name=m.name, parameters=m.parameters, instructions=self.current_instructions)

        # Compile render
        if stmt.render_decl:
            self.current_instructions = []
            for s in stmt.render_decl.body:
                self._compile_statement(s)
            self._emit(OpCode.RETURN_NULL, location=stmt.render_decl.location)
            ir_comp.render = IRFunction(name="render", parameters=[], instructions=self.current_instructions)

        self.current_instructions = saved_instructions
        self.module.components[stmt.name] = ir_comp

        comp_name_idx = self.module.add_constant(stmt.name)
        self._emit(OpCode.MAKE_COMPONENT, comp_name_idx, location=stmt.location)

    def _compile_function(self, stmt: FunctionDefNode):
        saved_instructions = self.current_instructions
        self.current_instructions = []

        for s in stmt.body:
            self._compile_statement(s)
        self._emit(OpCode.RETURN_NULL, location=stmt.location)

        ir_fn = IRFunction(name=stmt.name, parameters=stmt.parameters, instructions=self.current_instructions)
        self.module.functions[stmt.name] = ir_fn
        self.current_instructions = saved_instructions

        func_name_idx = self.module.add_constant(stmt.name)
        self._emit(OpCode.MAKE_FUNCTION, func_name_idx, location=stmt.location)

    def _compile_assignment(self, stmt: AssignNode):
        if isinstance(stmt.target, IdentifierNode):
            name_idx = self.module.add_constant(stmt.target.name)
            self._compile_expression(stmt.value)
            self._emit(OpCode.STORE_VAR, name_idx, location=stmt.location)
        elif isinstance(stmt.target, MemberAccessNode):
            self._compile_expression(stmt.target.target)
            self._compile_expression(stmt.value)
            prop_name_idx = self.module.add_constant(stmt.target.member)
            self._emit(OpCode.SET_PROP, prop_name_idx, location=stmt.location)
        elif isinstance(stmt.target, IndexNode):
            self._compile_expression(stmt.target.target)
            self._compile_expression(stmt.target.index)
            self._compile_expression(stmt.value)
            self._emit(OpCode.INDEX_SET, location=stmt.location)

    def _compile_if(self, stmt: IfNode):
        exit_jumps: List[int] = []

        # If branch
        self._compile_expression(stmt.condition)
        jump_false_ip = self._emit(OpCode.JUMP_IF_FALSE, 0, location=stmt.location)
        for s in stmt.then_body:
            self._compile_statement(s)
        exit_jumps.append(self._emit(OpCode.JUMP, 0, location=stmt.location))
        self._patch_jump(jump_false_ip, len(self.current_instructions))

        # Elif branches
        for elif_cond, elif_body in stmt.elif_branches:
            self._compile_expression(elif_cond)
            next_branch_ip = self._emit(OpCode.JUMP_IF_FALSE, 0, location=stmt.location)
            for s in elif_body:
                self._compile_statement(s)
            exit_jumps.append(self._emit(OpCode.JUMP, 0, location=stmt.location))
            self._patch_jump(next_branch_ip, len(self.current_instructions))

        # Else branch
        if stmt.else_body:
            for s in stmt.else_body:
                self._compile_statement(s)

        # Patch all exits
        for j in exit_jumps:
            self._patch_jump(j, len(self.current_instructions))

    def _compile_while(self, stmt: WhileNode):
        start_ip = len(self.current_instructions)
        loop_ctx = LoopContext(start_ip)
        self.loop_stack.append(loop_ctx)

        self._compile_expression(stmt.condition)
        exit_jump = self._emit(OpCode.JUMP_IF_FALSE, 0, location=stmt.location)

        for s in stmt.body:
            self._compile_statement(s)

        self._emit(OpCode.JUMP, start_ip, location=stmt.location)
        self._patch_jump(exit_jump, len(self.current_instructions))

        for bj in loop_ctx.break_jumps:
            self._patch_jump(bj, len(self.current_instructions))

        self.loop_stack.pop()

    def _compile_repeat(self, stmt: RepeatNode):
        # Desugar repeat count to a counter loop
        self._compile_expression(stmt.count)
        # Allocate internal loop counter
        counter_name_idx = self.module.add_constant("__repeat_counter__")
        self._emit(OpCode.DEFINE_VAR, counter_name_idx, location=stmt.location)

        start_ip = len(self.current_instructions)
        loop_ctx = LoopContext(start_ip)
        self.loop_stack.append(loop_ctx)

        # Condition: __repeat_counter__ > 0
        self._emit(OpCode.LOAD_VAR, counter_name_idx, location=stmt.location)
        zero_idx = self.module.add_constant(0)
        self._emit(OpCode.CONST, zero_idx, location=stmt.location)
        self._emit(OpCode.GREATER, location=stmt.location)
        exit_jump = self._emit(OpCode.JUMP_IF_FALSE, 0, location=stmt.location)

        for s in stmt.body:
            self._compile_statement(s)

        # Decrement counter
        self._emit(OpCode.LOAD_VAR, counter_name_idx, location=stmt.location)
        one_idx = self.module.add_constant(1)
        self._emit(OpCode.CONST, one_idx, location=stmt.location)
        self._emit(OpCode.SUB, location=stmt.location)
        self._emit(OpCode.STORE_VAR, counter_name_idx, location=stmt.location)

        self._emit(OpCode.JUMP, start_ip, location=stmt.location)
        self._patch_jump(exit_jump, len(self.current_instructions))

        for bj in loop_ctx.break_jumps:
            self._patch_jump(bj, len(self.current_instructions))

        self.loop_stack.pop()

    def _compile_for(self, stmt: ForNode):
        # Evaluate iterable
        self._compile_expression(stmt.iterable)
        iter_obj_idx = self.module.add_constant(f"__for_iter_{len(self.loop_stack)}__")
        self._emit(OpCode.DEFINE_VAR, iter_obj_idx, location=stmt.location)

        idx_var = self.module.add_constant(f"__for_idx_{len(self.loop_stack)}__")
        zero_idx = self.module.add_constant(0)
        self._emit(OpCode.CONST, zero_idx, location=stmt.location)
        self._emit(OpCode.DEFINE_VAR, idx_var, location=stmt.location)

        start_ip = len(self.current_instructions)
        loop_ctx = LoopContext(start_ip)
        self.loop_stack.append(loop_ctx)

        # Condition: idx < len(iter)
        self._emit(OpCode.LOAD_VAR, idx_var, location=stmt.location)
        self._emit(OpCode.LOAD_VAR, iter_obj_idx, location=stmt.location)
        len_name_idx = self.module.add_constant("len")
        self._emit(OpCode.CALL_BUILTIN, len_name_idx, 1, location=stmt.location)
        self._emit(OpCode.LESS, location=stmt.location)
        exit_jump = self._emit(OpCode.JUMP_IF_FALSE, 0, location=stmt.location)

        # Bind item = iter[idx]
        self._emit(OpCode.LOAD_VAR, iter_obj_idx, location=stmt.location)
        self._emit(OpCode.LOAD_VAR, idx_var, location=stmt.location)
        self._emit(OpCode.INDEX_GET, location=stmt.location)
        item_var_idx = self.module.add_constant(stmt.variable_name)
        self._emit(OpCode.DEFINE_VAR, item_var_idx, location=stmt.location)

        for s in stmt.body:
            self._compile_statement(s)

        # Advance index: idx = idx + 1
        self._emit(OpCode.LOAD_VAR, idx_var, location=stmt.location)
        one_idx = self.module.add_constant(1)
        self._emit(OpCode.CONST, one_idx, location=stmt.location)
        self._emit(OpCode.ADD, location=stmt.location)
        self._emit(OpCode.STORE_VAR, idx_var, location=stmt.location)

        self._emit(OpCode.JUMP, start_ip, location=stmt.location)
        self._patch_jump(exit_jump, len(self.current_instructions))

        for bj in loop_ctx.break_jumps:
            self._patch_jump(bj, len(self.current_instructions))

        self.loop_stack.pop()

    def _compile_try_catch(self, stmt: TryCatchNode):
        catch_jump_ip = self._emit(OpCode.PUSH_TRY, 0, self.module.add_constant(stmt.error_variable), location=stmt.location)
        for s in stmt.try_body:
            self._compile_statement(s)
        self._emit(OpCode.POP_TRY, location=stmt.location)
        exit_jump = self._emit(OpCode.JUMP, 0, location=stmt.location)

        # Catch entry point
        self._patch_jump(catch_jump_ip, len(self.current_instructions))
        for s in stmt.catch_body:
            self._compile_statement(s)

        self._patch_jump(exit_jump, len(self.current_instructions))

    # ---------------- Expression Compilation ----------------

    def _compile_expression(self, expr: ExpressionNode):
        if isinstance(expr, LiteralNode):
            const_idx = self.module.add_constant(expr.value)
            self._emit(OpCode.CONST, const_idx, location=expr.location)
            return

        if isinstance(expr, IdentifierNode):
            name_idx = self.module.add_constant(expr.name)
            self._emit(OpCode.LOAD_VAR, name_idx, location=expr.location)
            return

        if isinstance(expr, SelfNode):
            self._emit(OpCode.LOAD_SELF, location=expr.location)
            return

        if isinstance(expr, BinaryOpNode):
            # Short-circuit logical OR
            if expr.operator == TokenType.OR:
                self._compile_expression(expr.left)
                self._emit(OpCode.DUP, location=expr.location)
                jump_true = self._emit(OpCode.JUMP_IF_TRUE, 0, location=expr.location)
                self._emit(OpCode.POP, location=expr.location)
                self._compile_expression(expr.right)
                self._patch_jump(jump_true, len(self.current_instructions))
                return

            # Short-circuit logical AND
            if expr.operator == TokenType.AND:
                self._compile_expression(expr.left)
                self._emit(OpCode.DUP, location=expr.location)
                jump_false = self._emit(OpCode.JUMP_IF_FALSE, 0, location=expr.location)
                self._emit(OpCode.POP, location=expr.location)
                self._compile_expression(expr.right)
                self._patch_jump(jump_false, len(self.current_instructions))
                return

            self._compile_expression(expr.left)
            self._compile_expression(expr.right)

            op_table = {
                TokenType.PLUS: OpCode.ADD,
                TokenType.MINUS: OpCode.SUB,
                TokenType.STAR: OpCode.MUL,
                TokenType.SLASH: OpCode.DIV,
                TokenType.PERCENT: OpCode.MOD,
                TokenType.EQUAL_EQUAL: OpCode.EQUAL,
                TokenType.BANG_EQUAL: OpCode.NOT_EQUAL,
                TokenType.LESS: OpCode.LESS,
                TokenType.LESS_EQUAL: OpCode.LESS_EQUAL,
                TokenType.GREATER: OpCode.GREATER,
                TokenType.GREATER_EQUAL: OpCode.GREATER_EQUAL,
            }
            opcode = op_table.get(expr.operator)
            if opcode:
                self._emit(opcode, location=expr.location)
            return

        if isinstance(expr, UnaryOpNode):
            self._compile_expression(expr.operand)
            if expr.operator == TokenType.MINUS:
                self._emit(OpCode.NEG, location=expr.location)
            elif expr.operator == TokenType.NOT:
                self._emit(OpCode.NOT, location=expr.location)
            return

        if isinstance(expr, CallNode):
            # Check if calling a built-in directly by name
            if isinstance(expr.callee, IdentifierNode) and expr.callee.name in ("show", "len", "type", "str", "num"):
                for arg in expr.arguments:
                    self._compile_expression(arg.value)
                b_name_idx = self.module.add_constant(expr.callee.name)
                self._emit(OpCode.CALL_BUILTIN, b_name_idx, len(expr.arguments), location=expr.location)
                return

            # General call (Function, Method, or Class)
            self._compile_expression(expr.callee)
            for arg in expr.arguments:
                if arg.name:
                    n_idx = self.module.add_constant(arg.name)
                    self._emit(OpCode.CONST, n_idx, location=expr.location)
                self._compile_expression(arg.value)
            
            named_count = sum(1 for a in expr.arguments if a.name is not None)
            pos_count = len(expr.arguments) - named_count
            self._emit(OpCode.CALL, len(expr.arguments), named_count, pos_count, location=expr.location)
            return

        if isinstance(expr, MemberAccessNode):
            self._compile_expression(expr.target)
            prop_idx = self.module.add_constant(expr.member)
            self._emit(OpCode.GET_PROP, prop_idx, location=expr.location)
            return

        if isinstance(expr, IndexNode):
            self._compile_expression(expr.target)
            self._compile_expression(expr.index)
            self._emit(OpCode.INDEX_GET, location=expr.location)
            return

        if isinstance(expr, ListNode):
            for elem in expr.elements:
                self._compile_expression(elem)
            self._emit(OpCode.MAKE_LIST, len(expr.elements), location=expr.location)
            return

        if isinstance(expr, MapNode):
            for k, v in expr.entries:
                self._compile_expression(k)
                self._compile_expression(v)
            self._emit(OpCode.MAKE_MAP, len(expr.entries), location=expr.location)
            return

        if isinstance(expr, FunctionDefNode):
            anon_name = expr.name if expr.name else f"__anon_fn_{len(self.module.functions)}"
            saved_instructions = self.current_instructions
            self.current_instructions = []
            for s in expr.body:
                self._compile_statement(s)
            self._emit(OpCode.RETURN_NULL, location=expr.location)
            ir_fn = IRFunction(name=anon_name, parameters=expr.parameters, instructions=self.current_instructions)
            self.module.functions[anon_name] = ir_fn
            self.current_instructions = saved_instructions
            fn_name_idx = self.module.add_constant(anon_name)
            self._emit(OpCode.MAKE_FUNCTION, fn_name_idx, 1, location=expr.location)
            return

    # ---------------- Binary Bytecode Serializer ----------------

    def serialize_bytecode(self) -> bytes:
        data = {
            "magic": "STAR",
            "format": 1,
            "language": "0.6.0",
            "filename": self.module.filename,
            "constants": self.module.constants,
            "classes": {
                c_name: {
                    "properties": c.properties,
                    "methods": {
                        m_name: {
                            "params": m.parameters,
                            "instructions": [(inst.opcode.name, inst.operands) for inst in m.instructions]
                        }
                        for m_name, m in c.methods.items()
                    }
                }
                for c_name, c in self.module.classes.items()
            },
            "components": {
                c_name: {
                    "states": c.states,
                    "events": c.events,
                    "computeds": {
                        comp_k: {
                            "params": comp_fn.parameters,
                            "instructions": [(inst.opcode.name, inst.operands) for inst in comp_fn.instructions]
                        }
                        for comp_k, comp_fn in c.computeds.items()
                    },
                    "watchers": {
                        w_k: {
                            "params": w_fn.parameters,
                            "instructions": [(inst.opcode.name, inst.operands) for inst in w_fn.instructions]
                        }
                        for w_k, w_fn in c.watchers.items()
                    },
                    "methods": {
                        m_k: {
                            "params": m_fn.parameters,
                            "instructions": [(inst.opcode.name, inst.operands) for inst in m_fn.instructions]
                        }
                        for m_k, m_fn in c.methods.items()
                    },
                    "render": {
                        "params": c.render.parameters,
                        "instructions": [(inst.opcode.name, inst.operands) for inst in c.render.instructions]
                    } if c.render else None
                }
                for c_name, c in self.module.components.items()
            },
            "functions": {
                f_name: {
                    "params": f.parameters,
                    "instructions": [(inst.opcode.name, inst.operands) for inst in f.instructions]
                }
                for f_name, f in self.module.functions.items()
            },
            "main": [(inst.opcode.name, inst.operands) for inst in self.module.instructions]
        }
        json_bytes = json.dumps(data).encode("utf-8")
        header = struct.pack(">4sHH", b"STAR", 1, 3)
        return header + json_bytes

    @staticmethod
    def deserialize_bytecode(blob: bytes) -> IRModule:
        magic, fmt, lang = struct.unpack(">4sHH", blob[:8])
        if magic != b"STAR":
            raise ValueError("Invalid Star bytecode magic header.")
        data = json.loads(blob[8:].decode("utf-8"))

        module = IRModule(filename=data["filename"], constants=data["constants"])
        for c_name, c_data in data.get("classes", {}).items():
            methods = {}
            for m_name, m_data in c_data.get("methods", {}).items():
                insts = [Instruction(OpCode[op], ops) for op, ops in m_data["instructions"]]
                methods[m_name] = IRFunction(m_name, m_data["params"], insts)
            module.classes[c_name] = IRClass(c_name, c_data.get("properties", []), methods)

        for comp_name, comp_data in data.get("components", {}).items():
            computeds = {}
            for comp_k, c_fn_data in comp_data.get("computeds", {}).items():
                insts = [Instruction(OpCode[op], ops) for op, ops in c_fn_data["instructions"]]
                computeds[comp_k] = IRFunction(comp_k, c_fn_data["params"], insts)
            watchers = {}
            for w_k, w_fn_data in comp_data.get("watchers", {}).items():
                insts = [Instruction(OpCode[op], ops) for op, ops in w_fn_data["instructions"]]
                watchers[w_k] = IRFunction(w_k, w_fn_data["params"], insts)
            methods = {}
            for m_k, m_fn_data in comp_data.get("methods", {}).items():
                insts = [Instruction(OpCode[op], ops) for op, ops in m_fn_data["instructions"]]
                methods[m_k] = IRFunction(m_k, m_fn_data["params"], insts)
            render_fn = None
            if comp_data.get("render"):
                r_insts = [Instruction(OpCode[op], ops) for op, ops in comp_data["render"]["instructions"]]
                render_fn = IRFunction("render", comp_data["render"]["params"], r_insts)
            module.components[comp_name] = IRComponent(
                name=comp_name,
                states=comp_data.get("states", []),
                computeds=computeds,
                watchers=watchers,
                events=comp_data.get("events", []),
                methods=methods,
                render=render_fn
            )

        for f_name, f_data in data.get("functions", {}).items():
            insts = [Instruction(OpCode[op], ops) for op, ops in f_data["instructions"]]
            module.functions[f_name] = IRFunction(f_name, f_data["params"], insts)

        module.instructions = [Instruction(OpCode[op], ops) for op, ops in data["main"]]
        return module
