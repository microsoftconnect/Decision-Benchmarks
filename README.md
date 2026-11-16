# Decision Benchmarks

Decision models answer closed questions about an input and return a probability for each answer option, instead of
generating text. To measure them, we compiled 18 public benchmarks that we believe give a broad, reliable picture of
decision quality. Between them they cover classification, rule application, judging and preference, bias and calibration,
reasoning and multilingual decisions. Each has well-defined answers and an open licence. These benchmarks were created
and shared by researchers and developers across the open-source community, and we're grateful for their work. We
adapted each one to the request format used by Microsoft-Decision-1, and this repository adds a runner that sends them
to a model endpoint you choose and the scoring code that turns the answers into results (41,627 items in all).

Use it to reproduce published results, to evaluate your own deployment, or to compare models that accept the same
request format.

- [What's included](#whats-included)
- [Quick start](#quick-start)
- [Bring your own endpoint and key](#bring-your-own-endpoint-and-key)
- [Running benchmarks](#running-benchmarks)
- [How answers are scored](#how-answers-are-scored)
- [Using the data without the runner](#using-the-data-without-the-runner)
- [Repository layout](#repository-layout)
- [Licensing](#licensing)
- [Responsible use](#responsible-use)

## What's included

| Benchmark | What it tests | Items | Primary metric | Data licence |
|---|---|--:|---|---|
| [`jevbench`](benchmarks/jevbench/) | Typed decisions in 18 task families (choice, yes/no, score) | 231 | `accuracy` | MIT |
| [`jf100`](benchmarks/jf100/) | 100 authored reasoning items in 50 matched pairs | 100 | `accuracy` | MIT |
| [`laya_synth_bench`](benchmarks/laya_synth_bench/) | Several typed questions of different types about one text, in eight tasks | 1,470 | `accuracy` | MIT |
| [`tree_choice_cap`](benchmarks/tree_choice_cap/) | Picking the right leaf from a 320-leaf incident catalogue, step by step | 180 | `method_accuracy` | MIT |
| [`ood_calibration`](benchmarks/ood_calibration/) | Calibration on out-of-distribution support tickets | 900 | `accuracy` | MIT |
| [`healthbench_consensus`](benchmarks/healthbench_consensus/) | Whether a health-conversation answer meets a physician-graded rubric criterion | 2,000 | `accuracy` | MIT |
| [`jevqa_meta`](benchmarks/jevqa_meta/) | Video quality judged from encoding metadata, against VMAF | 1,936 | `pearson_r_expected_value` | MIT |
| [`decision_bench`](benchmarks/decision_bench/) | Typed questions about synthetic situations, with explicit rules and with judgement calls | 160 | `accuracy` | Apache-2.0 |
| [`jevbench_v15`](benchmarks/jevbench_v15/) | Typed questions on synthetic business cases in 12 domains | 240 | `accuracy` | Apache-2.0 |
| [`typed_ja_ru`](benchmarks/typed_ja_ru/) | Typed workflow decisions translated into Japanese and Russian | 778 | `accuracy` | Apache-2.0 |
| [`globalgroup`](benchmarks/globalgroup/) | Word-grouping puzzles in five languages and in English translation | 3,225 | `solve_rate` | Apache-2.0 |
| [`headline_ab`](benchmarks/headline_ab/) | Which of two headlines drew more clicks in a real A/B test | 10,000 | `pair_accuracy` | CC-BY-4.0 |
| [`three_terms`](benchmarks/three_terms/) | Which of two nouns is closer in meaning to a third, against human consensus | 2,555 | `accuracy` | CC-BY-4.0 |
| [`system_one_eval`](benchmarks/system_one_eval/) | 60 authored tasks: policy precedence, aggregation, joins, scheduling, access control, arithmetic | 60 | `accuracy` | CC-BY-4.0 |
| [`bias_audit`](benchmarks/bias_audit/) | Whether a decision changes when only a person's demographic descriptor changes | 4,628 | `swap_invariance` | MIT + CC-BY-4.0 |
| [`openjev_heldout`](benchmarks/openjev_heldout/) | Typed decisions in games, simulated controls and workflows | 9,479 | `accuracy` | CC0-1.0 |
| [`rewardbench2`](benchmarks/rewardbench2/) | Which of four completions is best | 1,865 | `accepted_accuracy` | ODC-BY-1.0 |
| [`belebele_xl`](benchmarks/belebele_xl/) | Reading comprehension: the same 70 questions in 26 languages | 1,820 | `accuracy` | CC-BY-SA-4.0 |

Each benchmark's folder has a README with its source, attribution, what we changed and any notes on its use.

## Quick start

Requirements: Python 3.10 or later, and access to a decision-model endpoint (see the next section). The runner has no
dependencies beyond the Python standard library.

```bash
git clone https://github.com/microsoftconnect/Decision-Benchmarks.git
cd Decision-Benchmarks/runner
pip install -e .                                  # installs the `dbrun` command

export DECISION_API_KEY="<your key>"              # read from the environment only; never written to disk or printed

dbrun plan  ../benchmarks/jf100                   # what the benchmark will send, without calling anything
dbrun run   ../benchmarks/jf100 --base-url "<your endpoint>" --limit 10    # a quick 10-item check
dbrun run   ../benchmarks/jf100 --base-url "<your endpoint>"               # the full benchmark
```

The last command prints the headline result, for example `jf100: accuracy = 0.81 (answered 100/100 requests)`, and
writes the details to `results/jf100/`.

Prefer not to install? From the repository root, `PYTHONPATH=runner python -m dbrun ...` works the same way.

## Bring your own endpoint and key

You need your own access to a model; this repository contains no keys and calls nothing by itself. The runner sends
each request as JSON to the endpoint you give it, with your key, and works with any endpoint that accepts this
request format: a `state` and typed `questions` in, a probability per answer option out.

### Microsoft-Decision-1 in Microsoft Foundry

1. Deploy the model in your Foundry resource and note the **endpoint** and the **deployment name** from the
   deployment's details page.
2. Run with the decision API path and your deployment name:

```bash
# with an API key (sent in the api-key header)
export DECISION_API_KEY="<your Foundry API key>"
dbrun run ../benchmarks/jf100 \
  --base-url "<your-foundry-resource-endpoint>/providers/microsoft/v1/systemone" \
  --model "<your-deployment-name>" \
  --api-key-header api-key

# or with Microsoft Entra ID (sent as a Bearer token; tokens last about an hour)
export DECISION_API_KEY="$(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)"
dbrun run ../benchmarks/jf100 \
  --base-url "<your-foundry-resource-endpoint>/providers/microsoft/v1/systemone" \
  --model "<your-deployment-name>"
```

If a long run outlives its Entra token, refresh the token and run the same command again: it picks up where it
stopped.

### Other endpoints

Any service that accepts the same request format works the same way: pass its URL with `--base-url` (the runner adds
`/v1/systemone` unless the URL already ends in `/systemone`), its model name with `--model` if it needs one, and your
key in `DECISION_API_KEY`. By default the key is sent as `Authorization: Bearer <key>`; use `--api-key-header <name>`
for services that expect it in another header, and `--header 'Name: value'` for any extra header a service needs.

Benchmarking a third party's model is governed by your agreement with that provider; check its terms first.

## Running benchmarks

| Command | What it does |
|---|---|
| `dbrun plan <benchmark>` | Shows the number of items, requests and questions, and the metric, without calling anything |
| `dbrun run <benchmark> --base-url <url>` | Sends every request, saves each answer as it arrives, then scores the run |
| `dbrun score <benchmark>` | Re-scores saved answers without calling the endpoint |

Useful options for `run`:

| Option | Default | Use |
|---|---|---|
| `--model` | none | The model or deployment name to put in each request |
| `--api-key-env` | `DECISION_API_KEY` | Read the key from a different environment variable |
| `--api-key-header` | `Authorization` | Send the key in another header (for example `api-key`) |
| `--concurrency` | 2 | Requests in flight at once; keep it low if your endpoint rate-limits |
| `--limit N` | all | Only the first N items, for a quick check |
| `--out` | `results/<id>` | Where answers and results are written |
| `--timeout` | 120 | Seconds per attempt |

**Outputs**, in `results/<id>/`:

- `answers.jsonl`: one line per request, with the answers or the error.
- `result.json`: the primary metric, every metric, slices and coverage.
- `per_item.jsonl`: each item's verdict.

**Resuming.** Run the same command again and requests already answered are skipped, so an interrupted or
rate-limited run can be finished later.

**Rate limits.** Rate-limited and temporarily failing requests are retried up to 10 times, waiting at least as long
as the endpoint asks and backing off further each time. A request that still fails is recorded as unanswered and left
out of the metrics; `result.json` reports how many (coverage).

**All benchmarks:**

```bash
for b in ../benchmarks/*/; do
  dbrun run "$b" --base-url "<your endpoint>" --model "<model>" --out "results/$(basename "$b")"
done
```

## How answers are scored

The runner scores every benchmark the same way, so results are comparable:

- **Yes/no questions** count as yes when the probability of yes reaches the threshold (0.5, or the benchmark's
  `scoring.noul_threshold`).
- **Choice and score questions** count as the most probable option; exact ties go to the option listed first.
- **Standard metrics:** `accuracy` (with `accuracy_by_type`), `ece` (expected calibration error, 10 bins), `brier`, and
  `rep_agreement` for benchmarks run more than once per item.
- **Benchmark-specific metrics:** where a benchmark has its own metric (for example nDCG, accepted-answer accuracy or
  correlation with human scores), its `scorer/scorer.py` computes it from the collected answers. The scorer runs
  locally in a separate Python process with network access disabled.
- **The headline metric** for each benchmark is its `scoring.primary` in `benchmark.json` (the table above).
- Answers that are missing or can't be read are left out of the metrics, never counted as wrong; `result.json`
  reports coverage so you can see how many.

## Using the data without the runner

Each `benchmarks/<id>/data/items.jsonl.gz` is a gzip-compressed JSON Lines file, one item per line (read it with
`gzip.open(path, "rt")` in Python, or `gunzip -c` / `zcat` on the command line; the runner reads it directly):

- `id`: the item's identifier.
- `state`: the input to decide about (text or JSON).
- `questions`: named questions, each with a `type` (`choice`, `noul` for yes/no, or `score`), `instructions`, and
  `criteria` (the answer options for `choice`, the ordered levels for `score`).
- `labels`: the correct answer for each question (a choice option, `true`/`false`, or a score level's index).
- `label_probs` (some benchmarks): the human or reference distribution over answers.
- `group`, `meta`: grouping and descriptive fields used for slices and scoring.

`state` and `questions` together form a request body. `benchmark.json` says whether an item's questions are sent
together or one at a time (`run.request_mode`), how many times (`run.reps`), and how answers are scored.

## Repository layout

```
├── README.md                 This page
├── TRANSPARENCY.md           Transparency note: intended uses, limitations, data details
├── LICENSE                   MIT: the repository's code and documentation
├── LICENSING.md              Which licence covers what
├── THIRD_PARTY_NOTICES.md    Attribution and notices for every source
├── runner/                   The dbrun runner (MIT) and its tests
└── benchmarks/<id>/
    ├── README.md             The benchmark's card: source, attribution, changes, notes
    ├── benchmark.json        How items are sent and scored
    ├── data/                 The items and their licence, set by the source
    │   ├── items.jsonl.gz
    │   └── LICENSE
    └── scorer/               The benchmark's metric code, where it has one (MIT)
        ├── scorer.py
        └── LICENSE
```

## Licensing

Code and data are kept apart so each is clearly licensed. The runner, the scorers, the manifests and the
documentation are Microsoft code under MIT. Each benchmark's `data/` folder is licensed by its source: MIT,
Apache-2.0, CC BY 4.0, CC0, ODC-BY or CC BY-SA 4.0. Where you redistribute or adapt a benchmark's data, follow its
licence: keep the notices, credit the source and indicate your changes, and share adaptations of CC BY-SA 4.0 data
(`belebele_xl`) under the same licence. See [LICENSING.md](LICENSING.md) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Responsible use

These benchmarks measure decision quality on public tasks. Results on them don't establish that a model is suitable
for a particular application; evaluate on data that represents your use case. The benchmarks are for evaluation:
don't use them to train or tune a model, or results on them stop being meaningful. Some benchmarks contain sensitive
material by design (harmful requests to be refused in `rewardbench2`, demographic variations used to test for bias
in `bias_audit`, health topics in `healthbench_consensus`); their READMEs say so. See [TRANSPARENCY.md](TRANSPARENCY.md) for
intended uses, limitations and how the data was prepared.

## Reporting issues

Please use GitHub Issues for bugs and questions. See [SUPPORT.md](SUPPORT.md) and, for security issues,
[SECURITY.md](SECURITY.md).

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor
License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your
contribution. For details, visit https://cla.opensource.microsoft.com.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact
[opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft
sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.
