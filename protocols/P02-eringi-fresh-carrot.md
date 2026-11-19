# P02: Eringi on fresh, unsterilised buried carrot (replicating OBS-01)

| | |
|---|---|
| Status | **Proposed, not adopted.** Needs Hakam's yes before it is frozen. |
| Season | Inoculate in spring 2027 (Mar to Apr), follow to Dec 2027; a second cohort can follow in autumn 2027 |
| Evidence it builds on | EV0121 (project pilot: fruited 2026-11-11, one bed, no controls); EV0116 (P. eryngii is a weak parasite of Apiaceae roots, host record); EV0131 (extrapolation: carrot is Apiaceae) |

## 1. Why this trial

The project's eringi bed fruited from fresh carrots that had been pulled, inoculated with pieces of a kit block, and buried again. As far as the project knows, published work has only used dried, sterilised carrot as an additive. The pilot had one bed and no controls, so two simpler explanations are still open:

1. **The kit pieces fruited on their own.** A kit block buried under a humid casing can fruit with no carrot at all.
2. **The fruit is not from the kit strain.** The pins have not been identified beyond their look.

This trial separates those explanations from a real carrot effect.

## 2. Hypotheses

* **H1 (primary).** Plots with kit pieces plus fresh carrot give more fresh eringi per plot than plots with the same mass of kit pieces and no carrot.
* **H2.** Carrot-only plots, with no inoculum, give no *P. eryngii*. This is the identity control.
* **Exploratory.** In the carrot plus kit arm, carrot tissue is colonised at day 60, and colonised share predicts yield.

## 3. Design

| | |
|---|---|
| Arms | **A** carrot + kit · **B** kit only (same kit mass, same depth) · **C** carrot only (no inoculum) |
| Plot | 50 × 50 cm, 10 fresh carrots (record total fresh mass), buried 5 cm, cased with the pilot's straw + leaf-litter mix at a fixed depth (5 cm) |
| Blocks | Bed rows, perpendicular to the main slope or shade gradient. Each row holds one plot of each arm. |
| Size | **12 rows × 3 arms = 36 plots.** Power for H1 is 0.78 at a 2× effect and 0.38 at 1.5× (`results/power.md`, SD 0.6 on the log scale assumed). |
| Inoculum | One kit block, or blocks from one lot, crumbled and split by weight: 30 g per plot in arms A and B |

## 4. Randomisation and blinding

* Assign arms within each row with `analysis/randomise.py P02 --blocks R01,...,R12 --per-arm 1 --seed <seed>`.
* Plots carry blind code stakes only. Once the casing is down, the arms look the same.
* The person who weighs the harvest reads only codes.
* The identity check (§6) is done on coded samples.

## 5. Outcomes

| Outcome | Definition |
|---|---|
| **Primary: fresh yield per plot** | Sum of trimmed fresh mass (g) of all *P. eryngii* harvested from the plot to 2027-12-31 |
| Fruiting plots | Share of plots with at least one fruit body ≥ 3 cm tall |
| Carrot colonisation | At day 60, lift 2 carrots per plot in arms A and C, split them lengthwise, photograph, and score % of the cut face with white mycelium (blinded). Do not return them. |
| Biological efficiency | Fresh yield ÷ (carrot dry mass + kit dry mass) × 100. Dry masses come from oven-dried subsamples. |
| Identity | One fruit body per fruiting plot: spore print and morphology. Send at least 3 fruit bodies (one per arm if any) for ITS barcoding, then compare with a sample from the source kit. |

## 6. Analysis plan

* **H1.** Log(yield + 1) ~ arm + (1 | row), comparing A with B. Report the yield ratio with its 95% CI. As a sensitivity check, run a Wilcoxon signed-rank test on the row-paired differences, because yields may include zeros.
* **H2.** Descriptive. Any confirmed *P. eryngii* in arm C points to contamination or wild inoculum, which invalidates the A versus C contrast. Report it either way.
* Plots lost to animals or digging are reported and dropped. No imputation.

## 7. Notes

* Disturbing the soil can expose the dog to buried kit material. Fence the trial bed.
* An optional later trial would add arm **D**: dried, sterilised carrot, the published practice. A versus D would test whether "fresh and unsterilised" is itself the improvement.

## 8. Registration and deviations

Tag `prereg/P02-v1` and register on OSF before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| | | |
