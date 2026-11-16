# SW17: fixed-controller training attribution, sealed 80-task evaluation

**Source status:** Numbers were supplied directly from the completed Kaggle SW17 scorecard output on 16 November 2026. The exact source notebook and split commitments are available in the repository. Independently verifying the 320 per-policy episode records and the ZIP archive is **pending** receipt/publication of the Kaggle output files. Do not imply this Markdown alone replaces those artifacts.

## Design

All arms share the exact custom Tiny Aya-derived Plain SFT base, agent tool schema, test set, and **four scripted initial reads only**, without a post-read rule-based recovery/stopping controller. Both new v4 adapters were trained from the same frozen SW09 learner-corrective adapter. Each v4 arm uses 800 rows (400 shared expert anchors + 400 differentiated examples), 80 optimizer steps, global batch 8, LR 5e-5 and identical training code. Corrective rows are learner-visited reference labels; rehearsal rows are ordinary reference-policy training states. Evaluation cases are from the same *synthetic* simulator family, with schema/service/region/prompt shifts. These are not an independent external benchmark.

## Sealed outcomes

| Policy | Strict /80 | Final state correct /80 | Evidence supported /80 | Unsafe proposals | Blocked proposals | Mean steps | Mean model calls |
|---|---:|---:|---:|---:|---:|---:|---:|
| Frozen SW09 corrective | 31 | 58 | 54 | 6 | 54 | 11.7750 | 7.7750 |
| Corrective v4 | **65** | 77 | 73 | **8** | 36 | 14.4375 | 10.4375 |
| Rehearsal v4 | **65** | **80** | **77** | **8** | 19 | 12.0875 | 8.0875 |
| Previous rehearsal v3 | 57 | 75 | 60 | 2 | 48 | 11.8750 | 7.8750 |

**Learning attribution:** Corrective v4 improves 31→65/80 (+34 strict successes, +42.5 percentage points) over the original frozen policy under identical inference controls. Rehearsal v4 also improves 31→65/80. On exact paired cases: corrective vs frozen 38 wins / 4 losses, exact two-sided McNemar p≈5.65e−8; rehearsal vs frozen 36 wins / 2 losses, p≈5.40e−9. These support improvement from *additional supervised fine-tuning*, but **not superiority of corrective-state labels over matched rehearsal**.

**Curriculum contrast:** Corrective vs rehearsal v4 has 5 paired wins / 5 losses, exact McNemar p=1.0. A difference in training loss does not establish better agent behavior.

**Safety blocker:** Under `injected_forbidden` (8 tasks), corrective v4 and rehearsal v4 each score 0/8 strict success, with **eight unsafe model proposals apiece**. These are rejected by the test harness; do not describe them as safe autonomous policies. Previous rehearsal v3 scores 6/8 with two unsafe proposals. Before real deployment, mitigate the unauthorized-action proposal rate. Note that zero executed forbidden mutations (if independently verified) does not erase the unsafe policy proposals.

**Resource tradeoff:** On average, corrective v4 needs 14.44 steps and 10.44 model calls, versus rehearsal v4's 12.09 steps and 8.09 model calls; their strict success is identical. Corrective v4 retains an interesting directional advantage on the 40 old-field tasks (34/40 vs rehearsal 29/40) but trails on the 40 unseen-field tasks (31/40 vs rehearsal 36/40). These subgroup comparisons are small, and these different task strata do not establish causal explanations.

**Decision:** Existing SW17 gate = `PASS_LEARNING_BUT_NOT_CORRECTIVE_SUPERIORITY`. `external_generalization_established=False`, `deploy=False`. This is evidence for the hackathon learning requirement, not permission to deploy the trained policy without a runtime authorization gate.

## Historical context (separate dataset)

SW12 sealed shifted protocol: frozen original 24/64; corrective v3 46/64; rehearsal v3 47/64. These numbers use another held-out case set and **must not be pooled** with SW17 without accounting for dependence.

## Data lineage and release

See [dataset generation process](DATASET_METHOD.md), exact [source notebook](../notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb), [final Hugging Face publisher](../notebooks/FINAL_HF_Publish_From_Kaggle.ipynb) and [canonical Hugging Face dataset card](../datasets/HF_DATASET_CARD.md). The public data release must contain actual 800-row JSONL files, selection audit, original split files and hashes, learner rollout traces, model training metadata, and per-episode scored evaluation records. **Do not claim those files are public until independently verified on the Hub.**
