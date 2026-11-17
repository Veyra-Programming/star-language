"""
Star Runtime Subsystem & ABI
Version 0.4.0
"""

from star_runtime.abi import ABI_VERSION, LANGUAGE_VERSION, BYTECODE_VERSION, IR_VERSION, TypeTag
from star_runtime.ffi import create_ffi_module, NativeLibraryHandle, NativeFunctionWrapper
from star_runtime.packages import PackageManager, Lockfile, Dependency
