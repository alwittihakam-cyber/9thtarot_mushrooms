# P03: Kikurage on sugi and Japanese cinnamon vs the akamegashiwa benchmark

| | |
|---|---|
| Status | **Proposed, not adopted.** This is proposal 4 from the Kaname River tree ranking, still awaiting Hakam's yes. |
| Season | Fell in winter 2026–27, inoculate in Apr 2027, harvest Jun to Sep 2027 and 2028 |
| Evidence it builds on | Akamegashiwa 32.3 to 37.8 kg/m³ in two Saga batches (EV0045, EV0050) but 4.1 in a third (EV0058); Machilus 5.1 to 14.3 (EV0046, EV0052); hinoki 0 (EV0066); konara poor (EV0071) and kunugi poor or nil in every Saga batch (EV0048, EV0055, EV0060, EV0063). Sugi and ヤブニッケイ have no trial (EV0129, EV0130). |

## 1. Why this trial

The plan grows kikurage on konara and cherry. On the published data, oaks are among the worst kikurage woods, and akamegashiwa, dogwood (ミズキ) and sweetgum are among the best. The project has easy access to sugi and Japanese cinnamon. No trial covers either, and the one conifer tested, hinoki, gave nothing. This trial finds out whether either wood is worth growing on.

## 2. Hypotheses

* **H1a.** Yield per m³ on sugi differs from yield on akamegashiwa. The prior expectation is lower.
* **H1b.** Yield per m³ on ヤブニッケイ differs from yield on akamegashiwa. The prior expectation is lower, with Machilus suggesting about a third.
* **Calibration arm.** Konara is included as a negative control. If konara does as well as akamegashiwa at this site, then site conditions, not wood, are driving yield, and the result must say so.

## 3. Design

| | |
|---|---|
| Strain | **One named strain of one species.** Record whether it is *Auricularia cornea* (アラゲキクラゲ, the species in every Japanese wood trial cited) or *A. heimuer* (キクラゲ). Results may not transfer between the two. |
| Arms | Akamegashiwa (benchmark) · sugi · ヤブニッケイ · konara (negative control) |
| Identity check | Confirm the "cinnamon" trees are ヤブニッケイ (*Cinnamomum yabunikkei*), not camphor (クスノキ). Keep a herbarium leaf for each source tree. |
| Size | **15 logs per arm** for the three main woods, from at least 3 source trees each, plus 8 konara logs. That is 53 logs. Power is 0.86 to detect a 2.5× difference and 0.27 at 1.5× (`results/power.md`, SD 0.8 on the log scale assumed from Saga's spread). |
| Blocks | Laying-yard position: 5 rows, each holding 3 logs of each main wood and 1 to 2 konara logs, allocated at random within the row |
| Logs | 90 cm long, 8 to 15 cm diameter, fresh bark. Inoculate with sawdust spawn at Saga's rate of 4× the diameter in holes. |

## 4. Outcomes and analysis

* **Primary.** Cumulative fresh yield over two seasons, in kg per m³ of log. Analyse log(yield + 0.1) with wood as a fixed effect and row as a random effect. Make two Holm-adjusted contrasts: sugi versus benchmark and ヤブニッケイ versus benchmark. Report the ratios with 95% CIs.
* **Secondary.** Days to first harvest; the share of logs that fruit; yield by year, because Saga's yields collapsed after year 1.
* **Blinding.** Harvests are weighed against blind codes. Bark type gives the wood away, so the person weighing cannot be fully blinded, which is a stated limitation.

## 5. Safety

* Elder (ニワトコ) is excluded because it is toxic to dogs.
* Konara comes only from trees that are not affected by oak wilt.

## 6. Registration and deviations

Tag `prereg/P03-v1` before inoculation.

| Date | Deviation | Reason |
|---|---|---|
| | | |
