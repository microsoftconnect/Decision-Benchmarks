# JevBench (public set)

Typed decisions in 18 task families (choice, yes/no, score).

| | |
|---|---|
| Items | 231 |
| Licence | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| Source | [github.com/fstandhartinger/jevbench](https://github.com/fstandhartinger/jevbench) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

JevBench public items, Florian Standhartinger and contributors, github.com/fstandhartinger/jevbench, MIT.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Packaged the 231 public items in our request format. Text, questions and answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
