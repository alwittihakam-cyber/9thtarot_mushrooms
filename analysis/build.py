#!/usr/bin/env python3
"""Validate the dataset and regenerate every derived result.

    python analysis/build.py            # validate + rebuild results/
    python analysis/build.py --check    # validate only, exit 1 on any error

The project's outcomes, in order of importance:
    culinary   taste (umami amino acids, 5'-nucleotides), aroma, texture, blind sensory
    potency    each species' key compounds (triterpenes, cordycepin, beta-glucans ...)
    fruiting   only "does it fruit on this substrate at all"; yield is not a goal

Outputs (deterministic text, safe to diff in CI):
    results/matrix_long.csv        one row per class x species x substrate cell
    results/matrix.md              readable tables per species
    results/plan_audit.csv / .md   each planting-plan pairing vs the evidence
    results/gaps.md                what is unknown for the woods the project can get
    results/summary.json
    results/figures/*.png|svg

Aggregation rule (docs/evidence-grading.md): within one outcome class, if any
claims are log-type (log, short log, stump, buried root) only those count. The
cell takes the claims at the BEST (lowest-numbered) evidence level; its outcome
is their median, rounded down. Claims spanning >= 2 outcome steps flag a
conflict. Weaker claims never override stronger ones.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RES = ROOT / "results"
FIG = RES / "figures"

CLASSES = ["culinary", "potency", "fruiting"]
CLASS_TITLE = {"culinary": "Culinary quality", "potency": "Chemical potency", "fruiting": "Fruits at all?"}
SCORE = {"none": 0, "poor": 1, "marginal": 2, "fruited-unquantified": 2.5, "good": 3, "excellent": 4}
LEVEL_NAME = {1: "E1 replicated trial", 2: "E2 single trial / report", 3: "E3 guide rating",
              4: "E4 project pilot", 5: "E5 extrapolation"}
ALLOWED_LEVEL = {"replicated-trial": {1}, "single-trial": {2}, "host-record": {2},
                 "guide-rating": {3}, "pilot": {4}, "extrapolation": {5}}
CLASS_DIMENSIONS = {
    "culinary": {"sensory", "taste-umami", "taste-5'-GMP", "aroma", "texture", "nutrition", "shelf-life", "morphology"},
    "potency": {"triterpenes", "polysaccharides", "beta-glucan", "cordycepin", "ergothioneine", "erinacines",
                "antioxidant", "bioactivity"},
    "fruiting": {"fruiting"}, "colonisation": {"colonisation"}, "host-record": {"host"},
}
LOG_FORMS = {"log", "short-log", "stump", "buried-root"}
PROJECT_WOODS = ["log-generic", "konara", "kunugi", "carpinus", "ostrya", "cerasus", "prunus-mume",
                 "acer", "celtis", "cinnamomum", "sugi", "daucus-root"]


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
    if errors:
        return errors

    sources = {s["source_id"]: s for s in tables["sources"]}
    for i, r in enumerate(tables["evidence"], start=2):
        where = f"data/evidence.csv:{i} ({r['claim_id']})"
        lvl = int(r["evidence_level"])
        st, mc, out = r["study_type"], r["metric_class"], r["outcome"]
        if lvl not in ALLOWED_LEVEL[st]:
            errors.append(f"{where}: study_type {st} cannot be E{lvl}")
        if lvl == 1 and not re.match(r"\d{4}-", sources[r["source_id"]]["verified"]):
            errors.append(f"{where}: E1 requires the replicated design to be verified in sources.csv")
        if lvl == 5 and not r["notes"].strip():
            errors.append(f"{where}: an extrapolation must state its reasoning in notes")
        if r["dimension"] not in CLASS_DIMENSIONS[mc]:
            errors.append(f"{where}: dimension {r['dimension']!r} does not belong to metric_class {mc!r}")
        if mc == "host-record" and out != "host":
            errors.append(f"{where}: host-record claims use outcome 'host'")
        if mc != "host-record" and out == "host":
            errors.append(f"{where}: outcome 'host' only for host-record claims")
        if mc == "colonisation" and out != "colonised":
            errors.append(f"{where}: colonisation claims use outcome 'colonised'")
        if mc in CLASSES and out not in SCORE:
            errors.append(f"{where}: {mc} outcome must be one of {list(SCORE)}")
        if out == "fruited-unquantified" and not (lvl == 4 and mc == "fruiting"):
            errors.append(f"{where}: 'fruited-unquantified' is reserved for project fruiting pilots")
        src = sources[r["source_id"]]
        if not (src["url"] or src["doi"]) and src["source_kind"] != "extrapolation":
            errors.append(f"{where}: source {r['source_id']} has neither DOI nor URL")
    return errors


# -------------------------------------------------------------------- aggregate
def label_for(score: float, pilot: bool = False) -> str:
    """Median score -> outcome label, rounding DOWN. 'fruited-unquantified' only for pilots."""
    best = "none"
    for name, s in sorted(SCORE.items(), key=lambda kv: kv[1]):
        if name == "fruited-unquantified" and not pilot:
            continue
        if s <= score + 1e-9:
            best = name
    return best


def aggregate(evidence: list[dict], cls: str = "fruiting") -> dict[tuple[str, str], dict]:
    """One cell per (species, substrate) for one outcome class."""
    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in evidence:
        cells[(r["species_id"], r["substrate_id"])].append(r)
    out = {}
    for key, claims in cells.items():
        graded = [c for c in claims if c["metric_class"] == cls]
        logs = [c for c in graded if c["substrate_form"] in LOG_FORMS]
        if logs:
            graded = logs
        other = sorted({c["metric_class"] for c in claims if c["metric_class"] != cls})
        row = {"class": cls, "species_id": key[0], "substrate_id": key[1],
               "best_level": "", "outcome": "", "conflict": "",
               "n_claims_in_class": len(graded), "n_claims_all": len(claims),
               "best_level_claims": "", "lower_level_claims": "",
               "dimensions": ";".join(sorted({c["dimension"] for c in graded})),
               "other_evidence": ";".join(other),
               "sources": ";".join(sorted({c["source_id"] for c in claims}))}
        if graded:
            best = min(int(c["evidence_level"]) for c in graded)
            top = [c for c in graded if int(c["evidence_level"]) == best]
            scores = sorted(SCORE[c["outcome"]] for c in top)
            n = len(scores)
            med = scores[n // 2] if n % 2 else (scores[n // 2 - 1] + scores[n // 2]) / 2
            row.update(best_level=best, outcome=label_for(med, pilot=(best == 4)),
                       conflict="yes" if max(scores) - min(scores) >= 2 else "",
                       best_level_claims=";".join(c["claim_id"] for c in top),
                       lower_level_claims=";".join(c["claim_id"] for c in graded if int(c["evidence_level"]) != best))
        out[key] = row
    return out


# ------------------------------------------------------------------- plan audit
def verdict(cell: dict | None) -> str:
    if not cell or cell["best_level"] == "":
        return "no evidence"
    lvl, out = int(cell["best_level"]), cell["outcome"]
    if lvl == 5:
        return "hypothesis only"
    if lvl == 4:
        return "project pilot only"
    if cell["conflict"]:
        return "mixed evidence"
    if out in ("excellent", "good"):
        return "supported"
    if out == "marginal":
        return "weak"
    return "contradicted"


VERDICT_ORDER = ["contradicted", "mixed evidence", "weak", "no evidence", "hypothesis only",
                 "project pilot only", "supported"]


def plan_audit(plan, cells_by_class, species, substrates):
    rows = []
    for p in plan:
        sp, sub = p["species_id"], p["substrate_id"]
        row = {"species": species[sp]["name_en"], "substrate": substrates[sub]["name_en"], "role": p["role"]}
        for cls in CLASSES:
            c = cells_by_class[cls].get((sp, sub))
            row[f"{cls}_verdict"] = verdict(c)
            row[f"{cls}_level"] = f"E{c['best_level']}" if c and c["best_level"] != "" else ""
        # Evidence about log culture in general (wood not named) for this species
        lg = []
        for cls in ("culinary", "potency"):
            c = cells_by_class[cls].get((sp, "log-generic"))
            if c and c["best_level"] != "":
                lg.append(f"{cls}: {c['outcome']}{' (mixed)' if c['conflict'] else ''} E{c['best_level']}")
        row["log_vs_sawdust_evidence"] = "; ".join(lg)
        row["species_id"], row["substrate_id"] = sp, sub
        rows.append(row)
    key = lambda r: (min(VERDICT_ORDER.index(r["culinary_verdict"]), VERDICT_ORDER.index(r["potency_verdict"])),
                     VERDICT_ORDER.index(r["fruiting_verdict"]), r["role"] != "now", r["species"])
    rows.sort(key=key)
    return rows


# --------------------------------------------------------------------- figures
COLORS = {"none": "#a8322f", "poor": "#e88b88", "marginal": "#e4e2dc", "fruited-unquantified": "#cde2fb",
          "good": "#86b6ef", "excellent": "#256abf"}
INK, MUTED, SURFACE = "#0b0b0b", "#6b6a66", "#fcfcfb"


def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams.update({"svg.hashsalt": "tanzawa", "font.family": "DejaVu Sans"})
    import matplotlib.pyplot as plt
    return plt


def _save(fig, stem):
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{stem}.{ext}", facecolor=SURFACE,
                    metadata={"Software": None} if ext == "png" else {"Date": None, "Creator": None})


def _draw_panel(ax, cells, sp_ids, columns, substrates, species, title, ylabels=True):
    from matplotlib.patches import Rectangle
    ax.set_facecolor(SURFACE)
    for yi, sp in enumerate(sp_ids):
        for xi, sub in enumerate(columns):
            c = cells.get((sp, sub))
            x, y = xi, len(sp_ids) - 1 - yi
            if not c or c["best_level"] == "":
                ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, fc="none", ec="#ecebe7", lw=.6))
                continue
            lvl = int(c["best_level"])
            if lvl == 5:
                ax.add_patch(Rectangle((x + .08, y + .08), .84, .84, fc="none", ec=MUTED, lw=.8, ls=(0, (2, 2))))
                ax.text(x + .5, y + .5, "?", ha="center", va="center", fontsize=7.5, color=MUTED)
                continue
            ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, fc=COLORS[c["outcome"]], ec=SURFACE, lw=1,
                                   hatch="////" if lvl == 4 else None))
            dark = c["outcome"] in ("excellent", "none")
            ax.text(x + .5, y + .5, f"E{lvl}", ha="center", va="center", fontsize=6.3,
                    color="#ffffff" if dark else INK, fontweight="bold")
            if c["conflict"]:
                ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, fc="none", ec=INK, lw=1.4))
    ax.set_xlim(0, len(columns))
    ax.set_ylim(0, len(sp_ids))
    ax.set_xticks([i + .5 for i in range(len(columns))])
    ax.set_xticklabels([substrates[s]["name_en"] for s in columns], rotation=60, ha="right", fontsize=7, color=INK)
    ax.set_yticks([len(sp_ids) - 1 - i + .5 for i in range(len(sp_ids))])
    ax.set_yticklabels([species[s]["name_en"] for s in sp_ids] if ylabels else [], fontsize=7.5, color=INK)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, loc="left", fontsize=9.5, color=INK, pad=6)


def _legend(fig, y=0.0):
    from matplotlib.patches import Patch
    handles = [Patch(fc=COLORS[k], ec="none", label=k) for k in ("excellent", "good", "marginal", "poor", "none")]
    handles += [Patch(fc=COLORS["fruited-unquantified"], ec="none", hatch="////", label="project pilot: fruited"),
                Patch(fc="none", ec=MUTED, ls="--", label="? extrapolation only"),
                Patch(fc="none", ec=INK, lw=1.4, label="mixed / conflicting claims")]
    fig.legend(handles=handles, loc="lower left", ncol=8, fontsize=7, frameon=False, bbox_to_anchor=(0.01, y))


def draw_overview(cells_by_class, species, substrates):
    plt = _mpl()
    sp_ids = list(species)
    fig, axes = plt.subplots(1, 3, figsize=(17, 8.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    for k, (ax, cls) in enumerate(zip(axes, CLASSES)):
        _draw_panel(ax, cells_by_class[cls], sp_ids, PROJECT_WOODS, substrates, species,
                    CLASS_TITLE[cls] + ("  (secondary)" if cls == "fruiting" else ""), ylabels=(k == 0))
    fig.suptitle("Species × the woods this project can get: best available evidence, by outcome",
                 x=0.01, ha="left", fontsize=11.5, color=INK)
    fig.text(0.01, 0.935, "Cell text = best evidence level (E1 strongest). Blank = nothing published or tested. "
             "'Any log' = studies comparing log culture with sawdust beds without naming the wood.",
             fontsize=7.5, color=MUTED)
    _legend(fig)
    fig.tight_layout(rect=(0, 0.05, 1, 0.93))
    _save(fig, "matrix_project_woods")
    plt.close(fig)


def draw_full(cells, cls, species, substrates):
    plt = _mpl()
    cols = [s for s in substrates if any(k[1] == s and v["best_level"] != "" for k, v in cells.items())]
    sp_ids = [s for s in species if any(k[0] == s and v["best_level"] != "" for k, v in cells.items())]
    if not cols:
        return
    w = max(7.5, 2.2 + 0.42 * len(cols))
    h = 2.4 + 0.34 * len(sp_ids)
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    _draw_panel(ax, cells, sp_ids, cols, substrates, species,
                f"{CLASS_TITLE[cls]}: every species and substrate with evidence")
    _legend(fig)
    fig.tight_layout(rect=(0, 0.08 if h < 6 else 0.05, 1, 1))
    _save(fig, f"matrix_all_{cls}")
    plt.close(fig)


def draw_profile(evidence, species):
    plt = _mpl()
    from matplotlib.patches import Patch
    ramp = {1: "#104281", 2: "#2a78d6", 3: "#6da7ec", 4: "#b7d3f6", 5: "#e4e2dc"}
    sp_ids = list(species)
    counts = {cls: {sp: [0] * 5 for sp in sp_ids} for cls in CLASSES}
    for r in evidence:
        if r["metric_class"] in CLASSES:
            counts[r["metric_class"]][r["species_id"]][int(r["evidence_level"]) - 1] += 1
    order = sorted(sp_ids, key=lambda s: (-sum(counts["culinary"][s]) - sum(counts["potency"][s]),
                                          -sum(counts["fruiting"][s]), species[s]["name_en"]))
    fig, axes = plt.subplots(1, 3, figsize=(12, 6.2), dpi=150, sharey=True)
    fig.patch.set_facecolor(SURFACE)
    xmax = max(sum(v) for c in counts.values() for v in c.values()) + 3
    for ax, cls in zip(axes, CLASSES):
        ax.set_facecolor(SURFACE)
        for i, sp in enumerate(order):
            left = 0
            for lv in range(1, 6):
                v = counts[cls][sp][lv - 1]
                if v:
                    ax.barh(len(order) - 1 - i, v, left=left, color=ramp[lv], height=.62, edgecolor=SURFACE, lw=1.2)
                left += v
            ax.text(left + .3, len(order) - 1 - i, str(left), va="center", fontsize=6.5, color=MUTED)
        ax.set_xlim(0, xmax)
        ax.set_title(CLASS_TITLE[cls], loc="left", fontsize=9.5)
        ax.grid(axis="x", color="#ecebe7", lw=.6)
        ax.set_axisbelow(True)
        ax.tick_params(length=0, labelsize=7)
        for s in ax.spines.values():
            s.set_visible(False)
    axes[0].set_yticks(range(len(order)))
    axes[0].set_yticklabels([species[s]["name_en"] for s in reversed(order)], fontsize=7.5)
    fig.suptitle("Claims per species, by outcome and evidence level", x=0.01, ha="left", fontsize=11)
    fig.legend(handles=[Patch(fc=ramp[lv], label=LEVEL_NAME[lv]) for lv in range(1, 6)], fontsize=7,
               frameon=False, loc="lower left", ncol=5, bbox_to_anchor=(0.01, 0))
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    _save(fig, "evidence_profile")
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
    cells_by_class = {cls: aggregate(evidence, cls) for cls in CLASSES}
    FIG.mkdir(parents=True, exist_ok=True)
    sp_order, sub_order = list(species), list(substrates)

    # long matrix: only cells with graded evidence in that class, plus non-graded cells once (class 'fruiting')
    long_rows = []
    for cls in CLASSES:
        for r in cells_by_class[cls].values():
            if r["best_level"] != "" or (cls == "fruiting" and not any(
                    cells_by_class[c][(r["species_id"], r["substrate_id"])]["best_level"] != "" for c in CLASSES)):
                long_rows.append(r)
    long_rows.sort(key=lambda r: (CLASSES.index(r["class"]), sp_order.index(r["species_id"]),
                                  sub_order.index(r["substrate_id"])))
    write_csv(RES / "matrix_long.csv", long_rows, list(long_rows[0].keys()))

    claims_by_id = {c["claim_id"]: c for c in evidence}
    lines = ["# Species × substrate matrix", "",
             "Generated by `analysis/build.py`; do not edit by hand. Culinary quality and chemical potency are the "
             "primary outcomes. *Fruits at all?* answers only whether the species fruits on the substrate; quantity "
             "is not a goal of this project.", ""]
    for sp in sp_order:
        block = []
        for cls in CLASSES:
            rows = [r for r in cells_by_class[cls].values() if r["species_id"] == sp and r["best_level"] != ""]
            if not rows:
                continue
            tab = []
            for r in sorted(rows, key=lambda r: (r["best_level"], -SCORE[r["outcome"]])):
                ev = []
                for cid in r["best_level_claims"].split(";"):
                    c = claims_by_id[cid]
                    form = "" if c["substrate_form"] == "log" else f" [{c['substrate_form']}]"
                    dim = f"{c['dimension']}: " if cls != "fruiting" else ""
                    ev.append(f"{cid} {dim}{c['value'] or c['outcome']}{form} ({c['source_id']})")
                tab.append({"sub": substrates[r["substrate_id"]]["name_en"], "lvl": f"E{r['best_level']}",
                            "out": r["outcome"] + (" ⚠ mixed" if r["conflict"] else ""), "ev": "; ".join(ev)})
            block += [f"### {CLASS_TITLE[cls]}", "",
                      md_table(tab, ["sub", "lvl", "out", "ev"], ["Substrate", "Best level", "Outcome", "Claims at best level"]), ""]
        if block:
            s = species[sp]
            lines += [f"## {s['name_en']} ({s['name_ja']}, *{s['scientific_name']}*)", ""] + block
    (RES / "matrix.md").write_text("\n".join(lines), encoding="utf-8")

    # plan audit
    audit = plan_audit(plan, cells_by_class, species, substrates)
    write_csv(RES / "plan_audit.csv", audit, list(audit[0].keys()))
    lines = ["# Audit of the planting plan", "",
             "Each species–substrate pairing in the Log Yard Plan v2, checked against the evidence for each outcome. "
             "Plan grades are not evidence. Generated by `analysis/build.py`.", "",
             "| Verdict | Culinary | Potency | Fruits at all? |", "|---|---|---|---|"]
    for v in VERDICT_ORDER:
        n = [sum(1 for a in audit if a[f"{c}_verdict"] == v) for c in CLASSES]
        if any(n):
            lines.append(f"| {v} | " + " | ".join(map(str, n)) + " |")
    lines += ["", "`log_vs_sawdust_evidence` reports studies on log culture in general (wood not named) for that "
              "species. It says log culture affects quality; it says nothing about which wood.", "",
              md_table(audit, ["species", "substrate", "role", "culinary_verdict", "potency_verdict", "fruiting_verdict",
                               "fruiting_level", "log_vs_sawdust_evidence"],
                       ["Species", "Planned substrate", "Role", "Culinary", "Potency", "Fruits at all?", "Level",
                        "Log vs sawdust evidence"]), ""]
    (RES / "plan_audit.md").write_text("\n".join(lines), encoding="utf-8")

    # gaps
    woods = [w for w in PROJECT_WOODS if w != "log-generic"]
    lines = ["# What is unknown for the woods the project can get", "",
             "Generated by `analysis/build.py`. A cell counts as known only with E1–E4 evidence.", ""]
    summary_gaps = {}
    for cls in CLASSES:
        known = [(sp, w) for sp in sp_order for w in woods
                 if (c := cells_by_class[cls].get((sp, w))) and c["best_level"] != "" and int(c["best_level"]) <= 4]
        total = len(sp_order) * len(woods)
        summary_gaps[cls] = f"{len(known)}/{total}"
        lines += [f"## {CLASS_TITLE[cls]}: {len(known)} of {total} species × wood cells have evidence", ""]
        if known:
            lines += [f"- {species[sp]['name_en']} × {substrates[w]['name_en']}: "
                      f"{cells_by_class[cls][(sp, w)]['outcome']} (E{cells_by_class[cls][(sp, w)]['best_level']})"
                      for sp, w in known]
        else:
            lines.append("- none")
        lines.append("")
    lines += ["## Unread sources", "",
              "Listed in `data/sources.csv` with `verified = no` and no claims extracted: "
              + ", ".join(s for s, v in sources.items() if "UNREAD" in s) + ".", ""]
    (RES / "gaps.md").write_text("\n".join(lines), encoding="utf-8")

    # figures
    draw_overview(cells_by_class, species, substrates)
    for cls in CLASSES:
        draw_full(cells_by_class[cls], cls, species, substrates)
    draw_profile(evidence, species)

    lv = defaultdict(int)
    by_class = defaultdict(int)
    for r in evidence:
        lv[int(r["evidence_level"])] += 1
        by_class[r["metric_class"]] += 1
    summary = {
        "claims": len(evidence), "claims_by_class": dict(sorted(by_class.items())), "sources": len(sources),
        "sources_reverified": sum(1 for s in sources.values() if re.match(r"\d{4}-", s["verified"])),
        "by_level": {f"E{k}": lv[k] for k in sorted(lv)},
        "plan_pairs": len(audit),
        "plan_verdicts": {c: {v: sum(1 for a in audit if a[f"{c}_verdict"] == v) for v in VERDICT_ORDER} for c in CLASSES},
        "project_wood_cells_with_evidence": summary_gaps,
    }
    (RES / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
