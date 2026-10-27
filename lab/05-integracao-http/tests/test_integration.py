import json
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from api import EventStore, make_handler  # noqa: E402
from agent import classify, sync  # noqa: E402


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = EventStore(Path(self.temp.name) / "events.sqlite3")
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.store))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.close_server)
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def close_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_accept_and_review_with_idempotence(self):
        dataset = [
            {"id": "LAB-001", "label": "A", "category": "OK", "quantity": 1},
            {"id": "LAB-002", "label": "B", "category": "", "quantity": -1},
        ]
        outcomes = sync(dataset, self.url)
        self.assertEqual([x["decision"] for x in outcomes], ["accepted", "review"])
        sync(dataset, self.url)  # reenviar não duplica IDs
        with urlopen(self.url + "/events", timeout=2) as res:
            counts = json.load(res)
        self.assertEqual(counts["total_records"], 2)
        self.assertEqual(counts["decisions"], {"accepted": 1, "review": 1})

    def test_localhost_only_and_dry_run(self):
        self.assertEqual(classify({"id": "LAB-001", "label": "A", "category": "B", "quantity": 3})["decision"], "accepted")
        with self.assertRaises(ValueError):
            sync([], "https://external.example.com")
        sync([{"id": "LAB-004", "label": "C", "category": "D", "quantity": 1}], self.url, dry_run=True)
        self.assertEqual(self.store.summary()["total_records"], 0)

    def test_reject_unexpected_identifier(self):
        request = Request(
            self.url + "/events",
            data=json.dumps({"record_id": "REAL-001", "decision": "accepted", "reason": "test"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(HTTPError) as err:
            urlopen(request, timeout=2)
        self.assertEqual(err.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
