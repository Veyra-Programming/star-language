# Star Programming Language Agent Guidelines

When working with Star code (`.star`, `.starb`, `.starmobile`):

1. **Toolchain & Execution**:
   - Always invoke the Star CLI via `star.bat` on Windows or `star` on Unix.
   - Run tests using `star test` or `star run <test_file.star>`.
   - Validate syntax and semantic correctness using `star check <file.star>`.
   - Preview declarative UI layouts using `star preview <file.star>`.
   - Compile source code into bytecode using `star compile <file.star>` $\rightarrow$ `.starb`.

2. **Language Syntax Rules**:
   - Functions and blocks end with `end`.
   - Natural conditionals: use `whenever <condition>` and `otherwise` instead of curly braces.
   - Return values with `give back <expression>` or `return <expression>`.
   - Variable declarations: `variable name = value` or `let name = value`.
   - Constant declarations: `constant NAME = value`.
   - Collection indexing: `list[0]`, `map["key"]`.

3. **Flutter & Mobile UI Rules**:
   - Universal declarative UI uses `Scaffold(...)`, `AppBar(...)`, `Column(...)`, `Row(...)`, `Container(...)`, `When(cond, a, b)`.
   - Use named parameters: `Scaffold(appBar = AppBar(title = Text("Title")))`.
   - Native Android bridges: use `WallpaperManager.setWallpaper(...)` and `GoogleBillingClient`.
