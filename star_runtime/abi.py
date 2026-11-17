"""
Star Runtime ABI Definitions & Versioning
Authoritative Reference: STAR_RUNTIME.md
"""

from enum import IntEnum

ABI_VERSION = 1
LANGUAGE_VERSION = "0.4.0"
BYTECODE_VERSION = 1
IR_VERSION = 1


class TypeTag(IntEnum):
    NULL = 0x00
    BOOLEAN = 0x01
    INTEGER = 0x02
    DECIMAL = 0x03
    TEXT = 0x04
    LIST = 0x05
    MAP = 0x06
    FUNCTION = 0x07
    CLASS = 0x08
    INSTANCE = 0x09
    MODULE = 0x0A
    NATIVE_HANDLE = 0x0B
