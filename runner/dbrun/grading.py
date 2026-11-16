"""Grading a run's answers: the standard metrics, slices, and a benchmark's own scorer.py.

Reading an answer
- Yes/no (`noul`): the answer is yes when its probability of yes reaches the threshold (0.5 unless the manifest's
  `scoring.noul_threshold` says otherwise).
- Choice and score: the most probable option. Exact ties go to the first in the order the request listed the options;
  options the request didn't list come after, in code-point order. A choice answer's own `choice` field doesn't
  override its probabilities, and a probability that isn't a finite number is ignored.
- An answer that is missing or can't be read is left out of every metric.

Standard metrics
- `accuracy`: right answers over answers read, pooled over every labelled question and repetition, plus
  `accuracy_by_type`.
- `ece`: expected calibration error of the chosen answer's probability, in 10 equal-width bins.
- `brier`: squared error of the full distribution against the label, averaged over the answers read.
- `rep_agreement` (benchmarks with more than one repetition): the share of questions answered the same way every time.

A benchmark's scorer.py runs in a separate Python process. It gets the items and, for each answered item, its answers
by repetition (`reps[r][qid]`) and the readings above (`read[r][qid]`), and returns `{"metrics": ..., "per_item": ...}`.
Its metrics are added beside the standard ones (replacing any of the same name) and its item verdicts replace the
standard ones. The manifest's `scoring.primary` names the headline metric.
"""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

LEVEL = re.compile(r"\s*[-+]?[0-9]+\s*")


def _number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def options(question: dict) -> list[str] | None:
    """A question's options in the order its request lists them: a choice question's criteria keys, or a score
    question's levels ("0", "1", ...)."""
    criteria = question.get("criteria")
    if question.get("type") == "choice" and isinstance(criteria, dict):
        return [str(k) for k in criteria]
    if question.get("type") == "score" and isinstance(criteria, list):
        return [str(i) for i in range(len(criteria))]
    return None


def predict(qtype: str, answer, threshold: float = 0.5, offered: list[str] | None = None):
    """(prediction, confidence, probabilities) in the labels' terms (a choice option, true or false, a score level's
    index), or None when the answer can't be read."""
    if not isinstance(answer, dict):
        return None
    if qtype == "noul":
        p = answer.get("noul")
        if not _number(p):
            probs = answer.get("probabilities")
            probs = probs if isinstance(probs, dict) else {}
            p = probs.get("true") if _number(probs.get("true")) else probs.get("yes")
        if not _number(p):
            return None
        p = float(p)
        yes = p >= threshold
        return yes, (p if yes else 1 - p), {"true": p, "false": 1 - p}
    raw = answer.get("probabilities")
    if not isinstance(raw, dict):
        return None
    probs = {str(k): float(v) for k, v in raw.items() if _number(v)}
    if not probs:
        return None
    order = [o for o in offered or () if o in probs]
    seen = set(order)
    order += sorted(k for k in probs if k not in seen)
    best = max(order, key=probs.__getitem__)
    if qtype == "score":
        return (int(best), probs[best], probs) if LEVEL.fullmatch(best) else None
    return best, probs[best], probs


def ece(pairs: list[tuple[float, bool]], bins: int = 10) -> float | None:
    if not pairs:
        return None
    buckets: list[list[tuple[float, bool]]] = [[] for _ in range(bins)]
    for conf, ok in pairs:
        buckets[min(bins - 1, int(conf * bins))].append((conf, ok))
    total = len(pairs)
    return sum(
        len(b) / total * abs(sum(c for c, _ in b) / len(b) - sum(o for _, o in b) / len(b)) for b in buckets if b
    )


def _rate(values: list[bool]) -> float | None:
    return sum(values) / len(values) if values else None


def _show(value) -> str:
    return ("yes" if value else "no") if isinstance(value, bool) else str(value)


def grade(manifest: dict, items: list[dict], records: list[dict]) -> tuple[dict, dict, dict]:
    """(metrics, per-item verdicts, scorer outputs) from a run's records, one per request:
    {item, rep, outcome, answers}."""
    threshold = manifest["scoring"].get("noul_threshold", 0.5)
    reps = manifest["run"]["reps"]
    by_item: dict[str, list[dict]] = defaultdict(lambda: [dict() for _ in range(reps)])
    failed_items: set[str] = set()
    for r in records:
        if r.get("outcome") == "ok" and r.get("answers") is not None:
            by_item[r["item"]][r["rep"]].update(r["answers"])
        else:
            failed_items.add(r["item"])
    correct: dict[str, list[bool]] = defaultdict(list)
    pairs, brier, agree = [], [], []
    per_item: dict[str, dict] = {}
    reads: dict[str, list[dict]] = {}
    for item in items:
        reps_answers = by_item.get(item["id"], [dict() for _ in range(reps)])
        labels = item.get("labels") or {}
        questions = item.get("questions") or {}
        read: list[dict] = [{} for _ in range(reps)]
        item_ok: list[bool] = []
        missing = False
        details = []
        for qid, q in questions.items():
            offered = options(q)
            preds = []
            for rep, answers in enumerate(reps_answers):
                pred = predict(q["type"], answers.get(qid), threshold, offered)
                preds.append(pred)
                read[rep][qid] = None if pred is None else pred[0]
                if pred is None:
                    missing = True
                    continue
                label = labels.get(qid)
                if label is None:
                    continue
                ok = pred[0] == label
                correct[q["type"]].append(ok)
                correct["all"].append(ok)
                item_ok.append(ok)
                pairs.append((pred[1], ok))
                if q["type"] == "noul":
                    brier.append((pred[2]["true"] - (1.0 if label else 0.0)) ** 2)
                else:
                    brier.append(sum((p - (1.0 if str(k) == str(label) else 0.0)) ** 2 for k, p in pred[2].items()))
            known = [p[0] for p in preds if p is not None]
            if reps > 1 and len(known) == reps:
                agree.append(len(set(map(str, known))) == 1)
            if known:
                gold = labels.get(qid)
                details.append(f"{qid}: {_show(known[0])}" + (f" (gold {_show(gold)})" if gold is not None else ""))
        if missing or (item["id"] in failed_items and not item_ok):
            verdict = None
        else:
            verdict = all(item_ok) if item_ok else None
        per_item[item["id"]] = {"ok": verdict, "detail": "; ".join(details)[:300]}
        reads[item["id"]] = read
    metrics = {
        "accuracy": _rate(correct["all"]),
        "accuracy_by_type": {t: _rate(v) for t, v in correct.items() if t != "all"},
        "ece": ece(pairs),
        "brier": sum(brier) / len(brier) if brier else None,
        "graded": len(correct["all"]),
        "items": len(items),
        "items_answered": sum(1 for i in items if per_item[i["id"]]["ok"] is not None),
    }
    if reps > 1:
        metrics["rep_agreement"] = _rate(agree)
    outputs = {item_id: {"reps": answers, "read": reads.get(item_id)} for item_id, answers in by_item.items()}
    return metrics, per_item, outputs


