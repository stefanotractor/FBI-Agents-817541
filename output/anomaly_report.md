# Anomaly Report

## Executive Summary
The user requested identification of routes with unusually high or low anomaly-related metrics across two datasets: **allarmi_raw** and **tipologia_raw**. Both datasets were filtered to focus on alarm-related occurrences and control outcomes indicating anomalies, respectively. Groups were defined by departure and arrival airports.
Across 9 groups analyzed, 9 were flagged as anomalous by the detection pipeline.

The analysis applied a robust, multi-method anomaly detection pipeline: Isolation Forest, Local Outlier Factor, and Z-score. A group was flagged only when at least two of the three methods agreed. The combined anomaly_score aggregates the three methods' normalized outputs into a continuous severity measure. This report provides a narrative assessment of the findings, with detailed interpretations of every data point and operational recommendations proportional to the actual risk distribution.

## Risk Distribution
Of the 9 flagged groups, 3 present **high risk**, 2 present **moderate risk**, and 4 present **lower-priority deviations**.

## Detailed Findings

### HIGH RISK: Tirana (TIA) → Verona (VRN)

- **Dataset**: tipologia_raw
- **Group Volume**: 6966 events
- **Baseline Mean**: 78.27 events
- **Z-Score**: 13.22
- **Ratio to Baseline**: 89x
- **Anomaly Score**: 2.00
- **Risk Score**: 100
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score
- **Risk Reason**: Flagged by 2 of 3 methods (Isolation Forest, Z-score) with a z-score of 13.2; deviation of 89.0x from baseline volume.

**Analytical Commentary**:
This group recorded 6966 events against a population average of 78.27, representing a 89-fold deviation with a Z-score of 13.22. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

### HIGH RISK: London City (LCY) → Firenze Peretola (FLR)

- **Dataset**: allarmi_raw
- **Group Volume**: 100605 events
- **Baseline Mean**: 3726.11 events
- **Z-Score**: 13.19
- **Ratio to Baseline**: 27x
- **Anomaly Score**: 1.97
- **Risk Score**: 97.51
- **Detection Consensus**: flagged by all 3 methods
- **Risk Reason**: Flagged by all three methods (Isolation Forest, LOF, Z-score) with a z-score of 13.2 and 27.0x the expected baseline volume. Strong consensus on this anomaly.

**Analytical Commentary**:
This group recorded 100605 events against a population average of 3726.11, representing a 27-fold deviation with a Z-score of 13.19. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

### HIGH RISK: London Gatwick (LGW) → Milano Malpensa (MXP)

- **Dataset**: allarmi_raw
- **Group Volume**: 103255 events
- **Baseline Mean**: 1200.64 events
- **Z-Score**: 13.54
- **Ratio to Baseline**: 86x
- **Anomaly Score**: 1.94
- **Risk Score**: 94.01
- **Detection Consensus**: flagged by all 3 methods
- **Risk Reason**: Flagged by all three methods (Isolation Forest, LOF, Z-score) with a z-score of 13.5 and 86.0x the expected baseline volume. Strong consensus on this anomaly.

**Analytical Commentary**:
This group recorded 103255 events against a population average of 1200.64, representing a 86-fold deviation with a Z-score of 13.54. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

### MEDIUM RISK: Tirana (TIA) → Bergamo Orio al Serio (BGY)

- **Dataset**: tipologia_raw
- **Group Volume**: 4793 events
- **Baseline Mean**: 16.36 events
- **Z-Score**: 9.05
- **Ratio to Baseline**: 293x
- **Anomaly Score**: 1.39
- **Risk Score**: 41.90
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score
- **Risk Reason**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=9.0, ratio=293.0x baseline.

**Analytical Commentary**:
This group recorded 4793 events against a population average of 16.36, representing a 293-fold deviation with a Z-score of 9.05. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

### MEDIUM RISK: Tirana (TIA) → Bologna (BLQ)

- **Dataset**: tipologia_raw
- **Group Volume**: 4138 events
- **Baseline Mean**: 18.15 events
- **Z-Score**: 7.79
- **Ratio to Baseline**: 228x
- **Anomaly Score**: 1.28
- **Risk Score**: 31.26
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score
- **Risk Reason**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=7.8, ratio=228.0x baseline.

