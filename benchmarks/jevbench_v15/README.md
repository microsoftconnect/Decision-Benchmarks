# JevBench-240

Typed questions on synthetic business cases in 12 domains.

| | |
|---|---|
| Items | 240 |
| Licence | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (`data/LICENSE`) |
| Source | [huggingface.co/datasets/JevBench/jevbench](https://huggingface.co/datasets/JevBench/jevbench) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

JevBench-240, Chen Feng (ML Lab, Queen's University Belfast), huggingface.co/datasets/JevBench/jevbench, Apache-2.0.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Used each of the 240 cases' main question set only, leaving out the source's follow-up variations. Answers unchanged.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
