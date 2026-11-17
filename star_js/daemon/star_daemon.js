/**
 * ============================================================================
 * 🛡️ Star.js Background Daemon Engine (star_daemon.js)
 * Persistent Background Service for CRDT Relay, File-Watcher, Fast Indexing & Health
 * ============================================================================
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const DAEMON_PORT = 7788;
const PID_FILE = path.join(process.cwd(), '.star_daemon.pid');
const LOG_FILE = path.join(process.cwd(), '.star_daemon.log');

class StarDaemon {
  constructor(options = {}) {
    this.port = options.port || DAEMON_PORT;
    this.server = null;
    this.startTime = Date.now();
    this.crdtStore = {
      pnCounters: {},
      orSets: {}
    };
    this.pendingOutbox = [];
    this.searchIndex = null;
    this.subscribers = new Set();
  }

  log(msg) {
    const entry = `[${new Date().toISOString()}] [StarDaemon] ${msg}\n`;
    try {
      fs.appendFileSync(LOG_FILE, entry);
    } catch (e) {}
    if (!process.env.STAR_DAEMON_SILENT) {
      process.stdout.write(entry);
    }
  }

  startServer() {
    this.server = http.createServer((req, res) => this.handleApi(req, res));
    this.server.listen(this.port, () => {
      this.log(`🌟 Star.js Background Daemon active on port ${this.port}`);
      this.log(`   - CRDT Hub & Relay: http://localhost:${this.port}/api/v1/daemon/crdt/sync`);
      this.log(`   - Health & Status: http://localhost:${this.port}/api/v1/daemon/status`);
      this.log(`   - Fast Search Query: http://localhost:${this.port}/api/v1/daemon/search`);
    });

    this.server.on('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        this.log(`Port ${this.port} is already in use by another StarDaemon instance.`);
      } else {
        this.log(`Daemon server error: ${err.message}`);
      }
    });

    this.initSearchIndex();
  }

  initSearchIndex() {
    this.searchIndex = {
      docs: [
        { id: '1', title: 'React Hooks in Star.js', category: 'Framework', route: '/docs/hooks', content: 'useState, useEffect, useReducer, and useSignal provide familiar state and lifecycle hooks with zero external dependencies.' },
        { id: '2', title: 'ODCS Disruption Continuity Architecture', category: 'Continuity', route: '/docs/odcs', content: '4-layer model guaranteeing local durability, CRDT consensus, runtime sensing, and zero intent loss receipts.' },
        { id: '3', title: 'Vite-like Lightning Dev Server', category: 'Tooling', route: '/docs/vite', content: 'Native ESM server with sub-10ms Hot Module Replacement, sitemap generation, and SEO structured schema.' },
        { id: '4', title: 'Cross-Platform Build Engine', category: 'Platform', route: '/docs/cross-platform', content: 'Build universal apps for Web, PWA, Desktop (Windows exe), and Mobile (Android APK) from one codebase.' },
        { id: '5', title: 'Star.html Easy Tagged Template Syntax', category: 'Syntax', route: '/docs/syntax', content: 'Ergonomic JSX-like syntax without needing Babel or heavy build pipelines.' }
      ]
    };
    this.log(`Search Index loaded with ${this.searchIndex.docs.length} core knowledge records.`);
  }

  handleApi(req, res) {
    const setCors = () => {
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    };

    setCors();

    if (req.method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }

    const parsedUrl = new URL(req.url, `http://localhost:${this.port}`);

    // GET /api/v1/daemon/status
    if (parsedUrl.pathname === '/api/v1/daemon/status') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        status: 'ONLINE',
        uptime_seconds: Math.floor((Date.now() - this.startTime) / 1000),
        port: this.port,
        crdt_counters: Object.keys(this.crdtStore.pnCounters).length,
        crdt_sets: Object.keys(this.crdtStore.orSets).length,
        outbox_queue_depth: this.pendingOutbox.length,
        memory_usage: process.memoryUsage(),
        version: '1.0.0',
        standard: 'ODCS-2.0.0'
      }, null, 2));
      return;
    }

    // POST /api/v1/daemon/crdt/sync
    if (parsedUrl.pathname === '/api/v1/daemon/crdt/sync' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', () => {
        try {
          const payload = JSON.parse(body);
          if (payload.pnCounter) {
            const { id, P, N } = payload.pnCounter;
            if (!this.crdtStore.pnCounters[id]) this.crdtStore.pnCounters[id] = { P: {}, N: {} };
            const cur = this.crdtStore.pnCounters[id];
            for (const [node, val] of Object.entries(P || {})) {
              cur.P[node] = Math.max(cur.P[node] || 0, val);
            }
            for (const [node, val] of Object.entries(N || {})) {
              cur.N[node] = Math.max(cur.N[node] || 0, val);
            }
          }
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: true, store: this.crdtStore }));
        } catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: e.message }));
        }
      });
      return;
    }

    // GET /api/v1/daemon/search?q=...
    if (parsedUrl.pathname === '/api/v1/daemon/search') {
      const q = (parsedUrl.searchParams.get('q') || '').toLowerCase();
      if (!q) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ results: [] }));
        return;
      }
      const matches = this.searchIndex.docs.filter(d =>
        d.title.toLowerCase().includes(q) ||
        d.category.toLowerCase().includes(q) ||
        d.content.toLowerCase().includes(q)
      );
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ query: q, count: matches.length, results: matches }));
      return;
    }

    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found in Star.js Daemon');
  }

  stop() {
    this.log('🛑 Shutting down StarDaemon gracefully...');
    if (this.server) {
      this.server.close();
    }
    if (fs.existsSync(PID_FILE)) {
      try { fs.unlinkSync(PID_FILE); } catch (e) {}
    }
  }
}

// ============================================================================
// DAEMON CLI LIFECYCLE MANAGEMENT
// ============================================================================

function startDaemon() {
  if (fs.existsSync(PID_FILE)) {
    const pid = fs.readFileSync(PID_FILE, 'utf-8').trim();
    try {
      process.kill(Number(pid), 0);
      console.log(`⭐ Star.js Daemon is ALREADY running (PID: ${pid}).`);
      return;
    } catch (e) {
      // Stale PID file
      fs.unlinkSync(PID_FILE);
    }
  }

  console.log(`⭐ Starting Star.js Background Daemon on port ${DAEMON_PORT}...`);
  const daemon = new StarDaemon();
  daemon.startServer();
  fs.writeFileSync(PID_FILE, String(process.pid));

  process.on('SIGINT', () => { daemon.stop(); process.exit(0); });
  process.on('SIGTERM', () => { daemon.stop(); process.exit(0); });
}

function stopDaemon() {
  if (!fs.existsSync(PID_FILE)) {
    console.log(`⭐ Star.js Daemon is NOT running.`);
    return;
  }
  const pid = fs.readFileSync(PID_FILE, 'utf-8').trim();
  try {
    process.kill(Number(pid), 'SIGTERM');
    console.log(`⭐ Stopped Star.js Daemon (PID: ${pid}).`);
    try { fs.unlinkSync(PID_FILE); } catch (e) {}
  } catch (err) {
    console.warn(`Could not kill process ${pid}: ${err.message}`);
    try { fs.unlinkSync(PID_FILE); } catch (e) {}
  }
}

function statusDaemon() {
  if (!fs.existsSync(PID_FILE)) {
    console.log(`⭐ Star.js Daemon Status: INACTIVE (Stopped)`);
    return;
  }
  const pid = fs.readFileSync(PID_FILE, 'utf-8').trim();
  try {
    process.kill(Number(pid), 0);
    console.log(`⭐ Star.js Daemon Status: RUNNING (PID: ${pid}, Port: ${DAEMON_PORT})`);
    console.log(`   - Logs: ${LOG_FILE}`);
  } catch (err) {
    console.log(`⭐ Star.js Daemon Status: INACTIVE (Stale PID file cleaned)`);
    try { fs.unlinkSync(PID_FILE); } catch (e) {}
  }
}

function viewLogs() {
  if (fs.existsSync(LOG_FILE)) {
    const logs = fs.readFileSync(LOG_FILE, 'utf-8');
    const lines = logs.trim().split('\n');
    console.log(`\n--- Star.js Daemon Logs (Last ${Math.min(lines.length, 25)} lines) ---`);
    console.log(lines.slice(-25).join('\n'));
    console.log('-----------------------------------------------------\n');
  } else {
    console.log(`No logs found at ${LOG_FILE}`);
  }
}

// Entrypoint dispatcher
const cmd = process.argv[2] || 'status';
if (cmd === 'start') {
  startDaemon();
} else if (cmd === 'stop') {
  stopDaemon();
} else if (cmd === 'status') {
  statusDaemon();
} else if (cmd === 'restart') {
  stopDaemon();
  setTimeout(startDaemon, 500);
} else if (cmd === 'logs') {
  viewLogs();
}

module.exports = {
  StarDaemon,
  startDaemon,
  stopDaemon,
  statusDaemon
};

