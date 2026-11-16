"""Scorer for the decision_bench benchmark: computes accuracy (the headline metric) and related figures.

score(items, outputs) receives the benchmark's items and, for each answered item, its answers by repetition
(`reps[r][qid]`) and their readings (`read[r][qid]`: a choice option, true or false, or a score level), and
returns {"metrics": {...}, "per_item": {...}}.
"""
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations
import statistics
SUBSETS = ('medium', 'hard')
DETAIL_CHARS = 300

def _show(value) -> str:
    return ('yes' if value else 'no') if isinstance(value, bool) else str(value)

def score(items: list[dict], outputs: dict) -> dict:
    states: dict[str, list[float]] = {}
    per_item = {}
    for item in items:
        labels = item.get('labels') or {}
        right: list[bool] = []
        shown: list[str] = []
        for rep, seen in enumerate((outputs.get(item['id']) or {}).get('read') or []):
            if not isinstance(seen, dict):
                continue
            for qid in item.get('questions') or {}:
                pred = seen.get(qid)
                if pred is None:
                    continue
                gold = labels.get(qid)
                right.append(pred == gold)
                if rep == 0:
                    shown.append(f'{qid}: {_show(pred)}' + (f' (gold {_show(gold)})' if gold is not None else ''))
        if not right:
            continue
        states.setdefault(item['meta']['subset'], []).append(sum(right) / len(right))
        note = f'{sum(right)} of {len(right)} read answers right'
        text = '; '.join(shown)
        text = f'{text[:DETAIL_CHARS - len(note) - 3]} · {note}' if text else note
        per_item[item['id']] = {'detail': text[:DETAIL_CHARS]}
    if not states:
        return {'metrics': {}, 'per_item': {}}
    metrics = {f'state_macro_accuracy_{subset}': statistics.mean(states[subset]) if states.get(subset) else None for subset in SUBSETS}
    return {'metrics': metrics, 'per_item': per_item}
