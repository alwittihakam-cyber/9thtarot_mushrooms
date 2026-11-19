# P01: Shiitake on raw konara: substrate-kit inoculum vs dowel spawn

| | |
|---|---|
| Status | **Planned by the project.** Pre-registration draft v1. Freeze before the first log is inoculated. |
| Season | Fell Dec 2026 to Jan 2027, inoculate Feb to Apr 2027, follow until Mar 2029 |
| Site | Project log yard, Tanzawa–Oyama foothills, Kanagawa |
| Lead | Hakam Al-Witti |
| Evidence it builds on | EV0122 (buna-shimeji kit inoculum on konara, project pilot, "up to ~40% faster", estimated); shiitake × konara is E3 excellent (IBARAKI-GUIDE) |
| Licence | CC BY-NC-SA 4.0 |

## 1. Why this trial

The project's own pilots suggest that a fully colonised substrate kit block, broken up and used as inoculum, colonises raw logs faster than commercial sawdust or dowel spawn: buna-shimeji on konara (OBS-02) and eringi on carrots (OBS-01). The speed-up was estimated by eye, never timed, and the strains in the kit and the spawn were different. If it holds, it is a cheap, spawn-free inoculation route for small growers, and nothing on it has been published.

This trial tests the claim on the project's main crop, under conditions where the claim could fail.

## 2. Hypotheses

* **H1 (primary).** Konara logs inoculated with kit-block inoculum reach end-face colonisation sooner than logs inoculated with dowel spawn of the same strain. The predicted effect is a time ratio of about 0.71, which means 1.4× faster.
* **H0.** There is no difference in time to colonisation.
* **Secondary, exploratory.** The kit arm differs from the dowel arm in (a) days to first fruiting, (b) yield per log volume over two years, (c) contamination at 12 months, and (d) the share of hana donko grade caps.

Two-sided tests. A result in the dowel arm's favour will be reported the same way.

## 3. Design

A randomised complete block design. **Blocks are source trees.** Every tree is cut into logs, and its logs are split equally between the two arms, so differences between trees (bark, density, felling date) cancel out.

| | |
|---|---|
| Arms | **Kit**: holes packed with crumbled shiitake kit block. **Dowel**: commercial wooden dowel spawn, one per hole. |
| Same strain | **Required.** Both inocula must be the same named strain from the same supplier. Example: a supplier that sells a strain both as plug spawn and as a ready-to-fruit block. If no matching pair can be bought, the result only compares *this kit with this dowel product*. Write that limit into the deviation log and the paper. |
| Sentinel logs | 1 uninoculated log from every second tree (5 logs). These show the background of wild shiitake and contaminants and are not part of the primary analysis. |
| Size | **10 source trees × 3 logs per arm × 2 arms = 60 logs**, plus 5 sentinels. This replaces 60 of the 70 shiitake logs the plan already counts, so the trial costs no extra wood. |
| Power | 0.97 to detect 1.4× faster and 0.56 to detect 1.2× faster (`results/power.md`, assuming a within-tree CV of about 30%). The trial is built to confirm or refute the pilot's large effect, not to find small ones. |

### Units and inclusion

* Konara (*Quercus serrata*) from healthy living trees. **Never** use trees with oak wilt (ナラ枯れ): no frass, no wilting, no ambrosia beetle holes.
* Logs 90 cm long and 8 to 15 cm in diameter, with bark intact on at least 95% of the surface.
* Felled while dormant, then rested 3 to 6 weeks before inoculation (WSU FS394E; Shimomura & Hasebe 2004).
* Exclude a log *before randomisation* if its bark is damaged or its diameter is out of range. After randomisation, no log is excluded. Every log stays in the analysis in its allocated arm (intention to treat).

## 4. Randomisation

1. Tag each tree (T01 to T10) when you fell it, and cut 6 qualifying logs from it.
2. Choose the seed by a public act on the day, such as the last four digits of the Nikkei 225 close, and record it here: `seed = ____`.
3. Run `python analysis/randomise.py P01 --blocks T01,...,T10 --per-arm 3 --seed <seed>`.
4. Fix the blind code to each log with an aluminium tag. `allocation.csv` stays with a second person, or in a sealed envelope, until the primary analysis is locked.
5. Inoculate in the order the file lists, so that arm is not confounded with time of day.

