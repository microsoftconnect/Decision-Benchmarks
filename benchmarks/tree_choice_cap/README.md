# Tree choice (teacher-forced steps)

Picking the right leaf from a 320-leaf incident catalogue, step by step.

| | |
|---|---|
| Items | 180 |
| Licence | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| Source | [huggingface.co/datasets/reachjalil/jev-tree-choice-cap](https://huggingface.co/datasets/reachjalil/jev-tree-choice-cap) |
| Scoring | `method_accuracy` (computed by `scorer/scorer.py`) |
| Code licence | `scorer/` is Microsoft code under MIT (`scorer/LICENSE`) |

## Attribution

jev-tree-choice-cap, reachjalil, huggingface.co/datasets/reachjalil/jev-tree-choice-cap, MIT (licence stated on the dataset; no copyright line is published, so the publisher is credited).

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Split the source's step-by-step catalogue walk into one multiple-choice request per step (180 items). Answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `scorer/scorer.py` | This benchmark's metrics, run by the runner after answers are collected | MIT (`scorer/LICENSE`), Microsoft |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
