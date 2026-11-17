# 🌟 STAR PRODUCTION DISTRIBUTION & SDK SPECIFICATION
**Version: 1.0.1**  
**Status: Authoritative Standard**  
**Document Class: Normative Architecture Specification**

---

## 1. Executive Summary & Philosophy

Star 1.2.0 establishes the formal boundary between the **Star development source repository** and the **User-facing Production SDK Binary Distribution**.

### The Core Distribution Invariant:
> **End-users install and execute Star as a self-contained, native binary toolchain (`star.exe`, `starc.exe`, `star-runtime.exe`). All Windows executables are verified Windows Portable Executables (PE32 / PE32+) with dual 64-bit and 32-bit (x64 / x86) compatibility. The distributed production SDK contains zero internal compiler or runtime source code (`.py`, `.pyc`).**

---

## 2. Production Binary SDK Layout

Release archives for target platforms (`Star-1.2.0-Windows-x64.zip` and `Star-1.2.0-Windows-x86.zip`) conform strictly to the following tree:

```text
Star-1.2.0-Windows-x64/ (or Star-1.2.0-Windows-x86/)
├── bin/
│   ├── star.exe             # Top-level CLI entrypoint & dispatcher (PE32/PE32+)
│   ├── starc.exe            # Star IR / Bytecode compiler (PE32/PE32+)
│   └── star-runtime.exe     # Virtual Machine execution engine (PE32/PE32+)
├── lib/
│   └── star/
│       ├── runtime/         # Compiled VM runtime artifacts (.starb)
│       ├── stdlib/          # Compiled standard library descriptors (.starb)
│       └── targets/         # Web (WASM), Desktop, Android, iOS targets
├── sdk/
│   ├── templates/           # Star project scaffolding templates
│   └── examples/            # Canonical reference applications
├── docs/                    # Offline documentation & The Star Book
├── licenses/                # MIT and third-party license notices
├── VERSION                  # "1.2.0"
├── SHA256SUMS               # Cryptographic hashes of all constituent files
└── star.manifest            # Machine-readable distribution manifest
```

---

## 2.1 Native PE Launcher Standard & 16-Bit Shield

All Windows binary launchers are compiled through `PELauncherCompiler`:
- **DOS & PE Signatures**: Every `.exe` contains a valid `MZ` header (offset 0) and `PE\0\0` signature at offset `e_lfanew`.
- **Dual Compatibility**: Compiled with `/platform:anycpu` (or dedicated x64/x86), ensuring native 64-bit execution on 64-bit Windows and native 32-bit execution on 32-bit Windows.
- **Zero 16-bit Classification**: Prevents Windows kernel fallback from misclassifying tools as unsupported 16-bit MS-DOS binaries.

---

## 3. Source Exclusion Gate

During the release packaging pipeline, the build orchestrator executes a strict **Source Exclusion Gate**:
1. Recursively traverses the distribution staging directory.
2. If any `.py`, `.pyc`, `.pyo`, or `__pycache__` directory is present, the release build fails immediately with a `SourceExclusionViolationError`.
3. Ensures that only native binaries, compiled bytecode descriptors (`.starb`), assets, and markdown documentation are published.

---

## 4. Deterministic Archive Standard

All distribution archives (`.zip`, `.starpkg`, `.tar.gz`) are built deterministically:
- **Timestamp Normalization**: File timestamps are normalized to `2026-01-01 00:00:00 UTC` to ensure byte-for-byte reproducible archive hashes.
- **Path Sorting**: Member entries are sorted alphabetically before serialization.
- **Permission Normalization**: Executable binaries are set to `0o755`, standard files to `0o644`.

---

## 5. Security & Zip-Slip Traversal Prevention

The `SecureExtractor` subsystem enforces hard security bounds on archive decompression:
1. **Pre-Validation**: All member names are validated before writing any file to disk.
2. **Traversal Rejection**: Any path containing `..`, leading slashes (`/`, `\`), or drive letters (`C:`) is immediately rejected with a `SecurityViolationError`.
3. **Atomic Extraction**: Archives are unpacked to an isolated temporary staging directory (`.tmp_extract_*`), checksums are verified against `star.manifest`, and files are moved atomically to the destination folder.

---

## 6. Automated PATH & Installation Workflow

When the installer or MSI runs:
1. Installs binaries to `C:\Program Files\Star\bin` (Windows) or `/usr/local/bin` (Linux/macOS).
2. Appends the binary directory to the user's persistent environment `PATH`.
3. On Windows, broadcasts a `WM_SETTINGCHANGE` notification so active terminal shells pick up the new PATH immediately.
4. Validates installation integrity via `star doctor --production`.
