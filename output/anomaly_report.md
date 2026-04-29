# Anomaly Report

## Executive Summary
The user requested to identify flights departing from Albania that have associated anomalies or alarms. The analysis covered 4 groups across two datasets: 'allarmi_raw' and 'tipologia_raw'. Filters applied: departure country = Albania and occurrences/outcomes indicating anomalies.
Of the 4 flagged groups, 2 present high risk, 0 moderate risk, and 2 lower-priority deviations.

## Risk Distribution
- **HIGH**: 2 groups
- **LOW**: 2 groups

## Detailed Findings
### Tirana International Airport (TIA) → 1
- **Dataset**: tipologia_raw
- **Events observed**: 18174
- **Baseline mean**: 15.0
- **Z-score**: 11.77
- **Ratio to baseline**: 1212.00x
- **Anomaly score**: 1222.77
- **Risk score**: 100.00
- **Risk reason**: Group tia|1 shows a z-score of 11.8, indicating volume 11.8 times above the population average for dataset tipologia_raw.
- **Analytical commentary**: 
  This group shows a statistically significant deviation with a z-score of 11.77, indicating an unusual spike in activity compared to the population baseline. The observed 18174 events exceed the average by 1212.0 times, suggesting a potential anomaly worth immediate attention.

### Tirana International Airport (TIA) → 2
- **Dataset**: tipologia_raw
- **Events observed**: 17425
- **Baseline mean**: 17.5
- **Z-score**: 11.28
- **Ratio to baseline**: 993.00x
- **Anomaly score**: 1003.28
- **Risk score**: 77.21
- **Risk reason**: Group tia|2 shows a z-score of 11.3, indicating volume 11.3 times above the population average for dataset tipologia_raw.
- **Analytical commentary**: 
  This group shows a statistically significant deviation with a z-score of 11.28, indicating an unusual spike in activity compared to the population baseline. The observed 17425 events exceed the average by 993.0 times, suggesting a potential anomaly worth immediate attention.

### Tirana International Airport (TIA) → 1
- **Dataset**: allarmi_raw
- **Events observed**: 12164
- **Baseline mean**: 38.3
- **Z-score**: 8.58
- **Ratio to baseline**: 318.00x
- **Anomaly score**: 325.58
- **Risk score**: 6.85
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This group shows a statistically significant deviation with a z-score of 8.58, indicating an unusual spike in activity compared to the population baseline. The observed 12164 events exceed the average by 318.0 times, suggesting a potential anomaly worth immediate attention.

### Tirana International Airport (TIA) → 2
- **Dataset**: allarmi_raw
- **Events observed**: 8172
- **Baseline mean**: 32.0
- **Z-score**: 5.63
- **Ratio to baseline**: 255.00x
- **Anomaly score**: 259.63
- **Risk score**: 0.00
- **Risk reason**: Minor deviation from baseline; monitor for trend changes.
- **Analytical commentary**: 
  This group shows a statistically significant deviation with a z-score of 5.63, indicating an unusual spike in activity compared to the population baseline. The observed 8172 events exceed the average by 255.0 times, suggesting a potential anomaly worth immediate attention.

## Methodology
Anomalies were detected by computing a population-level baseline for each group (dataset + group_key). Z-scores were calculated per group to identify statistical outliers. Hybrid flagging combined top-K ranking by anomaly score with a minimum confidence floor. Scope filtering restricted analysis to flights departing from Albania with alarm occurrences or control outcomes indicating anomalies. Grouping was performed by departure airport and month to detect monthly anomalies per route.

## Recommended Actions
Immediate review is recommended for the following high-risk groups:
- Tirana International Airport (TIA) → 1
- Tirana International Airport (TIA) → 2
Conduct operational triage and escalate to relevant stakeholders for further investigation.