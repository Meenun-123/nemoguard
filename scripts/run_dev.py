#!/usr/bin/env python3
"""
Dual-mode local development server for NemoGuard.
- Uses Uvicorn + FastAPI if installed.
- Gracefully falls back to Python standard library HTTP/SSE server if FastAPI is not yet installed.
"""
import sys
import os
import json
import uuid
import time
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from shared.config import settings
from ai.agent import NemoGuardAgent
from ai.model_client import MockModelClient

class StandaloneHandler(SimpleHTTPRequestHandler):
    """Zero-dependency HTTP and SSE server handler."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR / "apps" / "web"), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/v1/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = {
                "status": "healthy",
                "execution_mode": settings.ai_execution_mode,
                "model_id": settings.nvidia_model_id,
                "nebius_base_url": settings.nebius_base_url,
                "max_iterations": settings.max_agent_iterations
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        elif path.startswith("/api/v1/stream/"):
            task_id = path.split("/")[-1]
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            agent = NemoGuardAgent(model_client=MockModelClient())
            cached_req = getattr(self.server, "last_req", {
                "code": "def process(): pass",
                "task_description": "Default scan"
            })

            def on_event(evt):
                line = f"data: {json.dumps(evt.dict())}\n\n"
                try:
                    self.wfile.write(line.encode("utf-8"))
                    self.wfile.flush()
                except Exception:
                    pass

            agent.run(
                task_id=task_id,
                code=cached_req.get("code", ""),
                task_description=cached_req.get("task_description", ""),
                auto_verify=True,
                max_iterations=4,
                event_callback=on_event
            )
            return

        elif path == "/" or path == "":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/v1/analyze":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            req = json.loads(body)
            self.server.last_req = req # type: ignore
            task_id = f"task_{uuid.uuid4().hex[:8]}"

            self.send_response(202)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            resp = {
                "task_id": task_id,
                "status": "QUEUED",
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        self.send_error(404, "Endpoint not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()


def main():
    print("=" * 65)
    print("  NemoGuard: Autonomous Agentic Remediation Engine")
    print(f"  Mode: {settings.ai_execution_mode.upper()}")
    print(f"  NVIDIA Model: {settings.nvidia_model_id}")
    print(f"  URL: http://localhost:{settings.api_port}")
    print("=" * 65)

    try:
        import uvicorn
        import fastapi
        print("[*] Launching with FastAPI & Uvicorn engine...")
        uvicorn.run(
            "services.api.main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=True
        )
    except ImportError:
        print("[*] FastAPI/Uvicorn not installed yet.")
        print(f"[*] Starting built-in lightweight server on port {settings.api_port}...")
        httpd = HTTPServer((settings.api_host, settings.api_port), StandaloneHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()


if __name__ == "__main__":
    main()
