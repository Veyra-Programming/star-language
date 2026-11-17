## [1.3.0] - 2026-11-15 (Professional Star UI Motion & Animation Engine, Extended Component Suite & Bugfix Release)

### Added
- **Hardware-Accelerated Motion & Animation Engine (`star_sdk/animation/` · `use Animation` / `use Motion`)**:
  - **Full Easing Curve Library**: `Curves.linear`, `Curves.ease_in`, `Curves.ease_out`, `Curves.ease_in_out`, `Curves.bounce_in`, `Curves.bounce_out`, `Curves.bounce_in_out`, `Curves.elastic_in`, `Curves.elastic_out`, `Curves.spring`, `Curves.fast_out_slow_in`, `Curves.smooth_spring`, `Curves.overshoot`, and general `Curves.cubic_bezier(x1, y1, x2, y2)` solver.
  - **Spring Harmonic Physical Simulator (`SpringSimulation`)**: Real-time analytical ODE solver with mass, stiffness, damping, and initial velocity supporting under-damped, critically damped, and over-damped fluid motions.
  - **AnimationController Engine**: Microsecond-precision timing ticker with `.forward()`, `.reverse()`, `.reset()`, `.repeat()`, `.stop()`, bounds clamping, and reactive listener callbacks.
  - **Interpolation Tweens**: `Tween` (linear float), `ColorTween` (RGB hex interpolation), `OffsetTween` (2D coordinate translation), and `SizeTween`.
  - **Declarative Motion Virtual Nodes**:
    - `UI.animated_opacity(opacity, duration_ms, curve, child)`
    - `UI.animated_scale(scale, duration_ms, curve, child)`
    - `UI.animated_slide(offset_x, offset_y, duration_ms, curve, child)`
    - `UI.animated_rotation(angle_deg, duration_ms, curve, child)`
    - `UI.animated_container(width, height, bg, radius, duration_ms, curve, child)`
    - `UI.shimmer(width, height, radius, child)` & `UI.skeleton(width, height, radius)`
    - `UI.pulse(min_scale, max_scale, duration_ms, child)` & `UI.bounce(intensity, duration_ms, child)`
    - `UI.shake(intensity, duration_ms, child)` & `UI.glow(color, blur, duration_ms, child)`
    - `UI.marquee(text, speed)` & `UI.confetti(count, active)` & `UI.ripple(color, duration_ms)`
- **15+ Brand New Professional UI Components (`star_sdk/ui/` · `Star.js` · `star_js/star.js`)**:
  - `UI.modal`: Centered glassmorphic modal with frosted backdrop blur and close/confirm action listeners.
  - `UI.dialog`: Streamlined confirmation and alert dialog with animated scale-in pop.
  - `UI.drawer`: Slide-out panel for navigation and sidebars with customizable orientation.
  - `UI.accordion`: Expandable disclosure cards with smooth height collapse/expand.
  - `UI.dropdown`: Sleek select menus with floating popovers and active item indicators.
  - `UI.tooltip`: Contextual tooltip bubbles with arrow indicators and position configurations.
  - `UI.breadcrumbs`: Hierarchical navigational path trail.
  - `UI.pagination`: Numerical pagination control with previous/next triggers.
  - `UI.table`: Responsive data table with striped rows, uppercase header styling, and cell borders.
  - `UI.code_block`: Monospace code viewer with language badge and one-click copy button.
  - `UI.segmented_control`: Apple/Fluent-inspired pill switch for view modes and filters.
  - `UI.stepper`: Multi-step workflow indicator with step numbers, checkmarks, and connecting tracks.
  - `UI.rating`: Interactive 5-star rating widget with hover scale and golden glow.
  - `UI.fab`: Elevated floating action button with ambient glow and icon badge.
  - `UI.bottom_sheet`: Mobile-first sliding bottom sheet drawer with top grab handle.
- **Native Desktop 60 FPS Windowing & Animation Ticker (`star_backend/desktop/`)**:
  - `DesktopWindow.start_ticker(fps, callback)`: Non-blocking 60/120 FPS frame scheduler.
  - Native 2D canvas drawing routines for shimmer sweeps, skeleton loaders, outer luminous halos, modals, accordions, dropdowns, tables, and rating stars.
  - `DesktopRuntime` animation phase manager driving continuous silky smooth delta-time transitions.
- **Star.js Universal Web Motion Architecture (`Star.js` · `star_js/star.js`)**:
  - First-class `Star.Motion` module with spring solvers, Web Animation API bindings, keyframes, automatic button click ripples, and confetti particle bursts.
