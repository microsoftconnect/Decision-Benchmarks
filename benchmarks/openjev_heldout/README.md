# Open-Jev held-out typed decisions

Typed decisions in games, simulated controls and workflows.

| | |
|---|---|
| Items | 9,479 |
| Licence | [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (`data/LICENSE`) |
| Source | [huggingface.co/datasets/OpenAGILab/Jev-dataset](https://huggingface.co/datasets/OpenAGILab/Jev-dataset) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

Open-Jev dataset, Open-Jev contributors (huggingface.co/datasets/OpenAGILab/Jev-dataset); generated records CC0-1.0 (credit given as a courtesy).

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Converted the source's text-formatted questions back into our structured request format (10,000 held-out items). Answers unchanged. Items with question descriptions of unverified origin would be left out.

## Notes

- The 521 `customer-control-v1` items were removed: their short question descriptions come from third-party documentation without a verified licence. 9,479 items remain.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