# The scorer runs in its own process (python -I: no site packages, no current-directory imports) with Python's socket
# functions disabled, reading the items and outputs from stdin and printing its result as JSON on stdout; anything the
# scorer prints goes to stderr.
_HOST = r"""
import importlib.util, json, os, socket, sys
def _no_network(*args, **kwargs):
    raise OSError("network access is disabled for benchmark scorers")
socket.socket = socket.create_connection = socket.getaddrinfo = socket.socketpair = _no_network
folder, scorer = sys.argv[1], sys.argv[2]
out = os.fdopen(os.dup(sys.stdout.fileno()), "w", encoding="utf-8")
sys.stdout = sys.stderr
payload = json.loads(sys.stdin.read())
spec = importlib.util.spec_from_file_location("benchmark_scorer", os.path.join(folder, scorer))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
if hasattr(module, "score"):
    result = module.score(payload["items"], payload["outputs"])
else:
    per_item = {}
    for item in payload["items"]:
        verdict = module.verdict(item, payload["outputs"].get(item["id"]))
        if verdict is not None:
            per_item[item["id"]] = verdict
    result = {"metrics": {}, "per_item": per_item}
out.write(json.dumps(result, ensure_ascii=False, default=str))
out.flush()
"""


def run_scorer(folder: Path, scorer: str, items: list[dict], outputs: dict, timeout_s: int = 600) -> dict:
    folder = Path(folder).resolve()
    payload = json.dumps({"items": items, "outputs": outputs}, ensure_ascii=False)
    proc = subprocess.run(
        [sys.executable, "-I", "-B", "-c", _HOST, str(folder), scorer],
        input=payload,
        capture_output=True,
        text=True,
        timeout=timeout_s,
        cwd=str(folder),
    )
    if proc.returncode != 0:
        raise RuntimeError(f"{scorer} failed: {proc.stderr[-1500:]}")
    return json.loads(proc.stdout)


def slices(manifest: dict, items: list[dict], per_item: dict) -> dict:
    """Item-level accuracy broken down by the manifest's `scoring.slices` (keys of each item's `meta`)."""
    out: dict[str, dict] = {}
    for key in manifest["scoring"].get("slices", []):
        table: dict[str, dict] = {}
        for item in items:
            value = (item.get("meta") or {}).get(key)
            if value is None:
                continue
            row = table.setdefault(str(value), {"n": 0, "graded": 0, "ok": 0})
            row["n"] += 1
            verdict = per_item.get(item["id"], {}).get("ok")
            if verdict is not None:
                row["graded"] += 1
                row["ok"] += int(bool(verdict))
        for row in table.values():
            row["rate"] = row["ok"] / row["graded"] if row["graded"] else None
        out[key] = dict(sorted(table.items(), key=lambda kv: -kv[1]["n"]))
    return out


def coverage(planned: int, records: list[dict]) -> dict:
    answered = sum(1 for r in records if r.get("outcome") == "ok")
    return {"planned": planned, "answered": answered, "unanswered": len(records) - answered,
            "not_run": planned - len(records), "rate": answered / planned if planned else None}


def score(folder: Path, manifest: dict, items: list[dict], records: list[dict], planned: int) -> tuple[dict, dict]:
    """(result, per-item verdicts) for a run: standard metrics, the scorer's metrics, slices and coverage."""
    metrics, per_item, outputs = grade(manifest, items, records)
    from_scorer: list[str] = []
    scorer = manifest["scoring"].get("scorer")
    if scorer:
        scored = run_scorer(folder, scorer, items, outputs)
        for name, value in (scored.get("metrics") or {}).items():
            metrics[name] = value
            from_scorer.append(name)
        for item_id, verdict in (scored.get("per_item") or {}).items():
            per_item[item_id] = {**per_item.get(item_id, {}), **verdict}
    primary = manifest["scoring"]["primary"]
    result = {
        "benchmark": manifest["id"],
        "primary": {"name": primary, "value": metrics.get(primary)},
        "metrics": metrics,
        "from_scorer": from_scorer,
        "slices": slices(manifest, items, per_item),
        "coverage": coverage(planned, records),
    }
    return result, per_item
