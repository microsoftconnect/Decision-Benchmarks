# Belebele reading comprehension (26 languages)

Reading comprehension: the same 70 questions in 26 languages.

| | |
|---|---|
| Items | 1,820 |
| Licence | [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (`data/LICENSE`) |
| Source | [huggingface.co/datasets/facebook/belebele](https://huggingface.co/datasets/facebook/belebele) |
| Scoring | `accuracy` (standard metric, computed by the runner) |
| Code licence | no benchmark-specific code |

## Attribution

Belebele (Bandarkar et al., 2024), Meta, huggingface.co/datasets/facebook/belebele, CC BY-SA 4.0; passages from FLORES-200 (Meta), CC BY-SA 4.0.

## What we changed

Microsoft adapted this benchmark to the Microsoft-Decision-1 request format (a `state` and typed `questions`, with the source's answers as `labels`). Selected the same 70 questions in 26 languages and asked each as a four-option question, with the instruction in English. Passages, questions and answers unchanged.

## Notes

- Share-alike: these items are an adaptation of CC BY-SA 4.0 material and are released under CC BY-SA 4.0. Anything you derive from them must also be shared under CC BY-SA 4.0.

## Folder contents

| Path | What it is | Licence |
|---|---|---|
| `data/items.jsonl.gz` | The items, one JSON object per line, gzip-compressed (format in the repository README) | [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (`data/LICENSE`) |
| `data/LICENSE` | The data's licence terms | |
| `benchmark.json` | How items are sent and scored (read by the runner) | MIT (repository `LICENSE`) |
| `README.md` | This card | MIT (repository `LICENSE`) |
