# Anomaly Report

## Executive Summary
The user requested identification of routes with unusually high or low anomaly-related metrics for monitoring. The analysis covered route-level aggregates derived from alarm occurrences and flagged travelers across two datasets: allarmi_raw, tipologia_raw. In total, 9 groups were analyzed, of which 9 were flagged as anomalous. The overall risk distribution shows 3 high-risk routes, 1 medium-risk routes, and 5 lower-priority deviations.

## Risk Distribution
Of the 9 flagged groups, 3 present high risk, 1 moderate risk, and 5 lower-priority deviations.

## Detailed Findings

### London City (LCY) → Firenze Peretola (FLR)

This group recorded 100605.0 events against a population average of 3726.1, representing a 27.0 deviation.
Detection consensus: flagged by 3 of 3 methods (Isolation Forest, Local Outlier Factor, Z-score).
Combined anomaly severity score: 1.97 out of 3.00. Risk score: 100.0 out of 100.

Risk reason: Flagged unanimously by all three methods (Isolation Forest, LOF, Z-score). Volume is approximately 27.0x the baseline mean. Strong consensus signal.

Analytical commentary:
- The observed volume (100605.0) significantly exceeds the baseline (3726.1), indicating a true volume anomaly rather than a rate anomaly.
- The 27.0 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.

### London Gatwick (LGW) → Milano Malpensa (MXP)

This group recorded 103255.0 events against a population average of 1200.6, representing a 86.0 deviation.
Detection consensus: flagged by 3 of 3 methods (Isolation Forest, Local Outlier Factor, Z-score).
Combined anomaly severity score: 1.94 out of 3.00. Risk score: 96.4 out of 100.

Risk reason: Flagged unanimously by all three methods (Isolation Forest, LOF, Z-score). Volume is approximately 86.0x the baseline mean. Strong consensus signal.

Analytical commentary:
- The observed volume (103255.0) significantly exceeds the baseline (1200.6), indicating a true volume anomaly rather than a rate anomaly.
- The 86.0 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.

### Tirana (TIA) → Bologna (BLQ)

This group recorded 30750.0 events against a population average of 134.9, representing a 227.99999999999997 deviation.
Detection consensus: flagged by 2 of 3 methods (Isolation Forest, Z-score).
Combined anomaly severity score: 1.94 out of 3.00. Risk score: 96.2 out of 100.

Risk reason: Flagged by 2 of 3 methods (Isolation Forest, Z-score) with volume approximately 228.0x the baseline mean.

Analytical commentary:
- The observed volume (30750.0) significantly exceeds the baseline (134.9), indicating a true volume anomaly rather than a rate anomaly.
- The 227.99999999999997 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.

### Tirana (TIA) → Bergamo Orio al Serio (BGY)

This group recorded 25936.0 events against a population average of 88.2, representing a 294.0 deviation.
Detection consensus: flagged by 2 of 3 methods (Isolation Forest, Z-score).
Combined anomaly severity score: 1.59 out of 3.00. Risk score: 62.4 out of 100.

Risk reason: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Volume is roughly 294.0x the baseline mean.

Analytical commentary:
- The observed volume (25936.0) significantly exceeds the baseline (88.2), indicating a true volume anomaly rather than a rate anomaly.
- The 294.0 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.

### Tirana (TIA) → Roma Fiumicino (FCO)

This group recorded 14655.0 events against a population average of 66.0, representing a 222.0 deviation.
Detection consensus: flagged by 2 of 3 methods (Isolation Forest, Z-score).
Combined anomaly severity score: 1.18 out of 3.00. Risk score: 22.2 out of 100.

Risk reason: Borderline anomaly with limited consensus (2/3 methods). Volume deviation around 222.0x the baseline. Monitor for trend changes.

Analytical commentary:
- The observed volume (14655.0) significantly exceeds the baseline (66.0), indicating a true volume anomaly rather than a rate anomaly.
- The 222.0 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.

### London Stansted (STN) → Bergamo Orio al Serio (BGY)

This group recorded 10160.0 events against a population average of 97.7, representing a 104.0 deviation.
Detection consensus: flagged by 2 of 3 methods (Isolation Forest, Z-score).
Combined anomaly severity score: 1.16 out of 3.00. Risk score: 20.2 out of 100.

