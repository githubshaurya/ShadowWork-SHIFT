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
- [x] Four actual public SW12 v3 and SW17 v4 LoRA adapters uploaded (each includes 120,981,200-byte weights, config, tokenizer and provenance), confirmed by direct Hub listings and executed anonymous verifier.
- [x] The [SW12 v3 + SW17 v4 CPU-only Kaggle publisher](notebooks/FINAL_HF_Publish_From_Kaggle.ipynb) finished successfully. Exact source notebook execution is preserved in the Project source.
- [x] Exact SW12/SW17 training JSONLs, train/dev/sealed task splits, 160 train-only rollouts per study, 384 SW12 evaluation traces, 320 SW17 sealed evaluation traces, scorecards, methodology and dataset card publicly uploaded. Source/release SHA-256 checks pass.
- [ ] SW13–SW16 historical source ZIPs were not attached in the successful publisher run; publish the verified historical bundle using [CPU-only evidence addendum](notebooks/FINAL_HF_Publish_Historical_Evidence_Addendum.ipynb).
- [x] All four updated model repos and consolidated dataset repo added to existing HF collections; exact item lists printed by the executed publisher and confirmed by its `token=False` collection verification.
- [x] The executed publisher's anonymous `HfApi(token=False)` release gate passed; the connected HF file browser independently lists four complete model repositories and SW12/SW17 dataset files.
- [ ] Verify collection URLs in an ordinary browser (collection metadata visible but file-browser collection read returned an access error).
- [x] Programmatic anonymous Hugging Face release-gate checks passed in the completed publishing notebook. Manual ordinary-browser verification remains separately open.
- [x] Core SW09/SW12/SW14/SW15/SW16 notebooks and SW16 budget repair notebook uploaded to GitHub.
- [x] Offline result verification script added; source-archive ZIPs must be supplied by the user when running it.
- [ ] Optional: independent small replay/smoke test using the public model/adapter path.
- [ ] Refresh README and submission write-up to remove *empty/pending upload* claims and lead with confirmed SW17 results, matched-rehearsal tie, and forbidden-action failures. The user requested write-up editing later.

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

- [x] SW17 fixed-controller training gains disclosed (31/80 frozen vs 65/80 corrective v4 and 65/80 rehearsal v4). 
- [x] SW17 forbidden-action safety failures disclosed (8/8 unsafe proposals per v4 arm), final deployment HOLD. 
- [x] Transparent dataset generation, scripted-reference labels and matched-control methodology documented. 
- [x] Fixed-controller training comparisons disclosed.
- [x] Rehearsal stronger than corrective v3 disclosed.
- [x] Controller gains separated from LoRA gains.
- [x] SW16 deployment HOLD and v5 focused PASS distinguished.
- [x] Synthetic task and external-generalization limits disclosed.
- [x] Original v3 weight SHA-256 values recomputed from Project SW12 archive and matched public model provenance; v4 provenance hashes matched SW17 Project archive. All four uploaded training JSONL hashes matched the public SHA manifest; SW17 320-row scorecard and paired tests recomputed from Project evidence.

**No claim of completed submission** until the form is submitted and each required public artifact is confirmed.
