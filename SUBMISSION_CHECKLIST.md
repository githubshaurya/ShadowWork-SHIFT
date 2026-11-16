# First-round submission checklist — LEXSI Track 3, Problem 8

**Official instructions:** https://hackathon.lexsi.ai/  
**Deadline:** November 15, 2026 at 11:59 PM **Anywhere on Earth** (November 16, 2026 at 5:29 PM IST).

## Required public resources

- [x] Public GitHub repository: https://github.com/githubshaurya/ShadowWork-SHIFT
- [x] Written report and reproducibility guidance in the repository.
- [x] Exact Plain SFT base published with verified 7-shard hash metadata: https://huggingface.co/i-am-shaurya05/shadowwork-shift-plain-sft
- [x] SW08 and SW09 original adapters published: https://huggingface.co/i-am-shaurya05/shadowwork-shift-learner-corrective
- [x] SW09 original training and holdout evidence published: https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-evidence-and-training
- [x] Existing Hugging Face model **collection located**: https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac
- [x] Existing Hugging Face dataset **collection located**: https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812
- [x] New public repository shells created for the two SW12 v3 adapters and SW12–SW16 evidence.
- [ ] Upload SW12 v3 and SW17 v4 corrective/rehearsal complete adapters with the [updated CPU-only Kaggle publisher](notebooks/FINAL_HF_Publish_SW12_SW17_From_Kaggle.ipynb).
- [ ] Upload exact SW12 and SW17 training JSONLs, splits, train-only learner rollouts, scoring files, trace evidence and dataset card; attach available SW13–SW16 source ZIPs.
- [ ] Add new repos to the existing model and dataset collections; verify resulting membership.
- [ ] All released model/dataset files verified publicly downloadable and ungated.
- [ ] Verify collection URLs in an ordinary browser (collection metadata visible but file-browser collection read returned an access error).
- [ ] Public-link access verified without user login.
- [x] Core SW09/SW12/SW14/SW15/SW16 notebooks and SW16 budget repair notebook uploaded to GitHub.
- [x] Offline result verification script added; source-archive ZIPs must be supplied by the user when running it.
- [ ] Optional: independent small replay/smoke test using the public model/adapter path.

## Required form fields

- [ ] Registered participant/team email (participant supplies).
- [ ] Submission abstract (under 500 words; see `submission/ABSTRACT.md`).
- [ ] Hugging Face **model collection** URL, not only model repo URL.
- [ ] Hugging Face **dataset collection** URL, not only dataset repo URL.
- [ ] GitHub repository URL.
- [ ] Write-up URL (GitHub README/report is accepted).
- [ ] Track: **3 — Agentic fine-tuning**.
- [ ] Primary problem statement: **8 — Self-healing agents**.
- [ ] Repos/models used: Cohere Tiny Aya-derived model + AgentTune + AuditKIT; TRL/PEFT identified accurately.
- [ ] Final submit and confirmation recorded by participant.

## Safety and accuracy checks

- [x] SW17 fixed-controller training gains disclosed (31/80 frozen vs 65/80 corrective v4 and 65/80 rehearsal v4).\n- [x] SW17 forbidden-action safety failures disclosed (8/8 unsafe proposals per v4 arm), final deployment HOLD.\n- [x] Transparent dataset generation, scripted-reference labels and matched-control methodology documented.\n- [x] Fixed-controller training comparisons disclosed.
- [x] Rehearsal stronger than corrective v3 disclosed.
- [x] Controller gains separated from LoRA gains.
- [x] SW16 deployment HOLD and v5 focused PASS distinguished.
- [x] Synthetic task and external-generalization limits disclosed.
- [ ] Verify correct public v3/v4 weight files, complete SW12/SW17 training JSONLs, sealed traces, and generated SHA-256 release manifest after upload.

**No claim of completed submission** until the form is submitted and each required public artifact is confirmed.
