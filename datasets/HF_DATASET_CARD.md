---
pretty_name: "ShadowWork-SHIFT: Stateful Tool-Agent Recovery Training and Evidence"
language:
- en
tags:
- agents
- synthetic
- tool-use
- imitation-learning
- corrective-training
- auditkit
- lexsi
license: cc-by-nc-4.0
---

# ShadowWork-SHIFT: training datasets and evaluation evidence

**What this is:** Synthetic, executable, stateful configuration-maintenance tasks for measuring failure recovery in tool-using language models. The release includes paired corrective and expert-rehearsal supervised datasets, original train/dev/sealed task splits, learner-visited traces, selection audits, and held-out evaluation evidence. It is not a production-log or human-annotated dataset.

**Source code and methodology:** [GitHub](https://github.com/githubshaurya/ShadowWork-SHIFT) · [Detailed creation process](https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/docs/DATASET_METHOD.md).

## Construction

1. Use a seeded generator to create **eight SW12 failure families**, including no-op writes, conflicting commits, stale read-backs, false-positive acknowledgement and forbidden/injected requests. Vary one-check and two-check post-mutation evidence rules.
2. **Precommit train/development/sealed task identities and SHA-256 hashes before evaluation**; keep all supervised examples on the training split.
3. Execute the **frozen SW09 tool policy** on 160 train-only tasks and save real model action/observation histories.
4. Relabel learner-visited observation prefixes with a **scripted, observation-driven reference policy** under the SQLite tool gate. Validate action and persisted-state evidence. This is a **single-round, DAgger-inspired** procedure, *not* a human oracle, full iterative DAgger, or model-based reward labeling.
5. Select 400 learner-state rows stratified by failure group, verification protocol and reference action, prioritizing disagreements. Combine with 400 shared expert anchors. Build a **matched 800-row rehearsal control** using reference-policy states, with the same starting checkpoint and compute budget.
6. Publish the untouched split files, exact prompts/completions, evidence traces, audits and SHA manifests so the comparison can be inspected.

**SW12 audited statistics:** 192 train + 32 dev + 64 sealed tasks; 160 train-only model rollouts; 1,276 learner states; 387 disagreement candidates; 400 selected learner states, of which **175** differ from the frozen model's action; 800 unique rows per arm; **452** identical prompt/completion pairs across the two realized arms (400 planned shared anchors plus 52 additional matches). Those numbers are from `ShadowWork_12_Closed_Loop_Evidence.zip`, not targets invented for this card.

**SW17:** When the corresponding trained-run archive is included, see `sw17/` for its separate **10-family, 240/40/80-task** distribution-shift evaluation and 800-row v4 training arms. SW17 is a follow-up within the same synthetic simulator family, *not* an external benchmark. Do not mix SW12 and SW17 held-out denominators.

## Files

| Directory | Purpose |
|---|---|
| `sw12/*_training.jsonl` | Exact two 800-row supervised training files (`prompt`, `completion`) |
| `sw12/{train,dev,sealed}_tasks.jsonl` | Precommitted synthetic task splits |
| `sw12/collection/` | Train-only frozen-learner rollouts |
| `sw12/evaluation/` | Held-out action traces, tool observations and outcomes |
| `sw12/selection_audit.json`, `precommit.json` | Label-selection details and split identities |
| `sw12/*_training_metadata.json` | Model-init provenance and optimization settings |
| `sw17/` | Published v4 training JSONLs, frozen splits, 160 train-only learner rollouts, 320 sealed evaluations, scores, paired tests and training metadata |
| `sha256_release_manifest.json` | Released-file checksums |

The original SW09 training and 70-task holdout evidence are published separately at [SW09 dataset](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training).

## Integrity and limitations

The SW12 training rows and split JSONLs are published byte-for-byte from the archived run. Relevant original SHA values appear in [the methodological audit](https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/docs/DATASET_METHOD.md). Labels are scripted and verified within this simulator, not independently human-vetted. Because tasks share generator rules, generalization to unseen real services is **not established**. Rehearsal v3 scored **47/64**, versus **46/64** for corrective v3 under the same SW12 model-centric evaluation: failure-specific examples did not demonstrate unique superiority.

**Intended usage:** Study learned self-healing and matched controls for stateful tool agents, test training/holdout leakage, and reproduce recorded simulator outcomes. Not intended as a certification of safe real-world autonomous writes.

**License:** CC BY-NC 4.0 for this curated research release, consistent with the noncommercial model family. Check the separately published checkpoint's own terms before using weights.

## Related references

- [Ross et al. (2011): Dataset Aggregation (DAgger)](https://proceedings.mlr.press/v15/ross11a.html), methodological inspiration only.
- [Gebru et al.: Datasheets for Datasets](https://arxiv.org/abs/1803.09010), documentation framework.
- [Hugging Face dataset cards](https://huggingface.co/docs/hub/en/datasets-cards), distribution documentation.

**Maintainer:** [ShadowWork-SHIFT GitHub](https://github.com/githubshaurya/ShadowWork-SHIFT). Dataset and model artifacts are published independently from the codebase.
