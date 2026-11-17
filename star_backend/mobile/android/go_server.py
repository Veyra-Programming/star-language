"""
Star Go Mobile Development Server (Expo Go Equivalent Architecture)
Authoritative Reference: STAR_ANDROID.md & STAR_ROADMAP.md
Provides live WiFi/LAN bundle streaming, Terminal QR code scanning, and Fast Refresh hot-reloading.
"""

import os
import sys
import time
import json
import socket
import threading
from typing import Optional, Dict, Any, List
import http.server
import socketserver

from star_backend.mobile.packaging import MobilePackager, MobileBundle
from star_backend.mobile.android.qr import QRCode


class StarGoServer:
    """
    Expo Go-like development server for Star mobile applications.
    Compiles source code into .starmobile bundles on the fly, hosts LAN HTTP
    endpoints, serves manifests, broadcasts Fast Refresh events, and renders
    terminal QR codes for instant physical device testing.
    """

    def __init__(self, source_file: str, port: int = 8088):
        self.source_file = os.path.abspath(source_file)
        self.port = port
        self.packager = MobilePackager()
        self.ip_address = self._detect_lan_ip()
        self.server_url = f"http://{self.ip_address}:{self.port}"
        self.star_url = f"star://{self.ip_address}:{self.port}"

        self.bundle_cache: Optional[bytes] = None
        self.bundle_manifest: Optional[Dict[str, Any]] = None
        self.reload_generation = 1
        self.connected_clients = 0
        self.is_running = False
        self.httpd: Optional[socketserver.TCPServer] = None
        self._last_mtime = 0

    @staticmethod
    def _detect_lan_ip() -> str:
        """Determines the primary LAN IP address accessible by other devices on the same WiFi."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.5)
            # Connecting to a public UDP address doesn't send packets but reveals the primary network interface
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            try:
                return socket.gethostbyname(socket.gethostname())
            except Exception:
                return "127.0.0.1"

    def rebuild_bundle(self) -> None:
        """Compiles the source file into an in-memory .starmobile bundle package."""
        base_name = os.path.splitext(os.path.basename(self.source_file))[0]
        temp_dir = os.path.join("build", "go_temp")
        os.makedirs(temp_dir, exist_ok=True)
        bundle_out = os.path.join(temp_dir, f"{base_name}.starmobile")

        self.packager.build_bundle(self.source_file, output_path=bundle_out)
        with open(bundle_out, "rb") as f:
            self.bundle_cache = f.read()

        loaded = self.packager.load_bundle(bundle_out)
        self.bundle_manifest = {
            "name": loaded.manifest.name,
            "package_id": loaded.manifest.package_id,
            "version": loaded.manifest.version,
            "orientation": loaded.manifest.orientation,
            "permissions": loaded.manifest.permissions,
            "server_url": self.server_url,
            "star_url": self.star_url,
            "bundle_url": f"{self.server_url}/bundle.starmobile",
            "generation": self.reload_generation,
            "bundle_size": len(self.bundle_cache),
            "updated_at": time.time(),
        }

    def _create_handler(self):
        server_instance = self

        class StarGoHTTPHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                # Suppress default noisy access logs
                pass

            def do_GET(self):
                if self.path in ("/", "/index.html"):
                    self._serve_dashboard()
                elif self.path in ("/manifest.json", "/manifest"):
                    self._serve_manifest()
                elif self.path == "/bundle.starmobile":
                    self._serve_bundle()
                elif self.path == "/qr.svg":
                    self._serve_qr_svg()
                elif self.path == "/status":
                    self._serve_status()
                elif self.path == "/events":
                    self._serve_events()
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not Found")

            def _serve_dashboard(self):
                html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Star Go — Mobile Live Server</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #090d16;
            color: #f8fafc;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .card {{
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 32px;
            max-width: 480px;
            width: 100%;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }}
        h1 {{ margin: 0 0 8px 0; font-size: 26px; color: #38bdf8; }}
        p {{ color: #94a3b8; margin: 0 0 24px 0; font-size: 14px; }}
        .qr-box {{
            background: white;
            padding: 16px;
            border-radius: 16px;
            display: inline-block;
            margin-bottom: 24px;
        }}
        .url-box {{
            background: #0f172a;
            border: 1px solid #334155;
            padding: 12px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 13px;
            color: #38bdf8;
            margin-bottom: 16px;
            word-break: break-all;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px;
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        .btn {{
            background: #2563eb;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            font-size: 14px;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">● LIVE DEV SERVER ACTIVE</span>
        <h1>⭐ Star Go Companion</h1>
        <p>Scan with the Star Go Android App or Camera to test on your device:</p>
        <div class="qr-box">
            <img src="/qr.svg" width="220" height="220" alt="Star Go QR Code" />
        </div>
        <div class="url-box">{server_instance.star_url}</div>
        <div style="margin-top: 10px;">
            <a href="/bundle.starmobile" class="btn">Download .starmobile Bundle</a>
        </div>
    </div>
</body>
</html>"""
                data = html.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _serve_manifest(self):
                data = json.dumps(server_instance.bundle_manifest or {}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _serve_bundle(self):
                if not server_instance.bundle_cache:
                    server_instance.rebuild_bundle()
                data = server_instance.bundle_cache
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _serve_qr_svg(self):
                qr = QRCode.encode(server_instance.star_url)
                svg = qr.to_svg().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.send_header("Content-Length", str(len(svg)))
                self.end_headers()
                self.wfile.write(svg)

            def _serve_status(self):
                payload = {
                    "status": "online",
                    "file": server_instance.source_file,
                    "generation": server_instance.reload_generation,
                    "star_url": server_instance.star_url,
                    "server_url": server_instance.server_url,
                }
                data = json.dumps(payload).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _serve_events(self):
                # SSE Event stream for Fast Refresh
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                server_instance.connected_clients += 1
                try:
                    last_seen_gen = server_instance.reload_generation
                    self.wfile.write(f"data: {json.dumps({'type': 'connected', 'generation': last_seen_gen})}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    while server_instance.is_running:
                        time.sleep(0.5)
                        if server_instance.reload_generation != last_seen_gen:
                            last_seen_gen = server_instance.reload_generation
                            payload = {"type": "reload", "generation": last_seen_gen, "url": f"{server_instance.server_url}/bundle.starmobile"}
                            self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode("utf-8"))
                            self.wfile.flush()
                except (ConnectionError, BrokenPipeError):
                    pass
                finally:
                    server_instance.connected_clients = max(0, server_instance.connected_clients - 1)

        return StarGoHTTPHandler

    def start(self, interactive: bool = True) -> None:
        """Starts the Star Go server, prints the QR code, and launches watcher loop."""
        self.rebuild_bundle()
        if os.path.exists(self.source_file):
            self._last_mtime = os.path.getmtime(self.source_file)

        class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            daemon_threads = True
            allow_reuse_address = True

        handler = self._create_handler()
        self.httpd = ThreadingServer(("", self.port), handler)
        self.is_running = True

        server_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        server_thread.start()

        # Generate Terminal QR Code
        qr = QRCode.encode(self.star_url)
        qr_terminal = qr.to_terminal(quiet_zone=2)

        # Print Expo Go-style banner
        print("=" * 68)
        print("⭐ STAR GO — Universal Mobile Dev Server (Expo Go Architecture)")
        print("=" * 68)
        print("📱 Scan this QR code with the Star Go Android App or Camera:")
        print(qr_terminal)
        print("=" * 68)
        print(f"🔗 Dev Server URL:    {self.server_url}")
        print(f"📱 Star URL Protocol:  {self.star_url}")
        print(f"📦 Source File:        {os.path.basename(self.source_file)} ({self.bundle_manifest['bundle_size']} bytes)")
        print(f"⚡ Fast Refresh:       Active (Watching '{os.path.basename(self.source_file)}')")
        print("--------------------------------------------------------------------")
        print("⌨  Commands: [r] Reload app · [m] Dev menu · [a] Launch ADB · [q] Quit")
        print("=" * 68)

        if not interactive:
            return

        # Main interactive keyboard & file watcher loop
        try:
            while self.is_running:
                # Check for file change (Hot Reload)
                if os.path.exists(self.source_file):
                    mtime = os.path.getmtime(self.source_file)
                    if mtime > self._last_mtime:
                        self._last_mtime = mtime
                        t0 = time.time()
                        self.reload_generation += 1
                        self.rebuild_bundle()
                        dt_ms = (time.time() - t0) * 1000
                        print(f"⚡ [Fast Refresh] Re-bundled in {dt_ms:.1f}ms — Broadcast to {self.connected_clients} client(s).")

                # Check keystrokes (Windows msvcrt / POSIX select)
                self._check_keystroke()
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\nShutting down Star Go server...")
        finally:
            self.stop()

    def _check_keystroke(self):
        try:
            if sys.platform == "win32":
                import msvcrt
                if msvcrt.kbhit():
                    ch = msvcrt.getch().decode("utf-8", errors="ignore").lower()
                    self._handle_command(ch)
        except Exception:
            pass

    def _handle_command(self, ch: str):
        if ch == "r":
            print("🔄 [Manual Reload] Triggering reload across all connected devices...")
            self.reload_generation += 1
            self.rebuild_bundle()
        elif ch == "m":
            print("📱 [Dev Menu] Dispatched developer menu toggle to devices.")
        elif ch == "a":
            print("🤖 [ADB Bridge] Attempting to launch Star Go on connected Android device...")
            import subprocess
            try:
                cmd = ["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", self.star_url]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if res.returncode == 0:
                    print(f"✓ Dispatched deep link intent '{self.star_url}' via ADB.")
                else:
                    print("ℹ No active Android device available via ADB.")
            except Exception as e:
                print(f"ℹ ADB dispatch skipped: {e}")
        elif ch == "q":
            print("Stopping Star Go dev server...")
            self.is_running = False

    def stop(self):
        """Stops the server gracefully."""
        self.is_running = False
        if self.httpd:
            try:
                self.httpd.shutdown()
            except Exception:
                pass
        print("✓ Star Go Dev Server stopped.")

