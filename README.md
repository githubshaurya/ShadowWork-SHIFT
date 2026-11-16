# ShadowWork-SHIFT

### Teaching a tool-using agent to recover from failure, and proving that training changes its behavior

**LEXSI AI Safety & Alignment Hackathon · Track 3: Agentic Fine-tuning · Problem 8: Self-healing agents**

> **Headline:** **38.75% → 81.25% strict task success** on 80 sealed, fault-injected workflows (**31/80 → 65/80; +42.5 percentage points**) after LoRA fine-tuning, **with the same tool harness, same four initial observations, same inference controller, and same test tasks**. Corrective versus frozen: **38 paired wins, 4 losses; exact McNemar p = 5.65 × 10⁻⁸**.

[**Technical report**](docs/TECHNICAL_REPORT.md) · [**Dataset method**](docs/DATASET_METHOD.md) · [**SW17 evidence and paired tests**](docs/SW17_RESULTS.md) · [**Reproduction guide**](docs/REPRODUCIBILITY.md) · [**Model collection**](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac) · [**Dataset collection**](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812)

ShadowWork-SHIFT closes the loop between **failure discovery, recovery-data creation, real model fine-tuning, trace-grounded evaluation, and conservative redeployment decisions**. It uses a **Cohere Tiny Aya-derived open-weights model**, **LEXSI AgentTune** for the agentic execution/trajectory harness, **LEXSI AuditKIT** for evaluated tool episodes, and **TRL/PEFT** for LoRA optimization. The project is a runnable, public research/hackathon system with inspectable state transitions, saved training rows, adapters, logs, and held-out results.

## For judges: the one-minute case

| What matters | What we built and measured |
|---|---|
| **Real agentic failure modes** | Stateful SQLite maintenance tools that inject silent no-op writes, stale reads, conflicts, false-positive receipts, wrong writes, lease expiry, and authorization traps |
| **Actual closed-loop learning** | Frozen agent rollouts → learner-visited failure states → scripted reference repair labels → LoRA continuation → re-evaluation |
| **A controlled training effect** | On the **same 80 sealed SW17 tasks**, frozen SW09 **31/80**, corrective v4 **65/80**, matched rehearsal v4 **65/80** |
| **Training, not a better hand-coded controller** | **Identical four-read bootstrap and no subsequent controller repair** across every SW17 model arm; model chooses each remaining action |
| **Strong evaluation** | Exact paired McNemar tests, durable-state correctness, verification evidence, unsafe proposals, blocked calls, action count, token and model-call usage |
| **Actual LEXSI SDKs** | AgentTune `Project`, `ReActStrategy`, `DictToolHarness`; AuditKIT `AgentEvalRunner`, `AgentCase`, `FinalStateAssertion` |
| **Open release** | Exact custom base, four v3/v4 trained adapters, synthetic training JSONLs, precommitted splits, **160 SW12 + 160 SW17 learner rollouts**, **384 SW12 + 320 SW17 evaluated trajectories**, method and SHA-256 provenance on Hugging Face |

Our release matches the hackathon's central technical deliverables: **a dense Cohere-derived open-weights model, practical Track 3 tool-agent workflow, LEXSI SDK integration, public model/data artifacts, more than one before/after metric, and a reproducible write-up**. The participant must still complete the official submission form.

## 1. The problem: an acknowledgment is not a verified outcome

Suppose a tool agent is instructed to change a configuration setting. A tool may answer *“committed”* even when nothing persisted; a subsequent read may be stale; a lease may expire mid-retry; or a maintenance request may fail an approval or canary-health gate. A fluent response like *“done”* is not sufficient.

ShadowWork-SHIFT gives the agent a realistic control-plane workflow with typed tool arguments, a durable SQLite state, authorization constraints and fault schedules. The agent must **read policy and current state, perform permitted changes, recover from injected failure, verify durable state, and finish with evidence**. Unsafe mutation attempts are refused by the executable tool gate and remain visible in the logs.

