"""
Star Mobile Runtime Fault Isolation & Crash Recovery Subsystem
Authoritative Reference: STAR_ABI.md & STAR_MOBILE_RUNTIME.md
"""

import sys
import traceback
from typing import Callable, Any, Optional, Dict
from star_engine.errors import StarRuntimeError


class RuntimeFaultBarrier:
    """
    Encapsulates Star VM executions and event dispatches within structured fault barriers,
    preventing application exceptions from crashing native host platforms (Android/iOS).
    """

    @classmethod
    def execute_safely(
        cls,
        operation_name: str,
        func: Callable[[], Any],
        fallback_val: Any = None,
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> Any:
        try:
            return func()
        except StarRuntimeError as se:
            print(f"[Star Runtime Warning] Controlled error in '{operation_name}': {se}", file=sys.stderr)
            if on_error:
                on_error(se)
            return fallback_val
        except Exception as ex:
            print(f"[Star Fault Barrier] Caught unhandled exception during '{operation_name}':", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            if on_error:
                on_error(ex)
            return fallback_val
