# ShadowWork-SHIFT | Dataset construction and provenance

**Scope:** LEXSI Track 3, Problem 8, self-healing tool agents. **Dataset type:** entirely synthetic, English-language, stateful configuration-maintenance workflows with executable SQLite state and fault injection. **Origin:** experiment-specific generators, frozen learner rollouts, and scripted reference continuations, not scraped production tickets and not independently human-annotated data.

## 1. Motivation and what constitutes an example

The training examples teach one next tool action given a maintenance request, the four initial tool observations, and the sequence of tool calls/results. The objective is to train an agent to detect unsuccessful or unsafe state transitions, recover without unsafe mutation, and stop only after sufficient read-back evidence. Distinct fault classes include transient write conflicts, silently ignored writes, stale state reads, false-positive commit acknowledgments, wrong writes, injection-like untrusted notes, authorization denial, approval-policy edge cases, and expired write leases.

A **training row** is `{"prompt": "...", "completion": "[{...}]"}`. It is a **single action-label pair**, not a standalone full human dialogue or an independent task. Many rows can originate from the same generated task or rollout. Each **task** has a request, initial value, intended value, authorization conditions, required verification count, and deterministic fault schedule. A **rollout** is an actual frozen model's tool-action trajectory executed in the simulator. A **label** is the next action selected by an executable scripted reference continuation.

The original SW09 data and 70-task final holdout are already in the public [SW09 dataset](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training). SW12 and SW17 are newer, related experiments; do not combine their test cohorts into a single independent benchmark.

## 2. Task design and provenance

| Contract | SW12 | SW17 |
|---|---:|---:|
| Generator seed | `20261113` | `20261115` |
| Train tasks | 192 (8 groups × 24) | 240 (10 groups × 24) |
| Development tasks | 32 (8 × 4) | 40 (10 × 4) |
| Sealed test tasks | 64 (8 × 8) | 80 (10 × 8) |
| Train-only learner rollouts | 160 (20 per group) | 160 (16 per group) |
| Per-arm supervised examples | 800 | 800 |
| Common expert examples per arm | 400 | 400 |
| Curriculum-specific examples per arm | 400 | 400 |
| Max tool actions | 22 | 24 |
| Verification protocols | One and two post-write checks | One and two post-write checks |
| Shared starting policy | Original SW09 corrective LoRA | Original SW09 corrective LoRA |

SW12 groups are `normal`, `double_conflict`, `double_noop`, `wrong_then_stale`, `two_stale`, `false_positive`, `injected_forbidden`, and `injected_authorized`. SW17 adds `approval_not_required` and `lease_expired`. Both model protocol variants within every group. Fault behavior is implemented by an executable `RecoveryEnvironment` that stores persisted configuration values in SQLite and returns tool results that can differ from durable state.

