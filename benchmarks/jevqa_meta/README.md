# Video quality from encoding metadata

Video quality judged from encoding metadata, against VMAF.

| | |
|---|---|
| Items | 1,936 |
| Licence | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| Source | [github.com/slhck/vmaf-v1-vs-v0](https://github.com/slhck/vmaf-v1-vs-v0) |
| Scoring | `pearson_r_expected_value` (computed by `scorer/scorer.py`) |
| Code licence | `scorer/` is Microsoft code under MIT (`scorer/LICENSE`) |

## Attribution

Per-encode VMAF results from vmaf-v1-vs-v0, Werner Robitza, github.com/slhck/vmaf-v1-vs-v0, MIT. Only the results table is used; no video content.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Built each request from the source's published results table (video codec, bitrate, frame size and frame rate) plus a short guide we wrote, with one 10-band quality-rating question. The answer is the source's measured quality score.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `scorer/scorer.py` | This benchmark's metrics, run by the runner after answers are collected | MIT (`scorer/LICENSE`), Microsoft |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
