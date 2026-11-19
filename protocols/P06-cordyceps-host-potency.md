# P06: Cordyceps militaris on wild moth pupae vs silkworm vs beetle larvae: cordycepin and fruit-body form

| | |
|---|---|
| Status | **Proposed, not adopted.** |
| Season | Collect or rear hosts in summer and autumn 2027; inoculate as hosts pupate; harvest 50–70 days later. A second batch can follow in spring 2028. |
| Builds on | In the one replicated host comparison, beetle larvae (*Allomyrina dichotoma*, カブトムシ) gave the most cordycepin of 6 insects, about 34× silkworm pupae, while silkworm gave the best-formed fruit bodies (EV0112, EV0113, EV0147, EV0148; TURK-2022, n = 3 per host). Nobody has measured cordycepin from native Japanese moth pupae. The project's plan is to grow on **wild moth pupae first**, raised on site from eggs laid at the ULCANS LEDs, with silkworm as a backup. |
| Outcomes | Chemical potency (cordycepin, adenosine) and fruit-body form. Yield is not measured. |

## 1. Why this trial

The project wants Cordyceps on local moths, and the only evidence says the host can change cordycepin more than thirtyfold, and that the best-looking host is not the most potent one. That is a trade-off the business needs to see in its own hosts. This trial also repeats the beetle result, which comes from a single study with 3 replicates and is far above other published cordycepin values. A finding that large needs replicating before anyone relies on it.

## 2. Hypotheses

* **H1 (primary).** Cordycepin per g dry weight of fruit body differs between wild moth pupae and silkworm pupae.
* **H2 (primary, replication).** Cordycepin per g dry weight is higher on beetle larvae than on silkworm pupae. One-sided, the direction set by TURK-2022. H1 and H2 are Holm-adjusted together.
* **H3 (secondary, form).** Fruit-body count and length per host differ between hosts, with silkworm expected highest.
* **Secondary.** Adenosine; cordycepin in the whole host with fruit bodies (sclerotium + stroma), which is how TURK-2022 reported it; the share of hosts that produce fruit bodies; contamination. Holm-adjusted as one family.
* **Reference arm.** Brown rice medium, the usual commercial substrate, run alongside as a benchmark. It is described, not tested.

## 3. Design

| | |
|---|---|
| Strain | One *C. militaris* strain, confirmed fertile (it must fruit on rice in a pre-test). Record its supplier and code, and subculture no more than 3 times from the master, because strains lose fruiting with repeated subculture. |
| Arms | **Wild moth:** pupae of **one** native moth species reared on site, named before randomisation, with a voucher specimen kept. A native silk moth such as 天蚕 (*Antheraea yamamai*) is a candidate. · **Silkworm** pupae (*Bombyx mori*), bought fresh. · **Beetle** larvae (*A. dichotoma*), captive-bred, never wild-caught. · **Brown rice** reference. |
| Unit | One sterilised culture container. Insect arms hold a fixed **host fresh mass** per container (about 15 g: several pupae, or one beetle larva), recorded per container. Rice: fixed dry rice + nutrient broth, as the supplier specifies. |
| Size | **8 containers per arm × 4 arms = 32 containers**, in 2 inoculation batches of 4 containers per arm. |
| Host preparation | Hosts are killed by freezing at −20 °C for 48 h, surface-sterilised, and injected with a fixed volume of liquid culture, the same lot for every arm. The method is the same for every insect arm. |
| Culture | Indoors, not in the Martha tent (reishi only): 20 ± 2 °C in the dark until the hosts are fully colonised, then 18–22 °C, about 85% RH, and 12 h light. All containers on one rack, positions randomised. |
| Sampling | Harvest when the tallest stroma stops lengthening and before the tips turn soft (about day 50–70). Stroma (fruit bodies) and host are separated, weighed, freeze-dried and coded separately. |

**Power** (`results/power.md`). 8 containers per arm give 0.91 at a 1.3× difference and 1.00 at 1.5× if CV ≈ 15%; 0.40 and 0.72 if CV ≈ 30%. Cordycepin varies a lot between cultures, so assume the lower figures. The published beetle effect (about 34×) is detectable at any plausible CV. A wild-moth difference smaller than about 1.5× would be missed.

## 4. Randomisation and blinding

* `analysis/randomise.py P06 --blocks B1,B2 --per-arm 4 --seed <seed>`.
* Hosts look different, so the person inoculating cannot be blind. The form scorer (from photos with the host cropped out), the lab and the analyst see only codes.

## 5. Outcomes

| Outcome | Method |
|---|---|
| **Cordycepin (H1, H2)** | HPLC-UV at 260 nm against a cordycepin standard, mg per g dry weight of fruit body (`docs/quality-methods.md` §5) |
| Adenosine | Same run |
| Cordycepin in the whole host + fruit bodies | Same method, on a separate freeze-dried portion, to compare with TURK-2022 |
| **Fruit-body form (H3)** | Stroma count and length (mm) per container, from photos with a scale bar, scored blind |
| Share fruiting | Hosts with ≥ 1 stroma ≥ 10 mm / hosts inoculated |
| Contamination | Containers with visible competitor moulds by day 30, recorded and excluded from chemistry |
| Dry matter % | Freeze-dried mass ÷ fresh mass |

## 6. Analysis

* `log(cordycepin) ~ host + (1 | batch)`, contrasts wild moth − silkworm (two-sided) and beetle − silkworm (one-sided), Holm-adjusted.
* Form and the secondary family use the same model, Holm-adjusted together.
* Brown rice is reported beside the insect arms with 95% CIs.
* The result is presented as a **form–potency trade-off plot** for each host: median stroma length against cordycepin, with replicate points shown.

## 7. Ethics and safety

* Beetle larvae are captive-bred only. Wild moth pupae come from the project's own reared stock, so the trial takes nothing from the wild population. Hosts are frozen before inoculation.
* Keep culture containers and spent hosts out of the dog's reach and dispose of them sealed.
* Fruit bodies from this trial are not sold. They exist for assay.

## 8. Registration and deviations

Tag `prereg/P06-v1` and register on OSF before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| | | |
