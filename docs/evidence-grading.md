# How claims are graded

Every row in `data/evidence.csv` is one **claim**: a species, a substrate, an outcome, and the source it came from. A claim gets two independent labels. The **evidence level** says how much the source can be trusted for this question. The **outcome** says what the source found.

## Evidence levels

| Level | Name | What qualifies | Examples here |
|---|---|---|---|
| **E1** | Replicated trial | Peer-reviewed trial with replicated units and an inferential test, **and the design has been checked against the paper** (`sources.csv: verified`) | Sarıyer et al. 2023, hiratake on 4 log woods, 3 replicates, LSD P<0.05 |
| **E2** | Single trial or report | One trial without inferential statistics, a prefectural or institutional report, or a peer-reviewed study whose replication we could not check. Published host records also sit here. | Aichi maitake 10-wood trial; Saga kikurage tables; Frey et al. 2020 (abstract only) |
| **E3** | Guide rating or grower report | An expert rating such as ◎/○ with no data behind it in the source | Ibaraki prefectural log guide |
| **E4** | Project pilot | This project's own observation: unreplicated, unblinded, often unmeasured | Eringi on fresh carrot (OBS-01) |
| **E5** | Extrapolation | Reasoning from a related host, related fungus or wood traits. **Not a finding.** Every E5 row states its reasoning. | Golden oyster on zelkova, because zelkova is in the elm family |

Rules the validator enforces (`analysis/build.py`):

* The study type fixes the level: `replicated-trial` is E1, `single-trial` and `host-record` are E2, `guide-rating` is E3, `pilot` is E4, and `extrapolation` is E5.
* E1 needs a source marked as re-read. A paper that might be E1 is E2 until someone checks its design.
* An E5 row with no stated reasoning fails validation.
* **Project-plan grades are not evidence.** They live in `data/plan_assignments.csv`, and the audit tests them against the evidence.

## Outcomes

`metric_class` decides what a claim can say:

| metric_class | Allowed outcomes | Enters the matrix colour? |
|---|---|---|
| production | excellent · good · marginal · poor · none · fruited-unquantified (E4 only) | **Yes** |
| colonisation | colonised | No: shown as **C** |
| quality | excellent … none (e.g. bioactivity, cordycepin) | No: shown as **Q** |
| host-record | host | No: shown as **H** |

Production outcomes are read relative to the best wood in the same trial, or on the source's own scale:

* **excellent**: best or tied-best in the trial, ◎, or clearly above the reference wood
* **good**: fruits at a useful level, ○, or close to the reference
* **marginal**: fruits, but well below the best (roughly < 50%), or only for one year
* **poor**: a trace yield
* **none**: no fruiting, or no colonisation

For Saga's kikurage tables, which report kg per m³ of log, the cut-offs are fixed in advance: excellent ≥ 25, good 10–25, marginal 2–10, poor > 0–2, none 0. Where a source gives only a rank, `outcome_basis = rank-only` and the outcome follows from the rank. These cells are weaker than measured ones.

## From claims to a matrix cell

1. Keep only production claims. If any of them are log-type (log, short log, stump, buried root), keep only those, because this is a log-culture project and sawdust-bed results do not always transfer.
2. Keep the claims at the **best (lowest-numbered) level present**. A weaker claim never overrides a stronger one, however many weaker claims there are.
3. Take the median outcome of those claims and **round down**.
4. Flag a **conflict** if those claims span two or more outcome steps. A conflict usually means year-to-year or species-within-group variation, which is real information.

## Plan audit verdicts

| Verdict | Meaning |
|---|---|
| supported | Best level E1 to E3 and outcome good or excellent, with no conflict |
| weak | E1 to E3, marginal |
| contradicted | E1 to E3, poor or none |
| conflicting evidence | E1 to E3 claims disagree |
| project pilot only | Only the project's own observation |
| hypothesis only | Only an extrapolation |
| colonisation only / no production data | Evidence exists, but none of it is about yield |
| no evidence | Nothing found |

## Known limits

* **Taxon lumping.** Substrates are grouped at the level the project can act on, such as "evergreen oaks" or "cherry". `substrate_as_reported` keeps the exact taxon, and conflict flags show where a group hides real differences, such as シラカシ = 0 vs イチイガシ = 24.5 kg/m³ for kikurage.
* **Strain effects can rival wood effects.** In Aichi, maitake on the same konara ranged from 248 to 366 g/kg by strain, and one strain gave nothing on sugi or hinoki. A wood grade is never strain-free.
* **Fungus taxonomy.** The Japanese kikurage log trials all used *Auricularia cornea*. Whether they transfer to *A. heimuer* is unknown.
* **Coverage.** Literature was searched in English and Japanese through project research threads, not by a systematic review protocol. `sources.csv: verified` records which sources were re-read against the original on 2026-11-19. Rows from sources not re-read carry that status, so the gap is visible.
