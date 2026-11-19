# P05: Reishi yield on ume vs konara vs cherry (raw wood, through-bark)

| | |
|---|---|
| Status | **Proposed, not adopted.** |
| Evidence it builds on | Reishi on ume is the plan's grade A choice with 25 logs, the largest single reishi commitment. The only ume evidence is **bioactivity** (EV0083) and a **wild host record** (EV0084). No yield on ume has been found (`results/plan_audit.md`: "hypothesis only"). |

## 1. Why this trial

Kumakura et al. (2008) showed that reishi from ume trees had the strongest bioactivity of the hosts they tested. They did not measure yield. Ume prunings are free and on hand, and that may well be reason enough to use them, but how much ume yields compared with other woods is unknown. This trial measures it and keeps the project's own method: raw wood, no sterilisation, and no cut-face inoculation.

## 2. Hypotheses

* **H1.** Dry fruit-body mass per litre of log differs between ume and konara.
* **H2.** Dry fruit-body mass per litre of log differs between ume and cherry. The two contrasts are Holm-adjusted.
* **Exploratory, if a lab can be found.** Total triterpene content per gram of dry fruit body differs by wood. This would link yield to the Kumakura bioactivity result.

## 3. Design

| | |
|---|---|
| Strain | One *Ganoderma lingzhi* strain. Confirm the strain and record its supplier code. |
| Logs | Short fresh logs 25 to 40 cm long, drilled through the bark about 10 cm apart, stacked tight under the ULCANS through the first summer, then buried two-thirds deep in a shaded bed the next spring. This is the project's method. |
| Arms | Ume (prunings) · konara · cherry. Diameters are matched within ±2 cm across arms, because ume prunings are thin. |
| Size | **15 logs per arm = 45 logs.** Power is 0.87 at a 2× difference and 0.44 at 1.5× (`results/power.md`). |
| Blocks | 5 positions in the burial bed, each holding 3 logs per arm, randomised with `analysis/randomise.py P05`. |

## 4. Outcomes and analysis

* **Primary.** Oven-dry (60 °C) fruit-body mass over two seasons, in g per litre of log. Analyse log(yield + 1) with wood as a fixed effect and bed position as a random effect, using the two contrasts above.
* **Secondary.** Days to first primordium; the share of logs that fruit; antler versus kidney form (the Martha tent is not used in this trial).
* **Blinding.** The fruit bodies are weighed against blind codes by someone who did not bury the logs.

## 5. Registration and deviations

Tag `prereg/P05-v1` before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| | | |
