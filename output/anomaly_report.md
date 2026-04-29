# Anomaly Report

## Executive Summary
The user requested identification of anomalous routes based on alarm occurrences. Across 2 datasets and applied filters, 14 groups were flagged as anomalous. Of these, 2 present high risk, 4 moderate risk, and 8 lower-priority deviations. The analysis targeted routes formed by departure and arrival airports, focusing on alarm event counts and rates.

## Risk Distribution
Of the 14 flagged groups, 2 present high risk, 4 moderate risk, and 8 lower-priority deviations.

## Detailed Findings

### Tirana International (TIA) → Bergamo Orio al Serio (BGY)

- **Dataset**: tipologia_raw
- **Group Volume**: 4793 events
- **Records Analyzed**: 297
- **Event Rate**: 16.14 events per record
- **Baseline Mean**: 16.4 events
- **Baseline Std Dev**: 16.33
- **Z-Score**: 9.05
- **Ratio to Baseline**: 293.00x
- **Anomaly Score**: 301.05
- **Risk Score**: 100.00
- **Risk Reason**: This group shows a z-score of 9.0, indicating volume 4793.0 vs baseline 16.4 for dataset tipologia_raw.

**Analytical Commentary:**
This group shows a statistically significant deviation from the baseline, with a z-score of 9.05. 
It recorded 4793 events compared to a population average of 16.4, representing a 293.0-fold increase. 
Such a spike may indicate a localized surge in activity, a data quality issue, or an emerging pattern requiring further investigation.

### Tirana International (TIA) → blq

- **Dataset**: tipologia_raw
- **Group Volume**: 4138 events
- **Records Analyzed**: 231
- **Event Rate**: 17.91 events per record
- **Baseline Mean**: 18.1 events
- **Baseline Std Dev**: 16.11
- **Z-Score**: 7.79
- **Ratio to Baseline**: 228.00x
- **Anomaly Score**: 234.79
- **Risk Score**: 73.10
- **Risk Reason**: This group shows a z-score of 7.8, indicating volume 4138.0 vs baseline 18.1 for dataset tipologia_raw.

**Analytical Commentary:**
This group shows a statistically significant deviation from the baseline, with a z-score of 7.79. 
It recorded 4138 events compared to a population average of 18.1, representing a 228.0-fold increase. 
Such a spike may indicate a localized surge in activity, a data quality issue, or an emerging pattern requiring further investigation.

### Tirana International (TIA) → Roma Fiumicino (FCO)

- **Dataset**: tipologia_raw
- **Group Volume**: 1169 events
- **Records Analyzed**: 227
- **Event Rate**: 5.15 events per record
- **Baseline Mean**: 5.2 events
- **Baseline Std Dev**: 12.89
- **Z-Score**: 2.09
- **Ratio to Baseline**: 223.00x
- **Anomaly Score**: 224.09
- **Risk Score**: 68.76
- **Risk Reason**: Moderate deviation detected: z-score=2.1, ratio=223.0x baseline.

**Analytical Commentary:**
A two-fold or greater increase relative to baseline was observed, with 1169 events versus an expected 5.2. 
While not extreme in statistical terms, this ratio suggests a meaningful deviation that may warrant monitoring or targeted review.

### Tirana International (TIA) → Milano Malpensa (MXP)

- **Dataset**: tipologia_raw
- **Group Volume**: 3282 events
- **Records Analyzed**: 220
- **Event Rate**: 14.92 events per record
- **Baseline Mean**: 15.2 events
- **Baseline Std Dev**: 16.52
- **Z-Score**: 6.15
- **Ratio to Baseline**: 216.00x
- **Anomaly Score**: 221.15
- **Risk Score**: 67.56
- **Risk Reason**: Moderate deviation detected: z-score=6.1, ratio=216.0x baseline.

**Analytical Commentary:**
This group shows a statistically significant deviation from the baseline, with a z-score of 6.15. 
It recorded 3282 events compared to a population average of 15.2, representing a 216.0-fold increase. 
Such a spike may indicate a localized surge in activity, a data quality issue, or an emerging pattern requiring further investigation.

