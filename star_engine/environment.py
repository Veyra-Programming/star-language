"""
Star Language Lexical Environment & Scope Management
Authoritative Reference: STAR_SPEC.md (Section 6)
"""

from typing import Dict, Tuple, Optional, Any
from star_engine.tokens import SourceLocation
from star_engine.errors import StarNameError
from star_engine.types import StarValue


class Environment:
    def __init__(self, parent: Optional["Environment"] = None):
        self.parent = parent
        # Map: name -> (StarValue, is_constant: bool)
        self.bindings: Dict[str, Tuple[StarValue, bool]] = {}

    def define(self, name: str, value: StarValue, is_constant: bool = False, location: Optional[SourceLocation] = None, source_code: Optional[str] = None):
        if name in self.bindings:
            _, was_const = self.bindings[name]
            if was_const:
                raise StarNameError(
                    f"Cannot redefine constant '{name}' in the same scope.",
                    location,
                    f"Use a different name or declare '{name}' with 'variable' if it needs to change.",
                    source_code
                )
        self.bindings[name] = (value, is_constant)

    def assign(self, name: str, value: StarValue, location: Optional[SourceLocation] = None, source_code: Optional[str] = None):
        if name in self.bindings:
            _, is_const = self.bindings[name]
            if is_const:
                raise StarNameError(
                    f"Cannot reassign immutable constant '{name}'.",
                    location,
                    f"'{name}' was declared with 'constant'. Use 'variable' if you need to reassign it.",
                    source_code
                )
            self.bindings[name] = (value, False)
            return

        if self.parent is not None:
            curr = self.parent
            while curr is not None:
                if name in curr.bindings:
                    curr.assign(name, value, location, source_code)
                    return
                curr = curr.parent
            self.define(name, value, is_constant=False, location=location, source_code=source_code)
            return

        self.define(name, value, is_constant=False, location=location, source_code=source_code)

    def lookup(self, name: str, location: Optional[SourceLocation] = None, source_code: Optional[str] = None) -> StarValue:
        if name in self.bindings:
            return self.bindings[name][0]

        if self.parent is not None:
            return self.parent.lookup(name, location, source_code)

        raise StarNameError(
            f"Undefined identifier '{name}'.",
            location,
            f"Make sure '{name}' is declared and spelled correctly.",
            source_code
        )

    def is_defined(self, name: str) -> bool:
        if name in self.bindings:
            return True
        if self.parent:
            return self.parent.is_defined(name)
        return False

    def get(self, name: str, default: Optional[StarValue] = None) -> Optional[StarValue]:
        try:
            return self.lookup(name)
        except StarNameError:
            return default

    def __getitem__(self, name: str) -> StarValue:
        return self.lookup(name)
