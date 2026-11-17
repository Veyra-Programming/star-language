"""
Star Controlled Foreign Function Interface (FFI)
Authoritative Reference: STAR_RUNTIME.md (Section 4)
"""

import ctypes
import sys
import os
from typing import List, Dict, Any, Optional, Callable
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal, StarText, StarBuiltinFunction, StarModule
)
from star_engine.errors import StarRuntimeError, StarTypeError, StarValueError


class NativeFunctionWrapper(StarValue):
    def __init__(self, func_name: str, c_func: Any, param_types: List[str], return_type: str):
        self.func_name = func_name
        self.c_func = c_func
        self.param_types = param_types
        self.return_type = return_type

    @property
    def type_name(self) -> str:
        return "NativeFunction"

    def to_string(self) -> str:
        return f"<native function '{self.func_name}'>"

    def __repr__(self) -> str:
        return self.to_string()

    def __call__(self, *args: StarValue) -> StarValue:
        if len(args) != len(self.param_types):
            raise StarTypeError(
                f"Native function '{self.func_name}' expects {len(self.param_types)} arguments, got {len(args)}."
            )

        c_args = []
        for i, (arg, p_type) in enumerate(zip(args, self.param_types)):
            if p_type == "Text":
                if not isinstance(arg, StarText):
                    raise StarTypeError(f"Argument {i+1} to '{self.func_name}' must be Text.")
                c_args.append(arg.value.encode("utf-8"))
            elif p_type == "Integer":
                if not isinstance(arg, StarInteger):
                    raise StarTypeError(f"Argument {i+1} to '{self.func_name}' must be Integer.")
                c_args.append(int(arg.value))
            elif p_type == "Decimal":
                if not isinstance(arg, (StarInteger, StarDecimal)):
                    raise StarTypeError(f"Argument {i+1} to '{self.func_name}' must be Decimal.")
                c_args.append(float(arg.value))
            elif p_type == "Boolean":
                if not isinstance(arg, StarBoolean):
                    raise StarTypeError(f"Argument {i+1} to '{self.func_name}' must be Boolean.")
                c_args.append(bool(arg.value))
            else:
                raise StarTypeError(f"Unsupported FFI parameter type '{p_type}'.")

        try:
            res = self.c_func(*c_args)
        except Exception as e:
            raise StarRuntimeError(f"Native execution error in '{self.func_name}': {e}")

        if self.return_type == "Integer":
            return StarInteger(int(res))
        elif self.return_type == "Decimal":
            return StarDecimal(float(res))
        elif self.return_type == "Boolean":
            return StarBoolean(bool(res))
        elif self.return_type == "Text":
            if isinstance(res, bytes):
                return StarText(res.decode("utf-8"))
            return StarText(str(res) if res is not None else "")
        elif self.return_type in ("Null", "Void", None):
            return StarNull()

        return StarNull()


class NativeLibraryHandle(StarValue):
    def __init__(self, lib_name: str, c_lib: Any):
        self.lib_name = lib_name
        self.c_lib = c_lib

    @property
    def type_name(self) -> str:
        return "NativeLibrary"

    def to_string(self) -> str:
        return f"<native library '{self.lib_name}'>"

    def __repr__(self) -> str:
        return self.to_string()

    def bind(self, func_name: str, param_types: List[str], return_type: str) -> NativeFunctionWrapper:
        try:
            c_func = getattr(self.c_lib, func_name)
        except AttributeError:
            raise StarNameError(f"Symbol '{func_name}' not found in native library '{self.lib_name}'.")

        # Configure ctypes argtypes
        c_argtypes = []
        for pt in param_types:
            if pt == "Text":
                c_argtypes.append(ctypes.c_char_p)
            elif pt == "Integer":
                c_argtypes.append(ctypes.c_int64)
            elif pt == "Decimal":
                c_argtypes.append(ctypes.c_double)
            elif pt == "Boolean":
                c_argtypes.append(ctypes.c_bool)
            else:
                raise StarTypeError(f"Unsupported FFI parameter type '{pt}'.")
        c_func.argtypes = c_argtypes

        # Configure ctypes restype
        if return_type == "Integer":
            c_func.restype = ctypes.c_int64
        elif return_type == "Decimal":
            c_func.restype = ctypes.c_double
        elif return_type == "Boolean":
            c_func.restype = ctypes.c_bool
        elif return_type == "Text":
            c_func.restype = ctypes.c_char_p
        elif return_type in ("Null", "Void", None):
            c_func.restype = None

        return NativeFunctionWrapper(func_name, c_func, param_types, return_type)


def create_ffi_module(allow_native: bool = True) -> StarModule:
    exports: Dict[str, StarValue] = {}

    def _ffi_load(*args: StarValue) -> StarValue:
        if not allow_native:
            raise StarRuntimeError("Native FFI capability is not enabled for this project.")

        if len(args) < 1 or not isinstance(args[0], StarText):
            raise StarTypeError("FFI.load() requires library name Text.")

        lib_name = args[0].value
        try:
            if lib_name in ("c", "libc"):
                if sys.platform == "win32":
                    c_lib = ctypes.cdll.msvcrt
                else:
                    c_lib = ctypes.CDLL(None)
            else:
                c_lib = ctypes.CDLL(lib_name)
            
            handle = NativeLibraryHandle(lib_name, c_lib)
            
            # Helper method to bind
            def _bind(*b_args: StarValue) -> StarValue:
                if len(b_args) != 3 or not isinstance(b_args[0], StarText) or not isinstance(b_args[1], StarList) or not isinstance(b_args[2], StarText):
                    raise StarTypeError("bind() expects (func_name: Text, param_types: List, return_type: Text).")
                fn_name = b_args[0].value
                p_types = [t.to_string() if isinstance(t, StarText) else str(t) for t in b_args[1].elements]
                r_type = b_args[2].value
                native_fn = handle.bind(fn_name, p_types, r_type)
                return StarBuiltinFunction(fn_name, native_fn.__call__)

            exports_handle = {
                "bind": StarBuiltinFunction("bind", _bind)
            }
            return StarModule(f"NativeLib_{lib_name}", exports_handle)

        except Exception as e:
            raise StarRuntimeError(f"Could not load native library '{lib_name}': {e}")

    exports["load"] = StarBuiltinFunction("load", _ffi_load)
    return StarModule("FFI", exports)