### Tirana International (TIA) → Pisa Galileo Galilei (PSA)

- **Dataset**: tipologia_raw
- **Group Volume**: 3762 events
- **Records Analyzed**: 199
- **Event Rate**: 18.90 events per record
- **Baseline Mean**: 19.5 events
- **Baseline Std Dev**: 17.28
- **Z-Score**: 7.07
- **Ratio to Baseline**: 193.00x
- **Anomaly Score**: 199.07
- **Risk Score**: 58.60
- **Risk Reason**: Moderate deviation detected: z-score=7.1, ratio=193.0x baseline.

**Analytical Commentary:**
This group shows a statistically significant deviation from the baseline, with a z-score of 7.07. 
It recorded 3762 events compared to a population average of 19.5, representing a 193.0-fold increase. 
Such a spike may indicate a localized surge in activity, a data quality issue, or an emerging pattern requiring further investigation.

### Tirana International (TIA) → Treviso-Sant’Angelo (TSF)

- **Dataset**: tipologia_raw
- **Group Volume**: 2239 events
- **Records Analyzed**: 176
- **Event Rate**: 12.72 events per record
- **Baseline Mean**: 12.9 events
- **Baseline Std Dev**: 15.17
- **Z-Score**: 4.14
- **Ratio to Baseline**: 174.00x
- **Anomaly Score**: 177.14
- **Risk Score**: 49.70
- **Risk Reason**: Moderate deviation detected: z-score=4.1, ratio=174.0x baseline.

**Analytical Commentary:**
This group shows a statistically significant deviation from the baseline, with a z-score of 4.14. 
It recorded 2239 events compared to a population average of 12.9, representing a 174.0-fold increase. 
Such a spike may indicate a localized surge in activity, a data quality issue, or an emerging pattern requiring further investigation.

### Tirana International (TIA) → bri

- **Dataset**: tipologia_raw
- **Group Volume**: 884 events
- **Records Analyzed**: 122
- **Event Rate**: 7.25 events per record
- **Baseline Mean**: 7.3 events
- **Baseline Std Dev**: 11.01
- **Z-Score**: 1.54
- **Ratio to Baseline**: 121.00x
- **Anomaly Score**: 121.54
- **Risk Score**: 27.12
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Commentary:**
A two-fold or greater increase relative to baseline was observed, with 884 events versus an expected 7.3. 
While not extreme in statistical terms, this ratio suggests a meaningful deviation that may warrant monitoring or targeted review.

### Tirana International (TIA) → vrn

- **Dataset**: tipologia_raw
- **Group Volume**: 6966 events
- **Records Analyzed**: 90
- **Event Rate**: 77.40 events per record
- **Baseline Mean**: 78.3 events
- **Baseline Std Dev**: 528.19
- **Z-Score**: 13.22
- **Ratio to Baseline**: 89.00x
- **Anomaly Score**: 101.22
- **Risk Score**: 18.87
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Commentary:**
This group shows a statistically significant deviation from the baseline, with a z-score of 13.22. 
It recorded 6966 events compared to a population average of 78.3, representing a 89.0-fold increase. 
Such a spike may indicate a localized surge in activity, a data quality issue, or an emerging pattern requiring further investigation.

### London Heathrow (LHR) → lin

- **Dataset**: allarmi_raw
- **Group Volume**: 13253 events
- **Records Analyzed**: 101
- **Event Rate**: 131.22 events per record
- **Baseline Mean**: 135.2 events
- **Baseline Std Dev**: 1008.49
- **Z-Score**: 1.61
- **Ratio to Baseline**: 98.00x
- **Anomaly Score**: 98.61
- **Risk Score**: 17.81
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Commentary:**
A two-fold or greater increase relative to baseline was observed, with 13253 events versus an expected 135.2. 
While not extreme in statistical terms, this ratio suggests a meaningful deviation that may warrant monitoring or targeted review.

### lgw → Milano Malpensa (MXP)

