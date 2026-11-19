"""
Star Standard Library — Platform Independence Subsystem (use Platform / use OS)
Authoritative Reference: STAR_PLATFORM_SPEC.md
"""

from typing import Dict, Any, List, Optional
from star_engine.types import (
    StarValue, StarNull, StarBoolean, StarInteger, StarDecimal,
    StarText, StarList, StarMap, StarBuiltinFunction, StarModule, to_star_value, from_star_value
)
from star_engine.platform import Platform


def create_platform_module() -> StarModule:
    exports: Dict[str, StarValue] = {
        "os": StarText(Platform.os_name()),
        "arch": StarText(Platform.arch()),
        "is_windows": StarBoolean(Platform.is_windows()),
        "is_linux": StarBoolean(Platform.is_linux()),
        "is_macos": StarBoolean(Platform.is_macos()),
        "is_android": StarBoolean(Platform.is_android()),
        "is_64bit": StarBoolean(Platform.is_64bit()),
        "endian": StarText(Platform.endian()),
        "cpu_count": StarInteger(Platform.cpu_count()),
        "path_sep": StarText(Platform.path_separator()),
    }

    # 1. Platform.home_dir()
    exports["home_dir"] = StarBuiltinFunction("home_dir", lambda *a: StarText(Platform.home_dir()))

    # 2. Platform.temp_dir()
    exports["temp_dir"] = StarBuiltinFunction("temp_dir", lambda *a: StarText(Platform.temp_dir()))

    # 3. Platform.cwd()
    exports["cwd"] = StarBuiltinFunction("cwd", lambda *a: StarText(Platform.cwd()))

    # 4. Platform.normalize_path(path)
    exports["normalize_path"] = StarBuiltinFunction("normalize_path", lambda *a: StarText(Platform.normalize_path(a[0].to_string()) if a else ""))

    # 5. Platform.to_posix_path(path)
    exports["to_posix_path"] = StarBuiltinFunction("to_posix_path", lambda *a: StarText(Platform.to_posix_path(a[0].to_string()) if a else ""))

    # 6. Platform.env(key, default)
    def _env(*args: StarValue) -> StarValue:
        if not args:
            return StarNull()
        key = args[0].to_string()
        default = args[1].to_string() if len(args) > 1 else None
        res = Platform.get_env(key, default)
        return StarText(res) if res is not None else StarNull()
    exports["env"] = StarBuiltinFunction("env", _env)

    # 7. Platform.run_command(cmd)
    def _run_cmd(*args: StarValue) -> StarValue:
        if not args:
            return StarMap({})
        cmd = args[0].to_string()
        timeout = args[1].value if len(args) > 1 and isinstance(args[1], (StarInteger, StarDecimal)) else None
        res = Platform.run_command(cmd, timeout=timeout)
        return to_star_value(res)
    exports["run_command"] = StarBuiltinFunction("run_command", _run_cmd)

    # 8. Platform.info()
    exports["info"] = StarBuiltinFunction("info", lambda *a: to_star_value(Platform.platform_info()))

    return StarModule("Platform", exports)


def create_os_module() -> StarModule:
    plat = create_platform_module()
    return StarModule("OS", plat.exports)
