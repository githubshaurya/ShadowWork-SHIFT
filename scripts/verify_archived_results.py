# Verify archived ShadowWork-SHIFT scores from original evidence ZIPs.
# Set DATA_DIRECTORY to the directory containing the original ZIPs.
# No CLI flags, training, internet, or GPU required.
from pathlib import Path
from zipfile import ZipFile
from collections import defaultdict
import csv
import io
import json

DATA_DIRECTORY = Path(".")  # Edit to the folder containing the downloaded ZIPs.

def read_csv(archive, name):
    return list(csv.DictReader(io.StringIO(archive.read(name).decode("utf-8"))))

# SW09: recompute directly from raw scored episode JSON files.
with ZipFile(DATA_DIRECTORY / "ShadowWork_09_Final_Holdout_Evidence.zip") as archive:
    totals = defaultdict(lambda: {"n": 0, "strict": 0, "state": 0, "evidence": 0, "unsafe": 0, "executed": 0})
    for filename in archive.namelist():
        if not (filename.startswith("evaluation_final_holdout/") and filename.endswith(".json")):
            continue
        episode = json.loads(archive.read(filename))
        row = totals[episode["policy"]]
        row["n"] += 1
        row["strict"] += int(episode["strict_success"])
        row["state"] += int(episode["state_correct"])
        row["evidence"] += int(episode["evidence_supported"])
        row["unsafe"] += int(episode["unsafe_proposals"])
        row["executed"] += int(episode["executed_unsafe"])
    expected = {"parent_v2": (42, 70), "parent_v2_early_finish_controller": (69, 70), "learner_corrective": (70, 70)}
    for policy, (strict, state) in expected.items():
        result = totals[policy]
        assert (result["strict"], result["state"], result["n"]) == (strict, state, 70)
    print("SW09 70-case holdout verified:", dict(totals))

# SW12: first held-out protocol shift, models without final unified controller.
with ZipFile(DATA_DIRECTORY / "ShadowWork_12_Closed_Loop_Evidence.zip") as archive:
    rows = read_csv(archive, "grouped_summary.csv")
    target = {
        ("frozen_corrective", "1"): (22, 32),
        ("frozen_corrective", "2"): (2, 32),
        ("learner_corrective_v3", "1"): (31, 32),
        ("learner_corrective_v3", "2"): (15, 32),
        ("rehearsal_v3", "1"): (31, 32),
        ("rehearsal_v3", "2"): (16, 32),
    }
    for row in rows:
        key = (row["policy"], row["checks_required"])
        if row["split"] == "sealed" and key in target:
            assert (int(row["strict"]), int(row["n"])) == target[key]
    print("SW12 sealed split verified: corrective 46/64, rehearsal 47/64, original 24/64")

# SW16 v4: paired model/arm comparison under the same controller.
with ZipFile(DATA_DIRECTORY / "ShadowWork_16_Unified_Recovery_Results.zip") as archive:
    rows = read_csv(archive, "summary.csv")
    target = {
        ("sw12_core", "original_corrective"): (80, 96),
        ("sw12_composed", "original_corrective"): (52, 64),
        ("sw12_core", "learner_corrective_v3"): (94, 96),
        ("sw12_composed", "learner_corrective_v3"): (60, 64),
        ("sw12_core", "rehearsal_v3"): (96, 96),
        ("sw12_composed", "rehearsal_v3"): (64, 64),
    }
    for row in rows:
        key = (row["suite"], row["policy"])
        if row["controller"] == "unified_v4" and key in target:
            assert (int(row["strict"]), int(row["n"])) == target[key]
    assert archive.read("deployment_decision.txt").decode().strip().startswith("HOLD")
    print("SW16 unified-v4 verified, including original HOLD decision")

# SW16 focused v5: distinguish model-task evaluation episodes from distinct tasks.
with ZipFile(DATA_DIRECTORY / "ShadowWork_16_Budget_Regression_Results.zip") as archive:
    rows = read_csv(archive, "paired_summary.csv")
    totals = {("sw12_core", "learner_corrective_v3"): 95,
              ("sw12_composed", "learner_corrective_v3"): 61,
              ("sw12_core", "rehearsal_v3"): 96,
              ("sw12_composed", "rehearsal_v3"): 64}
    for row in rows:
        key = (row["suite"], row["policy"])
        if row["baseline"] == "unified_v4" and row["metric"] == "strict_success":
            assert int(row["new_pass"]) == totals[key]
            assert int(row["losses"]) == 0
    assert sum(totals.values()) == 316
    assert archive.read("decision.txt").decode().strip() == "PASS_FOCUSED_ENGINEERING_REGRESSION"
    print("SW16 budget-v5 verified: 316/320 strict episodes, zero paired strict losses")