**Strict success** requires all of: correct state or correct refusal, valid authorization, the required one or two matching post-write checks, and a supported final answer. We measure persisted-state correctness separately from evidence-backed completion.

## 2. The end-to-end self-healing pipeline

```text
Synthetic maintenance ticket + hidden fault schedule
                    │
                    ▼
       Tiny Aya-derived policy model
                    │
       LEXSI AgentTune Project
       ReActStrategy + DictToolHarness
                    │
                    ▼
       Stateful SQLite tool execution
       observed results + durable state
                    │
                    ▼
       LEXSI AuditKIT evaluation
       + replay/state/evidence assertions
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  Detect mismatch         Preserve episode
  and failure mode        audit + task identity
        │
        ▼
  Reference-policy continuation
  on real learner-visited states
        │
        ▼
  Matched training datasets
  corrective vs expert rehearsal
        │
        ▼
  TRL SFTTrainer + PEFT LoRA
  (same frozen starting adapter)
        │
        ▼
  Sealed matched-policy evaluation
  + paired tests + safety/deployment gate
```

The tools are deliberately used for distinct roles. **AgentTune** runs model-controlled agent/tool trajectories; **AuditKIT** scores agent episodes, including final-state assertions; **TRL/PEFT** actually updates LoRA parameters. The training code does not falsely attribute optimization to AgentTune. SDK classes and execution paths are visible in [the original SW17 notebook](notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb).

## 3. The experiment that isolates model learning (SW17)

We wanted evidence that improvement came from **updating the model**, rather than quietly replacing its tool-use logic with a more capable deterministic controller.

**Frozen design.** Generate and precommit **240 training**, **40 development**, and **80 sealed** tasks over ten fault families. Collect **160 real frozen-learner rollouts from training tasks only**. Build two **800-example** SFT datasets:

- **Corrective v4:** 400 shared expert anchors + 400 reference-labeled learner-visited states, with priority to genuine learner/reference disagreements.
- **Rehearsal v4:** the same 400 anchors + 400 ordinary reference-policy demonstrations, matched on task/failure/protocol/action strata wherever possible. **395 of the 400 control examples matched the exact action strata** recorded in the selection audit.

Both adapters start from the **exact same frozen SW09 corrective LoRA**, use **80 optimizer steps**, **learning rate 5 × 10⁻⁵**, **effective batch 8**, and the same tool grammar and tokenizer. Weights, source training hashes and optimization metadata were retained.

**Evaluation design.** For every policy and every sealed task, the controller performs the **same four initial reads** (ticket, runbook, health and approval). From that point onward, **the model selects actions**, without additional deterministic recovery/finish rules. Environment, fault schedule, scoring code, task IDs and action budget are held fixed.

| SW17 sealed policy | Strict tasks | Persisted state correct | Verification evidence supported | Unsafe proposals | Mean model calls |
|---|---:|---:|---:|---:|---:|
| Frozen SW09 starting model | 31/80 · 38.75% | 58/80 | 54/80 | 6 | 7.78 |
| **Corrective v4 fine-tuned** | **65/80 · 81.25%** | **77/80** | **73/80** | 8 | 10.44 |
| **Matched rehearsal v4 fine-tuned** | **65/80 · 81.25%** | **80/80** | **77/80** | 8 | 8.09 |
| Earlier rehearsal v3, additional transfer comparator | 57/80 · 71.25% | 75/80 | 60/80 | 2 | 7.88 |

**The proof that training mattered:**

1. **The intervention was parameter training.** The frozen model received no extra training; both v4 models were genuinely optimized and saved as distinct adapters.
2. **The controller was constant.** In SW17 all policies have exactly the same four initial scripted reads; none receives extra post-read hand-coded repair.
3. **The evaluation cases were paired.** The frozen and trained policies faced the same **80 precommitted sealed tasks** under identical stateful failure schedules.
4. **The difference is large and statistically supported.** Corrective v4 beats frozen on **38** tasks and loses on **4**; exact paired McNemar **p = 5.65 × 10⁻⁸**. Matched rehearsal also improves over frozen, with **36 wins and 2 losses, p = 5.40 × 10⁻⁹**.
5. **The control protects the inference.** Corrective v4 versus rehearsal v4 is **5 wins and 5 losses (p = 1.0)**. Hence the supported claim is **learning from additional supervised adaptation**, not an unproven claim that corrective examples are uniquely better than well-matched expert rehearsal.

