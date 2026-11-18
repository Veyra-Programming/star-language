"""
Star Language Runtime Types & Values
Authoritative Reference: STAR_SPEC.md (Section 7 & Section 8)
"""

from typing import Any, List, Dict, Callable, Optional, Tuple
from star_engine.errors import StarTypeError, StarNameError


class StarValue:
    @property
    def type_name(self) -> str:
        return "Value"

    def is_truthy(self) -> bool:
        return True

    def to_string(self) -> str:
        return str(self)


class StarNull(StarValue):
    @property
    def type_name(self) -> str:
        return "Null"

    def is_truthy(self) -> bool:
        return False

    def to_string(self) -> str:
        return "null"

    def __repr__(self) -> str:
        return "null"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, StarNull)


class StarBoolean(StarValue):
    def __init__(self, value: bool):
        self.value = bool(value)

    @property
    def type_name(self) -> str:
        return "Boolean"

    def is_truthy(self) -> bool:
        return self.value

    def to_string(self) -> str:
        return "true" if self.value else "false"

    def __repr__(self) -> str:
        return self.to_string()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, StarBoolean) and self.value == other.value


class StarInteger(StarValue):
    def __init__(self, value: int):
        self.value = int(value)

    @property
    def type_name(self) -> str:
        return "Integer"

    def is_truthy(self) -> bool:
        return True

    def to_string(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, StarInteger):
            return self.value == other.value
        if isinstance(other, StarDecimal):
            return self.value == other.value
        return False


class StarDecimal(StarValue):
    def __init__(self, value: float):
        self.value = float(value)

    @property
    def type_name(self) -> str:
        return "Decimal"

    def is_truthy(self) -> bool:
        return True

    def to_string(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.to_string()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, StarDecimal):
            return self.value == other.value
        if isinstance(other, StarInteger):
            return self.value == other.value
        return False


class StarText(StarValue):
    def __init__(self, value: str):
        self.value = str(value)

    @property
    def type_name(self) -> str:
        return "Text"

    def is_truthy(self) -> bool:
        return True

    def to_string(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f'"{self.value}"'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, StarText) and self.value == other.value


class StarList(StarValue):
    def __init__(self, elements: Optional[List[StarValue]] = None):
        self.elements = list(elements) if elements else []

    @property
    def type_name(self) -> str:
        return "List"

    def is_truthy(self) -> bool:
        return True

    def to_string(self) -> str:
        elems = [e.to_string() if isinstance(e, (StarInteger, StarDecimal, StarBoolean, StarNull)) else repr(e) for e in self.elements]
        return "[" + ", ".join(elems) + "]"

    def __repr__(self) -> str:
        return self.to_string()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, StarList) and self.elements == other.elements


class StarMap(StarValue):
    def __init__(self, entries: Optional[Dict[Any, StarValue]] = None):
        self.entries = dict(entries) if entries else {}

    @property
    def type_name(self) -> str:
        return "Map"

    def is_truthy(self) -> bool:
        return True

    def to_string(self) -> str:
        parts = [f'"{k}": {v.to_string()}' if isinstance(k, str) else f"{k}: {v.to_string()}" for k, v in self.entries.items()]
        return "{" + ", ".join(parts) + "}"

    def __repr__(self) -> str:
        return self.to_string()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, StarMap) and self.entries == other.entries

    def get(self, key: Any, default: Any = None) -> StarValue:
        return self.entries.get(key, default if isinstance(default, StarValue) else (to_star_value(default) if default is not None else StarNull()))

    def __getitem__(self, key: Any) -> StarValue:
        return self.entries[key]

    def __contains__(self, key: Any) -> bool:
        return key in self.entries


class StarFunction(StarValue):
    def __init__(self, name: str, parameters: List[str], body: Any, closure_env: Any):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure_env = closure_env

    @property
    def type_name(self) -> str:
        return "Function"

    def call(self, args: Optional[List[Any]] = None) -> "StarValue":
        from star_engine.interpreter import Interpreter, ReturnJump
        from star_engine.environment import Environment
        interp = Interpreter(filename=getattr(self, "filename", "<anon>"))
        call_args = [to_star_value(a) for a in (args or [])]
        func_env = Environment(parent=self.closure_env)
        for param_name, arg_val in zip(self.parameters, call_args):
            func_env.define(param_name, arg_val, is_constant=False)
        try:
            for s in self.body:
                interp.execute(s, func_env)
        except ReturnJump as r:
            return r.value
        return StarNull()

    def __call__(self, *args: Any) -> "StarValue":
        return self.call(list(args))

    def to_string(self) -> str:
        return f"<function {self.name}({', '.join(self.parameters)})>"

    def __repr__(self) -> str:
        return self.to_string()


