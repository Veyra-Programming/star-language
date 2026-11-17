# 🌟 Star.js — Universal Disruption-Proof Web & App Framework

> **React-like hooks (`useState`, `useEffect`), easy declarative `Star.html` syntax, cross-platform native builds (Web, PWA, Desktop, Mobile), Vite-like dev server, and persistent background daemon — all powered by the Open Digital Continuity Standard (ODCS-2.0.0).**  
> **Sub-16ms optimistic reactivity. Zero Intent Loss across total network blackouts.**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](package.json)
[![Standard](https://img.shields.io/badge/standard-ODCS--2.0.0-cyan.svg)](https://odcs.in)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Zero)-brightgreen.svg)](star.js)
[![License](https://img.shields.io/badge/license-Apache--2.0-orange.svg)](package.json)

---

## 🚀 Quick Overview

**Star.js** is a universal JavaScript web and application framework that bridges the visual clarity of **Star UI** and modern React-like component models with the enterprise disruption tolerance of the **Open Digital Continuity Standard (ODCS)**.

Whether targeting modern browsers, progressive web apps (PWAs), Windows desktop executables, or Android native apps, Star.js guarantees that user operations remain fluid, responsive, and cryptographically preserved even during complete network partitions, 480ms+ satellite jitter, or power grid failures.

---

## ✨ Key Capabilities

1. **React-like Hooks & Lifecycle Engine**:
   - `useState`, `useEffect`, `useReducer`, `useRef`, `useMemo`, `useCallback`, `createContext`, `useContext`, `useSignal`, and `useODCS`.
   - Familiar, intuitive state and effect management with zero build-step overhead.
2. **Easy Tagged Template Syntax (`Star.html`)**:
   - Zero-dependency HTML/JSX tagged template literal compiler:
     ```javascript
     return Star.html`
       <div class="card" onClick=${handleClick}>
         <h2>${title}</h2>
         <button disabled=${loading}>Count: ${count}</button>
       </div>
     `;
     ```
   - No Babel, webpack, or transpiler required. Pure standard vanilla JavaScript.
3. **Cross-Platform App Creation Suite**:
   - **Web & PWA**: Offline Service Worker, Stale-While-Revalidate caching, manifest, and 100/100 Lighthouse SEO score.
   - **Windows Desktop**: Zero-dependency Edge WebView2 wrapper executable with local WAL durability.
   - **Android Native (APK)**: Native WebView container with `AndroidManifest.xml`, offline asset bundle, hardware back-button listener, and touch vibration.
   - **iOS WebKit**: Safe-area insets, MetalKit shader acceleration, and touch event bridge.
4. **Vite-like Lightning Dev Server & Plugin Engine**:
   - Instant sub-10ms Hot Module Replacement (HMR).
   - Zero bundle startup: native ESM serving without upfront bundling.
5. **SEO & Fast Indexing Search Engine Plugins**:
   - **`StarSEOPlugin`**: Automatic injection of `<title>`, meta descriptions, Open Graph, Twitter Cards, Googlebot JSON-LD schemas, `sitemap.xml`, and `robots.txt`.
   - **`StarFastIndexPlugin`**: Build-time and runtime inverted search indexer with TF-IDF scoring and sub-millisecond client queries.
   - **`StarPWAPlugin`**: Automatic generation of `sw.js` and `manifest.webmanifest`.
6. **Background Daemon Engine (`StarDaemon`)**:
   - Persistent background process listening on port `7788`.
   - Shared CRDT sync hub keeping multi-tab and multi-window state replicated.
   - High-speed file watcher with instant HMR patch broadcasting.
   - Background outbox auto-drain queue.
7. **ODCS 4-Layer Disruption Continuity Architecture**:
   - **Layer 1: Local Durability**: IndexedDB WAL (`ODCS_Star_Vault`) with RFC 8785 canonical SHA-256 Merkle chaining.
   - **Layer 2: CRDT Consensus**: State-based `PNCounter` and Add-Wins `ORSet` models for Strong Eventual Consistency (SEC).
   - **Layer 2: Dual Transport Wire**: `ODCS-REL` (TCP-mode sequenced frames) + `ODCS-DGM` (UDP-mode 0-RTT datagrams with IEEE CRC32).
   - **Layer 3: Runtime Sensing**: Active RTT ping probing, jitter ratio monitoring, and adaptive mode shifting.
   - **Layer 4: Zero Intent Loss (ZIL)**: Sub-16ms optimistic UI mutations and tamper-evident cryptographic receipts.
8. **7-Preset Glassmorphic Design System**:
   - Instant theme switching: `midnight`, `aurora`, `cyberpunk`, `nord`, `sunset`, `dark`, and `light`.
9. **Zero External Dependencies**:
   - Self-contained standalone bundle (`Star.js` / `star.js`) with zero third-party npm runtime dependencies.

---

## 🛠️ CLI Reference

From your terminal or command prompt:

```bash
# Start Vite-like Dev Server with Sub-10ms Instant HMR
star js dev
# or: star-js dev --port 4000

# Scaffold a New Cross-Platform App
star js create my-app
# or: star-js create my-dashboard --template react-continuity

# Cross-Platform Builds
star js build --target web       # Optimized Web SPA
star js build --target pwa       # PWA with offline Service Worker & manifest
star js build --target desktop   # Windows Desktop wrapper
star js build --target android   # Android Native APK scaffolding

# Background Daemon Controls
star js daemon start             # Start background CRDT sync relay & watcher
star js daemon status            # Check daemon health & active queues
star js daemon logs              # View recent activity logs
star js daemon stop              # Gracefully shut down daemon

# SEO & Fast Search Indexing
star js sitemap                  # Generate sitemap.xml and robots.txt
star js search "crdt"            # Query fast inverted search index

# Launch Interactive Web Studio & ODCS Inspector
star js portal
```

---

## 💻 60-Second Quickstart (React Hooks + Star.html)

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Star.js App</title>
  <link rel="stylesheet" href="style.css">
  <script src="star.js"></script>
</head>
<body>
  <div id="app"></div>

  <script>
    const { useState, useEffect, useODCS, html, createApp } = Star;

    function App() {
      const [count, setCount] = useState(0);
      const odcs = useODCS();

      const handleClick = async () => {
        setCount(c => c + 1);
        // Mint Layer 4 ZIL receipt in <16ms!
        await odcs.preserve("CLICK", { count: count + 1 });
      };

      return html`
        <div class="star-card">
          <h2>🌟 Disruption-Tolerant Reactivity</h2>
          <p>Active Network Mode: <strong>${odcs.mode}</strong></p>
          <p>Current Count: <strong>${count}</strong></p>
          <button class="star-btn star-btn-primary" onClick=${handleClick}>
            Preserve Intent (+1)
          </button>
        </div>
      `;
    }

    createApp(App).mount("#app");
  </script>
</body>
</html>
```

---

## 🏛️ The Four ODCS Continuity Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: Application Continuity UX & Zero Intent Loss      │
│  • Sub-16ms Optimistic Mutations                            │
│  • ZIL Cryptographic Receipts (rcpt-179453-38e9a)           │
│  • Durable Outbox Pipeline & Idempotent Auto-Drain          │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Runtime Sensing & Telemetry Sensing               │
│  • Active/Passive RTT Probing (<1ms to 480ms Jitter)        │
│  • Battery, Storage Quota & Satellite Adaptation Policies   │
│  • Modes: OPTIMAL_ONLINE | DEGRADED_JITTER | SEVERED_OFFLINE│
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Transport & CRDT Consensus                        │
│  • Strong Eventual Consistency (SEC)                        │
│  • PN-Counter, Add-Wins OR-Set & Hybrid Logical Clock (HLC) │
│  • Dual-Transport: ODCS-REL (TCP-mode) & ODCS-DGM (UDP-mode)│
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Local Durability & Storage Anchor                 │
│  • Non-volatile IndexedDB WAL (ODCS_Star_Vault)             │
│  • Monotonic Sequence Counters & UUIDv7 Monotonic IDs       │
│  • RFC 8785 Canonical JSON Serialization & Hardware SHA-256 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Interactive Studio & Pre-Built Demos

Open `index.html` in your browser to launch the complete interactive **Star.js Studio, Cross-Platform Builder & ODCS Inspector**:

* 🛒 **Offline POS & E-Commerce**: `examples/offline_store.html`
* 🏥 **Emergency Field Triage**: `examples/emergency_triage.html`
* 💬 **CRDT Multi-Node Collab**: `examples/crdt_collaboration.html`

---

## 📄 License & Attribution

Architected by **Anirudha Puthraya** as part of the **Open Digital Continuity Standard (ODCS)** and the **Star Programming Language Ecosystem**.  
Released under the **Apache-2.0 License**.
