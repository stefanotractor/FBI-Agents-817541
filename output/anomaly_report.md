# Anomaly Report

## Executive Summary
The user requested an analysis to identify routes with unusually high anomaly counts during February. The scope covered two datasets—*allarmi_raw* and *tipologia_raw*—both filtered to February departures and grouped by route (origin and arrival airports).
Across 9 analyzed groups, 3 presented high risk, 2 moderate risk, and 4 lower-priority deviations.

## Risk Distribution
Of the 9 flagged groups, 3 present high risk, 2 moderate risk, and 4 lower-priority deviations.

## Detailed Findings
### High Risk
#### Tirana (TIA) → Verona (VRN)
- **Events**: 6966 (baseline mean: 78.3)
- **Z-score**: 13.22
- **Ratio to baseline**: 89.00x
- **Anomaly score**: 2.00
- **Risk score**: 100.00
- **Detection consensus**: flagged by 2 of 3 methods (Isolation Forest, Z-score)
- **Risk reason**: Flagged by 2 of 3 methods (Isolation Forest, Z-score) with a z-score of 13.2; deviation of 89.0x from baseline volume.

Analytical commentary: This route shows a pronounced deviation from expected behavior. The event volume significantly exceeds the population average, indicating a potential operational or security concern requiring immediate attention. The strong consensus among detection methods reinforces the reliability of this finding.
#### London City (LCY) → Firenze Peretola (FLR)
- **Events**: 100605 (baseline mean: 3726.1)
- **Z-score**: 13.19
- **Ratio to baseline**: 27.00x
- **Anomaly score**: 1.97
- **Risk score**: 97.51
- **Detection consensus**: flagged by all 3 methods (Isolation Forest, Local Outlier Factor, Z-score)
- **Risk reason**: Flagged by all three methods (Isolation Forest, LOF, Z-score) with a z-score of 13.2 and 27.0x the expected baseline volume. Strong consensus on this anomaly.

Analytical commentary: This route shows a pronounced deviation from expected behavior. The event volume significantly exceeds the population average, indicating a potential operational or security concern requiring immediate attention. The strong consensus among detection methods reinforces the reliability of this finding.
#### London Gatwick (LGW) → Milano Malpensa (MXP)
- **Events**: 103255 (baseline mean: 1200.6)
- **Z-score**: 13.54
- **Ratio to baseline**: 86.00x
- **Anomaly score**: 1.94
- **Risk score**: 94.01
- **Detection consensus**: flagged by all 3 methods (Isolation Forest, Local Outlier Factor, Z-score)
- **Risk reason**: Flagged by all three methods (Isolation Forest, LOF, Z-score) with a z-score of 13.5 and 86.0x the expected baseline volume. Strong consensus on this anomaly.

Analytical commentary: This route shows a pronounced deviation from expected behavior. The event volume significantly exceeds the population average, indicating a potential operational or security concern requiring immediate attention. The strong consensus among detection methods reinforces the reliability of this finding.
### Medium Risk
#### Tirana (TIA) → Bergamo Orio al Serio (BGY)
- **Events**: 4793 (baseline mean: 16.4)
- **Z-score**: 9.05
- **Ratio to baseline**: 293.00x
- **Anomaly score**: 1.39
- **Risk score**: 41.90
- **Detection consensus**: flagged by 2 of 3 methods (Isolation Forest, Z-score)
- **Risk reason**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=9.0, ratio=293.0x baseline.

Analytical commentary: This route exhibits a moderate but noteworthy deviation. While not an immediate operational threat, the elevated activity warrants enhanced monitoring and trend analysis to determine whether the pattern is transient or indicative of an emerging issue.
#### Tirana (TIA) → Bologna (BLQ)
- **Events**: 4138 (baseline mean: 18.1)
- **Z-score**: 7.79
- **Ratio to baseline**: 228.00x
- **Anomaly score**: 1.28
- **Risk score**: 31.26
- **Detection consensus**: flagged by 2 of 3 methods (Isolation Forest, Z-score)
- **Risk reason**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=7.8, ratio=228.0x baseline.