SW17 further changes service names, region names, request phrasing, and includes three previously unseen configuration fields in part of the sealed test cohort. This is **shift within a related synthetic workflow family**, not generalization to independently authored real production systems. The [executed and audited SW17 data-construction account](DATASET_METHOD.md#executed-sw17-dataset-construction-and-quantitative-audit) records **160 train-only rollouts → 1,311 learner states → 859 mismatch candidates → 400 selected learner-state rows (211 actual action corrections)**, 395/400 exact matched-control strata, a concrete recorded example, and immutable source hashes.

## 3. Generation pipeline

1. **Programmatic scenario generation.** Construct tasks from explicit value domains, typed fields, authorization and approval states, a bounded canary-error policy, failure groups and one-/two-check protocol flags. Generate separate train/development/sealed identities using fixed seeds. The outputs `train_tasks.jsonl`, `dev_tasks.jsonl`, `sealed_tasks.jsonl`, `precommit.json` and their SHA-256 values are recorded before model evaluation.
2. **Executable reference policy.** A rule-based next-action policy consumes structured tool observations such as ticket, runbook, health, approval, lease and committed-state checks, rather than using a separate language model judge. Its continuation is run against the SQLite environment and must achieve the defined strict-success condition on every generated task in the reference-solvability check. This is a **scripted reference**, not an externally certified optimal policy.
3. **Frozen learner-state collection.** Run the fixed original SW09 corrective model on **training-only** task IDs. Save the learner's actions, tool outputs, scores and identity hashes per episode. SW12 and SW17 each stratify 160 rollouts by group before sampling.
4. **Corrective label construction.** Replay each saved learner action through the same environment. At learner-visited states after the four scripted initial reads, ask the reference policy for the next action. Mark `correction=true` when the learner's original proposal differs from the reference. The teacher targets are **model-output-conditioned, programmatically validated labels**, not human ratings.
5. **Length and coverage filtering.** Remove examples exceeding the SFT token budget; select a mixture across fault group, verification count and next-action category, giving priority to actual learner/reference mismatches. Confirm coverage of all relevant groups and both verification protocols; verify prompt uniqueness for selected corrective rows.
6. **Matched counterfactual training sets.** Both arms contain 400 identical reference-policy rows. In the remaining 400, the corrective arm uses learner-visited states labeled by the reference. Rehearsal uses ordinary reference-policy states that do not require a learner mistake. SW12's rehearsal extras are the next 400 shuffled expert rows; SW17 more carefully tries to match each selected corrective row by group, protocol and next-action category, falling back to coarser matches when needed. The actual exact-matching count is recorded in SW17's `selection_audit.json`.
7. **Frozen, equal-budget optimization.** Each arm starts from the exact same SW09 corrective adapter on the same custom Tiny Aya-derived full checkpoint. Both use 800 rows, 80 optimizer steps, learning rate `5e-5`, effective global batch size 8, and the same frozen per-experiment evaluation conditions. SW17's T4 training implementation uses explicit completion-only labels, 4-bit frozen base/FP16 compute and FP32 LoRA parameters; its earlier software-workaround history does not change the experimental intent.

## 4. Verification and leakage boundaries

- **Persistent state, not acknowledgment alone:** completion requires authorized final values in SQLite plus required post-write matching checks; an apparent successful commit can be a silent no-op or false positive.
- **Forbidden actions:** authorization and argument-schema gates reject disallowed operations, and attempted unsafe mutations are logged separately from executed mutations.
- **Reference replay:** generated tasks must be solvable by the scripted reference under the action budget; learner rollout histories are replayed and checked against their originally saved tool results.
- **Sealed split commitment:** split SHA-256 digests and the `precommit.json` are saved before evaluation; existing files are compared and rejected if changed rather than silently regenerated.
- **No training on sealed rows:** training construction references only `train_tasks`, training-only learner rollouts, and the training-split reference states; development and sealed IDs are disjoint.
- **Paired scoring:** compare models on identical task IDs, a common fixed controller and common simulator. Report strict task success, persisted-state correctness, authorization proposals, model calls, token counts, and paired win/loss statistics where recorded.
- **Source file hashes:** each arm's `*_training_metadata.json` records the SHA-256 of its exact JSONL training file. `selection_audit.json` records selected correction counts, distributions and hashes; `final_provenance.json` and episode-level JSON permit follow-up audit.

The checks above are **code-level controls**, not proof that the scripted teacher is optimal or that the synthetic task families fully represent production reality. They are also not independent assessments by outside annotators.

## 5. Published fields and interpretation

**Task JSONL** includes `id`, `split`, `group`, `key`, `old`, `target`, `service`, `region`, `request`, `authorized`, `approved`, `requires_approval`, `canary_errors`, `max_canary_errors`, `allowed`, `checks_required`.

**Training JSONL** has `prompt` and `completion`. The prompt contains the tool-use rules, task and available action/result history; the completion is a JSON array containing exactly one structured tool action.

**Collection episode JSON** preserves frozen-model histories, generated action strings, source adapter hash and outcome. **Evaluation episode JSON** preserves task IDs, group, verification protocol, executed actions and tool results, final stored values, strict score, AuditKIT verdict and resource-use counters.

**Do not confuse:** 800 rows with 800 independent tasks; successful scripted reference rollout with independent ground-truth certification; simulator read-back with a real production database; or multiple model-task evaluations with that many distinct benchmark tasks.

## 6. Evaluation outcome and failure transparency (SW17)

On the **80-case precommitted SW17 sealed suite**, original frozen corrective achieved **31/80** strict success, learner-state corrective v4 **65/80**, equal-budget rehearsal v4 **65/80**, and an additional older rehearsal v3 **57/80**. Corrective versus frozen had **38 paired wins and 4 losses** (exact McNemar `p=5.653146e-8`); corrective versus rehearsal v4 had **5 wins and 5 losses** (`p=1.0`). Thus the clear result is learned adaptation, not superiority of this particular corrective curriculum.

The **eight `injected_forbidden` scenarios are a decisive failure category**: corrective v4 and rehearsal v4 both generated unsafe mutation proposals on all eight cases and scored zero strict successes. The synthetic runtime **blocked** those proposals; they are not evidence of executed forbidden writes. The original frozen model attempted six unsafe proposals, while a previous rehearsal v3 policy attempted two. Therefore **the learner improvements must not be interpreted as improving authorization safety**, and the deployment recommendation remains **HOLD**. These counterexamples are retained in the public task IDs and scored episode traces rather than excluded or silently repaired.

Publication must include the complete `policy_summary.csv`, `group_summary.csv`, `unseen_schema_summary.csv`, `paired_tests.csv`, `learning_gate.json`, both arm training hashes, and all available SW17 sealed episode traces so others can independently verify the result and its negative safety finding.

## 7. Licenses, suitability and limitations

The scenarios are synthetic, not derived from identifiable human subjects or confidential production logs. The public datasets are intended for controlled research/demos on stateful tool-use, failure detection and recovery. They do not contain evidence of safe performance on real business infrastructure and should not be used as a standalone safety certification for tool agents. The creator's chosen bundle license is **CC BY-NC 4.0**, and users must additionally observe applicable model and software licenses. Synthetic status does not eliminate the possibility of methodological bias.

**Main limitations:** only two closely related simulator families; hand-scripted fault distributions and reference policy; limited independently authored adversarial conditions; no external human labeling or adjudication; limited held-out tasks per group; possible lexical correlations; repeated test-family iteration across notebooks; protocol assumptions embedded in the synthetic environment.

## 8. Reproduce and audit

Source notebooks:
- [SW12 closed-loop dataset/training/evaluation](../notebooks/SW12_Closed_Loop_Adaptation.ipynb), especially the task generator and matched-data construction cells.
- [SW17 fixed-controller learning attribution](../notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb), especially the frozen task split, real learner rollouts, and training-row selection cells.
- [SW17 one-cell frozen evaluation](../notebooks/SW17_SINGLE_CELL_EVALUATION_AFTER_RESTART.ipynb).

Public dataset locations:
- SW09 existing dataset: https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training
- SW12–SW17 published dataset: https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets

**Publication verification complete:** the second Hugging Face repository publicly contains both SW12 and SW17 training JSONLs, precommitted splits, train-only learner rollouts, evaluated agent episodes and SHA-256 manifest. The completed Kaggle publisher confirmed anonymous file and collection access; see [release verification](PUBLIC_RELEASE_VERIFICATION.md).

## 9. Documentation conventions

This dataset is documented using the motivation, composition, collection process, preprocessing, intended use and limitation structure advocated by **Gebru et al., _Datasheets for Datasets_ (2021)** and Hugging Face's official [dataset card guidance](https://huggingface.co/docs/hub/datasets-cards). This is a documentation framework, **not** an endorsement or independent validation of our dataset by those authors.
