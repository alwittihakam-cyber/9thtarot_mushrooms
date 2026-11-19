# P05: Reishi on ume vs konara vs cherry: triterpenes and β-glucan (raw wood, through-bark)

| | |
|---|---|
| Status | **Proposed, not adopted.** |
| Season | Inoculate spring 2027; fruiting from summer 2027 and, after burial, summer 2028. Sample the first full-size fruit bodies. |
| Builds on | Reishi on ume is the plan's grade A choice (25 logs), the largest reishi commitment. The ume evidence is **bioactivity** from ume-grown reishi (EV0083: ACE, platelet and IL-8 assays) and a **wild host record** (EV0084). Log-grown reishi had about 1.2× the total triterpenoids of sawdust-grown reishi, with more lucidenic acids, higher antioxidant capacity and equal polysaccharides (EV0144–EV0146). No study compared reishi chemistry between named log woods. |
| Outcomes | Chemical potency. Culinary quality is not relevant to reishi. Yield is not measured; fruiting share is recorded as a gate. |

## 1. Why this trial

Reishi is sold on potency, so the wood that matters is the one that gives the most triterpenes and β-glucan, not the most mass. Kumakura et al. (2008) found ume-grown reishi had the strongest bioactivity of the hosts tested, but the test fungus grew on ume **sawdust** under sterile culture. The project's method is different: raw ume prunings, no sterilisation, through-bark inoculation and burial. This trial asks whether the ume advantage holds in the project's own system, against the project's other two woods.

## 2. Hypotheses

* **Gate.** A wood with a fruit body on fewer than 6 of its 16 logs by the end of the second season drops out of the potency comparison, and that is reported.
* **H1 (primary).** Total triterpenes per g dry weight are higher on ume than on konara. One-sided, because the prior direction is set by EV0083 and EV0144.
* **H2 (primary).** Total triterpenes per g dry weight differ between ume and cherry. Two-sided. H1 and H2 are Holm-adjusted together.
* **Secondary.** (a) β-glucan; (b) ganoderic and lucidenic acid profile (the main 6 to 10 peaks with standards); (c) ACE-inhibitory activity of a hot-water extract, repeating the Kumakura endpoint; (d) fruit-body form (kidney versus antler) and dry matter %. Holm-adjusted as one family.

## 3. Design

| | |
|---|---|
| Strain | One *Ganoderma lingzhi* strain. Record the strain and supplier code. |
| Logs | Short fresh logs 25–40 cm long, drilled through the bark about 10 cm apart, stacked tight under the ULCANS through the first summer, then buried two-thirds deep in a shaded bed the next spring. This is the project's method. |
| Arms | Ume (prunings) · konara · cherry. Diameters matched within ±2 cm across arms, because ume prunings are thin. |
| Size | **8 bed positions × 2 logs per arm × 3 arms = 48 logs.** The fruit bodies from a position's 2 logs of one arm are pooled into one sample, giving **8 independent replicates per arm**. |
| Sampling | Harvest when the white growing margin has gone and the pore surface has been releasing spores for 7–14 days. Brush off spores, slice, dry at 50 °C or freeze-dry, and keep coded. Same week for all arms (`docs/quality-methods.md` §1). The second-year fruit bodies are a separate, labelled sample, never pooled with the first. |
| Indoors | The Martha tent is not used, so all arms share the outdoor bed. |

**Power** (`results/power.md`). With 8 replicates per arm, 0.91 at a 1.3× difference and 1.00 at 1.5× if CV ≈ 15%; 0.40 and 0.72 if CV ≈ 30%. A one-sided H1 adds some power. Triterpene variation between commercial reishi samples is large, so treat a null at CV 30% as "not detected", not "no difference".

## 4. Randomisation and blinding

* `analysis/randomise.py P05 --blocks B1,...,B8 --per-arm 2 --seed <seed>`.
* Logs carry blind-code tags. Bark gives the wood away in the bed, so the harvester is not blind; the lab, the form scorer (from photos) and the analyst see only codes.

## 5. Outcomes

| Outcome | Method |
|---|---|
| Fruiting share (gate) | Logs with ≥ 1 mature fruit body by the end of season 2 / logs in the arm |
| **Total triterpenes (H1, H2)** | Vanillin–perchloric acid colorimetry against ursolic or oleanolic acid, per g dry weight (`docs/quality-methods.md` §5) |
| β-glucan | Megazyme yeast and mushroom β-glucan kit |
| Ganoderic and lucidenic acids | HPLC-UV or LC-MS with standards |
| ACE inhibition | Hot-water extract, IC₅₀; optional, if a lab can run it |
| Form | Photo from above and side, scored blind: kidney, antler, or mixed |
| Dry matter % | Oven 60 °C to constant mass, on a separate slice |

## 6. Analysis

* `log(y) ~ wood + (1 | position)`, contrasts ume − konara (one-sided) and ume − cherry (two-sided), Holm-adjusted.
* Secondary outcomes use the same model, Holm-adjusted as one family.
* Season-2 fruit bodies are analysed separately as a sensitivity check.
* Lost or dead logs are reported, not imputed.

## 7. Registration and deviations

Tag `prereg/P05-v2` before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| 2026-11-19 | v2: dry fruit-body mass replaced by triterpenes as primary, with β-glucan, acid profile and ACE as secondary; fruiting kept only as a gate. File renamed from `P05-reishi-ume-yield.md`. | Project priorities: potency, not yield. Changed before any data. |
