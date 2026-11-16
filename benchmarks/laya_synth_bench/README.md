# Jev vs Laya synthetic typed decisions

Several typed questions of different types about one text, in eight tasks.

| | |
|---|---|
| Items | 1,470 |
| Licence | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| Source | [github.com/harrymunro/jev-laya-benchmark](https://github.com/harrymunro/jev-laya-benchmark) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

Jev vs Laya synthetic typed-decision suite, Harry Munro, github.com/harrymunro/jev-laya-benchmark, MIT ("MIT for the code, data, and results").

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Built each request from the source's data fields and its question definitions, copied as written. Answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
