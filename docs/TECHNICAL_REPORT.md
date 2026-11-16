# Technical report: ShadowWork-SHIFT

**LEXSI AI Safety & Alignment Hackathon — Track 3, Problem 8 (Self-healing agents)**  
*Evidence freeze: artifacts generated November 2026.*

## Abstract

Stateful tool-using agents can fail despite syntactically valid actions: an acknowledged write may not persist, an observed state may be stale, the agent may terminate before collecting enough verification evidence, or a mutation may be unauthorized. ShadowWork-SHIFT investigates a self-healing pipeline for these failures using a Cohere Tiny Aya-derived tool policy, AgentTune tool execution and harnessing, AuditKIT recorded evaluation, learner-state corrective fine-tuning with TRL/PEFT LoRA, and conservative observation-grounded runtime controllers. Frozen and adapted policies are compared on matched synthetic workflows, with strict success requiring authorized and verified completion rather than merely a plausible final answer. On an SW09 sealed 70-task holdout, the original parent adapter scored 42/70 strict and a corrective adapter 70/70; importantly, a simple parent-plus-early-finish controller already scored 69/70. On a distinct SW12 shifted-protocol sealed 64-task evaluation, the original corrective adapter scored 24/64, corrective v3 scored 46/64, and compute/data-matched rehearsal v3 scored 47/64 without the final unified controller. With a common SW16 unified controller, original corrective, corrective v3, and rehearsal v3 scored 132/160, 154/160, and 160/160, respectively, on 160 SW12 core/composed tasks. A focused budgeted repair increased corrective v3 to 156/160 with no paired losses, without statistical significance for the two newly fixed cases. Results support effective self-healing *as an end-to-end engineered pipeline* and measurable adaptation benefits, but do not establish a unique advantage for failure-specific labels over rehearsal or transfer to external production environments.


**Final fixed-controller SW17 update:** corrective v4 and matched rehearsal v4 both reached **65/80 strict** versus **31/80** for the frozen starting policy on a new 80-task sealed synthetic suite, showing a 42.5-point training-associated improvement without corrective-curriculum superiority. Both v4 arms nevertheless proposed an unsafe mutation on **the eight authorization-forbidden task cases, with eight total unsafe proposals per v4 arm**; the tool gate blocked execution. This is a safety **HOLD**, not a deployment pass.
## 1. Problem and hypothesis

**Failure model.** The agent runs an authorized state transition in a gated workflow. Correctness is not determined by whether a tool returns an acknowledgment; it depends on the durable state and the evidence supporting termination. Failure families include:
- lease or approval mistakes; invalid/forbidden mutation attempts;
- silently ignored writes, wrong-value writes, conflicts or delayed commit effects;
- stale observations and misleading success acknowledgments;
- under-verification, unsupported finish decisions and exhausted action budgets;
- combinations of two faults in a run, including prompt-injection-like tool-observation text.

**Research question.** Can a small post-trained tool agent, coupled with a measured and state-aware recovery controller, safely finish more stateful tasks after failure? Specifically, can corrective training on learner-visited failures outperform a matched rehearsal control?

The answer is **partially positive**: the full pipeline and trained policies improve; corrective training has **not** consistently beaten rehearsal.

## 2. Stack and experiment boundary

- **Model:** Cohere Tiny Aya-derived custom Plain SFT checkpoint, followed by Oracle BC v2 LoRA, SW09 learner-corrective and rehearsal adapters, and SW12 v3 corrective/rehearsal continuations. The exact original custom base was loaded from `/kaggle/input/datasets/shaurya466/shift-plain/shadowork_123`; a generic upstream Tiny Aya checkpoint is *not* equivalent.
- **AgentTune:** Agent execution, ReActStrategy, DictToolHarness, Project/trajectory machinery and deployment-related evaluation where used. AgentTune is **not** credited for optimizing LoRA weights unless the notebook explicitly delegates the operation to it.
- **AuditKIT:** Recorded, state-checked episode scoring and failure diagnostics. Strict success is grounded in tool observations and persisted state, not in an independent LLM judge.
- **Optimization:** Hugging Face Transformers, PEFT, TRL and Accelerate; matched LoRA training arms are initialized from the same checkpoint. SW09 has 140 training workflows and matched learner-state versus on-policy data; SW12 uses 800 training rows per v3 arm over 80 optimization steps, learning rate 5e-5, global batch 8.
- **Controller:** A deterministic observation-driven recovery layer for stage/commit/check/finish, authorization, check-count evidence, and bounded retries. Later revisions v3 targeted, v4 unified and v5 budgeted are **not** model checkpoints.
- **Fault simulators:** SW09 authorization-gated protocol and SW12 SQLite-based shifted protocol. Shared schemas limit claims of independent generalization.

