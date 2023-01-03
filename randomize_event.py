"""Randomize labels in sample_ics files."""

import random
from pathlib import Path

from utils.data_checks.check_name import ACTIVITY_DICT


def _replace_summary(line: str, act_list: list) -> str:
    if line.startswith("SUMMARY:"):
        sample_summary = random.choice(act_list)
        line = f"SUMMARY:{sample_summary}\n"
    return line


def randomize_file(fname):
    lines = []
    with open(fname) as f:
        # From 'sample_ics/Commute.ics' to 'Commute'
        fstem = fname.stem
        for line in f:
            line = _replace_summary(line, ACTIVITY_DICT[fstem])
            lines.append(line)

    # Replace original file
    with open(f"{fname}", "w") as f:
        for line in lines:
            f.write(f"{line}")


sample_dir = Path("sample_ics")
assert sample_dir.exists(), "Run script from repository root"
# e.g. [PosixPath('sample_ics/Commute.ics'), PosixPath('sample_ics/Chores.ics'), ...]
ics_list = list(sample_dir.rglob("*.ics"))
assert ics_list, "No ICS found"

for fname in ics_list:
    randomize_file(fname)
    print(f"Replacing 'SUMMARY' in {fname}")
