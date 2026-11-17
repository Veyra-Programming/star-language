/**
 * ============================================================================
 * ⚡ Star.js Vite-like Dev Server & Plugin Engine (star_vite.js)
 * High-speed ESM-native dev server, instant HMR, SEO & Fast Search Indexing
 * ============================================================================
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.webmanifest': 'application/manifest+json',
  '.wasm': 'application/wasm'
};

// ============================================================================
// 1. BUILT-IN PLUGINS
// ============================================================================

/**
 * 🌟 StarSEOPlugin: Production SEO, OpenGraph, Twitter Cards, JSON-LD & Sitemap
 */
function StarSEOPlugin(options = {}) {
  const config = {
    title: options.title || 'Star.js — Universal Disruption-Proof App',
    description: options.description || 'Built on Star.js and ODCS v2.0 with React-like hooks and local durability.',
    keywords: options.keywords || ['star.js', 'react', 'odcs', 'crdt', 'offline-first', 'vite'],
    canonicalUrl: options.canonicalUrl || 'https://starjs.dev',
    siteName: options.siteName || 'Star.js',
    author: options.author || 'Anirudha Puthraya',
    ogImage: options.ogImage || '/og-image.png',
    twitterHandle: options.twitterHandle || '@star_lang',
    routes: options.routes || ['/', '/docs', '/studio', '/examples'],
    jsonLd: options.jsonLd || {
      '@context': 'https://schema.org',
      '@type': 'WebApplication',
      name: options.title || 'Star.js Application',
      applicationCategory: 'Productivity',
      operatingSystem: 'Universal (Web, Desktop, Mobile)',
      author: {
        '@type': 'Person',
        name: 'Anirudha Puthraya'
      }
    }
  };

  return {
    name: 'star-plugin-seo',
    renderHtml(htmlContent) {
      const keywordsStr = Array.isArray(config.keywords) ? config.keywords.join(', ') : config.keywords;
      const jsonLdStr = JSON.stringify(config.jsonLd, null, 2);

      const seoTags = `
    <!-- 🌟 Star.js Automated SEO Engine -->
    <title>${config.title}</title>
    <meta name="description" content="${config.description}">
    <meta name="keywords" content="${keywordsStr}">
    <meta name="author" content="${config.author}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="${config.canonicalUrl}">

    <!-- Open Graph / Facebook Meta Tags -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="${config.siteName}">
    <meta property="og:title" content="${config.title}">
    <meta property="og:description" content="${config.description}">
    <meta property="og:image" content="${config.ogImage}">
    <meta property="og:url" content="${config.canonicalUrl}">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:site" content="${config.twitterHandle}">
    <meta name="twitter:creator" content="${config.twitterHandle}">
    <meta name="twitter:title" content="${config.title}">
    <meta name="twitter:description" content="${config.description}">
    <meta name="twitter:image" content="${config.ogImage}">

    <!-- JSON-LD Structured Data Schema for Googlebot -->
    <script type="application/ld+json">
${jsonLdStr}
    </script>
`;
      if (htmlContent.includes('<head>')) {
        return htmlContent.replace('<head>', `<head>${seoTags}`);
      }
      return seoTags + htmlContent;
    },

    generateSitemap(domain = 'https://starjs.dev') {
      const now = new Date().toISOString().split('T')[0];
      const urls = config.routes.map(r => `  <url>
    <loc>${domain}${r}</loc>
    <lastmod>${now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>${r === '/' ? '1.0' : '0.8'}</priority>
  </url>`).join('\n');

      return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;
    },

    generateRobots(domain = 'https://starjs.dev') {
      return `User-agent: *
Allow: /
Sitemap: ${domain}/sitemap.xml
`;
    }
  };
}

/**
 * 🔍 StarFastIndexPlugin: Build-time & Runtime Inverted Search Index
 */
