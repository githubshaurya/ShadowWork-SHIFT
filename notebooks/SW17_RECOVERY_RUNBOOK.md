# SW17 second-arm recovery: historical troubleshooting runbook

**Status (16 November 2026): resolved.** Both SW17 v4 adapters completed training and the fixed-controller sealed evaluation was published. The steps below document an earlier interrupted Kaggle training session and its recovery procedure; they are **not outstanding work**. For final results, see [the SW17 result report](../docs/SW17_RESULTS.md) and [public scored evidence](https://huggingface.co/datasets/i-am-shaurya05/shadowwork-shift-datasets/tree/main/sw17).

**Evidence already observed (16 November 2026).**

- Runtime: Python 3.13.16; torch 2.11.0+cu130; TRL 1.7.1; Transformers 5.17.0; PEFT 0.21.2; Accelerate 1.15.0; datasets 4.8.5; pyarrow 23.0.1; bitsandbytes 0.49.2.
- `rehearsal_v4` completed **80/80 steps**, loss ~0.003893 in the last interval, adapter saved under `/kaggle/working/shadowwork/17_training_attribution/rehearsal_v4_adapter`.
- `learner_corrective_v4` loaded its model and verified pretokenized data, then failed while constructing DDP: rank 1 got NCCL remote-peer connection refused in `_verify_params_across_processes`.
- Rank 0's initiating failure was **not captured**. We cannot conclude whether the original cause was host OOM, GPU fault, stale distributed resources or another termination. The first arm's success argues against a basic incompatibility of the entire environment.
- **Do not rerun rehearsal or change package versions solely because of the rank 1 NCCL error.** Matching already-frozen training arms matters for the learning comparison.

## Recovery in the *same Kaggle runtime*

1. Verify that `/kaggle/working/shadowwork/17_training_attribution/rehearsal_v4_adapter/adapter_model.safetensors` and `rehearsal_v4_training_metadata.json` exist. Also verify both `*_v4_training.jsonl` files.
2. Keep this notebook's original Kaggle runtime and its `/kaggle/working` storage; **restart the Python/Jupyter kernel only**, not a new notebook/session that discards temporary files.
3. Use the latest SW17 GitHub notebook cells. Reexecute setup, split creation, CPU preflight and training-row construction. The patched collection cell validates all 160 saved rollout JSONs and skips GPU collection. The training cell validates the completed rehearsal weights/metadata and launches **only corrective v4**.
4. Wait for 80/80 optimizer steps and the final `Saved adapter` message. Don't infer evaluation quality from training loss alone.
5. **Restart the kernel again** before inference evaluation. Rerun the non-GPU setup cells. The patched training cell sees both arms completed and trains nothing.
6. Run the patched evaluation cell, which does **one** two-GPU launch and evaluates the frozen parent, corrective v4, rehearsal v4 and optional previous rehearsal v3 sequentially within each worker. Results are incrementally saved by task/policy and verified by hash when resuming.
7. Run the scorecard/paired-significance and ZIP export cells. Do not look at sealed results until both models are trained. Report directional differences honestly.

**Do not** replace this experiment's pinned versions or change `max_steps`, LR, seeds, model source, prompts, split commitments, LoRA parameters, or evaluation controller to make the numbers more favorable.

## If the single fresh-kernel corrective launch still fails

The evidence so far does not expose rank 0's primary error. On the Kaggle host, use a separate CPU-only diagnostics cell to inspect cgroup OOM counters before and after the attempt:

```python
from pathlib import Path
events = Path("/sys/fs/cgroup/memory.events")
print(events.read_text() if events.exists() else "cgroup memory events unavailable")
```

If `oom_kill` increases during the failed run, that supports a host/cgroup OOM cause. If it doesn't, retrieve **rank 0's first error, exit code, and the PyTorch elastic rank-0 error file** rather than treating rank 1's NCCL socket error as causal. `NCCL_DEBUG=INFO` and `TORCH_DISTRIBUTED_DEBUG=INFO` can help diagnose another failure, but do not modify numerical training options during the matched comparison.

## Sources

- [Accelerate notebook launcher usage and CUDA initialization rules](https://huggingface.co/docs/accelerate/basic_tutorials/notebook)
- [PyTorch distributed process-group shutdown](https://docs.pytorch.org/docs/stable/distributed.html#shutdown)
- [NVIDIA NCCL runtime and container troubleshooting](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/runtime_and_mpi_issues.html)
