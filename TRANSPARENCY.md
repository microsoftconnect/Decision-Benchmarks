# Transparency note: dbrun and Decision Benchmarks

## Overview

dbrun is a small, open-source command-line tool (Python standard library only) that sends benchmark items to a decision-model endpoint the user chooses, using the user's own API key, saves the answers, and scores them. It contains no model and no data of its own.

Decision Benchmarks is a set of 18 public benchmarks for decision models (models that answer closed questions about an input and return a probability for each answer option, instead of generating text), adapted by Microsoft to the request format used by Microsoft-Decision-1. It was developed to give a broad, reproducible measure of decision quality across classification, rule application, judging and preference, bias and calibration, reasoning and multilingual decisions. The benchmarks were created and shared by researchers and developers across the open-source community; each benchmark's README credits its authors and links to the original.

See the repository [README](README.md) and the [Microsoft-Decision-1 documentation](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision).

### What dbrun can do

dbrun was developed to run the benchmarks in this repository against any endpoint that accepts the same request format (a `state` and typed `questions` in; a probability per answer option out), and to score the answers the same way for every model, so results are comparable and reproducible. It can resume interrupted runs, retries rate-limited requests, and re-scores saved answers without calling the endpoint.

Decision Benchmarks is being released together with dbrun to enable users to reproduce published results, evaluate their own deployments, and compare models that accept the same request format.

### Intended uses

dbrun is best suited for running the benchmarks in this repository against a decision-model endpoint the user has access to, and for scoring the collected answers.

Decision Benchmarks is intended to be used either with dbrun or with any other tool that can send its items to a decision model and compare the answers with the labels; each item is a self-contained JSON request with its correct answer.

dbrun and Decision Benchmarks are being shared with the research community to facilitate reproduction of our results and foster further research in this area.

dbrun and Decision Benchmarks are intended to be used by domain experts who are independently capable of evaluating the quality of outputs before acting on them.

### Out-of-scope uses

dbrun is not well suited for evaluating generative (free-text) models, and it is not a load-testing or monitoring tool. It does not generate, execute or modify code, and it calls no system other than the endpoint the user supplies.

Decision Benchmarks is not well suited for training models (the benchmarks are for evaluation; training on them invalidates results), and it is not a safety or red-teaming benchmark: no benchmark in it contains prompt-injection, jailbreak or other attack material.

Most items are in English. Some benchmarks are multilingual (Belebele: 26 languages; GlobalGroup: Arabic, Chinese, English, Hindi and Spanish; Typed Decisions: Japanese and Russian), but many languages, regions and domains have few or no instances. As a result, Decision Benchmarks should not be used on its own to judge a model's suitability for a particular language, domain or population.

We do not recommend using results from dbrun or Decision Benchmarks as the only basis for choosing a model for a commercial or real-world application; evaluate on data that represents your use case. They are being released for benchmarking and research.

dbrun and Decision Benchmarks were not designed or evaluated for all possible downstream purposes. Developers should consider their inherent limitations as they select use cases, and evaluate and mitigate for accuracy, safety, and fairness concerns specific to each intended downstream use.

Without further testing and development, dbrun and Decision Benchmarks should not be used in highly regulated domains where inaccurate outputs could suggest actions that lead to injury or negatively impact an individual's legal, financial, or life opportunities.

We do not recommend using dbrun or Decision Benchmarks in the context of high-risk decision making (e.g. in law enforcement, legal, finance, or healthcare).

## Dataset details

### Dataset contents
Decision Benchmarks consists of 41,627 items in 18 benchmarks. Each item is one decision task: an input (`state`, text or JSON) and one or more closed questions about it.

Each instance includes an identifier, the input, its questions (each with a type: choice, yes/no or score; instructions; and the answer options or ordered levels), grouping and descriptive metadata, and, for four benchmarks, the human or reference distribution over answers.

Each instance is associated with labels giving the correct answer to each question, as published by the source benchmark (a choice option, yes or no, or a score level).

The source benchmarks were created by their authors between 2022 and 2026; Microsoft adapted them to the request format in October and November 2026.

Decision Benchmarks does not contain links to external data sources in its data files. Each benchmark's README links to its original source. Some source texts (for example, model completions) mention web addresses as part of their content.

### Data creation and processing
Decision Benchmarks is adapted from 18 existing public datasets: JevBench, Jev Frontier 100, LAYA Synthetic Bench, Tree Choice CAP, OOD Calibration, HealthBench (physician-consensus subset), JevQA metadata, decision-bench, JevBench v1.5, Typed Decisions (Japanese and Russian), GlobalGroup, the Upworthy Research Archive headline tests, the Three Terms Task, the System One eval, Jev Bias Audit (with BBQ), Open-Jev held-out sets, RewardBench 2 and Belebele. Each benchmark's README names its source, authors and licence.

