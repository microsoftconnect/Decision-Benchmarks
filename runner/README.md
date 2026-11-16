# dbrun: run and score the decision benchmarks

`dbrun` sends each benchmark's items to a decision-model endpoint that speaks the System One API, saves the answers,
and scores them the way our published results were scored. It is plain Python 3.10 or later with no dependencies
beyond the standard library.

## What a benchmark looks like

Each benchmark is a folder under `benchmarks/<id>/`:

| File | What it holds |
|---|---|
| `benchmark.json` | The manifest: how requests are sent (`run.request_mode`, `run.reps`) and how they are scored (`scoring.primary`, `scoring.slices`, `scoring.scorer`). |
| `items.jsonl` | One item per line. Each item is a System One request (`state` and typed `questions`) with the right answers in `labels`. |
| `scorer.py` | Optional. Metrics beyond the standard ones (for example nDCG@10, or accuracy where several answers are right). |
| `assets/` | Images, for benchmarks that use them. |
| `README.md` | The benchmark's card: its source, licence, attribution and what was changed. |

## Quick start

```bash
cd runner
pip install -e .                      # or run with PYTHONPATH=runner python -m dbrun ...

export DECISION_API_KEY=<your key>    # read from the environment; never written to disk or printed

# what a benchmark will send
dbrun plan ../benchmarks/di_gsm8k

# a quick check on the first 10 items
dbrun run ../benchmarks/di_gsm8k --base-url https://<your endpoint> --limit 10

# the full benchmark
dbrun run ../benchmarks/di_gsm8k --base-url https://<your endpoint> --model <model name>
```

`run` writes to `results/<id>/` (change it with `--out`):

- `answers.jsonl`: one line per request, with the answers or the error;
- `result.json`: the primary metric, every metric, slices and coverage;
- `per_item.jsonl`: each item's verdict.

Run the same command again to resume: requests already answered are skipped. `dbrun score <benchmark>` re-scores
saved answers without calling the endpoint.

## Options for `run`

| Option | Default | What it does |
|---|---|---|
| `--base-url` | (required) | The endpoint. `/v1/systemone` is added unless the URL already ends with it. |
| `--model` | none | The model name to send in each request, for endpoints that serve several models. |
| `--api-key-env` | `DECISION_API_KEY` | The environment variable holding the key. |
| `--api-key-header` | `Authorization` | Where the key goes: `Authorization` sends `Bearer <key>`; another name (for example `api-key` for Microsoft Foundry) sends the key as that header's value. |
| `--header 'Name: value'` | none | An extra header; repeat for more. |
| `--concurrency` | 2 | Requests in flight at once. Keep it low if the endpoint rate-limits. |
| `--timeout` | 120 | Seconds per attempt. |
| `--limit N` | all | Only the first N items. |
| `--items FILE` | the folder's | Items to use instead of the folder's `items.jsonl` (for example, ones built from the original source). |

Rate-limited and temporarily failing requests are retried up to 10 times, waiting at least as long as the endpoint
asks (`retry_after_ms` or `Retry-After`) and backing off further on each attempt. A request that still fails is
recorded as unanswered and left out of the metrics; `result.json` reports coverage so you can see how many.

## How answers are scored

- **Yes/no questions** are read as yes when the probability of yes reaches the threshold (0.5, or the manifest's
  `scoring.noul_threshold`).
- **Choice and score questions** are read as the most probable option. Exact ties go to the option listed first in
  the request.
- **Standard metrics:** `accuracy` (with `accuracy_by_type`), `ece` (expected calibration error, 10 bins), `brier`,
  and `rep_agreement` for benchmarks run more than once per item.
- **A benchmark's `scorer.py`** runs in a separate Python process with network access disabled, gets each answered item's
  answers and readings, and adds its own metrics. `scoring.primary` in the manifest names the headline metric.

Answers that are missing or can't be read are left out of every metric, never counted as wrong, unless a benchmark's
scorer says otherwise (some also report a figure that counts them as wrong).

## What the runner sends, and to where

- Only to the `--base-url` you give, over HTTPS (or HTTP if you give an `http://` URL).
- Each request body is the item's `state` and `questions` (and its images, base64-encoded, for image benchmarks),
  plus `model` if you set `--model`. Labels and metadata are never sent.
- Headers: `Content-Type: application/json`, the key (as `Authorization: Bearer <key>`, or in the header named by `--api-key-header`), and any `--header` you add.
- Nothing else: no telemetry, no other hosts. `scorer.py` files run offline.

## Tests

```bash
cd runner
python -m unittest discover -s tests
```

The tests use a local fake endpoint; they make no external calls.

## Licence

MIT. Each benchmark's data keeps its own licence, given in its folder.