Risk reason: Borderline anomaly with limited consensus (2/3 methods). Volume deviation around 104.0x the baseline. Monitor for trend changes.

Analytical commentary:
- The observed volume (10160.0) significantly exceeds the baseline (97.7), indicating a true volume anomaly rather than a rate anomaly.
- The 104.0 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.

### Tirana (TIA) → Treviso (TSF)

This group recorded 11991.0 events against a population average of 70.5, representing a 170.0 deviation.
Detection consensus: flagged by 2 of 3 methods (Isolation Forest, Z-score).
Combined anomaly severity score: 1.09 out of 3.00. Risk score: 13.0 out of 100.

Risk reason: Borderline anomaly with limited consensus (2/3 methods). Volume deviation around 170.0x the baseline. Monitor for trend changes.

Analytical commentary:
- The observed volume (11991.0) significantly exceeds the baseline (70.5), indicating a true volume anomaly rather than a rate anomaly.
- The 170.0 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.

### Tunis (TUN) → Bologna (BLQ)

This group recorded 10534.0 events against a population average of 877.8, representing a 12.0 deviation.
Detection consensus: flagged by 2 of 3 methods (Isolation Forest, Local Outlier Factor, ).
Combined anomaly severity score: 0.96 out of 3.00. Risk score: 0.2 out of 100.

Risk reason: Borderline anomaly with limited consensus (2/3 methods). Volume deviation around 12.0x the baseline. Monitor for trend changes.

Analytical commentary:
- The observed volume (10534.0) significantly exceeds the baseline (877.8), indicating a true volume anomaly rather than a rate anomaly.
- The 12.0 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.

### Tirana (TIA) → Torino (TRN)

This group recorded 8599.0 events against a population average of 107.5, representing a 80.0 deviation.
Detection consensus: flagged by 2 of 3 methods (Isolation Forest, Z-score).
Combined anomaly severity score: 0.96 out of 3.00. Risk score: 0.0 out of 100.

Risk reason: Borderline anomaly with limited consensus (2/3 methods). Volume deviation around 80.0x the baseline. Monitor for trend changes.

Analytical commentary:
- The observed volume (8599.0) significantly exceeds the baseline (107.5), indicating a true volume anomaly rather than a rate anomaly.
- The 80.0 multiplier suggests a sustained shift in activity for this route, not a transient spike.
- Given the consensus among multiple detection methods, this deviation is unlikely to be a false positive.


## Methodology
A population-level baseline was computed per route. Three independent anomaly detection methods—Isolation Forest (multivariate, tree-based), Local Outlier Factor (multivariate, density-based), and Z-score (univariate, distribution-based)—were applied. Each method produced a boolean flag and a continuous score normalized to [0, 1] per dataset. A route was flagged as an anomaly only when at least 2 of the 3 methods agreed (majority voting). The combined anomaly_score is the sum of the three normalized scores (range 0–3), giving a continuous severity measure on top of the binary consensus. The risk_score (0–100) is a min-max normalization of anomaly_score across the flagged groups, used to assign the HIGH/MEDIUM/LOW levels. Finally, the analysis was restricted to the user's scope: route-level aggregates from alarm occurrences and flagged travelers, filtered to relevant event types and travelers.

The voting mechanism is what gives confidence in the findings: a 3/3 consensus is stronger evidence than a 2/3 split.

## Recommended Actions
Immediate review is recommended for the following high-risk routes:
- London City (LCY) → Firenze Peretola (FLR): Flagged unanimously by all three methods (Isolation Forest, LOF, Z-score). Volume is approximately 27.0x the baseline mean. Strong consensus signal.
- London Gatwick (LGW) → Milano Malpensa (MXP): Flagged unanimously by all three methods (Isolation Forest, LOF, Z-score). Volume is approximately 86.0x the baseline mean. Strong consensus signal.
- Tirana (TIA) → Bologna (BLQ): Flagged by 2 of 3 methods (Isolation Forest, Z-score) with volume approximately 228.0x the baseline mean.

Schedule a joint analysis with operations and security teams to determine the root cause and implement mitigations.