**Analytical Commentary**:
This group recorded 4138 events against a population average of 18.15, representing a 228-fold deviation with a Z-score of 7.79. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

### LOW RISK: Tirana (TIA) → Pisa (PSA)

- **Dataset**: tipologia_raw
- **Group Volume**: 3762 events
- **Baseline Mean**: 19.49 events
- **Z-Score**: 7.07
- **Ratio to Baseline**: 193.00x
- **Anomaly Score**: 1.24
- **Risk Score**: 27.04
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score
- **Risk Reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

**Analytical Commentary**:
This group recorded 3762 events against a population average of 19.49, representing a 193.00-fold deviation with a Z-score of 7.07. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

### LOW RISK: Tirana (TIA) → Milano Malpensa (MXP)

- **Dataset**: tipologia_raw
- **Group Volume**: 3282 events
- **Baseline Mean**: 15.19 events
- **Z-Score**: 6.15
- **Ratio to Baseline**: 216x
- **Anomaly Score**: 1.13
- **Risk Score**: 16.21
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score
- **Risk Reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

**Analytical Commentary**:
This group recorded 3282 events against a population average of 15.19, representing a 216-fold deviation with a Z-score of 6.15. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

### LOW RISK: Tirana (TIA) → Treviso (TSF)

- **Dataset**: tipologia_raw
- **Group Volume**: 2239 events
- **Baseline Mean**: 12.87 events
- **Z-Score**: 4.14
- **Ratio to Baseline**: 174.00x
- **Anomaly Score**: 0.96
- **Risk Score**: 0.66
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Z-score
- **Risk Reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

**Analytical Commentary**:
This group recorded 2239 events against a population average of 12.87, representing a 174.00-fold deviation with a Z-score of 4.14. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

### LOW RISK: Tunis (TUN) → Bologna (BLQ)

- **Dataset**: allarmi_raw
- **Group Volume**: 10534 events
- **Baseline Mean**: 877.83 events
- **Z-Score**: 1.25
- **Ratio to Baseline**: 12x
- **Anomaly Score**: 0.96
- **Risk Score**: 0
- **Detection Consensus**: flagged by 2 of 3 methods: Isolation Forest, Local Outlier Factor
- **Risk Reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

**Analytical Commentary**:
This group recorded 10534 events against a population average of 877.83, representing a 12-fold deviation with a Z-score of 1.25. 
The anomaly reflects a plausible operational deviation warranting attention proportional to the risk level assigned.

## Methodology
Anomaly detection was performed using a population-level baseline computed per group. Three independent methods were applied: Isolation Forest (multivariate, tree-based), Local Outlier Factor (multivariate, density-based), and Z-score (univariate, distribution-based). A group was flagged only when at least 2 of the 3 methods agreed (majority voting). The combined anomaly_score is the sum of the three methods' normalized scores, providing a continuous severity measure on top of the binary consensus. Finally, the analysis was restricted to the user's scope: routes defined by departure and arrival airports, filtered for alarm-related events and control outcomes. The voting mechanism is what gives confidence in the findings: a 3/3 consensus is much stronger evidence than a 2/3 split.

## Recommended Actions
Immediate review is recommended for the following high-risk routes:
- **Tirana (TIA) → Verona (VRN)**: Flagged by 2 of 3 methods (Isolation Forest, Z-score) with a z-score of 13.2; deviation of 89.0x from baseline volume.
- **London City (LCY) → Firenze Peretola (FLR)**: Flagged by all three methods (Isolation Forest, LOF, Z-score) with a z-score of 13.2 and 27.0x the expected baseline volume. Strong consensus on this anomaly.
- **London Gatwick (LGW) → Milano Malpensa (MXP)**: Flagged by all three methods (Isolation Forest, LOF, Z-score) with a z-score of 13.5 and 86.0x the expected baseline volume. Strong consensus on this anomaly.
Schedule operational reviews and consider enhanced monitoring for these entities.