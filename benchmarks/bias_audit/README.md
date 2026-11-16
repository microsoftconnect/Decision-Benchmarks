# Counterfactual bias audit

Whether a decision changes when only a person's demographic descriptor changes.

| | |
|---|---|
| Items | 4,628 |
| Licence | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) for the audit's own items, and [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (`data/LICENSE-CC-BY-4.0`) for the BBQ-derived items |
| Source | [github.com/pawarbi/jev-bias-audit](https://github.com/pawarbi/jev-bias-audit) |
| Scoring | `swap_invariance` (computed by `scorer/scorer.py`) |
| Code licence | `scorer/` is Microsoft code under MIT (`scorer/LICENSE`) |

## Attribution

jev-bias-audit, Sandeep Pawar, github.com/pawarbi/jev-bias-audit, MIT. Items derived from BBQ (Parrish et al., 2022; github.com/nyu-mll/BBQ), CC BY 4.0.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Packaged the audit's scenarios (each in two demographic variants, two option orders and several wordings) and its BBQ-derived items as requests. Answers unchanged.

## Notes

- **Content note:** the scenarios describe fictional people with demographic descriptors (age, disability, gender identity, nationality, physical appearance, race and ethnicity, religion, socio-economic status, sexual orientation), some of them in stereotyped situations. They are there to test whether a decision changes when only the descriptor changes.
- Two licences apply to different items: each item's `meta.license` says which. Items derived from BBQ (`meta.category` set) are CC BY 4.0; the audit's own items are MIT.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [MIT](https://opensource.org/license/mit) (`data/LICENSE`) for the audit's own items, and [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (`data/LICENSE-CC-BY-4.0`) for the BBQ-derived items |
| `data/LICENSE`, `data/LICENSE-CC-BY-4.0` | The data's licence terms | |
| `scorer/scorer.py` | This benchmark's metrics, run by the runner after answers are collected | MIT (`scorer/LICENSE`), Microsoft |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
