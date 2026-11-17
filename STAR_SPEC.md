# STAR LANGUAGE SPECIFICATION
**Version: 1.0.0 (General Availability)**  
**Status: Locked & Authoritative Standard (Core ABI v1 · Mobile ABI v1)**  
**Document Class: Normative Specification**

---

## 1. Introduction

The **Star Programming Language** is a modern, high-level, human-readable programming language designed for clarity, safety, simplicity, and cross-platform application development across Web, Desktop, Android, and iOS.

This document constitutes the formal, authoritative specification of the Star language (version 1.0.0 General Availability). All implementations—whether reference interpreters, native optimizing compilers, or toolchains—must conform strictly to the rules defined herein.



---

## 2. Design Principles

1. **Clarity Over Cleverness**: Code readability is paramount. Syntax is clean, natural, and free of cryptic punctuation.
2. **Predictable Semantics**: Explicit scoping, no implicit type coercion for ambiguous operations, and deterministic evaluation.
3. **Actionable Diagnostics**: Errors must guide the programmer with exact locations and human-centric remediation advice.
4. **Specification Authority**: The language is defined by this specification, independent of any host implementation language.

---

## 3. Lexical Grammar

### 3.1 Character Set and Encoding
Star source code is a sequence of characters encoded in **UTF-8**.

### 3.2 Whitespace and Line Terminators
- Whitespace is defined as spaces (`U+0020`) and horizontal tabs (`U+0009`).
- Line terminators are carriage return (`\r`), line feed (`\n`), or `\r\n`.
- Newlines are significant in Star: they serve as statement delimiters unless inside parenthesized, bracketed, or braced sub-expressions. Multiple consecutive newlines are treated as a single statement separator.

### 3.3 Comments
A single-line comment begins with the hash symbol `#` and extends to the end of the line.
```text
# This is a comment in Star
variable x = 10 # Inline comment
```

### 3.4 Identifiers
An identifier begins with an ASCII letter (`a-z`, `A-Z`) or underscore (`_`), followed by any number of ASCII letters, digits (`0-9`), or underscores.
```text
Identifier := [a-zA-Z_][a-zA-Z0-9_]*
```

### 3.5 Reserved Keywords
The following keywords are reserved in Star 0.2 and cannot be used as identifiers:
```text
app          class        property     function
variable     constant     if           else
while        for          in           repeat
break        continue     return       show
input        try          catch        use
self         true         false        null
and          or           not
```

### 3.6 Literals

#### 3.6.1 Integer Literals
A sequence of one or more decimal digits:
```text
IntegerLiteral := [0-9]+
```
Example: `0`, `42`, `1000`

#### 3.6.2 Decimal Literals
A sequence of digits containing exactly one fractional point:
```text
DecimalLiteral := [0-9]+ '.' [0-9]+
```
Example: `0.0`, `3.14159`, `99.95`

#### 3.6.3 Text Literals
Enclosed in double quotes (`"..."`). Supports standard escape sequences:
- `\n` : Line feed
- `\r` : Carriage return
- `\t` : Tab
- `\"` : Double quote
- `\\` : Backslash
```text
TextLiteral := '"' ( [^"\\\n] | '\\' . )* '"'
```

#### 3.6.4 Boolean Literals
`true` and `false`.

#### 3.6.5 Null Literal
`null` denotes the deliberate absence of a value.

---

## 4. Operators and Precedence

Operators are evaluated in order of precedence from highest (binding tightest) to lowest. Associativity is left-to-right unless noted.

| Precedence | Category | Operators | Associativity | Description |
|:---|:---|:---|:---|:---|
| 1 (Highest) | Primary / Postfix | `(args)`, `[index]`, `.property` | Left-to-right | Calls, indexing, property access |
| 2 | Unary | `-`, `not` | Right-to-left | Numeric negation, logical NOT |
| 3 | Multiplicative | `*`, `/`, `%` | Left-to-right | Multiplication, division, modulo |
| 4 | Additive | `+`, `-` | Left-to-right | Addition, string concatenation, subtraction |
| 5 | Relational | `<`, `<=`, `>`, `>=` | Left-to-right | Less than, less or equal, greater, greater or equal |
| 6 | Equality | `==`, `!=` | Left-to-right | Equal to, not equal to |
| 7 | Logical AND | `and` | Left-to-right | Short-circuit logical AND |
| 8 | Logical OR | `or` | Left-to-right | Short-circuit logical OR |
| 9 (Lowest) | Assignment | `=` | Right-to-left | Variable / index / property assignment |

---

## 5. Syntactic Grammar (EBNF)

