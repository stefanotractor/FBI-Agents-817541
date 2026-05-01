# Anomaly Report

## Executive Summary
The user requested identification of anomalous routes where flights depart from airports in Albania. The analysis aggregated events by route (departure → arrival) across two datasets: tipologia_raw and allarmi_raw, both filtered to records where the departure country is Albania (codice_paese_part = 'alb'). A total of 6 route-level groups were analyzed. Of these, 6 groups were flagged as anomalous by the detection ensemble.

The anomaly detection pipeline combined three independent methods—Isolation Forest, Local Outlier Factor, and Z-score—to identify unusual deviations in event volumes and rates. A group was flagged only when at least two of the three methods agreed. This majority-voting mechanism ensures high confidence in the findings. The analysis did not rely on any single metric, but instead used a consensus-driven, ensemble approach to reduce false positives.

## Risk Distribution
Of the 6 flagged groups, 1 present **high risk**, 2 present **medium risk**, and 3 present **low-priority deviations**.

| Risk Level | Count |
|------------|-------|
| HIGH       | 1     |
| MEDIUM     | 2     |
| LOW        | 3     |

## Detailed Findings
### tia → vrn

This group recorded **6966 events** against a population average of **78.27**, representing a **89.00-fold deviation**.
The Z-score for this group is **13.22**, indicating a significant departure from the expected distribution.
The anomaly score, combining all three detection methods, is **2.0** out of a possible 3.0, reflecting the severity of the deviation.
The risk score assigned to this group is **100.0**, placing it in the **HIGH** tier.
This entity was flagged by **2 of 3 methods**: Isolation Forest, Z-score.

**Risk reason**: Flagged by 2 of 3 methods (Isolation Forest, Z-score) with a z-score of 13.2; deviation of 89.0x from baseline volume.

**Analytical commentary**: This represents a significant deviation that warrants immediate operational attention. The combination of volume spike, elevated rate, and strong consensus among detection methods suggests a real anomaly rather than noise. Reviewing the underlying events and operational context for this route is recommended to determine whether this reflects a security concern, data quality issue, or exceptional travel pattern.

---
### tia → bgy

This group recorded **4793 events** against a population average of **16.36**, representing a **293.00-fold deviation**.
The Z-score for this group is **9.05**, indicating a significant departure from the expected distribution.
The anomaly score, combining all three detection methods, is **1.39** out of a possible 3.0, reflecting the severity of the deviation.
The risk score assigned to this group is **41.52**, placing it in the **MEDIUM** tier.
This entity was flagged by **2 of 3 methods**: Isolation Forest, Z-score.

**Risk reason**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=9.0, ratio=293.0x baseline.

**Analytical commentary**: This deviation is moderate but consistent across multiple signals. While not an immediate threat, it may indicate an emerging pattern or seasonal effect that could warrant enhanced monitoring. Trend analysis over the next few reporting periods is advised to assess whether this is a transient fluctuation or the start of a sustained shift.

---
### tia → blq

This group recorded **4138 events** against a population average of **18.15**, representing a **228.00-fold deviation**.
The Z-score for this group is **7.79**, indicating a significant departure from the expected distribution.
The anomaly score, combining all three detection methods, is **1.28** out of a possible 3.0, reflecting the severity of the deviation.
The risk score assigned to this group is **30.8**, placing it in the **MEDIUM** tier.
This entity was flagged by **2 of 3 methods**: Isolation Forest, Z-score.

**Risk reason**: Moderate anomaly confirmed by 2 of 3 methods (Isolation Forest, Z-score). Z-score=7.8, ratio=228.0x baseline.

**Analytical commentary**: This deviation is moderate but consistent across multiple signals. While not an immediate threat, it may indicate an emerging pattern or seasonal effect that could warrant enhanced monitoring. Trend analysis over the next few reporting periods is advised to assess whether this is a transient fluctuation or the start of a sustained shift.

---
### tia → psa

This group recorded **3762 events** against a population average of **19.49**, representing a **193.00-fold deviation**.
The Z-score for this group is **7.07**, indicating a significant departure from the expected distribution.
The anomaly score, combining all three detection methods, is **1.24** out of a possible 3.0, reflecting the severity of the deviation.
The risk score assigned to this group is **26.56**, placing it in the **LOW** tier.
This entity was flagged by **2 of 3 methods**: Isolation Forest, Z-score.

**Risk reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

**Analytical commentary**: This group shows a mild deviation from baseline, likely reflecting a routine fluctuation in travel patterns. The anomaly is subtle and detected by only two methods, suggesting lower confidence. Routine monitoring is sufficient; no escalation is required at this time.

---
### tia → mxp

This group recorded **3282 events** against a population average of **15.19**, representing a **216.00-fold deviation**.
The Z-score for this group is **6.15**, indicating a significant departure from the expected distribution.
The anomaly score, combining all three detection methods, is **1.13** out of a possible 3.0, reflecting the severity of the deviation.
The risk score assigned to this group is **15.65**, placing it in the **LOW** tier.
This entity was flagged by **2 of 3 methods**: Isolation Forest, Z-score.

**Risk reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

**Analytical commentary**: This group shows a mild deviation from baseline, likely reflecting a routine fluctuation in travel patterns. The anomaly is subtle and detected by only two methods, suggesting lower confidence. Routine monitoring is sufficient; no escalation is required at this time.

---
### tia → tsf

This group recorded **2239 events** against a population average of **12.87**, representing a **174.00-fold deviation**.
The Z-score for this group is **4.14**, indicating a significant departure from the expected distribution.
The anomaly score, combining all three detection methods, is **0.96** out of a possible 3.0, reflecting the severity of the deviation.
The risk score assigned to this group is **0.0**, placing it in the **LOW** tier.
This entity was flagged by **2 of 3 methods**: Isolation Forest, Z-score.

**Risk reason**: Borderline anomaly with limited consensus (2/3 methods). Monitor for trend changes.

**Analytical commentary**: This group shows a mild deviation from baseline, likely reflecting a routine fluctuation in travel patterns. The anomaly is subtle and detected by only two methods, suggesting lower confidence. Routine monitoring is sufficient; no escalation is required at this time.

---
## Methodology
Anomalies were detected using an ensemble of three independent methods applied to each route-level group. First, a population-level baseline was computed for each group based on historical event volumes and rates. Isolation Forest, a tree-based multivariate method, identified points that are isolated in feature space, making them outliers relative to the majority of the data. Local Outlier Factor, a density-based method, compared local density around a point to that of its neighbors, flagging entities with significantly lower density as anomalies. Z-score, a univariate statistical method, measured how many standard deviations a group's event rate deviated from the mean, flagging values beyond a threshold as unusual. A group was flagged as an anomaly only when at least two of the three methods agreed (majority voting). The combined anomaly_score is the sum of the three methods' normalized scores, providing a continuous measure of severity. This voting mechanism ensures high confidence: a 3/3 consensus is stronger evidence than a 2/3 split.

## Recommended Actions
**Immediate review required.** The following high-risk routes should be prioritized for investigation:
- tia → vrn (Risk Score: 100.00)

Operational teams should examine the underlying events, passenger manifests, and operational logs for these routes. Determine whether the anomalies reflect security concerns, data quality issues, or exceptional travel patterns. If a security issue is suspected, escalate to the appropriate investigative unit immediately.