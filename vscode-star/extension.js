/**
 * ⭐ Star Programming Language Visual Studio Code Extension
 * Provides Syntax Highlighting, Real-Time Diagnostics, Flutter UI Preview,
 * Code Formatting, Rich Hover Documentation for Keywords & Variables,
 * and Android / Native Build Integration.
 */

const vscode = require('vscode');
const cp = require('child_process');
const path = require('path');
const fs = require('fs');

let diagnosticCollection;
let starStatusBarItem;

/**
 * Finds the star executable or batch script.
 */
function getStarLauncher() {
    const config = vscode.workspace.getConfiguration('star');
    const customPath = config.get('executablePath');
    if (customPath && fs.existsSync(customPath)) {
        return customPath;
    }

    // Default candidate paths - prioritized paths without spaces
    const candidates = [
        'E:\\Star\\star.bat',
        'C:\\Star\\star.bat',
        'E:\\STARLA~1\\star.bat',
        'G:\\Star\\star.bat',
        'E:\\Star Language\\star.bat',
        'star.bat'
    ];

    for (const c of candidates) {
        if (fs.existsSync(c)) {
            return c;
        }
    }

    return 'star.bat';
}

/**
 * Executes a Star command in a dedicated terminal.
 */
function runInTerminal(terminalName, commandArgs) {
    const launcher = getStarLauncher();
    let term = vscode.window.terminals.find(t => t.name === terminalName);
    if (!term) {
        term = vscode.window.createTerminal(terminalName);
    }
    term.show(true);

    let fullCmd;
    if (process.platform === 'win32') {
        if (launcher.includes(' ')) {
            const shell = (vscode.env.shell || '').toLowerCase();
            if (shell.includes('cmd')) {
                fullCmd = `"${launcher}" ${commandArgs}`;
            } else {
                fullCmd = `& "${launcher}" ${commandArgs}`;
            }
        } else {
            fullCmd = `${launcher} ${commandArgs}`;
        }
    } else {
        fullCmd = `"${launcher}" ${commandArgs}`;
    }
    term.sendText(fullCmd);
}

/**
 * Runs star check on a document and populates VS Code Diagnostics.
 */
function lintDocument(document) {
    if (!document || (document.languageId !== 'star' && !document.fileName.endsWith('.star'))) {
        return;
    }

    const filePath = document.fileName;
    if (!fs.existsSync(filePath)) {
        return;
    }

    const launcher = getStarLauncher();
    cp.execFile(launcher, ['check', filePath], { encoding: 'utf8' }, (err, stdout, stderr) => {
        const diagnostics = [];
        const output = (stdout || '') + '\n' + (stderr || '');
        const lines = output.split('\n');

        let currentMsg = null;
        let currentSeverity = vscode.DiagnosticSeverity.Error;
        let currentFile = null;
        let currentLine = 0;
        let currentCol = 0;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            if (line.startsWith('Star Warning:')) {
                currentMsg = line.replace('Star Warning:', '').trim();
                currentSeverity = vscode.DiagnosticSeverity.Warning;
            } else if (line.startsWith('Star Error:') || line.startsWith('Star Syntax Error:') || line.startsWith('Star Type Error:')) {
                currentMsg = line.trim();
                currentSeverity = vscode.DiagnosticSeverity.Error;
            } else if (line.startsWith('File:')) {
                currentFile = line.replace('File:', '').trim();
            } else if (line.startsWith('Line:')) {
                const match = line.match(/Line:\s*(\d+),\s*Column:\s*(\d+)/);
                if (match) {
                    currentLine = parseInt(match[1], 10);
                    currentCol = parseInt(match[2], 10);

                    if (currentMsg && currentLine > 0) {
                        const lineIdx = Math.max(0, currentLine - 1);
                        const colIdx = Math.max(0, currentCol - 1);
                        const range = new vscode.Range(lineIdx, colIdx, lineIdx, colIdx + 15);
                        const diag = new vscode.Diagnostic(range, currentMsg, currentSeverity);
                        diag.source = 'Star Doctor';
                        diagnostics.push(diag);
                        currentMsg = null;
                    }
                }
            }
        }

        diagnosticCollection.set(document.uri, diagnostics);
    });
}

