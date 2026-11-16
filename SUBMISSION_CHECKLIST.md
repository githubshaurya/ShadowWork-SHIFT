# LEXSI first-round submission: final verified checklist

**Project:** ShadowWork-SHIFT · **Track:** 3, Agentic Fine-tuning · **Problem:** 8, Self-healing agents

**Official rules and form entrypoint:** https://hackathon.lexsi.ai/  
**First-round submission cutoff:** November 15, 2026, **11:59 PM Anywhere on Earth**, equivalent to **November 16, 2026 at 5:29 PM IST**.

## Technical project and public artifact requirements

- [x] **Dense Cohere open-weights model:** exact custom Tiny Aya-derived Plain SFT checkpoint published, with base-shard provenance.
- [x] **LEXSI SDKs actually integrated:** AgentTune `Project`, `ReActStrategy` and `DictToolHarness`; AuditKIT `AgentEvalRunner`, `AgentEvalSpec` and `FinalStateAssertion` in the runnable SW17 notebook. Explicitly disclose TRL/PEFT as the actual SFT/LoRA weight optimizer.
- [x] **Real model training:** two distinct SW17 LoRA adapters optimized 80 steps each from an identical frozen SW09 start with 800-row matched datasets, LR 5e-5 and global batch 8; original weight and dataset hashes retained.
- [x] **Meaningful before/after metrics:** frozen original SW09 **31/80** vs corrective v4 **65/80** and matched rehearsal v4 **65/80** strict success under identical fixed-controller conditions. Exact corrective–frozen paired p=5.65e-8. State, evidence, unsafe proposals and model-call counts also published.
- [x] **Explicit safety / redeployment gate:** Tool authorization blocks forbidden mutation execution; SW17 authorization stress test records 8 unsafe proposals per v4 arm, and the policy deployment gate correctly remains `deploy=false`.
- [x] **Public GitHub source and write-up:** [README](README.md), [technical report](docs/TECHNICAL_REPORT.md), [abstract](submission/ABSTRACT.md), [dataset construction](docs/DATASET_METHOD.md), [SW17 notebook](notebooks/SW17_Fixed_Controller_Learning_Attribution_Kaggle.ipynb), [reproduction guide](docs/REPRODUCIBILITY.md).
- [x] **Exact original base public:** https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft
- [x] **SW09 original models and evidence public:** original corrective and rehearsal adapters + training/evaluation data.
- [x] **Four SW12/SW17 final adapters public:** corrective/rehearsal v3 and corrective/rehearsal v4, each with **120,981,200-byte LoRA weights** and unmodified original SHA-256 provenance. [Model collection](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac).
- [x] **Exact training data, tasks and logs public:** [Consolidated dataset](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets), 160+160 train-only rollouts, 384 SW12 + 320 SW17 evaluated episodes, training JSONLs, scorecards, paired tests, precommits, SHA-256 manifest and dataset card. [Dataset collection](https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812).
- [x] **Published collection membership verified:** user-executed Kaggle publisher source shows eight model entries and both data entries in the existing collections.
- [x] **Independent anonymous verification passed:** completed publisher checked files and collection membership with `HfApi(token=False)`, final output `PUBLIC RELEASE GATE PASS`. [Evidence ledger](docs/PUBLIC_RELEASE_VERIFICATION.md).
- [x] **SW17 Project ZIP integrity audited:** all 496 original archive member hashes pass; policy scores and exact paired tests recomputed.
- [x] **Strong abstract and write-up ready:** [form handoff](submission/FORM_READY.md) and [384-word abstract](submission/ABSTRACT.md).
- [x] **Public repository satisfies public demonstration/repository requirement:** https://github.com/githubshaurya/ShadowWork-SHIFT

## Required final participant action

- [ ] Enter the **registered participant/team email** in the form (not available to the assistant).
- [ ] Open **Submit your project** at https://hackathon.lexsi.ai/ and paste the [form-ready values](submission/FORM_READY.md).
- [ ] Submit the project **before 5:29 PM IST on November 16, 2026**.
- [ ] Preserve the official submission confirmation, submission identifier, or final success page.

## Deliberate scope choices (no blocker)

- **Historical SW13–SW16 archives:** retained in Project and described in the technical report but not included in the consolidated HF dataset. The core SW17 learning audit is complete; however, the official rule to host **all** created logs makes archiving these earlier traces on HF the conservative option for literal-completeness assurance. Keep them in an isolated `historical/` subdirectory or separate historical dataset if published.
- **Independent external benchmark:** not required for this first-round hackathon; SW17's prespecified synthetic schema shift is disclosed precisely.
- [x] **Hugging Face cleanup verified:** the public dataset card is byte-for-byte identical to the canonical GitHub card, with the finalized SW17 results; the empty placeholder `i-am-shaurya05/shadowwork-shift-models` no longer exists. Core model adapters, datasets, and both collections remain intact.
- **HF Space / video / slides:** optional for first-round submission because an accessible public GitHub repository and write-up satisfy the official public-project condition. Shortlisted teams can use these for final judging.
- **Browser-only HF collection UI:** a separate ordinary-browser check was not available inside this assistant environment. Actual completed anonymous API publication verification **did pass** and proves the public release and collection memberships; there is no technical publication blocker.
- **Deployment:** the training improvement gate and production deployment gate are intentionally distinct; `deploy=false` is a safety-control result, not an incomplete artifact.

**Status:** the **primary** model/data release, GitHub write-up, LEXSI SDK integration and numerical SW17 audit are complete. The only unconfirmed **mandatory participant action** is the official submission form. Optional release polish: synchronize HF's older mirrored `DATASET_METHOD.md` with the newly audited GitHub method; publish historical SW13–SW16 logs on HF to avoid any strict-reading ambiguity in the organizer's all-artifacts rule. A full fresh-environment GPU rerun has not been independently performed in this audit.
