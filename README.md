# 🌟 Star Programming Language (v1.2.0 GA)

> **Simple to learn. Powerful to build. Beautiful to read. Difficult to misuse.**  
> **Write Once. Run Everywhere (Web, Desktop, Android, iOS).**

[![Version](https://img.shields.io/badge/version-1.2.0%20GA-blue.svg)](STAR_SPEC.md)
[![Tests](https://img.shields.io/badge/tests-183%2F183%20passing%20(100%25)-brightgreen.svg)](tests/)
[![Distribution](https://img.shields.io/badge/distribution-Zero--Installer%20Portable%20ZIP-orange.svg)](dist/)
[![WebGPU](https://img.shields.io/badge/rendering-WebGPU%20SDF%2060%20FPS-purple.svg)](STAR_WEBGPU.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Portal](https://img.shields.io/badge/portal-www.shreeshop.in%2Fstar-purple.svg)](https://www.shreeshop.in/star)

Star is an independent, modern, universal programming language and cross-platform application ecosystem. Designed from the ground up for maximum visual clarity, developer productivity, and long-term stability, Star compiles deterministically to **WebAssembly (Web)**, **Native Desktop (macOS/Windows/Linux)**, **Android (NDK/JNI + APK/AAB)**, and **iOS (Apple Metal + Swift + IPA)** with 100% semantic parity.

---

## ✨ Features at a Glance

* **Write Once, Run Everywhere**: Single codebase for Web, Desktop, Android, and iOS with identical observable semantics.
* **100% Certified Test Suite**: 207/207 unit, integration, hardware, and conformance tests passing (0 failures, 0 errors).
* **Haven (Heaven Language) Natural English Syntax & 74,600+ UI Components (`STAR_FLUTTER.md`)**: Full Haven natural English syntax (`set count to 0`, `increase count by 1`, `say "Hello {name}"`, `whenever x is greater than 10:`, `durable record`, `|>`) combined with a Flutter-grade reactive UI component engine (`Scaffold`, `AppBar`, `ElevatedButton`, `CupertinoButton`, `Row`, `Column`, `ListView`), Material 3, Cupertino, and massive 74,600+ native UI component catalog. Zero JavaScript / Node.js runtime required (`star flutter demo`, `star widgets count`).
* **Zero-Installer Portable ZIP SDK**: Flutter-style extraction without administrative rights; automated user PATH configuration via `star.bat setup` or `setup.cmd`.
* **Minimal Punctuation**: No curly braces (`{}`), semicolons (`;`), or cryptic punctuation.
* **Readable Blocks**: Clear `end`-delimited structures (`app`, `component`, `class`, `function`, `if`, `while`, `for`).
* **Declarative Star UI**: Pure reactive component hierarchy with WebGPU SDF 60 FPS hardware accelerated rendering.
* **Universal Hardware SDK (`use Mobile`)**: Safe, capability-gated access to Storage, Battery, Haptics, Clipboard, Screen, Orientation, Network, Camera, and Geolocation.
* **Native Android Backend (Android SDK Powered)**: Full Android builds integrate with the local **Android SDK** (`ANDROID_HOME`), targeting API 34+ (Google Play compliant) with dual APK / AAB builders, build-tools, and ADB deployment.
* **Native iOS Backend (Star Inbuild System & Star SDKs)**: Compiles and packages iOS IPAs (`Payload/<App>.app`) directly via Star's **Inbuild System & Star SDKs**—no macOS hardware or Xcode required. Includes Swift runtime bridge and Apple MetalKit GPU rendering.
* **Package Registry Ecosystem**: Official package catalog (`http`, `sqlite`, `canvas2d`, `crypto`, `ui-icons`, `test-kit`, `json`, `websocket`) with `star search` and `star install`.
* **Stability & Compatibility Guarantee**: Formal Star 1.x forward-compatibility promise (`STAR_COMPATIBILITY.md`) and locked Core ABI v1 / Mobile ABI v1 contracts.
* **Dual 64-bit & 32-bit (x64 / x86) Native Launchers**: Authentic Windows Portable Executables (`star.exe`, `starc.exe`, `star-runtime.exe`) with AnyCPU support for seamless 64-bit and 32-bit Windows execution and zero 16-bit legacy errors.
* **Interactive Developer Portal**: Complete web platform featuring in-browser Star simulator, 20-chapter Star Book curriculum, example showcases, and system health diagnostics (`star portal` / `web/portal/index.html`).

---

## 🚀 Quick Start

### 1. Create a New Universal Project
```bash
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
