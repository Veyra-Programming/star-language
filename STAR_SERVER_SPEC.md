# ⚡ Star HyperFlow Engine & Server-Side Scripting Specification
**Authoritative Reference**: `STAR_SERVER_SPEC.md`  
**Version**: 1.3.0 Production GA  
**Status**: Certified & Active  

---

## 1. Executive Overview

The **Star HyperFlow Engine** (`use Server`, `use HTTP`) is a high-performance, asynchronous, event-driven server runtime and concurrency mesh built natively into the Star Programming Language.

HyperFlow introduces foundational architectural concepts that **no existing mainstream server language (Node.js, Go, Python/FastAPI, Rust/Actix, Java/Spring) contains natively**:

1. **ChronoState & Time-Reversible Execution**: Native, $O(1)$ in-memory micro-snapshots and vector-clocked checkpoints. If a multi-step operation or route handler encounters an unhandled fault, the server memory automatically time-rewinds without side-effects or dirty data leakage.
2. **Quantum-Reactive Live Pipeline**: Zero-serialization live synchronization between server state and connected clients. State mutations automatically emit RFC 6902-compliant delta frames over HTTP SSE or WebSockets with zero boilerplate.
3. **Sovereign Actor Mesh**: Concurrent actor processes with ring-buffer mailboxes, supervision trees, and request-reply futures (`ask` / `send`).
4. **Radix Trie Route Dispatch**: Sub-microsecond parameter extraction, wildcard capture, and chainable middleware pipelines.
5. **Production Security Shield**: Automatic Zip-Slip and path-traversal protection, token-bucket rate limiting, signed JWT tokens, and salted PBKDF2 password hashing.

---

## 2. Revolutionary Concepts Unique to Star

### 2.1 ChronoState (Time-Reversible In-Memory Memory Mesh)

In existing languages, partial request failures corrupt in-memory caches, objects, or state machines unless developers manually write complex saga orchestrators or compensation code.

In Star HyperFlow, any state store can be declared as a `ChronoStore`:

```star
use Server

constant server = Server.app("CommerceService")
constant store = server.chrono_store("inventory", {
    "stock": 50,
    "reserved": 0
})

server.post("/api/checkout", function(req, res)
    constant body = req.json()
    constant qty = body["quantity"]

    # 1. Establish an O(1) Transaction Checkpoint
    constant cp = store.checkpoint("pre_checkout")

    # 2. Speculatively apply state changes
    store.set("stock", store.get("stock") - qty)
    store.set("reserved", store.get("reserved") + qty)

    # 3. If validation fails, time-rewind state instantaneously!
    whenever store.get("stock") < 0:
        store.rewind(cp)
        res.status(400).json({
            "error": "Insufficient inventory. State rolled back!",
            "stock": store.get("stock"),
            "rolled_back": true
        })
    otherwise:
        store.commit()
        res.json({"status": "confirmed", "stock": store.get("stock")})
    end
end)
```

#### ChronoStore Methods
| Method | Description |
| :--- | :--- |
| `store.get(key, default=null)` | Retrieves current value of `key`. |
| `store.set(key, value)` | Mutates `key` and increments monotonic transaction tick. |
| `store.checkpoint(label)` | Creates an immutable structural snapshot with SHA-256 seal. |
| `store.rewind(label)` | Reverts in-memory state to the specified snapshot. |
| `store.commit(label)` | Seals state and records permanent transition. |
| `store.diff(labelA, labelB)` | Computes differential patch between two points in time. |
| `store.history()` | Retrieves full tamper-evident audit ledger. |
| `store.tick` | Monotonic state transition counter. |

---

### 2.2 Quantum-Reactive Live Pipeline (Zero-Boilerplate State Sync)

Traditional architectures require manual WebSocket wrappers, polling routines, or custom serialization code to stream updates.

Star's `ReactiveStore` automatically monitors mutations and streams delta frames:

```star
use Server

constant server = Server.app("DashboardApp")
constant live = server.reactive_store("metrics", {
    "active_connections": 0,
    "cpu_usage": 14.2
})

# Subscriptions automatically receive differential RFC 6902 JSON-patches:
live.set("cpu_usage", 18.7)
# -> Emits: event: patch \n data: {"op": "replace", "path": "/cpu_usage", "value": 18.7}
```

---

### 2.3 Sovereign Actor Mesh

Actors run concurrently in isolated execution contexts communicating strictly via bounded message queues:

```star
use Server

constant server = Server.app("WorkerService")

constant worker = server.spawn_actor("image_processor", function(msg)
    show "Processing file: " + msg["filename"]
    return {"status": "optimized", "bytes": 45000}
end)

# Fire-and-forget:
worker.send({"filename": "banner.png"})

# Request-Reply with synchronous/asynchronous future:
constant result = worker.ask({"filename": "avatar.png"}, timeout=2.0)
show "Processed result: " + result["status"]
```

---

## 3. Server-Side Scripting API Reference

### 3.1 Request Object (`req`)
- `req.method`: HTTP method string (`"GET"`, `"POST"`, `"PUT"`, `"DELETE"`, etc.)
- `req.path`: Normalized URL path string (e.g. `"/api/users/42"`)
- `req.params`: Map of captured URL route parameters (e.g. `{"id": "42"}`)
- `req.query`: Map of query parameters (e.g. `{"page": "2"}`)
- `req.headers`: Map of normalized HTTP request headers
- `req.body`: Raw request body string
- `req.json()`: Automatically parsed JSON payload into StarMap / StarList
- `req.form()`: Parsed URL-encoded form data map
- `req.ip`: Remote client IP address
- `req.param(name, default=null)`: Helper function to retrieve route parameter
- `req.header(name, default=null)`: Helper function to retrieve header value

### 3.2 Response Object (`res`)
- `res.status(code)`: Sets HTTP status code (chainable)
- `res.header(name, value)`: Sets HTTP response header (chainable)
- `res.json(data)`: Serializes Star data structure to UTF-8 JSON response
- `res.send(text)`: Transmits raw text or binary payload
- `res.html(html)`: Transmits HTML document with UTF-8 encoding
- `res.file(path)`: Streams static file with MIME detection, ETag, and 304 caching
- `res.redirect(url, code=302)`: Issues HTTP redirect
- `res.sse(event, data)`: Dispatches Server-Sent Event frame
- `res.error(message, code=500)`: Formats and sends standard JSON error payload

---

## 4. Enhanced Core Standard Library Methods

Star v1.3.0 introduces native method chaining on primitive types:

### 4.1 Text (`StarText`)
- `text.length` / `text.size`: Character count
- `text.uppercase()` / `text.lowercase()`: Case conversions
- `text.trim()`: Whitespace stripping
- `text.split(delimiter)`: Splitting into a `StarList`
- `text.contains(substr)`: Substring check
- `text.replace(from, to)`: Substring replacement
- `text.starts_with(prefix)` / `text.ends_with(suffix)`: Boundary tests

### 4.2 List (`StarList`)
- `list.length` / `list.size`: Element count
- `list.push(item)`: Appends element
- `list.pop()`: Removes and returns last element
- `list.join(delimiter)`: Concatenates elements into `StarText`
- `list.contains(item)`: Membership test
- `list.reverse()`: Returns reversed copy

### 4.3 Map (`StarMap`)
- `map.keys()`: Returns `StarList` of string keys
- `map.values()`: Returns `StarList` of values
- `map.has(key)`: Key existence check
- `map.size` / `map.length`: Key-value count
- `map.get(key, default=null)`: Safe key lookup

---

## 5. CLI Commands

```bash
# Start HyperFlow Server
star serve [file.star] [--port 8080] [--host 0.0.0.0]

# Inspect Registered Route Table
star server:routes [file.star]

# Execute Built-In Performance & Throughput Benchmark
star server:bench http://localhost:8080/api/health --requests 1000 --concurrency 20

# Scaffold New Server Project
star new my_api --template server
```