```ebnf
Program         ::= StatementList EOF

StatementList   ::= ( Statement? ( '\n' | ';' )+ )* Statement?

Statement       ::= AppDecl
                  | ClassDecl
                  | UseStmt
                  | FunctionDecl
                  | VarDecl
                  | ConstDecl
                  | Assignment
                  | ShowStmt
                  | ReturnStmt
                  | BreakStmt
                  | ContinueStmt
                  | IfStmt
                  | WhileStmt
                  | RepeatStmt
                  | ForStmt
                  | TryCatchStmt
                  | ExpressionStmt

AppDecl         ::= 'app' IDENTIFIER '\n' Block 'end'

ClassDecl       ::= 'class' IDENTIFIER '\n' ClassBody 'end'
ClassBody       ::= ( ( PropertyDecl | FunctionDecl ) ( '\n' | ';' )+ )*
PropertyDecl    ::= 'property' IDENTIFIER ( ':' TypeRef )? ( '=' Expression )?

UseStmt         ::= 'use' ( IDENTIFIER | TEXT )

FunctionDecl    ::= 'function' IDENTIFIER '(' ParamList? ')' '\n' Block 'end'
ParamList       ::= IDENTIFIER ( ',' IDENTIFIER )*

VarDecl         ::= 'variable' IDENTIFIER ( ':' TypeRef )? ( '=' Expression )?
ConstDecl       ::= 'constant' IDENTIFIER ( ':' TypeRef )? '=' Expression
Assignment      ::= AccessExpr '=' Expression

ShowStmt        ::= 'show' Expression
ReturnStmt      ::= 'return' Expression?
BreakStmt       ::= 'break'
ContinueStmt    ::= 'continue'

IfStmt          ::= 'if' Expression '\n' Block
                    ( 'else' 'if' Expression '\n' Block )*
                    ( 'else' '\n' Block )?
                    'end'

WhileStmt       ::= 'while' Expression '\n' Block 'end'
RepeatStmt      ::= 'repeat' Expression '\n' Block 'end'
ForStmt         ::= 'for' IDENTIFIER 'in' Expression '\n' Block 'end'
TryCatchStmt    ::= 'try' '\n' Block 'catch' IDENTIFIER '\n' Block 'end'

ExpressionStmt  ::= Expression

Block           ::= StatementList

Expression      ::= LogicalOrExpr

LogicalOrExpr   ::= LogicalAndExpr ( 'or' LogicalAndExpr )*
LogicalAndExpr  ::= EqualityExpr ( 'and' EqualityExpr )*
EqualityExpr    ::= RelationalExpr ( ( '==' | '!=' ) RelationalExpr )*
RelationalExpr  ::= AdditiveExpr ( ( '<' | '<=' | '>' | '>=' ) AdditiveExpr )*
AdditiveExpr    ::= MultiplicativeExpr ( ( '+' | '-' ) MultiplicativeExpr )*
MultiplicativeExpr ::= UnaryExpr ( ( '*' | '/' | '%' ) UnaryExpr )*
UnaryExpr       ::= ( '-' | 'not' ) UnaryExpr | PostfixExpr

PostfixExpr     ::= PrimaryExpr ( CallSuffix | IndexSuffix | MemberSuffix )*
CallSuffix      ::= '(' CallArgList? ')'
CallArgList     ::= ( PositionalOrNamedArg ( ',' PositionalOrNamedArg )* )?
PositionalOrNamedArg ::= ( IDENTIFIER '=' )? Expression
IndexSuffix     ::= '[' Expression ']'
MemberSuffix    ::= '.' IDENTIFIER

PrimaryExpr     ::= Literal
                  | IDENTIFIER
                  | 'self'
                  | '(' Expression ')'
                  | ListLiteral
                  | MapLiteral

Literal         ::= INTEGER | DECIMAL | TEXT | 'true' | 'false' | 'null'
ListLiteral     ::= '[' ( Expression ( ',' Expression )* )? ']'
MapLiteral      ::= '{' ( MapEntry ( ',' MapEntry )* )? '}'
MapEntry        ::= Expression ':' Expression

TypeRef         ::= 'Text' | 'Number' | 'Integer' | 'Decimal' | 'Boolean' | 'List' | 'Map' | 'Function' | 'Any'
```

---

## 6. Static Semantics & Scoping

### 6.1 Scopes
Star uses **lexical scoping**. A scope is created by:
- The global/module level
- `app` block
- `function` body
- `if`, `else if`, `else` blocks
- `while`, `repeat`, `for` loop blocks
- `try`, `catch` blocks

### 6.2 Variable Declarations and Mutability
- `variable name = value`: Declares a mutable variable within the current scope.
- `constant name = value`: Declares an immutable binding. Reassigning a constant is an error (`Star Name Error`).
- Shadowing: An inner scope may declare a variable with the same name as an outer scope. The inner declaration shadows the outer binding within that inner scope.

### 6.3 Resolution Rules
When resolving an identifier:
1. Search current scope.
2. Search enclosing outer scopes outward to global scope.
3. Search built-in identifiers.
4. If not found, raise a `Star Name Error`.

---

## 7. Runtime Type System

Star 0.2 provides dynamic typing with optional type annotations.

