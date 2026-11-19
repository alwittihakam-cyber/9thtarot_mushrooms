# P02: Eringi on fresh, unsterilised buried carrot: is it really "meatier"?

| | |
|---|---|
| Status | **Proposed, not adopted.** Needs Hakam's yes before it is frozen. |
| Season | Inoculate in spring 2027 (Mar to Apr). A second cohort can follow in autumn 2027. |
| Builds on | [OBS-01](../docs/observations/OBS-01.md). The pilot fruited to a full harvest by 2026-11-19 (EV0121), and five tasters found it "more meaty" than supermarket eringi in an informal comparison (EV0153). Eringi grown on willow sawdust scored best for taste and texture against birch and corncob (EV0142), so substrate can change eringi quality. Eringi is naturally a weak parasite of Apiaceae roots (EV0116), and carrot is an Apiaceae. |
| Outcomes | Culinary quality and chemical potency. Yield is not measured. |

## 1. Why this trial

OBS-01 gives three things to test: it fruited, it tasted meatier, and the caps looked unusual. None is yet a finding:

1. The kit pieces may have fruited **by themselves**, and the carrot may have added nothing.
2. "Meatier" came from an informal 5-person tasting against supermarket eringi, which differed in strain, freshness, maturity and growing system as well as substrate. Blinding was not recorded.
3. Broad, streaked caps may come from **light and air**, not from the carrot.

## 2. Hypotheses

* **H1 (primary, culinary).** In a blind panel, eringi from **carrot + kit** plots score higher on *umami / savoury-meaty* intensity than eringi from **kit-only** plots grown under the same casing and conditions.
* **H2 (co-primary, chemistry).** Carrot + kit eringi have a higher equivalent umami concentration (EUC: glutamate, aspartate and 5′-nucleotides, per g dry weight) than kit-only eringi.
* **H3 (secondary).** Carrot + kit eringi score higher than **commercial indoor eringi of the same strain** on umami/meaty intensity and on overall liking. This is the comparison behind "meatier than usual".
* **H4 (secondary, potency).** Ergothioneine and β-glucan differ between carrot + kit and kit-only eringi.
* **H5 (secondary, identity).** Carrot-only plots, with no inoculum, give no *P. eryngii*.

## 3. Design

| | |
|---|---|
| Arms | **A** carrot + kit · **B** kit only, with the same kit mass at the same depth · **C** carrot only, with no inoculum |
| Plot | 50 × 50 cm. 10 fresh carrots, buried 5 cm deep. Cased with the pilot's straw + leaf-litter mix at 5 cm. |
| Inoculum | One kit lot, crumbled and split by weight: 30 g per plot in arms A and B. Kit pieces keep the main comparison (carrot vs no carrot) free of genotype differences. The grower's own beds now use spore slurry and later liquid culture (OBS-01); see §6b. |
| Blocks | Rows across the shade gradient, each holding one plot of each arm. **12 rows = 36 plots.** |
| Commercial reference | Same strain as the kit, bought fresh within 2 days of each tasting session, from one shop |
| Sampling | First flush only. Harvest when the cap margin is still inrolled and the cap is ≤ 6 cm. That catches the pilot's form before the caps flatten (`docs/quality-methods.md` §1). |

**Power.**

* **H1:** with 24 panellists tasting A versus B, power is 0.74 for a 10-point difference and 0.97 for 15 points, assuming SD 18.
* **H2:** with 12 plots per arm, each one pooled replicate, power is 0.99 at 1.3× if CV ≈ 15%, and 0.56 if CV ≈ 30% (`results/power.md`).
* If arm B fruits on fewer than 6 plots, **that is itself the answer to "did the kit fruit alone?"** H1 and H2 then fall back to A versus the commercial reference, with that fallback reported.

## 4. Randomisation and blinding

* Assign arms within rows with `analysis/randomise.py P02 --blocks R01,...,R12 --per-arm 1 --seed <seed>`.
* Plots carry blind-code stakes only. Once cased, the arms look identical.
* The cook gets bags marked with 3-digit codes. Panellists taste under red light, because cap colour may differ between arms. Serving order follows a Williams design.
* The lab receives coded, freeze-dried samples.

