# Anomaly Report

## Executive Summary
The user requested to identify routes with unusually high or low anomaly-related metrics for anomaly detection.. Across the monitored datasets and applied filters, 11 route-level groups were flagged as anomalous.
Of these, 2 present **high risk**, 2 **medium risk**, and 7 **low-priority deviations**.

The analysis covered the following datasets and scope:
- **allarmi_raw**: filtered for 'voli con allarmi' and 'viaggiatori con allarmi'; grouped by departure and arrival airports using the 'tot' volume metric.
- **tipologia_raw**: filtered for 'allarmati'=1; grouped by departure and arrival airports using the 'entrati' traveler count metric.

Anomalies were detected using a population-level baseline per group, z-score normalization, and hybrid flagging combining top-K ranking with a confidence floor.

## Risk Distribution
Of the 11 flagged groups, 2 present **high risk**, 2 **medium risk**, and 7 **lower-priority deviations**.

| Risk Level | Count |
|------------|-------|
| HIGH       | 2     |
| MEDIUM     | 2     |
| LOW        | 7     |

## Detailed Findings
### High-Risk Routes
- **Tirana International Airport Nënë Tereza (tia) → Tirana, Bergamo Orio al Serio Airport (bgy) → Bergamo**
  - **Events**: 25936 (baseline mean: 88); z-score: 9.51
  - **Ratio to baseline**: 294.00x; anomaly score: 302.51
  - **Risk score**: 100.0; reason: This group shows a z-score of 9.5, indicating volume 25936.0 times above the population average for dataset tipologia_raw.
  - Analytical interpretation: This route recorded 25936 events against a population average of 88, representing a 294.0-fold deviation. The z-score of 9.51 confirms a statistically significant anomaly. Given the risk reason 'This group shows a z-score of 9.5, indicating volume 25936.0 times above the population average for dataset tipologia_raw.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

- **Tirana International Airport Nënë Tereza (tia) → Tirana, blq (unknown airport)**
  - **Events**: 30750 (baseline mean: 134); z-score: 11.31
  - **Ratio to baseline**: 228.00x; anomaly score: 238.31
  - **Risk score**: 71.8; reason: This group shows a z-score of 11.3, indicating volume 30750.0 times above the population average for dataset tipologia_raw.
  - Analytical interpretation: This route recorded 30750 events against a population average of 134, representing a 228.0-fold deviation. The z-score of 11.31 confirms a statistically significant anomaly. Given the risk reason 'This group shows a z-score of 11.3, indicating volume 30750.0 times above the population average for dataset tipologia_raw.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

### Medium-Risk Routes
- **Tirana International Airport Nënë Tereza (tia) → Tirana, Roma Fiumicino Leonardo da Vinci (fco) → Rome**
  - **Events**: 14655 (baseline mean: 66); z-score: 5.30
  - **Ratio to baseline**: 222.00x; anomaly score: 226.30
  - **Risk score**: 66.5; reason: Moderate deviation detected: z-score=5.3, ratio=222.0x baseline.
  - Analytical interpretation: This route recorded 14655 events against a population average of 66, representing a 222.0-fold deviation. The z-score of 5.30 confirms a statistically significant anomaly. Given the risk reason 'Moderate deviation detected: z-score=5.3, ratio=222.0x baseline.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

- **Tirana International Airport Nënë Tereza (tia) → Tirana, Treviso-Sant’Angelo Airport (tsf) → Treviso**
  - **Events**: 12993 (baseline mean: 76); z-score: 4.68
  - **Ratio to baseline**: 170.00x; anomaly score: 173.68
  - **Risk score**: 43.4; reason: Moderate deviation detected: z-score=4.7, ratio=170.0x baseline.
  - Analytical interpretation: This route recorded 12993 events against a population average of 76, representing a 170.0-fold deviation. The z-score of 4.68 confirms a statistically significant anomaly. Given the risk reason 'Moderate deviation detected: z-score=4.7, ratio=170.0x baseline.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

### Low-Risk Routes
- **Tirana International Airport Nënë Tereza (tia) → Tirana, cta (unknown airport)**
  - **Events**: 4577 (baseline mean: 34); z-score: 1.54
  - **Ratio to baseline**: 132.00x; anomaly score: 132.54
  - **Risk score**: 25.3; reason: Minor deviation from baseline; monitor for trend changes.
  - Analytical interpretation: This route recorded 4577 events against a population average of 34, representing a 132.0-fold deviation. The z-score of 1.54 confirms a statistically significant anomaly. Given the risk reason 'Minor deviation from baseline; monitor for trend changes.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

