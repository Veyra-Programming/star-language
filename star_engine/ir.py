"""
Star Language Intermediate Representation (Star IR) Data Structures & Opcodes
Authoritative Reference: STAR_IR.md
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from star_engine.tokens import SourceLocation


class OpCode(Enum):
    # --- Tier 1: Core VM Opcodes ---
    CONST = auto()             # CONST <const_idx>
    POP = auto()               # POP
    DUP = auto()               # DUP

    # Variables & Scopes
    DEFINE_VAR = auto()        # DEFINE_VAR <name_idx>
    DEFINE_CONST = auto()      # DEFINE_CONST <name_idx>
    LOAD_VAR = auto()          # LOAD_VAR <name_idx>
    STORE_VAR = auto()         # STORE_VAR <name_idx>
    LOAD_SELF = auto()         # LOAD_SELF

    # Arithmetic & Unary
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    NEG = auto()
    NOT = auto()

    # Comparisons
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # Control Flow
    JUMP = auto()              # JUMP <target_ip>
    JUMP_IF_FALSE = auto()     # JUMP_IF_FALSE <target_ip>
    JUMP_IF_TRUE = auto()      # JUMP_IF_TRUE <target_ip>

    # Calls & Return
    CALL = auto()              # CALL <arg_count>
    CALL_BUILTIN = auto()      # CALL_BUILTIN <name_idx> <arg_count>
    RETURN_VAL = auto()        # RETURN_VAL
    RETURN_NULL = auto()       # RETURN_NULL

    # --- Tier 2: Runtime ABI Opcodes ---
    MAKE_FUNCTION = auto()     # MAKE_FUNCTION <func_idx>
    MAKE_CLASS = auto()        # MAKE_CLASS <class_idx>
    MAKE_COMPONENT = auto()    # MAKE_COMPONENT <comp_idx>
    NEW_INSTANCE = auto()      # NEW_INSTANCE <class_name_idx> <named_count> <pos_count>
    GET_PROP = auto()          # GET_PROP <name_idx>
    SET_PROP = auto()          # SET_PROP <name_idx>

    # Reactivity & UI
    DEFINE_STATE = auto()      # DEFINE_STATE <name_idx>
    DEFINE_COMPUTED = auto()   # DEFINE_COMPUTED <name_idx>
    BIND_WATCH = auto()        # BIND_WATCH <target_idx>
    EMIT_EVENT = auto()        # EMIT_EVENT <name_idx> <arg_count>
    RENDER_TREE = auto()       # RENDER_TREE

    # Collections
    MAKE_LIST = auto()         # MAKE_LIST <count>
    MAKE_MAP = auto()          # MAKE_MAP <entry_count>
    INDEX_GET = auto()         # INDEX_GET
    INDEX_SET = auto()         # INDEX_SET

    # Modules & Errors
    USE_MODULE = auto()        # USE_MODULE <name_idx> <is_file>
    PUSH_TRY = auto()          # PUSH_TRY <catch_ip> <err_var_idx>
    POP_TRY = auto()           # POP_TRY


@dataclass
class Instruction:
    opcode: OpCode
    operands: List[Any] = field(default_factory=list)
    location: Optional[SourceLocation] = None

    def __str__(self) -> str:
        ops = ", ".join(str(o) for o in self.operands)
        return f"{self.opcode.name:<16} {ops}" if ops else self.opcode.name


@dataclass
class IRFunction:
    name: str
    parameters: List[str]
    instructions: List[Instruction] = field(default_factory=list)


@dataclass
class IRClass:
    name: str
    properties: List[str]
    methods: Dict[str, IRFunction] = field(default_factory=dict)
    defaults: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IRComponent:
    name: str
    states: List[str] = field(default_factory=list)
    computeds: Dict[str, IRFunction] = field(default_factory=dict)
    watchers: Dict[str, IRFunction] = field(default_factory=dict)
    events: List[str] = field(default_factory=list)
    methods: Dict[str, IRFunction] = field(default_factory=dict)
    render: Optional[IRFunction] = None


@dataclass
class IRModule:
    filename: str
    constants: List[Any] = field(default_factory=list)
    functions: Dict[str, IRFunction] = field(default_factory=dict)
    classes: Dict[str, IRClass] = field(default_factory=dict)
    components: Dict[str, IRComponent] = field(default_factory=dict)
    instructions: List[Instruction] = field(default_factory=list)

    def add_constant(self, val: Any) -> int:
        for idx, c in enumerate(self.constants):
            if c == val and type(c) == type(val):
                return idx
        self.constants.append(val)
        return len(self.constants) - 1

    def serialize(self) -> bytes:
        from star_engine.compiler import StarCompiler
        compiler = StarCompiler(filename=self.filename)
        compiler.module = self
        return compiler.serialize_bytecode()

    @staticmethod
    def deserialize(blob: bytes) -> "IRModule":
        from star_engine.compiler import StarCompiler
        return StarCompiler.deserialize_bytecode(blob)

    def disassemble(self) -> str:
        lines = []
        lines.append(f"=== Star IR Module: {self.filename} ===")
        lines.append(f"Format Version: 1 | Language: Star 0.3")
        lines.append(f"Constants ({len(self.constants)}):")
        for i, c in enumerate(self.constants):
            lines.append(f"  [{i:>2}] {repr(c)}")
        lines.append("")

        if self.classes:
            lines.append(f"Classes ({len(self.classes)}):")
            for c_name, c_def in self.classes.items():
                lines.append(f"  Class '{c_name}' (properties: {', '.join(c_def.properties)}):")
                for m_name, m_fn in c_def.methods.items():
                    lines.append(f"    Method '{m_name}'({', '.join(m_fn.parameters)}):")
                    for ip, inst in enumerate(m_fn.instructions):
                        lines.append(f"      {ip:04d}  {inst}")
            lines.append("")

        if self.components:
            lines.append(f"Components ({len(self.components)}):")
            for comp_name, comp_def in self.components.items():
                lines.append(f"  Component '{comp_name}' (states: {', '.join(comp_def.states)}):")
                for c_name, c_fn in comp_def.computeds.items():
                    lines.append(f"    Computed '{c_name}':")
                    for ip, inst in enumerate(c_fn.instructions):
                        lines.append(f"      {ip:04d}  {inst}")
                if comp_def.render:
                    lines.append(f"    Render:")
                    for ip, inst in enumerate(comp_def.render.instructions):
                        lines.append(f"      {ip:04d}  {inst}")
            lines.append("")

        if self.functions:
            lines.append(f"Functions ({len(self.functions)}):")
            for f_name, f_def in self.functions.items():
                lines.append(f"  Function '{f_name}'({', '.join(f_def.parameters)}):")
                for ip, inst in enumerate(f_def.instructions):
                    lines.append(f"    {ip:04d}  {inst}")
            lines.append("")

        lines.append(f"Main Entry Instructions ({len(self.instructions)}):")
        for ip, inst in enumerate(self.instructions):
            lines.append(f"  {ip:04d}  {inst}")

        return "\n".join(lines)


# Alias CompiledModule to IRModule for mobile/runtime compatibility
CompiledModule = IRModule
