# Reproducing ShadowWork-SHIFT

This project uses GPU-intensive Kaggle notebooks and **local-path model dependencies**. The measured experiments should be reproduced from the *exact* custom Plain SFT checkpoint; downloading any random Cohere model with a similar name is not equivalent.

## Hardware and environment

Original runs used Kaggle **2 × NVIDIA T4**. The SW09 extracted-input notebook pins AuditKIT `1.1.7`, AgentTune at Git commit `e56a1094b65cbf7c2c0b26d0db2ac4dffffa693a`, TRL `1.7.1`, PEFT `0.21.2`, Transformers `5.17.0`, Accelerate `1.15.0`, and BitsAndBytes `0.49.2`. Later notebooks may pin a slightly different environment; **respect each notebook's own dependency cell**. These were recorded versions, not guarantees that a fresh environment in future dates will resolve all dependencies.

## Training order

1. **Base**: Load the [already-published exact custom Plain SFT checkpoint](https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft) or the original Kaggle path `/kaggle/input/datasets/shaurya466/shift-plain/shadowork_123`. The seven public shard-hash commitments match SW09 `base_hashes.json`.
2. **SW08 Oracle BC v2**: Use the adapter from `ShadowWork_09_Kaggle_Input_Bundle.zip`. It is the parent for SW09 adaptation, not a standalone base model.
3. **SW09 original learner-state corrective**: Run `ShadowWork_09_Kaggle_Extracted_Input_Ready.ipynb` using the prepared inputs and v2 adapter in the same Kaggle input bundle. The notebook collects 140 train-only workflows, creates matched training rows and runs the corrective and on-policy comparator arms. Keep the separate final 70-case holdout detached.
4. **SW09 sealed holdout**: Use `ShadowWork_09_Final_Holdout_Extracted_Kaggle_Ready.ipynb`; verify split commitment before evaluation.
5. **SW12 shifted-protocol retraining**: Run `ShadowWork_12_Closed_Loop_Adaptation_Kaggle.ipynb` with the *frozen SW09 corrective adapter* as starting point. Both v3 policies receive equal-row/step matched training. Do not use SW12 sealed examples for training.
6. **SW13–16**: Run paired controller comparisons from the saved v3 adapters, never retrain implicitly when evaluating a controller. The final SW16 budgeted repair notebook uses the previous unified result as a **frozen comparison**, not a new independent model-training experiment.

## Evaluation and analysis

- Score `strict_success`, `state_correct`, `evidence_supported`, raw `unsafe_proposals`, and `executed_forbidden_mutations` separately.
- Group comparisons by `suite`, `policy`, and `controller`. Verify equal task IDs before paired significance testing.
- For two-sided exact McNemar statistics, compute from *discordant pairs* `wins` and `losses`, not from independent standard-error formulas.
- Preserve absolute paths only as **input instructions**; they are not valid public model base identifiers.
- Verify outputs against the `results/` tables and source ZIP members; SHA-256 manifests are available for core stages.

## End-to-end vs partial reproduction

A source archive replay and metric aggregation can run without GPU once the scored episode logs have been downloaded. See [the offline verification script](../scripts/verify_archived_results.py). Full model inference/training requires the custom full-precision base checkpoint, correct adapter, original tokenizer/chat template, fixed seeds and environment. The custom full Plain SFT base and SW08/SW09 adapters are already public. The release remains incomplete until the two SW12 v3 adapters and latest evaluation evidence are uploaded and checked for public accessibility. Use [this Kaggle publication notebook](../notebooks/FINAL_HF_Publish_From_Kaggle.ipynb).

## LEXSI component provenance

AgentTune components in SW09 and SW16 provide execution integration and recorded tool-event behavior; AuditKIT provides recorded-evaluation checks. SW12's optimization uses Hugging Face TRL+PEFT LoRA. This avoids conflating AgentTune execution integration with optimizer ownership.

## Security

Never commit Hugging Face tokens, Kaggle secrets, SSH private keys or private system paths containing credentials. Store a write-enabled HF token in **Kaggle Secrets**. The publishing notebook should validate file counts/hashes before upload, mark repos public, and print public readback URLs afterward.
