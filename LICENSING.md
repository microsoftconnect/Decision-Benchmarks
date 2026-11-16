# Licensing

This repository keeps code and data apart, so each is clearly licensed:

| Path | Contents | Licence |
|---|---|---|
| `runner/` | The command-line runner | MIT (`LICENSE`), Microsoft |
| `benchmarks/<id>/scorer/` | A benchmark's metric code | MIT (`scorer/LICENSE`), Microsoft |
| `benchmarks/<id>/benchmark.json`, READMEs | Manifests and documentation | MIT (`LICENSE`), Microsoft |
| `benchmarks/<id>/data/` | A benchmark's items | Set by its source: see `data/LICENSE` and the table below |

| Benchmark | Title | Items | Licence of `data/` |
|---|---|--:|---|
| [`jevbench`](benchmarks/jevbench/) | JevBench (public set) | 231 | MIT |
| [`jf100`](benchmarks/jf100/) | Jev Frontier 100 | 100 | MIT |
| [`laya_synth_bench`](benchmarks/laya_synth_bench/) | Jev vs Laya synthetic typed decisions | 1,470 | MIT |
| [`tree_choice_cap`](benchmarks/tree_choice_cap/) | Tree choice (teacher-forced steps) | 180 | MIT |
| [`ood_calibration`](benchmarks/ood_calibration/) | Out-of-distribution calibration (support tickets) | 900 | MIT |
| [`healthbench_consensus`](benchmarks/healthbench_consensus/) | HealthBench consensus grades | 2,000 | MIT |
| [`jevqa_meta`](benchmarks/jevqa_meta/) | Video quality from encoding metadata | 1,936 | MIT |
| [`decision_bench`](benchmarks/decision_bench/) | Decision Bench (medium and hard) | 160 | Apache-2.0 |
| [`jevbench_v15`](benchmarks/jevbench_v15/) | JevBench-240 | 240 | Apache-2.0 |
| [`typed_ja_ru`](benchmarks/typed_ja_ru/) | Typed decisions in Japanese and Russian | 778 | Apache-2.0 |
| [`globalgroup`](benchmarks/globalgroup/) | GlobalGroup word-grouping games | 3,225 | Apache-2.0 |
| [`headline_ab`](benchmarks/headline_ab/) | Upworthy headline A/B tests | 10,000 | CC-BY-4.0 |
| [`three_terms`](benchmarks/three_terms/) | Three Terms Task | 2,555 | CC-BY-4.0 |
| [`system_one_eval`](benchmarks/system_one_eval/) | System One eval (60 typed tasks) | 60 | CC-BY-4.0 |
| [`bias_audit`](benchmarks/bias_audit/) | Counterfactual bias audit | 4,628 | MIT + CC-BY-4.0 |
| [`openjev_heldout`](benchmarks/openjev_heldout/) | Open-Jev held-out typed decisions | 9,479 | CC0-1.0 |
| [`rewardbench2`](benchmarks/rewardbench2/) | RewardBench 2 | 1,865 | ODC-BY-1.0 |
| [`belebele_xl`](benchmarks/belebele_xl/) | Belebele reading comprehension (26 languages) | 1,820 | CC-BY-SA-4.0 |

Share-alike: `belebele_xl` is CC BY-SA 4.0, and anything derived from it must be shared under the same licence.