## 3. Evaluation definitions

**Strict task success:** correct allowed/refused decision, correct persistent state, sufficient final verification evidence, and appropriate task termination. **State correctness** measures the final persisted database state independently from strict completion. **Evidence support** measures whether the agent gathered the required checks before declaring completion. **Unsafe proposals** are raw model actions, including those blocked before execution; **executed forbidden mutations** count persisted unauthorized effects. These quantities must not be conflated.

Runs are paired by task IDs, fault settings, and controller configurations wherever the comparisons are described as matched. Action budgets and available tool schemas remain part of the evaluation specification.

## 4. Training and sealed SW09 result

The original SW09 learner-state training protocol:
1. Freeze Oracle BC v2 parent and 70-case sealed final holdout.
2. Collect actual parent rollouts on **140 train-only tasks** across seven conditions.
3. Replay learner-visited states and construct candidate corrective labels with a scripted reference continuation. The reference verifier is not a proof of globally optimal continuation.
4. Continue two adapters under matched optimization budgets, one with learner-state verified correction and the control with ordinary/on-policy rehearsal.
5. Evaluate selected policies on development tasks, then score the held-out 70 tasks under their published commitments.

SW09 final 70-task holdout, directly computed from the 210 episode JSONs in `ShadowWork_09_Final_Holdout_Evidence.zip`:

| Policy | Strict | Persisted-state correct | Unsafe raw proposals | Executed unsafe |
|---|---:|---:|---:|---:|
| Oracle BC v2 parent | 42/70 | 70/70 | 1 | 0 |
| Parent + early-finish controller | 69/70 | 70/70 | 1 | 0 |
| Learner-state corrective adapter | **70/70** | 70/70 | 0 | 0 |

The unexpectedly strong parent+controller row is a central control, not an inconvenient detail to hide.

## 5. SW12 shifted-protocol corrective vs rehearsal

SW12 introduces multi-check requirements and a more complex SQLite fault family. Training starts from the **frozen original SW09 learner-corrective adapter**. Both v3 arms share the old-anchor examples and matched row counts, compute, step count and initialization. The corrective arm trains on learner-visited corrections; the rehearsal arm receives ordinary expert/rehearsal alternatives.

On **64 sealed SW12 tasks without the final unified controller**:

| Policy | One-check (32) | Two-check (32) | All 64 |
|---|---:|---:|---:|
| Frozen original corrective | 22 | 2 | 24 |
| Corrective v3 | 31 | 15 | 46 |
| Matched rehearsal v3 | 31 | 16 | **47** |

The v3 training improvements are meaningful, but the two curricula are not separated in the corrective arm's favor. A dataset audit also showed blind spots in training coverage: no examples of certain **authorized but `approved=false`, `requires_approval=false`** states, and limited lease-expiry exposure. This constrains inference about a generalized self-healing learner.

## 6. Runtime controller ablations and cross-protocol recovery

**SW14 fresh SW12 tasks, 128 tasks per condition:** Conservative verification controller improves corrective v3 117→119/128 and rehearsal v3 103→114/128, while both maintain 128/128 correct state. The gains are controller attributable and must not be counted as LoRA training gains.

**SW15 new cross-protocol tasks:** Targeted v3 controller restores 70/70 SW09 retention for both v3 arms. On 80 SW12 tasks, corrected v3 is 62/80 strict, rehearsal v3 is 68/80 under the same targeted controller. The local deployment gate remains HOLD due to shifted-protocol success rates below 90%. SW15 is still within related simulators; this is not external production transfer.

## 7. SW16 unified controller and corrective attribution

On 160 SW12 core/composed task instances, use the same unified_v4 controller for each model:

| Model, fixed unified_v4 | Core 96 | Composed 64 | Total strict |
|---|---:|---:|---:|
| Original SW09 corrective | 80 | 52 | 132/160 (82.50%) |
| Corrective v3 | 94 | 60 | 154/160 (96.25%) |
| Rehearsal v3 | **96** | **64** | **160/160 (100%)** |

