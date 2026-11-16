# Public release verification: ShadowWork-SHIFT

**Audit date:** 16 November 2026. **Scope:** first-round public artifact submission for LEXSI Track 3, Problem 8. This verifies the actual published trained adapters and SW12/SW17 primary dataset; it is not a new experiment.

## 1. Publication evidence from the executed Kaggle notebook

The completed user-executed Kaggle publisher was preserved in Project sources as `notebookc285845831 (1).ipynb`; its publication logic is available in the [GitHub publication notebook](../notebooks/FINAL_HF_Publish_From_Kaggle.ipynb). It has no Python error outputs; code execution cells 1, 3, 5, 7, 9 and 11 completed in sequence. Its final `HfApi(token=False)` verification cell printed:

> PUBLIC RELEASE GATE PASS: four model adapters, exact training data, two collections, episode evidence, and dataset method visible without login.

This test deliberately disabled the Hugging Face token to simulate judge access. The same completed notebook printed the exact collection contents:

**Model collection:**
- `i-am-shaurya05/shadowwork-shift-plain-sft`
- `i-am-shaurya05/shadowwork-shift-oracle-bc-v2`
- `i-am-shaurya05/shadowwork-shift-rehearsal-bc`
- `i-am-shaurya05/shadowwork-shift-learner-corrective`
- `i-am-shaurya05/shadowwork-shift-corrective-v3`
- `i-am-shaurya05/shadowwork-shift-rehearsal-v3`
- `i-am-shaurya05/shadowwork-shift-corrective-v4`
- `i-am-shaurya05/shadowwork-shift-rehearsal-v4`

**Dataset collection:**
- `i-am-shaurya05/shadowwork-shift-evidence-and-training`
- `i-am-shaurya05/shadowwork-shift-datasets`

The public API verifier reported **1,058 public dataset files** at the time of execution, including all required SW12/SW17 task and training files. A separate connected Hugging Face file browser independently displayed the four trained v3/v4 adapter file inventories (each **120,981,200-byte safetensors file**) and both `sw12/` and `sw17/` dataset folders. All four adapters report `peft_type=LORA`, rank 16 and the correct public custom full base `i-am-shaurya05/shadowwork-shift-plain-sft`.

## 2. SW17 original archive and published data agreement

The exact Project-source `ShadowWork_17_Training_Attribution_Evidence.zip` contains **497 ZIP members**: 496 original files and its own `evidence_sha256_manifest.json`. The ZIP CRC check passes and **every recorded original SHA-256 matches** the underlying file. It contains the original train/dev/sealed JSONLs, 160 frozen learner collection rollouts, 320 sealed scored agent episodes, both exact 800-row v4 training JSONLs, metadata, scorecards, paired tests and model-weight fingerprints.

The public `sw17/` folder was independently enumerated: **496 files**, consisting of the same 160 train-only rollouts, **80 episodes per frozen SW09, corrective v4, rehearsal v4 and prior rehearsal v3** and 16 root metadata/results files. The project and published metadata agree on the frozen split hashes and model-weight fingerprints.

| SW17 original trained LoRA | Original SHA-256, present in publicly released provenance |
|---|---|
| Corrective v4 | `ebf7ed229641faf882f51d55c8aa0a12be748984cb7370d1399c236ab38bbff3` |
| Rehearsal v4 | `36e4f7b0686029465899d2931bb15deaf95e77f310da2f9c8f57a29996f74b99` |

The exact SW17 training datasets contain **800 rows per arm**. The learner-state selection audit records 160 train-only rollouts, 1,311 learner-visited states, 859 learner/reference mismatch candidates, 400 selected learner-state examples, 211 actual corrections, and **395/400 exact action-stratum matches** for the rehearsal control. The `precommit.json` preserves seed `20261115` and 240/40/80 train/dev/sealed task identity boundaries.

## 3. SW17 metric reproduction from original scored episodes

| Policy | Strict success | Correct persisted state | Evidence supported | Unsafe proposals |
|---|---:|---:|---:|---:|
| Frozen SW09 corrective | 31/80 | 58/80 | 54/80 | 6 |
| Corrective v4 | 65/80 | 77/80 | 73/80 | 8 |
| Rehearsal v4 | 65/80 | 80/80 | 77/80 | 8 |
| Previous rehearsal v3 | 57/80 | 75/80 | 60/80 | 2 |