class StarBuiltinFunction(StarValue):
    def __init__(self, name: str, fn: Callable[..., StarValue]):
        self.name = name
        self.fn = fn

    @property
    def type_name(self) -> str:
        return "Function"

    def call(self, args: Optional[List[Any]] = None) -> StarValue:
        star_args = [to_star_value(a) for a in (args or [])]
        return self.fn(*star_args)

    def __call__(self, *args: Any, **kwargs: Any) -> StarValue:
        star_args = [to_star_value(a) for a in args]
        return self.fn(*star_args)

    def to_string(self) -> str:
        return f"<built-in function {self.name}>"

    def __repr__(self) -> str:
        return self.to_string()


class StarClass(StarValue):
    def __init__(self, name: str, property_names: List[str], property_defaults: Dict[str, Any], methods: Dict[str, Any], closure_env: Any, is_durable: bool = False):
        self.name = name
        self.property_names = property_names
        self.property_defaults = property_defaults
        self.methods = methods
        self.closure_env = closure_env
        self.is_durable = is_durable

    @property
    def type_name(self) -> str:
        return "Class"

    def to_string(self) -> str:
        return f"<class {self.name}>"

    def __repr__(self) -> str:
        return self.to_string()


class StarInstance(StarValue):
    def __init__(self, star_class: StarClass, fields: Optional[Dict[str, StarValue]] = None):
        self.star_class = star_class
        self.fields: Dict[str, StarValue] = fields if fields is not None else {}

    @property
    def type_name(self) -> str:
        return self.star_class.name

    def get(self, name: str) -> StarValue:
        if name in self.fields:
            return self.fields[name]
        if name in self.star_class.methods:
            method_ast = self.star_class.methods[name]
            return StarMethod(instance=self, method_ast=method_ast, closure_env=self.star_class.closure_env)
        if name == "odcs_hash":
            import hashlib, json
            def _odcs_hash(*args):
                canonical = {k: v.to_string() for k, v in sorted(self.fields.items())}
                raw = json.dumps(canonical, sort_keys=True)
                return StarText(hashlib.sha256(raw.encode("utf-8")).hexdigest())
            return StarBuiltinFunction("odcs_hash", _odcs_hash)
        raise StarNameError(f"Unknown property or method '{name}' on '{self.star_class.name}'.", None, f"Available properties: {', '.join(self.star_class.property_names)}")

    def set(self, name: str, value: StarValue):
        if getattr(self.star_class, "is_durable", False):
            raise StarRuntimeError(f"ContinuityImmutabilityError: Durable record '{self.star_class.name}' is immutable. Field '{name}' cannot be modified.", None, "Durable records cannot be modified after creation.")
        if name not in self.star_class.property_names:
            raise StarNameError(f"Cannot set undefined property '{name}' on class '{self.star_class.name}'.", None, f"Declare `property {name}` in class '{self.star_class.name}' before assigning.")
        self.fields[name] = value

    def to_string(self) -> str:
        field_strs = [f"{k} = {v.to_string()}" for k, v in self.fields.items()]
        return f"{self.star_class.name}({', '.join(field_strs)})"

    def __repr__(self) -> str:
        return self.to_string()


class StarMethod(StarValue):
    def __init__(self, instance: StarInstance, method_ast: Any, closure_env: Any):
        self.instance = instance
        self.method_ast = method_ast
        self.closure_env = closure_env

    @property
    def type_name(self) -> str:
        return "Method"

    def to_string(self) -> str:
        return f"<method {self.method_ast.name} on {self.instance.star_class.name}>"

    def __repr__(self) -> str:
        return self.to_string()


class StarVirtualNode(StarValue):
    def __init__(self, tag: str, props: Optional[Dict[str, Any]] = None, children: Optional[List[Any]] = None, listeners: Optional[Dict[str, Any]] = None):
        self.tag = tag
        self.props = props if props is not None else {}
        self.children = children if children is not None else []
        self.listeners = listeners if listeners is not None else {}

    @property
    def type_name(self) -> str:
        return "VirtualNode"

    def to_string(self) -> str:
        child_str = f" [{len(self.children)} children]" if self.children else ""
        return f"<{self.tag}{child_str}>"

    def __repr__(self) -> str:
        return self.to_string()


