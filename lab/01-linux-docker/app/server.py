"""API HTTP demonstrativa: apenas biblioteca padrão, sem dados de terceiros."""

import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from time import monotonic
from urllib.parse import urlsplit

STARTED = monotonic()


class Handler(BaseHTTPRequestHandler):
    server_version = "PortfolioDemo"
    sys_version = ""

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            return self.reply_json(200, {"status": "ok", "service": "infra-demo"})
        if path == "/api/status":
            return self.reply_json(
                200,
                {
                    "service": "infra-demo",
                    "status": "operational",
                    "uptime_seconds": int(monotonic() - STARTED),
                    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
                },
            )
        if path == "/":
            return self.reply_json(
                200,
                {"name": "Laboratorio de Infraestrutura", "routes": ["/health", "/api/status"]},
            )
        return self.reply_json(404, {"error": "not_found"})

    def reply_json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Logs técnicos sem registrar corpo ou credenciais (somente console local).
        super().log_message(format, *args)


def main():
    host = os.environ.get("APP_HOST", "127.0.0.1")
    port = int(os.environ.get("APP_PORT", "8000"))
    print(f"Iniciando API de laboratório em {host}:{port}", flush=True)
    with ThreadingHTTPServer((host, port), Handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
