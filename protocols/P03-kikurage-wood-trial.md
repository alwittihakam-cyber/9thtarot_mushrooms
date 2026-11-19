# P03: Kikurage on sugi and Japanese cinnamon: texture and polysaccharides vs the akamegashiwa benchmark

| | |
|---|---|
| Status | **Proposed, not adopted.** This is proposal 4 from the Kaname River tree ranking, still awaiting the grower's yes. |
| Season | Fell in winter 2026–27, inoculate in Apr 2027, sample the first summer flush (Jun to Sep 2027). Repeat on the first 2028 flush if the 2027 panel is short. |
| Builds on | Fruiting on named woods: akamegashiwa fruited well in two of three Saga batches (EV0045, EV0050, EV0058); Machilus fruited moderately (EV0046, EV0052); hinoki gave nothing (EV0066); konara ranked last (EV0071) and kunugi was poor or nil in every Saga batch (EV0048, EV0055, EV0060, EV0063). Sugi and ヤブニッケイ have no trial (EV0129, EV0130). Bamboo sawdust raised kikurage polysaccharide and minerals (EV0150), so substrate can move kikurage chemistry. |
| Outcomes | Texture (the quality kikurage is bought for) and polysaccharides. Yield is not measured. Whether a log fruits at all is recorded, because a wood that does not fruit has no quality to compare. |

## 1. Why this trial

Kikurage is bought for its bite: the crunchy, springy "kori-kori" texture, fresh and after drying and rehydrating. Its taste is mild. So the useful question about a new wood is not "how much?" but "does it fruit, and is the texture as good?" Sugi and Japanese cinnamon are both easy for the project to get. No published trial covers either wood, for any outcome.

## 2. Hypotheses

* **Gate (fruiting).** Each wood is scored for the share of logs that fruit in the first season. A wood with fruit on fewer than 4 of its 12 logs drops out of the quality comparison, and that is reported as the result for that wood.
* **H1 (primary, texture).** Blind-rated *firmness / crunch* of kikurage from sugi differs from kikurage from akamegashiwa. **H1b:** the same for ヤブニッケイ. Two Holm-adjusted contrasts.
* **H2 (co-primary, texture, instrumental).** Rehydration ratio of dried kikurage, and the TPA hardness and springiness of rehydrated kikurage, differ between each test wood and akamegashiwa.
* **H3 (secondary, potency).** Total polysaccharides (phenol–sulfuric acid) per g dry weight differ between each test wood and akamegashiwa.
* **Calibration arm.** Konara, the plan's current wood and the poorest in the literature. If konara matches akamegashiwa here, site conditions are dominating and the result says so.

## 3. Design

| | |
|---|---|
| Strain | **One named strain of one species.** Record whether it is *Auricularia cornea* (アラゲキクラゲ, the species in every Japanese wood trial cited) or *A. heimuer* (キクラゲ). Results may not transfer between them. |
| Arms | Akamegashiwa (benchmark) · sugi · ヤブニッケイ · konara (calibration) |
| Identity check | Confirm the "cinnamon" trees are ヤブニッケイ (*Cinnamomum yabunikkei*), not camphor (クスノキ). Keep a pressed leaf from each source tree. |
| Size | **6 rows × 2 logs per arm × 4 arms = 48 logs.** Each row's 2 logs of one arm are pooled into one sample, giving **6 independent replicates per arm**. Logs come from at least 3 source trees per wood. |
| Logs | 90 cm long, 8–15 cm diameter, fresh bark. Sawdust spawn at Saga's rate of 4 × diameter (cm) holes. |
| Sampling | First flush that gives ≥ 3 ears on a log. Harvest at full expansion before the margin dries and curls (`docs/quality-methods.md` §1). Split each pooled sample: fresh portion for the panel, a fixed mass dried at 50 °C for rehydration and TPA, and a freeze-dried portion for the lab. |
| Panel | 24 panellists. Each tastes akamegashiwa against one test wood per session, blanched 2 min in unsalted water. Serving order follows a Williams design. |

**Power** (`results/power.md`). H1: 24 panellists give 0.74 for a 10-point difference and 0.97 for 15 points, assuming SD 18. H2 and H3: 6 replicates per arm give 0.79 at 1.3× and 0.99 at 1.5× if CV ≈ 15%, but only 0.28 and 0.57 if CV ≈ 30%. This trial can therefore find large chemistry differences only. Say so when reporting a null.

## 4. Randomisation and blinding

* `analysis/randomise.py P03 --blocks R01,...,R06 --per-arm 2 --seed <seed>`.
* Bark gives the wood away in the yard, so the harvester is not blind. Everything after harvest is: samples are bagged under blind codes, and the cook, panel, texture operator and lab see only codes.
* Colour may differ between woods, so the panel tastes under red light.

## 5. Outcomes

| Outcome | Method |
|---|---|
| Fruiting share (gate) | Logs with ≥ 1 harvestable ear by 30 Sep 2027 / logs in the arm |
| **Firmness / crunch (H1)** | 0–100 line scale, blanched, plus chewiness, juiciness, off-flavour and overall liking (`docs/quality-methods.md` §2) |
| **Rehydration ratio (H2)** | Dried mass × 100 g of water, 30 min at 20 °C, drained 5 min: rehydrated mass ÷ dry mass |
| **TPA hardness and springiness (H2)** | Rehydrated pieces, two-bite TPA where a texture analyser is available; otherwise a penetrometer with an 8 mm probe (§3) |
| Total polysaccharides (H3) | Phenol–sulfuric acid, per g dry weight, with dry matter % reported (§5) |
| Ear thickness, dry matter % | Callipers at the ear centre; oven 60 °C to constant mass |
| Shelf life of fresh ears | Days at 4 °C to the first score ≥ 2 (§3) |

## 6. Analysis

* **H1:** `rating ~ wood + serving_position + (1 | panellist)`, contrasts sugi − akamegashiwa and ヤブニッケイ − akamegashiwa, Holm-adjusted.
* **H2, H3:** `log(y) ~ wood + (1 | row)`, the same two contrasts, Holm-adjusted within each outcome. Konara − akamegashiwa is reported as the calibration contrast, not tested.
* Fruiting share: reported per wood with exact 95% CIs. No test.
* Logs that die or are lost are reported and not imputed.

## 7. Safety

* Elder (ニワトコ) is excluded because it is toxic to dogs.
* Konara comes only from trees free of oak wilt.

## 8. Registration and deviations

Tag `prereg/P03-v2` before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| 2026-11-19 | v2: yield per m³ replaced by texture and polysaccharides; fruiting kept only as a gate | Project priorities: quality and potency, not yield. Changed before any data. |