class StarReactiveState:
    def __init__(self, name: str, initial_value: StarValue):
        self.name = name
        self._value = initial_value
        self.listeners: List[Callable[[StarValue, StarValue], None]] = []

    @property
    def value(self) -> StarValue:
        return self._value

    def set_value(self, new_value: StarValue):
        old_value = self._value
        if old_value != new_value:
            self._value = new_value
            for listener in list(self.listeners):
                listener(new_value, old_value)


class StarComponent(StarValue):
    def __init__(self, name: str, state_decls: List[Any], computed_decls: List[Any], watch_decls: List[Any], event_decls: List[Any], methods: Dict[str, Any], render_decl: Any, closure_env: Any):
        self.name = name
        self.state_decls = state_decls
        self.computed_decls = computed_decls
        self.watch_decls = watch_decls
        self.event_decls = event_decls
        self.methods = methods
        self.render_decl = render_decl
        self.closure_env = closure_env

    @property
    def type_name(self) -> str:
        return "Component"

    def to_string(self) -> str:
        return f"<component {self.name}>"

    def __repr__(self) -> str:
        return self.to_string()


class StarComponentInstance(StarValue):
    def __init__(self, component: StarComponent, props: Optional[Dict[str, StarValue]] = None):
        self.component = component
        self.props = props if props is not None else {}
        self.state: Dict[str, StarReactiveState] = {}
        self.computed_cache: Dict[str, StarValue] = {}
        self.computed_dirty: Dict[str, bool] = {}
        self.current_vdom: Optional[StarVirtualNode] = None
        self.on_reconcile: Optional[Callable[['StarComponentInstance', Optional[StarVirtualNode]], None]] = None

    @property
    def type_name(self) -> str:
        return self.component.name

    def get_state(self, name: str) -> StarValue:
        if name in self.state:
            return self.state[name].value
        if name in self.props:
            return self.props[name]
        raise StarNameError(f"Unknown state or prop '{name}' on component '{self.component.name}'.")

    def set_state(self, name: str, value: StarValue):
        if name in self.state:
            self.state[name].set_value(value)
            for c_name in self.computed_dirty:
                self.computed_dirty[c_name] = True
            if self.on_reconcile:
                self.on_reconcile(self, self.current_vdom)
        else:
            self.state[name] = StarReactiveState(name, value)

    def to_string(self) -> str:
        state_strs = [f"{k}={v.value.to_string()}" for k, v in self.state.items()]
        return f"{self.component.name}({', '.join(state_strs)})"

    def __repr__(self) -> str:
        return self.to_string()


class StarModule(StarValue):
    def __init__(self, name: str, exports: Dict[str, StarValue]):
        self.name = name
        self.exports = exports

    @property
    def type_name(self) -> str:
        return "Module"

    def get(self, name: str) -> StarValue:
        if name in self.exports:
            return self.exports[name]
        raise StarNameError(f"Module '{self.name}' has no member '{name}'.")

    def __getitem__(self, name: str) -> StarValue:
        return self.get(name)

    def __getattr__(self, name: str) -> Any:
        if "exports" in self.__dict__ and name in self.exports:
            val = self.exports[name]
            if isinstance(val, StarBuiltinFunction):
                def _caller(*args, **kwargs):
                    star_args = [to_star_value(a) for a in args]
                    return val.fn(*star_args)
                return _caller
            return val
        raise AttributeError(f"Module '{self.name}' has no attribute '{name}'.")

    def to_string(self) -> str:
        return f"<module '{self.name}'>"

    def __repr__(self) -> str:
        return self.to_string()


# Value conversion helpers
def to_star_value(val: Any) -> StarValue:
    if val is None or isinstance(val, StarNull):
        return StarNull()
    if isinstance(val, bool):
        return StarBoolean(val)
    if isinstance(val, int):
        return StarInteger(val)
    if isinstance(val, float):
        return StarDecimal(val)
    if isinstance(val, str):
        return StarText(val)
    if isinstance(val, list):
        return StarList([to_star_value(x) for x in val])
    if isinstance(val, dict):
        return StarMap({k: to_star_value(v) for k, v in val.items()})
    if isinstance(val, StarValue):
        return val
    return StarText(str(val))


def from_star_value(val: Any) -> Any:
    if isinstance(val, StarNull) or val is None:
        return None
    if isinstance(val, StarBoolean):
        return val.value
    if isinstance(val, (StarInteger, StarDecimal)):
        return val.value
    if isinstance(val, StarText):
        return val.value
    if isinstance(val, StarList):
        return [from_star_value(x) for x in val.elements]
    if isinstance(val, StarMap):
        return {k: from_star_value(v) for k, v in val.entries.items()}
    if isinstance(val, StarValue):
        return val.to_string()
    return val
