# HealthBench consensus grades

Whether a health-conversation answer meets a physician-graded rubric criterion.

| | |
|---|---|
| Items | 2,000 |
| Licence | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| Source | [github.com/openai/simple-evals](https://github.com/openai/simple-evals) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

HealthBench (Arora et al., 2025, arXiv:2505.08775), OpenAI, github.com/openai/simple-evals, MIT.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Kept only the response–criterion pairs that every grading physician agreed on (2,000, balanced yes/no) and asked one yes/no question per pair: does the response meet the criterion? The physicians' grade is the answer.

## Notes

- **Content note:** the conversations are about health and medical topics. The items test whether a response meets a physician-written criterion; neither the items nor a model's answers to them are medical advice.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
