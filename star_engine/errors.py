"""
Star Language Diagnostic Error Engine
Authoritative Reference: STAR_SPEC.md (Section 9)
"""

from typing import Optional
from star_engine.tokens import SourceLocation


class StarDiagnosticError(Exception):
    def __init__(
        self,
        category: str,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        super().__init__(message)
        self.category = category
        self.message = message
        self.location = location
        self.suggestion = suggestion
        self.source_code = source_code

    def format(self, source_code: Optional[str] = None) -> str:
        src = source_code or self.source_code
        out = [f"\n{self.category}: {self.message}"]

        if self.location:
            out.append(f"File: {self.location.file}")
            out.append(f"Line: {self.location.line}, Column: {self.location.column}")

            if src:
                lines = src.splitlines()
                line_idx = self.location.line - 1
                if 0 <= line_idx < len(lines):
                    source_line = lines[line_idx]
                    out.append("")
                    out.append(f"    {source_line}")
                    col_offset = max(0, self.location.column - 1)
                    span_len = max(1, self.location.length)
                    pointer = " " * col_offset + "^" * span_len
                    out.append(f"    {pointer}")
                    out.append("")

        if self.suggestion:
            out.append(f"Suggestion: {self.suggestion}")

        return "\n".join(out)

    def __str__(self) -> str:
        return self.format()


class StarSyntaxError(StarDiagnosticError):
    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        super().__init__("Star Syntax Error", message, location, suggestion, source_code)


class StarRuntimeError(StarDiagnosticError):
    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        super().__init__("Star Runtime Error", message, location, suggestion, source_code)


class StarTypeError(StarDiagnosticError):
    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        super().__init__("Star Type Error", message, location, suggestion, source_code)


class StarNameError(StarDiagnosticError):
    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        super().__init__("Star Name Error", message, location, suggestion, source_code)


class StarValueError(StarDiagnosticError):
    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        super().__init__("Star Value Error", message, location, suggestion, source_code)


class StarInternalError(StarDiagnosticError):
    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        super().__init__("Star Internal Error", message, location, suggestion, source_code)


class StarWarning:
    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        self.category = "Star Warning"
        self.message = message
        self.location = location
        self.suggestion = suggestion
        self.source_code = source_code

    def format(self, source_code: Optional[str] = None) -> str:
        src = source_code or self.source_code
        out = [f"\n{self.category}: {self.message}"]

        if self.location:
            out.append(f"File: {self.location.file}")
            out.append(f"Line: {self.location.line}, Column: {self.location.column}")

            if src:
                lines = src.splitlines()
                line_idx = self.location.line - 1
                if 0 <= line_idx < len(lines):
                    source_line = lines[line_idx]
                    out.append("")
                    out.append(f"    {source_line}")
                    col_offset = max(0, self.location.column - 1)
                    span_len = max(1, self.location.length)
                    pointer = " " * col_offset + "^" * span_len
                    out.append(f"    {pointer}")
                    out.append("")

        if self.suggestion:
            out.append(f"Suggestion: {self.suggestion}")

        return "\n".join(out)

    def __str__(self) -> str:
        return self.format()
