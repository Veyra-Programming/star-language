# 🌟 STAR IR SPECIFICATION
**Version: 0.3.0-draft**  
**Status: Authoritative Standard for Intermediate Representation**

---

## 1. Introduction

The **Star Intermediate Representation (Star IR)** is the formal, versioned compilation contract between the Star language front-end (Lexer, Parser, AST, Semantic Analyzer) and all Star execution backends:
- **StarVM**: High-performance stack-based bytecode virtual machine.
- **Star Wasm Backend** (Future): WebAssembly compilation target.
- **Star Native Backend** (Future): LLVM/AOT machine code compilation target.

---

## 2. Execution & Virtual Machine Model

Star IR operates as a **typed stack machine** with lexical frame environments:
- **Value Stack**: Operands and intermediate computation results are pushed and popped.
- **Call Stack & Frames**: Function and method invocations allocate a new `CallFrame` containing the instruction pointer (`ip`), local environment bindings, and enclosing parent frame references.
- **Constant Pool**: Immutable literals (Numbers, Text, Identifiers) referenced by integer indices.

---

## 3. Opcode Architecture

Star IR separates instructions into two conceptual tiers: **Core VM Instructions** and **Runtime ABI Instructions**.

### 3.1 Tier 1: Core VM Instructions

#### Stack & Constants
- `CONST <index>`: Push constant at pool index onto stack.
- `POP`: Discard top value on stack.
- `DUP`: Duplicate top value on stack.

#### Variables & Bindings
- `DEFINE_VAR <name_idx>`: Declare mutable variable in current environment and initialize with popped value.
- `DEFINE_CONST <name_idx>`: Declare immutable constant in current environment and initialize with popped value.
- `LOAD_VAR <name_idx>`: Lookup variable name and push value onto stack.
- `STORE_VAR <name_idx>`: Reassign variable name with popped value.

#### Arithmetic & Unary
- `ADD`: Pop $b$, pop $a$, push $a + b$ (numbers) or concatenation (text).
- `SUB`: Pop $b$, pop $a$, push $a - b$.
- `MUL`: Pop $b$, pop $a$, push $a * b$.
- `DIV`: Pop $b$, pop $a$, push $a / b$ (raises error if $b = 0$).
- `MOD`: Pop $b$, pop $a$, push $a \% b$ (raises error if $b = 0$).
- `NEG`: Pop $a$, push $-a$.
- `NOT`: Pop $a$, push logical negation.

#### Comparisons
- `EQUAL`: Pop $b$, pop $a$, push $a == b$.
- `NOT_EQUAL`: Pop $b$, pop $a$, push $a \ne b$.
- `LESS`: Pop $b$, pop $a$, push $a < b$.
- `LESS_EQUAL`: Pop $b$, pop $a$, push $a \le b$.
- `GREATER`: Pop $b$, pop $a$, push $a > b$.
- `GREATER_EQUAL`: Pop $b$, pop $a$, push $a \ge b$.

#### Control Flow & Jumps
- `JUMP <offset>`: Unconditionally set `ip = offset`.
- `JUMP_IF_FALSE <offset>`: Peek/pop top condition. If falsy, jump to `offset`.
- `JUMP_IF_TRUE <offset>`: Peek/pop top condition. If truthy, jump to `offset`.

#### Calls & Returns
- `CALL <arg_count>`: Call callable object on stack with $N$ arguments.
- `CALL_BUILTIN <name_idx> <arg_count>`: Call standard built-in function (`show`, `len`, `type`, `str`, `num`).
- `RETURN_VAL`: Pop value and return from current frame.
- `RETURN_NULL`: Return `null` from current frame.

---

### 3.2 Tier 2: Runtime ABI & Object Instructions

#### Functions & Closures
- `MAKE_FUNCTION <func_def_idx>`: Capture current lexical environment and construct first-class `StarFunction`.

#### Classes & Object Model
- `MAKE_CLASS <class_def_idx>`: Construct `StarClass` blueprint with properties and method table.
- `NEW_INSTANCE <class_name_idx> <named_count> <pos_count>`: Instantiate class with evaluated arguments.
- `GET_PROP <name_idx>`: Pop object, lookup property or bound method, push value.
- `SET_PROP <name_idx>`: Pop object, pop value, set property.
- `CALL_METHOD <name_idx> <arg_count>`: Lookup and invoke method with `self` binding.

#### Collections
- `MAKE_LIST <element_count>`: Pop $N$ elements and construct `StarList`.
- `MAKE_MAP <entry_count>`: Pop $2N$ keys and values and construct `StarMap`.
- `INDEX_GET`: Pop index, pop target (List/Map/Text), push element.
- `INDEX_SET`: Pop value, pop index, pop target, update element.

#### Modules
- `USE_MODULE <name_idx> <is_file>`: Resolve and load module namespace.

---

## 4. Binary Bytecode Format (`.starb`)

Compiled Star Bytecode uses a structured binary container format:

```text
+-------------------------------------------------------------+
| Header: Magic "STAR" (4 bytes) | Format Ver (2B) | Star (2B)|
+-------------------------------------------------------------+
| Constant Pool (Count: 4B, Array of Tagged Constants)        |
+-------------------------------------------------------------+
| Class Descriptors Table (Count: 4B, Properties, Methods)    |
+-------------------------------------------------------------+
| Function Descriptors Table (Count: 4B, Param List, Blocks)  |
+-------------------------------------------------------------+
| Main Code Chunk (Instruction Count: 4B, Opcode Stream)      |
+-------------------------------------------------------------+
| Debug Line Number Mapping (Count: 4B, [IP -> Line, Col])    |
+-------------------------------------------------------------+
```

---

## 5. Human-Readable Disassembly Format

Running `star ir <file>` outputs standardized assembly:

```text
=== Star IR: main (Module: app.star) ===
Constants: [0: "Hello, World!", 1: "show"]
0000  CONST        0           ; "Hello, World!"
0001  CALL_BUILTIN 1, 1        ; show(1 args)
0002  RETURN_NULL
```
