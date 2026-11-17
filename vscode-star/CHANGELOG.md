# Change Log — Star Programming Language VS Code Extension

All notable changes to the **Star Programming Language Extension** (`star-programming-language`) will be documented in this file.

---

## [1.3.0] — 2026-11-13

### 🚀 Major Enhancements & New Features

- **📖 Interactive Hover Documentation**:
  - Full tooltips for all Star keywords (`whenever`, `otherwise`, `unless`, `give back`, `repeat`, `times`, `iteration`, `set ... to`, `increase ... by`, `decrease ... by`, `remember ... as`, `variable`, `let`, `constant`, `show`, `say`, `input`).
  - **In-Document Symbol Resolver**: Automatically discovers user-declared functions, variables, parameters, and components, showing their declaration signature, doc-comments, file line numbers, and types.
  - Comprehensive Flutter UI widget docs (`Scaffold`, `AppBar`, `Container`, `Card`, `When`, `ElevatedButton`, `Column`, `Row`, `BottomNavigationBar`, etc.).
  - Native Android hardware & platform APIs (`WallpaperManager`, `GoogleBillingClient`, `Gyroscope`, `Haptics`, `Sensor`, `EdgeInsets`, `Colors`, `Icons`).

- **🎨 Enhanced TextMate Color Syntax Highlighting (`star.tmLanguage.json`)**:
  - Re-architected scope classification matching VS Code Modern Dark and Light themes.
  - Blue (`storage.type`) for declarations (`function`, `variable`, `let`, `constant`, `app`, `component`).
  - Purple (`keyword.control`) for control flow (`if`, `while`, `for`, `repeat`, `return`, `give back`, `whenever`, `otherwise`, `unless`, `end`).
  - Yellow (`support.function.builtin`) for console built-ins (`show`, `say`, `input`, `print`).
  - Orange (`string.quoted`) for double and single quoted strings, plus in-string `{var}` interpolation highlighting.
  - Light Green (`constant.numeric`) for integer, float, and hex numbers.
  - Green (`comment.line`) for `#` and `//` comments.

- **🛡️ Workspace Trust & Restricted Mode Compatibility**:
  - Added `capabilities.untrustedWorkspaces.supported = true` so the extension is always fully functional even when opening single files without a workspace folder.
  - Configured `extensionKind: ["ui", "workspace"]` for optimal responsive local UI rendering.

- **🌟 Official Brand File Icon Theme**:
  - Included `star-icon-theme.json` with dedicated vector emblems for `.star` source files, `.starb` compiled bytecode, and `.starmobile` mobile bundles.

- **🤖 Android Build System Integration**:
  - Direct integration with local Android SDK (TargetSDK 34).
  - One-click build commands for both Android APK and Google Play App Bundle (AAB).

---

## [1.2.0] — 2026-11-13

- Initial release of official Star Language extension.
- Syntax highlighting and code snippet contributions.
- Real-time diagnostics with Star Doctor.
- Terminal UI preview (`star preview`).
- Bytecode compiler integration (`star compile`).
