# ShadowWork-SHIFT: how the training data were actually constructed

**Status: completed and audited.** This document describes the **executed** SW12 and SW17 pipelines, not an intended dataset recipe. Counts, row hashes, optimization histories and scored outcomes were checked against `ShadowWork_12_Closed_Loop_Evidence.zip` (581 archive members, 580 verified SHA-256 commitments) and `ShadowWork_17_Training_Attribution_Evidence.zip` (497 members, 496 verified commitments). The exact training rows, splits and scored trajectories are publicly released at [Hugging Face](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets).

## Purpose and provenance

The data are **synthetic stateful tool-agent workflows** designed to test whether a tool-using language model can recover from misleading acknowledgements, no-op writes, conflicts, stale reads, insufficient verification, unauthorized requests and injected instructions. The data were **not collected from production services, scraped from real user logs, or manually annotated by human operators**. Scenario specifications, fault injections, and a deterministic reference policy are authored for this controlled evaluation.

The pipeline resembles **one round of learner-state expert relabeling**, related in motivation to dataset aggregation (Ross, Gordon and Bagnell, [AISTATS 2011](https://proceedings.mlr.press/v15/ross11a.html)). It is **not full iterative DAgger**, and the scripted reference policy is not an independently validated optimal expert.

## Executed SW12 data pipeline

1. **Generate deterministic scenarios and holdouts.** Seed `20261113`; 8 failure families: normal, double conflict, double no-op, wrong-then-stale, two stale checks, false positive, injected forbidden, injected authorized. Each family contains both one-check and two-check verification protocols. Files: 192 training tasks, 32 development tasks, and 64 sealed evaluation tasks. The task JSONLs and their SHA-256 digests were written to `precommit.json` before learner collection and evaluation. Protocol action budget: 22.
2. **Run the frozen learner on training tasks.** Start from the archived SW09 corrective adapter on the exact 7-shard custom Plain SFT base (not a substitute generic upstream checkpoint). Collect 160 real policy rollouts on training tasks, distributed across all 8 failure families; store model actions, executable tool observations, final scores and source-model provenance.
3. **Generate reference actions using observable history.** A deterministic reference policy reads the ticket, runbook, health, approval, current mutation receipts and post-write checks. It selects an authorized next JSON tool action, with explicitly typed field/value checks and evidence requirements. It does not read a hidden simulator-success label to choose the next action. The implementation *does* know the benchmark protocol's check-count setting, communicated to the agent in the task instructions. The reference is executed on the same gated SQLite simulator to check feasibility.
4. **Construct learner-state training examples.** Replay saved learner action histories against the environment, and for each eligible learner-visited observation prefix create an `(observed prompt, reference next action)` label. Compare the original learner proposal against that reference. Token-length eligibility uses the same chat template as training; labels are not sourced from sealed cases.
5. **Build matched training arms.** Both arms have exactly **800 prompt-completion rows**, with **400 deliberately shared expert anchor rows** and 400 differentiated rows. Corrective arm: selected learner-visited prefixes, stratified by fault group, verification protocol and teacher action, prioritizing action disagreements. Rehearsal arm: ordinary reference-policy/expert states from training tasks. Both start from the **same frozen SW09 adapter**, with 80 training steps, LR `5e-5` and global batch 8. This is a *matched-size/compute* comparison, not a guarantee of identical example difficulty or token budgets.
6. **Independently check heldout performance.** Use the same workflow, tool grammar and evaluation controller per model. Strict success checks persisted SQLite state, authorization and sufficient post-mutation evidence, not just whether a language model says “completed.” Keep original JSON episodes and scorecards. Controller interventions are separate from fine-tuning effects.

## Independently audited SW12 facts

| Measurement | Verified count |
|---|---:|
| Train / development / sealed task specifications | 192 / 32 / 64 |
| Train-only learner rollouts | 160 |
| Candidate learner states | 1,276 |
| Learner-state action-disagreement candidates | 387 |
| Selected learner-state rows | 400 |
| Selected rows with an actual disagreement | **175** |
| Shared expert anchors per arm | 400 |
| Total rows per training arm | **800** |
| Identical realized prompt-completion pairs across arms | 452 |

The **452** realized identical pairs include the 400 intentionally shared anchors and 52 additional coincidental identical examples. Hence **do not claim all 400 differentiated corrective rows are errors**. The two published final training files are each 800 unique prompt-completion rows. Neither file contains direct development or sealed task IDs, although this simple leakage check does not establish statistical independence across a shared task generator.

### Original SW12 file commitments

- Train tasks SHA-256: `a41783c2370f2a9a33c90464c055b14161da028d11c273991b07e2f14c350793`
- Development tasks SHA-256: `5fce6aa19f454549d5379d2858bff47c0e65ac04f28d523825fbc2b8437adfce`
- Sealed tasks SHA-256: `3b91477db786aac7dd2f58ff0bc9e28f8033766e06d1d281625a7228731fba88`
- Corrective v3 training SHA-256: `50adf52ca783358f3a9504ea65e17599e8181f374fb18a0e13153c4a40acfd50`
- Rehearsal v3 training SHA-256: `cdf338acf469d8c7ffeb4e9c2749d1bb932d79d0a76fb7b3d9fe61740763671a`

The archived SW12 `selection_audit.json`, `precommit.json`, `final_provenance.json`, source notebook and per-episode JSONs provide the underlying audit trail.

## Executed SW17 dataset construction and quantitative audit

SW17 is the **fixed-controller training-attribution experiment**. Its purpose is to test a falsifiable hypothesis: under an unchanged inference-time controller, does training on real learner-visited failure states improve a compact tool agent's reliable recovery, and how does it compare with equal-budget expert rehearsal? The dataset was constructed specifically for this question, rather than assembled from unspecified internet text or generated by an unverified LLM judge.

### 1. Seeded tasks and a precommitted evaluation boundary

A fixed-seed generator (`20261115`) produces **360 executable SQLite maintenance tasks**: **240 training**, **40 development** and **80 sealed**. Ten failure groups receive **24/4/8** train/dev/sealed cases each: `normal`, `double_conflict`, `double_noop`, `wrong_then_stale`, `two_stale`, `false_positive`, `injected_forbidden`, `injected_authorized`, `approval_not_required`, and `lease_expired`. Both one-check and two-check verification requirements are balanced in each split; the sealed split has 40 tasks per verification protocol.

Each task specifies a permitted or forbidden configuration change, typed values, approval and scope conditions, canary health, service/region text, and the simulator's fault schedule. **The agent receives ticket/runbook/health/approval observations, not the hidden scenario record or fault label.** The simulator tracks durable configuration state in SQLite while allowing acknowledgments, retries and readbacks to disagree with that state. The task generator, split JSONLs, seed and SHA-256 digests were frozen in `precommit.json` **before learner rollouts and sealed evaluation**.

SW17 also varies ticket phrasing, service and region names, and withholds three configuration fields from training (`batch_window_ms`, `retention_days`, `max_inflight_jobs`). Forty sealed tasks use those unseen fields. This is a controlled **within-family schema-shift test**, not an independently authored external benchmark.

### 2. Collect actual frozen-agent decisions

Initialize the agent with the **same frozen SW09 corrective adapter** used as the later training starting point. Execute **160 actual model-driven episodes** on train-only tasks (16 per failure group), recording every structured action, returned observation, blocked attempt, final SQLite state and score. Four preliminary observations are scripted identically for every policy; subsequent actions come from the model.

The saved 160 rollouts yielded **1,311 eligible learner-visited states**, including **859 learner/reference action-disagreement candidates** before final selection. The learner's action is compared with an **observation-conditioned scripted reference continuation**, which reads the same tool history and is checked by replay on the stateful simulator. The reference is a reproducible executable policy, **not** a human annotator, independently validated optimal oracle or hidden sealed-label lookup.

### 3. Build correction and genuinely matched rehearsal curricula

Select **400 unique learner-state prompts**, prioritizing real action disagreements while covering all ten fault groups, both verification protocols and a range of reference actions. **211/400 selected learner states** have a different reference action from the frozen learner's original action; the other 189 are legitimate learner-visited observation contexts on which the reference agrees. This is why the release calls these *learner-state corrective examples*, not 400 fabricated individual failures.

Build a shared pool of **400 identical reference-policy anchor examples** for both arms. Then add **400 selected learner-state/reference pairs** to the corrective arm and **400 ordinary reference-policy pairs** to the rehearsal arm. For SW17, the rehearsal extras are greedily matched to corrective examples by **failure group, required check count and reference action** when possible, with **395/400 exact matches** on these three strata. Both final arms contain **800 unique prompt-completion pairs**; their **only 400 exact shared prompt-completion pairs** are the planned common anchors. The audited training files contain no explicit development or sealed task IDs.

A row is a prompt encoding the maintenance instruction, available tool schema and **actual observation history**, plus a completion encoding **exactly one JSON tool action**. The training data are **not** a collection of claimed human-expert conversations. Selection applies a **2,550-token SFT budget** and checks group/action coverage and uniqueness. Action targets are computed using the executable reference policy rather than silently hand-edited after evaluation.

### 4. Evidence-linked worked example

One actual corrective-arm training prompt is `SW17-TRAIN-02-006` (`double_noop`). The agent has already observed the ticket, runbook, canary health and approval, staged a valid configuration field, and obtained a commit-tool response resembling `{"status":"ok","committed":true}`. At this **recorded learner-visited prefix**, the supervised reference action is `[{"tool_name":"read_lease","parameters":{}}]`, not a premature `finish completed`. The model must continue evidence gathering and recovery rather than treating the receipt as proof of a durable update. The complete, unabridged prompt and action are present in the published `learner_corrective_v4_training.jsonl`.

This example illustrates the scientific target: **the distinction between a successful-looking tool message and enough observed evidence to finish correctly**. It is one representative training row, not a claim that the scripted teacher is infallible.

### 5. Equal starting weights, actual optimizer updates and paired tests

Both v4 adapters were trained from the **identical original SW09 corrective LoRA and exact custom seven-shard Plain SFT base**, using **80 optimizer steps**, LR `5e-5`, effective global batch **8** (two T4 GPUs), and completion-only loss labels that mask prompt tokens. Each arm's `*_training_metadata.json` contains its exact JSONL SHA-256, optimizer step/loss history (through step 80), runtime versions and final trained tensor provenance. The models are genuinely different saved weight files, not a comparison between prompts only.

For evaluation, every policy encounters the same **80 precommitted sealed tasks**, identical four-read bootstrap, same action limits and same tool/evidence rules, with **no extra post-bootstrap repair controller**. Frozen SW09 scores **31/80** strict; corrective v4 and matched rehearsal v4 each score **65/80**. Corrective vs frozen has **38 wins / 4 losses** on paired tasks (exact McNemar `p=5.653146e-8`). Corrective vs matched rehearsal has **5 wins / 5 losses** (`p=1`). Hence the data support **additional supervised learning under fixed inference controls**, **not** a demonstrated advantage of the learner-correction curriculum over a strong matched rehearsal baseline.

### 6. Auditable file commitments

| Artifact | Recorded value |
|---|---|
| Frozen train split SHA-256 | `6b2f73c0a0500656b071ca107f217bf3f1b6acb238d33bec0d211bb33caa71df` |
| Frozen development split SHA-256 | `6d812921273d236524dbbebacb5117840bb17d3645c27b78610122c92442e06e` |
| Frozen sealed split SHA-256 | `789c656e798913bb3a9dbe0e19ef937a665f1782d33298d7b24e95c9f30cdb12` |
| Corrective v4 training JSONL SHA-256 | `f52e2c97341107ec7ef14b9239781928d9aa3fadb37ec9b4d042a373d9a1b584` |
| Matched rehearsal v4 training JSONL SHA-256 | `1222b751f32b534031223050444d43d42dc1ba4a571474f5f6815698047eee3d` |
| Corrective v4 trained adapter SHA-256 | `ebf7ed229641faf882f51d55c8aa0a12be748984cb7370d1399c236ab38bbff3` |
| Rehearsal v4 trained adapter SHA-256 | `36e4f7b0686029465899d2931bb15deaf95e77f310da2f9c8f57a29996f74b99` |

These are **original experimental commitments**, reproduced from the saved evidence archive and reflected in the public release. Strict task and exact-ID leakage checks were performed. Because the synthetic generator and task grammar are related across splits, **this does not amount to near-duplicate-proof or independent production-distribution testing**.

## Dataset fields and reproducibility

- `*_training.jsonl`: each row contains `prompt` (observed history + action grammar) and `completion` (exact one-action JSON array). Corrective labels are tool actions, not free-form human rationales.
- `*_tasks.jsonl`: scenario specifications, including goal, authorized state, failure-family ID, check-count and task split. Task specification contains hidden simulator metadata and must **not** be passed wholesale to the agent during evaluation.
- `collection/*.json`: saved train-only model actions, tool observations, run metadata and scores.
- `selection_audit.json`: coverage and label selection, including count of actual corrections.
- `precommit.json`: seed and task-split checksums established before model evaluation.
- `evaluation/**/*.json` and scorecards: retained strict outcomes and execution evidence.

Recreate from the archived source notebooks in `notebooks/` using the exact base and starting adapters, pinned libraries, fixed generator seeds and task-identity commitments. Preserve the train/dev/sealed separation. **Do not include sealed test tasks or test traces in training.**

## Methodological boundaries

The simulator and reference policy were developed together. Reference-policy labels are procedural ground truth *within the simulator*, not independent human expert annotations. Some failures are deterministic scripted injections. The 64-case SW12 sealed test is small and shares grammar with training. In SW12, matched rehearsal slightly exceeds corrective training on strict success (**47/64 vs 46/64**), so the data do **not** demonstrate that learner-state corrections uniquely outperform ordinary rehearsal. Strong runtime-controller gains must be reported separately.

This documentation follows the questions recommended by [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) and the [Hugging Face dataset card guide](https://huggingface.co/docs/hub/en/datasets-cards), including source, generation, potential bias, recommended usage, and limitations. These references guide **documentation**, not claims of external dataset certification.
