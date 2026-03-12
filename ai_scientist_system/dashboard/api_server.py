"""Minimal dashboard API exposing budget and leaderboard snapshots."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, Dict


class DashboardHandler(BaseHTTPRequestHandler):
    state_provider: Callable[[], Dict] = lambda: {}

    def _send_json(self, payload: Dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path == "/health":
            self._send_json({"status": "ok"})
            return
        if self.path == "/state":
            self._send_json(self.state_provider())
            return
        self._send_json({"error": "not found"}, status=404)


def run_dashboard(host: str, port: int, state_provider: Callable[[], Dict]) -> None:
    DashboardHandler.state_provider = state_provider
    server = HTTPServer((host, port), DashboardHandler)
    server.serve_forever()
