"""Scorer for the tree_choice_cap benchmark: computes method_accuracy (the headline metric) and related figures.

score(items, outputs) receives the benchmark's items and, for each answered item, its answers by repetition
(`reps[r][qid]`) and their readings (`read[r][qid]`: a choice option, true or false, or a score level), and
returns {"metrics": {...}, "per_item": {...}}.
"""
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations
METHODS = (('tree', ('tree_l1', 'tree_l2', 'tree_l3')), ('flat', ('flat_bucket', 'flat_leaf')), ('truncate', ('truncate',)))
GROUPS = (('all', lambda m: True), ('tail', lambda m: not m['in_truncate']), ('injection', lambda m: m['trap']))
DETAIL_CHARS = 300

def walk(steps: dict, qids: tuple) -> bool | None:
    values = [steps.get(q) for q in qids]
    if any((v is False for v in values)):
        return False
    return None if any((v is None for v in values)) else True

def _rate(values: list[bool]) -> float | None:
    return sum(values) / len(values) if values else None

def score(items: list[dict], outputs: dict) -> dict:
    counted: dict[tuple[str, str], list[bool]] = {}
    per_item = {}
    read_any = False
    for item in items:
        labels = item.get('labels') or {}
        steps: dict[str, bool] = {}
        for seen in (outputs.get(item['id']) or {}).get('read') or []:
            if not isinstance(seen, dict):
                continue
            for qid in item['questions']:
                if qid in steps:
                    continue
                pred = seen.get(qid)
                if pred is not None:
                    gold = labels.get(qid)
                    steps[qid] = str(pred) == gold if gold is not None else False
        if not steps:
            continue
        read_any = True
        shown = []
        for method, qids in METHODS:
            verdict = walk(steps, qids)
            if verdict is None:
                shown.append(f'{method} unread')
                continue
            for group, member in GROUPS:
                if member(item['meta']):
                    counted.setdefault((method, group), []).append(verdict)
            wrong = next((q for q in qids if steps.get(q) is False), None)
            shown.append(f'{method} right' if verdict else f'{method} wrong ({wrong})')
        per_item[item['id']] = {'detail': ' · '.join(shown)[:DETAIL_CHARS]}
    if not read_any:
        return {'metrics': {}, 'per_item': {}}
    rates = {method: _rate(counted.get((method, 'all'), [])) for method, _ in METHODS}
    right = [sum(counted[method, 'all']) for method, _ in METHODS if counted.get((method, 'all'))]
    metrics: dict[str, float | None] = {'method_accuracy': sum(right) / (len(METHODS) * len(items)) if right else None}
    for method, _ in METHODS:
        metrics[f'method_accuracy_{method}'] = rates[method]
    for method, _ in METHODS:
        for group, _ in GROUPS[1:]:
            metrics[f'method_accuracy_{method}_{group}'] = _rate(counted.get((method, group), []))
    return {'metrics': metrics, 'per_item': per_item}
