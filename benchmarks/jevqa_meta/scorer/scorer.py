"""Scorer for the jevqa_meta benchmark: computes pearson_r_expected_value (the headline metric) and related figures.

score(items, outputs) receives the benchmark's items and, for each answered item, its answers by repetition
(`reps[r][qid]`) and their readings (`read[r][qid]`: a choice option, true or false, or a score level), and
returns {"metrics": {...}, "per_item": {...}}.
"""
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations
import collections
import math
import statistics
LEVELS = 10
CENTRES = [5 + 10 * i for i in range(LEVELS)]
GROUPS = ('codec', 'resolution')
DETAIL_CHARS = 300

def expected(probs: dict) -> float:
    weighted = sum((float(probs.get(str(i), 0.0)) * c for i, c in enumerate(CENTRES)))
    return weighted / max(1e-09, sum((float(probs.get(str(i), 0.0)) for i in range(LEVELS))))

def pearson(xs: list, ys: list) -> float | None:
    n = len(xs)
    if n < 2:
        return None
    mx, my = (statistics.mean(xs), statistics.mean(ys))
    sx = math.sqrt(sum(((x - mx) ** 2 for x in xs)))
    sy = math.sqrt(sum(((y - my) ** 2 for y in ys)))
    return sum(((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))) / (sx * sy) if sx and sy else None

def ranks(values: list) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return out

def spearman(xs: list, ys: list) -> float | None:
    return pearson(ranks(xs), ranks(ys))

def _share(flags) -> float | None:
    flags = list(flags)
    return float(statistics.mean(flags)) if flags else None

def score(items: list[dict], outputs: dict) -> dict:
    pairs = []
    per_item = {}
    for item in items:
        qid = next(iter(item['questions']))
        gold = (item.get('labels') or {}).get(qid)
        output = outputs.get(item['id']) or {}
        reps, read = (output.get('reps') or [], output.get('read') or [])
        for r, answers in enumerate(reps):
            band = read[r].get(qid) if r < len(read) and isinstance(read[r], dict) else None
            if band is None or gold is None:
                continue
            probs = ((answers or {}).get(qid) or {}).get('probabilities')
            try:
                value = expected(probs)
            except (AttributeError, TypeError, ValueError):
                continue
            vmaf = item['meta']['vmaf']
            pairs.append((value, vmaf, band, gold, item['meta']))
            if item['id'] not in per_item:
                text = f'{qid}: {band} (gold {gold}) · expected VMAF {value:.1f}, VMAF {vmaf:.1f}'
                per_item[item['id']] = {'detail': text[:DETAIL_CHARS]}
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    metrics: dict[str, float | int | None] = {'pearson_r_expected_value': pearson(xs, ys), 'spearman_rho_expected_value': spearman(xs, ys), 'rmse_expected_value': math.sqrt(statistics.mean(((a - b) ** 2 for a, b in zip(xs, ys, strict=True)))) if pairs else None, 'pearson_r_argmax_band': pearson([10 * p[2] + 5 for p in pairs], ys), 'band_within_one': _share((abs(p[2] - p[3]) <= 1 for p in pairs)), 'n_scored': len(pairs)}
    for key in GROUPS:
        groups = collections.defaultdict(list)
        for p in pairs:
            groups[p[4][key]].append(p)
        for value, members in sorted(groups.items()):
            metrics[f'pearson_r_{key}_{value}'] = pearson([p[0] for p in members], [p[1] for p in members])
            metrics[f'band_accuracy_{key}_{value}'] = _share((p[2] == p[3] for p in members))
    return {'metrics': metrics, 'per_item': per_item}
