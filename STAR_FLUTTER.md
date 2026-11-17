# 🌟 STAR FLUTTER & 74,600+ UI COMPONENTS WITH HAVEN SYNTAX
**Specification Version: 1.0.0 GA**  
**Status: Authoritative Standard for Star Flutter Engine with Haven (Heaven Language) Natural English Syntax**

---

## 1. Vision & Architecture Philosophy

Star combines the declarative reactive UI power of **Flutter** with the natural, human-readable expressiveness of **Haven (Heaven Language)** into an independent, universal programming language and cross-platform ecosystem.

### Key Pillars:
1. **Haven (Heaven Language) Natural English Syntax**:
   - Write software that reads like normal, intuitive English.
   - Declarative assignments: `set count to 0`, `let port be 8080`, `remember host as "localhost"`.
   - Natural mutations: `increase count by 1`, `decrease quota by 5`.
   - String interpolation: `say "Current count is {count}"`.
   - Conditionals: `whenever count is greater than 10: ... otherwise: ... end`, `unless offline: ... end`.
   - Natural comparisons: `is equal to`, `is not equal to`, `is greater than`, `is less than`, `is at least`, `is at most`, `is`.
   - Functional pipelines: `"  hello  " |> trim(_) |> uppercase(_)`.
   - Immutable records: `durable record Packet: ... end` with `.odcs_hash()`.
   - Functions: `define add(a, b): give back a + b end` and `to onClick(): increase count by 1 end`.
2. **Flutter-Style Widget Tree**:
   - Everything in the UI is an immutable widget tree (`Widget`, `StatelessWidget`, `StatefulWidget`, `State`, `BuildContext`).
3. **Pure Native Execution (Zero JavaScript / Node.js Overhead)**:
   - **Native Desktop (Windows, macOS, Linux)**: Direct2D/Canvas hardware 2D rendering with anti-aliasing, rounded corners, soft drop shadows, and linear gradients.
   - **Native Android (NDK/JNI + SurfaceView)**: Direct surface rendering via API 34+ with APK and AAB builders.
   - **Native iOS (Swift + Apple MetalKit)**: Direct Metal GPU command stream pipeline with IPA packaging.
   - **Native Web (WebAssembly + WebGPU SDF)**: Direct GPU shaders compiled to WASM bytecode without HTML DOM or JavaScript framework bottlenecks (identical to Flutter Web CanvasKit/Impeller).
   - **Terminal UI (TUI)**: 24-bit TrueColor ANSI box-drawing renderer with 60 FPS update budgets.
4. **Massive 60,000+ UI Component Catalog**:
   - Over **74,600+ registered UI components and vector glyphs** instantly accessible, searchable, and natively renderable.

---

## 2. Declarative UI Component Model in Haven Syntax

### 2.1 The Widget Hierarchy in Haven

Widgets are imported using `use Flutter`, `use Material`, `use Cupertino`, or `use Widgets`:

```haven
// 🌟 Star Native UI - Counter Application
// Authored in Haven (Heaven Language) Natural English Syntax

use Flutter
use Material
use Icons
use Colors

component FlutterCounter:
    remember count as 0

    to increment():
        increase count by 1
    end

    to decrement():
        decrease count by 1
    end

    render:
        Scaffold(
            appBar: AppBar(
                title: "🌟 Star Native UI · Haven Syntax",
                backgroundColor: Colors.indigo
            ),
            body: Center(
                child: Column(
                    children: [
                        Text("You have pushed the button this many times:"),
                        SizedBox(height: 8),
                        Text("Count: {count}"),
                        SizedBox(height: 20),
                        Row(
                            children: [
                                ElevatedButton("- Decrement", to ():
                                    decrease count by 1
                                end),
                                SizedBox(width: 16),
                                ElevatedButton("+ Increment", to ():
                                    increase count by 1
                                end)
                            ]
                        )
                    ]
                )
            ),
            floatingActionButton: FloatingActionButton(to ():
                increase count by 1
            end)
        )
    end
end

app CounterApp:
    FlutterCounter()
end
```

---

## 3. Supported Widget Suites