Analytical commentary: This route exhibits a moderate but noteworthy deviation. While not an immediate operational threat, the elevated activity warrants enhanced monitoring and trend analysis to determine whether the pattern is transient or indicative of an emerging issue.
### Lower-Priority Deviations
#### Tirana (TIA) → Pisa (PSA)
- **Events**: 3762 (baseline mean: 19.5)
- **Z-score**: 7.07
- **Ratio to baseline**: 193.00x
- **Anomaly score**: 1.24
- **Risk score**: 27.04
- **Detection consensus**: flagged by 2 of 3 methods (Isolation Forest, Z-score)
- **Risk reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

Analytical commentary: This route shows a mild deviation from expected patterns. While not a cause for immediate concern, routine monitoring is advised to ensure the activity remains within acceptable bounds.
#### Tirana (TIA) → Milano Malpensa (MXP)
- **Events**: 3282 (baseline mean: 15.2)
- **Z-score**: 6.15
- **Ratio to baseline**: 216.00x
- **Anomaly score**: 1.13
- **Risk score**: 16.21
- **Detection consensus**: flagged by 2 of 3 methods (Isolation Forest, Z-score)
- **Risk reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

Analytical commentary: This route shows a mild deviation from expected patterns. While not a cause for immediate concern, routine monitoring is advised to ensure the activity remains within acceptable bounds.
#### Tirana (TIA) → Treviso (TSF)
- **Events**: 2239 (baseline mean: 12.9)
- **Z-score**: 4.14
- **Ratio to baseline**: 174.00x
- **Anomaly score**: 0.96
- **Risk score**: 0.65
- **Detection consensus**: flagged by 2 of 3 methods (Isolation Forest, Z-score)
- **Risk reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

Analytical commentary: This route shows a mild deviation from expected patterns. While not a cause for immediate concern, routine monitoring is advised to ensure the activity remains within acceptable bounds.
#### Tunis (TUN) → Bologna (BLQ)
- **Events**: 10534 (baseline mean: 877.8)
- **Z-score**: 1.25
- **Ratio to baseline**: 12.00x
- **Anomaly score**: 0.96
- **Risk score**: 0.00
- **Detection consensus**: flagged by 2 of 3 methods (Isolation Forest, Local Outlier Factor)
- **Risk reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

Analytical commentary: This route shows a mild deviation from expected patterns. While not a cause for immediate concern, routine monitoring is advised to ensure the activity remains within acceptable bounds.
## Methodology
Anomaly detection was performed by computing a population-level baseline per route and applying three independent methods—Isolation Forest, Local Outlier Factor, and Z-score—to flag unusual behavior. A route was marked anomalous only when at least two of the three methods agreed (majority voting). The combined anomaly_score is the sum of the three methods' normalized scores, providing a continuous severity measure on top of the binary consensus. The analysis was restricted to February departures grouped by airport pairs as specified in the user’s query. The voting mechanism ensures high confidence: a 3/3 consensus is stronger evidence than a 2/3 split.
## Recommended Actions
Immediate review is recommended for the following high-risk routes:
- **Tirana (TIA) → Verona (VRN)**: Flagged by 2 of 3 methods (Isolation Forest, Z-score) with a z-score of 13.2; deviation of 89.0x from baseline volume.
- **London City (LCY) → Firenze Peretola (FLR)**: Flagged by all three methods (Isolation Forest, LOF, Z-score) with a z-score of 13.2 and 27.0x the expected baseline volume. Strong consensus on this anomaly.
- **London Gatwick (LGW) → Milano Malpensa (MXP)**: Flagged by all three methods (Isolation Forest, LOF, Z-score) with a z-score of 13.5 and 86.0x the expected baseline volume. Strong consensus on this anomaly.
Enhanced monitoring and trend analysis are advised for these medium-risk routes:
- **Tirana (TIA) → Bergamo Orio al Serio (BGY)**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=9.0, ratio=293.0x baseline.
- **Tirana (TIA) → Bologna (BLQ)**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=7.8, ratio=228.0x baseline.
Routine monitoring is sufficient for lower-priority deviations; no escalation is required.