/**
 * Comprehensive Star Language Hover Documentation Dictionary
 */
const HOVER_DOCS = {
    // Control Flow & Haven Natural Syntax
    'whenever': '### `whenever` *(Control Flow)*\n\nNatural conditional branch in Star (Haven syntax). Evaluates `<condition>` and executes the block if true. Paired with `otherwise` and closed by `end`.\n\n```star\nwhenever score >= 100\n    show "Winner!"\notherwise\n    show "Keep playing"\nend\n```',
    'otherwise': '### `otherwise` *(Control Flow)*\n\nFallback alternative branch for `whenever` and `if` conditional blocks.\n\n```star\nwhenever isConnected\n    show "Online"\notherwise\n    show "Reconnecting..."\nend\n```',
    'unless': '### `unless` *(Inverted Conditional)*\n\nExecutes the following block when `<condition>` evaluates to `false` (equivalent to `if not condition`).\n\n```star\nunless hasPermission\n    show "Access Denied"\nend\n```',
    'if': '### `if` *(Conditional Statement)*\n\nEvaluates condition and executes body if true. Terminated by `end`.\n\n```star\nif count == 0\n    show "Empty"\nend\n```',
    'else': '### `else` *(Conditional Branch)*\n\nAlternative fallback branch for `if` statement blocks.\n\n```star\nif x > 0\n    show "Positive"\nelse\n    show "Non-positive"\nend\n```',
    'while': '### `while` *(Loop Statement)*\n\nRepeats the block of code as long as the condition evaluates to `true`.\n\n```star\nwhile count < 10\n    show count\n    set count to count + 1\nend\n```',
    'for': '### `for` *(Loop Statement)*\n\nIterates over a range (`1..10`) or collection elements (`for each item in list`).\n\n```star\nfor i in 1..5\n    show i\nend\n```',
    'repeat': '### `repeat` *(Counted Loop)*\n\nExecutes a code block an exact number of times. Inside the loop, `iteration` provides the 1-based index.\n\n```star\nrepeat 5 times:\n    show "Round {iteration}"\nend\n```',
    'times': '### `times` *(Loop Quantifier)*\n\nUsed with `repeat` statement to specify loop iterations: `repeat 5 times:`.',
    'iteration': '### `iteration` *(Loop Context Variable)*\n\nImplicit 1-based index variable available inside `repeat N times:` blocks (1, 2, 3, ... N).',
    'each': '### `each` *(Iteration Modifier)*\n\nUsed in `for each item in collection:` loops for natural collection traversal.',
    'in': '### `in` *(Membership / Iteration)*\n\nUsed in `for` loops (`for x in list`) and membership expressions (`item in list`).',
    'until': '### `until` *(Loop Statement)*\n\nExecutes code block repeatedly until condition evaluates to true.',
    'forever': '### `forever` *(Infinite Loop)*\n\nExecutes block indefinitely until an explicit `break` or `return` is reached.',
    'break': '### `break` *(Loop Control)*\n\nImmediately terminates the innermost enclosing `while`, `for`, or `repeat` loop.',
    'continue': '### `continue` *(Loop Control)*\n\nSkips the remainder of the current loop iteration and advances to the next.',
    'end': '### `end` *(Block Terminator)*\n\nCloses any code block in Star (functions, conditionals, loops, components, and classes). Replaces curly braces `{}`.',
    'return': '### `return` *(Control Flow)*\n\nExits a function or method and returns an optional value to the caller.\n\n```star\nfunction add(a, b)\n    return a + b\nend\n```',
    'give back': '### `give back` *(Haven Return)*\n\nNatural English return statement in Star. Returns an expression value to the caller.\n\n```star\nfunction double(n)\n    give back n * 2\nend\n```',

    // Variable Declarations & State
    'variable': '### `variable` *(Variable Declaration)*\n\nDeclares a mutable variable in the current lexical scope.\n\n```star\nvariable count = 0\nvariable name = "Star"\n```',
    'let': '### `let` *(Binding Declaration)*\n\nDeclares a local variable binding. Supports standard assignment (`let x = 10`) or Haven natural phrasing (`let x be 10`).\n\n```star\nlet total = price * quantity\nlet title be "WallpaperApp"\n```',
    'constant': '### `constant` *(Constant Declaration)*\n\nDeclares an immutable compile-time constant that cannot be reassigned.\n\n```star\nconstant PI = 3.14159\nconstant MAX_WALLPAPERS = 1000\n```',
    'remember': '### `remember` *(State Variable)*\n\nDeclares a reactive persistent state variable in Haven syntax. In UI components, state changes trigger automatic view updates.\n\n```star\nremember score as 0\nremember selectedIndex as 0\n```',
    'set': '### `set` *(Assignment Statement)*\n\nAssigns a new value to a variable using Haven natural syntax (`set <var> to <expr>`).\n\n```star\nset count to count + 1\nset wallpaper.isPurchased to true\n```',
    'to': '### `to` *(Assignment Target)*\n\nKeyword used with `set` statements: `set <variable> to <expression>`.',
    'be': '### `be` *(Binding Keyword)*\n\nKeyword used with `let` bindings: `let <name> be <value>`.',
    'as': '### `as` *(Alias / State Keyword)*\n\nUsed with `remember` (`remember x as 10`) or module imports (`use math as m`).',
    'increase': '### `increase` *(Natural Increment)*\n\nIncrements a numeric variable by a specified step amount.\n\n```star\nincrease count by 1\nincrease coins by 500\n```',
    'decrease': '### `decrease` *(Natural Decrement)*\n\nDecrements a numeric variable by a specified step amount.\n\n```star\ndecrease balance by price\ndecrease lives by 1\n```',
    'by': '### `by` *(Step Keyword)*\n\nUsed with `increase` and `decrease` statements to define the step size (`increase x by 5`).',

    // Builtins & Standard I/O
    'show': '### `show` *(Built-in Output)*\n\nPrints expressions, strings, or variables to the terminal or debug console.\n\n```star\nshow "Hello World"\nshow 42\nshow user.name\n```',
    'say': '### `say` *(Haven Speech / Print)*\n\nNatural language output statement with built-in string interpolation (`{var}`).\n\n```star\nsay "Welcome, {username}! You have {coins} coins."\n```',
    'input': '### `input(prompt)` *(Built-in Input)*\n\nPrompts the user and reads a line of text from standard input (stdin).\n\n```star\nlet name = input("Enter your name: ")\n```',
    'print': '### `print` *(Built-in Output)*\n\nPrints a value to stdout.',
    'assert': '### `assert(condition, message)` *(Diagnostics)*\n\nVerifies that a condition is true; halts with an error if false.',
    'panic': '### `panic(message)` *(Runtime Failure)*\n\nImmediately halts execution and raises a critical runtime error.',

    // Functions, Classes, Records & Architecture
    'function': '### `function` *(Function Declaration)*\n\nDeclares a named callable function with parameter list and return value.\n\n```star\nfunction fibRecursive(n)\n    if n <= 1\n        return n\n    end\n    return fibRecursive(n - 1) + fibRecursive(n - 2)\nend\n```',
    'task': '### `task` *(Async Coroutine)*\n\nDeclares an asynchronous background task or coroutine that runs non-blockingly.',
    'action': '### `action` *(Event Action)*\n\nDeclares an action handler for UI events or dispatch operations.',
    'define': '### `define` *(Definition Keyword)*\n\nAlternative declaration keyword for functions, tasks, or contracts.',
    'app': '### `app` *(Application Entry Point)*\n\nDeclares the top-level application root component.\n\n```star\napp WallpaperApp:\n    render Scaffold(...)\nend\n```',
    'component': '### `component` *(Universal UI Component)*\n\nDeclares a stateful reactive Flutter/Star component with lifecycle methods (`state`, `computed`, `render`).\n\n```star\ncomponent CounterApp:\n    remember count as 0\n    render Column(...)\nend\n```',
    'blueprint': '### `blueprint` *(Contract / Interface)*\n\nDefines a structural blueprint or interface that classes and components adhere to.',
    'record': '### `record` *(Data Record)*\n\nDeclares a structured data schema with typed fields.\n\n```star\nrecord Wallpaper(id: String, title: String, price: Int)\n```',
    'durable': '### `durable` *(Persistence Modifier)*\n\nModifiers for `record` or `state` that automatically encrypts and persists data to disk with cryptographic SHA-256 ODCS hashing.\n\n```star\ndurable record Wallet(coins: Int, vip: Boolean)\n```',
    'class': '### `class` *(Object-Oriented Class)*\n\nDeclares an object-oriented class with fields, constructor, and methods.',
    'use': '### `use` *(Module Import)*\n\nImports a standard library module or another `.star` file.\n\n```star\nuse Flutter\nuse Material\nuse "wallpaper_data.star"\n```',
    'import': '### `import` *(Module Import)*\n\nImports definitions from external packages or modules.',
    'export': '### `export` *(Module Export)*\n\nExports definitions to make them accessible to other importing files.',
    'self': '### `self` *(Instance Reference)*\n\nRefers to the current class or component instance.',

    // Flutter & Universal Declarative UI
    'Scaffold': '### `Scaffold` *(Flutter Declarative UI)*\n\nImplements the top-level Material 3 layout structure.\n\n**Parameters:**\n- `appBar`: Top header bar (`AppBar`)\n- `body`: Main screen content widget\n- `floatingActionButton`: Floating action button\n- `bottomNavigationBar`: Bottom tabs navigation bar\n- `backgroundColor`: Background color\n\n```star\nScaffold(\n    appBar = AppBar(title = Text("3D Wallpapers")),\n    body = Center(child = Text("Hello Star!")),\n    bottomNavigationBar = BottomNavigationBar(...)\n)\n```',
    'AppBar': '### `AppBar` *(Header Bar Widget)*\n\nMaterial 3 application bar displayed at the top of a `Scaffold`.\n\n```star\nAppBar(\n    title = Text("Explore Wallpapers"),\n    backgroundColor = Colors.deepPurple\n)\n```',
    'Text': '### `Text` *(Typography Widget)*\n\nDisplays a string of styled text.\n\n```star\nText("Cyber City 2099", style = TextStyle(fontSize = 20, fontWeight = FontWeight.bold))\n```',
    'Column': '### `Column` *(Vertical Layout)*\n\nLays out its list of children vertically.\n\n```star\nColumn(children = [WidgetA(), WidgetB()])\n```',
    'Row': '### `Row` *(Horizontal Layout)*\n\nLays out its list of children horizontally.\n\n```star\nRow(children = [Icon(Icons.star), Text("5.0")])\n```',
    'Container': '### `Container` *(Box Styling Widget)*\n\nA convenience widget that combines common painting, positioning, and sizing.\n\n```star\nContainer(\n    padding = EdgeInsets.all(16),\n    decoration = BoxDecoration(borderRadius = BorderRadius.circular(12)),\n    child = ...\n)\n```',
    'Card': '### `Card` *(Material 3 Surface)*\n\nA Material design card surface with rounded corners and subtle drop elevation.\n\n```star\nCard(child = Padding(padding = EdgeInsets.all(12), child = Text("VIP Pass")))\n```',
    'ElevatedButton': '### `ElevatedButton` *(Action Button)*\n\nA Material 3 filled button with shadow elevation.\n\n```star\nElevatedButton(child = Text("Set Wallpaper"), onPressed = setWallpaperAction)\n```',
    'GestureDetector': '### `GestureDetector` *(Touch Interaction)*\n\nDetects physical gestures (`onTap`, `onDoubleTap`, `onLongPress`, `onPanUpdate`).',
    'When': '### `When(condition, true_widget, false_widget)` *(Conditional UI)*\n\nDeclarative UI conditional rendering. Shows `true_widget` when condition is met, otherwise `false_widget`.\n\n```star\nWhen(isPurchased, Text("Unlocked"), ElevatedButton(child = Text("Buy")))\n```',
    'Icon': '### `Icon` *(Vector Iconography)*\n\nRenders a vector Material symbol from `Icons.*`.\n\n```star\nIcon(Icons.wallpaper, color = Colors.white)\n```',
    'Image': '### `Image` *(Image Display)*\n\nRenders a 2D or 3D image from a local asset, network URL, or camera stream.\n\n```star\nImage(source = "assets/cyber.jpg", fit = BoxFit.cover)\n```',
    'Center': '### `Center` *(Centering Widget)*\n\nAligns its child widget in the middle of both horizontal and vertical axes.',
    'Padding': '### `Padding` *(Spacing Insets)*\n\nInsets its child by the given `EdgeInsets` padding.',
    'Expanded': '### `Expanded` *(Flex Expansion)*\n\nExpands a child of a `Row` or `Column` to fill all available empty space.',
    'SizedBox': '### `SizedBox` *(Fixed Dimensions)*\n\nA box with a specified fixed width and height for spacing.\n\n```star\nSizedBox(height = 16)\n```',
    'BottomNavigationBar': '### `BottomNavigationBar` *(Tab Navigation)*\n\nA bottom navigation bar with switching tab items.',
    'AnimatedContainer': '### `AnimatedContainer` *(Implicit Animation)*\n\nAnimates changes in size, background color, or border over a specified duration.',

    // Platform APIs & Hardware Bridges
    'WallpaperManager': '### `WallpaperManager` *(Android Native Wallpaper)*\n\nDirect bridge to native Android `android.app.WallpaperManager`.\n\n- `setWallpaper(imageUri, flag)`: Sets current wallpaper\n- `FLAG_SYSTEM = 1`: Sets Home Screen\n- `FLAG_LOCK = 2`: Sets Lock Screen\n- `FLAG_BOTH = 3`: Sets Both Screens',
    'GoogleBilling': '### `GoogleBilling` *(Google Play In-App Billing)*\n\nGoogle Play BillingClient v7.0.0 integration for VIP memberships, coin purchases, and subscriptions.',
    'GoogleBillingClient': '### `GoogleBillingClient` *(Billing Manager)*\n\nManages connections to Google Play Store billing service, handles purchase tokens, queries product details, and confirms purchases.',
    'Gyroscope': '### `Gyroscope` *(3D Motion Sensor)*\n\nReads real-time 3-axis hardware gyroscope sensor data (`x`, `y`, `z`) to power 3D Parallax holographic wallpaper effects.',
    'Haptics': '### `Haptics` *(Tactile Vibration)*\n\nNative haptic feedback bridge (`Haptics.impact()`, `Haptics.selection()`, `Haptics.vibrate()`).',
    'Colors': '### `Colors` *(Color Palette)*\n\nPredefined Material 3 palette: `Colors.deepPurple`, `Colors.amber`, `Colors.black`, `Colors.white`, etc.',
    'Icons': '### `Icons` *(Material Icons)*\n\nOfficial Material icons library: `Icons.wallpaper`, `Icons.star`, `Icons.shoppingCart`, `Icons.check`, etc.',
    'EdgeInsets': '### `EdgeInsets` *(Padding & Margins)*\n\nDimensions for container spacing (`EdgeInsets.all(16)`, `EdgeInsets.symmetric(horizontal = 20)`).',
    'BorderRadius': '### `BorderRadius` *(Corner Radii)*\n\nDefines rounded corners for boxes and cards (`BorderRadius.circular(16)`).'
};

