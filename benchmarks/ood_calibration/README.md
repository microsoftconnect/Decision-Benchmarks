# Out-of-distribution calibration (support tickets)

Calibration on out-of-distribution support tickets.

| | |
|---|---|
| Items | 900 |
| Licence | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| Source | [github.com/scienthoon/jev-ood-calibration](https://github.com/scienthoon/jev-ood-calibration) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

jev-ood-calibration, scienthoon, github.com/scienthoon/jev-ood-calibration; synthetic data CC0-1.0, code MIT.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Packaged the 900 generated support tickets in our request format. Answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
