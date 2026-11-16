# Submission abstract (under 500 words)

**ShadowWork-SHIFT: Learning to Self-Heal Stateful Tool Agents with Verifiable Recovery**

**Headline: 31/80 → 65/80 strict successes (+42.5 percentage points) after fine-tuning, with the controller held fixed.**

Tool-using AI agents often fail in ways ordinary answer-based benchmarks miss: a successful-looking write that never persists, a stale read, an expired lease, a misleading commit receipt, or an unauthorized state change. **ShadowWork-SHIFT** builds an end-to-end, evidence-grounded self-healing agent pipeline for **LEXSI Track 3, Problem 8** using a **Cohere Tiny Aya-derived open-weights checkpoint**, **LEXSI AgentTune** for stateful ReAct tool execution, **LEXSI AuditKIT** for agent-episode verification, and **TRL/PEFT** for actual LoRA fine-tuning.

Our pipeline (1) generates executable, fault-injected SQLite maintenance tasks, (2) collects frozen-agent tool trajectories, (3) identifies learner-visited decisions requiring repair, (4) constructs reference-labeled corrective training examples, (5) fine-tunes two matched adapters, and (6) evaluates durable state, verification evidence, authorized behavior, and deployment gates. Training rows and task splits are precommitted with SHA-256 hashes and published alongside per-episode traces and model weights.

**Crucially, we isolate training from runtime controller engineering.** In SW17, both new v4 adapters start from the same frozen SW09 model, receive **800 training rows and 80 optimizer steps each**, and face the **same 80 sealed tasks** under the identical four-read bootstrap with **no extra post-read repair controller**. The frozen model succeeds on **31/80 (38.75%)**, while corrective v4 reaches **65/80 (81.25%)**: **38 paired wins, four losses, exact McNemar p = 5.65 × 10⁻⁸**. Matched expert rehearsal also reaches **65/80**. This strengthens the central finding, **measurable improvement from learned model adaptation**, while the paired control accurately limits claims about any uniquely superior training curriculum. A separate SW12 protocol-shift experiment independently records **24/64 → 46/64** for corrective v3.

Our system treats evaluation as a deployment decision, not merely a leaderboard number. SW17 detects eight forbidden-action proposals per v4 arm; its executable authorization gate blocks them, and the deployment decision remains **HOLD**, even when the learning-improvement gate passes. This is an explicit, inspectable defense rather than an unsupported safety claim.

**All key artifacts are public**: the exact custom model base, trained v3/v4 LoRA adapters, matched training datasets, learner rollouts, sealed evaluation trajectories, audit scorecards, generation methodology, and notebooks.

**Track:** 3 · **Problem:** 8 · **SDKs:** AgentTune + AuditKIT · **Training:** TRL/PEFT LoRA

**Model collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-models-and-frozen-adapters-6af5c8a5a548fb703ab420ac

**Dataset collection:** https://huggingface.co/collections/i-am-shaurya05/shadowwork-shift-training-data-and-audit-evidence-6af5c8a51d44c02ee6e19812

**GitHub and full write-up:** https://github.com/githubshaurya/ShadowWork-SHIFT