/**
 * Searches the active document to provide hover information for user-defined
 * functions, variables, parameters, and types.
 */
function resolveDocumentSymbol(document, word, position) {
    if (!word || word.length === 0) return null;

    const lineCount = document.lineCount;

    // 1. Search for function declarations: `function <word>(...)` or `task <word>(...)`
    const funcRegex = new RegExp(`^\\s*(function|task|action|define)\\s+(${word})\\s*(\\([^\\)]*\\))`);
    for (let i = 0; i < lineCount; i++) {
        const text = document.lineAt(i).text;
        const match = text.match(funcRegex);
        if (match) {
            const kind = match[1];
            const name = match[2];
            const params = match[3];

            // Check if preceded by comment docstring
            let docComment = '';
            let prevLine = i - 1;
            while (prevLine >= 0) {
                const prevText = document.lineAt(prevLine).text.trim();
                if (prevText.startsWith('#') || prevText.startsWith('//')) {
                    const clean = prevText.replace(/^[#\/]+\s*/, '');
                    docComment = clean + (docComment ? '\n' + docComment : '');
                    prevLine--;
                } else {
                    break;
                }
            }

            let mdText = `### \`${kind} ${name}${params}\` *(User Function)*\n\n`;
            if (docComment) {
                mdText += `${docComment}\n\n`;
            }
            mdText += `Declared on line ${i + 1} of \`${path.basename(document.fileName)}\``;
            return mdText;
        }
    }

    // 2. Search for variable declarations: `variable <word> = ...` or `let <word> = ...`
    const varRegex = new RegExp(`^\\s*(variable|let|constant|remember|set)\\s+(${word})\\b(.*)$`);
    for (let i = 0; i < lineCount; i++) {
        const text = document.lineAt(i).text;
        const match = text.match(varRegex);
        if (match) {
            const decl = match[1];
            const rest = match[3].trim();
            const fullDecl = `${decl} ${word} ${rest}`.trim();

            let mdText = `### \`${word}\` *(${decl.toUpperCase()} Variable)*\n\n`;
            mdText += `\`\`\`star\n${fullDecl}\n\`\`\`\n\n`;
            mdText += `Declared on line ${i + 1} of \`${path.basename(document.fileName)}\``;
            return mdText;
        }
    }

    // 3. Search for components / classes: `component <word>`, `app <word>`, `class <word>`
    const typeRegex = new RegExp(`^\\s*(component|app|class|blueprint|record)\\s+(${word})\\b`);
    for (let i = 0; i < lineCount; i++) {
        const text = document.lineAt(i).text;
        const match = text.match(typeRegex);
        if (match) {
            const kind = match[1];
            let mdText = `### \`${word}\` *(User ${kind.toUpperCase()})*\n\n`;
            mdText += `Declared on line ${i + 1} of \`${path.basename(document.fileName)}\``;
            return mdText;
        }
    }

    // 4. Check if word is a parameter of the enclosing function
    const currentLineIdx = position.line;
    for (let i = currentLineIdx; i >= 0; i--) {
        const text = document.lineAt(i).text;
        const encMatch = text.match(/^\s*(function|task|action)\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)/);
        if (encMatch) {
            const funcName = encMatch[2];
            const paramList = encMatch[3].split(',').map(p => p.trim());
            if (paramList.includes(word)) {
                return `### \`${word}\` *(Parameter)*\n\nParameter of function \`${funcName}\` (line ${i + 1})`;
            }
            break;
        }
    }

    return null;
}

function activate(context) {
    console.log('⭐ Star Language Tools extension is now active!');

    diagnosticCollection = vscode.languages.createDiagnosticCollection('star');
    context.subscriptions.push(diagnosticCollection);

    // 1. Diagnostics on document open / save
    if (vscode.window.activeTextEditor) {
        lintDocument(vscode.window.activeTextEditor.document);
    }
    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(doc => lintDocument(doc)),
        vscode.workspace.onDidSaveTextDocument(doc => lintDocument(doc)),
        vscode.workspace.onDidCloseTextDocument(doc => diagnosticCollection.delete(doc.uri))
    );

    // 2. Command: Run Active File
    context.subscriptions.push(
        vscode.commands.registerCommand('star.run', (fileUri) => {
            let targetPath = null;
            if (fileUri && fileUri.fsPath) {
                targetPath = fileUri.fsPath;
            } else if (vscode.window.activeTextEditor) {
                targetPath = vscode.window.activeTextEditor.document.fileName;
            }

            if (!targetPath) {
                vscode.window.showWarningMessage('No Star (.star) file selected or active to run.');
                return;
            }

            if (vscode.window.activeTextEditor && vscode.window.activeTextEditor.document.isDirty) {
                vscode.window.activeTextEditor.document.save().then(() => {
                    runInTerminal('Star: Run', `run "${targetPath}"`);
                });
            } else {
                runInTerminal('Star: Run', `run "${targetPath}"`);
            }
        })
    );

    // 3. Command: Preview UI in TUI
    context.subscriptions.push(
        vscode.commands.registerCommand('star.preview', (fileUri) => {
            let targetPath = null;
            if (fileUri && fileUri.fsPath) {
                targetPath = fileUri.fsPath;
            } else if (vscode.window.activeTextEditor) {
                targetPath = vscode.window.activeTextEditor.document.fileName;
            }

            if (!targetPath) {
                vscode.window.showWarningMessage('No Star (.star) file selected or active to preview.');
                return;
            }

            if (vscode.window.activeTextEditor && vscode.window.activeTextEditor.document.isDirty) {
                vscode.window.activeTextEditor.document.save().then(() => {
                    runInTerminal('Star: Preview', `preview "${targetPath}"`);
                });
            } else {
                runInTerminal('Star: Preview', `preview "${targetPath}"`);
            }
        })
    );

    // 4. Command: Compile to Bytecode (.starb)
    context.subscriptions.push(
        vscode.commands.registerCommand('star.compile', (fileUri) => {
            let targetPath = null;
            if (fileUri && fileUri.fsPath) {
                targetPath = fileUri.fsPath;
            } else if (vscode.window.activeTextEditor) {
                targetPath = vscode.window.activeTextEditor.document.fileName;
            }
            if (!targetPath) return;

            const doCompile = () => {
                const launcher = getStarLauncher();
                cp.execFile(launcher, ['compile', targetPath], { encoding: 'utf8' }, (err, stdout, stderr) => {
                    if (err) {
                        vscode.window.showErrorMessage(`Compilation failed: ${stderr || err.message}`);
                    } else {
                        vscode.window.showInformationMessage(stdout.trim() || `✓ Compiled ${path.basename(targetPath)} successfully.`);
                    }
                });
            };

            if (vscode.window.activeTextEditor && vscode.window.activeTextEditor.document.isDirty) {
                vscode.window.activeTextEditor.document.save().then(doCompile);
            } else {
                doCompile();
            }
        })
    );

    // 5. Command: Check Syntax & Diagnostics
    context.subscriptions.push(
        vscode.commands.registerCommand('star.check', (fileUri) => {
            let doc = vscode.window.activeTextEditor ? vscode.window.activeTextEditor.document : null;
            if (doc) {
                lintDocument(doc);
                vscode.window.showInformationMessage(`Star Doctor checked: ${path.basename(doc.fileName)}`);
            }
        })
    );

    // 6. Command: Interactive REPL
    context.subscriptions.push(
        vscode.commands.registerCommand('star.repl', () => {
            runInTerminal('Star: REPL', 'repl');
        })
    );

    // 7. Command: Build Android APK
    context.subscriptions.push(
        vscode.commands.registerCommand('star.buildApk', () => {
            runInTerminal('Star: Build', 'build apk');
        })
    );

    // 8. Command: Build Android AAB
    context.subscriptions.push(
        vscode.commands.registerCommand('star.buildAab', () => {
            runInTerminal('Star: Build', 'build aab');
        })
    );

    // 9. Command: Deploy to Android Device
    context.subscriptions.push(
        vscode.commands.registerCommand('star.deployAndroid', () => {
            runInTerminal('Star: Deploy', 'deploy android');
        })
    );

    // 10. Command: Run Doctor Diagnostics
    context.subscriptions.push(
        vscode.commands.registerCommand('star.doctor', () => {
            runInTerminal('Star: Doctor', 'doctor');
        })
    );

    // 11. Command: Format Document
    context.subscriptions.push(
        vscode.commands.registerCommand('star.format', () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;
            const filePath = editor.document.fileName;
            const launcher = getStarLauncher();
            cp.execFile(launcher, ['format', filePath], { encoding: 'utf8' }, (err, stdout) => {
                if (!err) {
                    vscode.window.showInformationMessage(`✓ Formatted ${path.basename(filePath)}`);
                }
            });
        })
    );

    // 12. Register Document Formatting Provider
    context.subscriptions.push(
        vscode.languages.registerDocumentFormattingEditProvider('star', {
            provideDocumentFormattingEdits(document) {
                vscode.commands.executeCommand('star.format');
                return [];
            }
        })
    );

    // 13. Comprehensive Hover Provider (Keywords, Flutter Widgets, Platform APIs, User Variables & Functions)
    const documentSelectors = [
        { language: 'star' },
        { pattern: '**/*.star' },
        { pattern: '**/*.starb' },
        { pattern: '**/*.starmobile' }
    ];

    context.subscriptions.push(
        vscode.languages.registerHoverProvider(documentSelectors, {
            provideHover(document, position) {
                const lineText = document.lineAt(position.line).text;

                // A. Check multi-word natural phrases
                const phrases = [
                    'give back',
                    'is equal to',
                    'is not equal to',
                    'is greater than or equal to',
                    'is less than or equal to',
                    'is greater than',
                    'is less than',
                    'for each',
                    'durable record',
                    'repeat '
                ];

                for (const p of phrases) {
                    const idx = lineText.indexOf(p);
                    if (idx !== -1 && position.character >= idx && position.character <= idx + p.length) {
                        const cleanKey = p.trim();
                        if (HOVER_DOCS[cleanKey]) {
                            const md = new vscode.MarkdownString(HOVER_DOCS[cleanKey]);
                            md.isTrusted = true;
                            return new vscode.Hover(md);
                        }
                    }
                }

                // B. Single word token under cursor
                const range = document.getWordRangeAtPosition(position);
                if (!range) return null;
                const word = document.getText(range);

                // 1. Check predefined Star documentation dictionary
                if (HOVER_DOCS[word]) {
                    const md = new vscode.MarkdownString(HOVER_DOCS[word]);
                    md.isTrusted = true;
                    return new vscode.Hover(md, range);
                }

                // 2. Check user-defined functions, variables, parameters, and types in document
                const userDoc = resolveDocumentSymbol(document, word, position);
                if (userDoc) {
                    const md = new vscode.MarkdownString(userDoc);
                    md.isTrusted = true;
                    return new vscode.Hover(md, range);
                }

                return null;
            }
        })
    );

    // 14. Status Bar Item
    starStatusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    starStatusBarItem.command = 'star.showMenu';
    starStatusBarItem.text = '$(sparkle) Star v1.3.2';
    starStatusBarItem.tooltip = 'Star Programming Language Tools (Click for actions)';
    starStatusBarItem.show();
    context.subscriptions.push(starStatusBarItem);

    // 15. QuickPick Menu
    context.subscriptions.push(
        vscode.commands.registerCommand('star.showMenu', async () => {
            const items = [
                { label: '$(play) Run Active File', description: 'star run <file>', command: 'star.run' },
                { label: '$(device-mobile) Preview Star UI', description: 'star preview <file>', command: 'star.preview' },
                { label: '$(zap) Compile to Bytecode (.starb)', description: 'star compile <file>', command: 'star.compile' },
                { label: '$(check) Check Syntax & Diagnostics', description: 'star check <file>', command: 'star.check' },
                { label: '$(terminal) Launch Star Interactive REPL', description: 'star repl', command: 'star.repl' },
                { label: '$(package) Build Android APK', description: 'star build apk', command: 'star.buildApk' },
                { label: '$(package) Build Android AAB Bundle', description: 'star build aab', command: 'star.buildAab' },
                { label: '$(radio-tower) Deploy to Connected Device', description: 'star deploy android', command: 'star.deployAndroid' },
                { label: '$(pulse) Star Doctor Diagnostics', description: 'star doctor', command: 'star.doctor' }
            ];

            const selected = await vscode.window.showQuickPick(items, {
                placeHolder: 'Select a Star Language command to execute'
            });

            if (selected) {
                vscode.commands.executeCommand(selected.command);
            }
        })
    );
}

function deactivate() {
    if (diagnosticCollection) {
        diagnosticCollection.clear();
    }
}

module.exports = {
    activate,
    deactivate
};