function StarFastIndexPlugin(options = {}) {
  const rootDir = options.rootDir || process.cwd();
  const searchIndexFile = options.outputFile || 'search_index.json';

  return {
    name: 'star-plugin-fast-index',

    buildIndex(pages = []) {
      const docs = [];
      const index = {};
      const docLengths = {};
      const stopWords = new Set(['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with']);

      const tokenize = (text) => {
        if (!text) return [];
        return String(text).toLowerCase().replace(/[^\w\s\-]/g, ' ').split(/\s+/).filter(w => w.length >= 2 && !stopWords.has(w));
      };

      pages.forEach((page, idx) => {
        const id = page.id || `doc-${idx}`;
        docs.push({
          id,
          title: page.title,
          route: page.route || '/',
          category: page.category || 'General',
          content: page.content || ''
        });

        const tokens = [
          ...tokenize(page.title).map(t => ({ t, w: 3.0 })),
          ...tokenize(page.category).map(t => ({ t, w: 2.0 })),
          ...tokenize(page.content).map(t => ({ t, w: 1.0 }))
        ];
        docLengths[id] = tokens.length || 1;

        tokens.forEach(({ t, w }) => {
          if (!index[t]) index[t] = {};
          index[t][id] = (index[t][id] || 0) + w;
        });
      });

      return { docs, index, docLengths };
    }
  };
}

/**
 * 📱 StarPWAPlugin: Service Worker and Manifest Generator
 */
function StarPWAPlugin(options = {}) {
  const config = {
    name: options.name || 'Star.js App',
    shortName: options.shortName || 'StarApp',
    themeColor: options.themeColor || '#00f0ff',
    bgColor: options.bgColor || '#050711',
    display: options.display || 'standalone',
    startUrl: options.startUrl || '/'
  };

  return {
    name: 'star-plugin-pwa',

    generateManifest() {
      return JSON.stringify({
        name: config.name,
        short_name: config.shortName,
        start_url: config.startUrl,
        display: config.display,
        background_color: config.bgColor,
        theme_color: config.themeColor,
        icons: [
          { src: '/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icon-512.png', sizes: '512x512', type: 'image/png' }
        ]
      }, null, 2);
    },

    generateServiceWorker(precacheUrls = ['/', '/index.html', '/star.js', '/style.css']) {
      return `/**
 * 🌟 Star.js Disruption-Tolerant Service Worker
 * Powered by ODCS-2.0.0 Storage & Cache Strategy
 */
const CACHE_NAME = 'star-odcs-v1';
const PRECACHE = ${JSON.stringify(precacheUrls)};

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  // Stale-While-Revalidate with ODCS Offline Fallback
  e.respondWith(
    caches.match(e.request).then(cached => {
      const fetchPromise = fetch(e.request).then(networkRes => {
        if (networkRes && networkRes.status === 200 && networkRes.type === 'basic') {
          const resClone = networkRes.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, resClone));
        }
        return networkRes;
      }).catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
`;
    }
  };
}

// ============================================================================
// 2. VITE-LIKE LIGHTNING DEV SERVER
// ============================================================================

class StarViteServer {
  constructor(options = {}) {
    this.root = path.resolve(options.root || process.cwd());
    this.port = options.port || 3000;
    this.plugins = options.plugins || [
      StarSEOPlugin(),
      StarFastIndexPlugin({ rootDir: this.root }),
      StarPWAPlugin()
    ];
    this.clients = new Set(); // SSE / HMR client responses
    this.watcher = null;
    this.server = null;
  }

  start() {
    this.server = http.createServer((req, res) => this.handleRequest(req, res));
    this.server.listen(this.port, () => {
      console.log(`\n⚡ Star.js Vite-Like Dev Server running at:`);
      console.log(`   > Local:   http://localhost:${this.port}/`);
      console.log(`   > HMR:     Active (Instant Sub-10ms Hot Reload)`);
      console.log(`   > Plugins: ${this.plugins.map(p => p.name).join(', ')}`);
      console.log(`   > Root:    ${this.root}\n`);
    });

    this.startWatcher();
    return this;
  }

  handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    let pathname = decodeURIComponent(parsedUrl.pathname);