## 5. Outcomes

| Outcome | Method |
|---|---|
| **Umami / savoury-meaty intensity (H1)** | 0–100 line scale, pan-seared slices with no salt (`docs/quality-methods.md` §2) |
| **EUC (H2)** | HPLC free amino acids and 5′-nucleotides, Yamaguchi equation (§4) |
| Overall liking, firmness, juiciness, aroma | Same session |
| Ergothioneine, β-glucan | HPLC; Megazyme (§5) |
| Stipe firmness (penetrometer), cap thickness, dry matter % | Harvest day (§3) |
| Shelf life at 4 °C | Days to the first score ≥ 2 (§3) |
| Identity | One fruit body per fruiting plot: spore print and photos. At least 3 fruit bodies sent for ITS barcoding, compared with the source kit. |
| Carrot colonisation | Day 60: lift 2 carrots per plot (arms A and C), split them, and score the % of cut face with white mycelium (blinded) |

## 6. Morphology sub-study: why the zebra streaks?

* Within arm A, half of each row's plot area gets an extra **shade and humidity cover**: a 70% shade cloth tunnel with a damp hessian skirt. The other half stays as in the pilot.
* The cover is assigned at random to the left or right half in each row.
* Every cap is photographed from above under the same light. A blinded scorer rates streaking 0–3 (0 = none, 3 = dark radial streaks over more than half the cap).
* **Prediction:** if light or drying causes the streaks (OBS-01, hypotheses 1 and 2), covered halves will score lower.
* **Analysis:** an ordinal mixed model, `streak ~ cover + (1 | row)`. Exploratory.

## 6b. Inoculum lineage sub-study: does carrot select an adapted eringi?

The grower now inoculates carrot beds with a multispore slurry and plans to move to liquid culture (OBS-01, method change 2026-11-19). That makes a second question testable: **does growing eringi on carrot select a genotype that does better on carrot?**

* **Lines.** **G0:** the original kit strain, as liquid culture made from the kit block. **Carrot-selected:** liquid culture from a tissue clone of the best fruit body from the slurry beds (chosen before this trial on colonisation and fruiting only, without tasting, and documented with photos). Both lines are made the same way and used at the same dose.
* **Design.** 6 extra rows, each with one carrot plot per line, inoculated by the same watering-globe method, randomised with the same script. Plot size, carrots and casing as in §3.
* **Hypotheses (exploratory).** The carrot-selected line differs from G0 on (a) carrot colonisation at day 60, (b) blind umami/meaty rating and (c) EUC and ergothioneine.
* **Why not slurry vs liquid culture directly?** Slurry beds are a mix of unknown, changing genotypes, so a difference would have no fixed cause. The comparison that answers "did carrot adapt it?" is selected clone versus starting strain, both as liquid culture.
* **Analysis.** Same models as §7, with `line` in place of `arm`; 6 replicates per line, so only large differences are detectable (0.79 at 1.3× for assays if CV ≈ 15%).

## 7. Analysis plan

* **H1, H3:** `rating ~ arm + serving_position + (1 | panellist)`, with contrasts A − B (primary) and A − commercial (secondary).
* **H2, H4:** `log(EUC) ~ arm + (1 | row)`, contrast A − B. H4 is Holm-adjusted with the other secondary outcomes.
* **H5:** descriptive. If *P. eryngii* is confirmed in arm C, the result is flagged as contaminated.
* Plots lost to animals or digging are reported and dropped. No imputation.

## 8. Safety

Fence the bed: the dog must not dig up the kit material or the casing.

## 9. Registration and deviations

Tag `prereg/P02-v1` and register on OSF before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| 2026-11-19 | Grower switched own carrot beds to spore slurry via watering globes, liquid culture to follow. Added §6b (carrot-selected clone vs G0 kit strain). Main arms keep kit pieces. | Method change in the pilot; recorded before any P02 data |
| 2026-11-19 | Rebuilt around culinary quality and potency, using the grower's "meatier" note as the hypothesis; yield removed | Project priorities, set before any data |
