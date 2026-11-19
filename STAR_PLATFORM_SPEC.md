# Star Platform Independence & PAL Specification

**Version**: 1.0.0 (GA)  
**Standard**: Universal Platform Abstraction Layer (PAL)  
**Author**: Star Language Architectural Team  
**Status**: Canonical Standard & Production Specification

---

## 1. Overview & "Write Once, Run Anywhere" (WORA)

The **Star Platform Abstraction Layer (PAL)** enables complete platform independence across modern operating systems, hardware architectures, and deployment environments:
- **Desktop Operating Systems**: Windows (11 / 10 / Server, x64 / x86), Linux (Debian, Ubuntu, Fedora, Alpine, Arch, x64 / ARM64), macOS (Apple Silicon M-series, Intel x64).
- **Mobile Platforms**: Android (NDK/JNI, ARM64 / x86_64, API 24+ to 34+), iOS (Apple MetalKit + Swift Native Bridge, ARM64, iOS 15+).
- **Embedded & Edge**: Raspberry Pi (Linux ARM64 / ARM32), Docker Containers (Debian / Alpine).
- **Web & Browser**: WebAssembly (WASM) with 60 FPS Canvas & WebGPU rendering.

---

## 2. Platform Primitives & Standard Module (`use Platform`)

Star provides cross-platform primitives through `Platform` and `OS`:

```star
use Platform

// 1. Host Operating System & CPU Architecture
show Platform.os          // "windows", "linux", "macos", "android", "ios", "web"
show Platform.arch        // "x64", "arm64", "x86", "arm"
show Platform.is_64bit    // true
show Platform.is_windows  // true on Windows
show Platform.is_linux    // true on Linux
show Platform.is_macos    // true on macOS
show Platform.cpu_count   // Hardware thread/core count
show Platform.endian      // "little" or "big"

// 2. System-Independent Path Normalization
// Automatically resolves backslashes (\) on Windows vs slashes (/) on POSIX
variable cross_path = Platform.to_posix_path("src\\models\\user.star")
// => "src/models/user.star"

// 3. Universal System Directories
variable home = Platform.home_dir()
variable temp = Platform.temp_dir()
variable work = Platform.cwd()

// 4. Environment Variables
variable db_url = Platform.env("DATABASE_URL", "sqlite://app.db")

// 5. Cross-Platform Command Execution
variable cmd_res = Platform.run_command("echo Hello Star")
show cmd_res["stdout"]
```

---

## 3. Universal Launchers

Star provides native launchers for every target platform:
- **Windows**: `star.bat` (batch launcher) and `star.exe` (native x64 / x86 PE launcher).
- **Linux & macOS**: `star` and `star.sh` (POSIX shell runner with auto-discovery of `python3` / `python`).
- **Portable Python Runner**: `python -m star_engine` runs anywhere Python 3.10+ is installed without installation.
- **Universal Bytecode Bundles**: `star compile main.star` produces portable `.starb` bytecode that runs bit-for-bit identical on all OS targets.

---

## 4. Diagnostics CLI

```powershell
star platform:info
```
Outputs CPU architecture, OS release, endianness, CPU cores, home directory, and temp path.
