"""Scorer for the globalgroup benchmark: computes solve_rate (the headline metric) and related figures.

score(items, outputs) receives the benchmark's items and, for each answered item, its answers by repetition
(`reps[r][qid]`) and their readings (`read[r][qid]`: a choice option, true or false, or a score level), and
returns {"metrics": {...}, "per_item": {...}}.
"""
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations
import itertools
TOP = 2
DETAIL_CHARS = 300

def expected(probs, level) -> float:
    if isinstance(probs, dict) and probs:
        try:
            return sum((int(k) * float(v) for k, v in probs.items())) / TOP
        except (TypeError, ValueError):
            pass
    return (level or 0) / TOP

def auc(pos: list, neg: list) -> float | None:
    if not pos or not neg:
        return None
    wins = sum((1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg))
    return wins / (len(pos) * len(neg))

def partition(words: list, aff: dict) -> list:
    at = {w: i for i, w in enumerate(words)}
    m = [[0.0] * len(words) for _ in words]
    for pair, value in aff.items():
        a, b = (at[w] for w in pair)
        m[a][b] = m[b][a] = value

    def total(s: tuple) -> float:
        return sum((m[s[0]][s[1]], m[s[0]][s[2]], m[s[0]][s[3]], m[s[1]][s[2]], m[s[1]][s[3]], m[s[2]][s[3]]))
    remaining = list(range(len(words)))
    picked = []
    while len(remaining) > 4:
        best = max(itertools.combinations(remaining, 4), key=total)
        picked.append(frozenset((words[i] for i in best)))
        remaining = [i for i in remaining if i not in best]
    picked.append(frozenset((words[i] for i in remaining)))
    return picked

def reading(output: dict, qid: str):
    reps = output.get('reps') or []
    for r, read in enumerate(output.get('read') or []):
        level = read.get(qid) if isinstance(read, dict) else None
        if level is None:
            continue
        answer = reps[r].get(qid) if r < len(reps) and isinstance(reps[r], dict) else None
        return (level, answer.get('probabilities') if isinstance(answer, dict) else None)
    return None

def _mean(values: list) -> float | None:
    return sum(values) / len(values) if values else None

def score(items: list[dict], outputs: dict) -> dict:
    games: dict[str, dict] = {}
    aff: dict[str, dict] = {}
    setsc: dict[str, dict] = {}
    read_any = False
    for item in items:
        meta = item['meta']
        gid = meta['game_id']
        game = games.setdefault(gid, {'words': meta['words'], 'groups': meta['groups'], 'sets': None, 'items': []})
        game['items'].append(item)
        if meta['kind'] == 'set':
            game['sets'] = meta['sets']
        output = outputs.get(item['id']) or {}
        for qid in item['questions']:
            got = reading(output, qid)
            if got is None:
                continue
            read_any = True
            value = expected(got[1], got[0])
            if meta['kind'] == 'pair':
                word_a, word_b = meta['pairs'][int(qid[1:])]
                aff.setdefault(gid, {})[frozenset((word_a, word_b))] = value
            else:
                setsc.setdefault(gid, {})[qid] = value
    if not read_any:
        return {'metrics': {}, 'per_item': {}}
    pair_bin: list[bool] = []
    pair_auc: list[float | None] = []
    set_top1: list[bool] = []
    set_sep: list[bool] = []
    set_auc: list[float | None] = []
    blend_top1: list[bool] = []
    solved = groups_found = pair_complete = 0
    per_item = {}
    for gid, game in games.items():
        words, groups = (game['words'], [frozenset(g) for g in game['groups']])
        truth = {frozenset(p): TOP if any((p[0] in g and p[1] in g for g in groups)) else 0 for p in itertools.combinations(words, 2)}
        a = aff.get(gid, {})
        complete = len(a) == len(truth)
        if complete:
            pair_complete += 1
            pos = [v for k, v in a.items() if truth[k] == TOP]
            neg = [v for k, v in a.items() if truth[k] == 0]
            pair_bin.extend(((v >= 0.5) == (truth[k] == TOP) for k, v in a.items()))
            pair_auc.append(auc(pos, neg))
            found = sum((1 for s in partition(words, a) if s in groups))
            groups_found += found
            solved += found == 4
            told = f'pair-sum partition: {found} of 4 groups found' + (', solved' if found == 4 else '')
        else:
            told = f'unanswered: {len(a)} of {len(truth)} pair answers read'
        top_set = None
        ss = setsc.get(gid, {})
        if game['sets'] and len(ss) == len(game['sets']):
            sc = [(ss[f's{k}'], s['kind'] == 'true', s['words']) for k, s in enumerate(game['sets'])]
            pos = [v for v, t, _ in sc if t]
            neg = [v for v, t, _ in sc if not t]
            set_auc.append(auc(pos, neg))
            set_sep.append(min(pos) > max(neg))
            values = [v for v, _, _ in sc]
            top = max(range(len(sc)), key=values.__getitem__)
            set_top1.append(sc[top][1])
            top_set = f"top set s{top}: {('a real group' if sc[top][1] else 'a decoy')}"
            if complete:
                blend = [(sum((a.get(frozenset(p), 0.0) for p in itertools.combinations(ws, 2))) / 6 + v / 2, t) for v, t, ws in sc]
                blend_top1.append(max(blend, key=lambda x: x[0])[1])
        for item in game['items']:
            detail = told + (f' · {top_set}' if top_set and item['meta']['kind'] == 'set' else '')
            per_item[item['id']] = {'ok': found == 4 if complete else None, 'detail': detail[:DETAIL_CHARS]}
    n = len(games)
    return {'metrics': {'solve_rate': solved / n, 'solve_rate_answered': solved / pair_complete if pair_complete else None, 'groups_found_rate': groups_found / (4 * n), 'pair_binary_acc': _mean(pair_bin), 'pair_auc': _mean([x for x in pair_auc if x is not None]), 'set_top1_true': _mean(set_top1), 'set_perfect_separation': _mean(set_sep), 'set_auc': _mean([x for x in set_auc if x is not None]), 'blend_top1_true': _mean(blend_top1), 'games': n, 'games_pair_complete': pair_complete, 'games_set_complete': len(set_top1), 'games_solved': solved, 'groups_found': groups_found}, 'per_item': per_item}
