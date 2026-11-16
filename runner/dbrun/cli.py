"""Command line: plan, run and score a benchmark.

    python -m dbrun plan  benchmarks/<id>
    python -m dbrun run   benchmarks/<id> --base-url https://<endpoint> [--model <name>] [--out results/<id>]
    python -m dbrun score benchmarks/<id> [--out results/<id>]

`run` sends every request, appends each response to <out>/answers.jsonl as it arrives, and scores the run at the end.
Run it again to resume: requests already answered are skipped. The API key is read from the environment variable
named by --api-key-env (DECISION_API_KEY by default); it is never written to disk or printed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dbrun import benchmark, client, grading


def _out_dir(args, bench) -> Path:
    out = Path(args.out) if args.out else Path("results") / bench.id
    out.mkdir(parents=True, exist_ok=True)
    return out


def _load(args):
    bench = benchmark.load(args.benchmark, args.items)
    if args.limit:
        bench.items = bench.items[: args.limit]
    return bench


def _records(path: Path) -> dict[str, dict]:
    """The latest record for each request key."""
    out: dict[str, dict] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").split("\n"):
            if line.strip():
                rec = json.loads(line)
                out[rec["key"]] = rec
    return out


def cmd_plan(args) -> int:
    bench = _load(args)
    plan = benchmark.plan(bench)
    questions = sum(len(qids) for _, _, qids, _ in plan)
    print(json.dumps({"benchmark": bench.id, "items": len(bench.items), "requests": len(plan),
                      "questions": questions, "request_mode": bench.request_mode, "reps": bench.reps,
                      "primary": bench.manifest["scoring"]["primary"],
                      "scorer": bench.manifest["scoring"].get("scorer")}, indent=2))
    return 0


def cmd_run(args) -> int:
    bench = _load(args)
    env_var_name = args.env_var_name
    key = os.environ.get(env_var_name)
    if not key:
        print(f"Nothing found in the environment variable {env_var_name}: set it to your endpoint's key.", file=sys.stderr)
        return 2
    headers = dict(h.split(":", 1) for h in args.header or [])
    headers = {k.strip(): v.strip() for k, v in headers.items()}
    api = client.Client(args.base_url, key, headers, timeout_s=args.timeout, key_header=args.api_key_header)
    out = _out_dir(args, bench)
    answers_path = out / "answers.jsonl"
    done = {k for k, r in _records(answers_path).items() if r.get("outcome") == "ok"}
    todo = [p for p in benchmark.plan(bench) if p[0] not in done]
    print(f"{bench.id}: {len(todo)} requests to send ({len(done)} already answered)", file=sys.stderr)
    lock = threading.Lock()
    failures = 0

    def send(entry):
        req_key, item, qids, rep = entry
        result = api.send(benchmark.body(bench, item, qids, args.model))
        return {"key": req_key, "item": item["id"], "qids": qids, "rep": rep, **result}

    with answers_path.open("a", encoding="utf-8") as f, ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(send, entry) for entry in todo]
        for n, future in enumerate(as_completed(futures), 1):
            rec = future.result()
            with lock:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
            failures += rec["outcome"] != "ok"
            if n % 50 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)} sent, {failures} unanswered", file=sys.stderr)
    return cmd_score(args)


def cmd_score(args) -> int:
    bench = _load(args)
    out = _out_dir(args, bench)
    planned = benchmark.plan(bench)
    keys = {p[0] for p in planned}
    records = [r for k, r in _records(out / "answers.jsonl").items() if k in keys]
    result, per_item = grading.score(bench.folder, bench.manifest, bench.items, records, len(planned))
    (out / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (out / "per_item.jsonl").open("w", encoding="utf-8") as f:
        for item_id, verdict in per_item.items():
            f.write(json.dumps({"item": item_id, **verdict}, ensure_ascii=False) + "\n")
    p = result["primary"]
    cov = result["coverage"]
    print(f"{bench.id}: {p['name']} = {p['value']}  (answered {cov['answered']}/{cov['planned']} requests)")
    return 0


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < (3, 10):
        print("dbrun needs Python 3.10 or later (some benchmarks' scorers use its syntax).", file=sys.stderr)
        return 2
    ap = argparse.ArgumentParser(prog="dbrun", description="Run and score decision benchmarks.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan", "run", "score"):
        p = sub.add_parser(name)
        p.add_argument("benchmark", help="the benchmark's folder (with benchmark.json)")
        p.add_argument("--items", help="an items file to use instead of the folder's")
        p.add_argument("--limit", type=int, help="only the first N items (for a quick check)")
        if name != "plan":
            p.add_argument("--out", help="where answers and results go (default results/<id>)")
        if name == "run":
            p.add_argument("--base-url", required=True, help="the endpoint; /v1/systemone is added unless present")
            p.add_argument("--model", help="the model name to put in each request, if the endpoint needs one")
            p.add_argument("--api-key-env", dest="env_var_name", default="DECISION_API_KEY")
            p.add_argument("--api-key-header", default="Authorization",
                           help="header for the key: Authorization (sent as Bearer, the default) or another name, e.g. api-key")
            p.add_argument("--header", action="append", help="an extra header, 'Name: value' (repeatable)")
            p.add_argument("--concurrency", type=int, default=2)
            p.add_argument("--timeout", type=float, default=120.0, help="seconds per attempt")
    args = ap.parse_args(argv)
    return {"plan": cmd_plan, "run": cmd_run, "score": cmd_score}[args.cmd](args)
