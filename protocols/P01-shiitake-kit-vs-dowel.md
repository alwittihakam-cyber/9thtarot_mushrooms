# P01: Shiitake on raw konara: substrate-kit inoculum vs dowel spawn

| | |
|---|---|
| Status | **Planned by the project.** Pre-registration draft v2. Freeze before the first log is inoculated. |
| Season | Fell Dec 2026 to Jan 2027; inoculate Feb to Apr 2027; quality sampling from the first natural flush until spring 2029 |
| Site | Project log yard, Tanzawa–Oyama foothills, Kanagawa |
| Lead | J. A. Wittcop |
| Builds on | EV0122: buna-shimeji kit inoculum on konara, a project pilot judged "up to ~40% faster", but by estimate only. Shiitake on konara is rated E3 excellent for fruiting (IBARAKI-GUIDE). Log versus sawdust affects shiitake taste chemistry, but in mixed directions (EV0136, EV0137). |
| Outcomes | Culinary quality and chemical potency, as in [`docs/quality-methods.md`](../docs/quality-methods.md). Yield is not measured. |
| Licence | CC BY-NC-SA 4.0 |

## 1. Why this trial

The project's pilots suggest a fully colonised kit block, broken up and used as inoculum, colonises raw wood faster than dowel spawn. A faster route only helps if it **does not cost quality.** A strain kept as a fast-growing bag culture could, in principle, give a different mushroom on logs. This trial asks both questions together.

## 2. Hypotheses

* **H1 (co-primary, method).** Kit-block inoculum reaches end-face colonisation sooner than dowel spawn of the same strain. The predicted time ratio is about 0.71, that is, 1.4× faster.
* **H2 (co-primary, quality, non-inferiority).** Shiitake from kit-inoculated logs are **not worse** than shiitake from dowel-inoculated logs on blind-rated *overall liking*. The non-inferiority margin is 10 points on a 0–100 scale.
* **Secondary.** The arms differ in (a) umami chemistry: Glu + Asp, 5′-GMP and EUC; (b) β-glucan (lentinan) and ergothioneine; (c) cap thickness, firmness and the share of hana donko; (d) shelf life at 4 °C; (e) contamination at 12 months.

Both co-primaries are tested at α = 0.05. H1 is two-sided. H2 is one-sided against the margin. The trial is a success for the method only if H1 is supported **and** H2 holds.

## 3. Design

A randomised complete block design. **Blocks are source trees.** Each tree's logs are split equally between the arms.

| | |
|---|---|
| Arms | **Kit:** holes packed with crumbled shiitake kit block. **Dowel:** commercial dowel spawn, one per hole. |
| Same strain | **Required.** Both inocula are the same named strain from the same supplier. If no such pair can be bought, the result compares *this kit with this dowel product*, and that limit is written into the deviation log. |
| Sentinels | 1 uninoculated log from every second tree (5 logs) records the background of wild shiitake and contaminants. |
| Size | **10 trees × 3 logs per arm × 2 arms = 60 logs**, plus 5 sentinels. These are part of the 70 shiitake logs already planned. |
| Power, H1 | 0.97 at 1.4× faster; 0.56 at 1.2× (`results/power.md`) |
| Power, H2 | One sample per log. Each of 24 panellists tastes one kit sample and one dowel sample per session, over two sessions, and each panellist's sessions are averaged. This gives about 0.8 to exclude a 10-point deficit if the true difference is 0 and the within-taster SD is about 18. |
| Power, chemistry | 10 replicates per arm, one per tree, pooled within the tree. This gives 0.96 at 1.3× if CV ≈ 15%. |

### Units and inclusion

* Konara from healthy living trees. **Never use oak-wilt (ナラ枯れ) trees.**
* Logs 90 cm long and 8–15 cm in diameter, with ≥ 95% intact bark. Fell dormant trees and rest them 3–6 weeks.
* Exclusions happen only before randomisation. After it, every log stays in its allocated arm.

## 4. Randomisation and blinding

