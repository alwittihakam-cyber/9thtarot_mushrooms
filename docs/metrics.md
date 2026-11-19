# Metrics and how to measure them

All protocols use these definitions, so results can be compared across trials and with the literature.

## Log volume (Smalian's formula), a covariate

V = L × (A₁ + A₂) / 2, where Aᵢ = π (dᵢ / 2)²

* Measure the two end diameters *under the bark* (d₁, d₂) and the length L, in cm.
* V is in cm³. Divide by 1,000 for litres, or by 10⁶ for m³.
* Record the raw measurements in `logs.csv`, not just V.

## Log moisture, a covariate

Dry mass = fresh mass × (1 − MC), where MC is the moisture content on a wet basis.

* For MC, drill one 8 mm core at the log's mid-length on the day of inoculation, weigh it fresh, oven-dry it at 103 °C to constant mass, and weigh it again.
* A pin moisture meter is acceptable if it has been calibrated against cores for that wood.

## Quality and potency

The primary outcomes, and how to sample and measure them, are in [`quality-methods.md`](quality-methods.md): same-flush, same-stage sampling, the blind panel, texture and shelf life, umami chemistry (EUC) and the per-species potency assays.

## Fruiting share (a gate, not an outcome)

The share of logs or plots with at least one harvestable fruit body by a date fixed in each protocol. It answers "does this wood work at all?". The project does not weigh harvests as an outcome, and protocols do not compare yield.

## Days to colonisation (P01)

Each month, photograph both cut ends of every log under the same light, with a grey card and the blind-code tag in frame. A scorer who does not know the arm scores each end against this chart:

| Score | Cross-section showing colonisation (white mycelium or a clear advancing front) |
|---|---|
| 0 | none visible |
| 25 | up to a quarter |
| 50 | about half |
| 75 | most |
| 100 | the whole face |

**Days to colonisation** is the number of days to the first visit where *both* ends score ≥ 50.

Before the trial, the scorer re-scores a random 10% of the images at least a week later. Agreement is checked with a quadratic-weighted κ, and the target is ≥ 0.7.

## Contamination

Record each competitor that shows fruit bodies, stroma or a coloured zone on the bark or ends, such as *Trichoderma*, *Hypoxylon*, *Diatrype*, *Trametes* or *Schizophyllum*. Give the estimated % of bark surface it covers. Photograph anything that cannot be identified.

## Harvest record

For every harvest, record in `harvests.csv`: date, flush number, maturity stage, days from primordium, the number of caps pooled, cap diameter and cap thickness, and whether the sample was chilled within 1 h. Masses are recorded only where a method needs them (sample portions in `samples.csv`, dry matter % for assays).

## Environment

Log air temperature, relative humidity and soil temperature at each laying site every 30 minutes with a cheap logger. Rain comes from the nearest JMA AMeDAS station, which is Ebina or Odawara for this area. Record which station was used.
