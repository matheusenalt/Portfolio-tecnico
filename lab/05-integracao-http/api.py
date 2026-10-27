#!/usr/bin/env python3
"""Servidor local de integração para eventos fictícios (não usar em produção)."""

import argparse
import json
import sqlite3
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ALLOWED_DECISIONS = {"accepted", "review"}


class EventStore:
    """Persistência SQLite do laboratório, com chave única para idempotência."""

    def __init__(self, database: Path):
        self.database = database
        self.lock = threading.Lock()
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.database) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    record_id TEXT PRIMARY KEY,
                    decision TEXT NOT NULL CHECK(decision IN ('accepted', 'review')),
                    reason TEXT NOT NULL,
                    received_at TEXT NOT NULL
                )
            """)

    def upsert(self, payload: dict):
        if not isinstance(payload, dict):
            raise ValueError("JSON precisa ser um objeto")
        record_id = payload.get("record_id")
        decision = payload.get("decision")
        reason = payload.get("reason")
        if not isinstance(record_id, str) or not (1 <= len(record_id) <= 40):
            raise ValueError("record_id inválido")
        if not record_id.startswith("LAB-") or not record_id[4:].isalnum():
            raise ValueError("O laboratório aceita somente IDs sintéticos LAB-*")
        if decision not in ALLOWED_DECISIONS:
            raise ValueError("decision deve ser accepted ou review")
        if not isinstance(reason, str) or len(reason) > 120:
            raise ValueError("reason inválido")
        with self.lock, sqlite3.connect(self.database) as db:
            db.execute("""
                INSERT INTO events (record_id, decision, reason, received_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(record_id) DO UPDATE SET
                    decision=excluded.decision,
                    reason=excluded.reason,
                    received_at=excluded.received_at
            """, (record_id, decision, reason, datetime.now(timezone.utc).isoformat()))

    def summary(self):
        with self.lock, sqlite3.connect(self.database) as db:
            rows = db.execute("SELECT decision, COUNT(*) FROM events GROUP BY decision").fetchall()
        counts = {"accepted": 0, "review": 0}
        counts.update(dict(rows))
        return {"total_records": sum(counts.values()), "decisions": counts}


def make_handler(store: EventStore):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, payload):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/health":
                return self.reply(200, {"status": "ok"})
            if path == "/events":
                return self.reply(200, store.summary())
            return self.reply(404, {"error": "not_found"})

        def do_POST(self):
            if urlsplit(self.path).path != "/events":
                return self.reply(404, {"error": "not_found"})
            if self.headers.get_content_type() != "application/json":
                return self.reply(415, {"error": "content_type"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not (1 <= length <= 4096):
                    raise ValueError("tamanho inválido")
                payload = json.loads(self.rfile.read(length))
                store.upsert(payload)
            except (ValueError, json.JSONDecodeError, TypeError):
                return self.reply(400, {"error": "invalid_event"})
            return self.reply(200, {"status": "recorded"})

    return Handler


def main():
    parser = argparse.ArgumentParser(description="API de integração local sintética")
    parser.add_argument("--database", type=Path, default=Path("data/events.sqlite3"))
    parser.add_argument("--port", type=int, default=8091)
    args = parser.parse_args()
    store = EventStore(args.database)
    with ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(store)) as server:
        print(f"API local em http://127.0.0.1:{server.server_port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
