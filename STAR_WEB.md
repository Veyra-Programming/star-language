# 🌟 STAR WEB SPECIFICATION & WASM ABI
**Specification Version: 0.5.0**  
**Status: Authoritative Standard for Web Platform Target**

---

## 1. Overview

The **Star Web Platform Target** enables compiling Star source programs into WebAssembly (`.wasm`) and deployable browser bundles (`build/web/`) without requiring the application developer to write JavaScript or HTML.

---

## 2. Compilation Pipeline

```text
                  Star Source (.star)
                           │
                           ▼
                      Star Parser
                           │
                          AST
                           │
                   Semantic Analyzer
                           │
                      ⭐ Star IR
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      Direct WASM Opcodes      Web Runtime ABI Calls
     (i64.const, i64.add)     (star_ui_button, star_show)
              │                         │
              └────────────┬────────────┘
                           ▼
                    app.wasm binary
                           │
           + star_runtime.js + index.html
                           │
                           ▼
                    Browser Engine
```

---

## 3. Web Runtime ABI (Imports & Exports)

The compiled WebAssembly module imports standard runtime host functions from `star_env`:

### 3.1 Console & System Imports
- `star_show(text_ptr, text_len)`: Outputs text to browser console and debug log.
- `star_time_now()`: Returns current timestamp from high-resolution browser clock (`performance.now()`).

### 3.2 UI & Component Imports
- `star_ui_create_element(tag_id, text_ptr, text_len, callback_idx)`: Creates declarative UI component node.
- `star_ui_append_child(parent_id, child_id)`: Constructs hierarchical layout tree.
- `star_ui_render_root(root_id)`: Commits declarative UI tree to DOM.
- `star_ui_reconcile()`: Triggers reactive reconciliation when state modifications occur.

### 3.3 Module Exports
- `main()`: Entry point invoked by `star_runtime.js` upon module instantiation.
- `star_dispatch_event(callback_idx)`: Event handler callback called when browser events fire.

---

## 4. Web Build Artifact Structure

Executing `star build web` outputs the following standalone bundle:

```text
build/web/
├── index.html         # Application shell with responsive viewport
├── app.wasm           # Compiled WebAssembly binary
├── star_runtime.js    # Star Web Runtime & Reactive DOM Engine
├── styles.css         # Modern glassmorphic theme and styling
└── assets/            # Embedded project assets
```

---

## 5. Star.js — Universal Web & App Framework for Digital Continuity

In addition to WASM compilation, the Star ecosystem includes **Star.js** (`star_js/` & `Star.js`), a zero-dependency, standalone JavaScript framework uniting Star UI declarative components with the **Open Digital Continuity Standard (ODCS-2.0.0)**.

### 5.1 Architecture & ODCS Layer Integration
- **Layer 1: Local Durability**: IndexedDB Write-Ahead Log (`ODCS_Star_Vault`) with RFC 8785 canonical SHA-256 Merkle chaining.
- **Layer 2: CRDT Consensus**: State-based `PNCounter` and Add-Wins `ORSet` models for partition-tolerant multi-node convergence.
- **Layer 2: Dual Transport**: `ODCS-REL` (TCP-mode ordered sequences + CRC32) & `ODCS-DGM` (UDP-mode 0-RTT stateless datagrams).
- **Layer 3: Runtime Sensing**: Active RTT ping probing, jitter ratio monitoring, and automated degradation mode shifting (`OPTIMAL_ONLINE`, `DEGRADED_JITTER`, `SEVERED_OFFLINE`).
- **Layer 4: Zero Intent Loss (ZIL)**: `Star.Intent.preserve(action, payload)` mints tamper-evident cryptographic receipts in <16ms with durable outbox auto-drain.

### 5.2 Usage
```html
<script src="Star.js"></script>
<script>
  const { UI, createApp, reactive } = Star;
  const state = reactive({ clicks: 0 });

  function App() {
    return UI.card([
      UI.title("⭐ Star.js Continuity App", 2),
      UI.button(`Clicked: ${state.clicks}`, () => state.clicks++)
    ]);
  }

  createApp(App).mount("#root");
</script>
```
Visit `star_js/index.html` for the complete interactive Star.js Playground, Live Studio, and 4-Layer ODCS Inspector.

