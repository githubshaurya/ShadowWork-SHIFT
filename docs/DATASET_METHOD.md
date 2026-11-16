# ShadowWork-SHIFT: how the training data were actually constructed

**Status:** This is a description of the executed SW12 pipeline and the source-defined SW17 continuation. SW12 counts below were independently checked against the original `ShadowWork_12_Closed_Loop_Evidence.zip`. SW17's final dataset counts/holdout scores must be taken from its saved artifacts, not inferred from its intended configuration.

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

## SW17 continuation (source design, not a substitute for saved results)

SW17 has **10** failure families, introducing approval-not-required and lease-expired cases. The source-defined design uses 240 training, 40 development and 80 sealed tasks, plus 160 train-only learner rollouts. It expands heldout lexical/service/region and configuration-field variation; both v4 arms again use 800 rows and 400 shared anchors, start from the same SW09 adapter, and train for 80 steps. An initial four-read bootstrap is held identical across policies, with no additional deterministic repair controller. The finalized source `selection_audit.json`, saved training rows, precommit and evaluation episodes should be published *without replacing them with these design targets*. SW17 still uses the same family of synthetic workflow environments; **it is not an independent external benchmark**.

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
