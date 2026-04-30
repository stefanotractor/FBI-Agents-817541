# Anomaly Report
## Executive Summary
The user requested: **Identify anomalous flight routes departing from Albania during January.**. We analyzed 12 route-level groups across datasets allarmi_raw, tipologia_raw under filters codice_paese_part: alb; mese_partenza: 01; codice_paese_part: alb; mese_partenza: 01. Among these, 12 groups were flagged as anomalous by the risk engine. This is an analytical assessment of deviations from expected patterns; it is not an operational alarm.

## Risk Distribution
Of the 11 flagged groups, 1 present high risk, 4 moderate risk, and 6 lower-priority deviations.

## Detailed Findings

### Rinas Mother Teresa (TIA) → Bergamo Orio al Serio (BGY), January
- **Dataset**: tipologia_raw
- **Events observed**: 4793 (baseline mean: 16.4)
- **Z-score**: 9.05 (ratio to baseline: 293.00x)
- **Anomaly score**: 301.050 | **Risk score**: 100.00
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This group shows a significant deviation: 4793 events versus a population average of 16.4, a 293.0-fold increase. The z-score of 9.05 indicates a rare occurrence under normal conditions, suggesting either a localized spike in activity or an external factor influencing this route during the period.

### Rinas Mother Teresa (TIA) → BLQ, January
- **Dataset**: tipologia_raw
- **Events observed**: 4138 (baseline mean: 18.1)
- **Z-score**: 7.79 (ratio to baseline: 228.00x)
- **Anomaly score**: 234.792 | **Risk score**: 73.10
- **Risk reason**: This group shows a z-score of 7.8, indicating volume 228.0x above the population average for dataset tipologia_raw.
- **Analytical commentary**: 
  This group shows a significant deviation: 4138 events versus a population average of 18.1, a 228.0-fold increase. The z-score of 7.79 indicates a rare occurrence under normal conditions, suggesting either a localized spike in activity or an external factor influencing this route during the period.

### Rinas Mother Teresa (TIA) → Roma Fiumicino Leonardo da Vinci (FCO), January
- **Dataset**: tipologia_raw
- **Events observed**: 1169 (baseline mean: 5.2)
- **Z-score**: 2.09 (ratio to baseline: 223.00x)
- **Anomaly score**: 224.090 | **Risk score**: 68.76
- **Risk reason**: Moderate deviation detected: z-score=2.1, ratio=223.0x baseline.
- **Analytical commentary**: 
  This group shows a significant deviation: 1169 events versus a population average of 5.2, a 223.0-fold increase. The z-score of 2.09 indicates a rare occurrence under normal conditions, suggesting either a localized spike in activity or an external factor influencing this route during the period.

### Rinas Mother Teresa (TIA) → Milano Malpensa (MXP), January
- **Dataset**: tipologia_raw
- **Events observed**: 3282 (baseline mean: 15.2)
- **Z-score**: 6.15 (ratio to baseline: 216.00x)
- **Anomaly score**: 221.148 | **Risk score**: 67.56
- **Risk reason**: Moderate deviation detected: z-score=6.1, ratio=216.0x baseline.
- **Analytical commentary**: 
  This group shows a significant deviation: 3282 events versus a population average of 15.2, a 216.0-fold increase. The z-score of 6.15 indicates a rare occurrence under normal conditions, suggesting either a localized spike in activity or an external factor influencing this route during the period.

### Rinas Mother Teresa (TIA) → Pisa International Airport (PSA), January
- **Dataset**: tipologia_raw
- **Events observed**: 3762 (baseline mean: 19.5)
- **Z-score**: 7.07 (ratio to baseline: 193.00x)
- **Anomaly score**: 199.070 | **Risk score**: 58.60
- **Risk reason**: Moderate deviation detected: z-score=7.1, ratio=193.0x baseline.
- **Analytical commentary**: 
  This group shows a significant deviation: 3762 events versus a population average of 19.5, a 193.0-fold increase. The z-score of 7.07 indicates a rare occurrence under normal conditions, suggesting either a localized spike in activity or an external factor influencing this route during the period.

