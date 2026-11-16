---
license: cc-by-nc-4.0
language:
  - en
pretty_name: ShadowWork-SHIFT Self-Healing Tool-Agent Training and Audited Traces
tags:
  - agents
  - tool-use
  - synthetic
  - evaluation
  - agenttune
  - auditkit
  - self-healing
  - lexsi
---

# ShadowWork-SHIFT | Synthetic self-healing agent dataset

**Provenance:** Deterministically generated synthetic stateful-maintenance tasks; actual learner rollouts on train-only cases; observation-conditioned, scripted reference continuations; matched rehearsal controls; executable SQLite replay and SHA-256 split/row commitments. **No human-expert annotation, production incident collection or independent external benchmark is claimed.**

**Published data:** `i-am-shaurya05/shadowwork-shift-datasets` (SW12/SW17 training rows, committed splits, learner rollouts and evaluation episodes). See the original SW09 source data in [shadowwork-shift-evidence-and-training](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training).

## Why the dataset was created

Stateful tool agents can receive successful write receipts without persisted changes, observe stale reads, miss mandatory verification checks, or attempt unauthorized mutations. These records support controlled before/after studies of whether training on *states the agent actually visits* improves its one-action decisions beyond ordinary expert demonstration rehearsal, under the same recovery controller.

## How the data was created

1. A scripted task generator samples field/value changes, permission and approval states, health gates, verification protocols, and predefined fault schedules.
2. Tasks are split by ID into train, development and sealed test cohorts using fixed random seeds; exact JSONL split hashes are committed before evaluation.
3. A rule-based reference policy uses observed ticket/runbook/health/approval/lease/tool outputs, proposes the next tool action, and is tested by executing each reference trajectory against persisted SQLite state.
4. The **frozen original SW09 corrective agent** is run on train-only tasks; its actual action/result histories are recorded without access to test labels.
5. Each learner-visited prompt receives a reference-policy next-action label. Proposed-action/reference disagreement is logged and used to prioritize actual corrections.
6. Two **matched 800-row datasets** are built per experiment. Each arm shares 400 expert-anchor rows; the remaining 400 are learner-visited corrective examples or ordinary expert-state rehearsal examples. SW17 additionally matches rehearsal examples on fault category, one-/two-check protocol and action class when available.
7. Tool histories are replayed and checked for consistency, examples are token-budget-filtered, and finalized JSONL files are hashed. Neither the script nor the release claims human annotation.

## Dataset composition

| Content | SW12 | SW17 |
|---|---:|---:|
| Training tasks | 192 | 240 |
| Development tasks | 32 | 40 |
| Sealed task instances | 64 | 80 |
| Frozen learner rollouts from train-only tasks | 160 | 160 |
| Training examples per curriculum | 800 | 800 |
| Shared expert anchors per curriculum | 400 | 400 |
| Specialized examples per curriculum | 400 | 400 |

SW12 contains eight fault families (`normal`, `double_conflict`, `double_noop`, `wrong_then_stale`, `two_stale`, `false_positive`, `injected_forbidden`, `injected_authorized`). SW17 adds `approval_not_required` and `lease_expired`, plus unseen field names and changed service/region wording in the sealed split. One- and two-check protocols are both represented.

## File guide

- `sw12/train_tasks.jsonl`, `dev_tasks.jsonl`, `sealed_tasks.jsonl`: synthetic task parameters and original split identities.
- `sw12/learner_corrective_v3_training.jsonl`, `rehearsal_v3_training.jsonl`: exact matched v3 training rows.
- `sw12/selection_audit.json`, `precommit.json`, `*_training_metadata.json`: data construction counts, hashes and frozen settings.
- `sw12/evaluation/`: recorded, task-level evaluation runs with actions, observations and scores.
- `sw17/train_tasks.jsonl`, `dev_tasks.jsonl`, `sealed_tasks.jsonl`: the later, separate shifted task generator and frozen split.
- `sw17/learner_corrective_v4_training.jsonl`, `rehearsal_v4_training.jsonl`: exact matched v4 training rows.
- `sw17/selection_audit.json`, `precommit.json`, `*_training_metadata.json`: training provenance.
- `sw17/collection/` and `sw17/evaluation/`: train-only learner rollouts and sealed evaluation traces.
- `archived_evidence/`: selected SW09/SW13–SW16 original archives when supplied at publishing time.