- **GPU-Accelerated CSS Design System (`star_js/style.css` · `star_backend/wasm/styles.css`)**:
  - Added 770+ lines of sleek modern glassmorphism, spring curves, micro-interactions, and 12+ GPU-accelerated keyframe animations.
- **Production-Grade Android Build Engine & Gradle Wrapper (`star_backend/mobile/android/` · `star_engine/cli.py`)**:
  - **Smart Entrypoint Resolution (`_resolve_entry_file`)**: Robust resolution cascading from explicit arguments (`.star` auto-extension) to `star.toml` (`entry`), standard entries (`main.star`, `app.star`, `src/main.star`), solitary directory `.star` files, and repo showcase examples with clean diagnostics.
  - **Full Gradle Wrapper Generation**: Generated Android projects in `build/android/project` now include official Gradle 8.2 wrapper configurations (`gradlew.bat`, `gradlew`, `gradle/wrapper/gradle-wrapper.properties`, `gradle-wrapper.jar` stub).
  - **ProGuard / R8 Protection Rules**: Generates `app/proguard-rules.pro` keeping `org.starlang.runtime.**` JNI interfaces and native bridge bindings safe from code-shrinking regression.
  - **uv / Standalone Python Detection**: Updated Windows launcher (`star.bat`) to detect `%APPDATA%\uv\python\*\python.exe` eliminating Microsoft Store alias stalls.
  - **Resilient Android Host Simulation**: Hardened `MobileRuntime` with fallback execution ensuring smooth local surface simulation even with complex dynamic reactive states.
- **Star Go — Expo Go Companion App & QR Code Live Testing (`android/` · `apps/star_go/` · `star go`)**:
  - **Dedicated Android App Directory (`android/`)**: Standalone native Android Gradle project (`org.starlang.go`) with AGP 8.2, Gradle 8.2 wrapper, `MainActivity`, `QRScannerActivity`, `BundleDownloader`, `DevMenuBottomSheet`, and real-time `PerformanceOverlay` (60 FPS HUD).
  - **Star Go Dev Server (`star go [file.star] [--port 8088]`)**: Instant local development server detecting primary WiFi/LAN IP, compiling `.starmobile` bundles on the fly, and rendering a scannable ANSI terminal QR code.
  - **Zero-Dependency Pure-Python QR Code Engine (`star_backend/mobile/android/qr.py`)**: ISO/IEC 18004:2015 byte-mode matrix generator with Reed-Solomon GF(256) error correction, rendering Unicode double-row blocks (`█`, `▀`, `▄`, ` `) and SVG outputs without pip dependencies.
  - **Fast Refresh Hot-Reloading**: SSE event stream detecting file modifications on the host and automatically reloading connected physical devices in under 20ms.
  - **Shake-to-Dev-Menu Gesture**: Integrated accelerometer sensor listener to trigger the floating Developer Options menu for instant app reload, performance HUD toggle, and server management.
  - **CLI Commands**: Added `star go`, `star build go` (builds `build/android/star_go-debug.apk`), and `star run go`.
  - **Android App Launcher Icons & Logo Subsystem**: Bundles official Star logo assets (`assets/star_mobile_icon.png` and `assets/star_logo.png`) across all standard Android launcher resolutions (`mipmap-mdpi`, `mipmap-hdpi`, `mipmap-xhdpi`, `mipmap-xxhdpi`, `mipmap-xxxhdpi`, `drawable`) with `android:icon="@mipmap/ic_launcher"` and `android:roundIcon="@mipmap/ic_launcher_round"` in `AndroidManifest.xml` and packages them into the APK and AAB distributions.

### Fixed
- **Parser Missing Import Bug (`star_engine/parser.py`)**: Fixed missing `Any` import in `_desugar_pipe` type annotation that caused `NameError: name 'Any' is not defined`.
- **Virtual DOM Style Unit Bug (`Star.js` · `star_js/star.js`)**: Fixed style assignment in `renderDOM` where numeric CSS values (width, height, padding, margin, radius) were missing `px` units.
- **Star.js Malformed Function Declaration (`star_js/star.js`)**: Fixed duplicate `renderDOM` signature accidentally interleaved before hook runtime definitions.
- **UI Boolean Evaluation Bug (`star_sdk/ui/__init__.py`)**: Implemented `_to_bool` helper resolving Star Language integer/decimal/null truthiness semantics so `0` correctly evaluates as falsy in conditional UI widgets.
- **Container Children Nested Flattening (`star_sdk/ui/__init__.py`)**: Implemented recursive `_flatten_children` preventing StarList, list, and null elements from corrupting virtual node trees.
- **Android CLI Hardcoded Entrypoint Bug (`star_engine/cli.py`)**: Eliminated unhandled `FileNotFoundError: Source file not found: 'main.star'` by integrating `_resolve_entry_file` across `build android`, `build apk`, `build aab`, `run android`, `deploy android`, and `release mobile`.

