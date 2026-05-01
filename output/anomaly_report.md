# Anomaly Report

## Executive Summary
The user requested an analysis of anomalous routes departing from Albania to identify unusual travel patterns or elevated risk indicators. The scope covered two datasets: allarmi_raw and tipologia_raw, both filtered to events originating from Albania (codice_paese_part='alb'). Groups were defined by route (departure and arrival airports) and month of departure.

Across 6 monitored groups, 6 were flagged as anomalous. Risk distribution: 1 high-risk, 2 medium-risk, and 3 lower-priority deviations. This assessment is based on consensus among three independent detection methods—Isolation Forest, Local Outlier Factor, and Z-score—each providing a multivariate or univariate signal of deviation from baseline behavior.

## Risk Distribution
Of the 6 flagged groups, 1 present high risk, 2 moderate risk, and 3 lower-priority deviations. High-risk entities require immediate attention, while medium-risk groups should be placed under enhanced monitoring. Lower-risk anomalies are suitable for routine review cycles.

## Detailed Findings

### Tirana (TIA)→Verona (VRN)
- **Events**: 6,966 recorded against a baseline mean of 78.3.
- **Rate**: 77.40 events per unit, with a z-score of 13.22.
- **Deviation**: 89.00x the baseline volume.
- **Anomaly Score**: 2.00 (sum of three normalized method scores).
- **Risk Score**: 100.00 (HIGH risk).
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score.
- **Risk Reason**: Flagged by 2 of 3 methods (Isolation Forest, Z-score) with a z-score of 13.2; deviation of 89.0x from baseline volume.
- **Interpretation**: This group shows a substantial volume increase relative to baseline, suggesting either a seasonal surge, targeted activity, or data reporting anomaly. The high z-score and multi-method consensus strengthen confidence in the deviation.

### Tirana (TIA)→Bergamo Orio al Serio (BGY)
- **Events**: 4,793 recorded against a baseline mean of 16.4.
- **Rate**: 16.14 events per unit, with a z-score of 9.05.
- **Deviation**: 293.00x the baseline volume.
- **Anomaly Score**: 1.39 (sum of three normalized method scores).
- **Risk Score**: 41.52 (MEDIUM risk).
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score.
- **Risk Reason**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=9.0, ratio=293.0x baseline.
- **Interpretation**: This group shows a substantial volume increase relative to baseline, suggesting either a seasonal surge, targeted activity, or data reporting anomaly. The high z-score and multi-method consensus strengthen confidence in the deviation.

### Tirana (TIA)→Bologna (BLQ)
- **Events**: 4,138 recorded against a baseline mean of 18.1.
- **Rate**: 17.91 events per unit, with a z-score of 7.79.
- **Deviation**: 228.00x the baseline volume.
- **Anomaly Score**: 1.28 (sum of three normalized method scores).
- **Risk Score**: 30.80 (MEDIUM risk).
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score.
- **Risk Reason**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=7.8, ratio=228.0x baseline.
- **Interpretation**: This group shows a substantial volume increase relative to baseline, suggesting either a seasonal surge, targeted activity, or data reporting anomaly. The high z-score and multi-method consensus strengthen confidence in the deviation.

### Tirana (TIA)→Pisa (PSA)
- **Events**: 3,762 recorded against a baseline mean of 19.5.
- **Rate**: 18.90 events per unit, with a z-score of 7.07.
- **Deviation**: 193.00x the baseline volume.
- **Anomaly Score**: 1.24 (sum of three normalized method scores).
- **Risk Score**: 26.56 (LOW risk).
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score.
- **Risk Reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.
- **Interpretation**: This group shows a substantial volume increase relative to baseline, suggesting either a seasonal surge, targeted activity, or data reporting anomaly. The high z-score and multi-method consensus strengthen confidence in the deviation.

### Tirana (TIA)→Milano Malpensa (MXP)
- **Events**: 3,282 recorded against a baseline mean of 15.2.
- **Rate**: 14.92 events per unit, with a z-score of 6.15.
- **Deviation**: 216.00x the baseline volume.
- **Anomaly Score**: 1.13 (sum of three normalized method scores).
- **Risk Score**: 15.65 (LOW risk).
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score.
- **Risk Reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.
- **Interpretation**: This group shows a substantial volume increase relative to baseline, suggesting either a seasonal surge, targeted activity, or data reporting anomaly. The high z-score and multi-method consensus strengthen confidence in the deviation.

### Tirana (TIA)→Treviso (TSF)
- **Events**: 2,239 recorded against a baseline mean of 12.9.
- **Rate**: 12.72 events per unit, with a z-score of 4.14.
- **Deviation**: 174.00x the baseline volume.
- **Anomaly Score**: 0.96 (sum of three normalized method scores).
- **Risk Score**: 0.00 (LOW risk).
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score.
- **Risk Reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.
- **Interpretation**: This group shows a substantial volume increase relative to baseline, suggesting either a seasonal surge, targeted activity, or data reporting anomaly. The high z-score and multi-method consensus strengthen confidence in the deviation.

## Methodology
Anomaly detection was performed using a three-method ensemble: Isolation Forest (tree-based multivariate), Local Outlier Factor (density-based multivariate), and Z-score (univariate distribution-based). Each method independently evaluates whether a group’s behavior deviates from its historical baseline. A group is flagged as an anomaly only when at least two of the three methods agree (majority voting), ensuring high confidence in the findings. The combined anomaly_score aggregates normalized outputs from all methods to provide a continuous severity measure on top of the binary consensus.

The analysis was restricted to the user’s scope: routes departing from Albania, grouped by departure and arrival airports and month of travel. Population-level baselines were computed per group, enabling fair comparison across entities of varying sizes and seasonal patterns.

## Recommended Actions
Immediate review is recommended for the following high-risk groups:
- **Tirana (TIA)→Verona (VRN)**: Risk score 100.00. Investigate cause of elevated activity and validate data integrity.