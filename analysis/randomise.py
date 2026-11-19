#!/usr/bin/env python3
"""Generate a reproducible, blocked random allocation for a protocol.

    python analysis/randomise.py P01 --blocks T01,T02,T03 --per-arm 3 --seed 4821

* Blocks are the unit that varies most outside the treatment (source tree for
  logs, bed row for soil beds). Every block gets every arm equally.
* Each unit gets a neutral 4-character blind code. The allocation file maps
  code -> arm and should be held by someone who does not score outcomes.
  Scorers see only the codes (log tags, photo file names).
* Pick the seed by a public, unpredictable act (e.g. the last 4 digits of that
  day's Nikkei 225 close) and write it in the protocol BEFORE running this.

Writes trials/<protocol>/allocation.csv and blind_labels.csv.
"""
from __future__ import annotations

import argparse
import csv
import random
import string
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARMS = {
    "P01": ["kit-block", "dowel"],
    "P02": ["carrot+kit", "kit-only", "carrot-only"],
    "P03": ["akamegashiwa", "sugi", "yabunikkei", "konara"],
    "P04": ["celtis", "zelkova", "cerasus"],
    "P05": ["ume", "konara", "cerasus"],
    "P06": ["wild-moth", "silkworm", "beetle-larvae", "brown-rice"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("protocol", choices=sorted(ARMS))
    ap.add_argument("--blocks", required=True, help="comma-separated block ids, e.g. tree tags")
    ap.add_argument("--per-arm", type=int, required=True, help="units per arm in each block")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rng = random.Random(a.seed)
    arms = ARMS[a.protocol]
    alphabet = [c for c in string.ascii_uppercase + string.digits if c not in "O0I1"]
    used: set[str] = set()
    rows = []
    for block in [b.strip() for b in a.blocks.split(",") if b.strip()]:
        units = [arm for arm in arms for _ in range(a.per_arm)]
        rng.shuffle(units)
        for pos, arm in enumerate(units, start=1):
            code = ""
            while not code or code in used:
                code = "".join(rng.choice(alphabet) for _ in range(4))
            used.add(code)
            rows.append({"protocol": a.protocol, "block": block, "position_in_block": pos,
                         "blind_code": code, "arm": arm})
    out = Path(a.out) if a.out else ROOT / "trials" / a.protocol
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "allocation.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(out / "blind_labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["block", "position_in_block", "blind_code"])
        for r in rows:
            w.writerow([r["block"], r["position_in_block"], r["blind_code"]])
    print(f"{len(rows)} units allocated -> {out}/allocation.csv (keep sealed) and blind_labels.csv")


if __name__ == "__main__":
    main()
