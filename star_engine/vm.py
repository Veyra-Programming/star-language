"""
Star Bytecode Virtual Machine (StarVM)
Authoritative Reference: STAR_IR.md
"""

from typing import List, Dict, Any, Optional, Callable
from star_engine.tokens import SourceLocation
from star_engine.ir import OpCode, Instruction, IRModule, IRFunction, IRClass, IRComponent
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarFunction, StarBuiltinFunction,
    StarClass, StarInstance, StarMethod, StarModule,
    StarComponent, StarComponentInstance, StarReactiveState, StarVirtualNode,
    to_star_value
)
from star_engine.environment import Environment
from star_engine.modules import ModuleManager
from star_engine.errors import (
    StarRuntimeError, StarTypeError, StarNameError, StarValueError, StarDiagnosticError
)


class VMFunction(StarValue):
    def __init__(self, ir_function: IRFunction, closure_env: Environment):
        self.ir_function = ir_function
        self.closure_env = closure_env

    @property
    def type_name(self) -> str:
        return "Function"

    def to_string(self) -> str:
        return f"<function {self.ir_function.name}>"

    def __repr__(self) -> str:
        return self.to_string()


class VMMethod(StarValue):
    def __init__(self, instance: "VMInstance", ir_method: IRFunction, closure_env: Environment):
        self.instance = instance
        self.ir_method = ir_method
        self.closure_env = closure_env

    @property
    def type_name(self) -> str:
        return "Method"

    def to_string(self) -> str:
        return f"<method {self.ir_method.name}>"

    def __repr__(self) -> str:
        return self.to_string()


class VMClass(StarValue):
    def __init__(self, ir_class: IRClass, closure_env: Environment):
        self.ir_class = ir_class
        self.closure_env = closure_env

    @property
    def type_name(self) -> str:
        return "Class"

    def to_string(self) -> str:
        return f"<class {self.ir_class.name}>"

    def __repr__(self) -> str:
        return self.to_string()


class VMInstance(StarValue):
    def __init__(self, vm_class: VMClass):
        self.vm_class = vm_class
        self.fields: Dict[str, StarValue] = {}
        for p in vm_class.ir_class.properties:
            if hasattr(vm_class.ir_class, "defaults") and p in vm_class.ir_class.defaults:
                self.fields[p] = to_star_value(vm_class.ir_class.defaults[p])
            else:
                self.fields[p] = StarNull()

    @property
    def type_name(self) -> str:
        return self.vm_class.ir_class.name

    def get(self, name: str) -> StarValue:
        if name in self.fields:
            return self.fields[name]
        if name in self.vm_class.ir_class.methods:
            return VMMethod(self, self.vm_class.ir_class.methods[name], self.vm_class.closure_env)
        raise StarNameError(f"Unknown property or method '{name}' on '{self.vm_class.ir_class.name}'.", None, f"Available properties: {', '.join(self.vm_class.ir_class.properties)}")

    def set(self, name: str, value: StarValue):
        if name not in self.vm_class.ir_class.properties:
            raise StarNameError(f"Cannot set undefined property '{name}' on class '{self.vm_class.ir_class.name}'.", None, f"Declare `property {name}` before assigning.")
        self.fields[name] = value

    def to_string(self) -> str:
        field_strs = [f"{k} = {v.to_string()}" for k, v in self.fields.items()]
        return f"{self.vm_class.ir_class.name}({', '.join(field_strs)})"

    def __repr__(self) -> str:
        return self.to_string()


class VMComponent(StarValue):
    def __init__(self, ir_component: IRComponent, closure_env: Environment):
        self.ir_component = ir_component
        self.closure_env = closure_env

    @property
    def type_name(self) -> str:
        return "Component"

    def to_string(self) -> str:
        return f"<component {self.ir_component.name}>"

    def __repr__(self) -> str:
        return self.to_string()


