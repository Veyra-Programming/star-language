# 🌟 STAR ECOSYSTEM SPECIFICATION
**Version: 1.1.0**  
**Status: Authoritative Standard**  
**Document Class: Normative Architecture Specification**

---

## 1. Executive Summary

Star 1.1.0 establishes the comprehensive **Developer Ecosystem** standard for the Star programming language.

The ecosystem standardizes:
1. **Multi-Template Project Architecture**: Canonical layouts for CLI, Web, Desktop, Android, iOS, and Universal applications.
2. **The Official Package Registry**: Decentralized metadata, semantic versioning, reproducible lockfiles (`star.lock`), and binary package containers (`.starpkg`).
3. **The Official Star Developer Portal (`www.shreeshop.in/star`)**: Web showcase built with Star WebAssembly, hosting downloads, live multi-target playground, package discovery, and The Star Book.
4. **Universal Development Commands**: Uniform `star run` and `star build` workflows across all four supported targets.

---

## 2. Canonical Project Templates

Every Star project initialized via `star new <name> [--template <type>]` produces a deterministic directory tree:

```text
<app_name>/
├── src/
│   └── main.star          # Application entrypoint
├── assets/                # Images, fonts, and static resources
├── tests/
│   └── test_main.star     # Automated test suite
├── star.toml              # Project manifest and capability declarations
├── star.lock              # Deterministic cryptographic dependency lockfile
├── README.md              # Documentation and build instructions
└── .gitignore             # Ignored build outputs and cache directories
```

### Template Catalog:
| Template | Target | Description |
| :--- | :--- | :--- |
| `cli` | Command Line | Console IO, argument parsing, system tools |
| `web` | WebAssembly | DOM reconciliation, CSS styling, browser events |
| `desktop` | Native OS | Native windowing, menus, 2D vector layouts |
| `android` | Android NDK | JNI bridge, safe areas, APK/AAB builds |
| `ios` | iOS Metal | Swift bridge, MetalKit GPU shaders, IPA builds |
| `universal` | **Universal** | **Flagship: Write once, run across Web, Desktop, Android & iOS** |

---

## 3. Package Registry Lifecycle

The Star Package Registry enforces a reproducible dependency management pipeline:

```text
    Developer Machine                              Star Registry
   ┌─────────────────┐                           ┌────────────────┐
   │    star new     │                           │  Official Web  │
   │       ↓         │                           │    Catalog     │
   │  star search ───┼──────────────────────────►│  (www.shreeshop│
   │       ↓         │                           │   .in/star)    │
   │  star install ◄─┼───────────────────────────┤                │
   │       ↓         │                           │                │
   │  star package ──┼───► .starpkg container    │                │
   │       ↓         │         │                 │                │
   │  star publish ──┼─────────┴────────────────►│ Package Store  │
   └─────────────────┘                           └────────────────┘
```

1. **Manifest Registration (`star.toml`)**: Declares semantic dependencies.
2. **Lockfile Guarantee (`star.lock`)**: Records immutable SHA-256 digests and version resolutions.
3. **Package Distribution (`.starpkg`)**: Deterministic archive container holding compiled bytecode (`.starb`), descriptors, assets, and checksums.
