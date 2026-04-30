# Anomaly Report

## Executive Summary
The user requested identification of routes with anomalous event counts to support monitoring and investigative activities. The analysis covered route-level groupings derived from the datasets `allarmi_raw` and `tipologia_raw` under the specified filters.

Across 14 monitored route groups, 2 presented high risk, 4 moderate risk, and 8 lower-priority deviations. The overall distribution indicates that the majority of routes operated within expected parameters, with only a small subset requiring attention.

## Risk Distribution
Of the 14 flagged route groups, 2 present high risk, 4 moderate risk, and 8 lower-priority deviations. High-risk groups represent the most urgent cases for review, while medium-risk entities may benefit from enhanced monitoring. Low-risk deviations are noted for situational awareness but do not require immediate escalation.

## Detailed Findings

### HIGH Risk Entities

#### Tirana (TIA) → Bergamo Orio al Serio (BGY)

- **Events Observed**: 4793 (baseline mean: 16)
- **Z-Score**: 9.05
- **Ratio to Baseline**: 293.00x
- **Anomaly Score**: 301.05
- **Risk Score**: 100.00
- **Risk Reason**: This group shows a z-score of 9.0, indicating volume 9.0 times above the population average for dataset tipologia_raw.

**Analytical Interpretation:**
This route recorded 4793 events, significantly exceeding the population average of 16. The 9.0-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → blq

- **Events Observed**: 4138 (baseline mean: 18)
- **Z-Score**: 7.79
- **Ratio to Baseline**: 228.00x
- **Anomaly Score**: 234.79
- **Risk Score**: 73.10
- **Risk Reason**: This group shows a z-score of 7.8, indicating volume 7.8 times above the population average for dataset tipologia_raw.

**Analytical Interpretation:**
This route recorded 4138 events, significantly exceeding the population average of 18. The 7.8-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

### MEDIUM Risk Entities

#### Tirana (TIA) → Roma Fiumicino (FCO)

- **Events Observed**: 1169 (baseline mean: 5)
- **Z-Score**: 2.09
- **Ratio to Baseline**: 223.00x
- **Anomaly Score**: 224.09
- **Risk Score**: 68.76
- **Risk Reason**: Moderate deviation detected: z-score=2.1, ratio=223.0x baseline.

**Analytical Interpretation:**
This route recorded 1169 events, significantly exceeding the population average of 5. The 2.1-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → Milano Malpensa (MXP)

- **Events Observed**: 3282 (baseline mean: 15)
- **Z-Score**: 6.15
- **Ratio to Baseline**: 216.00x
- **Anomaly Score**: 221.15
- **Risk Score**: 67.56
- **Risk Reason**: Moderate deviation detected: z-score=6.1, ratio=216.0x baseline.

**Analytical Interpretation:**
This route recorded 3282 events, significantly exceeding the population average of 15. The 6.1-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → Pisa Galileo Galilei (PSA)

- **Events Observed**: 3762 (baseline mean: 19)
- **Z-Score**: 7.07
- **Ratio to Baseline**: 193.00x
- **Anomaly Score**: 199.07
- **Risk Score**: 58.60
- **Risk Reason**: Moderate deviation detected: z-score=7.1, ratio=193.0x baseline.

**Analytical Interpretation:**
This route recorded 3762 events, significantly exceeding the population average of 19. The 7.1-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → Treviso-Sant’Angelo (TSF)

- **Events Observed**: 2239 (baseline mean: 12)
- **Z-Score**: 4.14
- **Ratio to Baseline**: 174.00x
- **Anomaly Score**: 177.14
- **Risk Score**: 49.70
- **Risk Reason**: Moderate deviation detected: z-score=4.1, ratio=174.0x baseline.

**Analytical Interpretation:**
This route recorded 2239 events, significantly exceeding the population average of 12. The 4.1-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

### LOW Risk Entities

#### Tirana (TIA) → bri

- **Events Observed**: 884 (baseline mean: 7)
- **Z-Score**: 1.54
- **Ratio to Baseline**: 121.00x
- **Anomaly Score**: 121.54
- **Risk Score**: 27.12
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Interpretation:**
This route recorded 884 events, significantly exceeding the population average of 7. The 1.5-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → vrn

- **Events Observed**: 6966 (baseline mean: 78)
- **Z-Score**: 13.22
- **Ratio to Baseline**: 89.00x
- **Anomaly Score**: 101.22
- **Risk Score**: 18.87
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Interpretation:**
This route recorded 6966 events, significantly exceeding the population average of 78. The 13.2-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### London Heathrow (LHR) → lin

- **Events Observed**: 13451 (baseline mean: 137)
- **Z-Score**: 1.63
- **Ratio to Baseline**: 98.00x
- **Anomaly Score**: 98.63
- **Risk Score**: 17.82
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Interpretation:**
This route recorded 13451 events, significantly exceeding the population average of 137. The 1.6-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### lgw → Milano Malpensa (MXP)

- **Events Observed**: 103255 (baseline mean: 1200)
- **Z-Score**: 13.54
- **Ratio to Baseline**: 86.00x
- **Anomaly Score**: 98.54
- **Risk Score**: 17.78
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Interpretation:**
This route recorded 103255 events, significantly exceeding the population average of 1200. The 13.5-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → trn

- **Events Observed**: 1597 (baseline mean: 19)
- **Z-Score**: 2.91
- **Ratio to Baseline**: 80.00x
- **Anomaly Score**: 81.91
- **Risk Score**: 11.03
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Interpretation:**
This route recorded 1597 events, significantly exceeding the population average of 19. The 2.9-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → Roma Ciampino (CIA)

- **Events Observed**: 1079 (baseline mean: 13)
- **Z-Score**: 1.92
- **Ratio to Baseline**: 79.00x
- **Anomaly Score**: 79.92
- **Risk Score**: 10.22
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Interpretation:**
This route recorded 1079 events, significantly exceeding the population average of 13. The 1.9-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → goa

- **Events Observed**: 1338 (baseline mean: 17)
- **Z-Score**: 2.41
- **Ratio to Baseline**: 75.00x
- **Anomaly Score**: 76.41
- **Risk Score**: 8.80
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Interpretation:**
This route recorded 1338 events, significantly exceeding the population average of 17. The 2.4-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

#### Tirana (TIA) → aoi

- **Events Observed**: 985 (baseline mean: 18)
- **Z-Score**: 1.74
- **Ratio to Baseline**: 54.00x
- **Anomaly Score**: 54.74
- **Risk Score**: 0.00
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Interpretation:**
This route recorded 985 events, significantly exceeding the population average of 18. The 1.7-sigma deviation suggests a substantial volume spike that may reflect seasonal travel patterns, operational changes, or emerging risk factors.

## Methodology
Anomaly detection was performed by computing population-level baselines for each route group, then applying z-score normalization to identify statistically significant deviations. Hybrid flagging combined top-K ranking with a minimum confidence floor to reduce false positives. Scope filtering ensured only relevant route groups from the specified datasets were evaluated. This approach emphasizes precision and minimizes unnecessary escalations while surfacing the most material anomalies.

## Recommended Actions
Immediate review is recommended for the 2 high-risk route groups, particularly:
- Tirana (TIA) → Bergamo Orio al Serio (BGY) (risk score: 100.0)
- Tirana (TIA) → blq (risk score: 73.1)
Conduct operational debriefs and data validation for these routes to determine whether observed anomalies reflect true risk or data artifacts.