On the same corrective v3 model, the targeted_v3 controller scores 59/96 core and 35/64 composed; unified_v4 scores 94/96 and 60/64. Thus the more dramatic headline jump is **runtime engineering**, while the fixed-controller model comparison supports genuine **training/adaptation** gains.

SW16 SW09 retention (56 new tasks): corrective v3 and rehearsal v3 both score 56/56 strict under unified_v4, original corrective 45/56. The SW16 `deployment_decision.txt` was **HOLD**, specifically because one corrective-v3 composed-state regression occurred against the targeted baseline. The gate decision must remain visible even though aggregate strict success improved.



## SW17: fixed-controller adaptation, paired evaluation and authorization regression

SW17 generated 240 training tasks, 40 development tasks and **80 new precommitted sealed synthetic tasks** across 10 fault groups, including `approval_not_required` and `lease_expired`. Training used 160 actual original-learner rollouts from training-only tasks, 400 identical anchor demonstrations and 400 arm-specific training rows per arm. Both v4 LoRA adapters continued from the same original SW09 corrective checkpoint for 80 steps (effective batch 8, LR 5e-5), rather than using a revised controller. See [transparent dataset construction](DATASET_CONSTRUCTION.md).

All SW17 comparisons use the **same four scripted initial reads**, after which the model chooses subsequent actions with no additional repair controller. Strict success on the shared 80-task sealed suite:

| Policy | Strict | State correct | Evidence supported | Unsafe mutation proposals | Mean steps | Mean model calls |
|---|---:|---:|---:|---:|---:|---:|
| Original frozen SW09 corrective | 31/80 | 58/80 | 54/80 | 6 | 11.775 | 7.775 |
| Continued corrective v4 | **65/80** | 77/80 | 73/80 | 8 | 14.4375 | 10.4375 |
| Equal-budget rehearsal v4 | **65/80** | 80/80 | 77/80 | 8 | 12.0875 | 8.0875 |
| Earlier rehearsal v3, supplemental comparator | 57/80 | 75/80 | 60/80 | 2 | 11.875 | 7.875 |

**Causal interpretation:** under the fixed controller, corrective v4 makes **34 more strict successes (42.5 percentage points)** than its frozen starting policy; paired wins/losses = 38/4, exact McNemar `p=5.653146e-8`. Matched rehearsal v4 makes the **same 65/80** strict successes; corrective versus rehearsal discordances = 5/5, `p=1`. The evidence supports *model updating*, **not** a unique benefit of learner-visited corrective labels. The initial four observations are deterministic in every condition, so this is not fully controller-free interaction.

**Crucial negative safety result:** The eight `injected_forbidden` sealed tasks produced **eight unsafe mutation proposals in aggregate per v4 arm** and **0/8 strict successes**. Per-task proposal incidence requires inspecting the individual episode traces. Frozen original SW09 had 6 unsafe proposals and 2/8 strict successes; previous rehearsal v3 had 2 proposals and 6/8 strict successes. The simulator's authorization guard blocks disallowed tool calls, so a blocked *proposal* must not be equated with a forbidden *executed mutation*. Nevertheless, the v4 agents do **not** satisfy the proposed autonomous deployment requirements. SW17's recorded `experiment_gate=PASS_LEARNING_BUT_NOT_CORRECTIVE_SUPERIORITY` is a **narrow learning-attribution gate**; its recorded `deploy=false` remains controlling. The appropriate rollout recommendation is **HOLD** until unsafe proposals are addressed and evaluated on a fresh, untouched holdout.

**Generalization limits:** SW17 changes service/region/request vocabulary and adds previously unseen configuration fields, but remains within the same simulator family. Corrective v4 was 31/40 on unseen fields, rehearsal v4 36/40, previous rehearsal v3 40/40 and frozen SW09 18/40. This does not establish external transfer. All four SW17 evaluations refer to the **same 80 tasks**, not 320 independent tasks. The procedure and per-task trace packaging are documented in [SW17 notebook](../notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb) and the [dataset publication notebook](../notebooks/FINAL_HF_Publish_SW12_SW17_From_Kaggle.ipynb).

## 8. Focused budgeted v5 regression repair

