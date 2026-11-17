# ⭐ The Complete Star Programming Language Specification & Developer Reference Manual
**Official Version:** 1.2.0 General Availability (GA)  
**Authoritative Reference:** Star Language Open Source Project  
**Target Runtimes:** Web (WASM/WebGPU), Desktop (Windows/macOS/Linux), Android (NDK/JNI + APK/AAB), iOS (Metal + Swift + IPA), Terminal (TUI)

---

## 📑 Table of Contents

1. [Philosophy & Core Principles](#1-philosophy--core-principles)
2. [Lexical Structure & Conventions](#2-lexical-structure--conventions)
3. [Variables, Constants & Data Types](#3-variables-constants--data-types)
4. [Operators & Expressions](#4-operators--expressions)
5. [Control Flow: Natural & Traditional](#5-control-flow-natural--traditional)
6. [Functions, Closures & Methods](#6-functions-closures--methods)
7. [Object-Oriented Programming (Classes & Properties)](#7-object-oriented-programming-classes--properties)
8. [Reactive Component Architecture](#8-reactive-component-architecture)
9. [Flutter Universal Declarative UI (Zero-JS)](#9-flutter-universal-declarative-ui-zero-js)
10. [Native Mobile & Hardware SDK (`Mobile.*`)](#10-native-mobile--hardware-sdk-mobile)
11. [Google Play Billing & In-App Purchases Subsystem](#11-google-play-billing--in-app-purchases-subsystem)
12. [Android WallpaperManager System Service](#12-android-wallpapermanager-system-service)
13. [Compiler, Bytecode (`.starb`) & StarVM Architecture](#13-compiler-bytecode-starb--starvm-architecture)
14. [Star CLI Toolchain Reference](#14-star-cli-toolchain-reference)
15. [IDE & Shell Integration (VS Code & Windows Explorer)](#15-ide--shell-integration-vs-code--windows-explorer)
16. [Complete Production Example: 3D Parallax Wallpaper App](#16-complete-production-example-3d-parallax-wallpaper-app)
17. [AI Prompting Guide: How to Prompt ChatGPT & Antigravity for Star](#17-ai-prompting-guide-how-to-prompt-chatgpt--antigravity-for-star)

---

## 1. Philosophy & Core Principles

> **"Simple to learn. Powerful to build. Beautiful to read. Difficult to misuse."**

1. **Zero-Punctuation Noise**: No semicolons (`;`), no mandatory curly braces (`{}`), and no confusing type gymnastics.
2. **Deterministic Blocks**: Every scope block (`app`, `class`, `component`, `function`, `whenever`, `if`, `while`, `for`, `repeat`) cleanly terminates with `end`.
3. **Dual Syntax Compatibility**: Supports standard programming syntax alongside **Haven Natural English** syntax (`whenever ... otherwise`, `give back`, `remember`, `increase ... by`).
4. **Universal Declarative UI**: Flutter-style declarative widget hierarchy with Material 3 and Cupertino primitives, running natively with **zero JavaScript or Node.js runtime**.
5. **Write Once, Run Everywhere**: Single codebase deterministically targets Android APK/AAB, iOS IPA, Desktop executables, and WebAssembly.

---

## 2. Lexical Structure & Conventions

### File Extensions
- **`.star`**: Source code files (UTF-8 plain text).
- **`.starb`**: Compiled binary bytecode executed by the StarVM stack machine.
- **`.starmobile`**: Mobile application package / standalone bundle.

### Comments
Comments begin with `#` or `//` and extend to the end of the line. Multi-line block comments use `/* ... */`.
```star
# Single line comment
// Also a single line comment
/* Multi-line
   block comment */
```

### Identifiers
Identifiers start with an ASCII letter or underscore (`[a-zA-Z_]`) followed by alphanumeric characters or underscores. Keywords cannot be used as variable names.

---

## 3. Variables, Constants & Data Types

### Mutable Variables
Declared using `variable` or `let`:
```star
variable score = 100
score = 150

let username = "Alex"
username = "Jordan"
```

### Immutable Constants
Declared using `constant`:
```star
constant APP_NAME = "Nova3D Wallpapers"
constant PI = 3.1415926535
```

### Haven Natural Declarations
```star
set userCount to 10
increase userCount by 5
decrease userCount by 2
remember userTheme as "Dark"
```

### Primitive Types

| Type | Syntax Examples | Description |
| :--- | :--- | :--- |
| **Text (String)** | `"Hello"`, `'World'`, `"Value: ${count}"` | UTF-8 encoded string with interpolation |
| **Integer** | `0`, `42`, `-10`, `0xFF` | 64-bit signed integer |
| **Decimal (Float)** | `3.14`, `-0.05`, `1.5e3` | IEEE 754 64-bit floating point number |
| **Boolean** | `true`, `false` | Boolean truth values |
| **Null** | `null`, `nil` | Represents the absence of a value |

### Collections

#### Lists (Dynamic Arrays)
```star
variable categories = ["3D Parallax", "AMOLED", "Anime", "Cyberpunk"]

show(categories[0])        # Access: "3D Parallax"
categories[1] = "Minimal"  # Reassign
```

#### Maps (Key-Value Dictionaries)
```star
variable wallpaper = {
    "title": "Quantum Singularity 3D",
    "category": "Space",
    "isPremium": true,
    "resolution": "4K UHD"
}

show(wallpaper["title"])   # "Quantum Singularity 3D"
```

---

## 4. Operators & Expressions

### Arithmetic
`+`, `-`, `*`, `/`, `%`
```star
variable total = (100 * 2) + 50 - (10 / 2)
```

### Text Concatenation & Interpolation
```star
variable greeting = "Welcome to " + APP_NAME
variable message = "Active user count: ${userCount}"
```

### Comparison & Relational
`==`, `!=`, `<`, `<=`, `>`, `>=`
```star
whenever score >= 100
    show("High score achieved!")
end
```

### Logical Operators
`and`, `or`, `not`
```star
whenever isSubscribed and not isExpired
    show("Access VIP Vault")
end
```

### Pipeline Operator (`|>`)
Chains expressions sequentially:
```star
rawText |> String.trim |> String.toUpper |> show
```

---

## 5. Control Flow: Natural & Traditional

### The `whenever / otherwise` Construct (Recommended)
Idiomatic Star favors natural English conditional branching:
```star
whenever user.isVip
    show("VIP Member: Access Granted")
otherwise
    show("Standard User: Purchase Required")
end
```

### Traditional `if / else if / else`
```star
if rating >= 4.8
    show("Masterpiece Tier")
else if rating >= 4.0
    show("Featured Tier")
else
    show("Standard Tier")
end
```

### The `repeat` Loop
Executes a block an exact number of times:
```star
repeat 3
    show("Sparkle ✨")
end
```

### The `for-in` Loop
Iterates over lists and maps:
```star
for category in ["Neon", "Space", "Anime", "Nature"]
    show("Loading category: " + category)
end
```

### The `while` Loop
```star
variable retries = 0
while retries < 3
    show("Attempt: " + retries)
    retries = retries + 1
end
```

### Loop Control
`break` terminates the loop immediately; `continue` skips to the next iteration:
```star
for i in [1, 2, 3, 4, 5]
    if i == 2
        continue
    end
    if i == 4
        break
    end
    show(i)
end
```

---

## 6. Functions, Closures & Methods

Functions are declared with `function` and end with `end`. Values are returned via `give back` or `return`:

```star
function calculateParallax(tiltAngle, depthScale)
    variable offset = tiltAngle * depthScale
    give back offset
end

show(calculateParallax(2.5, 8.0)) # 20.0
```

### Closures & First-Class Functions
```star
function createMultiplier(factor)
    function multiply(value)
        give back value * factor
    end
    give back multiply
end

variable doubleIt = createMultiplier(2)
show(doubleIt(50)) # 100
```

### Lambdas / Anonymous Functions
```star
variable callback = (x, y) -> x + y
show(callback(10, 20)) # 30
```

---

## 7. Object-Oriented Programming (Classes & Properties)

Classes declare properties and methods. Methods access properties via `self`:

```star
class WallpaperModel

    property id
    property title
    property url
    property isPremium = false
    property downloadsCount = 0

    function recordDownload()
        self.downloadsCount = self.downloadsCount + 1
        show("Downloads for " + self.title + ": " + self.downloadsCount)
    end

    function getFormattedLabel()
        whenever self.isPremium
            give back self.title + " [VIP 👑]"
        otherwise
            give back self.title + " [FREE]"
        end
    end

end

# Instantiation using named arguments
variable item = WallpaperModel(
    id = "wp_001",
    title = "Cyberpunk Neon City",
    url = "https://images.unsplash.com/photo-1",
    isPremium = true
)

item.recordDownload()
show(item.getFormattedLabel())
```

---

## 8. Reactive Component Architecture

For dynamic, state-driven interfaces, Star provides reactive `component` structures:

```star
component WallpaperViewer

    state activeTab = "All"
    state isLiked = false
    state gyroEnabled = true

    computed displayTitle()
        give back "Category: " + self.activeTab
    end

    function toggleLike()
        self.isLiked = not self.isLiked
    end

    render()
        give back Scaffold(
            appBar = AppBar(title = Text(self.displayTitle())),
            body = Center(
                child = ElevatedButton(
                    child = Text(self.isLiked ? "❤️ Liked" : "🤍 Like"),
                    onPressed = () -> self.toggleLike()
                )
            )
        )
    end

end
```

---

## 9. Flutter Universal Declarative UI (Zero-JS)

Star compiles a Flutter declarative widget tree directly to native bytecode without JavaScript:

```star
app Nova3DApp

use Material
use Flutter

function build()
    give back Scaffold(
        backgroundColor = Color(0xFF0F172A),
        appBar = AppBar(
            title = Text("Nova3D Wallpapers"),
            backgroundColor = Colors.indigo,
            elevation = 4.0
        ),
        body = Column(
            crossAxisAlignment = CrossAxisAlignment.start,
            children = [
                Text("Trending Today", style = TextStyle(fontSize = 24.0, fontWeight = FontWeight.bold, color = Colors.white)),
                SizedBox(height = 12.0),
                GestureDetector(
                    onTap = () -> show("Wallpaper tapped"),
                    child = Container(
                        height = 320.0,
                        margin = EdgeInsets.symmetric(horizontal = 16.0),
                        decoration = BoxDecoration(
                            borderRadius = BorderRadius.circular(20.0),
                            boxShadow = [
                                BoxShadow(color = Colors.black87, blurRadius = 18.0)
                            ]
                        ),
                        child = Stack(
                            children = [
                                Image.network("https://images.unsplash.com/photo-1", fit = BoxFit.cover),
                                Positioned(
                                    bottom = 16.0,
                                    left = 16.0,
                                    child = Text("Neon Samurai 4K", style = TextStyle(color = Colors.white, fontSize = 20.0))
                                )
                            ]
                        )
                    )
                )
            ]
        )
    )
end

end
```

### Common Declarative Widgets
- **Structural**: `Scaffold`, `AppBar`, `BottomNavigationBar`, `FloatingActionButton`, `SafeArea`
- **Layout**: `Column`, `Row`, `Stack`, `Positioned`, `Container`, `Padding`, `Center`, `Expanded`, `SizedBox`, `Wrap`, `Spacer`
- **Interactive**: `GestureDetector`, `ElevatedButton`, `InkWell`, `CupertinoButton`
- **Content**: `Text`, `Image`, `Icon`, `Card`, `ListView`, `GridView`
- **Conditional**: `When(condition, trueWidget, falseWidget)`, `SwitchCase`, `Visibility`, `Opacity`
- **Styling**: `Colors`, `Icons`, `BorderRadius`, `EdgeInsets`, `BoxDecoration`, `TextStyle`, `LinearGradient`, `BoxShadow`

---

## 10. Native Mobile & Hardware SDK (`Mobile.*`)

Star provides unified hardware access across Android and iOS via `Mobile.Hardware`:

```star
# Gyroscope 3D Parallax Tracking
variable gyroListener = Mobile.Hardware.Sensor.listenGyroscope((pitch, roll, yaw) ->
    variable offsetX = pitch * 12.0
    variable offsetY = roll * 12.0
    updateParallax(offsetX, offsetY)
end)

# Haptic Feedback & Vibration
Mobile.Hardware.Haptics.vibrate(35) # 35ms light impact

# Battery & Device Metrics
variable batteryLevel = Mobile.Hardware.Battery.level() # 0 to 100
variable isCharging = Mobile.Hardware.Battery.isCharging()

# System Clipboard
Mobile.Hardware.Clipboard.setText("https://wallpaper.app/dl/neon")
```

---

## 11. Google Play Billing & In-App Purchases Subsystem

Full native support for Google Play BillingClient v7.0.0:

```star
class GoogleBillingManager

    property billingClient

    function init(packageName)
        self.billingClient = GoogleBillingClient(
            targetPackage = packageName,
            enablePendingPurchases = true
        )
    end

    function purchaseMonthlyVip()
        variable result = self.billingClient.launchSubscriptionFlow("nova_vip_monthly")
        whenever result["status"] == "SUCCESS"
            show("Subscription active! Bonus coins granted: +200")
            give back true
        otherwise
            show("Purchase cancelled or failed.")
            give back false
        end
    end

    function buyCoinPack(packSku)
        # Sku examples: "coins_pack_500", "coins_pack_1500"
        variable result = self.billingClient.launchPurchaseFlow(packSku)
        give back result
    end

end
```

---

## 12. Android WallpaperManager System Service

Direct integration with the Android OS `WallpaperManager` API:

```star
class AndroidWallpaperBridge

    constant FLAG_SYSTEM = 1 # Home Screen
    constant FLAG_LOCK   = 2 # Lock Screen
    constant FLAG_BOTH   = 3 # Home & Lock Screens

    function setWallpaper(imageUrl, targetFlag)
        whenever targetFlag == self.FLAG_SYSTEM
            show("Setting Home Screen Wallpaper: " + imageUrl)
            give back AndroidWallpaperService.setWallpaper(imageUrl, 1)
        otherwise whenever targetFlag == self.FLAG_LOCK
            show("Setting Lock Screen Wallpaper: " + imageUrl)
            give back AndroidWallpaperService.setWallpaper(imageUrl, 2)
        otherwise
            show("Setting Both Screens: " + imageUrl)
            give back AndroidWallpaperService.setWallpaper(imageUrl, 3)
        end
    end

end
```

---

## 13. Compiler, Bytecode (`.starb`) & StarVM Architecture

```
Star Source (.star)
      │
      ▼
┌──────────────┐     AST     ┌────────────────────┐
│    Lexer     │ ──────────> │       Parser       │
└──────────────┘             └────────────────────┘
                                       │
                                       ▼
                             ┌────────────────────┐
                             │ Semantic Analyzer  │ (Type safety, linting, unused variables)
                             └────────────────────┘
                                       │
                                       ▼
                             ┌────────────────────┐
                             │   Star Compiler    │
                             └────────────────────┘
                                       │
                                       ▼
                             Bytecode Binary (.starb)
                                       │
                                       ▼
┌────────────────────────────────────────────────────────┐
│                        StarVM                          │
│  - Tagged Value Layout (64-bit Core ABI v1)            │
│  - 32-bit Aligned Draw Operations (Mobile ABI v1)      │
│  - Call Frames, Stack Operations, Memory Safety        │
└────────────────────────────────────────────────────────┘
```

---

## 14. Star CLI Toolchain Reference

```bash
# Running & Previewing
star run <file.star>                 # Execute directly on StarVM
star preview <file.star>             # Interactive TUI layout preview
star repl                            # Launch interactive Star REPL terminal

# Quality & Verification
star check <file.star>               # Run static analyzer and linter
star format <file.star>              # Auto-format source code
star test                            # Run full automated test suite (219 certified tests)
star doctor                          # Complete toolchain diagnostic check

# Compilation & Mobile Packaging
star compile <file.star>             # Compile to .starb binary bytecode
star build apk                       # Build signed release Android APK
star build aab                       # Build Google Play Android App Bundle
star build ipa                       # Build iOS IPA (Star Inbuild System)
star deploy android                  # One-click install to USB device via ADB

# Shell & Tooling Setup
star register                        # Register Windows File Explorer icons & context menus
star vscode                          # Install / update official VS Code extension
```

---

## 15. IDE & Shell Integration

### Visual Studio Code
- **Official Extension**: `star-lang.star-programming-language` on the Visual Studio Marketplace.
- **Shortcuts**:
  - `F5`: Run active file (`star.run`)
  - `Shift + F5`: Preview UI in TUI (`star.preview`)
  - `Ctrl + Shift + C`: Run Star Doctor diagnostics (`star.check`)
- **Features**: Syntax highlighting, live inline diagnostics in Problems panel, rich snippets, hover documentation, and status bar control hub.

### Windows File Explorer
- Native multi-resolution icons for `.star` (source), `.starb` (bytecode), and `.starmobile` (bundles).
- Right-click context menus: "Run with Star", "Compile with Star", "Check Syntax with Star Doctor".

### Google Antigravity Agent Ecosystem
- Pre-installed plugin at `~/.gemini/config/plugins/star-language/`.
- Equips AI pair programmers to write, build, test, and debug Star applications automatically.

---

## 16. Complete Production Example: 3D Parallax Wallpaper App

```star
app Nova3DWallpaperApp

use Material
use Flutter
use "android_service.star"
use "google_billing.star"

variable currentCategory = "Cyberpunk"
variable activeWallpaper = {
    "title": "Quantum Singularity 3D",
    "url": "https://images.unsplash.com/photo-quantum",
    "isVip": true
}

function applyWallpaper(targetFlag)
    AndroidWallpaperService.setWallpaper(activeWallpaper["url"], targetFlag)
    AndroidHapticService.vibrate(30)
    show("Applied: " + activeWallpaper["title"])
end

function handleVipPurchase()
    variable billing = GoogleBillingClient(targetPackage = "com.anig.nova3d.wallpapers")
    variable result = billing.launchSubscriptionFlow("nova_vip_monthly")
    whenever result["status"] == "SUCCESS"
        show("VIP Unlocked! 👑")
    otherwise
        show("Purchase canceled.")
    end
end

function build()
    give back Scaffold(
        backgroundColor = Color(0xFF0F172A),
        appBar = AppBar(
            title = Text("🌟 Nova3D Wallpapers"),
            backgroundColor = Colors.indigo
        ),
        body = Center(
            child = Column(
                mainAxisAlignment = MainAxisAlignment.center,
                children = [
                    Text(activeWallpaper["title"], style = TextStyle(fontSize = 24.0, fontWeight = FontWeight.bold, color = Colors.white)),
                    SizedBox(height = 16.0),
                    ElevatedButton(
                        child = Text("Apply to Home & Lock Screens"),
                        onPressed = () -> applyWallpaper(3)
                    ),
                    SizedBox(height = 8.0),
                    ElevatedButton(
                        child = Text("Unlock All VIP Wallpapers ($2.99/mo)"),
                        onPressed = () -> handleVipPurchase()
                    )
                ]
            )
        )
    )
end

end
```

---

## 17. AI Prompting Guide: How to Prompt ChatGPT & Antigravity for Star

When asking an AI model (such as ChatGPT, Claude, or Antigravity) to generate Star code, include this prompt specification to guarantee correct syntax:

```text
You are an expert Star Programming Language (v1.2.0 GA) engineer.
Follow these mandatory syntax rules for Star (.star):
1. NO curly braces ({}) for blocks. Every block (app, class, component, function, whenever, if, while, for, repeat) MUST end with 'end'.
2. NO semicolons (;).
3. Use 'whenever <condition>' and 'otherwise' for natural branching, or 'if' / 'else'.
4. Return values with 'give back <expr>' or 'return <expr>'.
5. Variables are declared with 'variable name = val' or 'let name = val'. Constants use 'constant NAME = val'.
6. Declarative Flutter UI uses Scaffold(...), AppBar(...), Column(...), Row(...), Container(...), When(cond, trueW, falseW).
7. Native Android services use 'WallpaperManager.setWallpaper(url, flag)' and 'GoogleBillingClient'.
```

---
*Copyright © 2026 Star Language Open Source Project. All specifications conform to ABI v1.0 Production Standard.*

