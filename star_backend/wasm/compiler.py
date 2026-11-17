"""
Star IR to WebAssembly (WASM) Compiler
Authoritative Reference: STAR_WEB.md
"""

from typing import List, Dict, Any, Optional, Tuple
from star_engine.ir import OpCode, Instruction, IRModule, IRFunction
from star_backend.wasm.emitter import WasmEmitter, encode_i32_leb128, encode_i64_leb128, encode_u32_leb128


class WasmCompiler:
    def __init__(self, ir_module: IRModule):
        self.ir_module = ir_module
        self.emitter = WasmEmitter()
        self.string_table: Dict[str, Tuple[int, int]] = {}  # str -> (offset, length)
        self.current_memory_offset = 1024

    def compile(self) -> bytes:
        # 1. Setup string table in linear memory data section
        for c in self.ir_module.constants:
            if isinstance(c, str):
                encoded = c.encode("utf-8")
                offset = self.current_memory_offset
                self.emitter.add_data(offset, encoded)
                self.string_table[c] = (offset, len(encoded))
                self.current_memory_offset += len(encoded) + 4

        # 2. Add Host Imports (Star Web Runtime ABI)
        # i32 = 0x7F, i64 = 0x7E, f64 = 0x7C
        self.import_show = self.emitter.add_import_func("star_env", "star_show", [0x7F, 0x7F], [])  # (ptr, len) -> void
        self.import_ui_title = self.emitter.add_import_func("star_env", "star_ui_title", [0x7F, 0x7F], [])
        self.import_ui_text = self.emitter.add_import_func("star_env", "star_ui_text", [0x7F, 0x7F], [])
        self.import_ui_button = self.emitter.add_import_func("star_env", "star_ui_button", [0x7F, 0x7F, 0x7F], [])  # (ptr, len, callback_id)
        self.import_ui_column = self.emitter.add_import_func("star_env", "star_ui_column", [0x7F], [])  # (child_count)
        self.import_ui_card = self.emitter.add_import_func("star_env", "star_ui_card", [0x7F], [])
        self.import_time_now = self.emitter.add_import_func("star_env", "star_time_now", [], [0x7C])  # () -> f64

        # 3. Compile Main Instructions to WASM bytecode
        main_body = self._compile_instruction_block(self.ir_module.instructions)
        self.emitter.add_function([], [], main_body, export_name="main")

        return self.emitter.emit_binary()

    def _compile_instruction_block(self, instructions: List[Instruction]) -> bytes:
        body = bytearray()
        # Local variables: 0 locals declared at function level for this prototype block
        body.append(0x00)  # local count: 0

        for inst in instructions:
            op = inst.opcode

            if op == OpCode.CONST:
                val = self.ir_module.constants[inst.operands[0]]
                if isinstance(val, int):
                    body.append(0x42)  # i64.const
                    body.extend(encode_i64_leb128(val))
                elif isinstance(val, str):
                    offset, length = self.string_table.get(val, (0, 0))
                    body.append(0x41)  # i32.const offset
                    body.extend(encode_i32_leb128(offset))
                    body.append(0x41)  # i32.const length
                    body.extend(encode_i32_leb128(length))
                else:
                    body.append(0x42)  # i64.const 0
                    body.extend(encode_i64_leb128(0))

            elif op == OpCode.ADD:
                body.append(0x7C)  # i64.add

            elif op == OpCode.SUB:
                body.append(0x7D)  # i64.sub

            elif op == OpCode.MUL:
                body.append(0x7E)  # i64.mul

            elif op == OpCode.DIV:
                body.append(0x7F)  # i64.div_s

            elif op == OpCode.CALL_BUILTIN:
                name = self.ir_module.constants[inst.operands[0]]
                if name == "show":
                    body.append(0x10)  # call
                    body.extend(encode_u32_leb128(self.import_show))

            elif op == OpCode.POP:
                body.append(0x1A)  # drop

            elif op == OpCode.RETURN_NULL or op == OpCode.RETURN_VAL:
                body.append(0x0F)  # return

        body.append(0x0B)  # end opcode for function body
        return bytes(body)
