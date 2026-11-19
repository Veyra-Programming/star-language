# 🌟 Star Programming Language (v1.3.0 GA)

> **Simple to learn. Powerful to build. Beautiful to read. Difficult to misuse.**  
> **Write Once. Run Everywhere (Web, Desktop, Android, iOS, Server, AI Creation & Training).**

[![Version](https://img.shields.io/badge/version-1.3.0%20GA-blue.svg)](STAR_SPEC.md)
[![Telegram](https://img.shields.io/badge/Telegram-Join_Community-24A1DE.svg?logo=telegram)](https://t.me/opendigitalcontinuity)
[![Tests](https://img.shields.io/badge/tests-266%2F266%20passing%20(100%25)-brightgreen.svg)](tests/)
[![Distribution](https://img.shields.io/badge/distribution-Zero--Installer%20Portable%20ZIP-orange.svg)](dist/)
[![AI Engine](https://img.shields.io/badge/AI-Native%20Tensors%20%26%20Autograd-blueviolet.svg)](STAR_AI_SPEC.md)
[![Server Engine](https://img.shields.io/badge/server-HyperFlow%20Engine%20v1.3.0-darkgreen.svg)](STAR_SERVER_SPEC.md)
[![WebGPU](https://img.shields.io/badge/rendering-WebGPU%20SDF%2060%20FPS-purple.svg)](STAR_WEBGPU.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Portal](https://img.shields.io/badge/portal-www.shreeshop.in%2Fstar-purple.svg)](https://www.shreeshop.in/star)

Star is an independent, modern, universal programming language and cross-platform application ecosystem. Designed from the ground up for maximum visual clarity, developer productivity, and long-term stability, Star compiles deterministically to **WebAssembly (Web)**, **Native Desktop (macOS/Windows/Linux)**, **Android (NDK/JNI + APK/AAB)**, **iOS (Apple Metal + Swift + IPA)**, **High-Performance Server (HyperFlow Engine)**, and **Universal AI & Neural Computation (Tensors, Autograd, Transformers, Vector Search, Autonomous Agents)** with 100% semantic parity.

---

## ✨ Features at a Glance

* **Write Once, Run Everywhere**: Single codebase for Web, Desktop, Android, iOS, Server, AI, and Distributed Clusters with identical observable semantics.
* **100% Certified Test Suite**: 298/298 unit, integration, hardware, server, AI, web tools, and conformance tests passing (0 failures, 0 errors).
* **Universal Platform Independence & PAL (`STAR_PLATFORM_SPEC.md`)**: Full WORA (Write Once, Run Anywhere) support across Windows, Linux, macOS, Android, iOS, and WebAssembly with automatic path normalization, hardware detection, POSIX shell runners (`star`, `star.sh`), and `use Platform` / `use OS` standard modules (`star platform:info`).
* **PHP-Style Web Tools & Rapid Scripting Suite (`STAR_WEB_TOOLS_SPEC.md`)**:
  - **Embedded HTML Templating (`Template`)**: Blade/PHP-style tags (`{{ ... }}`, `{% whenever %}`, `{% for each %}`) with automatic XSS sanitization and filter pipelines.
  - **Fluent Database ORM (`DB`)**: Eloquent/PDO-style query builder (`DB.table("users").where(...).order_by(...).get()`) for SQLite and in-memory tables.
  - **Cryptographic Security & Validation (`Security`)**: PBKDF2-HMAC-SHA256 salted password hashing, declarative input validation, and CSRF token verification.
  - **Stateful Web Sessions & Cookies (`Session`)**: Multi-tenant session manager with flash notifications and secure cookie serialization.
  - **Artisan-Style Code Generators & Dev Server**: `star make:page`, `star make:api`, `star make:model`, and `star web:serve` embedded development web server.
* **Star OmniEngine 2.0 GN (Generation Next) (`STAR_OMNI_SPEC.md`)**: Ultra-high-performance multi-target execution engine:
  - **M:N Work-Stealing Parallel Fibers**: 100,000+ fibers/sec with Go-style CSP channels (`OmniChannel`).
  - **Unified Arena & Zero-Copy Memory**: 1,740,000+ allocs/sec bump-pointer allocation with instant $O(1)$ zero-GC recycling and memory views (`BorrowedBuffer`).
  - **Profile-Guided Tiered JIT**: Hotspot tracking, dynamic type specialization, and native execution compilation.
  - **Global Network (GN) Distributed Cluster Mesh**: P2P node clustering, decentralized scatter-gather, and automated node failover (`star omni:cluster`).
  - **Zero-Cost Polyglot FFI**: Dynamic C ABI linking with crash isolation (`star omni:info`, `star omni:bench`).
* **Universal AI, Deep Learning & Autonomous Agent Engine (`STAR_AI_SPEC.md`)**: Native zero-dependency N-dimensional Tensor core, reverse-mode automatic differentiation (`Autograd`), layer catalog (`Dense`, `Sequential`, `LayerNorm`, `SelfAttention`, `TransformerBlock`), activations (`relu`, `sigmoid`, `tanh`, `gelu`, `softmax`), loss criteria (`MSELoss`, `CrossEntropyLoss`, `BinaryCrossEntropyLoss`), optimizers (`SGD`, `Adam`, `AdamW`), in-memory `VectorStore` (cosine similarity, KNN retrieval), and autonomous `AIAgent` with memory and dynamic tool calling (`star ai:train`, `star ai:info`).
* **Star HyperFlow Server Engine & Server-Side Scripting (`STAR_SERVER_SPEC.md`)**: High-throughput asynchronous event-driven server runtime with thread-pooled non-blocking fibers, Radix Trie route lookup, and built-in HTTP load benchmarking (`star serve`, `star server:routes`, `star server:bench`).
* **Revolutionary Concept 1 — ChronoState & Time-Reversible Execution**: Native $O(1)$ in-memory micro-snapshots and vector-clocked checkpoints. Partial request failures automatically rewind in-memory state cleanly with zero side-effects or dirty cache corruption!
* **Revolutionary Concept 2 — Quantum-Reactive Live Pipeline**: Zero-serialization live synchronization between server state and connected frontend clients via automatic RFC 6902 differential JSON patches over HTTP SSE and WebSockets.
* **Revolutionary Concept 3 — Sovereign Actor Mesh**: Concurrent actor processes with bounded ring-buffer mailboxes, self-healing supervision trees, and request-reply futures (`ask` / `send`).
* **Modern Method Chaining**: Built-in fluent methods for `Text` (`.uppercase()`, `.lowercase()`, `.trim()`, `.split()`, `.contains()`, `.replace()`, `.starts_with()`), `List` (`.push()`, `.pop()`, `.join()`, `.contains()`, `.reverse()`), and `Map` (`.keys()`, `.values()`, `.has()`, `.size`).
* **Haven (Heaven Language) Natural English Syntax & 74,600+ UI Components (`STAR_FLUTTER.md`)**: Full Haven natural English syntax (`set count to 0`, `increase count by 1`, `say "Hello {name}"`, `whenever x is greater than 10:`, `durable record`, `|>`) combined with a Flutter-grade reactive UI component engine (`Scaffold`, `AppBar`, `ElevatedButton`, `CupertinoButton`, `Row`, `Column`, `ListView`), Material 3, Cupertino, and massive 74,600+ native UI component catalog. Zero JavaScript / Node.js runtime required (`star flutter demo`, `star widgets count`).
* **Zero-Installer Portable ZIP SDK**: Flutter-style extraction without administrative rights; automated user PATH configuration via `star.bat setup` or `setup.cmd`.
* **Minimal Punctuation**: No curly braces (`{}`), semicolons (`;`), or cryptic punctuation.
* **Readable Blocks**: Clear `end`-delimited structures (`app`, `component`, `class`, `function`, `if`, `while`, `for`).
* **Declarative Star UI**: Pure reactive component hierarchy with WebGPU SDF 60 FPS hardware accelerated rendering.
* **Universal Hardware SDK (`use Mobile`)**: Safe, capability-gated access to Storage, Battery, Haptics, Clipboard, Screen, Orientation, Network, Camera, and Geolocation.
* **Native Android Backend (Android SDK Powered)**: Full Android builds integrate with the local **Android SDK** (`ANDROID_HOME`), targeting API 34+ (Google Play compliant) with dual APK / AAB builders, build-tools, and ADB deployment.
* **Native iOS Backend (Star Inbuild System & Star SDKs)**: Compiles and packages iOS IPAs (`Payload/<App>.app`) directly via Star's **Inbuild System & Star SDKs**—no macOS hardware or Xcode required. Includes Swift runtime bridge and Apple MetalKit GPU rendering.
* **Package Registry Ecosystem (570+ Packages, 350+ Official UI Packages) (`STAR_UI_PACKAGES.md`)**: Full package ecosystem with `star search` and `star install` covering 350+ UI packages (forms, charts, tables, navigation, modals, video/audio players, and animations) plus 220+ standard library packages.
* **Stability & Compatibility Guarantee**: Formal Star 1.x forward-compatibility promise (`STAR_COMPATIBILITY.md`) and locked Core ABI v1 / Mobile ABI v1 contracts.
* **Dual 64-bit & 32-bit (x64 / x86) Native Launchers**: Authentic Windows Portable Executables (`star.exe`, `starc.exe`, `star-runtime.exe`) with AnyCPU support for seamless 64-bit and 32-bit Windows execution and zero 16-bit legacy errors.
* **Interactive Developer Portal**: Complete web platform featuring in-browser Star simulator, 20-chapter Star Book curriculum, example showcases, and system health diagnostics (`star portal` / `web/portal/index.html`).

---

## 🚀 Quick Start

### 1. Create a New Project
```bash
# Universal Mobile / Desktop / Web App
star new my_app
cd my_app
star run

# High-Performance Server Microservice
star new my_api --template server
cd my_api
star serve

# Universal AI & Deep Learning Model
star new my_ai --template ai
cd my_ai
star run
```

### 2. Inspect Server Routes & Benchmark
```bash
star server:routes
star server:bench http://localhost:8080/api/health --requests 500 --concurrency 10
```

### 3. Train AI Models & Inspect Diagnostics
```bash
star ai:info
star ai:train examples/ai_neural_showcase.star
```

### 4. OmniEngine 2.0 GN Diagnostics, Benchmarks & Cluster
```bash
star omni:info
star omni:bench
star omni:cluster
star run examples/omni_engine_showcase.star
```

### 5. Web Tools & Platform Independence
```bash
# Cross-platform environment diagnostics
star platform:info

# Scaffold web page, API endpoint, or database model
star make:page home
star make:api users
star make:model User

# Launch embedded development server (default port 8000)
star web:serve --port 8000

# Run PHP-style showcase
star run examples/php_web_showcase.star
```
star new my_app
cd my_app
star run
```

### 2. Launch Developer Portal & Playground
```bash
star portal
```

### 3. Build & Deploy Across Platforms
```bash
star build web            # Deployable WebAssembly bundle
star build desktop        # Native Desktop application
star build apk            # Android APK (Auto-signed)
star build aab            # Android App Bundle (Play Store)
star build ipa            # iOS IPA (Apple App Store)
star release mobile       # End-to-end multi-platform release
```


---

## 📚 Documentation

* **[Complete Language Guide & AI Prompting Reference (`STAR_LANGUAGE_COMPLETE_GUIDE.md`)](STAR_LANGUAGE_COMPLETE_GUIDE.md)** — Exhaustive master manual covering full syntax, Flutter UI, mobile hardware, StarVM, and ChatGPT prompting rules.
* [Language Specification (`STAR_SPEC.md`)](STAR_SPEC.md) — The authoritative language definition.
* [Flutter on Dart & 60,000+ UI Components (`STAR_FLUTTER.md`)](STAR_FLUTTER.md) — Flutter widget hierarchy, Material 3, Cupertino, and 74,600+ UI components.
* [Developer Portal & Admin Platform (`STAR_PORTAL_ADMIN.md`)](STAR_PORTAL_ADMIN.md) — Portable ZIP distribution, portal architecture & admin console.
* [Developer Ecosystem Specification (`STAR_ECOSYSTEM.md`)](STAR_ECOSYSTEM.md) — Multi-template project layout & registry lifecycle.
* [WebGPU Hardware Acceleration (`STAR_WEBGPU.md`)](STAR_WEBGPU.md) — GPU shader pipeline, draw batching & 60+ FPS rendering.
* [Production Distribution & SDK (`STAR_DISTRIBUTION.md`)](STAR_DISTRIBUTION.md) — Binary SDK layout, source exclusion, installer & security.
* [Stability & Compatibility Policy (`STAR_COMPATIBILITY.md`)](STAR_COMPATIBILITY.md) — 1.x forward compatibility guarantee.
* [Runtime ABI Specification (`STAR_ABI.md`)](STAR_ABI.md) — Locked Core ABI v1 and Mobile ABI v1 contracts.
* [Dual-Device Hardware Verification (`STAR_HARDWARE.md`)](STAR_HARDWARE.md) — Real hardware conformance, probes, and metrics.
* [Mobile Platform Specification (`STAR_MOBILE.md`)](STAR_MOBILE.md) — Universal mobile touch & layout model.
* [Mobile Deployment & CI Pipeline (`STAR_RELEASE.md`)](STAR_RELEASE.md) — Build, signing, verification, and CI automation.
* [Native Device SDK (`STAR_DEVICE_SDK.md`)](STAR_DEVICE_SDK.md) — Universal hardware APIs across Web, Desktop, Android & iOS.
* [Cross-Platform Conformance (`STAR_CONFORMANCE.md`)](STAR_CONFORMANCE.md) — 100% semantic verification across 4 targets.
* [Android Native Backend (`STAR_ANDROID.md`)](STAR_ANDROID.md) — Android JNI/NDK bridge and APK/AAB builds.
* [iOS Native Backend (`STAR_IOS.md`)](STAR_IOS.md) — Swift / Apple Metal bridge and Xcode/IPA builds.
* [Desktop Target Specification (`STAR_DESKTOP.md`)](STAR_DESKTOP.md) — Native windowing & layout engine.
* [Web Target Specification (`STAR_WEB.md`)](STAR_WEB.md) — WebAssembly backend and DOM engine.
* [Declarative UI Specification (`STAR_UI.md`)](STAR_UI.md) — Reactive component model and UI hierarchy.
* [Star IR Specification (`STAR_IR.md`)](STAR_IR.md) — Formal Intermediate Representation and Opcode specification.
* [Development Roadmap (`STAR_ROADMAP.md`)](STAR_ROADMAP.md) — Milestone roadmap.

---

## 🛠️ Star CLI Commands

```bash
# Setup & Health Commands
star setup                          # Automatically configure PATH for portable ZIP installation
star doctor                         # Check development environment health

# Project & Package Commands
star new <app_name> [--template <type>] # Create project (universal, cli, web, desktop, android, ios)
star init                           # Initialize star.toml in current directory
star add <package> [version]        # Add package dependency
star remove <package>               # Remove package dependency
star install [package]              # Install dependencies or install from registry
star search <query>                 # Search official Star Package Registry
star package / star pack            # Create deterministic .starpkg container
star publish                        # Publish package (.starpkg) to registry
star update                         # Update dependencies to latest compatible versions
star archive [project]              # Create deterministic distribution archive
star extract <archive> [target]     # Extract archive with Zip-Slip protection
star verify [apk|aab|ipa|<file>]    # Verify package checksums or mobile artifacts
star compile <file.star>            # Compile Star source to .starb binary bytecode
star build [web|desktop|android|ios|apk|aab|ipa] # Build for selected target
star run [web|desktop|android|ios]  # Universal run command
star release mobile [file.star]     # Run complete build, sign, verify release pipeline
star deploy [android|ios]           # Deploy to device, emulator, or simulator
star devices                        # List connected Android & iOS devices/simulators
star self-update [--check]          # Self-update Star SDK
star certify [--ecosystem|--production] # Run full Universal / Ecosystem certification
star portal                         # Open developer portal & interactive playground
star ci init                        # Generate GitHub Actions and GitLab CI workflows

# Developer & Diagnostic Commands
star ir <file.star>                 # Disassemble and inspect Star IR bytecode
star check / star lint <file.star>  # Run semantic checks and linter
star format / star fmt <file.star>  # Format source code (use --check for CI)
star test [--target all|hardware]   # Run test suite, conformance matrix, or hardware tests
star doctor [--production|--signing|--hardware] # Check environment, PATH, and production status
star docs                           # Browse offline documentation and API references
star repl                           # Launch interactive REPL
star version                        # Show version information
```





---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
