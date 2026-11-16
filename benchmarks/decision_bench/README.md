# Decision Bench (medium and hard)

Typed questions about synthetic situations, with explicit rules and with judgement calls.

| | |
|---|---|
| Items | 160 |
| Licence | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (`data/LICENSE`) |
| Source | [huggingface.co/datasets/akhilaaa3/decision-bench](https://huggingface.co/datasets/akhilaaa3/decision-bench) |
| Scoring | `accuracy` (computed by `scorer/scorer.py`) |
| Code licence | `scorer/` is Microsoft code under MIT (`scorer/LICENSE`) |

## Attribution

Decision Bench, akhilaaa3, huggingface.co/datasets/akhilaaa3/decision-bench, Apache-2.0.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Used the medium and hard sets (160 situations) as published, one question per request. Answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `scorer/scorer.py` | This benchmark's metrics, run by the runner after answers are collected | MIT (`scorer/LICENSE`), Microsoft |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