In addition, **corrective v4 achieved 31/40 on previously unseen configuration fields**, compared with **18/40** for frozen SW09; the matched v4 rehearsal achieved **36/40**. This demonstrates useful within-family schema-shift evaluation rather than an external-world benchmark.

### Evidence-backed safety control, not score chasing

An essential part of self-healing is knowing when **not** to redeploy. The eight SW17 authorization-forbidden cases produced **eight unsafe model proposals per v4 arm** and **0/8 strict successes** in that category. The simulator's authorization gate **blocked those proposals from executing**. The experiment therefore records **training-evidence PASS / deployment HOLD**, rather than promoting a policy that still needs work on forbidden requests. This explicit separation of **proposal safety, execution safety and task success** is part of the system's design. The suite remains synthetic and no real-world deployment certification is implied.

The complete analysis is in [SW17 results](docs/SW17_RESULTS.md), and the underlying records are [public on Hugging Face](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets/tree/main/sw17).

## 4. Earlier checks: repeatability across failure and recovery settings

| Study | Comparison | Verified takeaway |
|---|---|---|
| **SW09** | Parent 42/70 → controller-only 69/70 → learner corrective 70/70 | Establishes the importance of controlling **runtime engineering** separately from learned changes |
| **SW12** | Frozen 24/64 → corrective v3 46/64; rehearsal v3 47/64 | Additional training works under a shifted verification protocol |
| **SW15** | Cross-protocol retention tests on SW09 and shifted tasks | Tests earlier learned policies and bounded controller recovery across related workflows |
| **SW16** | Shared unified controller: frozen 132/160; corrective v3 154/160; rehearsal v3 160/160 | Confirms adaptation effects persist with the **same** controller |
| **SW17** | Shared minimal controller: frozen 31/80; both trained v4 arms 65/80 | The clearest isolation of the **model-training effect**, with an explicit safety gate |

These experiments assess different test suites and controller configurations; their denominators are **not pooled**.

## 5. What is published

### Hugging Face collections (the two official form links)

**[All released models and LoRA adapters](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac)**

**[Training datasets, task splits, failure logs and evaluation evidence](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812)**

### Exact released checkpoints

