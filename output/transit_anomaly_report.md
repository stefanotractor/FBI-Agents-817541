# Transit Anomaly Report

## Executive Summary
The analysis identified 18 flagged transit routes with varying risk levels. This report summarizes the anomaly landscape and provides actionable insights for operational review.

## Risk Distribution
- **HIGH risk routes:** 2
- **MEDIUM risk routes:** 0
- **LOW risk routes:** 16

## Top High-Risk Routes
- **Route:** londra ? (lgw) → milano malpensa (mxp)
  - Risk Score: 99.99999999999952
  - Alert Rate: 1200.63
  - Total Alarms: 103254.0
  - Risk Reason: Very high alert rate on this route

- **Route:** londra london city (lcy) → firenze firenze peretola (flr)
  - Risk Score: 97.3721541590194
  - Alert Rate: 3726.11
  - Total Alarms: 100605.0
  - Risk Reason: Very high alert rate on this route

### Other flagged routes for monitoring
- **Route:** londra london heathrow (lhr) → milano linate (lin) (Risk: LOW)
  - Risk Score: 10.59669659243088
  - Alert Rate: 130.01
  - Total Alarms: 13131.0

- **Route:** tunis carthage (tun) → bologna guglielmo marconi (blq) (Risk: LOW)
  - Risk Score: 8.020435494271078
  - Alert Rate: 877.83
  - Total Alarms: 10534.0

- **Route:** doha hamad international (doh) → milano malpensa (mxp) (Risk: LOW)
  - Risk Score: 1.2241456276970326
  - Alert Rate: 61.38
  - Total Alarms: 3683.0

- **Route:** londra stansted (stn) → bergamo orio al serio (bgy) (Risk: LOW)
  - Risk Score: 0.9047170279251976
  - Alert Rate: 33.28
  - Total Alarms: 3361.0

- **Route:** buenos aires ezeiza ministro pistarini (eze) → roma fiumicino (fco) (Risk: LOW)
  - Risk Score: 0.7469867566092913
  - Alert Rate: 103.29
  - Total Alarms: 3202.0

- **Route:** addis ababa bole international (add) → roma fiumicino (fco) (Risk: LOW)
  - Risk Score: 0.6834978423689267
  - Alert Rate: 108.21
  - Total Alarms: 3138.0

- **Route:** londra stansted (stn) → roma ciampino (cia) (Risk: LOW)
  - Risk Score: 0.6686176280938412
  - Alert Rate: 38.09
  - Total Alarms: 3123.0

- **Route:** abu dhabi abu dhabi international (auh) → roma fiumicino (fco) (Risk: LOW)
  - Risk Score: 0.6289370566936135
  - Alert Rate: 75.20
  - Total Alarms: 3083.0

- **Route:** san paolo sao paulo/guarulhos-governador andre franco montoro international (gru) → roma fiumicino (fco) (Risk: LOW)
  - Risk Score: 0.5753682853033055
  - Alert Rate: 73.88
  - Total Alarms: 3029.0

- **Route:** tirana rinas mother teresa (tia) → bergamo orio al serio (bgy) (Risk: LOW)
  - Risk Score: 0.3938296711472627
  - Alert Rate: 30.93
  - Total Alarms: 2846.0

## Main Drivers
Risk levels reflect statistical deviations rather than confirmed threats. Key metrics influencing risk classification include:

- **Anomaly Score:** Average 29851.50 — measures deviation from baseline patterns.
- **Alert Rate:** Average 374.82 — frequency of anomaly triggers per route.
- **Total Alarms:** Average 14923 — cumulative anomaly events per route.
Routes flagged as HIGH require immediate operational review to validate anomalies and assess operational impact.

## Recommended Next Actions
1. **Immediate Review:** Conduct urgent analysis on all HIGH risk routes to determine root cause and validate findings.
2. **Operational Escalation:** Notify relevant stakeholders and implement enhanced monitoring for affected routes.
3. **Follow-up Analysis:** Schedule periodic reassessment to track risk evolution and validate mitigation effectiveness.