## [1.2.0] - 2026-08-30 (Official Developer Platform & Ecosystem Admin Console)

### Added
- **Flutter-Style Pure ZIP SDK Distribution (`STAR_PORTAL_ADMIN.md`)**:
  - Zero-installer portable archives: `Star-1.2.0-windows-x64.zip`, `Star-1.2.0-linux-x86_64.tar.gz`, `Star-1.2.0-macos-universal.zip`.
  - Cryptographic verification via dual SHA-256 and SHA-512 digests.
- **Automated In-Place Setup (`star setup`)**:
  - Added `star setup` command for instant portable PATH configuration.
- **Flagship Developer Portal Expansion (`web/portal/` · `www.shreeshop.in/star`)**:
  - The Star Book expanded to complete **20-Chapter Curriculum** covering syntax, OOP, functional patterns, UI, native targets, WebGPU, and security.
  - **Examples Gallery**: 6 canonical showcase apps (Dashboard, E-Commerce, Chat, Fitness, Vector Editor, 2D Game).
  - **Developer Tools Hub**: Unified showcase for Star CLI, Compiler, StarVM, LSP, Debugger, Formatter, DevTools, and Doctor.
  - **Interactive `star doctor` Web Dashboard**: Live in-browser diagnostics simulator with 10/10 health validation.
- **Dedicated Ecosystem Admin Console (`/star/admin`)**:
  - Authenticated admin platform with real-time telemetry metrics (48,291+ downloads, 3,842 developers).
  - Release Publisher Engine with automated checksum generation.
  - Package Registry Moderation and approval workflows.
  - Security & Audit Log monitoring with malware scans and signature audits.
  - Geolocation and country download analytics.

## [1.1.0] - 2026-08-30 (Developer Ecosystem & Official Star Portal)


### Added
- **Multi-Template Project Scaffolding Engine (`star_engine/project.py`)**:
  - Six canonical project templates: `cli`, `web`, `desktop`, `android`, `ios`, and `universal` (flagship).
  - CLI commands: `star new <name> [--template <type>]`.
- **Official Star Developer Portal & Live Multi-Target Playground (`www.shreeshop.in/star` · `web/portal/`)**:
  - Showcasing *"Built with Star WebAssembly"*.
  - 5-target live interactive playground (`Universal`, `CLI`, `Web`, `Desktop`, `Mobile`).
  - Production Download Center for Windows (MSI/ZIP), Linux (tar.gz/AppImage), macOS (.pkg), and Mobile starter kits.
  - The Star Book (12-chapter comprehensive curriculum) and interactive API reference.
- **Star Package Registry Subsystem (`star_runtime/registry.py`)**:
  - Full lifecycle commands: `star search`, `star install`, `star remove`, `star package`, `star publish`, `star update`.
  - Deterministic `.starpkg` container format and lockfile dependency synchronization.
- **WebGPU Hardware Acceleration Engine (`star_backend/webgpu/` · `STAR_WEBGPU.md`)**:
  - Additive WGSL shader pipeline (vertex transformation, SDF anti-aliased fragment, blur compute pass).
  - High-performance GPU draw call batching and instanced rendering.
- **Production Tooling & Certification**:
  - `star certify --ecosystem` verifying project templates, registry, WebGPU pipeline, and multi-platform compilation.

## [1.0.1] - 2026-08-30 (Production SDK & Distribution System)


### Added
- **Production SDK & Distribution System (`STAR_DISTRIBUTION.md`)**:
  - Clean binary SDK layout (`bin/star.exe`, `starc.exe`, `star-runtime.exe`, `lib/`, `sdk/`, `docs/`, `VERSION`, `star.manifest`).
  - **Source Exclusion Gate**: Strictly verifies zero `.py`, `.pyc`, or `__pycache__` files in the distributed production bundle.
- **Deterministic Archive & Secure Extraction Engine (`star_distribution/`)**:
  - Deterministic archive packaging with timestamp normalization and reproducible SHA-256 hashes (`star archive`).
  - Hardened Zip-Slip / path-traversal protection and atomic failure rollback (`star extract`).