**Availability:** core SW12 and SW17 dataset files are now uploaded and anonymously accessible; older optional SW13–SW16 source archives remain separately retained as historical supplements. See [public verification ledger](PUBLIC_RELEASE_VERIFICATION.md).

## Training and evaluation

Both v3 and v4 comparisons use the **same frozen SW09 corrective LoRA starting point**, matched optimizer budget (80 steps, 800 rows/arm, effective batch 8, learning rate `5e-5`), and a shared controller **within each comparison**. The model base is a specific, public Tiny Aya-derived full checkpoint; it is not interchangeable with upstream Tiny Aya weights.

**Previously established SW12 sealed 64-task result before the final unified controller:** frozen original 24/64, corrective v3 46/64, rehearsal v3 47/64 strict successes. This demonstrates model-adaptation gains but not corrective-curriculum superiority. SW17 results must be reported separately after their complete scored evaluation, not filled in from training loss.

## SW17 measured outcome and safety release gate

The completed **80-task SW17 sealed suite** uses the same four-read bootstrap, no additional repair controller, and the same task cases for every policy:

| Policy | Strict success | Correct final SQLite state | Unsafe tool-mutation proposals |
|---|---:|---:|---:|
| Frozen original corrective | 31/80 | 58/80 | 6 |
| Corrective v4 | **65/80** | 77/80 | **8** |
| Matched rehearsal v4 | **65/80** | 80/80 | **8** |
| Previous rehearsal v3 (supplementary) | 57/80 | 75/80 | 2 |

Continued training increased corrective strict success by **42.5 percentage points** relative to its frozen starting policy (paired 38 wins / 4 losses; exact McNemar `p=5.653146e-8`), but **corrective training did not outperform ordinary matched rehearsal** (5 wins / 5 losses, `p=1`). This is training improvement, not evidence of superior corrective-data curation.

**Safety warning:** Both v4 arms generated **eight unsafe mutation proposals across eight `injected_forbidden` tasks** (0/8 strict success per arm). The simulated safety gate blocked unauthorized execution, but the attempted actions show that trained policies are **not authorized for autonomous deployment**. The experiment's learning-evidence gate `PASS_LEARNING_BUT_NOT_CORRECTIVE_SUPERIORITY` is distinct from the recorded **`deploy=false`** decision. Do not describe this as universal safety, successful adversarial robustness or production readiness.

The sealed SW17 dataset changes field/service/region terminology but is not an independent external benchmark; do not pool its 80 task cases with historical tests as independent replications.

## Quality checks

All reference tasks must terminate with correct persisted-state/evidence outcomes within the episode budget. Training-only learner histories are replayed against the same simulator; candidate action/reference mismatches, coverage, token-budget filtering, deduplication and matched-row counts are logged. Evaluation uses action/result traces, SQLite state, AuditKIT recorded checks and paired strict-success statistics. Original split files and training JSONLs have SHA-256 integrity commitments.

**Limitations:** fully synthetic, author-scripted reference labels, two related protocol environments, limited adversarial and external coverage. These data do **not** establish safe deployment or real-world recovery efficacy. A shared simulator's successful reference policy is not proof of independent correctness, and 800 action rows are not 800 independent tasks.

## Use and license

For **non-commercial research, hackathon evaluation and reproducible controlled tool-agent recovery studies** under CC BY-NC 4.0 and the applicable upstream model/tool terms. Do not treat any simulated results as operational safety guarantees.

**Complete, auditable methodology and source:** [GitHub dataset construction and provenance](https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/docs/DATASET_CONSTRUCTION.md), [SW12 notebook](https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/notebooks/SW12_Closed_Loop_Adaptation.ipynb), [SW17 notebook](https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb).

Documentation design follows the transparency prompts in Gebru et al., *Datasheets for Datasets* (2021), and [Hugging Face dataset card guidance](https://huggingface.co/docs/hub/datasets-cards). This does not imply external review or endorsement.
