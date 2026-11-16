# Three Terms Task

Which of two nouns is closer in meaning to a third, against human consensus.

| | |
|---|---|
| Items | 2,555 |
| Licence | [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (`data/LICENSE`) |
| Source | [osf.io/at8cs](https://osf.io/at8cs) |
| Scoring | `accuracy` (computed by `scorer/scorer.py`) |
| Code licence | `scorer/` is Microsoft code under MIT (`scorer/LICENSE`) |

## Attribution

Three Terms Task (Borghesani, Armoza, Hebart, Bellec and Brambati, Scientific Data 2023; osf.io/at8cs), CC BY 4.0. Nouns from THINGS (Hebart et al., 2019).

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Wrote one multiple-choice question per word triplet (which word is closer in meaning to the anchor word?). The answer is the human raters' majority.

## Notes

- Only the public per-triplet summary (`data/Results_Summary_1322.csv`: counts of raters' choices per triplet) is included. The anonymised individual-subject data, which is gated, is not included, and uses related to that data are not covered by this release.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `scorer/scorer.py` | This benchmark's metrics, run by the runner after answers are collected | MIT (`scorer/LICENSE`), Microsoft |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
