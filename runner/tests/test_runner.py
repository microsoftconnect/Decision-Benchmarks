"""Tests for dbrun. Run with: python -m unittest discover -s tests (from the runner folder)."""

from __future__ import annotations

import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from dbrun import benchmark, cli, client, grading

MANIFEST = {
    "id": "toy",
    "type": "basic",
    "scoring": {"primary": "accuracy", "slices": ["kind"]},
    "items": {"path": "items.jsonl", "count": 2},
    "run": {"request_mode": "item", "reps": 1},
}
ITEMS = [
    {"id": "a", "state": "A cracked mug.", "meta": {"kind": "damage"},
     "questions": {"damaged": {"type": "noul", "instructions": "Damaged?"},
                   "action": {"type": "choice", "instructions": "Next step?",
                              "criteria": {"refund": "Refund", "replace": "Replace"}}},
     "labels": {"damaged": True, "action": "refund"}},
    {"id": "b", "state": "Arrived fine.", "meta": {"kind": "ok"},
     "questions": {"urgency": {"type": "score", "instructions": "How urgent?", "criteria": ["Low", "High"]}},
     "labels": {"urgency": 0}},
]


def write_bench(folder: Path, manifest=MANIFEST, items=ITEMS, scorer: str | None = None) -> Path:
    (folder / "benchmark.json").write_text(json.dumps(manifest))
    (folder / "items.jsonl").write_text("\n".join(json.dumps(i) for i in items) + "\n")
    if scorer:
        (folder / "scorer.py").write_text(scorer)
    return folder


class Predict(unittest.TestCase):
    def test_noul_threshold(self):
        self.assertEqual(grading.predict("noul", {"noul": 0.5})[0], True)
        self.assertEqual(grading.predict("noul", {"noul": 0.49})[0], False)
        self.assertEqual(grading.predict("noul", {"noul": 0.6}, threshold=0.7)[0], False)

    def test_choice_ties_follow_request_order(self):
        ans = {"probabilities": {"b": 0.5, "a": 0.5}}
        self.assertEqual(grading.predict("choice", ans, offered=["a", "b"])[0], "a")
        self.assertEqual(grading.predict("choice", ans, offered=["b", "a"])[0], "b")

    def test_choice_field_does_not_override(self):
        ans = {"choice": "a", "probabilities": {"a": 0.2, "b": 0.8}}
        self.assertEqual(grading.predict("choice", ans, offered=["a", "b"])[0], "b")

    def test_score_level(self):
        self.assertEqual(grading.predict("score", {"probabilities": {"0": 0.3, "1": 0.7}}, offered=["0", "1"])[0], 1)

    def test_unreadable(self):
        self.assertIsNone(grading.predict("noul", {"noul": "x"}))
        self.assertIsNone(grading.predict("choice", {"probabilities": {}}))
        self.assertIsNone(grading.predict("choice", None))


class Grade(unittest.TestCase):
    def test_metrics_and_slices(self):
        records = [
            {"item": "a", "rep": 0, "outcome": "ok", "answers": {
                "damaged": {"type": "noul", "noul": 0.9},
                "action": {"type": "choice", "probabilities": {"refund": 0.3, "replace": 0.7}}}},
            {"item": "b", "rep": 0, "outcome": "ok", "answers": {
                "urgency": {"type": "score", "probabilities": {"0": 0.8, "1": 0.2}}}},
        ]
        metrics, per_item, outputs = grading.grade(MANIFEST, ITEMS, records)
        self.assertAlmostEqual(metrics["accuracy"], 2 / 3)
        self.assertEqual(metrics["graded"], 3)
        self.assertFalse(per_item["a"]["ok"])
        self.assertTrue(per_item["b"]["ok"])
        self.assertEqual(outputs["a"]["read"][0], {"damaged": True, "action": "replace"})
        table = grading.slices(MANIFEST, ITEMS, per_item)
        self.assertEqual(table["kind"]["ok"]["rate"], 1.0)

    def test_failed_request_leaves_item_ungraded(self):
        records = [{"item": "b", "rep": 0, "outcome": "error", "answers": None}]
        metrics, per_item, _ = grading.grade(MANIFEST, ITEMS, records)
        self.assertIsNone(per_item["b"]["ok"])
        self.assertIsNone(metrics["accuracy"])