A subsequent conservative intervention addressed repeated silent no-op commits and excess unsupported finish actions. The controller reserves sufficient action budget before an additional authorized stage/commit/check sequence and activates only after repeated confirmed failure.

Comparison against the frozen unified_v4 result over the same 320 model-task cases:

| Model | Core v4→v5 | Composed v4→v5 | Total v5 strict | Total v5 state correct |
|---|---|---|---:|---:|
| Corrective v3 | 94→95/96 | 60→61/64 | **156/160** | 160/160 |
| Rehearsal v3 | 96→96/96 | 64→64/64 | **160/160** | 160/160 |
| **Combined** | | | **316/320 (98.75%)** | **320/320** |

Only **9/320** episodes invoked the new bounded intervention, with **two strict wins, zero strict losses** compared to unified_v4; raw unsafe model proposals and executed forbidden mutations were zero on these v5 runs. Each individual one-win comparison against v4 has exact McNemar `p=1.0` (not significant). The narrow test passes its **focused engineering regression gate**. It is not a second independent holdout or evidence of generic deployment safety.

## 9. Threat model and measured safety

Attacker/fault influence includes injected content appearing in tool observations, false-positive authority cues, and unauthorized mutation attempts. The enforced security boundary is the workflow's authorization, approval and lease constraints plus postcondition verification, **not** a promise that an LLM will never propose unsafe actions.

SW16 v5 recorded zero executed forbidden mutations on 320 episodes and zero raw unsafe proposals for the two v3 adapters. These are empirical simulator results on a specified test suite, not a universal zero-risk guarantee. Genuine deployment would require independent tests of concurrency, unmodeled schemas, adversarial prompt injection and faulty ground-truth verifiers.

## 10. Statistical reasoning and limitations

- **Do not mix cohorts:** SW09 70 tasks, SW12 sealed 64, SW14 fresh 128, SW15 70+80, and SW16 56+96+64 were used in different phases with differing controllers.
- **Do not attribute controller effects to fine-tuning.** The parent SW09 controller nearly matches the corrective policy; the SW16 controller has large fixed-model benefits.
- **Do not oversell corrective superiority.** SW12 rehearsal matches or outperforms corrective in multiple tests, including the latest strict 160/160 vs 156/160.
- **Repeated task-family tuning:** SW16 includes post-hoc controller repairs informed by failures. Only prospective untouched external evaluations could validate generality.
- **No independent real-world benchmark.** The two simulated workflows are related, with overlapping interfaces.
- **Verification quality:** Counterfactual/teacher labels depend on a scripted continuation and oracle quality. False assumptions or schema coverage gaps can bias learned data.
- **No universal safety.** The simulation explicitly gates writes; adversarial real tools can behave differently.
- **Model provenance:** all adapters depend on a custom locally published Plain SFT checkpoint and must be uploaded with the correct base and tokenizer. Adapters alone are not standalone inference weights.
- **Resources:** original experiments ran on Kaggle two-T4 sessions. No independent replicate on alternative hardware is claimed.

## 11. Future work with more compute and time

Create a prespecified training curriculum with authorization counterfactuals, expired leases, no-op and conflict compositions; compare verified corrective, matched rehearsal, and counterfactual ablations from the same starting weights; freeze the controller before paired evaluation; evaluate on additional independent task schemas and an external benchmark with a separately written oracle; preregister a prospective holdout and report both task success and unsafe proposal rates with confidence intervals.

## 12. Reproducibility and references

Primary sources are the unmodified source notebooks, exported adapters, and episode archives described in [ARTIFACTS.md](ARTIFACTS.md), with compact exact results in [results/README.md](../results/README.md).

- LEXSI hackathon and Track 3 Problem 8: https://hackathon.lexsi.ai/
- AgentTune: https://github.com/Lexsi-Labs/AgentTune
- DAgger: Ross, Gordon & Bagnell (2011), *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*, https://proceedings.mlr.press/v15/ross11a.html
- Hugging Face TRL: https://huggingface.co/docs/trl/sft_trainer
- Hugging Face PEFT: https://huggingface.co/docs/peft/

**AI usage disclosure.** ChatGPT assisted with code/notebooks, experiment planning, analysis and release documentation. Numerical claims in this report are restricted to inspected archived output, not generated by an LLM judge.
