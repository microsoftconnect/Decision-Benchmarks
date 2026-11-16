# Jev Frontier 100

100 authored reasoning items in 50 matched pairs.

| | |
|---|---|
| Items | 100 |
| Licence | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| Source | [github.com/softpudding/jev-frontier-100](https://github.com/softpudding/jev-frontier-100) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

Jev Frontier 100, JF100 contributors, github.com/softpudding/jev-frontier-100, MIT.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Packaged the 100 authored items in our request format. Text, questions and answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
