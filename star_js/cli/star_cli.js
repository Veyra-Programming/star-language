#!/usr/bin/env node
/**
 * ============================================================================
 * ⭐ Star.js Unified CLI (star_cli.js)
 * High-speed developer CLI for Vite-server, Daemon, Cross-Platform Builds & SEO
 * ============================================================================
 */

const path = require('path');
const fs = require('fs');
const { createViteServer } = require('../bundler/star_vite.js');
const { StarPlatformPackager } = require('../platform/star_platform.js');
const { startDaemon, stopDaemon, statusDaemon } = require('../daemon/star_daemon.js');

const args = process.argv.slice(2);
const command = args[0] || 'portal';

function printHelp() {
  console.log(`
🌟 Star.js CLI — Universal Disruption-Tolerant Web & App Framework

Usage:
  star-js <command> [options]

Core Commands:
  dev [--port <port>]               Start Vite-like dev server with sub-10ms instant HMR
  build [--target <target>]         Build for target: web, pwa, desktop, android, ios
  create <app-name>                 Scaffold a new React-like Star.js cross-platform app
  preview [--port <port>]           Preview production build
  portal                            Open interactive Star.js Studio & ODCS Inspector

Daemon Commands:
  daemon start                      Start background CRDT sync relay & file-watcher
  daemon stop                       Stop background daemon
  daemon status                     Check daemon health and active CRDT queues
  daemon restart                    Restart background daemon
  daemon logs                       View recent daemon activity logs

SEO & Search Engine Plugins:
  sitemap                           Generate search engine sitemap.xml & robots.txt
  search <query>                    Query the fast inverted search index

Examples:
  star-js dev --port 4000
  star-js create my-dashboard
  star-js build --target desktop
  star-js daemon start
`);
}

switch (command) {
  case 'help':
  case '--help':
  case '-h':
    printHelp();
    break;

  case 'dev': {
    const portIdx = args.indexOf('--port');
    const port = portIdx !== -1 && args[portIdx + 1] ? Number(args[portIdx + 1]) : 3000;
    const rootDir = process.cwd();
    const server = createViteServer({ root: rootDir, port });
    server.start();
    break;
  }

  case 'build': {
    const targetIdx = args.indexOf('--target');
    const target = targetIdx !== -1 && args[targetIdx + 1] ? args[targetIdx + 1].toLowerCase() : 'web';
    const packager = new StarPlatformPackager({ rootDir: process.cwd() });
    packager.build(target);
    break;
  }

  case 'create':
  case 'new': {
    const appName = args[1];
    if (!appName) {
      console.error('❌ Error: App name required. Example: star-js create my-app');
      process.exit(1);
    }
    const packager = new StarPlatformPackager({ rootDir: process.cwd() });
    packager.createProject(appName);
    break;
  }

  case 'daemon': {
    const sub = args[1] || 'status';
    const daemonScript = path.join(__dirname, '..', 'daemon', 'star_daemon.js');
    require('child_process').fork(daemonScript, [sub], { stdio: 'inherit' });
    break;
  }

  case 'search': {
    const query = args.slice(1).join(' ');
    if (!query) {
      console.log('Please provide a query: star-js search <term>');
      break;
    }
    const Star = require('../star.js');
    const idx = new Star.FastSearchIndex();
    idx.addDocument({ id: '1', title: 'React Hooks in Star.js', category: 'Hooks', content: 'useState and useEffect manage state with zero dependencies' });
    idx.addDocument({ id: '2', title: 'ODCS CRDT Replication', category: 'Continuity', content: 'Conflict-free replicated data types sync state across nodes' });
    idx.addDocument({ id: '3', title: 'Vite-like Fast Dev Server', category: 'Tooling', content: 'Sub-10ms instant HMR and automatic sitemap generation' });
    idx.addDocument({ id: '4', title: 'Cross-Platform App Builder', category: 'Platform', content: 'Export to Web, PWA, Windows desktop, and Android native apps' });

    const results = idx.search(query);
    console.log(`\n🔍 Search Results for: "${query}" (${results.length} found):`);
    results.forEach((r, i) => {
      console.log(`  ${i + 1}. [${r.category}] ${r.title} (Score: ${r.score})`);
      console.log(`     ${r.snippet}`);
    });
    console.log('');
    break;
  }

  case 'sitemap': {
    const { StarSEOPlugin } = require('../bundler/star_vite.js');
    const seo = StarSEOPlugin();
    const sitemap = seo.generateSitemap();
    fs.writeFileSync(path.join(process.cwd(), 'sitemap.xml'), sitemap);
    const robots = seo.generateRobots();
    fs.writeFileSync(path.join(process.cwd(), 'robots.txt'), robots);
    console.log('✅ Generated sitemap.xml and robots.txt in current directory.');
    break;
  }

  case 'portal':
  default: {
    const portalIndex = path.resolve(__dirname, '..', 'index.html');
    console.log(`⭐ Opening Star.js Web & App Framework Portal: file:///${portalIndex.replace(/\\/g, '/')}`);
    const openCmd = process.platform === 'win32' ? 'start' : process.platform === 'darwin' ? 'open' : 'xdg-open';
    require('child_process').exec(`${openCmd} "${portalIndex}"`);
    break;
  }
}

