#!/usr/bin/env python3
"""Validate the dataset and regenerate every derived result.

    python analysis/build.py            # validate + rebuild results/
    python analysis/build.py --check    # validate only, exit 1 on any error

Outputs (all deterministic, safe to diff in CI):
    results/matrix_long.csv        one row per species x substrate cell with evidence
    results/matrix.md              the same, as readable tables per species
    results/plan_audit.csv / .md   each wood in the project plan vs the evidence
    results/gaps.md                project woods with no production evidence
    results/figures/*.png|svg      matrix heatmaps and evidence profile

Aggregation rule (see docs/evidence-grading.md):
    For each cell, only production claims count; if any of them are log-type
    (log, short log, stump, buried root) only those count, because the project
    is log culture and sawdust-bed results do not always transfer. The cell takes the claims at the
    BEST (lowest-numbered) evidence level present; their outcome is the median
    of those claims, rounded down (conservative). If those claims span two or
    more outcome steps the cell is flagged as a conflict. Lower-grade claims are
    kept in the record but never override a better-grade one.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RES = ROOT / "results"
FIG = RES / "figures"

SCORE = {"none": 0, "poor": 1, "marginal": 2, "fruited-unquantified": 2.5, "good": 3, "excellent": 4}
LEVEL_NAME = {1: "E1 replicated trial", 2: "E2 single trial / report", 3: "E3 guide rating",
              4: "E4 project pilot", 5: "E5 extrapolation"}
# Which study types may carry which evidence level.
ALLOWED_LEVEL = {
    "replicated-trial": {1},
    "single-trial": {2},
    "host-record": {2},
    "guide-rating": {3},
    "pilot": {4},
    "extrapolation": {5},
}
LOG_FORMS = {"log", "short-log", "stump", "buried-root"}
PROJECT_WOODS = ["konara", "kunugi", "carpinus", "ostrya", "cerasus", "prunus-mume",
                 "acer", "celtis", "cinnamomum", "sugi"]


# --------------------------------------------------------------------------- io
def read(name: str) -> list[dict]:
    with open(DATA / f"{name}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


# --------------------------------------------------------------------- validate
def validate() -> list[str]:
    """Check every table against datapackage.json plus the grading rules."""
    pkg = json.loads((ROOT / "datapackage.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    tables: dict[str, list[dict]] = {}
    for res in pkg["resources"]:
        rows = read(res["name"])
        tables[res["name"]] = rows
        schema = res["schema"]
        names = [f["name"] for f in schema["fields"]]
        if rows and list(rows[0].keys()) != names:
            errors.append(f"{res['name']}: columns {list(rows[0].keys())} != schema {names}")
            continue
        pk = schema.get("primaryKey")
        seen = set()
        for i, r in enumerate(rows, start=2):
            where = f"{res['path']}:{i}"
            if pk:
                if r[pk] in seen:
                    errors.append(f"{where}: duplicate {pk} {r[pk]!r}")
                seen.add(r[pk])
            for fd in schema["fields"]:
                v = r[fd["name"]]
                c = fd.get("constraints", {})
                if c.get("required") and not v.strip():
                    errors.append(f"{where}: {fd['name']} is required")
                    continue
                if not v:
                    continue
                if fd["type"] == "integer":
                    if not re.fullmatch(r"-?\d+", v):
                        errors.append(f"{where}: {fd['name']}={v!r} is not an integer")
                        continue
                    v = int(v)
                if "enum" in c and v not in c["enum"]:
                    errors.append(f"{where}: {fd['name']}={v!r} not in {c['enum']}")
                if "pattern" in fd and not re.fullmatch(fd["pattern"], str(v)):
                    errors.append(f"{where}: {fd['name']}={v!r} does not match {fd['pattern']}")
        for fk in schema.get("foreignKeys", []):
            ref = fk["reference"]
            keys = {x[ref["fields"]] for x in read(ref["resource"])}
            for i, r in enumerate(rows, start=2):
                if r[fk["fields"]] not in keys:
                    errors.append(f"{res['path']}:{i}: {fk['fields']}={r[fk['fields']]!r} not found in {ref['resource']}")

    # Grading rules that a schema alone cannot express.
    sources = {s["source_id"]: s for s in tables["sources"]}
    for i, r in enumerate(tables["evidence"], start=2):
        where = f"data/evidence.csv:{i} ({r['claim_id']})"
        lvl = int(r["evidence_level"]) if r["evidence_level"].isdigit() else None
        st = r["study_type"]
        if st in ALLOWED_LEVEL and lvl not in ALLOWED_LEVEL[st]:
            errors.append(f"{where}: study_type {st} cannot be E{lvl}")
        if lvl == 1 and sources.get(r["source_id"], {}).get("verified", "no") in ("no", "partial"):
            errors.append(f"{where}: E1 requires the replicated design to be verified in sources.csv")
        if lvl == 5 and not r["notes"].strip():
            errors.append(f"{where}: an extrapolation must state its reasoning in notes")
        if r["metric_class"] == "host-record" and r["outcome"] != "host":
            errors.append(f"{where}: host-record claims use outcome 'host'")
        if r["outcome"] == "host" and r["metric_class"] != "host-record":
            errors.append(f"{where}: outcome 'host' only for host-record claims")
        if r["metric_class"] == "colonisation" and r["outcome"] != "colonised":
            errors.append(f"{where}: colonisation claims use outcome 'colonised'")
        if r["metric_class"] == "production" and r["outcome"] not in SCORE:
            errors.append(f"{where}: production outcome must be one of {list(SCORE)}")
        if r["outcome"] == "fruited-unquantified" and lvl != 4:
            errors.append(f"{where}: 'fruited-unquantified' is reserved for project pilots")
        src = sources.get(r["source_id"])
        if src and not (src["url"] or src["doi"]) and src["source_kind"] != "extrapolation":
            errors.append(f"{where}: source {r['source_id']} has neither DOI nor URL")
    return errors


# -------------------------------------------------------------------- aggregate
def label_for(score: float, pilot: bool = False) -> str:
    """Median score -> outcome label, rounding DOWN (conservative).

    'fruited-unquantified' (2.5) is only a valid label for project pilots; a
    median of 2.5 from measured claims rounds down to 'marginal'.
    """
    best = "none"
    for name, s in sorted(SCORE.items(), key=lambda kv: kv[1]):
        if name == "fruited-unquantified" and not pilot:
            continue
        if s <= score + 1e-9:
            best = name
    return best


def aggregate(evidence: list[dict]) -> dict[tuple[str, str], dict]:
    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in evidence:
        cells[(r["species_id"], r["substrate_id"])].append(r)
    out = {}
    for key, claims in cells.items():
        prod = [c for c in claims if c["metric_class"] == "production"]
        # The project is log culture: when log-type claims exist, they decide the cell.
        logs = [c for c in prod if c["substrate_form"] in LOG_FORMS]
        if logs:
            prod = logs
        other = sorted({c["metric_class"] for c in claims if c["metric_class"] != "production"})
        row = {
            "species_id": key[0], "substrate_id": key[1],
            "best_level": "", "outcome": "", "conflict": "",
            "n_production_claims": len(prod), "n_claims": len(claims),
            "best_level_claims": "", "lower_level_claims": "",
            "other_evidence": ";".join(other), "sources": "",
        }
        if prod:
            best = min(int(c["evidence_level"]) for c in prod)
            top = [c for c in prod if int(c["evidence_level"]) == best]
            scores = sorted(SCORE[c["outcome"]] for c in top)
            n = len(scores)
            med = scores[n // 2] if n % 2 else (scores[n // 2 - 1] + scores[n // 2]) / 2
            row.update(
                best_level=best,
                outcome=label_for(med, pilot=(best == 4)),
                conflict="yes" if (max(scores) - min(scores)) >= 2 else "",
                best_level_claims=";".join(c["claim_id"] for c in top),
                lower_level_claims=";".join(c["claim_id"] for c in prod if int(c["evidence_level"]) != best),
            )
        row["sources"] = ";".join(sorted({c["source_id"] for c in claims}))
        out[key] = row
    return out


# ------------------------------------------------------------------- plan audit
def verdict(cell: dict | None) -> str:
    if not cell or cell["best_level"] == "":
        if cell and "colonisation" in cell["other_evidence"]:
            return "colonisation only"
        if cell and cell["other_evidence"]:
            return "no production data"
        return "no evidence"
    lvl, out = int(cell["best_level"]), cell["outcome"]
    if lvl == 5:
        return "hypothesis only"
    if lvl == 4:
        return "project pilot only"
    if cell["conflict"]:
        return "conflicting evidence"
    if out in ("excellent", "good"):
        return "supported"
    if out == "marginal":
        return "weak"
    return "contradicted"


VERDICT_ORDER = ["contradicted", "conflicting evidence", "weak", "no production data", "no evidence",
                 "hypothesis only", "colonisation only", "project pilot only", "supported"]


def plan_audit(plan, cells, species, substrates):
    rows = []
    for p in plan:
        cell = cells.get((p["species_id"], p["substrate_id"]))
        v = verdict(cell)
        # Better-evidenced woods the project can actually get.
        alts = []
        for (sp, sub), c in cells.items():
            if sp != p["species_id"] or sub == p["substrate_id"] or c["best_level"] == "":
                continue
            if int(c["best_level"]) <= 3 and c["outcome"] == "excellent" and not c["conflict"] \
                    and substrates[sub]["project_access"] in ("have", "maybe", "plan"):
                alts.append(f"{substrates[sub]['name_en']} (E{c['best_level']})")
        rows.append({
            "species": species[p["species_id"]]["name_en"],
            "substrate": substrates[p["substrate_id"]]["name_en"],
            "role": p["role"], "plan_grade": p["plan_grade"], "logs_planned": p["logs_planned"],
            "verdict": v,
            "best_level": f"E{cell['best_level']}" if cell and cell["best_level"] != "" else "",
            "outcome": cell["outcome"] if cell else "",
            "claims": cell["best_level_claims"] if cell else "",
            "better_evidenced_project_woods": "; ".join(sorted(alts)),
            "species_id": p["species_id"], "substrate_id": p["substrate_id"],
        })
    rows.sort(key=lambda r: (VERDICT_ORDER.index(r["verdict"]), r["role"] != "now", r["species"]))
    return rows


# --------------------------------------------------------------------- figures
COLORS = {  # diverging: failure (red) <- neutral -> success (blue); validated pair from the dataviz palette
    "none": "#a8322f", "poor": "#e88b88", "marginal": "#e4e2dc", "fruited-unquantified": "#cde2fb",
    "good": "#86b6ef", "excellent": "#256abf",
}
INK = "#0b0b0b"
MUTED = "#6b6a66"
SURFACE = "#fcfcfb"


def draw_matrix(cells, species, substrates, columns, path_stem, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch, Rectangle

    matplotlib.rcParams.update({"svg.hashsalt": "tanzawa", "font.family": "DejaVu Sans"})
    sp_ids = list(species)
    w = max(8.0, 1.9 + 0.48 * len(columns))
    h = 1.6 + 0.36 * len(sp_ids) + 1.3
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for yi, sp in enumerate(sp_ids):
        for xi, sub in enumerate(columns):
            c = cells.get((sp, sub))
            x, y = xi, len(sp_ids) - 1 - yi
            if not c:
                ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, fc="none", ec="#ecebe7", lw=.6))
                continue
            if c["best_level"] == "":
                ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, fc="none", ec="#d6d4cd", lw=.6))
                mark = {"host-record": "H", "colonisation": "C", "quality": "Q"}
                t = "".join(mark[k] for k in c["other_evidence"].split(";") if k in mark)
                ax.text(x + .5, y + .5, t, ha="center", va="center", fontsize=6.5, color=MUTED)
                continue
            lvl = int(c["best_level"])
            if lvl == 5:
                ax.add_patch(Rectangle((x + .06, y + .06), .88, .88, fc="none", ec=MUTED, lw=.8, ls=(0, (2, 2))))
                ax.text(x + .5, y + .5, "?", ha="center", va="center", fontsize=8, color=MUTED)
                continue
            fc = COLORS[c["outcome"]]
            ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, fc=fc, ec=SURFACE, lw=1,
                                   hatch="////" if lvl == 4 else None))
            dark = c["outcome"] in ("excellent", "none")
            ax.text(x + .5, y + .5, f"E{lvl}", ha="center", va="center", fontsize=6.5,
                    color="#ffffff" if dark else INK, fontweight="bold")
            if c["conflict"]:
                ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, fc="none", ec=INK, lw=1.4))
    ax.set_xlim(0, len(columns))
    ax.set_ylim(0, len(sp_ids))
    ax.set_xticks([i + .5 for i in range(len(columns))])
    ax.set_xticklabels([substrates[s]["name_en"] for s in columns], rotation=55, ha="right", fontsize=7.5, color=INK)
    ax.set_yticks([len(sp_ids) - 1 - i + .5 for i in range(len(sp_ids))])
    ax.set_yticklabels([species[s]["name_en"] for s in sp_ids], fontsize=7.5, color=INK)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title + "\n", loc="left", fontsize=10, color=INK, pad=6)
    ax.text(0, 1.012, "Cell text = best evidence level (E1 strongest). H host record, C colonisation only, "
            "Q quality only. Production claims only decide the colour.", transform=ax.transAxes,
            fontsize=6.5, color=MUTED, va="bottom")
    handles = [Patch(fc=COLORS[k], ec="none", label=k.replace("-", " ")) for k in
               ("excellent", "good", "marginal", "poor", "none")]
    handles += [Patch(fc=COLORS["fruited-unquantified"], ec="none", hatch="////", label="project pilot (fruited)"),
                Patch(fc="none", ec=MUTED, ls="--", label="? extrapolation only"),
                Patch(fc="none", ec=INK, lw=1.4, label="conflicting claims")]
    fig.legend(handles=handles, loc="lower left", ncol=4, fontsize=7, frameon=False, bbox_to_anchor=(0.01, 0.0))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{path_stem}.{ext}", facecolor=SURFACE,
                    metadata={"Software": None} if ext == "png" else {"Date": None, "Creator": None})
    plt.close(fig)


def draw_profile(evidence, species):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    levels = [1, 2, 3, 4, 5]
    ramp = {1: "#104281", 2: "#2a78d6", 3: "#6da7ec", 4: "#b7d3f6", 5: "#e4e2dc"}
    counts = {sp: [0] * 5 for sp in species}
    for r in evidence:
        if r["metric_class"] == "production":
            counts[r["species_id"]][int(r["evidence_level"]) - 1] += 1
    order = sorted(species, key=lambda s: (-sum(counts[s][:3]), species[s]["name_en"]))
    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for i, sp in enumerate(order):
        left = 0
        for lv in levels:
            v = counts[sp][lv - 1]
            if v:
                ax.barh(len(order) - 1 - i, v, left=left, color=ramp[lv], height=.62, edgecolor=SURFACE, linewidth=1.5)
            left += v
        ax.text(left + .2, len(order) - 1 - i, str(left), va="center", fontsize=7, color=MUTED)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([species[s]["name_en"] for s in reversed(order)], fontsize=7.5)
    ax.set_xlabel("production claims (species × substrate)", fontsize=8, color=INK)
    ax.tick_params(length=0, labelsize=7.5)
    ax.grid(axis="x", color="#ecebe7", lw=.6)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("How much of each species' wood choice rests on real trials", loc="left", fontsize=10)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=ramp[lv], label=LEVEL_NAME[lv]) for lv in levels], fontsize=7,
              frameon=False, loc="lower right")
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"evidence_profile.{ext}", facecolor=SURFACE,
                    metadata={"Software": None} if ext == "png" else {"Date": None, "Creator": None})
    plt.close(fig)


# ------------------------------------------------------------------- markdown
def md_table(rows, cols, heads):
    out = ["| " + " | ".join(heads) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r[c]).replace("|", "/") for c in cols) + " |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only")
    args = ap.parse_args()

    errors = validate()
    if errors:
        print(f"{len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1
    evidence = read("evidence")
    print(f"OK: {len(evidence)} claims validated")
    if args.check:
        return 0

    species = {r["species_id"]: r for r in read("species")}
    substrates = {r["substrate_id"]: r for r in read("substrates")}
    sources = {r["source_id"]: r for r in read("sources")}
    plan = read("plan_assignments")
    cells = aggregate(evidence)
    FIG.mkdir(parents=True, exist_ok=True)

    # long matrix
    sp_order = list(species)
    sub_order = list(substrates)
    long_rows = sorted(cells.values(), key=lambda r: (sp_order.index(r["species_id"]), sub_order.index(r["substrate_id"])))
    write_csv(RES / "matrix_long.csv", long_rows, list(long_rows[0].keys()))

    # matrix.md, per species
    claims_by_id = {c["claim_id"]: c for c in evidence}
    lines = ["# Species × substrate matrix", "",
             "Generated by `analysis/build.py`; do not edit by hand. Production evidence only decides the grade; "
             "`other` lists host records, colonisation or quality data that do not.", ""]
    for sp in sp_order:
        rows = [r for r in long_rows if r["species_id"] == sp]
        if not rows:
            continue
        lines += [f"## {species[sp]['name_en']} ({species[sp]['name_ja']}, *{species[sp]['scientific_name']}*)", ""]
        tab = []
        for r in sorted(rows, key=lambda r: (r["best_level"] == "", r["best_level"] or 9, -SCORE.get(r["outcome"], -1))):
            ev = []
            for cid in r["best_level_claims"].split(";") if r["best_level_claims"] else []:
                c = claims_by_id[cid]
                form = "" if c["substrate_form"] == "log" else f" [{c['substrate_form']}]"
                ev.append(f"{cid}: {c['value'] or c['outcome']}{form} ({c['source_id']})")
            tab.append({
                "sub": substrates[r["substrate_id"]]["name_en"],
                "lvl": f"E{r['best_level']}" if r["best_level"] != "" else "",
                "out": (r["outcome"] or "") + (" ⚠ conflict" if r["conflict"] else ""),
                "ev": "; ".join(ev), "oth": r["other_evidence"],
            })
        lines += [md_table(tab, ["sub", "lvl", "out", "ev", "oth"], ["Substrate", "Best level", "Outcome", "Claims at best level", "Other"]), ""]
    (RES / "matrix.md").write_text("\n".join(lines), encoding="utf-8")

    # plan audit
    audit = plan_audit(plan, cells, species, substrates)
    write_csv(RES / "plan_audit.csv", audit, list(audit[0].keys()))
    counts = defaultdict(int)
    for a in audit:
        counts[a["verdict"]] += 1
    lines = ["# Audit of the Log Yard Plan wood assignments", "",
             "Each species–substrate pair in the project plan, checked against the evidence. "
             "Plan grades are the plan's own; they are not evidence. Generated by `analysis/build.py`.", "",
             "| Verdict | Pairs |", "|---|---|"]
    lines += [f"| {v} | {counts[v]} |" for v in VERDICT_ORDER if counts[v]]
    lines += ["", md_table(audit, ["species", "substrate", "role", "plan_grade", "verdict", "best_level", "outcome",
                                   "better_evidenced_project_woods"],
                           ["Species", "Planned substrate", "Role", "Plan grade", "Verdict", "Best level", "Outcome",
                            "Better-evidenced woods the project can get"]), ""]
    (RES / "plan_audit.md").write_text("\n".join(lines), encoding="utf-8")

    # gaps: project woods x cultivated wood species with no production evidence
    wood_species = [s for s in sp_order if "wood" in species[s]["guild"] or "root/butt" in species[s]["guild"]]
    lines = ["# Evidence gaps for the woods the project can get", "",
             "Cells with no production evidence at E1–E4. `?` = only an extrapolation exists; blank = nothing at all. "
             "Generated by `analysis/build.py`.", "",
             "| Species | " + " | ".join(substrates[w]["name_en"] for w in PROJECT_WOODS) + " |",
             "|---|" + "---|" * len(PROJECT_WOODS)]
    n_gap = 0
    for sp in wood_species:
        row = []
        for w in PROJECT_WOODS:
            c = cells.get((sp, w))
            if c and c["best_level"] != "" and int(c["best_level"]) <= 4:
                row.append(f"E{c['best_level']} {c['outcome']}")
            else:
                n_gap += 1
                row.append("?" if c and c["best_level"] == 5 else ("H/C/Q" if c else ""))
        lines.append(f"| {species[sp]['name_en']} | " + " | ".join(row) + " |")
    total = len(wood_species) * len(PROJECT_WOODS)
    lines[2] += f"\n\n**{n_gap} of {total} cells ({100 * n_gap / total:.0f}%) have no production evidence.**"
    (RES / "gaps.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # figures
    draw_matrix(cells, species, substrates, PROJECT_WOODS, "matrix_project_woods",
                "Species × the woods this project can get: best available evidence")
    evidenced = [s for s in sub_order if any(k[1] == s for k in cells)]
    draw_matrix(cells, species, substrates, evidenced, "matrix_all",
                "Species × every substrate with any evidence")
    draw_profile(evidence, species)

    # summary for README
    lv = defaultdict(int)
    for r in evidence:
        lv[int(r["evidence_level"])] += 1
    summary = {
        "claims": len(evidence), "sources": len(sources),
        "sources_reverified": sum(1 for s in sources.values() if re.match(r"\d{4}-", s["verified"])),
        "by_level": {f"E{k}": lv[k] for k in sorted(lv)},
        "cells": len(cells), "plan_pairs": len(audit), "plan_verdicts": dict(sorted(counts.items())),
        "project_wood_gaps": f"{n_gap}/{total}",
    }
    (RES / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
