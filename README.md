# ShadowWork-SHIFT

**Self-healing stateful tool agents through corrective adaptation and evidence-grounded recovery**

[![Track 3](https://img.shields.io/badge/LEXSI-Track%203-blue)](https://hackathon.lexsi.ai/)
[![Problem 8](https://img.shields.io/badge/Problem-Self--healing%20agents-informational)](https://hackathon.lexsi.ai/)

ShadowWork-SHIFT is an experimental pipeline for **LEXSI.ai's AI Safety & Alignment Hackathon, Track 3, Problem 8: Self-healing agents**. It studies how a compact open-weights Cohere Tiny Aya policy can recover from failures in *stateful*, authorization-gated tool workflows: silent no-ops, incorrect writes, stale readbacks, commit conflicts, and misleading completion signals.

The pipeline detects and diagnoses failing runs, uses learner-visited states and verified corrective continuations for LoRA adaptation, evaluates policies against matched rehearsal controls, and gates recovery changes on strictly checked persisted state and task evidence. **AgentTune** is used for agent execution and tool harnesses, with **AuditKIT** for evaluation and diagnostics. LoRA optimization uses **TRL/PEFT**, not a claim that AgentTune natively performed those weight updates.

> **Status:** Experimental research prototype, *not production certified*. The exact custom Plain SFT base and three SW08/SW09 adapters, SW09 training traces, and 70-case holdout evidence were published previously; SW12 v3 and SW17 v4 adapters, plus SW12–SW17 exact data and evidence, are in the final publication pipeline; verify actual uploaded files before submission.

## Results at a glance

**SW09 sealed holdout (70 independently designated tasks, common evaluator):**

| Policy / controller | Strict success | Persisted state correct |
|---|---:|---:|
| Frozen Oracle BC v2 parent | **42/70** (60.0%) | 70/70 |
| Frozen parent + deterministic early-finish controller | 69/70 (98.6%) | 70/70 |
| SW09 learner-state corrective adapter | **70/70** (100%) | 70/70 |

The parent + controller row is crucial: a non-learning stopping intervention already produces a large improvement. The SW09 result alone **does not establish** that corrective training is indispensable.

**SW12 sealed shifted-protocol evaluation (64 tasks; no final unified controller):**

| Model | One-check strict | Two-check strict | Total strict |
|---|---:|---:|---:|
| Original SW09 corrective adapter, frozen | 22/32 | 2/32 | **24/64** |
| Corrective v3 adaptation | 31/32 | 15/32 | **46/64** |
| Matched rehearsal v3 | 31/32 | 16/32 | **47/64** |

SW12 v3 used equal-sized training arms, initialized from the same original SW09 corrective adapter. Corrective v3 improved substantially on the shifted protocol, but **did not outperform rehearsal**.

**SW16 later evaluation, identical unified_v4 controller across models (160 SW12 tasks = 96 core + 64 composed):**

| Model | Core strict | Composed strict | Total |
|---|---:|---:|---:|
| Original corrective adapter | 80/96 | 52/64 | **132/160 (82.5%)** |
| Corrective v3 | 94/96 | 60/64 | **154/160 (96.25%)** |
| Rehearsal v3 | 96/96 | 64/64 | **160/160 (100%)** |

Thus there is real **adaptation benefit holding the controller fixed**, but **not demonstrated superiority of failure-specific corrective labels over ordinary matched rehearsal**.

**Focused SW16 budgeted_v5 repair (320 model-task episodes, two v3 adapters):** Corrective v3 **156/160** strict; rehearsal v3 **160/160**; **316/320** combined strict successes and **320/320** correct persisted states. Relative to unified_v4, exactly two corrective-v3 strict failures were repaired, with zero losses, but each one-case improvement has exact paired `p=1` and **is not statistically significant**. No forbidden state mutations were executed in these recorded runs. The notebook's local gate was `PASS_FOCUSED_ENGINEERING_REGRESSION`; this is **not external deployment certification**.

### SW17 fixed-controller model-learning comparison (80 sealed tasks)

| Policy | Strict success | Final state correct | Unsafe mutation proposals |
|---|---:|---:|---:|
| Frozen original SW09 corrective | 31/80 (38.75%) | 58/80 | 6 |
| Corrective v4, 80-step continued training | **65/80 (81.25%)** | 77/80 | 8 |
| Matched rehearsal v4, same training budget | **65/80 (81.25%)** | 80/80 | 8 |
| Previously trained rehearsal v3 (additional baseline) | 57/80 (71.25%) | 75/80 | 2 |

**Training attribution:** corrective v4 improves by **34/80 tasks (+42.5 percentage points)** versus the frozen starting adapter with the same four-read bootstrap and *no additional repair controller*. Paired: 38 wins, 4 losses, exact McNemar `p=5.65e-8`. Rehearsal v4 is identically successful: 5 wins and 5 losses versus corrective v4, exact `p=1`. This establishes **fine-tuning gains**, not special corrective-curriculum superiority.

**Important SW17 safety failure:** both v4 arms recorded **eight unsafe proposals across eight forbidden-task episodes** and **0/8 strict success** in the `injected_forbidden` group. The synthetic runtime blocked unauthorized mutations, but **the policies themselves are not safe to deploy**. Original frozen SW09 had 6 unsafe proposals in that group; previous rehearsal v3 had 2. The SW17 notebook's `PASS_LEARNING_BUT_NOT_CORRECTIVE_SUPERIORITY` is a *learning-evidence gate*, **not** a deployment pass; `deploy=false`. No independent external benchmark is claimed.

**Transparent data creation:** See [dataset construction and provenance](docs/DATASET_CONSTRUCTION.md) and [publication-ready Hugging Face dataset card](docs/HF_DATASET_CARD.md) for fully synthetic generation, actual train-only learner rollouts, scripted reference labeling, matched 800-row curricula and original split/hash evidence. The new CPU-only [SW12+SW17 publishing notebook](notebooks/FINAL_HF_Publish_SW12_SW17_From_Kaggle.ipynb) publishes all four pre-trained LoRA adapters and dataset artifacts without any training.

For full cohort definitions, controller attribution, failure taxonomy and limitations, see [Technical report](docs/TECHNICAL_REPORT.md).

## Architecture

```text
Simulated workflow + fault scenario
           |
           v
  Tiny Aya policy + AgentTune tool harness
           |
           v
  Stateful tool execution + explicit observations
           |
           v
  AuditKIT / state checks / failure classification
           |
           +--> learner-visited corrective examples
           |            |
           |            v
           |       TRL / PEFT LoRA adaptation
           |            |
           v            v
   Frozen controller / matched model comparisons
           |
           v
    Paired accuracy, state, evidence and safety gates
```

**Two distinct kinds of improvement are separated in all analysis:**
1. **Model adaptation:** Original corrective versus v3 corrective/rehearsal under the *same* controller.
2. **Runtime engineering:** Targeted / unified / budgeted controllers compared on the *same* model.

## Reproduce

1. Use a Kaggle GPU notebook environment with **two T4 GPUs** for the original training configuration.
2. Obtain the [exact publicly released custom Plain SFT checkpoint](https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft) and [Oracle BC v2 adapter](https://huggingface.co/i-am-shaurya05/shadowwork-shift-oracle-bc-v2), or use the original Kaggle-mounted paths from the notebooks. SW12 v3 weights still require their own final upload.
3. Run the numbered notebooks in [notebooks/](notebooks/) only when all exact inputs are attached. They preserve the original experiment protocols and are **not** a promise of plug-and-play inference with an unrelated base model.
4. Evaluate the resulting policies with the archived task specifications and scoring definitions; report **strict** success separately from final DB-state correctness and evidence support.
5. Inspect [Results](results/README.md) for cohort-specific summary CSVs and named source archives. **Do not add success counts across different controllers or reused task sets.**

See [Reproduction guide](docs/REPRODUCIBILITY.md) for dependencies, frozen checks, data boundaries, and verification details.

## Publications

- [Model collection (existing)](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac)
- [Dataset/evidence collection (existing)](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812)
- [Exact published custom Plain SFT base](https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft)
- [Original corrective adapter](https://huggingface.co/i-am-shaurya05/shadowwork-shift-learner-corrective) and [matched SW09 rehearsal adapter](https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-bc)
- [Original SW09 training data and audited holdout traces](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training)
- [SW12 corrective v3 repository (empty until upload)](https://huggingface.co/i-am-shaurya05/shadowwork-shift-corrective-v3) and [SW12 rehearsal v3 repository (empty until upload)](https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-v3)
- [SW12–SW17 training/evidence repository (pending upload)](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets)

**Important:** Both public collections existed before this GitHub release; the v3 models and latest datasets are not yet populated. Follow the [updated SW12+SW17 Kaggle publishing notebook](notebooks/FINAL_HF_Publish_SW12_SW17_From_Kaggle.ipynb) and independently verify public collection membership and read access before submitting.

## Main limitations

- Both protocol suites are **synthetic and share a task schema**, so SW12 is not an independent real-world benchmark.
- SW16 controller work followed earlier failure inspection; it is engineering validation, **not an untouched prospective external test**.
- SW12 rehearsal v3 equals or outperforms corrective v3 on important cohorts.
- Controller improvements and learned improvements cannot be pooled into one causal estimate.
- No unrestricted deployment or guarantees beyond the tested authorization and mutation semantics.
- Both SW12 v3 adapter weights remain Kaggle-hosted until their public Hugging Face releases are completed.

## Repository navigation

- [Technical report](docs/TECHNICAL_REPORT.md): design, methods, quantified evidence, safety and threats to validity.
- [Reproducibility](docs/REPRODUCIBILITY.md): environment, source lineage and practical steps.
- [Artifact manifest](docs/ARTIFACTS.md): original experiment ZIPs, weights, seeds and provenance.
- [Results](results/README.md): compact verified result tables.
- [Offline verification script](scripts/verify_archived_results.py): recompute exact counts from source archives.
- [Audited dataset creation and provenance](docs/DATASET_METHOD.md): seeded simulator generation, frozen learner rollouts, observation-conditioned labeling, matched controls, exact split and training hashes, and caveats.
- [SW17 fixed-controller results](docs/SW17_RESULTS.md): 31/80 frozen → 65/80 after each v4 fine-tuning arm; matched rehearsal tie; 8 unsafe proposals per v4 arm, so **not deployable**.
- [Hugging Face dataset card](datasets/HF_DATASET_CARD.md): intended uses, generation, row counts, provenance and limitations.
- [Hugging Face publishing notebook](notebooks/FINAL_HF_Publish_From_Kaggle.ipynb): uploads existing SW12 v3 and SW17 v4 adapters plus the exact audited SW12/SW17 training datasets and traces; **does not train**.
- [Submission checklist](SUBMISSION_CHECKLIST.md): final public-link and form gate.

**Acknowledgment:** Built for the [LEXSI AI Safety & Alignment Hackathon](https://hackathon.lexsi.ai/) using the Cohere open-weight model ecosystem, AgentTune, AuditKIT, TRL, PEFT, and the Hugging Face Hub. No claim is made that the two LEXSI libraries by themselves perform the LoRA optimization.

**AI assistance disclosure:** ChatGPT assisted with experimental coding, analysis, documentation and release packaging. The human participant is responsible for evaluating the evidence, approvals, and submission.