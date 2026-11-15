# Submission abstract (under 500 words)

**ShadowWork-SHIFT: Self-Healing Stateful Tool Agents with Corrective Adaptation and Evidence-Grounded Recovery**

Agents operating stateful tools can fail even when their output parses correctly: writes can silently do nothing, return stale values, conflict with concurrent state, or be acknowledged without persisting. An agent may then declare success without sufficient evidence, or attempt an unauthorized mutation. ShadowWork-SHIFT targets LEXSI Track 3's self-healing agents problem with a compact Cohere Tiny Aya-derived policy, AgentTune tool execution, AuditKIT state-checked evaluation, corrective LoRA adaptation using TRL/PEFT, and conservative runtime recovery with explicit deployment gates.

We collect learner-visited failure states, construct corrective continuations, compare matched rehearsal controls, and separate model improvements from controller effects. On a 70-task sealed SW09 holdout, the original parent policy achieves 42/70 strict success while the corrective adapter reaches 70/70; a simple deterministic stopping controller on the parent already reaches 69/70, showing why controller attribution matters. On a shifted SW12 sealed 64-task protocol, original corrective reaches 24/64, corrective v3 reaches 46/64, and matched rehearsal v3 reaches 47/64 without the final unified controller. On 160 SW12 core/composed tasks using an identical unified controller, these models respectively achieve 132/160, 154/160 and 160/160. A final focused budgeted-controller repair yields 316/320 strict successes across two v3 model arms and 320/320 correct persistent states, with no executed forbidden mutations in the evaluated episodes.

The key finding is that failure detection, task-grounded adaptation and bounded evidence-aware runtime control can markedly improve workflow reliability, while ordinary rehearsal remains a strong and sometimes superior training baseline. Our results cover controlled synthetic workflows, not independent real-world production generalization. We release the source notebooks, evaluation protocols, training datasets, model adapters, and trace evidence for reproducibility.

**Track:** 3 (Agentic fine-tuning). **Problem:** 8 (Self-healing agents).  
**Code:** https://github.com/githubshaurya/ShadowWork-SHIFT  
**Full write-up:** https://github.com/githubshaurya/ShadowWork-SHIFT/blob/main/docs/TECHNICAL_REPORT.md

*Release note: Do not submit this abstract until the advertised public model/dataset releases and both HF collections are complete.*
