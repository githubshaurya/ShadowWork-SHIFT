# Reproducing ShadowWork-SHIFT

ShadowWork-SHIFT is publicly released as executable source notebooks, exact trained adapters, train/development/sealed task specifications, learner tool trajectories and state-backed evaluation evidence. **The fastest audit requires only the public files and CPU; reproducing training requires the original Kaggle 2×T4 configuration.**

## One-minute reproducibility route (no retraining)

1. Open the [public SW12/SW17 dataset](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets) and its `sw17/` directory. Review `precommit.json`, `selection_audit.json`, `policy_summary.csv`, `paired_tests.csv`, `episode_scorecard.csv`, `learning_gate.json`, train/dev/sealed JSONLs and `evaluation/sealed/` JSON traces.
2. Verify the sealed suite contains **80 distinct tasks** each evaluated with four frozen policies. The consolidated `episode_scorecard.csv` contains **320 rows**. Paired strict-success results are frozen SW09 **31/80**, corrective v4 **65/80**, rehearsal v4 **65/80**, and earlier rehearsal v3 **57/80**.
3. Recompute exact McNemar statistics from paired `strict_success` values by `task_id`: corrective vs frozen **38 wins / 4 losses, p=5.653146e−8**; rehearsal vs frozen **36 wins / 2 losses, p=5.398761e−9**; corrective vs rehearsal **5 wins / 5 losses, p=1**.
4. Read the saved per-episode `history`, `score`, `auditkit_verdict`, `final_value` and model-call usage. The [original SW17 scoring cell](../notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb) independently replays every recorded action against the SQLite simulator, asserts identical observed tool results, final persisted state and strict score.
5. Cross-check `sha256_release_manifest.json` against downloaded data, plus model cards' `provenance/original_weights_sha256.txt` and the original `final_provenance.json` weight digests.
6. For a quick anonymous Hub metadata test, run [scripts/verify_hf_public_release.py](../scripts/verify_hf_public_release.py). For a **deeper no-GPU check**, run [scripts/verify_sw17_public_evidence.py](../scripts/verify_sw17_public_evidence.py): it independently downloads all 496 public SW17 data files, checks release hashes and training/split metadata, verifies 320 individual episode strict outcomes, and recomputes exact paired McNemar tests. Full stateful SQLite **replay** remains in the executed source notebook.

No GPU is required to inspect a task, recompute scorecard statistics or audit SHA-256 commitments.

## Software, hardware and actual SDK roles