### Rinas Mother Teresa (TIA) → Treviso-Sant’Angelo (TSF), January
- **Dataset**: tipologia_raw
- **Events observed**: 2239 (baseline mean: 12.9)
- **Z-score**: 4.14 (ratio to baseline: 174.00x)
- **Anomaly score**: 177.145 | **Risk score**: 49.70
- **Risk reason**: Moderate deviation detected: z-score=4.1, ratio=174.0x baseline.
- **Analytical commentary**: 
  This group shows a significant deviation: 2239 events versus a population average of 12.9, a 174.0-fold increase. The z-score of 4.14 indicates a rare occurrence under normal conditions, suggesting either a localized spike in activity or an external factor influencing this route during the period.

### Rinas Mother Teresa (TIA) → BRI, January
- **Dataset**: tipologia_raw
- **Events observed**: 884 (baseline mean: 7.3)
- **Z-score**: 1.54 (ratio to baseline: 121.00x)
- **Anomaly score**: 121.543 | **Risk score**: 27.12
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This group exhibits a moderate elevation: 884 events compared to a baseline of 7.3, representing a 121.0-fold deviation. While not extreme, it warrants monitoring for trend development.

### Rinas Mother Teresa (TIA) → VRN, January
- **Dataset**: tipologia_raw
- **Events observed**: 6966 (baseline mean: 78.3)
- **Z-score**: 13.22 (ratio to baseline: 89.00x)
- **Anomaly score**: 101.223 | **Risk score**: 18.87
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This group shows a significant deviation: 6966 events versus a population average of 78.3, a 89.0-fold increase. The z-score of 13.22 indicates a rare occurrence under normal conditions, suggesting either a localized spike in activity or an external factor influencing this route during the period.

### Rinas Mother Teresa (TIA) → TRN, January
- **Dataset**: tipologia_raw
- **Events observed**: 1597 (baseline mean: 20.0)
- **Z-score**: 2.91 (ratio to baseline: 80.00x)
- **Anomaly score**: 81.912 | **Risk score**: 11.03
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This group shows a significant deviation: 1597 events versus a population average of 20.0, a 80.0-fold increase. The z-score of 2.91 indicates a rare occurrence under normal conditions, suggesting either a localized spike in activity or an external factor influencing this route during the period.

### Rinas Mother Teresa (TIA) → Roma Ciampino (CIA), January
- **Dataset**: tipologia_raw
- **Events observed**: 1079 (baseline mean: 13.7)
- **Z-score**: 1.92 (ratio to baseline: 79.00x)
- **Anomaly score**: 79.917 | **Risk score**: 10.22
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This group exhibits a moderate elevation: 1079 events compared to a baseline of 13.7, representing a 79.0-fold deviation. While not extreme, it warrants monitoring for trend development.

#### Other flagged groups (summary)
- Rinas Mother Teresa (TIA) → GOA, January: risk=8.80, events=1338, z=2.41
- Rinas Mother Teresa (TIA) → AOI, January: risk=0.00, events=985, z=1.74

## Methodology
Anomalies were detected by computing a population-level baseline per route across the two datasets. For each group, a z-score was derived from the observed event count versus the baseline mean and standard deviation. Hybrid flagging combined top-K ranking by anomaly score with a minimum confidence floor. Only groups within the user’s specified scope (departures from Albania in January) were evaluated.

## Recommended Actions
Immediate review is recommended for the following high-risk routes:
- **Rinas Mother Teresa (TIA) → BLQ, January**: This group shows a z-score of 7.8, indicating volume 228.0x above the population average for dataset tipologia_raw. (risk score: 73.10)
Operations should prioritize these entities to validate whether the deviations reflect true anomalies or data artifacts.