"""Scorer for the rewardbench2 benchmark: computes accepted_accuracy (the headline metric) and related figures.

score(items, outputs) receives the benchmark's items and, for each answered item, its answers by repetition
(`reps[r][qid]`) and their readings (`read[r][qid]`: a choice option, true or false, or a score level), and
returns {"metrics": {...}, "per_item": {...}}.
"""
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations
DETAIL_CHARS = 300

def accepted(item: dict, qid: str) -> list | None:
    listed = ((item.get('meta') or {}).get('accepted') or {}).get(qid)
    if listed:
        return list(listed)
    label = (item.get('labels') or {}).get(qid)
    return None if label is None else [label]

def _show(value) -> str:
    return ('yes' if value else 'no') if isinstance(value, bool) else str(value)

def score(items: list[dict], outputs: dict) -> dict:
    right = graded = 0
    per_item = {}
    for item in items:
        output = outputs.get(item['id']) or {}
        reps, read = (output.get('reps') or [], output.get('read') or [])
        oks: list[bool] = []
        unread = not reps
        details, labels = ([], {})
        for qid in item.get('questions') or {}:
            gold = accepted(item, qid)
            labels[qid] = gold
            known = []
            for r in range(len(reps)):
                p = read[r].get(qid) if r < len(read) and isinstance(read[r], dict) else None
                if p is None:
                    unread = True
                    continue
                known.append(p)
                if gold is not None:
                    oks.append(p in gold)
            if known:
                shown = f" (accepted {', '.join(map(_show, gold))})" if gold else ''
                details.append(f'{qid}: {_show(known[0])}{shown}')
        right += sum(oks)
        graded += len(oks)
        per_item[item['id']] = {'ok': None if unread or not oks else all(oks), 'label': labels, 'detail': '; '.join(details)[:DETAIL_CHARS]}
    return {'metrics': {'accepted_accuracy': right / graded if graded else None, 'accepted_graded': graded}, 'per_item': per_item}
