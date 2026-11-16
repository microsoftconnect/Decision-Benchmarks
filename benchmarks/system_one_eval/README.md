# System One eval (60 typed tasks)

60 authored tasks: policy precedence, aggregation, joins, scheduling, access control, arithmetic.

| | |
|---|---|
| Items | 60 |
| Licence | [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (`data/LICENSE`) |
| Source | [huggingface.co/datasets/blazeofchi/system-one-eval](https://huggingface.co/datasets/blazeofchi/system-one-eval) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

system-one-eval, blazeofchi, huggingface.co/datasets/blazeofchi/system-one-eval, CC BY 4.0.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Packaged the 60 authored tasks in our request format. Answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
