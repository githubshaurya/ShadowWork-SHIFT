# ShadowWork-SHIFT | Final form handoff

**Track:** 3 — Agentic Fine-tuning

**Problem statement:** 8 — Self-healing agents

**Project title:** ShadowWork-SHIFT: Learning to Self-Heal Stateful Tool Agents with Verifiable Recovery

**Registered email:** Enter the email associated with the hackathon registration. Do not substitute a model-account email unless it is the registered one.

**Abstract (under 500 words):** Copy the current [submission/ABSTRACT.md](ABSTRACT.md) text, excluding its markdown title if the form has a separate title field. It is **384 words including links** as of November 16.

**Hugging Face model collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac

**Hugging Face dataset collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812

**GitHub repository:** https://github.com/githubshaurya/ShadowWork-SHIFT

**Primary write-up URL:** https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/README.md

**Extended technical write-up (if another field or optional comment):** https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/docs/TECHNICAL_REPORT.md

**Models and repositories used:** Cohere Tiny Aya-derived dense custom Plain SFT checkpoint; LEXSI AgentTune (`Project`, `ReActStrategy`, `DictToolHarness`) and LEXSI AuditKIT (`AgentEvalRunner`, `AgentEvalSpec`, `FinalStateAssertion`); TRL `SFTTrainer`, Hugging Face PEFT LoRA, Transformers/Accelerate/BitsAndBytes; Hugging Face Hub for released models, adapters, datasets and logs. **AgentTune handles agent execution; TRL/PEFT perform the LoRA parameter updates.**

**Core measurable result:** SW17 80 frozen-sealed synthetic tasks, common controller: frozen SW09 **31/80 (38.75%)**, corrective v4 **65/80 (81.25%)**, matched rehearsal v4 **65/80 (81.25%)**. Paired corrective–frozen: **38 wins / 4 losses, exact p = 5.65e−8**. Distinct SW12 shifted-protocol test: **24/64 frozen vs 46/64 corrective v3**.

**Safety statement:** The simulator prevents executed unauthorized state mutations; the SW17 evaluation detects eight forbidden-action proposals per v4 arm, so the policy deployment gate remains HOLD. This is the result of a measured, transparent safety decision. Training gain and policy-level authorization reliability are reported separately.

**Public verification:** [Release audit](../docs/PUBLIC_RELEASE_VERIFICATION.md) records an actual completed unauthenticated Hub API gate and exact published collection contents. Do not hold submission for an unnecessary historical evidence addendum.

## Action still requiring a human

Open the [official hackathon site](https://hackathon.lexsi.ai/) and use **Submit your project**. Enter the registered email and fields above, submit, and preserve the confirmation. **Deadline: November 15, 2026, 11:59 PM Anywhere on Earth = November 16, 2026, 5:29 PM IST.**

This is a complete form handoff, **not** a claim that an official submission was sent.