- **Cross-Platform Automated Installer & PATH Management (`star_distribution/path_manager.py`)**:
  - Windows environment registry configuration and `WM_SETTINGCHANGE` broadcasting.
  - Linux/macOS binary link and shell configuration scripts.
- **Self-Update Subsystem (`star_distribution/updater.py`)**:
  - `star self-update` and `star self-update --check` with atomic staging and rollback.
- **Production Diagnostics & Certification**:
  - `star doctor --production` reporting binary status, PATH configuration, 0 source files, and checksums.
  - `star certify --production` executing the 15-gate production certification matrix.

## [1.0.0] - 2026-08-30 (General Availability)


### Added
- **Official Star 1.0.0 General Availability Production Release**:
  - Stable Universal Platform spanning Web (WASM + DOM), Native Desktop (macOS/Windows/Linux), Android (NDK/JNI + APK/AAB), and iOS (Swift/Metal + IPA).
- **Formal Star 1.x Compatibility Guarantee (`STAR_COMPATIBILITY.md`)**:
  - Full forward-compatibility guarantee across all future Star 1.x releases.
- **Star Package Registry & Ecosystem Subsystem (`star_runtime/registry.py`)**:
  - Official ecosystem package catalog (`http`, `sqlite`, `canvas2d`, `crypto`, `ui-icons`, `test-kit`).
  - CLI commands: `star search`, `star install <pkg>`, `star publish`, `star update`.
- **Official Star Developer Portal & Download Center (`web/portal/` · `www.shreeshop.in/star`)**:
  - Interactive multi-snippet Star playground running in WebAssembly.
  - Download Center for Windows (MSI/ZIP), Linux (tar.gz/AppImage), macOS (universal .pkg), and Mobile SDKs.
  - 12-Chapter "Learn Star" documentation curriculum.
- **20-Gate Star 1.0.0 Release Certification Engine (`star certify`)**:
  - Full automated production certification matrix.

## [0.9.0] - 2026-08-30 (Release Candidate)


### Added
- **Formal ABI & API Freeze (`STAR_ABI.md`)**:
  - Core Runtime ABI Version 1 and Mobile ABI Version 1 locked and frozen.
  - Universal `Mobile.*` device API contracts finalized across 10 modules.
  - Forward-compatibility guarantee across all future Star 1.x releases.
- **Runtime Hardening & Crash Fault Isolation (`star_runtime/mobile/isolation.py`)**:
  - `RuntimeFaultBarrier` preventing Star VM exceptions from crashing host native platforms.
  - Safe exception unwinding and memory autorelease guards for Android and iOS bridges.
- **Rendering Pipeline & 60 FPS Optimization (`star_backend/mobile/renderer.py`)**:
  - `RenderCommandOptimizer` with viewport culling, dirty rect invalidation, and batching.
  - Realistic RC performance criteria: mean & p95 frame time <= 16.67ms.
- **Android & iOS Release Candidate Compliance Suites**:
  - Google Play RC validation (Target SDK 34+, 64-bit ARM64 support, signed AAB structure).
  - Apple App Store RC validation (Privacy manifest, ARM64 Mach-O slices, iOS 15+ target).
- **Official Star Developer Portal & Playground (`web/portal/`)**:
  - Modern, responsive documentation center with live in-browser mobile runtime playground.
- **Automated Full-Stack Release Certification (`star certify`, `star doctor --rc`)**:
  - 7-gate certification pipeline evaluating ABI freeze, conformance, hardware, performance, packaging, and security.

## [0.8.7] - 2026-08-30


### Added
- **Dual-Device Hardware Verification & Platform Stabilization (`STAR_HARDWARE.md`)**:
  - Hardware discovery subsystem for connected physical devices, emulators, and simulators (`star devices`).
  - Standardized hardware capability probes (`star_backend/mobile/hardware/probes.py`).
  - Real-device multi-touch and gesture recognition verification suite (`tests/hardware/test_touch.py`, `test_multitouch.py`).
  - Safe area inset, notch, dynamic island, and orientation verification (`tests/hardware/test_safe_area.py`, `test_orientation.py`).
  - Lifecycle state machine and native low-memory warning delivery (`tests/hardware/test_lifecycle.py`, `test_memory.py`).
  - 60 FPS performance benchmarking & frame jitter profiler (`star_backend/mobile/hardware/metrics.py`).
  - Hardware test session recorder and diagnostic bundle exporter (`build/hardware/session-*/`).
  - Dual-device hardware test runner & comparison dashboard (`star test hardware`).