### 3.1 Material Design 3 (Google M3)
- **App Shell & Surfaces**: `MaterialApp`, `Scaffold`, `AppBar`, `BottomNavigationBar`, `NavigationBar`, `NavigationRail`, `Drawer`, `BottomAppBar`, `FloatingActionButton`.
- **Buttons**: `ElevatedButton`, `FilledButton`, `FilledTonalButton`, `OutlinedButton`, `TextButton`, `IconButton`, `SegmentedButton`.
- **Input & Controls**: `TextField`, `Checkbox`, `Switch`, `Slider`, `RangeSlider`, `Radio`, `Chip`, `ActionChip`, `FilterChip`.
- **Surfaces & Feedback**: `Card`, `Badge`, `ListTile`, `CircularProgressIndicator`, `LinearProgressIndicator`, `SnackBar`, `AlertDialog`, `BottomSheet`, `TabBar`.

### 3.2 Cupertino (Apple iOS)
- **App Shell & Surfaces**: `CupertinoApp`, `CupertinoPageScaffold`, `CupertinoNavigationBar`, `CupertinoTabBar`, `CupertinoTabScaffold`.
- **Buttons & Controls**: `CupertinoButton`, `CupertinoTextField`, `CupertinoSwitch`, `CupertinoSlider`, `CupertinoSegmentedControl`, `CupertinoActivityIndicator`.

### 3.3 Fluent UI (Desktop Windows)
- **App Shell & Surfaces**: `FluentApp`, `NavigationView`, `Acrylic`, `Mica`, `Expander`, `InfoBar`, `ContentDialog`.

### 3.4 Foundation Layout Widgets
- `Container`, `Padding`, `Center`, `Align`, `SizedBox`, `Expanded`, `Spacer`, `Row`, `Column`, `Stack`, `Positioned`, `Wrap`, `ListView`, `GridView`, `SingleChildScrollView`, `Text`, `Icon`, `Image`, `Divider`, `GestureDetector`, `AnimatedContainer`, `Hero`.
- **Geometry & Styling**: `EdgeInsets.all(16)`, `EdgeInsets.symmetric(vertical: 8, horizontal: 16)`, `BorderRadius.circular(12)`, `TextStyle(...)`, `BoxDecoration(...)`.

---

## 4. The 60,000+ UI Component Catalog

Star includes an indexed, high-performance Component Catalog with **74,600+ components** (`use Catalog` or `use Widgets`):

### Catalog Breakdown:
| Category | Source / Breakdown | Count |
|---|---|---|
| **Google Material Symbols** | 70 core glyphs × 5 styles (Filled, Outlined, Rounded, Sharp, TwoTone) × 10 colors × 5 sizes | **17,500** |
| **Apple Cupertino SF Symbols** | 37 SF glyphs × 10 colors × 5 sizes × 2 variants | **3,700** |
| **Universal Base Widgets** | 30 base widgets × 10 design systems × 10 colors × 5 sizes | **15,000** |
| **Domain Surface Cards & Kits** | 15 card types × 10 themes × 10 colors × 6 state variants | **9,000** |
| **DataViz, Grids, Media & FinTech** | 14 advanced widgets × 10 themes × 10 colors × 6 states × 2 layouts | **16,800** |
| **Extended Permutations & Icons** | Additional Lucide, FontAwesome, and theme variants | **12,600+** |
| **TOTAL REGISTERED** | **Authoritatively Indexed & Native Renderable** | **74,600+** |

### Using the Catalog in Haven Syntax:
```haven
use Catalog
use Widgets

// Retrieve pre-styled themed component
let myButton be Catalog.get("Aurora_Button_Indigo_Md")
let myBadge be Catalog.get("Cyberpunk_Badge_Rose_Lg")
let myChart be Catalog.get("Nord_CandlestickChart_Emerald_Active_Compact")
```

---

## 5. CLI Tooling & Commands

```bash
# Launch interactive Flutter demo
star flutter demo

# Count registered native UI components (74,600+)
star widgets count

# Search 74,600+ component library
star widgets search button
star widgets search chart
star widgets search card

# Inspect a component specification
star widgets inspect Aurora_Button_Indigo_Md

# Preview any Star Flutter app in terminal TUI
star preview examples/flutter_counter.star
star preview examples/flutter_showcase.star

# Run natively on Desktop, Android, iOS, or WebGPU
star run desktop
star build apk
star build ipa
star build wasm
```

---

## 6. Zero JavaScript Guarantee

Star does NOT require Node.js, npm, JavaScript runtimes, or browser wrappers to execute applications.  
All applications compile directly to native host executables, mobile binaries (APK/AAB/IPA), WebAssembly bytecode (`.wasm`), or 24-bit TrueColor ANSI terminal streams.
