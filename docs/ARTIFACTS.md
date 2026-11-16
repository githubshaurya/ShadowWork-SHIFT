# Artifact inventory and provenance

This inventory separates **source notebooks**, **trained weights**, **training/benchmark datasets**, and **evidence archives**. A ZIP being present in Project/Kaggle is *not* proof that it is already publicly downloadable.

## Checkpoint lineage

```
Cohere Tiny Aya-derived custom Plain SFT (~3.35B, full checkpoint)
  (Kaggle input: shaurya466/shift-plain/shadowork_123)
  |
  +--> Oracle BC v2 LoRA
          |
          +--> SW09 learner-state corrective LoRA (original corrective)
                  |
                  +--> SW12 learner-corrective v3 LoRA
                  |
                  +--> SW12 matched rehearsal v3 LoRA
          |
          +--> SW09 on-policy/rehearsal BC comparator
```

**Caution:** Original archive configs reference **local Kaggle** base paths. The publicly released SW08/SW09 adapter configs now point to the exact already-public custom base; SW12 v3 configs must be rewritten *as metadata only* during their pending release. Verify tokenizers and original weight hashes. Do not silently substitute a generic Tiny Aya base.

## Primary archived sources

| Artifact | Contents | Status |
|---|---|---|
| `ShadowWork_09_Kaggle_Input_Bundle.zip` | SW08 Oracle BC v2 adapter, prepared train-only source ZIP | Available in Project and on Kaggle; publication pending |
| `ShadowWork_09_Learner_State_Verified_Recovery_Kaggle.ipynb` | Original embedded-data SW09 pipeline | Available source |
| `ShadowWork_09_Kaggle_Extracted_Input_Ready.ipynb` | Final extracted-input SW09 training pipeline | Preferred runnable source |
| `ShadowWork_09_learner_corrective_Adapter.zip` | SW09 original corrective LoRA weights and tokenizer | Available in Project; HF upload pending |
| `ShadowWork_09_rehearsal_bc_Adapter.zip` | SW09 matched comparator | Available in Project; HF upload pending |
| `ShadowWork_09_Final_Holdout_Evidence.zip` | 210 scored episodes + split commitments | Available in Project; HF upload pending |
| `ShadowWork_12_Closed_Loop_Evidence.zip` | v3 corrective and rehearsal adapters, training rows, task splits, episode scores, manifests | Available in Project; HF upload pending |
| `ShadowWork_13_Live_Results.zip` | Initial live controller evidence, scorecards, traces | Available in Project |
| `ShadowWork_14_Controller_Repair_Results1.zip` | Fresh 128-task paired controller experiment | Available in Project |
| `ShadowWork_15_Cross_Protocol_Recovery_Results.zip` | 70 SW09 + 80 SW12 new tasks and controller comparisons | Available in Project |
| `ShadowWork_16_Unified_Recovery_Results.zip` | 1,096 evaluated episodes, SW09 retention + SW12 core/composed, deployment gate | Available in Project |
| `ShadowWork_16_Budget_Regression_Results.zip` | 320 v5 episodes, paired_summary.csv, paired_task_results.csv, gate | Available in Project |

Preferred rendered notebook names in GitHub should use descriptive `SW09_...`, `SW12_...` rather than the generic Kaggle download filename `notebook12903defcf*.ipynb`.

## Prespecified identity and split checks

- SW09 final holdout: 70 cases in seven 10-case failure groups; `holdout_sha256=1e13aa4d951ae1acdcc5d8ec9bdd43a3ec7e0897a0254aeff037e33ba9866197` as recorded in `holdout_commitment.json`.
- SW12 source generator: seed `20261113`, max 22 actions; train/dev/sealed split hashes in `final_provenance.json`.
- SW12 starting adapter digest: `680659a3c6fce48e18f4ce8087b3fbb2c5806d4427e90c2b5cc6c49a524bb441`; v3 training source hashes in per-arm `*_training_metadata.json`.
- SW12 v3: 800 training rows per matched arm, 80 optimizer steps, LR `5e-5`, global batch 8.

## Verified existing public artifacts and pending new uploads

**Previously published on November 12, 2026:**

- Exact full seven-shard Plain SFT base: https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft
- Oracle BC v2 parent adapter: https://huggingface.co/i-am-shaurya05/shadowwork-shift-oracle-bc-v2
- Original SW09 learner-state corrective: https://huggingface.co/i-am-shaurya05/shadowwork-shift-learner-corrective
- Original SW09 matched rehearsal adapter: https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-bc
- SW09 original training/holdout data, audit reports and simulator code: https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training
- Previously created model collection: https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac
- Previously created data collection: https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812

**Created Nov 15, pending model/data upload and final public verification:**

- SW12 corrective v3 adapter: https://huggingface.co/i-am-shaurya05/shadowwork-shift-corrective-v3
- SW12 rehearsal v3 adapter: https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-v3
- SW12–SW16 dataset and audited evidence: https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets
- Publishing source: [FINAL_HF_Publish_From_Kaggle.ipynb](../notebooks/FINAL_HF_Publish_From_Kaggle.ipynb)

The seven base weight-shard hashes publicly documented in `provenance/base_checkpoint_shards_sha256.json` match the seven hashes independently present in SW09 final holdout `base_hashes.json`. Existing public collections are visible in account metadata; their browser access and final membership should still be verified independently.

## Integrity conventions

Retain the original evidence ZIPs in a `source_archives/` staging directory until checked; keep ZIP member names and SHA-256 checksums. Publish only curated, relevant artifacts, not redundant generated copies of identical tasks. Recompute metrics from exported episode JSONs and scorecards. No hand-entered data should replace raw traces for scientific verification.

## SW17 actual trained weights and data provenance (pending HF upload)

SW17 continuation from the original SW09 corrective adapter completed both equal-budget training arms. Original 80-step rehearsal_v4 adapter saved first, then learner_corrective_v4 saved after recovery from a repeated DDP launch failure. Both training JSONLs contain 800 rows, share 400 original expert anchors, and record hashes in `*_training_metadata.json`. The sealed test was precommitted as 80 synthetic tasks across 10 groups. Under identical four-read bootstrap and no further repair controller: frozen SW09 31/80, corrective v4 65/80 and rehearsal v4 65/80 strict. **Both v4 arms attempted unsafe mutations in all eight injected_forbidden tasks**, blocked by the simulator; do not claim deployment approval. See [dataset construction](DATASET_CONSTRUCTION.md) and [SW17 technical results](../results/README.md).

The CPU-only [final SW12+SW17 publisher](../notebooks/FINAL_HF_Publish_SW12_SW17_From_Kaggle.ipynb) is the preferred replacement for the earlier SW12-only publisher; it uploads **four actual LoRA adapters**, exact SW12+SW17 training/split/audit/trace records, the transparent HF dataset card and release SHA-256 manifest. **The new HF model/data repos remain pending until that notebook actually succeeds and public files are verified.**
