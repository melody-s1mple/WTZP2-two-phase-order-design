"""WTZP2 reported-table archive.

This script does not claim to be the original dense eigenvalue solver named in
the manuscript appendix. It records and exports the numerical values reported in
WTZP2_draft_v0.11.tex so that the active project has machine-readable source
files for the tables currently printed in the manuscript.
"""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
CODE.mkdir(exist_ok=True)

experiment_a = [
    {"N": 120, "mu_soft_G_large": 12.4536, "mu_soft_G_small": 15.7973},
    {"N": 200, "mu_soft_G_large": 12.4437, "mu_soft_G_small": 15.7198},
]
experiment_b = [
    {"N": 120, "mu_relaxed": 13.2116, "n1": 13.3779, "n2": 14.0167, "n4": 14.2303, "n8": 14.1701, "n16": 14.3731, "n32": 14.6016},
    {"N": 240, "mu_relaxed": 13.1803, "n1": 13.3315, "n2": 13.9744, "n4": 14.1895, "n8": 14.2929, "n16": 14.1853, "n32": 14.3757},
    {"N": 480, "mu_relaxed": 13.1658, "n1": 13.3094, "n2": 13.9541, "n4": 14.1698, "n8": 14.2734, "n16": 14.3317, "n32": 14.1990},
]
joint_limit = [
    {"n": 1, "N": 67, "gap": 0.1800},
    {"n": 2, "N": 134, "gap": 0.7954},
    {"n": 4, "N": 268, "gap": 1.0008},
    {"n": 8, "N": 536, "gap": 1.0996},
    {"n": 16, "N": 1072, "gap": 1.1553},
    {"n": 32, "N": 2144, "gap": 1.1889},
    {"n": 64, "N": 4288, "gap": 1.2101},
    {"n": 128, "N": 8576, "gap": 1.2236},
    {"n": 256, "N": 17152, "gap": 1.2325},
]
boundary_control = [
    {"n": 1, "difference": 2.492, "middle_soft_gap": 2.672, "start_soft_gap": 0.180},
    {"n": 2, "difference": 0.507, "middle_soft_gap": 1.3024, "start_soft_gap": 0.7954},
    {"n": 4, "difference": 0.205, "middle_soft_gap": 1.2058, "start_soft_gap": 1.0008},
    {"n": 8, "difference": 0.096, "middle_soft_gap": 1.1956, "start_soft_gap": 1.0996},
    {"n": 16, "difference": 0.048, "middle_soft_gap": 1.2033, "start_soft_gap": 1.1553},
    {"n": 32, "difference": 0.025, "middle_soft_gap": 1.2139, "start_soft_gap": 1.1889},
    {"n": 64, "difference": 0.013, "middle_soft_gap": 1.2229, "start_soft_gap": 1.2101},
]

def write_csv(name, rows):
    path = CODE / name
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)

write_csv("WTZP2_experiment_A_reported.csv", experiment_a)
write_csv("WTZP2_experiment_B_reported.csv", experiment_b)
write_csv("WTZP2_joint_limit_reported.csv", joint_limit)
write_csv("WTZP2_boundary_control_reported.csv", boundary_control)
with (CODE / "WTZP2_reported_tables_manifest.json").open("w", encoding="utf-8") as f:
    json.dump({
        "source": "WTZP2_draft_v0.11.tex reported numerical appendix values",
        "status": "reported-table archive, not original solver output",
        "tables": ["experiment_a", "experiment_b", "joint_limit", "boundary_control"],
        "limitations": [
            "Original dense eigenvalue solver scripts named in the manuscript were not present in the active project folder.",
            "CSV files are machine-readable records of manuscript-reported values, not independently recomputed eigenvalues.",
            "Boundary-control middle_soft_gap entries for n=2,4,8,16,32 are derived from the archived centered-start difference plus the archived start-soft joint-limit gap."
        ],
    }, f, indent=2)
print("wrote WTZP2 reported table CSV archive")
