"""Loading a benchmark folder and planning the requests its items send.

A benchmark folder holds `benchmark.json` (the manifest), `items.jsonl` (one item per line), optionally `scorer.py`
(metrics beyond the standard ones) and, for image benchmarks, `assets/`. Each item is already a System One request:
a `state` and typed `questions`, with the right answers in `labels`.
"""

from __future__ import annotations

import base64
import gzip
import json
from dataclasses import dataclass
from pathlib import Path

IMAGE_FORMATS = {".png": "png", ".jpg": "jpeg", ".jpeg": "jpeg"}


@dataclass
class Benchmark:
    folder: Path
    manifest: dict
    items: list[dict]

    @property
    def id(self) -> str:
        return self.manifest["id"]

    @property
    def request_mode(self) -> str:
        return self.manifest["run"]["request_mode"]

    @property
    def reps(self) -> int:
        return self.manifest["run"]["reps"]


def load(folder: str | Path, items_path: str | Path | None = None) -> Benchmark:
    """Reads a benchmark folder. `items_path` overrides the manifest's items file (for example, items you built from
    the original source)."""
    folder = Path(folder).resolve()
    manifest = json.loads((folder / "benchmark.json").read_text(encoding="utf-8"))
    if manifest.get("type") != "basic":
        raise ValueError(f"{manifest.get('id')}: only basic benchmarks are supported, not {manifest.get('type')!r}")
    if items_path is None:
        items_path = folder / ((manifest.get("items") or {}).get("path") or "items.jsonl")
    items_path = Path(items_path)
    raw = gzip.decompress(items_path.read_bytes()) if items_path.suffix == ".gz" else items_path.read_bytes()
    lines = raw.decode("utf-8").split("\n")
    items = [json.loads(line) for line in lines if line.strip()]
    return Benchmark(folder, manifest, items)


def request_groups(item: dict, request_mode: str) -> list[list[str]]:
    """The question ids of each request an item sends: all at once (`item`), one each (`question`), or the batches
    the item lists itself (`batches`)."""
    questions = item.get("questions") or {}
    if request_mode == "item":
        groups = [list(questions)]
    elif request_mode == "batches":
        groups = [list(batch) for batch in item.get("batches") or []]
    else:
        groups = [[q] for q in questions]
    return [g for g in groups if g]


def request_key(item_id: str, qids: list[str], rep: int) -> str:
    """Names one request within a run, so a run can be resumed."""
    return f"{item_id}|{'+'.join(qids)}|{rep}"


def plan(bench: Benchmark) -> list[tuple[str, dict, list[str], int]]:
    """(key, item, question ids, rep) for every request the benchmark sends, in order."""
    out = []
    for item in bench.items:
        for qids in request_groups(item, bench.request_mode):
            for rep in range(bench.reps):
                out.append((request_key(item["id"], qids, rep), item, qids, rep))
    return out


def body(bench: Benchmark, item: dict, qids: list[str], model: str | None = None) -> dict:
    """The System One request body for some of an item's questions, with the item's images inline."""
    questions = item.get("questions") or {}
    out: dict = {}
    if model:
        out["model"] = model
    out["state"] = item.get("state", "")
    out["questions"] = {q: questions[q] for q in qids}
    assets = item.get("assets") or {}
    if assets:
        out["assets"] = {}
        for ref, rel in assets.items():
            path = bench.folder / rel
            fmt = IMAGE_FORMATS.get(path.suffix.lower())
            if fmt is None:
                raise ValueError(f"{item['id']}: unsupported image type {path.suffix!r} for {ref!r}")
            data = base64.b64encode(path.read_bytes()).decode("ascii")
            out["assets"][ref] = {"type": "image", "format": fmt, "data_base64": data}
    return out
