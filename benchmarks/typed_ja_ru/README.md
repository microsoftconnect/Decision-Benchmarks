# Typed decisions in Japanese and Russian

Typed workflow decisions translated into Japanese and Russian.

| | |
|---|---|
| Items | 778 |
| Licence | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (`data/LICENSE`) |
| Source | [huggingface.co/datasets/GeneLab/typed-decisions-ja](https://huggingface.co/datasets/GeneLab/typed-decisions-ja)<br>[huggingface.co/datasets/yyhlm/typed-decisions-ru](https://huggingface.co/datasets/yyhlm/typed-decisions-ru) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

typed-decisions-ja (hiroki-abe-58, huggingface.co/datasets/GeneLab/typed-decisions-ja) and typed-decisions-ru (huggingface.co/datasets/yyhlm/typed-decisions-ru), both Apache-2.0; machine translations of LocalLLaMA/typed-decisions (Apache-2.0).

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Combined the Japanese and Russian translations (778 cases), sent as published. Answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