class VMComponentInstance(StarValue):
    def __init__(self, vm_component: VMComponent, props: Optional[Dict[str, StarValue]] = None):
        self.vm_component = vm_component
        self.props = props if props is not None else {}
        self.state: Dict[str, StarReactiveState] = {s: StarReactiveState(s, StarNull()) for s in vm_component.ir_component.states}
        self.computed_cache: Dict[str, StarValue] = {}
        self.computed_dirty: Dict[str, bool] = {c: True for c in vm_component.ir_component.computeds}
        self.current_vdom: Optional[StarVirtualNode] = None

    @property
    def type_name(self) -> str:
        return self.vm_component.ir_component.name

    def to_string(self) -> str:
        state_strs = [f"{k}={v.value.to_string()}" for k, v in self.state.items()]
        return f"{self.vm_component.ir_component.name}({', '.join(state_strs)})"

    def __repr__(self) -> str:
        return self.to_string()


class CallFrame:
    def __init__(self, instructions: List[Instruction], env: Environment, return_ip: int = 0):
        self.instructions = instructions
        self.ip = 0
        self.env = env
        self.return_ip = return_ip
        self.try_stack: List[Tuple[int, str]] = []  # (catch_ip, error_var_name)


class StarVM:
    def __init__(self, module: IRModule, output_handler: Optional[Callable[[str], None]] = None):
        self.module = module
        self.output_handler = output_handler or print
        self.stack: List[StarValue] = []
        self.frames: List[CallFrame] = []
        self.global_env = Environment()
        self.module_manager = ModuleManager(self)
        self.filename = module.filename
        self._init_builtins()

    def _init_builtins(self):
        def _show(*args: StarValue) -> StarValue:
            text = " ".join(a.to_string() for a in args)
            self.output_handler(text)
            return StarNull()

        def _len(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("len() takes 1 argument.")
            v = args[0]
            if isinstance(v, StarText):
                return StarInteger(len(v.value))
            if isinstance(v, StarList):
                return StarInteger(len(v.elements))
            if isinstance(v, StarMap):
                return StarInteger(len(v.entries))
            raise StarTypeError(f"Cannot get length of type '{v.type_name}'.")

        def _type(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("type() takes 1 argument.")
            return StarText(args[0].type_name)

        def _str(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("str() takes 1 argument.")
            return StarText(args[0].to_string())

        def _num(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("num() takes 1 argument.")
            v = args[0]
            if isinstance(v, (StarInteger, StarDecimal)):
                return v
            if isinstance(v, StarBoolean):
                return StarInteger(1 if v.value else 0)
            if isinstance(v, StarText):
                try:
                    if "." in v.value:
                        return StarDecimal(float(v.value))
                    return StarInteger(int(v.value))
                except ValueError:
                    raise StarValueError(f"Cannot convert '{v.value}' to Number.")
            raise StarTypeError(f"Cannot convert '{v.type_name}' to Number.")

        self.builtins: Dict[str, Callable[..., StarValue]] = {
            "show": _show,
            "len": _len,
            "type": _type,
            "str": _str,
            "num": _num,
        }

        # Modules
        for m_name, mod in self.module_manager.loaded_modules.items():
            self.global_env.define(m_name, mod, is_constant=True)

    def execute(self, stmt: Any = None, env: Any = None):
        # Compatibility helper for ModuleManager
        if stmt is not None and env is not None:
            from star_engine.interpreter import Interpreter
            interp = Interpreter(output_handler=self.output_handler)
            return interp.execute(stmt, env)

    def run(self) -> StarValue:
        main_frame = CallFrame(self.module.instructions, self.global_env)
        self.frames = [main_frame]
        self.stack = []

        last_val: StarValue = StarNull()

        while self.frames:
            frame = self.frames[-1]

            if frame.ip >= len(frame.instructions):
                self.frames.pop()
                continue

            inst = frame.instructions[frame.ip]
            frame.ip += 1

            try:
                op = inst.opcode

                # --- Core VM Opcodes ---
                if op == OpCode.CONST:
                    val = self.module.constants[inst.operands[0]]
                    self.stack.append(to_star_value(val))

                elif op == OpCode.POP:
                    if self.stack:
                        self.stack.pop()

                elif op == OpCode.DUP:
                    if self.stack:
                        self.stack.append(self.stack[-1])

                elif op == OpCode.DEFINE_VAR:
                    name = self.module.constants[inst.operands[0]]
                    val = self.stack.pop() if self.stack else StarNull()
                    frame.env.define(name, val, is_constant=False)

                elif op == OpCode.DEFINE_CONST:
                    name = self.module.constants[inst.operands[0]]
                    val = self.stack.pop() if self.stack else StarNull()
                    frame.env.define(name, val, is_constant=True)

                elif op == OpCode.LOAD_VAR:
                    name = self.module.constants[inst.operands[0]]
                    val = frame.env.lookup(name, location=inst.location)
                    self.stack.append(val)

                elif op == OpCode.STORE_VAR:
                    name = self.module.constants[inst.operands[0]]
                    val = self.stack.pop()
                    frame.env.assign(name, val, location=inst.location)

                elif op == OpCode.LOAD_SELF:
                    val = frame.env.lookup("self", location=inst.location)
                    self.stack.append(val)

                # Arithmetic
                elif op == OpCode.ADD:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    if isinstance(a, StarInteger) and isinstance(b, StarInteger):
                        self.stack.append(StarInteger(a.value + b.value))
                    elif isinstance(a, (StarInteger, StarDecimal)) and isinstance(b, (StarInteger, StarDecimal)):
                        self.stack.append(StarDecimal(float(a.value) + float(b.value)))
                    elif isinstance(a, StarText) or isinstance(b, StarText):
                        self.stack.append(StarText(a.to_string() + b.to_string()))
                    else:
                        raise StarTypeError(f"Cannot add types '{a.type_name}' and '{b.type_name}'.", inst.location)

                elif op == OpCode.SUB:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    if isinstance(a, StarInteger) and isinstance(b, StarInteger):
                        self.stack.append(StarInteger(a.value - b.value))
                    elif isinstance(a, (StarInteger, StarDecimal)) and isinstance(b, (StarInteger, StarDecimal)):
                        self.stack.append(StarDecimal(float(a.value) - float(b.value)))
                    else:
                        raise StarTypeError("Subtraction requires numbers.", inst.location)

                elif op == OpCode.MUL:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    if isinstance(a, StarInteger) and isinstance(b, StarInteger):
                        self.stack.append(StarInteger(a.value * b.value))
                    elif isinstance(a, (StarInteger, StarDecimal)) and isinstance(b, (StarInteger, StarDecimal)):
                        self.stack.append(StarDecimal(float(a.value) * float(b.value)))
                    else:
                        raise StarTypeError("Multiplication requires numbers.", inst.location)

                elif op == OpCode.DIV:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    if not isinstance(a, (StarInteger, StarDecimal)) or not isinstance(b, (StarInteger, StarDecimal)):
                        raise StarTypeError("Division requires numbers.", inst.location)
                    if b.value == 0:
                        raise StarRuntimeError("Division by zero.", inst.location)
                    res = float(a.value) / float(b.value)
                    if res.is_integer() and isinstance(a, StarInteger) and isinstance(b, StarInteger):
                        self.stack.append(StarInteger(int(res)))
                    else:
                        self.stack.append(StarDecimal(res))

                elif op == OpCode.MOD:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    if not isinstance(a, (StarInteger, StarDecimal)) or not isinstance(b, (StarInteger, StarDecimal)):
                        raise StarTypeError("Modulo requires numbers.", inst.location)
                    if b.value == 0:
                        raise StarRuntimeError("Modulo by zero.", inst.location)
                    self.stack.append(StarInteger(int(a.value) % int(b.value)))

                elif op == OpCode.NEG:
                    a = self.stack.pop()
                    if isinstance(a, StarInteger):
                        self.stack.append(StarInteger(-a.value))
                    elif isinstance(a, StarDecimal):
                        self.stack.append(StarDecimal(-a.value))
                    else:
                        raise StarTypeError("Negation requires a number.", inst.location)

                elif op == OpCode.NOT:
                    a = self.stack.pop()
                    self.stack.append(StarBoolean(not a.is_truthy()))

                # Comparisons
                elif op == OpCode.EQUAL:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(StarBoolean(a == b))

                elif op == OpCode.NOT_EQUAL:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(StarBoolean(a != b))

                elif op == OpCode.LESS:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(StarBoolean(float(a.value) < float(b.value)))

                elif op == OpCode.LESS_EQUAL:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(StarBoolean(float(a.value) <= float(b.value)))

                elif op == OpCode.GREATER:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(StarBoolean(float(a.value) > float(b.value)))

                elif op == OpCode.GREATER_EQUAL:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.stack.append(StarBoolean(float(a.value) >= float(b.value)))

                # Jumps
                elif op == OpCode.JUMP:
                    frame.ip = inst.operands[0]

                elif op == OpCode.JUMP_IF_FALSE:
                    val = self.stack.pop()
                    if not val.is_truthy():
                        frame.ip = inst.operands[0]

                elif op == OpCode.JUMP_IF_TRUE:
                    val = self.stack.pop()
                    if val.is_truthy():
                        frame.ip = inst.operands[0]

                # Built-in Calls
                elif op == OpCode.CALL_BUILTIN:
                    name = self.module.constants[inst.operands[0]]
                    arg_count = inst.operands[1]
                    args = [self.stack.pop() for _ in range(arg_count)][::-1]
                    fn = self.builtins.get(name)
                    if not fn:
                        raise StarNameError(f"Unknown builtin function '{name}'.", inst.location)
                    res = fn(*args)
                    self.stack.append(res)

                # General Calls
                elif op == OpCode.CALL:
                    total_args = inst.operands[0]
                    named_count = inst.operands[1] if len(inst.operands) > 1 else 0
                    pos_count = inst.operands[2] if len(inst.operands) > 2 else total_args
                    total_items = named_count * 2 + pos_count
                    # Pop args
                    raw_items = [self.stack.pop() for _ in range(total_items)][::-1]
                    callee = self.stack.pop()

                    args = raw_items[:pos_count]
                    kwargs = {}
                    named_items = raw_items[pos_count:]
                    for k_idx in range(0, len(named_items), 2):
                        k_item = named_items[k_idx]
                        key = k_item.value if hasattr(k_item, "value") else str(k_item)
                        val = named_items[k_idx + 1]
                        kwargs[key] = val

                    if isinstance(callee, VMClass):
                        instance = VMInstance(callee)
                        # Assign positional arguments to properties
                        for i, arg in enumerate(args):
                            if i < len(callee.ir_class.properties):
                                instance.fields[callee.ir_class.properties[i]] = arg
                        # Assign named kwargs to properties
                        for k, v in kwargs.items():
                            instance.fields[k] = v
                        self.stack.append(instance)

                    elif isinstance(callee, VMMethod):
                        method_env = Environment(parent=callee.closure_env)
                        method_env.define("self", callee.instance, is_constant=True)
                        for param_name, arg_val in zip(callee.ir_method.parameters, args):
                            method_env.define(param_name, arg_val, is_constant=False)
                        for k, v in kwargs.items():
                            method_env.define(k, v, is_constant=False)
                        new_frame = CallFrame(callee.ir_method.instructions, method_env)
                        self.frames.append(new_frame)

                    elif isinstance(callee, VMFunction):
                        func_env = Environment(parent=callee.closure_env)
                        for param_name, arg_val in zip(callee.ir_function.parameters, args):
                            func_env.define(param_name, arg_val, is_constant=False)
                        for k, v in kwargs.items():
                            func_env.define(k, v, is_constant=False)
                        new_frame = CallFrame(callee.ir_function.instructions, func_env)
                        self.frames.append(new_frame)

                    elif isinstance(callee, (VMComponent, StarComponent)):
                        props_dict = {f"arg_{i}": a for i, a in enumerate(args)}
                        props_dict.update(kwargs)
                        inst_obj = VMComponentInstance(callee, props_dict) if isinstance(callee, VMComponent) else StarComponentInstance(callee, props_dict)
                        ir_comp = callee.ir_component if isinstance(callee, VMComponent) else None
                        if ir_comp and ir_comp.render:
                            render_env = Environment(parent=callee.closure_env)
                            for s_name in ir_comp.states:
                                render_env.define(s_name, inst_obj.state[s_name].value)
                            new_frame = CallFrame(ir_comp.render.instructions, render_env)
                            self.frames.append(new_frame)
                        else:
                            self.stack.append(inst_obj)

                    elif isinstance(callee, StarFunction):
                        from star_engine.interpreter import Interpreter, ReturnJump
                        interp = Interpreter(output_handler=self.output_handler)
                        func_env = Environment(parent=callee.closure_env)
                        for param_name, arg_val in zip(callee.parameters, args):
                            func_env.define(param_name, arg_val, is_constant=False)
                        for k, v in kwargs.items():
                            func_env.define(k, v, is_constant=False)
                        ret_val = StarNull()
                        for s in callee.body:
                            try:
                                interp.execute(s, func_env)
                            except ReturnJump as r:
                                ret_val = r.value
                                break
                        self.stack.append(ret_val)

                    elif isinstance(callee, VMClass):
                        instance_obj = VMInstance(callee)
                        for prop_name, arg_val in zip(callee.ir_class.properties, args):
                            instance_obj.fields[prop_name] = arg_val
                        for k, v in kwargs.items():
                            instance_obj.fields[k] = v
                        self.stack.append(instance_obj)

                    elif isinstance(callee, StarClass):
                        instance_obj = StarInstance(callee)
                        from star_engine.interpreter import Interpreter
                        interp = Interpreter(output_handler=self.output_handler)
                        for prop_name, init_ast in callee.property_defaults.items():
                            if init_ast is not None:
                                instance_obj.fields[prop_name] = interp.evaluate(init_ast, callee.closure_env)
                            else:
                                instance_obj.fields[prop_name] = StarNull()
                        for prop_name, arg_val in zip(callee.property_names, args):
                            instance_obj.fields[prop_name] = arg_val
                        for k, v in kwargs.items():
                            instance_obj.fields[k] = v
                        self.stack.append(instance_obj)

                    elif isinstance(callee, StarMethod):
                        from star_engine.interpreter import Interpreter, ReturnJump
                        interp = Interpreter(output_handler=self.output_handler)
                        method_env = Environment(parent=callee.closure_env)
                        method_env.define("self", callee.instance, is_constant=True)
                        for param_name, arg_val in zip(callee.method_ast.parameters, args):
                            method_env.define(param_name, arg_val, is_constant=False)
                        for k, v in kwargs.items():
                            method_env.define(k, v, is_constant=False)
                        ret_val = StarNull()
                        for s in callee.method_ast.body:
                            try:
                                interp.execute(s, method_env)
                            except ReturnJump as r:
                                ret_val = r.value
                                break
                        self.stack.append(ret_val)

                    elif isinstance(callee, StarBuiltinFunction):
                        if kwargs:
                            res = callee.fn(StarMap(kwargs), *args)
                        else:
                            res = callee.fn(*args)
                        self.stack.append(res)
                    else:
                        raise StarTypeError(f"Cannot call value of type '{callee.type_name}'.", inst.location)

                elif op == OpCode.RETURN_VAL:
                    last_val = self.stack.pop() if self.stack else StarNull()
                    self.frames.pop()
                    if self.frames:
                        self.stack.append(last_val)

                elif op == OpCode.RETURN_NULL:
                    last_val = StarNull()
                    self.frames.pop()
                    if self.frames:
                        self.stack.append(last_val)

                # Functions & Classes & Components
                elif op == OpCode.MAKE_FUNCTION:
                    name = self.module.constants[inst.operands[0]]
                    ir_fn = self.module.functions[name]
                    fn_obj = VMFunction(ir_fn, frame.env)
                    frame.env.define(name, fn_obj, is_constant=False)
                    push_to_stack = (len(inst.operands) > 1 and inst.operands[1] == 1) or name.startswith("__anon_fn_")
                    if push_to_stack:
                        self.stack.append(fn_obj)

                elif op == OpCode.MAKE_CLASS:
                    name = self.module.constants[inst.operands[0]]
                    ir_cls = self.module.classes[name]
                    cls_obj = VMClass(ir_cls, frame.env)
                    frame.env.define(name, cls_obj, is_constant=False)

                elif op == OpCode.MAKE_COMPONENT:
                    name = self.module.constants[inst.operands[0]]
                    ir_comp = self.module.components[name]
                    comp_obj = VMComponent(ir_comp, frame.env)
                    frame.env.define(name, comp_obj, is_constant=False)

                # Properties & Indexing
                elif op == OpCode.GET_PROP:
                    prop_name = self.module.constants[inst.operands[0]]
                    target = self.stack.pop()
                    if isinstance(target, (VMInstance, StarInstance)):
                        self.stack.append(target.get(prop_name))
                    elif isinstance(target, StarModule):
                        self.stack.append(target.get(prop_name))
                    elif isinstance(target, StarVirtualNode):
                        if prop_name == "widget_type":
                            self.stack.append(StarText(target.tag.capitalize()))
                        elif prop_name == "tag":
                            self.stack.append(StarText(target.tag))
                        elif prop_name == "props":
                            self.stack.append(StarMap({k: to_star_value(v) for k, v in target.props.items()}))
                        elif prop_name in target.props:
                            self.stack.append(to_star_value(target.props[prop_name]))
                        elif prop_name == "children":
                            self.stack.append(StarList([to_star_value(c) for c in target.children]))
                        else:
                            self.stack.append(StarNull())
                    elif isinstance(target, StarMap):
                        self.stack.append(target.entries.get(prop_name, StarNull()))
                    else:
                        raise StarTypeError(f"Cannot get property '{prop_name}' on '{target.type_name}'.", inst.location)

                elif op == OpCode.SET_PROP:
                    prop_name = self.module.constants[inst.operands[0]]
                    val = self.stack.pop()
                    target = self.stack.pop()
                    if isinstance(target, (VMInstance, StarInstance)):
                        target.set(prop_name, val)
                    elif isinstance(target, StarMap):
                        target.entries[prop_name] = val
                    else:
                        raise StarTypeError(f"Cannot set property '{prop_name}' on '{target.type_name}'.", inst.location)

                elif op == OpCode.INDEX_GET:
                    idx = self.stack.pop()
                    target = self.stack.pop()
                    if isinstance(target, StarList):
                        self.stack.append(target.elements[int(idx.value)])
                    elif isinstance(target, StarText):
                        self.stack.append(StarText(target.value[int(idx.value)]))
                    elif isinstance(target, StarMap):
                        key = idx.value if isinstance(idx, (StarInteger, StarDecimal, StarText, StarBoolean)) else idx.to_string()
                        self.stack.append(target.entries.get(key, StarNull()))
                    else:
                        raise StarTypeError(f"Cannot index into '{target.type_name}'.", inst.location)

                elif op == OpCode.INDEX_SET:
                    val = self.stack.pop()
                    idx = self.stack.pop()
                    target = self.stack.pop()
                    if isinstance(target, StarList):
                        target.elements[int(idx.value)] = val
                    elif isinstance(target, StarMap):
                        key = idx.value if isinstance(idx, (StarInteger, StarDecimal, StarText, StarBoolean)) else idx.to_string()
                        target.entries[key] = val
                    else:
                        raise StarTypeError(f"Cannot assign by index on '{target.type_name}'.", inst.location)

                # Collections
                elif op == OpCode.MAKE_LIST:
                    count = inst.operands[0]
                    elems = [self.stack.pop() for _ in range(count)][::-1]
                    self.stack.append(StarList(elems))

                elif op == OpCode.MAKE_MAP:
                    count = inst.operands[0]
                    pairs = []
                    for _ in range(count):
                        val = self.stack.pop()
                        key_val = self.stack.pop()
                        k = key_val.value if isinstance(key_val, (StarInteger, StarDecimal, StarText, StarBoolean)) else key_val.to_string()
                        pairs.append((k, val))
                    entries = {k: v for k, v in reversed(pairs)}
                    self.stack.append(StarMap(entries))

                # Modules
                elif op == OpCode.USE_MODULE:
                    mod_name = self.module.constants[inst.operands[0]]
                    is_file = bool(inst.operands[1])
                    mod = self.module_manager.load_module(mod_name, is_file, inst.location)
                    if mod.name not in frame.env.bindings:
                        frame.env.define(mod.name, mod, is_constant=True)
                    if mod_name in ("Flutter", "Material", "Cupertino", "Widgets"):
                        for exp_name, exp_val in mod.exports.items():
                            if not exp_name.startswith("_") and exp_name not in frame.env.bindings:
                                frame.env.define(exp_name, exp_val, is_constant=True)

                # Try/Catch
                elif op == OpCode.PUSH_TRY:
                    catch_ip = inst.operands[0]
                    err_var = self.module.constants[inst.operands[1]]
                    frame.try_stack.append((catch_ip, err_var))

                elif op == OpCode.POP_TRY:
                    if frame.try_stack:
                        frame.try_stack.pop()

            except Exception as err:
                if frame.try_stack:
                    catch_ip, err_var = frame.try_stack.pop()
                    frame.ip = catch_ip
                    err_msg = err.message if isinstance(err, StarDiagnosticError) else str(err)
                    frame.env.define(err_var, StarText(err_msg), is_constant=False)
                else:
                    raise err

        return last_val