| Artifact | Public repository |
|---|---|
| Original custom Cohere Tiny Aya-derived Plain SFT full base | [shadowwork-shift-plain-sft](https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft) |
| SW09 learner-corrective starting adapter | [shadowwork-shift-learner-corrective](https://huggingface.co/i-am-shaurya05/shadowwork-shift-learner-corrective) |
| SW12 corrective v3 | [shadowwork-shift-corrective-v3](https://huggingface.co/i-am-shaurya05/shadowwork-shift-corrective-v3) |
| SW12 matched rehearsal v3 | [shadowwork-shift-rehearsal-v3](https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-v3) |
| SW17 corrective v4 | [shadowwork-shift-corrective-v4](https://huggingface.co/i-am-shaurya05/shadowwork-shift-corrective-v4) |
| SW17 matched rehearsal v4 | [shadowwork-shift-rehearsal-v4](https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-v4) |

All four v3/v4 repositories contain the trained **120,981,200-byte** `adapter_model.safetensors`, `adapter_config.json`, tokenizer resources and provenance. Every adapter points to the **exact custom public base**, not a generic similarly named upstream checkpoint.

The [SW12/SW17 consolidated public dataset](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets) hosts both exact 800-row-per-arm curricula, task splits, split commitments, learner rollouts, scored episode logs, paired tests, release hashes and a [dataset card](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets/blob/main/README.md). Original [SW09 training and holdout data](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training) are also public. Dataset construction follows [a fully documented executable process](docs/DATASET_METHOD.md), using synthetic tasks and **programmatic observation-grounded reference labels**, not invented human annotations.

### Reproduce and inspect

1. **Read the exact experiments:** [SW17 fixed-controller notebook](notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb), [SW12 shifted-protocol notebook](notebooks/SW12_Closed_Loop_Adaptation.ipynb), and the [reproduction guide](docs/REPRODUCIBILITY.md).
2. **Audit without GPU:** download the published `sw17/` files and recompute scores from `episode_scorecard.csv`, `policy_summary.csv`, `paired_tests.csv` and per-task `evaluation/sealed/` JSONs. [Project evidence audit](docs/SW17_RESULTS.md) describes the measured comparisons.
3. **Full training reproduction:** original runs used **2 × NVIDIA T4** with pinned TRL, PEFT, Transformers, Accelerate, BitsAndBytes, AgentTune and AuditKIT versions. The exact starting adapter, task seeds, hashing commitments and completion-only labels matter.
4. **Release checking:** [anonymous public-release verifier](scripts/verify_hf_public_release.py) checks all four model files, training data and collection memberships. [Publication notebook](notebooks/FINAL_HF_Publish_From_Kaggle.ipynb) only uploads **already-trained** artifacts, never retrains.

Full experiment lineage, detailed checks, efficiency tradeoffs and limitations are in the [technical report](docs/TECHNICAL_REPORT.md). The agent experiments use a controlled **synthetic simulator family**, so the result should be interpreted as validated synthetic recovery rather than production-world transfer.

## 6. Alignment with LEXSI's Track 3 submission expectations

| Required component | Evidence in this release |
|---|---|
| Cohere dense open-weights language model | [Exact Tiny Aya-derived custom checkpoint](https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft) |
| Agentic fine-tuning and self-healing | Saved failure-conditioned datasets, **real 80-step LoRA training**, recovered-state evaluation |
| Track SDKs integrated | **AgentTune + AuditKIT** jointly exercised in SW17 agent/harness and episode scoring; TRL/PEFT used for optimizer |
| Before/after metrics (multiple) | Strict task success, state correctness, evidence support, unsafe proposals, tool/model calls, tokens |
| Training-causality safeguards | Same starting weights, matched rehearsal comparator, fixed controller, identical sealed tasks, exact paired tests |
| Public models/adapters, logs, datasets | Hugging Face [model collection](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac) and [dataset collection](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812) |
| Reproducible GitHub write-up | This README, [technical report](docs/TECHNICAL_REPORT.md), [dataset method](docs/DATASET_METHOD.md), notebooks and provenance |
| Responsible deployment decision | Task improvement gate evaluated separately from authorization/safety gate, which remains **HOLD** |

This matrix describes the **published technical submission**. Completing the official hackathon form is the participant's final submission action.

## Repository navigation

- [Technical report](docs/TECHNICAL_REPORT.md) · [SW17 result analysis](docs/SW17_RESULTS.md) · [Dataset construction](docs/DATASET_METHOD.md)
- [Complete notebook sources](notebooks/) · [Reproduction steps](docs/REPRODUCIBILITY.md) · [Artifact provenance](docs/ARTIFACTS.md) · [Checks](SUBMISSION_CHECKLIST.md)
- [Offline result verification](scripts/verify_archived_results.py) · [Anonymous Hugging Face verification](scripts/verify_hf_public_release.py)
- [Final abstract (under 500 words)](submission/ABSTRACT.md)

**Acknowledgments and attribution.** Developed for the [LEXSI AI Safety & Alignment Hackathon](https://hackathon.lexsi.ai/) in the Cohere Labs open-weights ecosystem. LEXSI **AgentTune** and **AuditKIT** are actual runtime/evaluation dependencies; **TRL/PEFT** carry out the supervised LoRA parameter updates. ChatGPT assisted with coding, analysis, source documentation and release packaging; the participant is responsible for experimental decisions and the final submission.
