# Public artifact inventory and provenance

All **core ShadowWork-SHIFT experiment deliverables are published**: exact model base, trained adapters, SW09/SW12/SW17 training data, split commitments, auditable agent trajectories, scored task records, methodology and source notebooks. The consolidated public dataset additionally includes selected SW13–SW16 historical engineering evidence, isolated from the primary sealed evaluation cohorts.

## Model lineage: original training start must be preserved

```text
Exact custom Cohere Tiny Aya-derived Plain SFT full checkpoint
  └── SW08 Oracle BC v2 adapter
       ├── SW09 learner-corrective adapter  [frozen start for v3 and v4]
       │    ├── SW12 corrective v3
       │    ├── SW12 rehearsal v3
       │    ├── SW17 corrective v4
       │    └── SW17 rehearsal v4
       └── SW09 ordinary rehearsal baseline
```

**Important:** Adapter config metadata in the published repos references the **exact public custom base** at `i-am-shaurya05/shadowwork-shift-plain-sft`. The original Kaggle-local config values remain under `provenance/original_adapter_config.json` and the LoRA tensors themselves were not changed by publication.

## Hugging Face: verified public model files

| Release | Hub repository | Key public files |
|---|---|---|
| Full original Plain SFT checkpoint | [Base model](https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft) | Full sharded custom checkpoint |
| SW08 Oracle BC v2 | [Parent LoRA](https://huggingface.co/i-am-shaurya05/shadowwork-shift-oracle-bc-v2) | Original adapter |
| SW09 frozen corrective starting adapter | [SW09 corrective](https://huggingface.co/i-am-shaurya05/shadowwork-shift-learner-corrective) | Original adapter |
| SW09 rehearsal baseline | [SW09 rehearsal](https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-bc) | Original comparator |
| SW12 corrective v3 | [Corrective v3](https://huggingface.co/i-am-shaurya05/shadowwork-shift-corrective-v3) | 120,981,200-byte `adapter_model.safetensors`, config, tokenizer, provenance |
| SW12 matched rehearsal v3 | [Rehearsal v3](https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-v3) | 120,981,200-byte adapter, config, tokenizer, provenance |
| SW17 corrective v4 | [Corrective v4](https://huggingface.co/i-am-shaurya05/shadowwork-shift-corrective-v4) | 120,981,200-byte adapter, config, tokenizer, provenance |
| SW17 matched rehearsal v4 | [Rehearsal v4](https://huggingface.co/i-am-shaurya05/shadowwork-shift-rehearsal-v4) | 120,981,200-byte adapter, config, tokenizer, provenance |

**Model collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac

Original SW17 v4 LoRA weight digests in `final_provenance.json`, matched against the publicly published `provenance/original_weights_sha256.txt` entries:

| Adapter | Exact SHA-256 |
|---|---|
| corrective v4 | `ebf7ed229641faf882f51d55c8aa0a12be748984cb7370d1399c236ab38bbff3` |
| rehearsal v4 | `36e4f7b0686029465899d2931bb15deaf95e77f310da2f9c8f57a29996f74b99` |

## Public datasets and executable evidence

**Dataset collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812

**Consolidated SW12/SW17 dataset with separately organized SW13–SW16 historical evidence:** https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets

| Dataset folder | Content published | Audit evidence |
|---|---|---|
| `sw12/` | 192 train, 32 dev, 64 sealed task specifications; 800-row corrective and 800-row rehearsal training JSONLs; 160 learner-visited train-only rollouts; 384 evaluated episode traces | `precommit.json`, `selection_audit.json`, `all_episode_scorecard.csv`, `grouped_summary.csv`, `*_training_metadata.json`, `final_provenance.json` |
| `sw17/` | 240 train, 40 dev, 80 sealed task specifications; 800-row corrective v4 and 800-row rehearsal v4 JSONLs; 160 train-only learner rollouts; 320 sealed evaluated episodes across four policies | `precommit.json`, `selection_audit.json`, `episode_scorecard.csv`, `policy_summary.csv`, `paired_tests.csv`, `learning_gate.json`, `final_provenance.json` |
| `historical/sw13_live/`, `sw14_controller/`, `sw15_cross_protocol/`, `sw16_unified/`, `sw16_budget/` | Separately archived historical synthetic controller/recovery evidence: scorecards, protocols, summaries and selected task files; not pooled with SW12/SW17 sealed outcomes | [Historical directory](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets/tree/main/historical), `historical/README.md`, root `sha256_release_manifest.json` |

The same dataset root also contains `README.md` (public Hugging Face dataset card), `DATASET_METHOD.md` and `sha256_release_manifest.json`. The SW17 Project ZIP itself has **497 files** with **496 verified SHA-256 commitments** including its local manifest. Those scientific records agree with the public SW17 scorecard: original frozen SW09 **31/80**, corrective v4 **65/80**, rehearsal v4 **65/80**, earlier v3 rehearsal **57/80**.

Original SW09 training and 70-task holdout evidence: https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training

For programmatic reproduction, see [DATASET_METHOD.md](DATASET_METHOD.md), [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and [the anonymous public release verifier](../scripts/verify_hf_public_release.py).

## Source notebooks and evidence archives

| Source | What it demonstrates |
|---|---|
| [SW17 fixed-controller learning attribution](../notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb) | Actual AgentTune/AuditKIT tool execution, fixed task split, learner rollouts, matched labels and LoRA training, paired replay scoring |
| [SW12 protocol-shift study](../notebooks/SW12_Closed_Loop_Adaptation.ipynb) | Synthetic protocol generation, v3 corrective vs rehearsal matched training, 64-task sealed evaluation |
| [Final Hugging Face publisher](../notebooks/FINAL_HF_Publish_From_Kaggle.ipynb) | Uploads already-trained v3/v4 adapters and exact SW12/SW17 artifacts, with anonymous verification |
| [SW17 result analysis](SW17_RESULTS.md) | 80-task outcome table, matched McNemar comparisons, final state and safety gate |
| [Result archive verifier](../scripts/verify_archived_results.py) | CPU-only reproduction of historical task summaries and archived episode checks |

Original Project-source ZIP archives retained separately: `ShadowWork_09_Final_Holdout_Evidence.zip`, `ShadowWork_12_Closed_Loop_Evidence.zip`, `ShadowWork_13_Live_Results.zip`, `ShadowWork_14_Controller_Repair_Results1.zip`, `ShadowWork_15_Cross_Protocol_Recovery_Results.zip`, `ShadowWork_16_Unified_Recovery_Results.zip`, `ShadowWork_16_Budget_Regression_Results.zip`, and `ShadowWork_17_Training_Attribution_Evidence.zip`. Selected SW13–SW16 extracted historical evidence is now also public under the consolidated dataset's `historical/` directory; the original ZIP files are not required to inspect the published scorecards.

## Immutable experiment commitments

- **SW09 original:** 70-case final holdout split and starting-adapter provenance, publicly released independently.
- **SW12 v3:** seed `20261113`; 192/32/64 task split; 800 rows per arm, 80 optimizer steps, LR `5e-5`, global batch 8; original SW09 starting-adapter digest `680659a3c6fce48e18f4ce8087b3fbb2c5806d4427e90c2b5cc6c49a524bb441`.
- **SW17 v4:** seed `20261115`; 240/40/80 split; 10 failure categories; 160 frozen starting-model train rollouts; each arm 400 shared anchors plus 400 differentiated rows, 800 total; 80 optimizer steps at the same LR/global batch; original SW09 starting-adapter digest identical to SW12.
- **SW17 split SHA-256:** train `6b2f73c0a0500656b071ca107f217bf3f1b6acb238d33bec0d211bb33caa71df`, dev `6d812921273d236524dbbebacb5117840bb17d3645c27b78610122c92442e06e`, sealed `789c656e798913bb3a9dbe0e19ef937a665f1782d33298d7b24e95c9f30cdb12`.
- **SW17 training JSONL SHA-256:** corrective `f52e2c97341107ec7ef14b9239781928d9aa3fadb37ec9b4d042a373d9a1b584`; rehearsal `1222b751f32b534031223050444d43d42dc1ba4a571474f5f6815698047eee3d`.

These checks link **exact serialized training rows, original frozen task splits, saved trained tensors, and sealed outcomes** into one auditable release. The experiment remains within related synthetic task environments, and the recorded authorization gate still controls deployment.
