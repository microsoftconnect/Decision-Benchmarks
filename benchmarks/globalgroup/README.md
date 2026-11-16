# GlobalGroup word-grouping games

Word-grouping puzzles in five languages and in English translation.

| | |
|---|---|
| Items | 3,225 |
| Licence | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (`data/LICENSE`); the request wording adapted from connections-eval is MIT (`data/LICENSE-MIT`) |
| Source | [github.com/cgsol/globalgroup](https://github.com/cgsol/globalgroup) |
| Scoring | `solve_rate` (computed by `scorer/scorer.py`) |
| Code licence | `scorer/` is Microsoft code under MIT (`scorer/LICENSE`) |

## Attribution

GlobalGroup (Guerra-Solano, Li and Li, EMNLP 2025), github.com/cgsol/globalgroup, Apache-2.0. Request wording after connections-eval (github.com/matsonj/eval-connections), MIT, Copyright (c) 2025 connections-eval.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Recast each word-grouping puzzle as rating questions (do these words belong together?), using the wording of a published MIT-licensed solver. Answers come from the source's groups.

## Notes

- **NYT data isolated and removed.** The GlobalGroup source repository also contains New York Times Connections puzzles (`all_nyt_grouping_game511.xlsx` and the `nyt-seq` / `nyt-shuf` game sets). None of that data is used: these items are built only from the native-speaker game files (English, Spanish, Chinese, Hindi and Arabic, and the English translations of the last four), and every word group in them was checked against the native-speaker grouping files.
- One group in the authors' own English groupings ("peak, peek, peke, pique") is identical to a New York Times Connections group, so the 5 English games that contain it (15 items) were removed.
- The request text names no New York Times product: the solver's opening sentence was reworded to "Word-grouping puzzle: the sixteen words form four hidden groups of four related words each."

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (`data/LICENSE`); the request wording adapted from connections-eval is MIT (`data/LICENSE-MIT`) |
| `data/LICENSE`, `data/LICENSE-MIT` | The data's licence terms | |
| `scorer/scorer.py` | This benchmark's metrics, run by the runner after answers are collected | MIT (`scorer/LICENSE`), Microsoft |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
