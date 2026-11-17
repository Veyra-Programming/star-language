"""
Star Language Controlled FFI Unit Tests
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from star_runtime.ffi import create_ffi_module
from star_engine.types import StarText, StarInteger, StarList
from star_engine.errors import StarRuntimeError


class TestFFI(unittest.TestCase):
    def test_ffi_load_c_library(self):
        ffi_mod = create_ffi_module(allow_native=True)
        load_fn = ffi_mod.get("load")
        c_lib = load_fn(StarText("c"))
        self.assertIsNotNone(c_lib)

    def test_ffi_disallowed_capability_raises_error(self):
        ffi_mod = create_ffi_module(allow_native=False)
        load_fn = ffi_mod.get("load")
        with self.assertRaises(StarRuntimeError):
            load_fn(StarText("c"))


if __name__ == "__main__":
    unittest.main()
