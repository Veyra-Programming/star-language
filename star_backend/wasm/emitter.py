"""
Star WebAssembly Binary Emitter
Authoritative Reference: STAR_WEB.md (Section 2)
"""

import struct
from typing import List, Dict, Any, Optional, Tuple


def encode_u32_leb128(val: int) -> bytes:
    res = bytearray()
    while True:
        byte = val & 0x7F
        val >>= 7
        if val == 0:
            res.append(byte)
            break
        else:
            res.append(byte | 0x80)
    return bytes(res)


def encode_i32_leb128(val: int) -> bytes:
    res = bytearray()
    more = True
    while more:
        byte = val & 0x7F
        val >>= 7
        if (val == 0 and not (byte & 0x40)) or (val == -1 and (byte & 0x40)):
            more = False
        else:
            byte |= 0x80
        res.append(byte)
    return bytes(res)


def encode_i64_leb128(val: int) -> bytes:
    res = bytearray()
    more = True
    while more:
        byte = val & 0x7F
        val >>= 7
        if (val == 0 and not (byte & 0x40)) or (val == -1 and (byte & 0x40)):
            more = False
        else:
            byte |= 0x80
        res.append(byte)
    return bytes(res)


class WasmSection:
    CUSTOM = 0
    TYPE = 1
    IMPORT = 2
    FUNCTION = 3
    TABLE = 4
    MEMORY = 5
    GLOBAL = 6
    EXPORT = 7
    START = 8
    ELEMENT = 9
    CODE = 10
    DATA = 11


class WasmEmitter:
    def __init__(self):
        self.types: List[Tuple[List[int], List[int]]] = []  # (param_types, return_types)
        self.imports: List[Tuple[str, str, int, int]] = []  # (mod, name, kind, type_idx)
        self.functions: List[int] = []  # type_indices for defined functions
        self.exports: List[Tuple[str, int, int]] = []  # (name, kind, index)
        self.code_bodies: List[bytes] = []
        self.data_segments: List[Tuple[int, bytes]] = []  # (offset, bytes)
        self.memory_pages = 1

    def add_type(self, params: List[int], returns: List[int]) -> int:
        entry = (params, returns)
        for i, t in enumerate(self.types):
            if t == entry:
                return i
        self.types.append(entry)
        return len(self.types) - 1

    def add_import_func(self, module: str, name: str, params: List[int], returns: List[int]) -> int:
        type_idx = self.add_type(params, returns)
        idx = len(self.imports)
        self.imports.append((module, name, 0, type_idx))
        return idx

    def add_function(self, params: List[int], returns: List[int], body_bytes: bytes, export_name: Optional[str] = None) -> int:
        type_idx = self.add_type(params, returns)
        func_idx = len(self.imports) + len(self.functions)
        self.functions.append(type_idx)
        self.code_bodies.append(body_bytes)

        if export_name:
            self.exports.append((export_name, 0, func_idx))
        return func_idx

    def add_data(self, offset: int, data: bytes) -> int:
        self.data_segments.append((offset, data))
        return offset

    def emit_binary(self) -> bytes:
        out = bytearray()
        # 1. Magic + Version
        out.extend(b"\x00asm\x01\x00\x00\x00")

        # 2. Type Section
        if self.types:
            type_payload = bytearray()
            type_payload.extend(encode_u32_leb128(len(self.types)))
            for params, returns in self.types:
                type_payload.append(0x60)  # func type form
                type_payload.extend(encode_u32_leb128(len(params)))
                for p in params:
                    type_payload.append(p)
                type_payload.extend(encode_u32_leb128(len(returns)))
                for r in returns:
                    type_payload.append(r)
            out.append(WasmSection.TYPE)
            out.extend(encode_u32_leb128(len(type_payload)))
            out.extend(type_payload)

        # 3. Import Section
        if self.imports:
            imp_payload = bytearray()
            imp_payload.extend(encode_u32_leb128(len(self.imports)))
            for mod, name, kind, type_idx in self.imports:
                mod_b = mod.encode("utf-8")
                imp_payload.extend(encode_u32_leb128(len(mod_b)))
                imp_payload.extend(mod_b)
                name_b = name.encode("utf-8")
                imp_payload.extend(encode_u32_leb128(len(name_b)))
                imp_payload.extend(name_b)
                imp_payload.append(kind)  # 0 = func
                imp_payload.extend(encode_u32_leb128(type_idx))
            out.append(WasmSection.IMPORT)
            out.extend(encode_u32_leb128(len(imp_payload)))
            out.extend(imp_payload)

        # 4. Function Section
        if self.functions:
            fn_payload = bytearray()
            fn_payload.extend(encode_u32_leb128(len(self.functions)))
            for t_idx in self.functions:
                fn_payload.extend(encode_u32_leb128(t_idx))
            out.append(WasmSection.FUNCTION)
            out.extend(encode_u32_leb128(len(fn_payload)))
            out.extend(fn_payload)

        # 5. Memory Section
        mem_payload = bytearray()
        mem_payload.extend(encode_u32_leb128(1))  # 1 memory
        mem_payload.append(0x00)  # flags: min only
        mem_payload.extend(encode_u32_leb128(self.memory_pages))
        out.append(WasmSection.MEMORY)
        out.extend(encode_u32_leb128(len(mem_payload)))
        out.extend(mem_payload)

        # 6. Export Section (Memory + Functions)
        export_list = [("memory", 2, 0)] + self.exports  # kind 2 = memory
        exp_payload = bytearray()
        exp_payload.extend(encode_u32_leb128(len(export_list)))
        for name, kind, idx in export_list:
            name_b = name.encode("utf-8")
            exp_payload.extend(encode_u32_leb128(len(name_b)))
            exp_payload.extend(name_b)
            exp_payload.append(kind)
            exp_payload.extend(encode_u32_leb128(idx))
        out.append(WasmSection.EXPORT)
        out.extend(encode_u32_leb128(len(exp_payload)))
        out.extend(exp_payload)

        # 7. Code Section
        if self.code_bodies:
            code_payload = bytearray()
            code_payload.extend(encode_u32_leb128(len(self.code_bodies)))
            for body in self.code_bodies:
                code_payload.extend(encode_u32_leb128(len(body)))
                code_payload.extend(body)
            out.append(WasmSection.CODE)
            out.extend(encode_u32_leb128(len(code_payload)))
            out.extend(code_payload)

        # 8. Data Section
        if self.data_segments:
            data_payload = bytearray()
            data_payload.extend(encode_u32_leb128(len(self.data_segments)))
            for offset, d_bytes in self.data_segments:
                data_payload.append(0x00)  # memory index 0
                data_payload.append(0x41)  # i32.const
                data_payload.extend(encode_i32_leb128(offset))
                data_payload.append(0x0B)  # end
                data_payload.extend(encode_u32_leb128(len(d_bytes)))
                data_payload.extend(d_bytes)
            out.append(WasmSection.DATA)
            out.extend(encode_u32_leb128(len(data_payload)))
            out.extend(data_payload)

        return bytes(out)