### 7.1 Core Types
1. **`Null`**: Single value `null`.
2. **`Boolean`**: `true` or `false`.
3. **`Integer`**: 64-bit signed integer.
4. **`Decimal`**: 64-bit IEEE 754 floating-point number.
5. **`Text`**: Immutable UTF-8 sequence of characters.
6. **`List`**: Ordered, dynamically-sized array of Star values.
7. **`Map`**: Key-value dictionary where keys are hashable values (Text, Integer, Boolean).
8. **`Function`**: First-class callable block supporting lexical closures.
9. **`Class`**: Object blueprint defining properties and member methods.
10. **`Instance`**: Concrete instance of a `Class` with encapsulated property state and explicit `self` reference.
11. **`Module`**: Encapsulated namespace of functions, constants, and classes.

### 7.2 Type Operations & Coercion Rules
- Addition `+`:
  - `Integer + Integer` -> `Integer`
  - `Decimal + Decimal` / `Integer + Decimal` / `Decimal + Integer` -> `Decimal`
  - `Text + Text` -> `Text` (concatenation)
  - `Text + Value` or `Value + Text` -> `Text` (automatic text representation conversion)
- Subtraction `-`, Multiplication `*`, Division `/`, Modulo `%`:
  - Defined strictly for numeric operands (`Integer`, `Decimal`).
  - Division by zero raises `Star Runtime Error`.
- Comparison (`<`, `<=`, `>`, `>=`):
  - Defined for numbers between numbers, and strings between strings (lexicographical).
  - Comparing incompatible types raises `Star Type Error`.
- Equality (`==`, `!=`):
  - Values of different types are not equal (`null == 0` evaluates to `false`).
  - Lists and maps compare by structural value equality in Star 0.2.

### 7.3 Truthiness
In conditional expressions (`if`, `while`):
- `false` and `null` evaluate to **falsy**.
- `0`, `""`, `[]`, `{}` and all other values evaluate to **truthy**.

---

## 8. Object Model & Modules

### 8.1 Classes, Properties & Methods
- A `class` encapsulates properties and methods.
- Properties are declared with `property <name> (= <default>)?`.
- Methods are defined inside the class with `function <name>(<params>) ... end`.
- Methods access instance properties explicitly through `self.<property>`. Calling instance methods is done via `self.<method>()`.
- Accessing or setting an undeclared property on an instance raises a `Star Name Error`.
- Instantiation is invoked with `ClassName(prop1 = val1, prop2 = val2)` or positional arguments matching property declaration order.

### 8.2 Module System & Standard Library
- `use <ModuleName>` imports built-in or local modules.
- Standard Library Modules:
  - `Math`: `PI`, `E`, `abs(x)`, `sqrt(x)`, `min(a, b)`, `max(a, b)`, `round(x)`, `floor(x)`, `ceil(x)`, `pow(b, e)`
  - `Time`: `now()`, `sleep(seconds)`
  - `String`: `trim(text)`, `uppercase(text)`, `lowercase(text)`, `split(text, delim)`, `contains(text, sub)`
  - `IO`: `readFile(path)`, `writeFile(path, content)`, `fileExists(path)`
  - `System`: `platform()`, `args()`
- Relative file imports: `use "relative/path.star"` imports symbols from another Star source file.

---

## 9. Diagnostic Error & Warning Classification

### 9.1 Fatal Diagnostic Errors
1. **`Star Syntax Error`**: Invalid token, unclosed block, illegal grammar production.
2. **`Star Runtime Error`**: Division by zero, out-of-bounds index, invalid runtime operation.
3. **`Star Type Error`**: Incompatible operand types (e.g., subtracting text).
4. **`Star Name Error`**: Undeclared identifier, unknown class property, or modifying an immutable constant.
5. **`Star Value Error`**: Invalid argument value passed to an operation.
6. **`Star Internal Error`**: Unhandled compiler or runtime defect.

### 9.2 Linter Warnings
1. **`Star Warning`**: Non-fatal diagnostic findings detected during semantic analysis:
   - Unreachable code after `return`, `break`, or `continue`.
   - Variable declared but never read.
   - Shadowing an outer variable unintentionally.

---

## 10. Formatter Specification (`star format`)

The official Star formatter enforces:
- Standard 4-space indentation for nested blocks.
- One space surrounding binary operators (`+`, `-`, `*`, `/`, `==`, `=`, etc.).
- Comma separated lists format with a trailing space (`[1, 2, 3]`).
- Clean separation between top-level declarations and classes.
- `--check` flag returns exit code `0` if formatted correctly, `1` if changes needed (ideal for CI).

### Diagnostic Visual Layout Standard
```text
Star Type Error: Cannot perform arithmetic on Text and Boolean.

File: src/main.star
Line: 12, Column: 14

    variable result = "hello" - true
                                ^^^^

Suggestion: Arithmetic subtraction is only defined for Integer and Decimal values.
```

---

## 10. Conformance and Compliance

An implementation is **Star 0.1 Conforming** if and only if it:
1. Accepts all valid Star 0.1 programs defined by the Syntactic Grammar without syntax error.
2. Rejects all invalid programs with informative diagnostic messages.
3. Passes the canonical Star Conformance Test Suite (`conformance/`).
