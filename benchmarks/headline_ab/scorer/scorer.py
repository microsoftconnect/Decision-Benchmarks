"""Scorer for the headline_ab benchmark: computes pair_accuracy (the headline metric) and related figures.

score(items, outputs) receives the benchmark's items and, for each answered item, its answers by repetition
(`reps[r][qid]`) and their readings (`read[r][qid]`: a choice option, true or false, or a score level), and
returns {"metrics": {...}, "per_item": {...}}.
"""
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations
import math
import statistics
ORDERS = ('winner_first', 'loser_first')
BANDS = ('none', 'weak', 'clear')
CONFIDENT = (0.8, 1.01)
DETAIL_CHARS = 300

def _number(value) -> bool:
    return isinstance(value, int | float) and (not isinstance(value, bool)) and math.isfinite(value)

def probability(answer: dict, key: str) -> float:
    value = (answer.get('probabilities') or {}).get(key, 0.0)
    return float(value) if _number(value) else 0.0

def p_true(answer: dict) -> float | None:
    p = answer.get('noul')
    if not _number(p):
        probs = answer.get('probabilities')
        probs = probs if isinstance(probs, dict) else {}
        p = probs.get('true') if _number(probs.get('true')) else probs.get('yes')
    return float(p) if _number(p) else None

def _show(value) -> str:
    return ('yes' if value else 'no') if isinstance(value, bool) else str(value)

def _rate(values: list[bool]) -> float | None:
    return sum(values) / len(values) if values else None

def _mean(values: list):
    return statistics.mean(values) if values else None

def score(items: list[dict], outputs: dict) -> dict:
    meta_by_pair: dict[str, dict] = {}
    by_order: dict[tuple[str, str], dict] = {}
    studio_detail: dict[str, str] = {}
    for item in items:
        meta = item['meta']
        meta_by_pair[meta['pair_id']] = meta
        output = outputs.get(item['id']) or {}
        reps, reads = (output.get('reps') or [], output.get('read') or [])
        labels = item.get('labels') or {}
        details, record = ([], {})
        for qid in item['questions']:
            known = [seen.get(qid) for seen in reads if isinstance(seen, dict) and seen.get(qid) is not None]
            if known:
                gold = labels.get(qid)
                details.append(f'{qid}: {_show(known[0])}' + (f' (gold {_show(gold)})' if gold is not None else ''))
            first = reads[0].get(qid) if reads and isinstance(reads[0], dict) else None
            answer = reps[0].get(qid) if reps and isinstance(reps[0], dict) else None
            if first is None or not isinstance(answer, dict):
                continue
            if qid == 'pick':
                record['p_winner'] = probability(answer, labels.get(qid))
                record['p_a'] = probability(answer, 'a')
            elif qid in ('emotional', 'curiosity'):
                record[f'{qid}_a'] = p_true(answer)
        studio_detail[item['id']] = '; '.join(details)
        if 'p_winner' in record:
            by_order[meta['pair_id'], meta['order']] = record
    pairs = []
    for pid, meta in meta_by_pair.items():
        wf, lf = (by_order.get((pid, 'winner_first')), by_order.get((pid, 'loser_first')))
        if not wf or not lf:
            continue
        pw = (wf['p_winner'] + lf['p_winner']) / 2
        pair = {'pid': pid, 'pw': pw, 'ok': pw > 0.5, 'conf': max(pw, 1 - pw), 'pfirst': (wf['p_a'] + lf['p_a']) / 2, 'flip': (wf['p_winner'] > 0.5) != (lf['p_winner'] > 0.5), 'tie': wf['p_winner'] == 0.5 or lf['p_winner'] == 0.5, 'band': meta['band'], 'decisive': meta['decisive']}
        for q, name in (('emotional', 'emo'), ('curiosity', 'cur')):
            if wf.get(f'{q}_a') is not None and lf.get(f'{q}_a') is not None:
                pair[name] = (wf[f'{q}_a'] + (1 - lf[f'{q}_a'])) / 2
        pairs.append(pair)
    if not pairs:
        return {'metrics': {}, 'per_item': {}}
    emo = [p['emo'] for p in pairs if 'emo' in p]
    cur = [p['cur'] for p in pairs if 'cur' in p]
    confident = [p for p in pairs if CONFIDENT[0] <= p['conf'] < CONFIDENT[1]]
    metrics: dict[str, float | int | None] = {'pair_accuracy': _rate([p['ok'] for p in pairs]), 'pairs_scored': len(pairs), 'decisive_pair_accuracy': _rate([p['ok'] for p in pairs if p['decisive']])}
    for band in BANDS:
        metrics[f'pair_accuracy_{band}'] = _rate([p['ok'] for p in pairs if p['band'] == band])
    metrics['confident_pair_accuracy'] = _rate([p['ok'] for p in confident])
    metrics['confident_pairs'] = len(confident)
    metrics['order_flip_rate'] = _mean([p['flip'] for p in pairs])
    metrics['order_ties'] = sum((p['tie'] for p in pairs))
    metrics['first_slot_probability'] = _mean([p['pfirst'] for p in pairs])
    metrics['winner_judged_more_emotional_pct'] = 100 * statistics.mean((e > 0.5 for e in emo)) if emo else None
    metrics['winner_judged_more_withholding_pct'] = 100 * statistics.mean((c > 0.5 for c in cur)) if cur else None
    scored = {p['pid']: p for p in pairs}
    per_item = {}
    for item in items:
        pair = scored.get(item['meta']['pair_id'])
        if pair is None:
            continue
        text = studio_detail[item['id']] + (f" · pair {('right' if pair['ok'] else 'wrong')}: mean p(winner) {pair['pw']:.3f} over both orders" + (', which disagree' if pair['flip'] else ''))
        per_item[item['id']] = {'detail': text[:DETAIL_CHARS]}
    return {'metrics': metrics, 'per_item': per_item}