## 5. Procedures (identical in both arms except the inoculum)

* **Holes.** Drill twice the log diameter in cm, in staggered rows; a 10 cm log gets 20 holes (IBARAKI-GUIDE). Use the same drill bit (Ø 8.5 mm × 25 mm) for both arms.
* **Kit arm.** Use a block that is fully colonised, has not yet fruited, and is under 2 weeks from purchase. Crumble it in a clean tub and pack each hole level with a tamper. Record the block mass used per log.
* **Dowel arm.** Hammer one dowel into each hole.
* **Seal both arms with wax** so that the holes look alike. This is what makes blinded scoring possible.
* Lay all logs together in one random mixed stack in the same shaded laying yard, under the same watering, which is the hand hose schedule logged in `events.csv`.
* Fruiting: allow natural flushes in year 1. From year 2, use one forced-fruiting soak per season, the same day for all logs.

## 6. Outcomes

| Outcome | Definition | When |
|---|---|---|
| **Primary: days to colonisation** | Days from inoculation to the first monthly score where **both** cut ends show ≥ 50% of the cross-section colonised (white mycelium or a clear colonisation front). The score comes from blinded photos. | Monthly from day 60 |
| Days to first fruiting | Days from inoculation to the first fruit body ≥ 2 cm cap diameter | Weekly in season |
| Yield per log volume | Total fresh mass of all harvests in kg per m³ of log. Volume uses Smalian's formula from both end diameters and the length (`docs/metrics.md`) | To Mar 2029 |
| Biological efficiency | Fresh mass ÷ log dry mass × 100. Dry mass is estimated from fresh mass and a moisture core (`docs/metrics.md`) | To Mar 2029 |
| Contamination | % of logs with Hypoxylon, Trichoderma or other competitor fruit bodies or stroma | Day 365 |
| Hana donko share | Share of caps graded hana donko at harvest | Each harvest |

**Scoring.** Each month, photograph both ends of each log with a grey card and the blind code tag in frame. A scorer who did not inoculate scores the photos in random order, using the 0/25/50/75/100% chart in `docs/metrics.md`. Before the trial, the scorer re-scores 10% of the photos to check agreement, and the pre-trial target is a weighted κ of at least 0.7.

## 7. Analysis plan (fixed before data)

* **Primary.** A linear mixed model on log(days): `log(days) ~ arm + log(diameter) + (1 | tree)`. Report the time ratio exp(β_arm) with its 95% CI. Because the design is balanced, a paired t-test on per-tree mean differences gives the same answer, and both will be reported.
* **Censoring.** A log that has not reached the threshold by day 540 is assigned 540, which is conservative for the faster arm. As a sensitivity check, an interval-censored Weibull model will be fitted.
* **Secondary outcomes** are tested with Holm correction across the four. Yield and BE are analysed on the log scale with the same model.
* No interim analyses on the primary outcome, and no early stopping for efficacy. Lost or stolen logs are reported, and missing data are not imputed for the primary analysis.
* Code: `analysis/p01_analysis.py` will be committed **before** the allocation is unsealed.

## 8. What would count as support

* The pilot claim is **supported** if the 95% CI for the time ratio lies entirely below 1.
* It is **refuted as a large effect** if the CI excludes 0.71, that is, if a 1.4× speed-up is ruled out.
* Anything else is inconclusive. It will be reported as such, with the estimate.

## 9. Data files

`trials/P01/`: `logs.csv`, `colonisation.csv`, `harvests.csv`, `events.csv` and `environment.csv`, using the templates in `templates/`, plus the photos (`photos/<date>/<blind_code>_<end>.jpg`). All raw data are published with the results, including if H1 fails.

## 10. Registration and deviations

1. Fill in the seed, supplier, strain and dates.
2. Commit, then tag the commit: `git tag prereg/P01-v1`.
3. Upload this file to OSF Registries (https://osf.io/registries) before the first inoculation.
4. Record every later change below, with its date and reason. Never edit the text above.

| Date | Deviation | Reason |
|---|---|---|
| | | |
