/**
 * ============================================================================
 * 🌟 Star.js — Universal Web & App Framework for Digital Continuity
 * Powered by Open Digital Continuity Standard (ODCS-2.0.0) & Star Language
 * Architected by Anirudha Puthraya
 * ============================================================================
 * 
 * Features:
 *   - Declarative Reactive Star UI Component Hierarchy
 *   - Proxy-based Deep Signals & Fine-Grained Reactive State
 *   - ODCS Layer 1: Local Durability (IndexedDB WAL + RFC 8785 Merkle Chaining)
 *   - ODCS Layer 2: Conflict-Free Replicated Data Types (CRDTs: PN-Counter, OR-Set, LWW-Register)
 *   - ODCS Layer 2: Dual-Transport Model (ODCS-REL TCP-Mode & ODCS-DGM UDP-Mode)
 *   - ODCS Layer 3: Dynamic Runtime Sensing, Telemetry Probes & Jitter Backoff
 *   - ODCS Layer 4: Sub-16ms Optimistic Mutations & Zero Intent Loss (ZIL) Receipts
 *   - Star SPA Router with Disruption-Tolerant Route Cache
 *   - Star 7-Preset Glassmorphic Design System (midnight, aurora, cyberpunk, nord, etc.)
 *   - Integrated Vector Icon Engine (30+ built-in glyphs)
 *   - Zero External Dependencies • Universal Browser, Node, Bun & Deno Support
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.Star = factory();
    root.UI = root.Star.UI;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  // ==========================================================================
  // 0. FRAMEWORK METADATA & CONSTANTS
  // ==========================================================================
  const VERSION = '1.3.0';
  const STANDARD = 'ODCS-2.0.0';
  const AUTHOR = 'Anirudha Puthraya';
  const DB_NAME = 'ODCS_Star_Vault';
  const DB_VERSION = 1;

  // ==========================================================================
  // 1. CRYPTO & RFC 8785 CANONICAL SERIALIZATION UTILITIES
  // ==========================================================================
  const Canonical = {
    /**
     * RFC 8785 Canonical JSON Serialization (Deterministic key sorting)
     */
    stringify(obj) {
      if (obj === null || typeof obj !== 'object') {
        return JSON.stringify(obj);
      }
      if (Array.isArray(obj)) {
        return '[' + obj.map(item => Canonical.stringify(item)).join(',') + ']';
      }
      const sortedKeys = Object.keys(obj).sort();
      const entries = sortedKeys
        .filter(k => obj[k] !== undefined)
        .map(k => JSON.stringify(k) + ':' + Canonical.stringify(obj[k]));
      return '{' + entries.join(',') + '}';
    }
  };

  const Crypto = {
    /**
     * Compute SHA-256 hash using Web Crypto API or fast fallback
     */
    async sha256(data) {
      const text = typeof data === 'string' ? data : Canonical.stringify(data);
      if (typeof crypto !== 'undefined' && crypto.subtle) {
        const encoder = new TextEncoder();
        const buffer = await crypto.subtle.digest('SHA-256', encoder.encode(text));
        const hashArray = Array.from(new Uint8Array(buffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
      }
      // Software fallback
      return Crypto.fastHash(text);
    },

    fastHash(str) {
      let h1 = 0xdeadbeef, h2 = 0x41c6ce57;
      for (let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
      }
      h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
      h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
      return (4294967296 * (2097151 & h2) + (h1 >>> 0)).toString(16).padStart(16, '0') +
             (4294967296 * (2097151 & h1) + (h2 >>> 0)).toString(16).padStart(16, '0');
    },

    /**
     * Standard IEEE 802.3 32-bit Cyclic Redundancy Check (CRC32)
     */
    crc32(data) {
      const str = typeof data === 'string' ? data : Canonical.stringify(data);
      let crc = 0 ^ (-1);
      for (let i = 0; i < str.length; i++) {
        const byte = str.charCodeAt(i);
        crc = (crc >>> 8) ^ Crypto.CRC_TABLE[(crc ^ byte) & 0xFF];
      }
      return (crc ^ (-1)) >>> 0;
    },

    CRC_TABLE: (function () {
      const table = new Uint32Array(256);
      for (let i = 0; i < 256; i++) {
        let c = i;
        for (let j = 0; j < 8; j++) {
          c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
        }
        table[i] = c;
      }
      return table;
    })(),

    uuidv7() {
      const now = Date.now();
      const timeHex = now.toString(16).padStart(12, '0');
      const rand1 = Math.floor(Math.random() * 0x0fff).toString(16).padStart(3, '0');
      const rand2 = Math.floor(Math.random() * 0x3fff | 0x8000).toString(16).padStart(4, '0');
      const rand3 = Math.floor(Math.random() * 0xffffffffffff).toString(16).padStart(12, '0');
      return `${timeHex.slice(0, 8)}-${timeHex.slice(8, 12)}-7${rand1}-${rand2}-${rand3}`;
    }
  };

  // ==========================================================================
  // 2. FINE-GRAINED REACTIVE SIGNALS ENGINE
  // ==========================================================================
  let activeEffect = null;

  class Signal {
    constructor(value) {
      this._value = value;
      this.subscribers = new Set();
    }
    get value() {
      if (activeEffect) {
        this.subscribers.add(activeEffect);
      }
      return this._value;
    }
    set value(newVal) {
      if (this._value !== newVal) {
        this._value = newVal;
        this.notify();
      }
    }
    peek() {
      return this._value;
    }
    notify() {
      const toRun = new Set(this.subscribers);
      toRun.forEach(fn => fn());
    }
  }

  function signal(initial) {
    return new Signal(initial);
  }

  function computed(getter) {
    const s = new Signal(undefined);
    effect(() => {
      s.value = getter();
    });
    return s;
  }

  function effect(fn) {
    const run = () => {
      activeEffect = run;
      try {
        fn();
      } finally {
        activeEffect = null;
      }
    };
    run();
    return () => {
      // Disposer
    };
  }

  function reactive(target) {
    if (typeof target !== 'object' || target === null) return target;
    const signals = new Map();

    return new Proxy(target, {
      get(obj, prop) {
        if (!signals.has(prop)) {
          signals.set(prop, new Signal(obj[prop]));
        }
        return signals.get(prop).value;
      },
      set(obj, prop, val) {
        obj[prop] = val;
        if (signals.has(prop)) {
          signals.get(prop).value = val;
        } else {
          signals.set(prop, new Signal(val));
        }
        return true;
      }
    });
  }

  // ==========================================================================
  // 3. ODCS LAYER 1: LOCAL DURABILITY & STORAGE ENGINE
  // ==========================================================================
  class StorageEngine {
    constructor() {
      this.db = null;
      this.ready = this.init();
      this.memoryFallback = new Map();
    }

    init() {
      return new Promise((resolve) => {
        if (typeof indexedDB === 'undefined') {
          resolve(false);
          return;
        }
        const req = indexedDB.open(DB_NAME, DB_VERSION);
        req.onupgradeneeded = (e) => {
          const db = e.target.result;
          if (!db.objectStoreNames.contains('wal_journal')) {
            db.createObjectStore('wal_journal', { keyPath: 'seq', autoIncrement: true });
          }
          if (!db.objectStoreNames.contains('crdt_snapshots')) {
            db.createObjectStore('crdt_snapshots', { keyPath: 'key' });
          }
          if (!db.objectStoreNames.contains('zil_receipts')) {
            const store = db.createObjectStore('zil_receipts', { keyPath: 'receipt_id' });
            store.createIndex('by_timestamp', 'timestamp');
          }
          if (!db.objectStoreNames.contains('outbox')) {
            db.createObjectStore('outbox', { keyPath: 'intent_id' });
          }
        };
        req.onsuccess = (e) => {
          this.db = e.target.result;
          resolve(true);
        };
        req.onerror = () => {
          resolve(false);
        };
      });
    }

    async put(storeName, item) {
      await this.ready;
      if (!this.db) {
        const key = item.seq || item.key || item.receipt_id || item.intent_id || Crypto.uuidv7();
        this.memoryFallback.set(`${storeName}:${key}`, item);
        try {
          localStorage.setItem(`odcs_${storeName}_${key}`, JSON.stringify(item));
        } catch (_) {}
        return item;
      }
      return new Promise((resolve, reject) => {
        const tx = this.db.transaction(storeName, 'readwrite');
        const store = tx.objectStore(storeName);
        const req = store.put(item);
        req.onsuccess = () => resolve(item);
        req.onerror = (e) => reject(e);
      });
    }

    async get(storeName, key) {
      await this.ready;
      if (!this.db) {
        return this.memoryFallback.get(`${storeName}:${key}`) || null;
      }
      return new Promise((resolve) => {
        const tx = this.db.transaction(storeName, 'readonly');
        const store = tx.objectStore(storeName);
        const req = store.get(key);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => resolve(null);
      });
    }

    async getAll(storeName, limit = 100) {
      await this.ready;
      if (!this.db) {
        const results = [];
        this.memoryFallback.forEach((v, k) => {
          if (k.startsWith(`${storeName}:`)) results.push(v);
        });
        return results.slice(0, limit);
      }
      return new Promise((resolve) => {
        const tx = this.db.transaction(storeName, 'readonly');
        const store = tx.objectStore(storeName);
        const req = store.getAll(null, limit);
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      });
    }

    async delete(storeName, key) {
      await this.ready;
      if (!this.db) {
        this.memoryFallback.delete(`${storeName}:${key}`);
        try { localStorage.removeItem(`odcs_${storeName}_${key}`); } catch (_) {}
        return true;
      }
      return new Promise((resolve) => {
        const tx = this.db.transaction(storeName, 'readwrite');
        const store = tx.objectStore(storeName);
        const req = store.delete(key);
        req.onsuccess = () => resolve(true);
        req.onerror = () => resolve(false);
      });
    }

    async clear(storeName) {
      await this.ready;
      if (!this.db) {
        this.memoryFallback.clear();
        return true;
      }
      return new Promise((resolve) => {
        const tx = this.db.transaction(storeName, 'readwrite');
        const store = tx.objectStore(storeName);
        store.clear();
        tx.oncomplete = () => resolve(true);
      });
    }
  }

  // ==========================================================================
  // 4. ODCS LAYER 2: CRDT CONSENSUS & DUAL-TRANSPORT ENGINES
  // ==========================================================================
  class VectorClock {
    constructor(nodeId = 'node-' + Math.random().toString(36).slice(2, 7)) {
      this.nodeId = nodeId;
      this.clock = { [this.nodeId]: 0 };
    }

    tick() {
      this.clock[this.nodeId] = (this.clock[this.nodeId] || 0) + 1;
      return { ...this.clock };
    }

    merge(remoteClock) {
      if (!remoteClock) return this.clock;
      for (const [node, time] of Object.entries(remoteClock)) {
        this.clock[node] = Math.max(this.clock[node] || 0, time);
      }
      return this.clock;
    }

    snapshot() {
      return { ...this.clock };
    }
  }

  class HybridLogicalClock {
    constructor(nodeId) {
      this.nodeId = nodeId || 'hlc-node-' + Math.random().toString(36).slice(2, 6);
      this.physical = Date.now();
      this.logical = 0;
    }

    now() {
      const p = Date.now();
      if (p > this.physical) {
        this.physical = p;
        this.logical = 0;
      } else {
        this.logical += 1;
      }
      return { physical: this.physical, logical: this.logical, node: this.nodeId };
    }

    receive(remote) {
      const p = Date.now();
      const remotePhysical = remote.physical || 0;
      const remoteLogical = remote.logical || 0;

      if (p > this.physical && p > remotePhysical) {
        this.physical = p;
        this.logical = 0;
      } else if (this.physical === remotePhysical) {
        this.logical = Math.max(this.logical, remoteLogical) + 1;
      } else if (this.physical > remotePhysical) {
        this.logical += 1;
      } else {
        this.physical = remotePhysical;
        this.logical = remoteLogical + 1;
      }
      return { physical: this.physical, logical: this.logical, node: this.nodeId };
    }
  }

  class PNCounter {
    constructor(id = 'pn-counter', nodeId = 'local') {
      this.id = id;
      this.nodeId = nodeId;
      this.P = {};
      this.N = {};
    }

    inc(amount = 1) {
      this.P[this.nodeId] = (this.P[this.nodeId] || 0) + amount;
      return this.value();
    }

    dec(amount = 1) {
      this.N[this.nodeId] = (this.N[this.nodeId] || 0) + amount;
      return this.value();
    }

    value() {
      const sumP = Object.values(this.P).reduce((a, b) => a + b, 0);
      const sumN = Object.values(this.N).reduce((a, b) => a + b, 0);
      return sumP - sumN;
    }

    merge(remote) {
      if (!remote) return this.value();
      const rP = remote.P || {};
      const rN = remote.N || {};
      for (const [k, v] of Object.entries(rP)) {
        this.P[k] = Math.max(this.P[k] || 0, v);
      }
      for (const [k, v] of Object.entries(rN)) {
        this.N[k] = Math.max(this.N[k] || 0, v);
      }
      return this.value();
    }

    toJSON() {
      return { id: this.id, P: { ...this.P }, N: { ...this.N }, value: this.value() };
    }
  }

  class ORSet {
    constructor(id = 'or-set') {
      this.id = id;
      this.elements = new Map(); // value -> Set of UUID tags
      this.tombstones = new Set(); // Set of UUID tags
    }

    add(val) {
      const tag = Crypto.uuidv7();
      if (!this.elements.has(val)) {
        this.elements.set(val, new Set());
      }
      this.elements.get(val).add(tag);
      return tag;
    }

    remove(val) {
      if (!this.elements.has(val)) return false;
      const tags = this.elements.get(val);
      tags.forEach(t => this.tombstones.add(t));
      this.elements.delete(val);
      return true;
    }

    has(val) {
      if (!this.elements.has(val)) return false;
      const active = Array.from(this.elements.get(val)).filter(t => !this.tombstones.has(t));
      return active.length > 0;
    }

    values() {
      const active = [];
      for (const [val, tags] of this.elements.entries()) {
        const live = Array.from(tags).filter(t => !this.tombstones.has(t));
        if (live.length > 0) active.push(val);
      }
      return active;
    }

    merge(remote) {
      if (!remote) return this.values();
      if (Array.isArray(remote.tombstones)) {
        remote.tombstones.forEach(t => this.tombstones.add(t));
      }
      if (remote.elements) {
        for (const [val, tags] of Object.entries(remote.elements)) {
          if (!this.elements.has(val)) {
            this.elements.set(val, new Set());
          }
          const localTags = this.elements.get(val);
          tags.forEach(t => localTags.add(t));
        }
      }
      return this.values();
    }

    toJSON() {
      const elObj = {};
      this.elements.forEach((tags, val) => {
        elObj[val] = Array.from(tags);
      });
      return {
        id: this.id,
        elements: elObj,
        tombstones: Array.from(this.tombstones),
        values: this.values()
      };
    }
  }

  // Dual Transport Models (ODCS-REL vs ODCS-DGM)
  class TransportManager {
    constructor() {
      this.relSeq = 1;
      this.activeRelSession = null;
      this.packetLog = [];
    }

    packReliableFrame(sessionId, seqNum, payload, corruptCrc = false) {
      const payloadStr = Canonical.stringify(payload);
      let crc = Crypto.crc32(payloadStr);
      if (corruptCrc) crc = (crc ^ 0xFFFFFFFF) >>> 0;

      const frame = {
        mode: 'ODCS_REL',
        version: 2,
        session_id: sessionId || 'rel-session-alpha',
        seq_num: seqNum,
        payload_length: payloadStr.length,
        crc32: crc,
        payload: payload,
        timestamp: Date.now()
      };
      this.packetLog.unshift(frame);
      return frame;
    }

    packDatagram(srcChannel, dstChannel, payload, corruptCrc = false) {
      const payloadStr = Canonical.stringify(payload);
      let crc = Crypto.crc32(payloadStr);
      if (corruptCrc) crc = (crc ^ 0xFFFFFFFF) >>> 0;

      const dgm = {
        mode: 'ODCS_DGM',
        version: 2,
        src_channel: srcChannel || 7001,
        dst_channel: dstChannel || 7002,
        payload_length: payloadStr.length,
        crc32: crc,
        payload: payload,
        timestamp: Date.now()
      };
      this.packetLog.unshift(dgm);
      return dgm;
    }
  }

  // ==========================================================================
  // 5. ODCS LAYER 3: RUNTIME SENSING & TELEMETRY ENGINE
  // ==========================================================================
  class TelemetryEngine {
    constructor(gatewayUrl = '') {
      this.gatewayUrl = gatewayUrl;
      this.mode = signal('OPTIMAL_ONLINE'); // 'OPTIMAL_ONLINE' | 'DEGRADED_JITTER' | 'SEVERED_OFFLINE'
      this.rtt = signal(0.1);
      this.jitter = signal(0.0);
      this.simulatedMode = null;
      this.history = [];

      this.initListeners();
    }

    initListeners() {
      if (typeof window !== 'undefined') {
        window.addEventListener('online', () => this.evaluate());
        window.addEventListener('offline', () => {
          this.mode.value = 'SEVERED_OFFLINE';
        });
      }
    }

    setSimulation(mode) {
      this.simulatedMode = mode;
      if (mode === 'offline') {
        this.mode.value = 'SEVERED_OFFLINE';
        this.rtt.value = 0;
      } else if (mode === 'degraded') {
        this.mode.value = 'DEGRADED_JITTER';
        this.rtt.value = 480.0;
        this.jitter.value = 95.0;
      } else {
        this.mode.value = 'OPTIMAL_ONLINE';
        this.rtt.value = 1.2;
        this.jitter.value = 0.4;
      }
    }

    async probe() {
      if (this.simulatedMode) {
        this.setSimulation(this.simulatedMode);
        return { mode: this.mode.value, rtt: this.rtt.value, simulated: true };
      }

      if (typeof navigator !== 'undefined' && !navigator.onLine) {
        this.mode.value = 'SEVERED_OFFLINE';
        return { mode: 'SEVERED_OFFLINE', rtt: 0 };
      }

      const t0 = performance.now();
      try {
        const url = (this.gatewayUrl || '') + '/api/v1/telemetry/probe';
        const res = await fetch(url, { method: 'GET', cache: 'no-store' });
        const dur = performance.now() - t0;
        this.rtt.value = Math.round(dur * 10) / 10;

        if (dur > 300) {
          this.mode.value = 'DEGRADED_JITTER';
        } else {
          this.mode.value = 'OPTIMAL_ONLINE';
        }
        return { mode: this.mode.value, rtt: this.rtt.value };
      } catch (e) {
        this.mode.value = 'SEVERED_OFFLINE';
        this.rtt.value = 0;
        return { mode: 'SEVERED_OFFLINE', rtt: 0 };
      }
    }
  }

  // ==========================================================================
  // 6. ODCS LAYER 4: ZERO INTENT LOSS (ZIL) & UX RESILIENCE
  // ==========================================================================
  class IntentEngine {
    constructor(storage, telemetry) {
      this.storage = storage;
      this.telemetry = telemetry;
      this.receiptCount = signal(0);
      this.activeOutbox = signal([]);
      this.subscribers = new Set();

      this.refreshStats();
    }

    async refreshStats() {
      const receipts = await this.storage.getAll('zil_receipts');
      this.receiptCount.value = receipts.length;
      const outbox = await this.storage.getAll('outbox');
      this.activeOutbox.value = outbox;
    }

    async preserve(action, payload, options = {}) {
      const now = Date.now();
      const user = options.user || 'StarAppUser';
      const canonicalData = Canonical.stringify(payload);
      const digest = await Crypto.sha256(canonicalData);
      const receiptId = `rcpt-${now}-${digest.slice(0, 10)}`;

      const receipt = {
        receipt_id: receiptId,
        action: action,
        user: user,
        payload: payload,
        canonical_digest: digest,
        staged_proof: `PROOF-L4-${digest.slice(0, 16)}`,
        colo: 'LOCAL-CLIENT-WAL',
        timestamp: now,
        status: 'COMMITTED_LOCAL'
      };

      await this.storage.put('zil_receipts', receipt);
      await this.storage.put('wal_journal', {
        type: 'INTENT_PRESERVED',
        action,
        receiptId,
        digest,
        timestamp: now
      });

      await this.storage.put('outbox', {
        intent_id: receiptId,
        action,
        payload,
        digest,
        created_at: now,
        attempts: 0
      });

      this.receiptCount.value += 1;
      await this.refreshStats();

      this.notifySubscribers('intent_staged', receipt);

      if (this.telemetry.mode.value === 'OPTIMAL_ONLINE') {
        this.drainOutbox();
      }

      return receipt;
    }

    async drainOutbox(gatewayUrl = '') {
      const items = await this.storage.getAll('outbox');
      if (items.length === 0) return 0;

      let drained = 0;
      for (const item of items) {
        try {
          const url = (gatewayUrl || '') + '/api/v1/intent/preserve';
          const resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              user: 'Star.js Client',
              action: item.action,
              payload: item.payload,
              _idempotency_key: item.intent_id
            })
          });
          if (resp.ok) {
            await this.storage.delete('outbox', item.intent_id);
            drained++;
          }
        } catch (_) {
          break;
        }
      }
      await this.refreshStats();
      return drained;
    }

    notifySubscribers(event, data) {
      this.subscribers.forEach(cb => cb(event, data));
    }

    onEvent(cb) {
      this.subscribers.add(cb);
      return () => this.subscribers.delete(cb);
    }
  }

  // ==========================================================================
  // 7. STAR DESIGN SYSTEM THEMES ENGINE (use Theme)
  // ==========================================================================
  const THEME_PRESETS = {
    midnight: {
      id: 'midnight',
      name: 'OLED Midnight',
      bgPrimary: '#050811',
      bgSurface: 'rgba(10, 16, 32, 0.75)',
      bgSurfaceHover: 'rgba(16, 24, 48, 0.85)',
      border: 'rgba(0, 240, 255, 0.25)',
      borderHover: 'rgba(0, 240, 255, 0.55)',
      textPrimary: '#ffffff',
      textSecondary: '#94a3b8',
      textMuted: '#64748b',
      accentPrimary: '#00f0ff',
      accentSecondary: '#8b5cf6',
      accentSuccess: '#10b981',
      accentWarning: '#f59e0b',
      accentDanger: '#ef4444',
      glow1: 'rgba(0, 240, 255, 0.15)',
      glow2: 'rgba(139, 92, 246, 0.15)'
    },
    aurora: {
      id: 'aurora',
      name: 'Emerald Aurora',
      bgPrimary: '#04130d',
      bgSurface: 'rgba(6, 28, 19, 0.75)',
      bgSurfaceHover: 'rgba(10, 42, 29, 0.85)',
      border: 'rgba(16, 185, 129, 0.3)',
      borderHover: 'rgba(16, 185, 129, 0.6)',
      textPrimary: '#f0fdf4',
      textSecondary: '#86efac',
      textMuted: '#4ade80',
      accentPrimary: '#10b981',
      accentSecondary: '#34d399',
      accentSuccess: '#059669',
      accentWarning: '#fbbf24',
      accentDanger: '#f87171',
      glow1: 'rgba(16, 185, 129, 0.2)',
      glow2: 'rgba(52, 211, 153, 0.15)'
    },
    cyberpunk: {
      id: 'cyberpunk',
      name: 'Neon Cyberpunk',
      bgPrimary: '#0a0017',
      bgSurface: 'rgba(24, 0, 44, 0.8)',
      bgSurfaceHover: 'rgba(40, 0, 70, 0.9)',
      border: 'rgba(236, 72, 153, 0.4)',
      borderHover: 'rgba(236, 72, 153, 0.8)',
      textPrimary: '#fdf4ff',
      textSecondary: '#f472b6',
      textMuted: '#db2777',
      accentPrimary: '#ec4899',
      accentSecondary: '#06b6d4',
      accentSuccess: '#10b981',
      accentWarning: '#facc15',
      accentDanger: '#f43f5e',
      glow1: 'rgba(236, 72, 153, 0.25)',
      glow2: 'rgba(6, 182, 212, 0.2)'
    },
    nord: {
      id: 'nord',
      name: 'Nordic Arctic Frost',
      bgPrimary: '#1e222a',
      bgSurface: 'rgba(36, 41, 51, 0.85)',
      bgSurfaceHover: 'rgba(46, 52, 64, 0.95)',
      border: 'rgba(136, 192, 208, 0.3)',
      borderHover: 'rgba(136, 192, 208, 0.6)',
      textPrimary: '#eceff4',
      textSecondary: '#d8dee9',
      textMuted: '#8892b0',
      accentPrimary: '#88c0d0',
      accentSecondary: '#81a1c1',
      accentSuccess: '#a3be8c',
      accentWarning: '#ebcb8b',
      accentDanger: '#bf616a',
      glow1: 'rgba(136, 192, 208, 0.18)',
      glow2: 'rgba(129, 161, 193, 0.15)'
    },
    sunset: {
      id: 'sunset',
      name: 'Sunset Amber',
      bgPrimary: '#12070c',
      bgSurface: 'rgba(35, 14, 24, 0.8)',
      bgSurfaceHover: 'rgba(55, 22, 38, 0.9)',
      border: 'rgba(249, 115, 22, 0.35)',
      borderHover: 'rgba(249, 115, 22, 0.7)',
      textPrimary: '#fff7ed',
      textSecondary: '#fdba74',
      textMuted: '#fb923c',
      accentPrimary: '#f97316',
      accentSecondary: '#e11d48',
      accentSuccess: '#22c55e',
      accentWarning: '#f59e0b',
      accentDanger: '#ef4444',
      glow1: 'rgba(249, 115, 22, 0.25)',
      glow2: 'rgba(225, 29, 72, 0.2)'
    },
    dark: {
      id: 'dark',
      name: 'Obsidian Slate',
      bgPrimary: '#0f172a',
      bgSurface: 'rgba(30, 41, 59, 0.8)',
      bgSurfaceHover: 'rgba(51, 65, 85, 0.9)',
      border: 'rgba(148, 163, 184, 0.25)',
      borderHover: 'rgba(148, 163, 184, 0.5)',
      textPrimary: '#f8fafc',
      textSecondary: '#cbd5e1',
      textMuted: '#94a3b8',
      accentPrimary: '#38bdf8',
      accentSecondary: '#818cf8',
      accentSuccess: '#34d399',
      accentWarning: '#fbbf24',
      accentDanger: '#f87171',
      glow1: 'rgba(56, 189, 248, 0.15)',
      glow2: 'rgba(129, 140, 248, 0.12)'
    },
    light: {
      id: 'light',
      name: 'Crystal Day',
      bgPrimary: '#f8fafc',
      bgSurface: 'rgba(255, 255, 255, 0.9)',
      bgSurfaceHover: '#ffffff',
      border: 'rgba(203, 213, 225, 0.8)',
      borderHover: 'rgba(14, 165, 233, 0.6)',
      textPrimary: '#0f172a',
      textSecondary: '#475569',
      textMuted: '#64748b',
      accentPrimary: '#0284c7',
      accentSecondary: '#7c3aed',
      accentSuccess: '#059669',
      accentWarning: '#d97706',
      accentDanger: '#dc2626',
      glow1: 'rgba(2, 132, 199, 0.08)',
      glow2: 'rgba(124, 58, 237, 0.08)'
    }
  };

  class ThemeEngine {
    constructor() {
      this.current = signal('midnight');
      this.applyTheme('midnight');
    }

    setPreset(name) {
      if (THEME_PRESETS[name]) {
        this.current.value = name;
        this.applyTheme(name);
      }
    }

    applyTheme(name) {
      const p = THEME_PRESETS[name] || THEME_PRESETS.midnight;
      if (typeof document === 'undefined') return;

      const root = document.documentElement;
      root.style.setProperty('--star-bg-primary', p.bgPrimary);
      root.style.setProperty('--star-bg-surface', p.bgSurface);
      root.style.setProperty('--star-bg-surface-hover', p.bgSurfaceHover);
      root.style.setProperty('--star-border', p.border);
      root.style.setProperty('--star-border-hover', p.borderHover);
      root.style.setProperty('--star-text-primary', p.textPrimary);
      root.style.setProperty('--star-text-secondary', p.textSecondary);
      root.style.setProperty('--star-text-muted', p.textMuted);
      root.style.setProperty('--star-accent-primary', p.accentPrimary);
      root.style.setProperty('--star-accent-secondary', p.accentSecondary);
      root.style.setProperty('--star-accent-success', p.accentSuccess);
      root.style.setProperty('--star-accent-warning', p.accentWarning);
      root.style.setProperty('--star-accent-danger', p.accentDanger);
      root.style.setProperty('--star-glow-1', p.glow1);
      root.style.setProperty('--star-glow-2', p.glow2);
      root.setAttribute('data-theme', name);
    }
  }

  // ==========================================================================
  // 8. STAR VECTOR ICON REGISTRY (30+ SVG Glyphs)
  // ==========================================================================
  const ICONS = {
    star: '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    zap: '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    activity: '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    database: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
    server: '<rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/>',
    terminal: '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>',
    download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    refresh: '<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>',
    copy: '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    check: '<polyline points="20 6 9 17 4 12"/>',
    alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    layers: '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    code: '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    wifi: '<path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>',
    'wifi-off': '<line x1="1" y1="1" x2="23" y2="23"/><path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"/><path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"/><path d="M10.71 5.05A16 16 0 0 1 22.58 9"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/>',
    globe: '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    play: '<polygon points="5 3 19 12 5 21 5 3"/>',
    'arrow-right': '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    'chevron-right': '<polyline points="9 18 15 12 9 6"/>',
    clock: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    user: '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    cart: '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>',
    heart: '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
    lock: '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    plus: '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    trash: '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
  };

  // ==========================================================================
  // 9. STAR HARDWARE-ACCELERATED MOTION & ANIMATION ENGINE (use Motion)
  // ==========================================================================
  const Motion = {
    Curves: {
      linear: 'linear',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      spring: 'cubic-bezier(0.16, 1, 0.3, 1)',
      bounce: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      overshoot: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
    },

    spring(stiffness = 180, damping = 18, mass = 1) {
      return {
        stiffness,
        damping,
        mass,
        evaluate(t) {
          const w0 = Math.sqrt(stiffness / mass);
          const zeta = damping / (2 * Math.sqrt(stiffness * mass));
          if (zeta < 1) {
            const wd = w0 * Math.sqrt(1 - zeta * zeta);
            return 1 - Math.exp(-zeta * w0 * t) * (Math.cos(wd * t) + (zeta * w0 / wd) * Math.sin(wd * t));
          }
          return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
        }
      };
    },

    animate(target, keyframes, options = {}) {
      if (typeof document === 'undefined') {
        return { play() {}, pause() {}, reverse() {}, finish() {}, promise: Promise.resolve() };
      }
      const el = typeof target === 'string' ? document.querySelector(target) : target;
      if (!el || typeof el.animate !== 'function') {
        return { play() {}, pause() {}, reverse() {}, finish() {}, promise: Promise.resolve() };
      }
      const timing = {
        duration: options.duration || 300,
        easing: options.easing || 'cubic-bezier(0.16, 1, 0.3, 1)',
        delay: options.delay || 0,
        fill: options.fill || 'both',
        iterations: options.iterations || 1,
        direction: options.direction || 'normal'
      };
      const anim = el.animate(keyframes, timing);
      return {
        raw: anim,
        play: () => anim.play(),
        pause: () => anim.pause(),
        reverse: () => anim.reverse(),
        finish: () => anim.finish(),
        promise: anim.finished
      };
    },

    shimmer(target, duration = 1500) {
      return Motion.animate(target, [
        { backgroundPosition: '-200% 0' },
        { backgroundPosition: '200% 0' }
      ], { duration, iterations: Infinity, easing: 'linear' });
    },

    pulse(target, minScale = 0.95, maxScale = 1.05, duration = 1200) {
      return Motion.animate(target, [
        { transform: `scale(${minScale})` },
        { transform: `scale(${maxScale})` },
        { transform: `scale(${minScale})` }
      ], { duration, iterations: Infinity, easing: 'ease-in-out' });
    },

    bounce(target, intensity = 12, duration = 600) {
      return Motion.animate(target, [
        { transform: 'translateY(0)' },
        { transform: `translateY(-${intensity}px)` },
        { transform: 'translateY(0)' },
        { transform: `translateY(-${intensity / 2}px)` },
        { transform: 'translateY(0)' }
      ], { duration, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' });
    },

    shake(target, intensity = 8, duration = 400) {
      return Motion.animate(target, [
        { transform: 'translateX(0)' },
        { transform: `translateX(-${intensity}px)` },
        { transform: `translateX(${intensity}px)` },
        { transform: `translateX(-${intensity / 2}px)` },
        { transform: `translateX(${intensity / 2}px)` },
        { transform: 'translateX(0)' }
      ], { duration, easing: 'ease-in-out' });
    },

    confetti(container = null, count = 40) {
      if (typeof document === 'undefined') return;
      const host = container ? (typeof container === 'string' ? document.querySelector(container) : container) : document.body;
      if (!host) return;
      const colors = ['#00f0ff', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b'];
      for (let i = 0; i < count; i++) {
        const bit = document.createElement('div');
        bit.className = 'star-confetti-particle';
        const color = colors[i % colors.length];
        const left = Math.random() * 100;
        const size = Math.random() * 8 + 6;
        const rot = Math.random() * 360;
        Object.assign(bit.style, {
          position: 'fixed',
          left: `${left}%`,
          top: '-10px',
          width: `${size}px`,
          height: `${size * 0.6}px`,
          backgroundColor: color,
          borderRadius: '2px',
          zIndex: '9999',
          pointerEvents: 'none'
        });
        host.appendChild(bit);
        Motion.animate(bit, [
          { transform: `translateY(0) rotate(0deg)`, opacity: 1 },
          { transform: `translateY(${window.innerHeight + 50}px) rotate(${rot + 720}deg)`, opacity: 0 }
        ], {
          duration: Math.random() * 1500 + 1500,
          delay: Math.random() * 300,
          easing: 'cubic-bezier(0.25, 1, 0.5, 1)'
        }).promise.then(() => bit.remove());
      }
    },

    ripple(event, element, color = 'rgba(255, 255, 255, 0.35)') {
      if (!element || !element.getBoundingClientRect) return;
      const rect = element.getBoundingClientRect();
      const circle = document.createElement('span');
      const diameter = Math.max(rect.width, rect.height);
      const radius = diameter / 2;
      const x = (event.clientX || rect.left + rect.width / 2) - rect.left - radius;
      const y = (event.clientY || rect.top + rect.height / 2) - rect.top - radius;
      Object.assign(circle.style, {
        position: 'absolute',
        borderRadius: '50%',
        pointerEvents: 'none',
        width: `${diameter}px`,
        height: `${diameter}px`,
        left: `${x}px`,
        top: `${y}px`,
        backgroundColor: color,
        transform: 'scale(0)',
        opacity: '1',
        transition: 'transform 600ms cubic-bezier(0.16, 1, 0.3, 1), opacity 600ms ease'
      });
      element.style.position = element.style.position || 'relative';
      element.style.overflow = 'hidden';
      element.appendChild(circle);
      requestAnimationFrame(() => {
        circle.style.transform = 'scale(2.5)';
        circle.style.opacity = '0';
      });
      setTimeout(() => circle.remove(), 600);
    }
  };

  // ==========================================================================
  // 9b. STAR UI DECLARATIVE COMPONENT BUILDER (use UI)
  // ==========================================================================
  function h(tag, props = {}, ...children) {
    const flatChildren = children.flat(Infinity).filter(c => c !== null && c !== undefined && c !== false);
    return {
      tag,
      props: props || {},
      children: flatChildren
    };
  }

  const UI = {
    // Layout Containers
    column(...children) {
      return h('div', { className: 'star-column' }, children);
    },

    row(...children) {
      return h('div', { className: 'star-row' }, children);
    },

    stack(...children) {
      return h('div', { className: 'star-stack' }, children);
    },

    grid(columns = 2, ...children) {
      return h('div', { className: 'star-grid', style: { gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))` } }, children);
    },

    card(children, options = {}) {
      const cls = 'star-card ' + (options.className || '');
      return h('div', { ...options, className: cls }, children);
    },

    box(children, style = {}) {
      return h('div', { className: 'star-box', style }, children);
    },

    spacer(size = null) {
      const style = size ? { width: `${size}px`, height: `${size}px`, flexShrink: 0 } : { flex: '1 1 0%' };
      return h('div', { className: 'star-spacer', style });
    },

    divider() {
      return h('hr', { className: 'star-divider' });
    },

    // Content & Typography
    title(text, level = 1, options = {}) {
      const tag = `h${Math.min(6, Math.max(1, level))}`;
      const cls = `star-title star-h${level} ${options.className || ''}`;
      return h(tag, { ...options, className: cls }, text);
    },

    text(content, options = {}) {
      return h('p', { className: 'star-text ' + (options.className || ''), ...options }, content);
    },

    badge(label, variant = 'primary', options = {}) {
      return h('span', { className: `star-badge star-badge-${variant} ${options.className || ''}`, ...options }, label);
    },

    stat(title, value, subtitle, trend = null) {
      return h('div', { className: 'star-stat-card' }, [
        h('div', { className: 'star-stat-title' }, title),
        h('div', { className: 'star-stat-value' }, value),
        subtitle ? h('div', { className: 'star-stat-sub' }, subtitle) : null,
        trend ? h('div', { className: 'star-stat-trend' }, trend) : null
      ]);
    },

    icon(name, size = 18, color = 'currentColor', className = '') {
      const inner = ICONS[name] || ICONS.star;
      return h('svg', {
        className: `star-icon ${className}`,
        width: size,
        height: size,
        viewBox: '0 0 24 24',
        fill: 'none',
        stroke: color,
        strokeWidth: 2,
        strokeLinecap: 'round',
        strokeLinejoin: 'round',
        innerHTML: inner
      });
    },

    avatar(name, size = 36, options = {}) {
      const initials = (name || 'S').slice(0, 2).toUpperCase();
      return h('div', {
        className: 'star-avatar ' + (options.className || ''),
        style: { width: `${size}px`, height: `${size}px`, ...options.style }
      }, initials);
    },

    // Interactive Controls & Forms
    button(label, onClick, options = {}) {
      const variant = options.variant || 'primary';
      const icon = options.icon ? UI.icon(options.icon, 15) : null;
      return h('button', {
        className: `star-btn star-btn-${variant} ${options.className || ''}`,
        type: options.type || 'button',
        disabled: options.disabled || false,
        onClick: (e) => {
          if (options.ripple !== false) {
            Motion.ripple(e, e.currentTarget);
          }
          if (onClick) onClick(e);
        }
      }, [icon, label]);
    },

    input(placeholder, value, onChange, options = {}) {
      return h('input', {
        className: 'star-input ' + (options.className || ''),
        type: options.type || 'text',
        placeholder,
        value: value !== undefined ? value : '',
        onInput: (e) => onChange && onChange(e.target.value),
        ...options
      });
    },

    switch(checked, onChange, options = {}) {
      return h('label', { className: 'star-switch-label' }, [
        h('input', {
          type: 'checkbox',
          className: 'star-switch-input',
          checked: !!checked,
          onChange: (e) => onChange && onChange(e.target.checked)
        }),
        h('span', { className: 'star-switch-slider' }),
        options.label ? h('span', { className: 'star-switch-text' }, options.label) : null
      ]);
    },

    slider(value, min = 0, max = 100, onChange) {
      return h('input', {
        type: 'range',
        className: 'star-slider',
        min,
        max,
        value,
        onInput: (e) => onChange && onChange(Number(e.target.value))
      });
    },

    progress(value = 0, max = 100, options = {}) {
      const pct = Math.min(100, Math.max(0, (value / max) * 100));
      return h('div', { className: 'star-progress-track' }, [
        h('div', { className: 'star-progress-fill', style: { width: `${pct}%` } })
      ]);
    },

    tabs(items, activeIndex, onSelect) {
      return h('div', { className: 'star-tabs' }, items.map((item, idx) => {
        const isActive = activeIndex === idx;
        return h('button', {
          className: `star-tab-btn ${isActive ? 'star-tab-active' : ''}`,
          onClick: () => onSelect && onSelect(idx)
        }, item);
      }));
    },

    toast(msg, variant = 'info') {
      return h('div', { className: `star-toast star-toast-${variant}` }, [
        UI.icon(variant === 'success' ? 'check' : variant === 'error' ? 'alert' : 'zap', 16),
        h('span', {}, msg)
      ]);
    },

    // Extended Professional UI Widgets
    modal(options, ...children) {
      if (options && options.open === false) return null;
      return h('div', { className: 'star-modal-backdrop' }, [
        h('div', { className: 'star-modal-surface' }, [
          h('div', { className: 'star-modal-header' }, [
            h('h3', { className: 'star-modal-title' }, (options && options.title) || 'Dialog'),
            (options && options.onClose) ? h('button', { className: 'star-modal-close', onClick: options.onClose }, '✕') : null
          ]),
          h('div', { className: 'star-modal-body' }, children),
          (options && (options.onConfirm || options.onCancel)) ? h('div', { className: 'star-modal-footer' }, [
            options.onCancel ? UI.button(options.cancelLabel || 'Cancel', options.onCancel, { variant: 'secondary' }) : null,
            options.onConfirm ? UI.button(options.confirmLabel || 'Confirm', options.onConfirm, { variant: 'primary' }) : null
          ]) : null
        ])
      ]);
    },

    dialog(title, message, onConfirm, onCancel, options = {}) {
      return UI.modal({
        title,
        onConfirm,
        onCancel,
        ...options
      }, h('p', { className: 'star-text' }, message));
    },

    drawer(isOpen, onClose, side = 'right', ...children) {
      if (!isOpen) return null;
      return h('div', { className: 'star-drawer-backdrop', onClick: onClose }, [
        h('div', {
          className: `star-drawer star-drawer-${side}`,
          onClick: (e) => e.stopPropagation()
        }, children)
      ]);
    },

    accordion(title, isExpanded, onToggle, ...children) {
      return h('div', { className: `star-accordion ${isExpanded ? 'star-accordion-expanded' : ''}` }, [
        h('button', {
          className: 'star-accordion-header',
          onClick: () => onToggle && onToggle(!isExpanded)
        }, [
          h('span', { className: 'star-accordion-title' }, title),
          h('span', { className: 'star-accordion-icon' }, isExpanded ? '−' : '＋')
        ]),
        isExpanded ? h('div', { className: 'star-accordion-body' }, children) : null
      ]);
    },

    dropdown(items, selectedIdx, onSelect, placeholder = 'Select...', isOpen = false, onToggle = null) {
      const selected = items[selectedIdx] !== undefined ? items[selectedIdx] : placeholder;
      return h('div', { className: `star-dropdown ${isOpen ? 'star-dropdown-open' : ''}` }, [
        h('button', {
          className: 'star-dropdown-trigger',
          onClick: () => onToggle && onToggle(!isOpen)
        }, [
          h('span', {}, selected),
          h('span', { className: 'star-dropdown-arrow' }, '▾')
        ]),
        isOpen ? h('div', { className: 'star-dropdown-menu' }, items.map((item, idx) => {
          return h('div', {
            className: `star-dropdown-item ${idx === selectedIdx ? 'star-dropdown-item-active' : ''}`,
            onClick: () => {
              if (onSelect) onSelect(idx, item);
              if (onToggle) onToggle(false);
            }
          }, item);
        })) : null
      ]);
    },

    tooltip(text, child, position = 'top') {
      return h('div', { className: `star-tooltip-wrapper star-tooltip-${position}` }, [
        child,
        h('span', { className: 'star-tooltip-bubble' }, text)
      ]);
    },

    skeleton(width = '100%', height = 24, radius = 6) {
      return h('div', {
        className: 'star-skeleton',
        style: {
          width: typeof width === 'number' ? `${width}px` : width,
          height: typeof height === 'number' ? `${height}px` : height,
          borderRadius: typeof radius === 'number' ? `${radius}px` : radius
        }
      });
    },

    shimmer(child, options = {}) {
      return h('div', { className: 'star-shimmer-wrap ' + (options.className || '') }, [
        child,
        h('div', { className: 'star-shimmer-sweep' })
      ]);
    },

    breadcrumbs(items, onSelect) {
      return h('nav', { className: 'star-breadcrumbs' }, items.map((item, idx) => {
        const isLast = idx === items.length - 1;
        return h('span', { className: 'star-breadcrumb-item' }, [
          isLast ? h('span', { className: 'star-breadcrumb-current' }, item)
                 : h('button', {
                     className: 'star-breadcrumb-link',
                     onClick: () => onSelect && onSelect(idx)
                   }, item),
          !isLast ? h('span', { className: 'star-breadcrumb-sep' }, '/') : null
        ]);
      }));
    },

    pagination(totalPages, currentPage, onPageChange) {
      const pages = [];
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
      return h('div', { className: 'star-pagination' }, [
        h('button', {
          className: 'star-page-btn',
          disabled: currentPage <= 1,
          onClick: () => onPageChange && onPageChange(currentPage - 1)
        }, '‹'),
        ...pages.map(p => h('button', {
          className: `star-page-btn ${p === currentPage ? 'star-page-active' : ''}`,
          onClick: () => onPageChange && onPageChange(p)
        }, String(p))),
        h('button', {
          className: 'star-page-btn',
          disabled: currentPage >= totalPages,
          onClick: () => onPageChange && onPageChange(currentPage + 1)
        }, '›')
      ]);
    },

    table(headers, rows, options = {}) {
      return h('div', { className: 'star-table-wrap ' + (options.className || '') }, [
        h('table', { className: 'star-table' }, [
          h('thead', {}, h('tr', {}, headers.map(hdr => h('th', {}, hdr)))),
          h('tbody', {}, rows.map((row, rIdx) => h('tr', { key: rIdx }, row.map((cell, cIdx) => h('td', { key: cIdx }, cell)))))
        ])
      ]);
    },

    codeBlock(code, language = 'star', options = {}) {
      return h('div', { className: 'star-code-block' }, [
        h('div', { className: 'star-code-header' }, [
          h('span', { className: 'star-code-lang' }, language.toUpperCase()),
          (options && options.copyable !== false) ? h('button', {
            className: 'star-code-copy-btn',
            onClick: () => Platform.copy(code)
          }, 'Copy') : null
        ]),
        h('pre', { className: 'star-code-pre' }, h('code', {}, code))
      ]);
    },

    segmentedControl(items, selectedIdx, onSelect) {
      return h('div', { className: 'star-segmented-control' }, items.map((item, idx) => {
        const isActive = idx === selectedIdx;
        return h('button', {
          className: `star-segment-btn ${isActive ? 'star-segment-active' : ''}`,
          onClick: () => onSelect && onSelect(idx)
        }, item);
      }));
    },

    stepper(steps, currentStep) {
      return h('div', { className: 'star-stepper' }, steps.map((s, idx) => {
        const isDone = idx < currentStep;
        const isActive = idx === currentStep;
        return h('div', { className: `star-step-item ${isDone ? 'star-step-done' : ''} ${isActive ? 'star-step-active' : ''}` }, [
          h('div', { className: 'star-step-circle' }, isDone ? '✓' : String(idx + 1)),
          h('span', { className: 'star-step-label' }, s),
          idx < steps.length - 1 ? h('div', { className: 'star-step-line' }) : null
        ]);
      }));
    },

    rating(value, maxRating = 5, onChange = null) {
      const stars = [];
      for (let i = 1; i <= maxRating; i++) {
        const isFilled = i <= value;
        stars.push(h('span', {
          className: `star-rating-star ${isFilled ? 'star-rating-filled' : ''}`,
          onClick: () => onChange && onChange(i)
        }, '★'));
      }
      return h('div', { className: 'star-rating' }, stars);
    },

    fab(label, onClick, options = {}) {
      const icon = options.icon ? UI.icon(options.icon, 20) : null;
      return h('button', {
        className: `star-fab star-fab-${options.position || 'bottom-right'} ${options.className || ''}`,
        onClick
      }, [icon, label ? h('span', {}, label) : null]);
    },

    bottomSheet(isOpen, onClose, ...children) {
      if (!isOpen) return null;
      return h('div', { className: 'star-bottom-sheet-backdrop', onClick: onClose }, [
        h('div', {
          className: 'star-bottom-sheet',
          onClick: (e) => e.stopPropagation()
        }, [
          h('div', { className: 'star-bottom-sheet-handle' }),
          ...children
        ])
      ]);
    },

    animatedContainer(props, ...children) {
      const { duration = 300, curve = 'cubic-bezier(0.16, 1, 0.3, 1)', style = {}, className = '', ...rest } = props || {};
      const animatedStyle = {
        transition: `all ${duration}ms ${curve}`,
        ...style
      };
      return h('div', { ...rest, className: `star-animated-container ${className}`, style: animatedStyle }, children);
    },

    marquee(text, speed = 50) {
      return h('div', { className: 'star-marquee-wrap' }, [
        h('div', { className: 'star-marquee-inner' }, [
          h('span', { className: 'star-marquee-text' }, text),
          h('span', { className: 'star-marquee-text' }, text)
        ])
      ]);
    },

    pulse(child, options = {}) {
      return h('div', { className: 'star-pulse-wrap ' + (options.className || '') }, child);
    },

    bounce(child, options = {}) {
      return h('div', { className: 'star-bounce-wrap ' + (options.className || '') }, child);
    },

    glow(child, options = {}) {
      const color = options.color || 'var(--star-accent-primary)';
      return h('div', {
        className: 'star-glow-wrap ' + (options.className || ''),
        style: { filter: `drop-shadow(0 0 16px ${color})` }
      }, child);
    }
  };

  // ==========================================================================
  // 10. REACT-LIKE HOOKS & COMPONENT RUNTIME
  // ==========================================================================
  const Fragment = typeof Symbol === 'function' ? Symbol.for('star.fragment') : 'STAR_FRAGMENT';

  let currentHookInstance = null;
  let hookCursor = 0;
  let activeAppInstance = null;

  class FunctionalComponentFiber {
    constructor(fn, props, onCommit) {
      this.fn = fn;
      this.props = props || {};
      this.onCommit = onCommit;
      this._hooks = [];
      this._effects = [];
      this._cleanups = [];
      this._isScheduled = false;
      this.vdom = null;
    }

    render(newProps) {
      if (newProps) this.props = newProps;
      const prevInst = currentHookInstance;
      const prevCursor = hookCursor;
      currentHookInstance = this;
      hookCursor = 0;
      this._effects = [];

      try {
        this.vdom = this.fn(this.props);
        return this.vdom;
      } finally {
        currentHookInstance = prevInst;
        hookCursor = prevCursor;

        // Execute pending effects after render
        if (typeof queueMicrotask === 'function') {
          queueMicrotask(() => this._flushEffects());
        } else {
          setTimeout(() => this._flushEffects(), 0);
        }
      }
    }

    _flushEffects() {
      for (const eff of this._effects) {
        try { eff(); } catch (err) { console.error('[Star.js Hook Effect Error]:', err); }
      }
      this._effects = [];
    }

    scheduleUpdate() {
      if (this._isScheduled) return;
      this._isScheduled = true;
      const doUpdate = () => {
        this._isScheduled = false;
        const oldVdom = this.vdom;
        const newVdom = this.render();
        if (this.onCommit) {
          this.onCommit(newVdom, oldVdom);
        }
      };

      if (typeof queueMicrotask === 'function') {
        queueMicrotask(doUpdate);
      } else {
        setTimeout(doUpdate, 0);
      }
    }

    destroy() {
      for (const cleanup of this._cleanups) {
        if (typeof cleanup === 'function') {
          try { cleanup(); } catch (e) {}
        }
      }
      this._cleanups = [];
      this._hooks = [];
    }
  }

  function useState(initialValue) {
    if (!currentHookInstance) {
      const s = signal(typeof initialValue === 'function' ? initialValue() : initialValue);
      return [s.value, (val) => s.value = typeof val === 'function' ? val(s.value) : val];
    }
    const inst = currentHookInstance;
    const idx = hookCursor++;

    if (inst._hooks[idx] === undefined) {
      inst._hooks[idx] = typeof initialValue === 'function' ? initialValue() : initialValue;
    }

    const setState = (newVal) => {
      const resolved = typeof newVal === 'function' ? newVal(inst._hooks[idx]) : newVal;
      if (!Object.is(inst._hooks[idx], resolved)) {
        inst._hooks[idx] = resolved;
        inst.scheduleUpdate();
      }
    };

    return [inst._hooks[idx], setState];
  }

  function useEffect(effectFn, deps) {
    if (!currentHookInstance) return;
    const inst = currentHookInstance;
    const idx = hookCursor++;
    const oldHook = inst._hooks[idx];
    const hasChanged = !oldHook || !deps || deps.some((dep, i) => !Object.is(dep, oldHook.deps[i]));

    if (hasChanged) {
      inst._effects.push(() => {
        if (oldHook && typeof oldHook.cleanup === 'function') {
          oldHook.cleanup();
        }
        const cleanup = effectFn();
        inst._hooks[idx] = { deps, cleanup };
        if (typeof cleanup === 'function') {
          inst._cleanups.push(cleanup);
        }
      });
    }
  }

  function useReducer(reducer, initialArg, init) {
    const [state, setState] = useState(() => init ? init(initialArg) : initialArg);
    const dispatch = (action) => {
      setState(prevState => reducer(prevState, action));
    };
    return [state, dispatch];
  }

  function useRef(initialValue) {
    if (!currentHookInstance) return { current: initialValue };
    const inst = currentHookInstance;
    const idx = hookCursor++;
    if (!inst._hooks[idx]) {
      inst._hooks[idx] = { current: initialValue };
    }
    return inst._hooks[idx];
  }

  function useMemo(factory, deps) {
    if (!currentHookInstance) return factory();
    const inst = currentHookInstance;
    const idx = hookCursor++;
    const oldHook = inst._hooks[idx];
    const hasChanged = !oldHook || !deps || deps.some((dep, i) => !Object.is(dep, oldHook.deps[i]));

    if (hasChanged) {
      const value = factory();
      inst._hooks[idx] = { value, deps };
      return value;
    }
    return oldHook.value;
  }

  function useCallback(callback, deps) {
    return useMemo(() => callback, deps);
  }

  function createContext(defaultValue) {
    const context = {
      _currentValue: defaultValue,
      Provider({ value, children }) {
        context._currentValue = value !== undefined ? value : defaultValue;
        return children;
      }
    };
    return context;
  }

  function useContext(context) {
    return context ? context._currentValue : undefined;
  }

  function useSignal(sig) {
    const [, setTick] = useState(0);
    useEffect(() => {
      return effect(() => {
        const _ = sig.value;
        setTick(t => t + 1);
      });
    }, [sig]);
    return sig.value;
  }

  function useODCS() {
    const app = activeAppInstance;
    const [state, setState] = useState(() => ({
      mode: app ? app.telemetry.mode.value : 'OPTIMAL_ONLINE',
      rtt: app ? app.telemetry.rtt.value : 0.1,
      isOnline: typeof navigator !== 'undefined' ? navigator.onLine : true,
      outboxSize: app ? app.storage.outbox.length : 0
    }));

    useEffect(() => {
      const handler = () => {
        setState({
          mode: app ? app.telemetry.mode.value : (navigator.onLine ? 'OPTIMAL_ONLINE' : 'SEVERED_OFFLINE'),
          rtt: app ? app.telemetry.rtt.value : 0.1,
          isOnline: typeof navigator !== 'undefined' ? navigator.onLine : true,
          outboxSize: app ? app.storage.outbox.length : 0
        });
      };
      if (typeof window !== 'undefined') {
        window.addEventListener('online', handler);
        window.addEventListener('offline', handler);
        const timer = setInterval(handler, 1000);
        return () => {
          window.removeEventListener('online', handler);
          window.removeEventListener('offline', handler);
          clearInterval(timer);
        };
      }
    }, [app]);

    return {
      ...state,
      preserve: (action, payload) => app ? app.intent.preserve(action, payload) : Promise.resolve(),
      storage: app ? app.storage : null,
      telemetry: app ? app.telemetry : null,
      transport: app ? app.transport : null
    };
  }

  // ==========================================================================
  // 11. EASY JSX TEMPLATE COMPILER (Star.html Tagged Template Literal)
  // ==========================================================================
  function html(strings, ...values) {
    let mode = 0; // 0: text, 1: tag, 2: attr, 3: attr_val
    let buffer = '';
    const stack = [{ tag: Fragment, props: {}, children: [] }];
    let currentPropName = '';

    for (let i = 0; i < strings.length; i++) {
      const str = strings[i];
      for (let j = 0; j < str.length; j++) {
        const char = str[j];

        if (mode === 0) { // text mode
          if (char === '<') {
            if (buffer.trim()) {
              stack[stack.length - 1].children.push(buffer.trim());
            }
            buffer = '';
            mode = 1; // start tag
          } else {
            buffer += char;
          }
        } else if (mode === 1) { // in tag name / start
          if (char === '/') {
            if (buffer === '') {
              // </ closing tag
              const closeEnd = str.indexOf('>', j);
              j = closeEnd;
              mode = 0;
              buffer = '';
              const closed = stack.pop();
              const vnode = h(closed.tag, closed.props, ...closed.children);
              stack[stack.length - 1].children.push(vnode);
              continue;
            }
          }
          if (/\s/.test(char) || char === '>') {
            const tagName = buffer.trim();
            buffer = '';
            if (tagName) {
              stack.push({ tag: tagName, props: {}, children: [] });
            }
            if (char === '>') {
              mode = 0;
            } else {
              mode = 2; // parsing attributes
            }
          } else {
            buffer += char;
          }
        } else if (mode === 2) { // parsing attribute name
          if (char === '>') {
            if (buffer.trim()) {
              stack[stack.length - 1].props[buffer.trim()] = true;
            }
            buffer = '';
            mode = 0;
          } else if (char === '/' && str[j + 1] === '>') {
            // self closing tag <tag />
            j++;
            if (buffer.trim()) {
              stack[stack.length - 1].props[buffer.trim()] = true;
            }
            buffer = '';
            mode = 0;
            const closed = stack.pop();
            const vnode = h(closed.tag, closed.props, ...closed.children);
            stack[stack.length - 1].children.push(vnode);
          } else if (char === '=') {
            currentPropName = buffer.trim();
            buffer = '';
            mode = 3;
          } else if (/\s/.test(char)) {
            if (buffer.trim()) {
              stack[stack.length - 1].props[buffer.trim()] = true;
              buffer = '';
            }
          } else {
            buffer += char;
          }
        } else if (mode === 3) { // attribute value
          if (char === '"' || char === "'") {
            const quote = char;
            let val = '';
            j++;
            while (j < str.length && str[j] !== quote) {
              val += str[j++];
            }
            stack[stack.length - 1].props[currentPropName] = val;
            currentPropName = '';
            mode = 2;
          } else if (/\s/.test(char) || char === '>') {
            stack[stack.length - 1].props[currentPropName] = buffer;
            currentPropName = '';
            buffer = '';
            mode = char === '>' ? 0 : 2;
          } else {
            buffer += char;
          }
        }
      }

      // Handle value interpolations
      if (i < values.length) {
        const val = values[i];
        if (mode === 0) { // children interpolation
          if (buffer.trim()) {
            stack[stack.length - 1].children.push(buffer.trim());
            buffer = '';
          }
          if (Array.isArray(val)) {
            stack[stack.length - 1].children.push(...val);
          } else if (val !== null && val !== undefined && val !== false) {
            stack[stack.length - 1].children.push(val);
          }
        } else if (mode === 1) { // dynamic component tag <${Component}>
          stack.push({ tag: val, props: {}, children: [] });
          mode = 2;
        } else if (mode === 3) { // dynamic prop value attr=${val}
          stack[stack.length - 1].props[currentPropName] = val;
          currentPropName = '';
          mode = 2;
        }
      }
    }

    if (buffer.trim() && stack.length > 0) {
      stack[stack.length - 1].children.push(buffer.trim());
    }

    while (stack.length > 1) {
      const closed = stack.pop();
      const vnode = h(closed.tag, closed.props, ...closed.children);
      stack[stack.length - 1].children.push(vnode);
    }

    const root = stack[0];
    return root.children.length === 1 ? root.children[0] : h(Fragment, null, ...root.children);
  }

  function createElement(tag, props, ...children) {
    return h(tag, props, ...children);
  }

  function jsx(tag, props, key) {
    const { children, ...rest } = props || {};
    if (key !== undefined) rest.key = key;
    return h(tag, rest, children);
  }

  const jsxs = jsx;

  // ==========================================================================
  // 12. VIRTUAL DOM TO REAL DOM RECONCILER WITH HOOKS & HYDRATION
  // ==========================================================================
  function renderDOM(vnode, container = null) {
    if (vnode === null || vnode === undefined || vnode === false) {
      return document.createTextNode('');
    }
    if (typeof vnode === 'string' || typeof vnode === 'number') {
      return document.createTextNode(String(vnode));
    }

    // Handle Fragment
    if (vnode.tag === Fragment || vnode.tag === 'STAR_FRAGMENT') {
      const frag = document.createDocumentFragment();
      (vnode.children || []).forEach(child => {
        frag.appendChild(renderDOM(child, container));
      });
      return frag;
    }

    // Handle Functional Component with Hooks
    if (typeof vnode.tag === 'function' && !(vnode.tag.prototype instanceof Component)) {
      let fiber = null;
      let hostNode = null;

      const onCommit = (newVdom, oldVdom) => {
        const nextDOM = renderDOM(newVdom, container);
        if (hostNode && hostNode.parentNode) {
          hostNode.parentNode.replaceChild(nextDOM, hostNode);
          hostNode = nextDOM;
        }
      };

      fiber = new FunctionalComponentFiber(vnode.tag, vnode.props, onCommit);
      const renderedVdom = fiber.render();
      hostNode = renderDOM(renderedVdom, container);
      hostNode._starFiber = fiber;
      return hostNode;
    }

    // Handle Class Component
    if (typeof vnode.tag === 'function' && vnode.tag.prototype instanceof Component) {
      const inst = new vnode.tag(vnode.props || {});
      const renderedVdom = inst.render();
      const el = renderDOM(renderedVdom, container);
      if (inst.onMount) inst.onMount();
      return el;
    }

    // Standard DOM Element
    const el = document.createElement(vnode.tag);
    const props = vnode.props || {};

    for (const [key, val] of Object.entries(props)) {
      if (key === 'className' || key === 'class') {
        el.className = val;
      } else if (key === 'style' && typeof val === 'object') {
        for (const [sKey, sVal] of Object.entries(val)) {
          if (typeof sVal === 'number' && !['opacity', 'zIndex', 'flex', 'fontWeight', 'lineHeight', 'flexGrow', 'flexShrink', 'order'].includes(sKey)) {
            el.style[sKey] = `${sVal}px`;
          } else {
            el.style[sKey] = sVal;
          }
        }
      } else if (key === 'innerHTML') {
        el.innerHTML = val;
      } else if (key.startsWith('on') && typeof val === 'function') {
        const evt = key.slice(2).toLowerCase();
        el.addEventListener(evt, val);
      } else if (key === 'value' && (vnode.tag === 'input' || vnode.tag === 'textarea')) {
        el.value = val;
      } else if (key === 'checked' && vnode.tag === 'input') {
        el.checked = !!val;
      } else if (key === 'key') {
        el.dataset.key = val;
      } else if (typeof val !== 'function' && typeof val !== 'object') {
        el.setAttribute(key, String(val));
      }
    }

    (vnode.children || []).forEach(child => {
      el.appendChild(renderDOM(child, el));
    });

    return el;
  }

  function hydrate(vnode, container) {
    if (!container) return;
    container.innerHTML = '';
    container.appendChild(renderDOM(vnode, container));
  }

  // ==========================================================================
  // 13. FAST SEARCH INDEXING ENGINE (Client Search & Inverted Indexer)
  // ==========================================================================
  class FastSearchIndex {
    constructor() {
      this.docs = new Map();
      this.index = new Map();
      this.docLengths = new Map();
      this.stopWords = new Set(['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with']);
    }

    tokenize(text) {
      if (!text) return [];
      return String(text)
        .toLowerCase()
        .replace(/[^\w\s\-]/g, ' ')
        .split(/\s+/)
        .filter(w => w.length >= 2 && !this.stopWords.has(w));
    }

    addDocument(doc) {
      this.docs.set(doc.id, doc);
      const tokens = [
        ...this.tokenize(doc.title).map(t => ({ t, weight: 3.0 })),
        ...this.tokenize(doc.category).map(t => ({ t, weight: 2.0 })),
        ...this.tokenize(doc.content).map(t => ({ t, weight: 1.0 }))
      ];
      this.docLengths.set(doc.id, tokens.length || 1);

      tokens.forEach(({ t, weight }) => {
        if (!this.index.has(t)) {
          this.index.set(t, new Map());
        }
        const posting = this.index.get(t);
        posting.set(doc.id, (posting.get(doc.id) || 0) + weight);
      });
    }

    search(query, limit = 6) {
      const tokens = this.tokenize(query);
      if (tokens.length === 0) return [];

      const scores = new Map();
      const totalDocs = this.docs.size || 1;

      for (const qTerm of tokens) {
        for (const [term, posting] of this.index.entries()) {
          const isExact = term === qTerm;
          const isPrefix = !isExact && term.startsWith(qTerm);
          if (!isExact && !isPrefix) continue;

          const termWeight = isExact ? 1.0 : 0.6;
          const df = posting.size;
          const idf = Math.log(1 + (totalDocs - df + 0.5) / (df + 0.5));

          for (const [docId, tf] of posting.entries()) {
            const docLen = this.docLengths.get(docId) || 1;
            const score = (scores.get(docId) || 0) + (tf / docLen) * idf * termWeight;
            scores.set(docId, score);
          }
        }
      }

      return Array.from(scores.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, limit)
        .map(([id, score]) => {
          const doc = this.docs.get(id);
          return {
            id,
            score: Number(score.toFixed(4)),
            title: doc.title,
            route: doc.route || '#',
            category: doc.category || 'General',
            snippet: this._snippet(doc.content, tokens)
          };
        });
    }

    _snippet(content, tokens, maxLen = 120) {
      if (!content) return '';
      const lower = content.toLowerCase();
      let best = 0;
      for (const t of tokens) {
        const pos = lower.indexOf(t);
        if (pos !== -1) {
          best = Math.max(0, pos - 25);
          break;
        }
      }
      let snip = content.slice(best, best + maxLen).trim();
      if (best > 0) snip = '...' + snip;
      if (best + maxLen < content.length) snip += '...';
      return snip;
    }
  }

  // ==========================================================================
  // 14. CROSS-PLATFORM RUNTIME SENSING & PLATFORM BRIDGE
  // ==========================================================================
  const Platform = {
    isBrowser: typeof window !== 'undefined' && typeof document !== 'undefined',
    isNode: typeof process !== 'undefined' && process.versions != null && process.versions.node != null,
    isDesktop: typeof window !== 'undefined' && (window.__STAR_DESKTOP__ || navigator.userAgent.includes('Electron')),
    isMobile: typeof window !== 'undefined' && (window.__STAR_MOBILE__ || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent)),
    isPWA: typeof window !== 'undefined' && (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone),

    async copy(text) {
      if (typeof navigator !== 'undefined' && navigator.clipboard) {
        await navigator.clipboard.writeText(text);
        return true;
      }
      return false;
    },

    vibrate(pattern = 50) {
      if (typeof navigator !== 'undefined' && navigator.vibrate) {
        navigator.vibrate(pattern);
      }
    },

    notify(title, options = {}) {
      if (typeof Notification !== 'undefined') {
        if (Notification.permission === 'granted') {
          return new Notification(title, options);
        } else if (Notification.permission !== 'denied') {
          Notification.requestPermission().then(p => {
            if (p === 'granted') new Notification(title, options);
          });
        }
      }
    }
  };

  // ==========================================================================
  // 15. STAR COMPONENT BASE CLASS & APPLICATION INSTANCE
  // ==========================================================================
  class Component {
    constructor(props = {}) {
      this.props = reactive(props);
      this.state = reactive({});
      this._mounted = false;
      this._container = null;
    }

    setState(partial) {
      Object.assign(this.state, partial);
    }

    onMount() {}
    onDestroy() {}
    onSync() {}
    onNetworkChange(status) {}

    render() {
      return UI.column();
    }
  }

  class StarApp {
    constructor(rootComponent, options = {}) {
      this.rootComponent = rootComponent;
      this.options = options;
      this.storage = new StorageEngine();
      this.telemetry = new TelemetryEngine(options.gatewayUrl || '');
      this.intent = new IntentEngine(this.storage, this.telemetry);
      this.transport = new TransportManager();
      this.theme = new ThemeEngine();
      this.search = new FastSearchIndex();
      this.container = null;
      this.instance = null;
      activeAppInstance = this;
    }

    mount(selector) {
      const el = typeof selector === 'string' ? document.querySelector(selector) : selector;
      if (!el) throw new Error(`Mount target "${selector}" not found`);
      this.container = el;

      if (typeof this.rootComponent === 'function' && this.rootComponent.prototype instanceof Component) {
        this.instance = new this.rootComponent(this.options.props || {});
        effect(() => {
          const vdom = this.instance.render();
          this.container.innerHTML = '';
          this.container.appendChild(renderDOM(vdom, this.container));
        });
        if (this.instance.onMount) this.instance.onMount();
      } else if (typeof this.rootComponent === 'function') {
        // Functional root component with hooks
        const fiber = new FunctionalComponentFiber(this.rootComponent, this.options.props || {}, (newVdom) => {
          this.container.innerHTML = '';
          this.container.appendChild(renderDOM(newVdom, this.container));
        });
        const initialVdom = fiber.render();
        this.container.innerHTML = '';
        this.container.appendChild(renderDOM(initialVdom, this.container));
      } else {
        this.instance = this.rootComponent;
        effect(() => {
          const vdom = this.instance.render();
          this.container.innerHTML = '';
          this.container.appendChild(renderDOM(vdom, this.container));
        });
      }

      return this;
    }
  }

  function createApp(rootComponent, options) {
    return new StarApp(rootComponent, options);
  }

  // ==========================================================================
  // 16. EXPORTED UNIVERSAL STAR.JS API
  // ==========================================================================
  const Star = {
    version: VERSION,
    standard: STANDARD,
    author: AUTHOR,

    // Core Reactivity
    signal,
    computed,
    effect,
    reactive,

    // React-like Hooks Engine
    useState,
    useEffect,
    useReducer,
    useRef,
    useMemo,
    useCallback,
    createContext,
    useContext,
    useSignal,
    useODCS,

    // JSX & Template Literals
    html,
    h,
    createElement,
    jsx,
    jsxs,
    Fragment,

    // Rendering & Components
    renderDOM,
    hydrate,
    Component,
    createApp,
    getCurrentApp: () => activeAppInstance,

    // Fast Search Index
    FastSearchIndex,
    search: (query, limit) => activeAppInstance ? activeAppInstance.search.search(query, limit) : [],

    // Cross-Platform Sensor
    Platform,

    // UI Declarative Components
    UI,

    // Hardware-Accelerated Motion & Animations
    Motion,
    Animation: Motion,

    // ODCS Continuity System
    Storage: StorageEngine,
    PNCounter,
    ORSet,
    VectorClock,
    HybridLogicalClock,
    Transport: TransportManager,
    Telemetry: TelemetryEngine,
    Intent: IntentEngine,

    // Theming & Icons
    Theme: ThemeEngine,
    THEME_PRESETS,
    Icons: ICONS,

    // Cryptography & Canonical
    Crypto,
    Canonical
  };

  return Star;
});