    // HMR Event Stream Endpoint
    if (pathname === '/@star/hmr') {
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*'
      });
      res.write('data: {"type":"connected"}\n\n');
      this.clients.add(res);
      req.on('close', () => this.clients.delete(res));
      return;
    }

    // Dynamic SEO endpoints
    if (pathname === '/sitemap.xml') {
      const seoPlugin = this.plugins.find(p => p.name === 'star-plugin-seo');
      if (seoPlugin) {
        res.writeHead(200, { 'Content-Type': 'application/xml; charset=utf-8' });
        res.end(seoPlugin.generateSitemap());
        return;
      }
    }

    if (pathname === '/robots.txt') {
      const seoPlugin = this.plugins.find(p => p.name === 'star-plugin-seo');
      if (seoPlugin) {
        res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end(seoPlugin.generateRobots());
        return;
      }
    }

    if (pathname === '/manifest.webmanifest' || pathname === '/manifest.json') {
      const pwaPlugin = this.plugins.find(p => p.name === 'star-plugin-pwa');
      if (pwaPlugin) {
        res.writeHead(200, { 'Content-Type': 'application/manifest+json' });
        res.end(pwaPlugin.generateManifest());
        return;
      }
    }

    if (pathname === '/sw.js') {
      const pwaPlugin = this.plugins.find(p => p.name === 'star-plugin-pwa');
      if (pwaPlugin) {
        res.writeHead(200, { 'Content-Type': 'application/javascript; charset=utf-8' });
        res.end(pwaPlugin.generateServiceWorker());
        return;
      }
    }

    // Default file resolution
    if (pathname === '/') pathname = '/index.html';
    let filePath = path.join(this.root, pathname);

    // If file does not exist, check fallback for SPA
    if (!fs.existsSync(filePath)) {
      filePath = path.join(this.root, 'index.html');
      if (!fs.existsSync(filePath)) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end(`404 Not Found: ${pathname}`);
        return;
      }
    }

    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      filePath = path.join(filePath, 'index.html');
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end(`500 Server Error: ${err.message}`);
        return;
      }

      let content = data;
      if (ext === '.html') {
        let htmlStr = data.toString('utf-8');

        // Apply HTML transformation plugins (like SEO Plugin)
        for (const plugin of this.plugins) {
          if (typeof plugin.renderHtml === 'function') {
            htmlStr = plugin.renderHtml(htmlStr);
          }
        }

        // Inject HMR Client Script
        const hmrScript = `
<!-- ⚡ Star.js Instant HMR Client -->
<script>
(() => {
  const es = new EventSource('/@star/hmr');
  es.onmessage = (e) => {
    try {
      const msg = JSON.parse(e.data);
      if (msg.type === 'reload') {
        console.log('[Star HMR] Reloading due to change in:', msg.file);
        location.reload();
      }
    } catch (err) {}
  };
  es.onerror = () => console.warn('[Star HMR] Connection lost, retrying...');
})();
</script>
`;
        if (htmlStr.includes('</body>')) {
          htmlStr = htmlStr.replace('</body>', `${hmrScript}</body>`);
        } else {
          htmlStr += hmrScript;
        }

        content = Buffer.from(htmlStr, 'utf-8');
      }

      res.writeHead(200, {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache'
      });
      res.end(content);
    });
  }

  startWatcher() {
    try {
      this.watcher = fs.watch(this.root, { recursive: true }, (eventType, filename) => {
        if (!filename) return;
        // Ignore git, node_modules, log files
        if (filename.includes('.git') || filename.includes('node_modules') || filename.endsWith('.log')) return;

        this.broadcastHMR({
          type: 'reload',
          file: filename,
          timestamp: Date.now()
        });
      });
    } catch (err) {
      console.warn('[Star Vite Watcher]:', err.message);
    }
  }

  broadcastHMR(msg) {
    const data = `data: ${JSON.stringify(msg)}\n\n`;
    for (const client of this.clients) {
      try {
        client.write(data);
      } catch (e) {
        this.clients.delete(client);
      }
    }
  }

  stop() {
    if (this.watcher) this.watcher.close();
    if (this.server) this.server.close();
  }
}

function createViteServer(options) {
  return new StarViteServer(options);
}

module.exports = {
  createViteServer,
  StarSEOPlugin,
  StarFastIndexPlugin,
  StarPWAPlugin
};