The existing data consisted of decision tasks with known answers: synthetic business and workflow cases, authored reasoning items, health-conversation responses graded by physicians, video-encoding metadata with quality scores, word-grouping puzzles, real headline A/B test results, word-similarity judgements, bias test scenarios, game and control logs, model completions with preference labels, and reading-comprehension passages and questions.

The existing data was originally collected or created by the source benchmarks' authors (academic researchers, companies such as OpenAI, Meta and the Allen Institute for AI, and independent developers), in some cases from earlier public sources such as Wikimedia projects (Belebele), Upworthy's published A/B tests, and the BBQ bias benchmark.

Decision Benchmarks was created by converting each source's items, unchanged in text and answers, into the Microsoft-Decision-1 request format, selecting the published subsets described in each benchmark's README.

Dataset creation was carried out by members of the Microsoft team using automated conversion scripts, with each benchmark's output checked by the team against its source (item counts, checksums and answers).

Decision Benchmarks includes no data crawled by Microsoft. Some sources were themselves built from public web content (for example, Belebele from Wikimedia projects and the headline tests from Upworthy's published experiments).

### People and identifiers

Data points do not correspond to individual people. Three Terms uses only the public per-triplet summary of raters' choices, not the gated individual-subject data; HealthBench grades are physicians' aggregate judgements.

Decision Benchmarks does not include data from or about real children. Some synthetic scenarios (for example, the bias-audit scenarios) mention fictional people of different ages.

The existing data used to create the dataset did not contain information intended to identify a person. Synthetic cases use made-up names and contact details, and some RewardBench 2 safety prompts and completions mention public figures or contain model-invented contact details.

Decision Benchmarks is not believed to contain information that could be used to identify a private individual.

### Sensitive or harmful content

The existing data contained information that might be considered sensitive: health-related conversations (HealthBench) and demographic descriptors (age, disability, gender identity, nationality, physical appearance, race and ethnicity, religion, socio-economic status, sexual orientation) used in fictional scenarios to test whether a decision changes when only the descriptor changes (bias audit).

The existing data contained requests that might be considered offensive or harmful: the RewardBench 2 Safety subset (450 items) asks which of several completions best handles requests a model should refuse or answer carefully (including sexually explicit, hateful or derogatory, misinformation, privacy-invading and impossible requests), and some rejected completions comply with them.

Decision Benchmarks contains information that might be considered sensitive, as described above: health topics and demographic descriptors of fictional people, used to test decision quality and bias.

No harmful content was removed beyond the source benchmarks' own curation; the Safety subset is kept because it measures whether a model prefers safe responses. Content was removed from two sources for rights reasons: 521 items from Open-Jev held-out sets and the GlobalGroup part derived from NYT Connections puzzles.

Decision Benchmarks contains content that might be considered offensive, limited to the RewardBench 2 Safety subset described above.

### Other processing

Duplicate removal was not needed beyond the sources' own; the team checked that each benchmark's items are unique by identifier.

The data was not relabelled. Labels are the sources' own: written by the benchmarks' authors, by physicians (HealthBench), by human raters (Three Terms, Upworthy click results), computed by program (procedurally generated tasks) or chosen by the source's curators (RewardBench 2).

Other processing: the items were converted into the request format; internal tracking fields were removed from item metadata; bias-audit items record which license covers each item.

## How to get started

Clone https://github.com/microsoftconnect/Decision-Benchmarks, install the runner (`pip install -e runner`), set your own key in the DECISION_API_KEY environment variable, and run `dbrun run benchmarks/<id> --base-url <your endpoint>`. The repository README covers Microsoft Foundry endpoints (API key or Microsoft Entra ID), other endpoints, options, outputs and scoring.

## Validation

To assess how effective Decision Benchmarks would be at its intended purpose, our team looked for benchmarks with well-defined answers, open licenses, provenance traceable to the original creators, and coverage of a broad range of decision types and languages.

Specifically, we traced each benchmark's origin back to its original creators, reviewed its license and content with Microsoft's legal and open-source reviewers, checked each released file against its source (counts and checksums), and verified the release's conditions automatically before publication.

## Evaluation

dbrun was evaluated on its ability to send requests correctly, handle rate limits and failures, resume runs, and score answers exactly as our internal evaluation does.

### Evaluation methods

We used automated tests (15 unit and end-to-end tests against a local test endpoint) and an equivalence check: each of the nine benchmark-specific scorers in dbrun gives exactly the same results as the internal scorer it was made from.

The release was also scanned with CodeQL and an internal check for credentials and internal references, and reviewed by Microsoft security and the team.

The model used for evaluation was Microsoft-Decision-1.1. For more on this model, please see <https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision>

Results may vary if dbrun is used with a different model or endpoint, based on its design, configuration and training.

dbrun does not generate content. It sends the user's requests to the endpoint the user names, with the user's own key, which it reads from an environment variable and never writes to disk or prints. Benchmark scorers run locally in a separate Python process with network access disabled.

### Evaluation results

At a high level, we found that dbrun sends, resumes and scores runs correctly in all tests, and its scorers match the internal scorers exactly.

## Limitations

### Code

dbrun was developed for benchmarking. Further testing and validation are needed before using it as part of a production system.

dbrun is language-independent: it passes the benchmarks' text through unchanged. Results in languages other than English should be interpreted by someone who is both an expert in the task and a native speaker of that language.

Benchmark results describe a model's decisions on public tasks; they don't establish that a model is suitable for a particular application. Decisions based on a model's outputs should be made with human oversight.

dbrun does not include a model. When used with Microsoft-Decision-1, see https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision for that model's capabilities and limitations.

dbrun sends benchmark text to the endpoint the user chooses; it does not act on model outputs, call tools or execute code. Users should only send benchmarks to endpoints they trust and are permitted to use.

### Data

Decision Benchmarks was developed for benchmarking. Results on it don't establish that a model is suitable for a particular application.

Most of Decision Benchmarks is in English; three benchmarks cover other languages (Belebele 26 languages; GlobalGroup five; Typed Decisions Japanese and Russian), some of them machine-translated.

Decision Benchmarks inherits any errors or noise in its sources' labels; some labels (for example, click results and rater consensus) reflect human behavior rather than a single right answer.

Decision Benchmarks is missing the parts of some sources that could not be redistributed (described in each benchmark's README).

The ability to access the source datasets linked from each benchmark's README is beyond the control of the team.

Decision Benchmarks has not been systematically evaluated for sociocultural, economic, demographic or linguistic bias beyond the bias audit it includes. Developers should consider the potential for bias as they select use cases, and evaluate and mitigate for accuracy, safety, and fairness concerns specific to each intended downstream use.

Decision Benchmarks should not be used as the sole basis for decisions in highly regulated domains where inaccurate or incomplete outputs could lead to injury or negatively impact an individual's legal, financial, or life opportunities.

Decision Benchmarks was developed for use with Microsoft-Decision-1.1 and any model that accepts the same request format. See https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision for Microsoft-Decision-1.1's capabilities and limitations.

## Best practices

Better results can be achieved by keeping concurrency low on rate-limited endpoints and by reading each benchmark's README before interpreting its results.

The benchmarks are evaluation sets: we recommend using them only for evaluation, not for training or tuning a model, so that results stay meaningful.

We strongly encourage users to use models and services that support robust Responsible AI mitigations, such as Microsoft Foundry. Such services continually update their safety and RAI mitigations with the latest industry standards for responsible use. For more on responsible use, please see:

- [What is Azure AI Content Safety?](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview)

- [Deploy and use Microsoft Decision models](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision)

It is the user's responsibility to ensure that the use of dbrun and Decision Benchmarks complies with relevant data protection regulations, organizational guidelines and the terms of any model provider whose endpoint they benchmark.

## License

The code and documentation are released under the MIT License. Each benchmark's data keeps its source's license (MIT, Apache-2.0, CC BY 4.0, CC0 1.0, ODC-BY 1.0 or CC BY-SA 4.0), stated in its data/LICENSE file; see [LICENSING.md](LICENSING.md).

Nothing disclosed here, including the Out of Scope Uses section, should be interpreted as or deemed a restriction or modification to the licenses the code and data are released under.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft's Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party's policies.

## Ethics

Microsoft did not collect new data from people or annotate data for this release; no Institutional Review Board approval was required. The sources' own data collection is described in their papers and dataset cards.

## Contact

This work was conducted by members of Microsoft. We welcome feedback and collaboration from our audience. If you have suggestions, questions, or observe unexpected/offensive behavior in our technology, please contact us at <decision-feedback@microsoft.com>

If the team receives reports of undesired behavior/content or identifies issues independently, we will update this repository with appropriate mitigations.
