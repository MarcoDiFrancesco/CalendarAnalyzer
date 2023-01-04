"""Randomize labels in sample_ics files."""

import random
from pathlib import Path

from utils.data_checks.check_name import ACTIVITY_DICT


def _replace_summary(line: str, act_list: list) -> str:
    if line.startswith("SUMMARY"):
        sample_summary = random.choice(act_list)
        line = f"SUMMARY:{sample_summary}\n"
    return line


def _replace_date(line: str, act_list: list) -> str:
    """Add random time to dates.

    e.g. From 18:30 -> 19:30 is
    'DTSTART:20221103T183000Z' -> 'DTSTART:20221103T193000Z'
    Note: 1970 dates do not have Z at the end
    'DTSTART:19700329T183000'  -> 'DTSTART:19700329T193000'
    Note: some lines contain Time Zone, in that case ignore them
    'DTSTART;TZID=Europe/Rome:20191019T083000'
    """
    if line.startswith(
        ("DTSTART:", "DTEND:", "DTSTAMP:", "CREATED:", "LAST-MODIFIED:")
    ):
        # e.g. ['DTSTART', '20221216T080000Z']
        label, datetime = line.split(":")
        datetime = datetime.strip("\n")
        # e.g. 0800
        hourmin = datetime[9:13]
        hourmin = _add_random_time(hourmin, label)
        new_datetime = f"{datetime[:9]}{hourmin}{datetime[13:]}"
        assert len(datetime) == len(new_datetime), "Datetime length mismatch"
        line = f"{label}:{new_datetime}\n"
    return line


def _add_random_time(hourmin_str: str, label: str) -> str:
    """Add random time to hour-minute format.

    e.g. '0700' -> '0800'
    e.g. '1700' -> '1900'
    Note: time >= 20:00 does not increase
    e.g. '2200' -> '2200'
    """
    if label in ["DTSTART"]:
        time_list = [0, 1]
    elif label in ["DTEND", "DTSTAMP", "CREATED", "LAST-MODIFIED"]:
        time_list = [2, 3]
    else:
        raise KeyError()
    # '0806' -> 806
    hourmin = int(hourmin_str)
    # If would not exceed midnight
    if hourmin <= 2000:
        # e.g. from 19:30 + 3h = 22:30 is '1930' -> '2230'
        hourmin += random.choice(time_list) * 100
    assert hourmin <= 2359, f"Time should not exceed 23:59, got {hourmin}"
    # 830 -> '0890'
    hourmin_str = str(hourmin).zfill(4)
    return hourmin_str


def randomize_file(fname):
    lines = []
    with open(fname) as f:
        # From 'sample_ics/Commute.ics' to 'Commute'
        fstem = fname.stem
        for line in f:
            line = _replace_summary(line, ACTIVITY_DICT[fstem])
            line = _replace_date(line, ACTIVITY_DICT[fstem])
            lines.append(line)

    # Replace original file
    with open(f"{fname}.sample", "w") as f:
        for line in lines:
            f.write(f"{line}")


sample_dir = Path("sample_ics")
assert sample_dir.exists(), "Run script from repository root"
# e.g. [PosixPath('sample_ics/Commute.ics'), PosixPath('sample_ics/Chores.ics'), ...]
ics_list = list(sample_dir.rglob("*.ics"))
assert ics_list, "No ICS found"

# Test file
randomize_file(Path("sample_ics/Commute.ics"))
print("Replacing")

# for fname in ics_list:
#     print(f"Replacing values in {fname}")
#     randomize_file(fname)
