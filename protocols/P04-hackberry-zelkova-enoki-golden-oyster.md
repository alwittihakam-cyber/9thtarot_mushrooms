# P04: Enoki and golden oyster on hackberry and zelkova vs cherry

| | |
|---|---|
| Status | **Proposed, not adopted.** It extends proposal 5 from the Kaname River tree ranking. |
| Evidence it builds on | Enoki on cherry (plan B) and golden oyster on cherry (plan B) both have **no evidence** (`results/plan_audit.md`). Hackberry is a recorded wild enoki host (EV0118). Elm is rated best for golden oyster (EV0022). Zelkova is in the elm family (EV0124). Hackberry is now Cannabaceae, so it is a weaker analogue (EV0125). |

## 1. Why this trial

Two of the plan's current wood choices rest on nothing at all. Meanwhile, the project already has hackberry (エノキ), the tree that enoki is named after, and zelkova grows nearby. This trial puts all three woods side by side for both species.

## 2. Hypotheses

* **Enoki, H1.** Yield per kg of log differs between hackberry and cherry.
* **Golden oyster, H2.** Yield per kg of log differs between zelkova and cherry, and between hackberry and cherry. These are two Holm-adjusted contrasts.

## 3. Design

| | |
|---|---|
| Arms | 2 species × 3 woods: hackberry, zelkova and cherry. Zelkova comes only from branches or windfall, because large ケヤキ are often protected. |
| Size | **10 logs per wood per species = 60 logs.** Power is 0.70 at a 2× difference (`results/power.md`). This size screens for large differences only. |
| Enoki method | The project's buried short-log method for long stems: 30 cm logs buried in the ULCANS leaf-litter bed. Fruiting happens in the cold season (Nov to Mar). |
| Golden oyster method | 30 cm short logs at the downwind end of the tent, as the plan already sets out. Fruiting happens Jun to Sep. |
| Blocks | Bed position for enoki and stack position for golden oyster, randomised with `analysis/randomise.py P04`. |

## 4. Outcomes and analysis

* **Primary.** Fresh yield over two fruiting seasons, in g per kg of log fresh mass at inoculation. Analyse log(yield + 1) with wood as a fixed effect and block as a random effect, separately for each species.
* **Secondary.** Days to first fruiting; the share of logs fruiting; for enoki, stem length, the premium trait.
* Golden oyster is native to Japan, so it carries no invasion concern in Kanagawa. Its documented effect on wood-fungus diversity in the US was in a region where it was introduced (Veerabahu et al. 2025).

## 5. Registration and deviations

Tag `prereg/P04-v1` before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| | | |
