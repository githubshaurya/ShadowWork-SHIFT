"""Audit public SW17 training provenance and scored evidence, no GPU or API key.

Requires: pip install huggingface_hub. Run directly from Python or a notebook.
This recalculates published metrics from episode JSONs; full SQLite replay is in SW17 notebook.
"""

from hashlib import sha256
from math import comb
from pathlib import Path
import csv
import json

from huggingface_hub import HfApi, hf_hub_download, snapshot_download

DATASET_ID = "i-am-shaurya05/shadowwork-shift-datasets"
MODEL_IDS = {
    "learner_corrective_v4": "i-am-shaurya05/shadowwork-shift-corrective-v4",
    "rehearsal_v4": "i-am-shaurya05/shadowwork-shift-rehearsal-v4",
}
EXPECTED_SUCCESS = {
    "frozen_sw09": 31,
    "corrective_v4": 65,
    "rehearsal_v4": 65,
    "previous_rehearsal_v3": 57,
}

# Fetch the exact public files without a login token.
root = Path(snapshot_download(
    repo_id=DATASET_ID,
    repo_type="dataset",
    allow_patterns=["sw17/**", "sha256_release_manifest.json"],
    token=False,
))
release_manifest = json.loads((root / "sha256_release_manifest.json").read_text())
public_files = sorted(p for p in (root / "sw17").rglob("*") if p.is_file())
assert len(public_files) == 496, len(public_files)
for file in public_files:
    key = file.relative_to(root).as_posix()
    assert sha256(file.read_bytes()).hexdigest() == release_manifest[key], key
print("PASS: all 496 SW17 release-file hashes")

# Task-level split isolation, prespecified hashes and authentic training rows.
precommit = json.loads((root / "sw17/precommit.json").read_text())
tasks = {}
for split, expected in [("train", 240), ("dev", 40), ("sealed", 80)]:
    file = root / f"sw17/{split}_tasks.jsonl"
    assert sha256(file.read_bytes()).hexdigest() == precommit["split_sha256"][split]
    rows = [json.loads(line) for line in file.read_text().splitlines()]
    assert len(rows) == expected
    assert len({row["id"] for row in rows}) == expected
    tasks[split] = rows
all_ids = [row["id"] for split in tasks.values() for row in split]
assert len(set(all_ids)) == 360, "Train/dev/sealed task IDs must be disjoint"

selection = json.loads((root / "sw17/selection_audit.json").read_text())
assert selection["rollouts"] == 160
assert selection["learner_states"] == 1311
assert selection["actual_correction_candidates"] == 859
assert selection["selected_learner_states"] == 400
assert selection["selected_actual_corrections"] == 211
assert selection["matched_control_exact_action_strata"] == 395
assert len(list((root / "sw17/collection").glob("*.json"))) == 160

training_rows = {}
for arm in MODEL_IDS:
    path = root / f"sw17/{arm}_training.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(rows) == len({row["prompt"] for row in rows}) == 800
    assert sha256(path.read_bytes()).hexdigest() == selection[
        "corrective_sha256" if arm == "learner_corrective_v4" else "rehearsal_sha256"
    ]
    metadata = json.loads((root / f"sw17/{arm}_training_metadata.json").read_text())
    assert metadata["steps"] == 80
    assert metadata["train_rows"] == 800
    assert metadata["training_sha256"] == sha256(path.read_bytes()).hexdigest()
    assert metadata["loss_history"][-1]["step"] == 80
    training_rows[arm] = rows

corrective_pairs = {
    (row["prompt"], row["completion"])
    for row in training_rows["learner_corrective_v4"]
}
rehearsal_pairs = {
    (row["prompt"], row["completion"])
    for row in training_rows["rehearsal_v4"]
}
assert len(corrective_pairs & rehearsal_pairs) == 400
print("PASS: disjoint task splits, 80-step training histories, 400 shared anchors")

# Recompute all strict-success counts from 320 independently stored episode JSONs.
scorecard = list(csv.DictReader((root / "sw17/episode_scorecard.csv").open()))
assert len(scorecard) == 320
outcomes = {}
for policy, target in EXPECTED_SUCCESS.items():
    folder = root / "sw17/evaluation/sealed" / policy
    files = sorted(folder.glob("*.json"))
    assert len(files) == 80
    policy_outcomes = {}
    for file in files:
        episode = json.loads(file.read_text())
        task_id = episode["task_id"]
        assert task_id == file.stem
        assert episode["policy"] == policy
        assert episode["score"]["steps"] == len(episode["history"])
        assert (episode["auditkit_verdict"] == "success") == episode["score"]["strict_success"]
        assert task_id not in policy_outcomes
        policy_outcomes[task_id] = bool(episode["score"]["strict_success"])
    assert set(policy_outcomes) == {task["id"] for task in tasks["sealed"]}
    assert sum(policy_outcomes.values()) == target
    for row in (r for r in scorecard if r["policy"] == policy):
        assert policy_outcomes[row["task_id"]] == (row["strict_success"].lower() == "true")
    outcomes[policy] = policy_outcomes
    print(f"PASS: {policy}: {target}/80 strict success")

# Exact two-sided paired McNemar from matching sealed task IDs, not unpaired tests.
recorded_tests = {
    (r["candidate"], r["reference"]): r
    for r in csv.DictReader((root / "sw17/paired_tests.csv").open())
}
for candidate, reference in [
    ("corrective_v4", "frozen_sw09"),
    ("rehearsal_v4", "frozen_sw09"),
    ("corrective_v4", "rehearsal_v4"),
]:
    a, b = outcomes[candidate], outcomes[reference]
    wins = sum(a[k] and not b[k] for k in a)
    losses = sum(not a[k] and b[k] for k in a)
    discordant = wins + losses
    p_value = min(1.0, 2 * sum(comb(discordant, i)
        for i in range(min(wins, losses) + 1)) / (2 ** discordant))
    recorded = recorded_tests[candidate, reference]
    assert (wins, losses) == (int(recorded["wins"]), int(recorded["losses"]))
    assert abs(p_value - float(recorded["exact_mcnemar_p"])) < 1e-12
    print(f"PASS: {candidate} vs {reference}: {wins} wins, {losses} losses, p={p_value:.10g}")

# These are published fingerprint claims; checking the entire tensor-byte hashes
# would additionally require downloading each full 121MB adapter safetensors file.
provenance = json.loads((root / "sw17/final_provenance.json").read_text())
for arm, model_id in MODEL_IDS.items():
    path = hf_hub_download(model_id, "provenance/original_weights_sha256.txt", token=False)
    recorded_hash = Path(path).read_text().strip()
    assert recorded_hash == provenance["model_weights_sha256"][arm]
    info = HfApi(token=False).model_info(model_id, files_metadata=True, token=False)
    weight_files = [f for f in info.siblings if f.rfilename == "adapter_model.safetensors"]
    assert len(weight_files) == 1 and weight_files[0].size == 120981200
print("PASS: public v4 model metadata and original weight fingerprints")
print("SW17 PUBLIC EVIDENCE AUDIT PASS")