## [0.8.6] - 2026-08-30


### Added
- **Mobile Deployment, Signing & CI Pipeline (`STAR_RELEASE.md`)**:
  - Unified project configuration model in `star_engine/mobile_config.py`.
  - Secure Android debug and release signing profiles with automatic development keystore.
  - iOS code signing abstraction for development and distribution with provisioning profile management.
  - Artifact verification engine for APK, AAB, and IPA packages (`star verify`).
  - Cryptographic build provenance descriptors (`.build.json` and `.sha256`).
  - Unified release workflow command: `star release mobile`.
  - CI/CD workflow generator for GitHub Actions and GitLab CI (`star ci init`).

## [0.8.5] - 2026-08-30

### Added
- **Native Device Hardware SDK & Cross-Platform Conformance (`STAR_DEVICE_SDK.md`, `STAR_CONFORMANCE.md`)**:
  - Universal hardware APIs: `Mobile.Storage`, `Mobile.Battery`, `Mobile.Haptics`, `Mobile.Clipboard`, `Mobile.Screen`, `Mobile.Orientation`, `Mobile.Share`, `Mobile.Network`, `Mobile.Geolocation`, `Mobile.Camera`.
  - Provider architecture for Web, Desktop, Android, and iOS targets with identical observable semantics.
  - Capability security enforcement via `CapabilityManager` on every device invocation.
  - 10-module cross-platform conformance test suite (`star test --target all` / `star test --conformance`).

## [0.8.4] - 2026-08-30

### Added
- **iOS Native Backend & Apple Metal Bridge (`STAR_IOS.md`)**:
  - Swift / C ABI bridge (`StarNativeBridge.swift`, `StarRuntime.h`).
  - UIKit `StarViewController` lifecycle integration and Dynamic Island safe-area updates.
  - Apple Metal GPU rendering engine via MetalKit (`StarMetalView.swift`).
  - `UITouch` event translation to Star gestures.
  - Xcode project scaffolding and `.ipa` distribution container packaging.

## [0.8.3] - 2026-08-30

### Added
- **Android Native Backend & Dual APK/AAB Packaging (`STAR_ANDROID.md`)**:
  - Android NDK/JNI C++20 bridge (`star_jni_bridge.cpp`, `StarNativeBridge.java`).
  - `StarActivity` lifecycle controller and Android `MotionEvent` translation.
  - Hardware-accelerated `SurfaceView` renderer.
  - Dual artifact builder for `.apk` and `.aab` packages with automatic debug keystore signing.

## [0.8.0] - 2026-08-30

### Added
- **Formal Star Mobile Specification & Runtime ABI (`STAR_MOBILE.md`, `STAR_MOBILE_RUNTIME.md`)**:
  - Declarative mobile UI components (`safe_area`, `scroll_view`, `app_bar`, `bottom_navigation`, `switch`, `slider`, `action_sheet`).
  - Multi-touch gesture recognition subsystem (`Tap`, `Pan`, `Swipe`, `Pinch`, `Rotate`).
  - Portable `.starmobile` application container format with SHA-256 integrity verification.

## [0.7.0] - 2026-08-30

### Added
- **Developer Productivity Subsystems**:
  - Language Server Protocol (LSP) for VS Code / IDE integration.
  - Interactive Debugger (`star debug`) with breakpoints and step inspection.
  - Hot Module Reload & DevTools (`star dev`).
  - Official API Documentation Generator (`star doc`).
  - Comprehensive Environment & Toolchain Diagnostics (`star doctor`).

## [0.6.0] - 2026-08-30


### Added
- **Formal Star Desktop Specification (`STAR_DESKTOP.md`)**:
  - Authoritative specification for cross-platform desktop windowing and declarative layout engine.
- **Native Desktop Windowing & Layout Engine (`star_backend/desktop/`)**:
  - `DesktopWindow` abstraction supporting native GUI display and automated headless test execution.
  - Deterministic 2D layout calculation pass (`column`, `row`, `card`, `title`, `text`, `button`, `badge`, `input`, `progress`).
  - Interactive hit testing and automatic event dispatching.
- **Desktop Application Packaging & Distribution**:
  - Desktop bundle format (`.stardesktop`) combining IR bytecode with window metadata.
  - CLI integration: `star build desktop` and `star run desktop`.
  - Desktop verification test suite (`tests/test_desktop_backend.py`).

## [0.5.0] - 2026-08-30

