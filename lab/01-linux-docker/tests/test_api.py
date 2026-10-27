"""Testes reais da API usando servidor local em porta efêmera."""

import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from server import Handler  # noqa: E402


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_health(self):
        with urlopen(self.base_url + "/health", timeout=2) as res:
            self.assertEqual(res.status, 200)
            self.assertEqual(json.load(res)["status"], "ok")
            self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")

    def test_status(self):
        with urlopen(self.base_url + "/api/status", timeout=2) as res:
            data = json.load(res)
            self.assertEqual(data["status"], "operational")
            self.assertGreaterEqual(data["uptime_seconds"], 0)
            self.assertIn("checked_at_utc", data)

    def test_missing_route_returns_404(self):
        with self.assertRaises(HTTPError) as err:
            urlopen(self.base_url + "/rota-inexistente", timeout=2)
        self.assertEqual(err.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
