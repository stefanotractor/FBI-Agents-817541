# Anomaly Report


## Executive Summary

The user requested: 'Identify anomalous routes originating in Albania by analyzing departure airports and associated alarm/event metrics.'. This analysis examined 12 route groups departing from Albania via Istanbul across datasets allarmi_raw, tipologia_raw under filters codice_paese_part: ['alb']; areoporto_partenza: ['ist']; codice_paese_part: ['alb'].
A total of 12 groups were flagged as anomalous, with risk distribution: 2 HIGH, 4 MEDIUM, 6 LOW.
This is an analytical assessment based on statistical deviation from historical baselines, not an operational alarm.

## Risk Distribution
Of the 12 flagged groups, 2 present high risk, 4 moderate risk, and 6 lower-priority deviations.

## Detailed Findings

### TIA (TIA) → BGY (BGY)
- **Dataset**: tipologia_raw
- **Events observed**: 4793.00 (baseline mean: 16.36)
- **Z-score**: 9.05
- **Ratio to baseline**: 293.0x
- **Anomaly score**: 301.05
- **Risk score**: 100.00
- **Risk reason**: This group shows a z-score of 9.0, indicating volume 9.0 standard deviations from the population average for dataset tipologia_raw.
- **Analytical commentary**: 
  This route recorded 4793 events against a population average of 16, representing a 293.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → BLQ (BLQ)
- **Dataset**: tipologia_raw
- **Events observed**: 4138.00 (baseline mean: 18.15)
- **Z-score**: 7.79
- **Ratio to baseline**: 228.0x
- **Anomaly score**: 234.79
- **Risk score**: 73.10
- **Risk reason**: This group shows a z-score of 7.8, indicating volume 7.8 standard deviations from the population average for dataset tipologia_raw.
- **Analytical commentary**: 
  This route recorded 4138 events against a population average of 18, representing a 228.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → FCO (FCO)
- **Dataset**: tipologia_raw
- **Events observed**: 1169.00 (baseline mean: 5.24)
- **Z-score**: 2.09
- **Ratio to baseline**: 223.0x
- **Anomaly score**: 224.09
- **Risk score**: 68.76
- **Risk reason**: Moderate deviation detected: z-score=2.1, ratio=223.0x baseline.
- **Analytical commentary**: 
  This route recorded 1169 events against a population average of 5, representing a 223.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → MXP (MXP)
- **Dataset**: tipologia_raw
- **Events observed**: 3282.00 (baseline mean: 15.19)
- **Z-score**: 6.15
- **Ratio to baseline**: 216.0x
- **Anomaly score**: 221.15
- **Risk score**: 67.56
- **Risk reason**: Moderate deviation detected: z-score=6.1, ratio=216.0x baseline.
- **Analytical commentary**: 
  This route recorded 3282 events against a population average of 15, representing a 216.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → PSA (PSA)
- **Dataset**: tipologia_raw
- **Events observed**: 3762.00 (baseline mean: 19.49)
- **Z-score**: 7.07
- **Ratio to baseline**: 193.0x
- **Anomaly score**: 199.07
- **Risk score**: 58.60
- **Risk reason**: Moderate deviation detected: z-score=7.1, ratio=193.0x baseline.
- **Analytical commentary**: 
  This route recorded 3762 events against a population average of 19, representing a 193.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → TSF (TSF)
- **Dataset**: tipologia_raw
- **Events observed**: 2239.00 (baseline mean: 12.87)
- **Z-score**: 4.14
- **Ratio to baseline**: 174.0x
- **Anomaly score**: 177.14
- **Risk score**: 49.70
- **Risk reason**: Moderate deviation detected: z-score=4.1, ratio=174.0x baseline.
- **Analytical commentary**: 
  This route recorded 2239 events against a population average of 12, representing a 174.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → BRI (BRI)
- **Dataset**: tipologia_raw
- **Events observed**: 884.00 (baseline mean: 7.31)
- **Z-score**: 1.54
- **Ratio to baseline**: 121.0x
- **Anomaly score**: 121.54
- **Risk score**: 27.12
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This route recorded 884 events against a population average of 7, representing a 121.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → VRN (VRN)
- **Dataset**: tipologia_raw
- **Events observed**: 6966.00 (baseline mean: 78.27)
- **Z-score**: 13.22
- **Ratio to baseline**: 89.0x
- **Anomaly score**: 101.22
- **Risk score**: 18.87
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This route recorded 6966 events against a population average of 78, representing a 89.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → TRN (TRN)
- **Dataset**: tipologia_raw
- **Events observed**: 1597.00 (baseline mean: 19.96)
- **Z-score**: 2.91
- **Ratio to baseline**: 80.0x
- **Anomaly score**: 81.91
- **Risk score**: 11.03
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This route recorded 1597 events against a population average of 19, representing a 80.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → CIA (CIA)
- **Dataset**: tipologia_raw
- **Events observed**: 1079.00 (baseline mean: 13.66)
- **Z-score**: 1.92
- **Ratio to baseline**: 79.0x
- **Anomaly score**: 79.92
- **Risk score**: 10.22
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This route recorded 1079 events against a population average of 13, representing a 79.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → GOA (GOA)
- **Dataset**: tipologia_raw
- **Events observed**: 1338.00 (baseline mean: 17.84)
- **Z-score**: 2.41
- **Ratio to baseline**: 75.0x
- **Anomaly score**: 76.41
- **Risk score**: 8.80
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This route recorded 1338 events against a population average of 17, representing a 75.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

### TIA (TIA) → AOI (AOI)
- **Dataset**: tipologia_raw
- **Events observed**: 985.00 (baseline mean: 18.24)
- **Z-score**: 1.74
- **Ratio to baseline**: 54.0x
- **Anomaly score**: 54.74
- **Risk score**: 0.00
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This route recorded 985 events against a population average of 18, representing a 54.0-fold deviation. The elevated activity suggests a potential concentration of risk factors requiring further investigation.

## Methodology
Anomalies were detected by computing population-level baselines per route group across the specified datasets. For each group, a z-score was derived from the observed event volume against the baseline mean and standard deviation. Hybrid flagging combined top-K ranking by anomaly score with a minimum confidence floor to ensure statistical significance. Scope filtering restricted analysis to routes departing from Albania via Istanbul, ensuring relevance to the user's query.

## Recommended Actions
Immediate review is recommended for the following high-risk routes:
- TIA (TIA) → BGY (BGY)
- TIA (TIA) → BLQ (BLQ)