class Requests(unittest.TestCase):
    def test_plan_modes(self):
        with tempfile.TemporaryDirectory() as tmp:
            bench = benchmark.load(write_bench(Path(tmp)))
            self.assertEqual(len(benchmark.plan(bench)), 2)
            bench.manifest["run"] = {"request_mode": "question", "reps": 2}
            plan = benchmark.plan(bench)
            self.assertEqual(len(plan), 6)
            self.assertEqual(plan[0][0], "a|damaged|0")

    def test_gzipped_items(self):
        import gzip
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            write_bench(folder, manifest={**MANIFEST, "items": {"path": "data/items.jsonl.gz", "count": 2}})
            (folder / "data").mkdir()
            (folder / "data" / "items.jsonl.gz").write_bytes(gzip.compress("\n".join(json.dumps(i) for i in ITEMS).encode() + b"\n"))
            bench = benchmark.load(folder)
            self.assertEqual([i["id"] for i in bench.items], ["a", "b"])

    def test_body_has_no_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            bench = benchmark.load(write_bench(Path(tmp)))
            body = benchmark.body(bench, ITEMS[0], ["damaged"], model="m")
            self.assertEqual(set(body), {"model", "state", "questions"})
            self.assertNotIn("labels", json.dumps(body))

    def test_images_inline(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "assets").mkdir()
            (folder / "assets" / "x.png").write_bytes(b"\x89PNG")
            item = {**ITEMS[1], "state": "image:x.png", "assets": {"x.png": "assets/x.png"}}
            bench = benchmark.load(write_bench(folder, items=[item]))
            body = benchmark.body(bench, item, ["urgency"])
            self.assertEqual(body["assets"]["x.png"]["format"], "png")


class FakeEndpoint(BaseHTTPRequestHandler):
    """Answers every question; rate-limits the first request it sees; records the headers it was sent."""
    seen: list[dict] = []
    limited = {"done": False}

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        FakeEndpoint.seen.append({"path": self.path, "auth": self.headers.get("Authorization"), "body": body})
        if not FakeEndpoint.limited["done"]:
            FakeEndpoint.limited["done"] = True
            return self._send(429, {"error": "rate limited"}, {"Retry-After": "0"})
        answers = {}
        for qid, q in body["questions"].items():
            if q["type"] == "noul":
                answers[qid] = {"type": "noul", "noul": 0.9}
            else:
                opts = list(q["criteria"]) if isinstance(q["criteria"], dict) else [str(i) for i in range(len(q["criteria"]))]
                answers[qid] = {"type": q["type"], "probabilities": {o: (0.9 if i == 0 else 0.1) for i, o in enumerate(opts)}}
        self._send(200, {"model": "fake", "answers": answers, "usage": {"input_tokens": 1, "output_tokens": 1}})

    def _send(self, status, payload, headers=None):
        data = json.dumps(payload).encode()
        self.send_response(status)
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


class EndToEnd(unittest.TestCase):
    def test_run_retries_and_scores(self):
        server = HTTPServer(("127.0.0.1", 0), FakeEndpoint)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        scorer = "def score(items, outputs):\n    return {'metrics': {'answered_items': len(outputs)}, 'per_item': {}}\n"
        try:
            with tempfile.TemporaryDirectory() as tmp:
                (Path(tmp) / "bench").mkdir()
                folder = write_bench(Path(tmp) / "bench",
                                     manifest={**MANIFEST, "scoring": {**MANIFEST["scoring"], "scorer": "scorer.py"}},
                                     scorer=scorer)
                out = Path(tmp) / "out"
                os.environ["DBRUN_TEST_KEY"] = "test-key"
                rc = cli.main(["run", str(folder), "--base-url", f"http://127.0.0.1:{server.server_port}",
                               "--api-key-env", "DBRUN_TEST_KEY", "--out", str(out), "--concurrency", "1"])
                self.assertEqual(rc, 0)
                result = json.loads((out / "result.json").read_text())
                self.assertEqual(result["coverage"]["answered"], 2)
                self.assertEqual(result["metrics"]["answered_items"], 2)
                self.assertAlmostEqual(result["primary"]["value"], 1.0)
                self.assertTrue(all(s["path"] == "/v1/systemone" for s in FakeEndpoint.seen))
                self.assertTrue(all(s["auth"] == "Bearer test-key" for s in FakeEndpoint.seen))
                self.assertNotIn("test-key", (out / "answers.jsonl").read_text())
                # resuming sends nothing new
                before = len(FakeEndpoint.seen)
                cli.main(["run", str(folder), "--base-url", f"http://127.0.0.1:{server.server_port}",
                          "--api-key-env", "DBRUN_TEST_KEY", "--out", str(out)])
                self.assertEqual(len(FakeEndpoint.seen), before)
        finally:
            server.shutdown()

    def test_key_header(self):
        c = client.Client("https://x", "k1")
        self.assertEqual(c._headers["Authorization"], "Bearer k1")
        c = client.Client("https://x", "k2", key_header="api-key")
        self.assertEqual(c._headers["api-key"], "k2")
        self.assertNotIn("Authorization", c._headers)

    def test_endpoint_url(self):
        self.assertEqual(client.endpoint_url("https://x/"), "https://x/v1/systemone")
        self.assertEqual(client.endpoint_url("https://x/v1/systemone"), "https://x/v1/systemone")


class ScorerIsolation(unittest.TestCase):
    def test_scorer_cannot_open_network_connections(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "scorer.py").write_text(
                "import socket\n"
                "def score(items, outputs):\n"
                "    socket.create_connection(('127.0.0.1', 9))\n"
            )
            with self.assertRaises(RuntimeError) as caught:
                grading.run_scorer(Path(tmp), "scorer.py", [], {})
            self.assertIn("network access is disabled", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
