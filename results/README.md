# Verified result summaries

These are **verified transcriptions from archived CSV and JSON artifacts**, not estimates. Exact SW12/SW17 training, scored traces and supporting files have now been **published in the [public Hugging Face dataset](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets)**. The [release verification ledger](../docs/PUBLIC_RELEASE_VERIFICATION.md) records independent file and hash checks.

## SW09 70-task final holdout

Source: `ShadowWork_09_Final_Holdout_Evidence.zip` (210 scored JSONs).

| policy | n | strict | state_correct | evidence_supported | unsafe_proposals | executed_unsafe |
|---|---:|---:|---:|---:|---:|---:|
| parent_v2 | 70 | 42 | 70 | 65 | 1 | 0 |
| parent_v2_early_finish_controller | 70 | 69 | 70 | 70 | 1 | 0 |
| learner_corrective | 70 | 70 | 70 | 70 | 0 | 0 |

## SW12 sealed shifted-protocol, 64 tasks, model-only/fixed baseline

Source: `ShadowWork_12_Closed_Loop_Evidence.zip/grouped_summary.csv`.

| policy | one_check (n=32) | two_check (n=32) | total_strict |
|---|---:|---:|---:|
| frozen_corrective | 22 | 2 | 24 |
| learner_corrective_v3 | 31 | 15 | 46 |
| rehearsal_v3 | 31 | 16 | 47 |

## SW14 128 fresh tasks (same models, controller change)

Source: `ShadowWork_14_Controller_Repair_Results1.zip/summary.csv`.

| policy | no_controller | conservative_v2 |
|---|---:|---:|
| learner_corrective_v3 | 117/128 | 119/128 |
| rehearsal_v3 | 103/128 | 114/128 |

## SW15 cross-protocol tasks

Source: `ShadowWork_15_Cross_Protocol_Recovery_Results.zip/summary.csv`.

| suite | policy | baseline controller | targeted_v3 controller |
|---|---|---:|---:|
| SW09 new, 70 | corrective v3 | 47/70 | 70/70 |
| SW09 new, 70 | rehearsal v3 | 58/70 | 70/70 |
| SW12 new, 80 | corrective v3 | conservative_v2 55/80 | 62/80 |
| SW12 new, 80 | rehearsal v3 | conservative_v2 61/80 | 68/80 |

**Gate:** SW15 deployment_decision.txt = HOLD, below 90% on SW12 new.

## SW16 identical unified_v4 controller, 160 SW12 tasks

Source: `ShadowWork_16_Unified_Recovery_Results.zip/summary.csv`.

| model | SW12 core n=96 | SW12 composed n=64 | combined |
|---|---:|---:|---:|
| original_corrective | 80 | 52 | 132/160 |
| learner_corrective_v3 | 94 | 60 | 154/160 |
| rehearsal_v3 | 96 | 64 | 160/160 |

**Runtime controller ablation, same models:**

| model | core targeted_v3→unified_v4 | composed targeted_v3→unified_v4 |
|---|---|---|
| corrective_v3 | 59→94/96 | 35→60/64 |
| rehearsal_v3 | 82→96/96 | 46→64/64 |

**SW09 retention under unified_v4:** corrective v3 56/56; rehearsal v3 56/56; original corrective 45/56.

**Gate:** SW16 deployment_decision.txt = HOLD due to one corrective-v3 composed-state regression.

## SW16 budgeted_v5 focused regression

Source: `ShadowWork_16_Budget_Regression_Results.zip/paired_summary.csv` and `decision.txt`.

| model | SW12 core strict | SW12 composed strict | combined strict | combined state_correct |
|---|---:|---:|---:|---:|
| corrective_v3 | 95/96 | 61/64 | 156/160 | 160/160 |
| rehearsal_v3 | 96/96 | 64/64 | 160/160 | 160/160 |
| **sum** | **191/192** | **125/128** | **316/320** | **320/320** |

**Against unified_v4:** 2 strict wins and 0 strict losses in 320 paired cases; 9/320 invocations of the new bounded retry; 0 raw unsafe model proposals and 0 forbidden executed mutations. Improvements of one case per corrective-v3 suite are not statistically significant (each two-sided exact McNemar `p=1.0`). Decision: `PASS_FOCUSED_ENGINEERING_REGRESSION`, *not* unrestricted deployment approval.

## Interpretation rule

**Never label 316/320 as 316 independent tasks.** They are 320 model-task evaluation episodes, comprising two trained model arms applied to the same 160 task instances. Similarly, never combine SW09, SW12, SW15 and SW16 results as independent samples without accounting for repeated task families and evaluation reuse.

## SW17 fixed-controller sealed learning attribution (80 distinct synthetic tasks)

Source: the [public original SW17 scorecards and 320 per-task evaluated trajectories](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets/tree/main/sw17), independently checked against the exact Project evidence ZIP and its 496 SHA-256 commitments. All three primary policies use identical four-read bootstrap and no post-bootstrap recovery controller.

| Policy | Strict /80 | Persisted-state correct /80 | Evidence supported /80 | Unsafe proposals | Mean tool steps | Mean model calls |
|---|---:|---:|---:|---:|---:|---:|
| frozen_sw09 | 31 | 58 | 54 | 6 | 11.7750 | 7.7750 |
| corrective_v4 | **65** | 77 | 73 | **8** | 14.4375 | 10.4375 |
| rehearsal_v4 | **65** | 80 | 77 | **8** | 12.0875 | 8.0875 |
| previous_rehearsal_v3 (optional) | 57 | 75 | 60 | 2 | 11.8750 | 7.8750 |

Paired exact McNemar: corrective_v4 vs frozen_sw09 **38 wins / 4 losses, p=5.653146e-8**; rehearsal_v4 vs frozen_sw09 **36 / 2, p=5.398761e-9**; corrective_v4 vs rehearsal_v4 **5 / 5, p=1.0**; corrective_v4 vs previous_rehearsal_v3 **19 / 11, p=0.2004884**. Do not use these significance values to infer independent generalization across task families.

**Authorization counterexample:** `injected_forbidden` has **0/8 strict successes and 8 unsafe mutation proposals in each v4 arm**, compared with **2/8 strict and 6 proposals** in frozen SW09 and **6/8 strict and 2 proposals** in previous rehearsal v3. These are *attempted unsafe tool proposals*, which the simulator blocks, rather than confirmed unsafe executed state changes. The evaluated v4 agents are **NOT approved for unattended deployment**. The notebook's narrow learning gate `PASS_LEARNING_BUT_NOT_CORRECTIVE_SUPERIORITY` must be accompanied by its `deploy=false` decision and this safety HOLD. Under the SW17 40 unseen-field tasks: corrective 31/40, rehearsal v4 36/40, frozen SW09 18/40, previous rehearsal v3 40/40; performance is not monotonic across every subgroup.

**Training-effect conclusion:** **+42.5 percentage points** from 31/80 to 65/80 with an unchanged four-read bootstrap and no extra post-read controller. Both trained curricula achieve 65/80, supporting **model learning** without a special-curriculum superiority claim. Exact source methodology: [dataset construction](../docs/DATASET_METHOD.md); full inference: [technical report](../docs/TECHNICAL_REPORT.md).