The original training runs used **2 × NVIDIA T4 GPUs** on Kaggle. The final SW17 source pins AgentTune from [Git commit `e56a1094b65cbf7c2c0b26d0db2ac4dffffa693a`](https://github.com/Lexsi-Labs/AgentTune), AuditKIT `1.1.7`, TRL `1.7.1`, PEFT `0.21.2`, Transformers `5.17.0`, Accelerate `1.15.0`, and BitsAndBytes `0.49.2`. For exact replication, use the dependency cells in the source notebooks, including their documented T4 FP16 / FP32 trainable LoRA workaround. These are pinned observed environments, not broad version compatibility guarantees.

- **LEXSI AgentTune:** `Project` combines `ReActStrategy` and a `DictToolHarness` derivative that forwards tool calls to the SQLite maintenance environment, recording full action/observation trajectories. Source: SW17 `run_episode`, `SQLiteToolHarness`.
- **LEXSI AuditKIT:** `AgentEvalRunner` evaluates `AgentCase` specifications with `FinalStateAssertion` and the `episode_from_eventlog` converter; the independent stateful replay asserts consistency.
- **TRL / PEFT / Transformers:** `SFTTrainer` performs the LoRA parameter optimization. These are the real training libraries; using AgentTune for the agentic spine does **not** imply it implements the SFT optimizer.

## Checkpoint lineage

```text
Custom Tiny Aya-derived Plain SFT full checkpoint
  └── Oracle BC v2 parent LoRA
       ├── Original SW09 learner-corrective adapter (frozen v3/v4 starting point)
       │    ├── SW12 corrective v3        [800 rows / 80 steps]
       │    ├── SW12 matched rehearsal v3 [800 rows / 80 steps]
       │    ├── SW17 corrective v4        [800 rows / 80 steps]
       │    └── SW17 matched rehearsal v4 [800 rows / 80 steps]
       └── SW09 ordinary rehearsal adapter (historical comparator)
```

The **exact released full base** is [`i-am-shaurya05/shadowwork-shift-plain-sft`](https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft). The starting corrective adapter is [`i-am-shaurya05/shadowwork-shift-learner-corrective`](https://huggingface.co/i-am-shaurya05/shadowwork-shift-learner-corrective). The released v3/v4 adapters point to that full custom base and preserve the original Kaggle adapter configurations and exact weight SHA-256 in `provenance/`. Using a generic Cohere Tiny Aya checkpoint instead would change the experiment.

## Full experiment reproduction

The final SW17 source [SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb](../notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb) documents the exact protocol. Original user-executed source and resulting ZIP are retained as Project artifacts. It creates ten fault groups with 24 training, four development and eight sealed tasks per group; precommits all splits and hashes **before model inference**.

1. Load the full base and original frozen SW09 corrective adapter; verify source/checkpoint digests.
2. Generate **240 training**, **40 development** and **80 sealed** task identities with seed `20261115`, store exact task JSONLs and `precommit.json`. Ensure sealed tasks remain outside training construction.
3. Run the frozen starting adapter over **160 train-only episodes**, preserving actual model outputs and all tool observations in `collection/`.
4. Replay observed learner histories; label decision states with the scripted observation-only reference policy. Build 800-row corrective and 800-row expert-rehearsal datasets: 400 identical expert anchors per arm plus 400 curriculum-specific rows. Exact action-stratum matching is achieved for **395/400** control extras, per `selection_audit.json`.
5. Fine-tune from the **same starting adapter** under matched optimization (80 steps per arm, LR `5e-5`, effective batch 8). The trainer uses explicit completion-only labels and retains exact source hashes in `*_training_metadata.json`.
6. Evaluate frozen SW09, corrective v4, rehearsal v4 and optional prior rehearsal v3 on **the same 80 sealed tasks**. The first four reads are scripted identically, and **the model chooses all later actions without any added recovery controller**.
7. Replay every task's saved tool history against the SQLite environment, compare AuditKIT verdict and strict score, compute group/field breakdowns and paired tests, and export the manifest-protected source evidence archive. Do not merge results across SW09, SW12 and SW17 as though their tasks were independent.

Earlier SW09, SW12, SW14, SW15 and SW16 protocols are in the appropriately named [notebooks](../notebooks/) and [historical result inventory](ARTIFACTS.md).

## What the key metrics establish

- **Strict success:** correct allowed/refused decision, correct durable value, sufficient post-write readbacks, and a supported terminal action. The **primary metric**.
- **State correctness:** verified persisted state, independent from the final reply.
- **Evidence support:** completed the requisite one or two matching checks after the last write.
- **Unsafe proposals vs executed forbidden mutations:** the model's suggested unauthorized action is measured **even if** the tool authorization gate blocks it. SW17 discovered eight unsafe proposals in each v4 arm on the eight forbidden-injection tasks; these policy issues trigger `deploy=false`.
- **Efficiency:** model calls, tool actions and generated/input tokens, tracked for each policy.
- **Paired tests:** wins/losses on identical task IDs, not an unpaired difference-of-proportions test.

The training-effect comparison is the frozen vs v4 comparison **holding the inference controller constant**. The contrast between corrective and matched rehearsal tests whether **learner-visited corrective data** outperforms regular expert rehearsal; the SW17 result was a tie. Neither result is an independent production benchmark, since the task environment is synthetic.

## Release and audit

- **Hugging Face model collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac
- **Hugging Face dataset collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812
- **SW12/SW17 exact datasets and evidence:** https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets
- **SW09 original train/holdout:** https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training
- **Publication notebook:** [FINAL_HF_Publish_From_Kaggle.ipynb](../notebooks/FINAL_HF_Publish_From_Kaggle.ipynb) **publishes already-trained artifacts, no optimization or evaluation**.
- **Full dataset methodology:** [DATASET_METHOD.md](DATASET_METHOD.md), including scripted reference labels, synthetic design, split commitments and matched-control selection.

**Public availability has been verified for the four v3/v4 adapter repositories and SW12/SW17 dataset folders.** Historic SW13–SW16 traces have been retained in Project ZIP archives and analyzed in the report; they need not be merged into the clean, primary SW12/SW17 public dataset release.
