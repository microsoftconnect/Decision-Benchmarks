# Upworthy headline A/B tests

Which of two headlines drew more clicks in a real A/B test.

| | |
|---|---|
| Items | 10,000 |
| Licence | [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (`data/LICENSE`); the headline pairs and question wording from jev-headline-bench are MIT (`data/LICENSE-MIT`) |
| Source | [osf.io/jd64p](https://osf.io/jd64p)<br>[github.com/Gaurav-Gosain/jev-headline-bench](https://github.com/Gaurav-Gosain/jev-headline-bench) |
| Scoring | `pair_accuracy` (computed by `scorer/scorer.py`) |
| Code licence | `scorer/` is Microsoft code under MIT (`scorer/LICENSE`) |

## Attribution

Upworthy Research Archive (J. Nathan Matias, Kevin Munger, Marianne Aubin Le Quere and Charles Ebersole, 2021; osf.io/jd64p), CC BY 4.0. Headline pairs and question wording from jev-headline-bench (Gaurav Gosain, github.com/Gaurav-Gosain/jev-headline-bench), MIT.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Asked each of 5,000 A/B tests twice, with the two headlines in both orders, using the source runner's question wording. The answer is the headline that actually won.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (`data/LICENSE`); the headline pairs and question wording from jev-headline-bench are MIT (`data/LICENSE-MIT`) |
| `data/LICENSE`, `data/LICENSE-MIT` | The data's licence terms | |
| `scorer/scorer.py` | This benchmark's metrics, run by the runner after answers are collected | MIT (`scorer/LICENSE`), Microsoft |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