- **Dataset**: allarmi_raw
- **Group Volume**: 103255 events
- **Records Analyzed**: 86
- **Event Rate**: 1200.64 events per record
- **Baseline Mean**: 1200.6 events
- **Baseline Std Dev**: 10779.21
- **Z-Score**: 13.54
- **Ratio to Baseline**: 86.00x
- **Anomaly Score**: 98.54
- **Risk Score**: 17.78
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Commentary:**
This group shows a statistically significant deviation from the baseline, with a z-score of 13.54. 
It recorded 103255 events compared to a population average of 1200.6, representing a 86.0-fold increase. 
Such a spike may indicate a localized surge in activity, a data quality issue, or an emerging pattern requiring further investigation.

### Tirana International (TIA) → trn

- **Dataset**: tipologia_raw
- **Group Volume**: 1597 events
- **Records Analyzed**: 80
- **Event Rate**: 19.96 events per record
- **Baseline Mean**: 20.0 events
- **Baseline Std Dev**: 17.99
- **Z-Score**: 2.91
- **Ratio to Baseline**: 80.00x
- **Anomaly Score**: 81.91
- **Risk Score**: 11.03
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Commentary:**
A two-fold or greater increase relative to baseline was observed, with 1597 events versus an expected 20.0. 
While not extreme in statistical terms, this ratio suggests a meaningful deviation that may warrant monitoring or targeted review.

### Tirana International (TIA) → Roma Ciampino (CIA)

- **Dataset**: tipologia_raw
- **Group Volume**: 1079 events
- **Records Analyzed**: 81
- **Event Rate**: 13.32 events per record
- **Baseline Mean**: 13.7 events
- **Baseline Std Dev**: 18.22
- **Z-Score**: 1.92
- **Ratio to Baseline**: 79.00x
- **Anomaly Score**: 79.92
- **Risk Score**: 10.22
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Commentary:**
A two-fold or greater increase relative to baseline was observed, with 1079 events versus an expected 13.7. 
While not extreme in statistical terms, this ratio suggests a meaningful deviation that may warrant monitoring or targeted review.

### Tirana International (TIA) → goa

- **Dataset**: tipologia_raw
- **Group Volume**: 1338 events
- **Records Analyzed**: 75
- **Event Rate**: 17.84 events per record
- **Baseline Mean**: 17.8 events
- **Baseline Std Dev**: 32.31
- **Z-Score**: 2.41
- **Ratio to Baseline**: 75.00x
- **Anomaly Score**: 76.41
- **Risk Score**: 8.80
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Commentary:**
A two-fold or greater increase relative to baseline was observed, with 1338 events versus an expected 17.8. 
While not extreme in statistical terms, this ratio suggests a meaningful deviation that may warrant monitoring or targeted review.

### Tirana International (TIA) → aoi

- **Dataset**: tipologia_raw
- **Group Volume**: 985 events
- **Records Analyzed**: 55
- **Event Rate**: 17.91 events per record
- **Baseline Mean**: 18.2 events
- **Baseline Std Dev**: 22.76
- **Z-Score**: 1.74
- **Ratio to Baseline**: 54.00x
- **Anomaly Score**: 54.74
- **Risk Score**: 0.00
- **Risk Reason**: Minor deviation from baseline; monitor for trend changes.

**Analytical Commentary:**
A two-fold or greater increase relative to baseline was observed, with 985 events versus an expected 18.2. 
While not extreme in statistical terms, this ratio suggests a meaningful deviation that may warrant monitoring or targeted review.

## Methodology
Population-level baselines were computed for each route group across the filtered datasets. 
Anomalies were detected using z-score thresholds and a hybrid flagging strategy combining top-K selection and a minimum confidence floor. 
Scope filters restricted analysis to specified alarm types and transit categories. 
All findings are relative to the computed baseline and should be interpreted as deviations from expected patterns.

## Recommended Actions
Immediate review is recommended for the following high-risk groups:
- Tirana International (TIA) → Bergamo Orio al Serio (BGY) (risk score: 100.00)
- Tirana International (TIA) → blq (risk score: 73.10)