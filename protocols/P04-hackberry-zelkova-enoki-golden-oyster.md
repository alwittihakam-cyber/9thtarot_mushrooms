# P04: Enoki and golden oyster on hackberry and zelkova vs cherry: taste, texture and ergothioneine

| | |
|---|---|
| Status | **Proposed, not adopted.** It extends proposal 5 from the Kaname River tree ranking. |
| Season | Fell in winter 2026–27, inoculate in spring 2027. Golden oyster: first summer flush (Jun to Sep 2027). Enoki: first cold-season flush (Nov 2027 to Mar 2028). |
| Builds on | Enoki on cherry and golden oyster on cherry both have **no evidence** for any outcome (`results/plan_audit.md`). Hackberry is a recorded wild enoki host (EV0118). Elm is rated best for golden oyster (EV0022), and zelkova is in the elm family (EV0124). Hackberry is now Cannabaceae, so it is a weaker analogue for golden oyster (EV0125). No study measured either species' quality by wood. |
| Outcomes | Culinary quality and ergothioneine. Yield is not measured. Fruiting share is recorded as a gate. |

## 1. Why this trial

Two of the plan's wood choices rest on nothing at all. The project already has hackberry (エノキ), the tree enoki is named after, and zelkova grows nearby. Wild-type enoki from logs is a different product from the white bottle-grown kind: a brown, glossy cap, a short dark stem and much more flavour. Golden oyster is sold on aroma and colour and is fragile after harvest. So the question for each wood is whether it gives a better mushroom to eat, not a heavier one.

## 2. Hypotheses

Each species is a separate trial with its own family of tests.

* **Gate.** A wood with fruit on fewer than 4 of its 8 logs in the first season drops out of that species' quality comparison, and that is reported.
* **Enoki, H1 (primary).** Blind-rated *umami / savoury* intensity differs between hackberry and cherry.
* **Golden oyster, H2 (primary).** Blind-rated *overall liking* differs between zelkova and cherry, and between hackberry and cherry. Two Holm-adjusted contrasts.
* **Both species, H3 (co-primary, potency).** Ergothioneine per g dry weight differs between each test wood and cherry.
* **Secondary.** EUC (Glu, Asp, 5′-nucleotides); β-glucan; firmness; for enoki, stem length and cap colour; for golden oyster, cap colour retention and shelf life at 4 °C. Holm-adjusted as one family per species.

## 3. Design

| | |
|---|---|
| Arms | 2 species × 3 woods: hackberry, zelkova and cherry. Zelkova only from branches or windfall, because large ケヤキ are often protected. |
| Size | **8 logs per wood per species = 48 short logs.** Each log is one replicate (pool ≥ 3 caps). If a log gives fewer than 3 caps, pool it with its block partner of the same arm and halve the replicate count for that block. |
| Enoki method | The project's buried short-log method: 30 cm logs buried in the ULCANS leaf-litter bed. Fruiting in the cold season. |
| Golden oyster method | 30 cm short logs at the downwind end of the tent, as in the plan. Fruiting Jun to Sep. |
| Blocks | 4 bed positions (enoki) and 4 stack positions (golden oyster), each holding 2 logs of each wood. |
| Sampling | Enoki: harvest when the cap is 2–4 cm and still convex. Golden oyster: harvest before the cap margin flattens and before spore drop. Same day for all arms, chilled within 1 h (`docs/quality-methods.md` §1). |
| Panel | 24 panellists per species, pan-seared with no salt, Williams-balanced order. Enoki also as a fixed-ratio dashi, because its umami shows best in broth. |

**Power** (`results/power.md`). Panel: 0.74 at a 10-point difference and 0.97 at 15 (SD 18). Ergothioneine: 8 replicates per arm give 0.91 at 1.3× and 1.00 at 1.5× if CV ≈ 15%; 0.40 and 0.72 if CV ≈ 30%.

## 4. Randomisation and blinding

* `analysis/randomise.py P04 --blocks E1,E2,E3,E4 --per-arm 2 --seed <seed>` for enoki, and again with blocks G1–G4 and a second seed for golden oyster.
* Bark differs, so the harvester is not blind. The cook, panel, texture operator and lab see only codes. Golden oyster colour may differ by wood, so its panel tastes under red light; cap colour is scored separately from photos.

## 5. Outcomes

| Outcome | Method |
|---|---|
| Fruiting share (gate) | Logs with ≥ 1 harvestable flush in the first season / logs in the arm |
| **Umami / savoury (enoki H1)**, **overall liking (golden oyster H2)** | 0–100 line scales, with aroma, firmness, juiciness, bitterness and the other attribute (`docs/quality-methods.md` §2) |
| **Ergothioneine (H3)** | HPLC, per g dry weight, with dry matter % (§5) |
| EUC | HPLC free amino acids and 5′-nucleotides, Yamaguchi equation (§4) |
| β-glucan | Megazyme kit (§5) |
| Firmness | Penetrometer, cap centre and stipe mid-point (§3) |
| Enoki stem length, cap colour | Callipers; photo under a grey card, scored blind |
| Shelf life | Days at 4 °C to the first score ≥ 2 (§3); golden oyster colour fading is scored as part of it |

## 6. Analysis

* Panel outcomes: `rating ~ wood + serving_position + (1 | panellist)`, per species.
* Chemistry and texture: `log(y) ~ wood + (1 | block)`, per species.
* Contrasts are each test wood minus cherry, Holm-adjusted within each species and outcome family.
* Golden oyster is native to Japan, so the trial raises no invasion concern in Kanagawa. Its documented effect on wood-fungus diversity in the US was where it was introduced (Veerabahu et al. 2025).

## 7. Registration and deviations

Tag `prereg/P04-v2` before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| 2026-11-19 | v2: yield per kg log replaced by blind panel and ergothioneine; fruiting kept only as a gate | Project priorities: quality and potency, not yield. Changed before any data. |