1. Tag each tree (T01 to T10) and cut 6 qualifying logs from it.
2. Fix the seed by a public act on the day, such as the last 4 digits of the Nikkei 225 close, and record it here: `seed = ____`.
3. Run `python analysis/randomise.py P01 --blocks T01,...,T10 --per-arm 3 --seed <seed>`.
4. Fit the logs with blind-code tags. The allocation file stays with a second person until the analysis code is committed.
5. **Wax over both hole types.** Arms then look alike in the yard, in photos and in the kitchen.
6. The colonisation scorer, the cook, the panellists and the lab see only codes.

## 5. Procedures

* **Holes:** 2 × diameter (cm) per log, in staggered rows, with the same 8.5 mm bit for both arms.
* **Kit arm:** use a fully colonised block that has not fruited and is less than 2 weeks from purchase. Crumble it into a clean tub, pack each hole level and wax it.
* **Dowel arm:** hammer in one dowel per hole and wax it.
* Lay all logs in one randomly mixed stack, with the same shade and the same hand watering. Log every watering in `events.csv`.
* **Fan:** manage the fan the same way for both arms during each flush, following the grower's staged method ([MET-01](../docs/observations/MET-01.md)): pointed away in the early stage, directly at the caps in mid-stage, and away again late. Fan placement must not favour either arm, because hana donko share is an outcome. Log fan direction changes in `events.csv`.
* **Fruiting:** natural flushes only. Sample quality from the **first natural autumn or spring flush** in which at least 6 logs per arm fruit.

## 6. Outcomes

| Outcome | Definition |
|---|---|
| **Days to colonisation (H1)** | Days to the first monthly score where **both** cut ends are ≥ 50% colonised. Scored from blinded photos against the chart in `docs/metrics.md`. |
| **Overall liking (H2)** | Blind panel, 0–100 line scale, pan-seared to the standard method (`docs/quality-methods.md` §2) |
| Umami / meaty intensity, aroma, firmness | Same panel and session, as secondary attributes |
| Glu + Asp, 5′-GMP, EUC | Freeze-dried pooled sample per tree and arm, HPLC (`docs/quality-methods.md` §4) |
| β-glucan, ergothioneine | Same samples (§5) |
| Cap thickness, firmness, hana donko share | On the harvest day (§3) |
| Shelf life | Days at 4 °C to the first score ≥ 2 (§3) |
| Contamination | % of logs with competitor fruit bodies or stroma at day 365 |

## 7. Analysis plan (fixed before data)

* **H1:** `log(days) ~ arm + log(diameter) + (1 | tree)`. Report the time ratio with its 95% CI. A log not colonised by day 540 is set to 540, with an interval-censored Weibull model as a sensitivity check.
* **H2:** `liking ~ arm + serving_position + session + (1 | taster)`. Non-inferiority holds if the lower 95% bound of (kit − dowel) is above −10.
* **Secondary outcomes:** the same mixed-model structure, with tree as the block for log-level measures. Holm correction across the secondary family.
* No interim efficacy analyses. Missing logs are reported and not imputed.
* The code `analysis/p01_analysis.py` is committed before the allocation is unsealed.

## 8. What counts as support

* **The method is supported** if the H1 CI for the time ratio lies below 1 **and** H2 non-inferiority holds.
* **The method is rejected for premium use** if kit-inoculated shiitake is significantly worse on liking, even if it colonises faster.
* Results are published whichever way they go.

## 9. Data files

`trials/P01/`: `logs.csv`, `colonisation.csv`, `samples.csv`, `sensory.csv`, `assays.csv`, `texture.csv`, `shelf_life.csv`, `events.csv`, `environment.csv` (templates in `templates/`), and photos.

## 10. Registration and deviations

Fill in the seed, supplier, strain, panel recruitment and lab. Commit, tag `prereg/P01-v2`, and register on OSF Registries before the first inoculation.

| Date | Deviation | Reason |
|---|---|---|
| 2026-11-19 | v2: primary outcome changed from yield-linked measures to culinary quality and potency; yield removed | Project priorities: quality and potency, not yield. The change was made before any data existed. |
