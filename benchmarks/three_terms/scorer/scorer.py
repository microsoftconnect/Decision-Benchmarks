"""Scorer for the three_terms benchmark: computes accuracy (the headline metric) and related figures.

score(items, outputs) receives the benchmark's items and, for each answered item, its answers by repetition
(`reps[r][qid]`) and their readings (`read[r][qid]`: a choice option, true or false, or a score level), and
returns {"metrics": {...}, "per_item": {...}}.
"""
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations
import math
QID = 'closer'
DETAIL_CHARS = 300

def _number(value) -> bool:
    return isinstance(value, int | float) and (not isinstance(value, bool)) and math.isfinite(value)

def _mean(values: list) -> float | None:
    return sum(values) / len(values) if values else None

def reading(output: dict):
    reps = output.get('reps') or []
    for r, read in enumerate(output.get('read') or []):
        option = read.get(QID) if isinstance(read, dict) else None
        if option is None:
            continue
        answer = reps[r].get(QID) if r < len(reps) and isinstance(reps[r], dict) else None
        return (option, answer.get('probabilities') if isinstance(answer, dict) else None)
    return None

def score(items: list[dict], outputs: dict) -> dict:
    answered = []
    for item in items:
        got = reading(outputs.get(item['id']) or {})
        if got is None:
            continue
        pred, probs = got
        if isinstance(probs, dict) and probs:
            p = {k: float(probs[k]) if _number(probs.get(k)) else 0.0 for k in ('a', 'b')}
        else:
            p = {k: float(pred == k) for k in ('a', 'b')}
        answered.append((item, pred, p, item['label_probs'][QID]))
    if not answered:
        return {'metrics': {}, 'per_item': {}}
    scored = [(item, pred) for item, pred, _, _ in answered if item['labels'][QID] is not None]
    weights = sum((item['meta']['agreement'] for item, _ in scored))
    right = sum((item['meta']['agreement'] * (pred == item['labels'][QID]) for item, pred in scored))
    metrics = {'rater_agreement_argmax': _mean([h.get(pred, 0.0) for _, pred, _, h in answered]), 'rater_agreement_dist': _mean([h['a'] * p['a'] + h['b'] * p['b'] for _, _, p, h in answered]), 'tvd_to_human_dist': _mean([abs(p['a'] - h['a']) for _, _, p, h in answered]), 'agreement_weighted_acc': right / weights if scored and weights else None, 'human_single_rater_ceiling': _mean([item['meta']['majority_share'] for item, _ in scored])}
    per_item = {}
    for item, pred, _, _ in answered:
        meta, gold = (item['meta'], item['labels'][QID])
        chose = {'a': meta['n_a'], 'b': meta['n_b']}.get(pred, 0)
        text = f'{QID}: {pred}' + (f' (gold {gold})' if gold is not None else '')
        text += f" · {chose} of {meta['n_resp']} raters chose {pred}"
        per_item[item['id']] = {'detail': text[:DETAIL_CHARS]}
    return {'metrics': metrics, 'per_item': per_item}
