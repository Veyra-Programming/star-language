---
name: star-lang
description: Full developer instructions for the Star Programming Language. Use when authoring, compiling, building, testing, or debugging Star source code (.star), bytecode (.starb), Flutter universal UI, or Android applications.
---

# Star Programming Language Skill

The **Star Programming Language** is a modern, high-performance universal programming language designed for zero-JS Flutter UI, cross-platform compilation, and native mobile applications.

## Common CLI Commands

- `star run <file.star>`: Execute Star source directly on the StarVM stack machine.
- `star preview <file.star>`: Render declarative UI in Terminal User Interface (TUI).
- `star check <file.star>`: Run semantic validation, AST analysis, and type checking.
- `star compile <file.star>`: Compile Star source to `.starb` binary bytecode.
- `star test`: Execute test suites and conformance matrices.
- `star doctor`: Verify toolchain health, Android SDK, and environment setup.
- `star build apk`: Build release Android APK package.
- `star deploy android`: Deploy APK to attached physical device or emulator.
- `star register`: Register Windows File Explorer associations and context menus.
- `star vscode`: Install or update the official VS Code extension.

## Idiomatic Star Syntax

### Variables & Functions
```star
variable score = 100
constant APP_NAME = "Nova3D Wallpapers"

function calculatePoints(base, bonus)
    whenever bonus > 0
        give back base + (bonus * 2)
    otherwise
        give back base
    end
end
```

### Flutter Declarative UI
```star
app WallpaperApp

use Material
use Flutter

function build()
    give back Scaffold(
        appBar = AppBar(
            title = Text("Nova3D Wallpapers"),
            backgroundColor = Colors.indigo
        ),
        body = Center(
            child = Column(
                mainAxisAlignment = MainAxisAlignment.center,
                children = [
                    Text("4K Parallax Wallpapers", style = TextStyle(fontSize = 24.0, fontWeight = FontWeight.bold)),
                    SizedBox(height = 16.0),
                    ElevatedButton(
                        child = Text("Explore Wallpapers"),
                        onPressed = () -> show("Exploring...")
                    )
                ]
            )
        )
    )
end

end
```

### Android WallpaperManager Bridge
```star
use "android_service.star"

function setHomeScreen(url)
    # FLAG_SYSTEM = 1, FLAG_LOCK = 2, FLAG_BOTH = 3
    AndroidWallpaperService.setWallpaper(url, 1)
    AndroidHapticService.vibrate(25)
end
```