### Added
- **Formal Star Web & UI Specifications (`STAR_WEB.md`, `STAR_UI.md`)**:
  - Authoritative specifications for WASM emission, declarative UI component model, and reactive state graph.
- **WebAssembly Compiler & Emitter (`star_backend/wasm/`)**:
  - Star IR to standard Wasm binary bytecode compiler.
  - Lightweight reactive DOM runtime (`runtime.js`).
- **Star SDK UI & Theme Subsystems (`star_sdk/ui/`, `star_sdk/theme/`)**:
  - Declarative components (`UI.title`, `UI.button`, `UI.input`, `UI.card`, etc.).
  - Multi-theme preset engine (`dark`, `light`, `cyberpunk`, `nord`).
- **Web CLI Toolchain**:
  - `star build web` and `star run web` dev server with hot build delivery.

## [0.4.0] - 2026-08-30

### Added
- **Formal Star Runtime ABI Specification (`STAR_RUNTIME.md`)**:
  - Runtime ABI Version 1 specification.
  - Tagged value representations, memory layout, and call frame conventions.
- **Controlled Native Foreign Function Interface (`use FFI` / `Star.FFI`)**:
  - Capability-gated native dynamic library loading (`FFI.load`).
  - Strict type marshalling between Star values and native C types (`Text` <-> `const char*`, `Integer` <-> `int64_t`, `Decimal` <-> `double`, `Boolean` <-> `bool`).
  - Safety boundary disallowing raw unchecked pointer manipulation.
- **Package Management Subsystem (`star_runtime/packages.py`)**:
  - Project dependency management in `star.toml`.
  - Deterministic lockfile generation (`star.lock`) with SHA-256 integrity checksums.
  - Package distribution container packer (`.starpkg`).
  - CLI commands: `star add`, `star remove`, `star install`, `star pack`.
- **Physical Separation of Compiler & Runtime**:
  - `star_engine/` (Compiler Frontend & Virtual Machine) and `star_runtime/` (Runtime ABI, FFI, and Package Resolver).

## [0.3.0] - 2026-08-30

### Added
- **Dedicated Star IR Specification (`STAR_IR.md`)**:
  - Typed stack-machine opcode set (Core VM & Runtime ABI opcodes).
- **AST → Star IR Bytecode Compiler (`compiler.py`)**:
  - Bytecode serialization and deserialization in `.starb` binary container format.
- **Star Bytecode Virtual Machine (`vm.py`)**:
  - Stack execution engine with call frames, local registers, and native Standard Library integration.
- **Dual-Engine Conformance Verification**:
  - Test suite asserting 100% semantic parity between Reference Interpreter and StarVM.

## [0.2.0] - 2026-08-30

### Added
- **Object-Oriented System**:
  - `class`, `property`, and methods.
  - Explicit `self` referencing (`self.property`, `self.method()`).
  - Instantiation supporting named arguments (`User(name = "Alex")`) and positional arguments.
  - Strict property existence validation.
- **Module System & Standard Library**:
  - `use <ModuleName>` and `use "file.star"` with cyclic import prevention.
  - Standard Library modules: `Math`, `Time`, `String`, `IO`, `System`.
- **Semantic Analyzer & Linter**:
  - Static detection of unused variables, unreachable code, unclosed/illegal loop jumps (`break`/`continue`).
  - Separation between fatal errors and non-fatal `StarWarning` diagnostics.
  - Support for `star check <file> [--strict]`.
- **Official Code Formatter**:
  - Canonical 4-space indentation and expression normalization.
  - Support for `star format <file> [--write] [--check]`.
- **Expanded Conformance Suite**:
  - Conformance test cases for classes, state mutation, and module imports.

## [0.1.0-draft] - 2026-08-30

### Added
- Official **Star Language Specification** (`STAR_SPEC.md`).
- **Star Syntax Guide** (`STAR_SYNTAX.md`).
- **Star Architecture Blueprint** (`STAR_ARCHITECTURE.md`).
- **Star Development Roadmap** (`STAR_ROADMAP.md`).
- Core language design:
  - Lexical grammar (identifiers, numbers, texts, escape sequences, comments).
  - Explicit block structures (`app`, `function`, `if`, `while`, `repeat`, `for`, `try ... catch`).
  - Scoping model (`variable`, `constant`, lexical closures).
  - Expression operator precedence with Pratt parsing.
  - Standardized diagnostic error categories (`Star Syntax Error`, `Star Type Error`, `Star Name Error`, `Star Runtime Error`, etc.).
