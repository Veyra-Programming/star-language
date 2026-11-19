"""
Star OmniEngine 2.0 GN — Zero-Cost Polyglot FFI & Native Dynamic Binding
Authoritative Reference: STAR_OMNI_SPEC.md
"""

import ctypes
import os
import sys
from typing import Dict, Any, Optional, List, Callable


class NativeFunctionWrapper:
    """Wraps a native C symbol with automatic type marshaling and error safety."""
    def __init__(self, name: str, c_func: Any, arg_types: Optional[List[Any]] = None, restype: Optional[Any] = None):
        self.name = name
        self.c_func = c_func
        if arg_types:
            self.c_func.argtypes = arg_types
        if restype:
            self.c_func.restype = restype

    def __call__(self, *args) -> Any:
        try:
            return self.c_func(*args)
        except Exception as err:
            raise RuntimeError(f"Native FFI call to '{self.name}' failed: {err}")


class PolyglotFFIEngine:
    """
    Zero-overhead FFI engine connecting Star to native C/C++, Rust, and system libraries.
    """
    def __init__(self):
        self.loaded_libraries: Dict[str, ctypes.CDLL] = {}
        self._init_standard_c_library()

    def _init_standard_c_library(self):
        # Platform-specific standard C runtime
        try:
            if sys.platform == "win32":
                self.libc = ctypes.cdll.msvcrt
            elif sys.platform == "darwin":
                self.libc = ctypes.CDLL("libc.dylib")
            else:
                self.libc = ctypes.CDLL("libc.so.6")
            self.loaded_libraries["libc"] = self.libc
        except Exception:
            self.libc = None

    def load_library(self, lib_path: str, alias: Optional[str] = None) -> ctypes.CDLL:
        name = alias or os.path.basename(lib_path)
        if name in self.loaded_libraries:
            return self.loaded_libraries[name]

        if not os.path.exists(lib_path) and not os.path.isabs(lib_path):
            # Try system loader
            lib = ctypes.CDLL(lib_path)
        else:
            lib = ctypes.CDLL(os.path.abspath(lib_path))

        self.loaded_libraries[name] = lib
        return lib

    def bind_function(
        self,
        lib_name: str,
        func_name: str,
        arg_types: Optional[List[Any]] = None,
        restype: Optional[Any] = None
    ) -> NativeFunctionWrapper:
        lib = self.loaded_libraries.get(lib_name)
        if not lib:
            raise ValueError(f"Native library '{lib_name}' is not loaded.")

        if not hasattr(lib, func_name):
            raise AttributeError(f"Symbol '{func_name}' not found in library '{lib_name}'.")

        c_fn = getattr(lib, func_name)
        return NativeFunctionWrapper(func_name, c_fn, arg_types, restype)

    def stats(self) -> Dict[str, Any]:
        return {
            "loaded_libraries": list(self.loaded_libraries.keys()),
            "libc_available": self.libc is not None,
            "platform": sys.platform,
        }
