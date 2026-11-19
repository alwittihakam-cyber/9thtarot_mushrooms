# Measuring culinary quality and chemical potency

These are the project's primary outcomes. Every protocol uses the methods below, so results can be compared across trials and published. The project does not measure yield.

## 1. Sampling: compare like with like

Quality changes with flush and maturity as much as with substrate. In shiitake, β-glucan in the second and third flushes fell to 68.5% and 62.3% of the first (Lee et al. 2020). In maitake, β-glucan differed significantly between production lots (Hokkaido FPRI 2021). So:

* **Same flush.** Compare arms only within the same flush, normally the first natural flush.
* **Same stage.** Harvest every arm at the same pre-defined maturity stage, written into each protocol. For eringi: cap margin still inrolled. For shiitake: veil just breaking.
* **Same day and handling.** Harvest all arms on the same day, or within 24 h. Trim to the same standard, and chill to 2–4 °C within 1 h.
* **The unit is the log or plot, not the cap.** Pool 3 or more caps per log or plot into one sample, then split it:
  * **Sensory portion:** cook within 24 h.
  * **Assay portion:** freeze at −20 °C on the day, then freeze-dry. Ship it frozen or dry to the lab, coded.
  * **Texture portion:** measure fresh, on the day of harvest.
* **Record** flush number, harvest date, days from primordium, cap diameter and cap thickness for every sample.

## 2. Blind sensory panel

| | |
|---|---|
| Panel | 12 to 40 tasters (`results/power.md`). Use chefs and regular mushroom buyers where possible. Exclude anyone who knows the allocation. |
| Preparation | Slice 5 mm thick. Pan-sear in a non-stick pan with a fixed weight of neutral oil, at a fixed temperature and time, with no salt. Also make a fixed-ratio dashi (mushroom : water, 80 °C, 30 min) for umami-led species. Use the same cook, pan and recipe for every arm. |
| Coding | 3-digit random codes from `analysis/randomise.py`. Balance serving order across tasters with a Williams design, so that each arm appears equally often in each position. |
| Scales | 0–100 line scales for **umami / savoury-meaty**, **aroma intensity**, **firmness**, **juiciness**, **bitterness / off-flavour** and **overall liking**, plus one free-text comment. |
| Difference test | Where the question is "can anyone tell?", run a triangle test (ISO 4120) before the rating test. |
| Conditions | Same room, same time of day, under red light if colour would give the arm away. Water and plain crackers between samples. |
| Analysis | Mixed model: `rating ~ arm + serving_position + (1 | taster)`. One primary attribute is named in each protocol. The other attributes are Holm-adjusted. |

## 3. Texture and morphology

* **Firmness:** a fruit penetrometer with an 8 mm flat probe, at a fixed point (cap centre and stipe mid-point), giving peak force in N. A university texture analyser running a two-bite TPA is better, if one is available.
* **Cap thickness:** callipers at the cap centre. **Dry matter %:** oven 60 °C to constant mass.
* **Shelf life:** keep a coded sample at 4 °C in a perforated tray. On day 0, 3, 5, 7 and 10, score colour (photo under a grey card), slime and odour on 0–3 scales, and record mass loss %. Shelf life is the number of days to the first score ≥ 2.
* **Morphology:** photograph each sample from above and from the side under the same light, with a scale bar. Score the features named in each protocol, such as the cap streaking seen in OBS-01.

## 4. Umami chemistry (culinary)

Send a commercial or university laboratory freeze-dried samples for:

* **Free amino acids** by HPLC. Report glutamate (Glu) and aspartate (Asp) as the MSG-like group.
* **5′-nucleotides** by HPLC: 5′-GMP, 5′-IMP, 5′-XMP and 5′-AMP.
* **Equivalent umami concentration (EUC)** in g MSG per 100 g dry weight. EUC = Σaᵢbᵢ + 1218 (Σaᵢbᵢ)(Σaⱼbⱼ), where aᵢ is the content of Glu or Asp (relative umami bi = 1 and 0.077), and aⱼ is the content of 5′-nucleotides (bj = 1 for IMP, 2.3 for GMP, 0.61 for XMP, 0.18 for AMP). This is Yamaguchi's synergy equation, widely used for mushrooms.
* **Shiitake only:** lenthionine, the key sulfur aroma of dried and rehydrated shiitake, by GC-MS. Only include it if the trial dries product.

In Japan, labs such as the Japan Food Research Laboratories (日本食品分析センター) and prefectural food research institutes run these assays. Get a quote per sample before freezing the protocol.

## 5. Chemical potency, by species

| Species | Key compounds (primary in **bold**) | Assay |
|---|---|---|
| Reishi | **Total triterpenes**; ganoderic and lucidenic acid profile; β-glucan | Colorimetric total triterpenes (vanillin–perchloric acid); HPLC-UV or LC-MS for individual acids; Megazyme β-glucan kit |
| Cordyceps militaris | **Cordycepin**; adenosine | HPLC-UV, 260 nm |
| Cordyceps chanhua | **N6-(2-hydroxyethyl)-adenosine (HEA)**; adenosine | HPLC |
| Lion's mane | **Hericenones** (fruit body); erinacines (mainly mycelium); β-glucan | LC-MS with standards (specialist lab) |
| Turkey tail | **β-glucan / protein-bound polysaccharide** (the PSK/PSP fraction is an extract, not a whole-mushroom assay) | Megazyme β-glucan; hot-water extract yield |
| Shiitake | **β-glucan (lentinan)**; eritadenine; ergothioneine | Megazyme; HPLC |
| Maitake | **β-glucan** | Megazyme (Congo red as a cheap screen; Hokkaido FPRI 2021) |
| Oyster group (hiratake, Italian, golden, eringi) | **Ergothioneine**; β-glucan | HPLC; Megazyme |
| Kikurage | **Polysaccharides**; texture (rehydration ratio for dried product) | Phenol–sulfuric total sugars; rehydration ratio |
| Nameko, mukitake, kuritake, buna-shimeji, enoki, chestnut mushroom | Ergothioneine; β-glucan (culinary endpoints come first for these) | HPLC; Megazyme |

Report every compound per gram of **dry** weight, and give the dry-matter % alongside, so that a wetter mushroom does not look less potent.

## 6. What the literature already shows (and does not)

Studies that change only the substrate and measure quality are rare. Here is what was found, with grades in `data/evidence.csv`:

* **Log versus sawdust bed, wood not named.**
  * Maitake: logs gave more umami/sweet amino acids and more 5′-GMP (E2).
  * Nameko: log-grown soup was preferred on taste and aroma (E2).
  * Shiitake: sawdust gave more free amino acids, including bitter ones, while logs gave slightly more 5′-GMP. The evidence is mixed (E2).
  * Reishi: logs gave more total triterpenes and lucidenic acids, with equal polysaccharides (E2, commercial samples).
* **Substrate species.**
  * Eringi grown on willow sawdust scored best for taste and texture against birch and corncob (E2).
  * Reishi from ume trees had the strongest bioactivity (E2).
  * Cordyceps militaris on beetle larvae had about 34× the cordycepin of silkworm pupae, but silkworm gave the best-formed fruit bodies (E1).
* **Not found.** No study compared culinary quality or potency **between named log woods** for any of the project's species. Every cell for the project's woods except two is empty (`results/gaps.md`). That gap is why protocols P01–P06 exist.
