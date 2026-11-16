"""Independently verify the public ShadowWork-SHIFT Hugging Face release.

Requires: huggingface_hub (no token, GPU or project files).
Run as one notebook cell or paste into a Python notebook.
"""

from huggingface_hub import HfApi

owner = "i-am-shaurya05"
dataset = f"{owner}/shadowwork-shift-datasets"
models = [
    f"{owner}/shadowwork-shift-corrective-v3",
    f"{owner}/shadowwork-shift-rehearsal-v3",
    f"{owner}/shadowwork-shift-corrective-v4",
    f"{owner}/shadowwork-shift-rehearsal-v4",
]
model_collection = (
    f"{owner}/shadowwork-shift-models-and-frozen-adapters-"
    "6af5c8a5a548fb703ab420ac"
)
dataset_collection = (
    f"{owner}/shadowwork-shift-training-data-and-audit-evidence-"
    "6af5c8a51d44c02ee6e19812"
)

required_data = {
    "README.md",
    "DATASET_METHOD.md",
    "sha256_release_manifest.json",
    "sw12/precommit.json",
    "sw12/selection_audit.json",
    "sw12/learner_corrective_v3_training.jsonl",
    "sw12/rehearsal_v3_training.jsonl",
    "sw12/collection/SW12-TRAIN-00-000.json",
    "sw12/sealed_tasks.jsonl",
    "sw17/precommit.json",
    "sw17/selection_audit.json",
    "sw17/learner_corrective_v4_training.jsonl",
    "sw17/rehearsal_v4_training.jsonl",
    "sw17/policy_summary.csv",
    "sw17/paired_tests.csv",
    "sw17/sealed_tasks.jsonl",
}

# Disable authentication intentionally to reproduce judge/public access.
hub = HfApi(token=False)
for model in models:
    info = hub.model_info(model, files_metadata=True, token=False)
    names = {entry.rfilename: entry for entry in info.siblings}
    assert not info.private and not info.gated, model
    assert {"README.md", "adapter_config.json", "adapter_model.safetensors"} <= names.keys(), model
    weights = names["adapter_model.safetensors"]
    assert weights.size is not None and weights.size > 100_000_000, (
        "Expected full trained LoRA weight file missing", model
    )
    print("Public trained adapter verified:", model, f"({weights.size:,} bytes)")

info = hub.dataset_info(dataset, token=False)
published = {entry.rfilename for entry in info.siblings}
assert not info.private and required_data <= published, (
    "Missing dataset files", sorted(required_data - published)
)
print("Public dataset verified:", dataset, f"({len(published):,} files)")

model_items = hub.get_collection(model_collection, token=False).items
data_items = hub.get_collection(dataset_collection, token=False).items
assert set(models) <= {
    item.item_id for item in model_items if item.item_type == "model"
}
assert dataset in {
    item.item_id for item in data_items if item.item_type == "dataset"
}

print("PASS: all required public models, training/evaluation data and collections.")