The 320-row episode-level scorecard reproduces the exact paired tests: corrective vs frozen **38 wins, 4 losses, p=5.65314621780999e−8**; rehearsal vs frozen **36 wins, 2 losses, p=5.398760549724102e−9**; corrective vs rehearsal **5 wins, 5 losses, p=1.0**. These comparisons hold the four-read bootstrap and evaluation task IDs constant, isolating the influence of continued training as far as the controlled experimental design permits.

The model's proposed unauthorized mutations remain explicitly separate from *executed* forbidden state changes, and the recorded policy deployment decision is **HOLD**.

## 4. SW12 public evidence

The public `sw12/` directory contains **558 files**: 160 train-only learner rollouts, 384 evaluated episode records and 14 root data/score/provenance files, plus directory entries. Both 800-row SW12 training JSONLs are present, and their recorded release hashes match the source archives. The two public v3 model provenance files match the original adapter weight hashes:

- SW12 corrective v3: `f1bf0dedc42b65d60f8f39563f6c569f7d15c72dd1d1b5266f83e501e59da741`
- SW12 rehearsal v3: `fb693d1907fdd6a714bbfd0e664a8cb6091c325146f524e0e0a2f7b68e5c866f`

## 5. URLs checked and release boundary

- **Models collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac
- **Datasets collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812
- **Primary dataset:** https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets
- **Main code and report:** https://github.com/githubshaurya/ShadowWork-SHIFT
- **Anonymous release-verifier script:** https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/scripts/verify_hf_public_release.py

The **programmatic anonymous Hugging Face collection membership checks passed** in the completed publisher run. These are recorded API checks; an independent graphical-browser check of the collection pages was not part of that audit. The participant subsequently confirmed receipt of the first-round hackathon form, documented separately in the [submission checklist](../SUBMISSION_CHECKLIST.md).

## 6. Reproducible data-quality and score verification

The new [CPU-only public SW17 evidence verifier](../scripts/verify_sw17_public_evidence.py) provides a stricter independent audit than model/dataset existence checks alone. It recomputes the SHA-256 of **every one of the 496 public SW17 files** against the release manifest, verifies the **240/40/80 disjoint task splits**, confirms the real **160-rollout / 1,311-state / 859-disagreement-candidate / 400-selection / 211-actual-correction** dataset lineage, and checks the **395/400 exact rehearsal-stratum matches**, **400 common anchors**, both **80-step training logs**, all **320 sealed episode outcomes**, and the exact paired McNemar tests.

The checking logic was tested on the original local SW17 evidence ZIP with an offline substitute for the Hub download layer and printed `SW17 PUBLIC EVIDENCE AUDIT PASS`. The script's **network download path has not yet been run end-to-end** in this audit environment; it is provided so judges can run it anonymously against the public files. Full SQLite action-by-action **replay** is implemented separately in the source SW17 notebook.

**Release scope (updated 16 November 2026):** the main SW09/SW12/SW17 experiment record is public; selected inspectable SW13–SW16 controller-development scorecards, protocols and summaries have also been published in the [consolidated dataset's `historical/` directory](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets/tree/main/historical). These are separate historical synthetic evaluations, not additional SW12/SW17 sealed cases. Original source ZIP archives remain retained as Project evidence.

**Latest public manifest audit (16 November 2026, after historical publication):** `sha256_release_manifest.json` retains exactly **558 SW12 and 496 SW17 data-file entries**, plus the subsequently published historical entries. The previously identified root metadata mismatch is **resolved**: the live Hugging Face `README.md` has SHA-256 `a8029f98ce5c2b81462f8c264bbff73b86715faa3a471c1335b808e842544ed3`, exactly matching the current release manifest. The live `DATASET_METHOD.md` has SHA-256 `eaa34f56e41620b93ccf47589ed99360d41b037f3f391c10ae7a2b87513b1b1a`, also matching its current manifest entry. These two hashes were recalculated from public file text, not inferred from file names. The primary SW12/SW17 manifest entries remain preserved; the public-checking script remains available for a more exhaustive file-by-file audit.

**Methodology synchronization:** the public Hugging Face `DATASET_METHOD.md` is now text-identical to [the GitHub methodology](DATASET_METHOD.md), including the executed SW17 counts, worked learner-state example and matched evaluation details. No dataset-methodology synchronization remains pending.

