"""
Star Language Module System & Standard Library
Authoritative Reference: STAR_SPEC.md (Section 8.2)
"""

import os
import math
import time
import sys
from typing import Dict, Optional, Any, Callable
from star_engine.tokens import SourceLocation
from star_engine.errors import StarRuntimeError, StarTypeError, StarValueError
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, StarModule, to_star_value
)


class ModuleManager:
    def __init__(self, interpreter: Any):
        self.interpreter = interpreter
        self.loaded_modules: Dict[str, StarModule] = {}
        self.loading_stack: set = set()
        self._init_stdlib()

    def _init_stdlib(self):
        # 1. Math Module
        math_exports: Dict[str, StarValue] = {
            "PI": StarDecimal(math.pi),
            "E": StarDecimal(math.e),
        }

        def _math_abs(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Math.abs() expects 1 argument.")
            v = args[0]
            if isinstance(v, StarInteger):
                return StarInteger(abs(v.value))
            if isinstance(v, StarDecimal):
                return StarDecimal(abs(v.value))
            raise StarTypeError("Math.abs() requires a number.")

        def _math_sqrt(*args: StarValue) -> StarValue:
            if len(args) != 1:
                raise StarValueError("Math.sqrt() expects 1 argument.")
            v = args[0]
            if not isinstance(v, (StarInteger, StarDecimal)):
                raise StarTypeError("Math.sqrt() requires a number.")
            if v.value < 0:
                raise StarValueError("Math.sqrt() cannot take negative numbers.")
            return StarDecimal(math.sqrt(v.value))

        def _math_pow(*args: StarValue) -> StarValue:
            if len(args) != 2:
                raise StarValueError("Math.pow() expects 2 arguments: base, exponent.")
            b, e = args[0], args[1]
            if not isinstance(b, (StarInteger, StarDecimal)) or not isinstance(e, (StarInteger, StarDecimal)):
                raise StarTypeError("Math.pow() requires numbers.")
            res = math.pow(b.value, e.value)
            if isinstance(b, StarInteger) and isinstance(e, StarInteger) and e.value >= 0:
                return StarInteger(int(res))
            return StarDecimal(res)

        def _math_min(*args: StarValue) -> StarValue:
            if len(args) != 2:
                raise StarValueError("Math.min() expects 2 arguments.")
            a, b = args[0], args[1]
            if not isinstance(a, (StarInteger, StarDecimal)) or not isinstance(b, (StarInteger, StarDecimal)):
                raise StarTypeError("Math.min() requires numbers.")
            return a if a.value <= b.value else b

        def _math_max(*args: StarValue) -> StarValue:
            if len(args) != 2:
                raise StarValueError("Math.max() expects 2 arguments.")
            a, b = args[0], args[1]
            if not isinstance(a, (StarInteger, StarDecimal)) or not isinstance(b, (StarInteger, StarDecimal)):
                raise StarTypeError("Math.max() requires numbers.")
            return a if a.value >= b.value else b

        def _math_floor(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], (StarInteger, StarDecimal)):
                raise StarTypeError("Math.floor() requires a number.")
            return StarInteger(math.floor(args[0].value))

        def _math_ceil(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], (StarInteger, StarDecimal)):
                raise StarTypeError("Math.ceil() requires a number.")
            return StarInteger(math.ceil(args[0].value))

        def _math_round(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], (StarInteger, StarDecimal)):
                raise StarTypeError("Math.round() requires a number.")
            return StarInteger(round(args[0].value))

        math_exports["abs"] = StarBuiltinFunction("abs", _math_abs)
        math_exports["sqrt"] = StarBuiltinFunction("sqrt", _math_sqrt)
        math_exports["pow"] = StarBuiltinFunction("pow", _math_pow)
        math_exports["min"] = StarBuiltinFunction("min", _math_min)
        math_exports["max"] = StarBuiltinFunction("max", _math_max)
        math_exports["floor"] = StarBuiltinFunction("floor", _math_floor)
        math_exports["ceil"] = StarBuiltinFunction("ceil", _math_ceil)
        math_exports["round"] = StarBuiltinFunction("round", _math_round)
        self.loaded_modules["Math"] = StarModule("Math", math_exports)

        # 2. Time Module
        time_exports: Dict[str, StarValue] = {}

        def _time_now(*args: StarValue) -> StarValue:
            return StarDecimal(time.time())

        def _time_sleep(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], (StarInteger, StarDecimal)):
                raise StarTypeError("Time.sleep() requires a number of seconds.")
            time.sleep(args[0].value)
            return StarNull()

        time_exports["now"] = StarBuiltinFunction("now", _time_now)
        time_exports["sleep"] = StarBuiltinFunction("sleep", _time_sleep)
        self.loaded_modules["Time"] = StarModule("Time", time_exports)

        # 3. String Module
        string_exports: Dict[str, StarValue] = {}

        def _str_trim(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], StarText):
                raise StarTypeError("String.trim() requires a Text argument.")
            return StarText(args[0].value.strip())

        def _str_upper(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], StarText):
                raise StarTypeError("String.uppercase() requires a Text argument.")
            return StarText(args[0].value.upper())

        def _str_lower(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], StarText):
                raise StarTypeError("String.lowercase() requires a Text argument.")
            return StarText(args[0].value.lower())

        def _str_contains(*args: StarValue) -> StarValue:
            if len(args) != 2 or not isinstance(args[0], StarText) or not isinstance(args[1], StarText):
                raise StarTypeError("String.contains() requires (Text, Text).")
            return StarBoolean(args[1].value in args[0].value)

        def _str_split(*args: StarValue) -> StarValue:
            if len(args) != 2 or not isinstance(args[0], StarText) or not isinstance(args[1], StarText):
                raise StarTypeError("String.split() requires (Text, delimiter: Text).")
            parts = args[0].value.split(args[1].value)
            return StarList([StarText(p) for p in parts])

        string_exports["trim"] = StarBuiltinFunction("trim", _str_trim)
        string_exports["uppercase"] = StarBuiltinFunction("uppercase", _str_upper)
        string_exports["lowercase"] = StarBuiltinFunction("lowercase", _str_lower)
        string_exports["contains"] = StarBuiltinFunction("contains", _str_contains)
        string_exports["split"] = StarBuiltinFunction("split", _str_split)
        self.loaded_modules["String"] = StarModule("String", string_exports)

        # 4. IO Module
        io_exports: Dict[str, StarValue] = {}

        def _io_read(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], StarText):
                raise StarTypeError("IO.readFile() requires a path Text.")
            path = args[0].value
            if not os.path.exists(path):
                raise StarRuntimeError(f"File not found: '{path}'")
            with open(path, "r", encoding="utf-8") as f:
                return StarText(f.read())

        def _io_write(*args: StarValue) -> StarValue:
            if len(args) != 2 or not isinstance(args[0], StarText) or not isinstance(args[1], StarText):
                raise StarTypeError("IO.writeFile() requires (path: Text, content: Text).")
            path = args[0].value
            with open(path, "w", encoding="utf-8") as f:
                f.write(args[1].value)
            return StarNull()

        def _io_exists(*args: StarValue) -> StarValue:
            if len(args) != 1 or not isinstance(args[0], StarText):
                raise StarTypeError("IO.fileExists() requires a path Text.")
            return StarBoolean(os.path.exists(args[0].value))

        io_exports["readFile"] = StarBuiltinFunction("readFile", _io_read)
        io_exports["writeFile"] = StarBuiltinFunction("writeFile", _io_write)
        io_exports["fileExists"] = StarBuiltinFunction("fileExists", _io_exists)
        self.loaded_modules["IO"] = StarModule("IO", io_exports)

        # 5. System Module
        sys_exports: Dict[str, StarValue] = {
            "platform": StarBuiltinFunction("platform", lambda *args: StarText(sys.platform)),
            "args": StarBuiltinFunction("args", lambda *args: StarList([StarText(a) for a in sys.argv[1:]]))
        }
        self.loaded_modules["System"] = StarModule("System", sys_exports)

        # 6. Controlled FFI Module
        from star_runtime.ffi import create_ffi_module
        self.loaded_modules["FFI"] = create_ffi_module(allow_native=True)

        # 7. Declarative UI Module
        from star_sdk.ui import create_ui_module
        self.loaded_modules["UI"] = create_ui_module()

        # 7b. Hardware-Accelerated Animation & Motion Suite
        from star_sdk.animation import create_animation_module
        anim_mod = create_animation_module()
        self.loaded_modules["Animation"] = anim_mod
        self.loaded_modules["Motion"] = anim_mod

        # 8. Theme System Module
        from star_sdk.theme import create_theme_module
        self.loaded_modules["Theme"] = create_theme_module()

        # 9. Mobile SDK & Hardware Bridge
        from star_sdk.mobile import create_mobile_module
        self.loaded_modules["Mobile"] = create_mobile_module()

        # 10. Flutter & Dart-like UI Architecture + 60,000+ UI Components Catalog
        from star_sdk.flutter import (
            create_flutter_module, create_material_module, create_cupertino_module,
            create_fluent_module, create_widgets_module, create_icons_module,
            create_colors_module, create_catalog_module
        )
        self.loaded_modules["Flutter"] = create_flutter_module()
        self.loaded_modules["Material"] = create_material_module()
        self.loaded_modules["Cupertino"] = create_cupertino_module()
        self.loaded_modules["Fluent"] = create_fluent_module()
        self.loaded_modules["Widgets"] = create_widgets_module()
        self.loaded_modules["Catalog"] = create_catalog_module()
        self.loaded_modules["Icons"] = create_icons_module()
        self.loaded_modules["Colors"] = create_colors_module()

        # 11. High-Performance HyperFlow Server & Concurrency Mesh
        from star_sdk.server import create_server_module
        server_mod = create_server_module()
        self.loaded_modules["Server"] = server_mod
        self.loaded_modules["HTTP"] = server_mod

        # 12. Universal AI, Tensor, Neural & Autonomous Agent Subsystem
        from star_sdk.ai import create_ai_module
        ai_mod = create_ai_module()
        self.loaded_modules["AI"] = ai_mod
        self.loaded_modules["Tensor"] = ai_mod
        self.loaded_modules["Neural"] = ai_mod
        self.loaded_modules["Agent"] = ai_mod

        # 13. OmniEngine 2.0 GN (Universal Execution, Parallel Fibers & Compute Grid)
        from star_sdk.omni import create_omni_module, create_fiber_module, create_grid_module
        omni_mod = create_omni_module()
        self.loaded_modules["Omni"] = omni_mod
        self.loaded_modules["Fiber"] = create_fiber_module()
        self.loaded_modules["Grid"] = create_grid_module()
        self.loaded_modules["JIT"] = omni_mod

    def load_module(self, name_or_path: str, is_file: bool, location: Optional[SourceLocation] = None) -> StarModule:
        # Check stdlib and preloaded modules
        if not is_file and name_or_path in self.loaded_modules:
            return self.loaded_modules[name_or_path]
        if name_or_path in self.loaded_modules:
            return self.loaded_modules[name_or_path]

        # Resolve file path, package path, or stdlib module
        interp_file = getattr(self.interpreter, "filename", "<stdin>")
        base_dir = os.path.dirname(interp_file) if interp_file != "<stdin>" else os.getcwd()
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        search_roots = []
        for d in [base_dir, os.getcwd(), repo_root]:
            if d and os.path.isdir(d) and d not in search_roots:
                search_roots.append(d)

        clean_name = name_or_path.replace("\\", "/")
        clean_name_nostar = clean_name[:-5] if clean_name.endswith(".star") else clean_name

        target_path = None

        # 1. Direct path check if absolute or exists relative to cwd
        if os.path.isabs(name_or_path) and os.path.exists(name_or_path):
            target_path = os.path.normpath(name_or_path)
        elif os.path.exists(os.path.normpath(name_or_path)):
            target_path = os.path.normpath(name_or_path)

        # 2. Search candidate paths across search_roots
        if not target_path:
            candidate_rel_paths = [
                clean_name,
                f"{clean_name}.star",
                f"{clean_name_nostar}.star",
                os.path.join(clean_name, "main.star"),
                os.path.join(clean_name, "index.star"),
                os.path.join("packages", clean_name),
                os.path.join("packages", f"{clean_name_nostar}.star"),
                os.path.join("packages", clean_name_nostar, "main.star"),
                os.path.join("modules", clean_name),
                os.path.join("modules", f"{clean_name_nostar}.star"),
                os.path.join("modules", clean_name_nostar, "index.star"),
                os.path.join("modules", clean_name_nostar, "main.star"),
                os.path.join("lib", clean_name),
                os.path.join("lib", f"{clean_name_nostar}.star"),
                os.path.join("lib", clean_name_nostar, "index.star"),
                os.path.join("lib", clean_name_nostar, "main.star"),
            ]
            for root in search_roots:
                for rel in candidate_rel_paths:
                    p = os.path.normpath(os.path.join(root, rel))
                    if os.path.isfile(p):
                        target_path = p
                        break
                if target_path:
                    break

        # 3. If still not found and bare module name (no slash), search category subdirectories of modules/ and lib/
        if not target_path and "/" not in clean_name_nostar and "\\" not in clean_name_nostar:
            for root in search_roots:
                for sub_dir in ["modules", "lib"]:
                    container = os.path.join(root, sub_dir)
                    if os.path.isdir(container):
                        for cat in sorted(os.listdir(container)):
                            cat_path = os.path.join(container, cat)
                            if os.path.isdir(cat_path):
                                p = os.path.normpath(os.path.join(cat_path, f"{clean_name_nostar}.star"))
                                if os.path.isfile(p):
                                    target_path = p
                                    break
                    if target_path:
                        break
                if target_path:
                    break

        # 4. Fallback default path for clear error reporting
        if not target_path:
            target_path = os.path.normpath(os.path.join(base_dir, name_or_path))
            if not target_path.endswith(".star"):
                target_path += ".star"

        if target_path in self.loaded_modules:
            return self.loaded_modules[target_path]

        if target_path in self.loading_stack:
            raise StarRuntimeError(f"Circular module dependency detected when loading '{name_or_path}'.", location)

        if not os.path.exists(target_path):
            raise StarRuntimeError(f"Cannot find module or file '{name_or_path}' (searched '{target_path}').", location)

        self.loading_stack.add(target_path)
        try:
            from star_engine.lexer import Lexer
            from star_engine.parser import Parser
            from star_engine.environment import Environment

            with open(target_path, "r", encoding="utf-8") as f:
                source = f.read()

            lexer = Lexer(source, filename=target_path)
            tokens = lexer.tokenize()
            parser = Parser(tokens, source_code=source, filename=target_path)
            program = parser.parse()

            module_env = Environment(parent=self.interpreter.global_env)
            for stmt in program.statements:
                self.interpreter.execute(stmt, module_env)

            exports = {k: v for k, (v, _) in module_env.bindings.items()}
            mod_name = os.path.splitext(os.path.basename(target_path))[0]
            module = StarModule(mod_name, exports)
            self.loaded_modules[target_path] = module
            self.loaded_modules[name_or_path] = module
            self.loaded_modules[mod_name] = module
            return module
        finally:
            self.loading_stack.remove(target_path)
