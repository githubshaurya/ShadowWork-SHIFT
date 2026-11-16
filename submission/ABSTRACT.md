# Submission abstract (under 500 words)

**ShadowWork-SHIFT: Self-Healing Stateful Tool Agents with Learned Adaptation and Evidence-Grounded Recovery**

Tool-using agents can misinterpret acknowledged-but-unpersisted writes, stale observations, concurrent write conflicts and insufficient verification as task completion. ShadowWork-SHIFT implements a measured self-healing pipeline for LEXSI Track 3, Problem 8, with a Cohere Tiny Aya-derived custom checkpoint, AgentTune tool execution, AuditKIT episode verification, actual TRL/PEFT LoRA fine-tuning, and explicit authorization and redeployment gates.

We generate executable, synthetic SQLite maintenance workflows with predefined fault schedules and policy constraints; precommit train/development/sealed task IDs and SHA-256 hashes; collect actual frozen-learner tool traces on training tasks; label learner-visited failure states using a scripted observation-based reference policy; replay histories and verify reference trajectories against persisted state; and build equal-budget corrective and matched-rehearsal training datasets. The original training JSONLs, task generators, decision traces, evaluation evidence and honest dataset card are released for reproducibility. Reference labels are **programmatic**, not independently human-annotated.

SW12's precommitted shifted-protocol 64-task comparison gave **24/64** strict success for frozen SW09 corrective, **46/64** for corrective v3 and **47/64** for matched rehearsal v3 under the same evaluation setup. SW17 then used a new precommitted 80-task suite with an identical four-read bootstrap and **no additional repair controller**. Frozen SW09 scored **31/80**, corrective v4 **65/80**, and equal-budget rehearsal v4 **65/80**. Corrective fine-tuning gained **34/80 successes (+42.5 percentage points)** over its frozen starting model (38 paired wins, four losses, exact McNemar `p=5.65e-8`); corrective and rehearsal were tied (five wins and five losses; `p=1`). The conclusion is **demonstrated learned adaptation**, not demonstrated superiority of learner-state correction over ordinary rehearsal.

The evaluation also exposed a vital safety limitation: **both v4 policies made unsafe mutation proposals in all eight authorization-forbidden SW17 tasks**, causing 0/8 strict successes per v4 arm in that group. The simulator's authorization gate blocked those attempts; they were not permitted tool mutations. Consequently, **the deployment decision is HOLD**, despite the significant learning gain. All tasks remain synthetic and related; no independent production-transfer or universal safety claim is made.

**Track:** 3 (Agentic fine-tuning). **Problem:** 8 (Self-healing agents).  
**Code:** https://github.com/githubshaurya/ShadowWork-SHIFT  
**Dataset construction:** https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/docs/DATASET_CONSTRUCTION.md  
**Full write-up:** https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/docs/TECHNICAL_REPORT.md

*Release status: verify the final SW12+SW17 public Hugging Face model/data uploads and both collections before entering their links in the official submission form.*