- **Tirana International Airport Nënë Tereza (tia) → Tirana, bri (unknown airport)**
  - **Events**: 5725 (baseline mean: 47); z-score: 1.97
  - **Ratio to baseline**: 120.00x; anomaly score: 120.97
  - **Risk score**: 20.2; reason: Minor deviation from baseline; monitor for trend changes.
  - Analytical interpretation: This route recorded 5725 events against a population average of 47, representing a 120.0-fold deviation. The z-score of 1.97 confirms a statistically significant anomaly. Given the risk reason 'Minor deviation from baseline; monitor for trend changes.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

- **London Stansted Airport (stn) → London, Bergamo Orio al Serio Airport (bgy) → Bergamo**
  - **Events**: 10160 (baseline mean: 97); z-score: 3.62
  - **Ratio to baseline**: 104.00x; anomaly score: 106.62
  - **Risk score**: 13.9; reason: Minor deviation from baseline; monitor for trend changes.
  - Analytical interpretation: This route recorded 10160 events against a population average of 97, representing a 104.0-fold deviation. The z-score of 3.62 confirms a statistically significant anomaly. Given the risk reason 'Minor deviation from baseline; monitor for trend changes.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

- **London Heathrow Airport (lhr) → London, lin (unknown airport)**
  - **Events**: 13131 (baseline mean: 135); z-score: 1.59
  - **Ratio to baseline**: 97.00x; anomaly score: 97.59
  - **Risk score**: 10.0; reason: Minor deviation from baseline; monitor for trend changes.
  - Analytical interpretation: This route recorded 13131 events against a population average of 135, representing a 97.0-fold deviation. The z-score of 1.59 confirms a statistically significant anomaly. Given the risk reason 'Minor deviation from baseline; monitor for trend changes.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

- **lgw (unknown airport), Milano Malpensa (mxp) → Milan**
  - **Events**: 103254 (baseline mean: 1214); z-score: 13.52
  - **Ratio to baseline**: 85.00x; anomaly score: 97.52
  - **Risk score**: 9.9; reason: Minor deviation from baseline; monitor for trend changes.
  - Analytical interpretation: This route recorded 103254 events against a population average of 1214, representing a 85.0-fold deviation. The z-score of 13.52 confirms a statistically significant anomaly. Given the risk reason 'Minor deviation from baseline; monitor for trend changes.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

- **Tirana International Airport Nënë Tereza (tia) → Tirana, trn (unknown airport)**
  - **Events**: 8599 (baseline mean: 107); z-score: 3.04
  - **Ratio to baseline**: 80.00x; anomaly score: 82.04
  - **Risk score**: 3.1; reason: Minor deviation from baseline; monitor for trend changes.
  - Analytical interpretation: This route recorded 8599 events against a population average of 107, representing a 80.0-fold deviation. The z-score of 3.04 confirms a statistically significant anomaly. Given the risk reason 'Minor deviation from baseline; monitor for trend changes.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.

- **Tirana International Airport Nënë Tereza (tia) → Tirana, goa (unknown airport)**
  - **Events**: 5515 (baseline mean: 74); z-score: 1.89
  - **Ratio to baseline**: 74.00x; anomaly score: 74.89
  - **Risk score**: 0.0; reason: Minor deviation from baseline; monitor for trend changes.
  - Analytical interpretation: This route recorded 5515 events against a population average of 74, representing a 74.0-fold deviation. The z-score of 1.89 confirms a statistically significant anomaly. Given the risk reason 'Minor deviation from baseline; monitor for trend changes.', this deviation likely reflects a localized spike in alarms or travelers rather than a seasonal effect.


## Methodology
Anomalies were identified by computing a population-level baseline mean and standard deviation for each route-level group across the two datasets. Z-scores were derived per group, and a hybrid flagging strategy combined top-K ranking with a minimum confidence floor to isolate statistically and operationally significant deviations. Scope filters ensured only relevant alarm occurrences and alarmed travelers were considered. This approach emphasizes precision and minimizes false positives while surfacing meaningful deviations for review.

## Recommended Actions
Immediate review is recommended for the following high-risk routes:
- **Tirana International Airport Nënë Tereza (tia) → Tirana, Bergamo Orio al Serio Airport (bgy) → Bergamo**: risk score 100.0 due to 'This group shows a z-score of 9.5, indicating volume 25936.0 times above the population average for dataset tipologia_raw.'. Escalate to operations for triage and mitigation planning.
- **Tirana International Airport Nënë Tereza (tia) → Tirana, blq (unknown airport)**: risk score 71.8 due to 'This group shows a z-score of 11.3, indicating volume 30750.0 times above the population average for dataset tipologia_raw.'. Escalate to operations for triage and mitigation planning.