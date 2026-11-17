"""
Star Mobile Hardware Test Session Recorder
Authoritative Reference: STAR_HARDWARE.md (Section 18)
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from star_backend.mobile.hardware.device import MobileDevice
from star_backend.mobile.hardware.metrics import HardwarePerformanceMetrics
from star_backend.mobile.hardware.probes import ProbeResult


class HardwareSessionRecorder:
    """
    Records and serializes hardware test sessions, capability probes,
    gesture traces, and performance telemetry into diagnostic session bundles.
    """
    def __init__(self, device: MobileDevice, session_dir: Optional[str] = None):
        self.device = device
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        self.session_dir = session_dir or os.path.join("build", "hardware", f"session_{timestamp}_{device.platform.value}")
        os.makedirs(self.session_dir, exist_ok=True)
        self.events: List[Dict[str, Any]] = []
        self.gestures: List[Dict[str, Any]] = []
        self.probes: List[ProbeResult] = []
        self.metrics: Optional[HardwarePerformanceMetrics] = None

    def record_event(self, event_type: str, data: Dict[str, Any]) -> None:
        self.events.append({
            "timestamp": time.time(),
            "type": event_type,
            "data": data
        })

    def record_gesture(self, gesture_name: str, data: Dict[str, Any]) -> None:
        self.gestures.append({
            "timestamp": time.time(),
            "name": gesture_name,
            "data": data
        })

    def record_probes(self, probes: List[ProbeResult]) -> None:
        self.probes.extend(probes)

    def record_metrics(self, metrics: HardwarePerformanceMetrics) -> None:
        self.metrics = metrics

    def finalize(self) -> str:
        # 1. device.json
        with open(os.path.join(self.session_dir, "device.json"), "w", encoding="utf-8") as f:
            json.dump(self.device.to_dict(), f, indent=2)

        # 2. metrics.json
        if self.metrics:
            with open(os.path.join(self.session_dir, "metrics.json"), "w", encoding="utf-8") as f:
                json.dump(self.metrics.to_dict(), f, indent=2)

        # 3. probes.json
        with open(os.path.join(self.session_dir, "probes.json"), "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.probes], f, indent=2)

        # 4. events.json & gestures.json
        with open(os.path.join(self.session_dir, "events.json"), "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2)

        with open(os.path.join(self.session_dir, "gestures.json"), "w", encoding="utf-8") as f:
            json.dump(self.gestures, f, indent=2)

        # 5. report.html
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Star Hardware Verification Report — {self.device.model}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 32px; }}
        h1 {{ color: #38bdf8; font-size: 24px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th, td {{ padding: 12px; border-bottom: 1px solid #334155; text-align: left; }}
        th {{ background: #1e293b; color: #94a3b8; }}
        .badge-pass {{ background: #059669; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>⭐ Star Mobile Hardware Verification Report</h1>
    <p>Device: <strong>{self.device.model}</strong> ({self.device.platform.value.upper()}) | OS: {self.device.os_version}</p>
    <table>
        <tr><th>Capability</th><th>Status</th><th>Latency</th></tr>
        {"".join(f"<tr><td>{p.capability}</td><td><span class='badge-pass'>{p.status.value}</span></td><td>{p.latency_ms:.2f}ms</td></tr>" for p in self.probes)}
    </table>
</body>
</html>"""
        with open(os.path.join(self.session_dir, "report.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

        return self.session_dir
