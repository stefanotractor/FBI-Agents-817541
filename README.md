# Classical vs Multi-Agent Pipeline for Anomaly Detection

## Team Members

- **Stefano Losurdo** — Captain  
- **Michele Baldo**  
- **Matteo Perrucci**  

**Company:** Whitehall Reply  
**Project type:** Machine Learning project — Anomaly Detection  
**Main notebook:** `main.ipynb`  
**Data folder:** `data/`

---

## [Section 1] Introduction

This project focuses on **anomaly detection in airport transit and passenger-related data** provided by **Whitehall Reply**. The goal is to identify abnormal routes or route-level patterns that may require further operational investigation.

The work compares two different approaches:

1. a **Classical Pipeline**, manually designed and implemented step by step;
2. a **Multi-Agent Pipeline**, where multiple specialized agents collaborate to automate parts of the machine learning workflow.

The main objective is not only to detect anomalies, but also to understand how the two approaches differ in terms of:

- data preparation effort;
- transparency and interpretability;
- anomaly detection quality;
- operational usability;
- degree of automation;
- robustness of the final output.

The problem is framed as an **unsupervised anomaly detection task**, since the available data does not provide a fully reliable ground-truth label indicating which routes are truly anomalous. For this reason, the project relies on statistical signals, unsupervised learning models, consensus logic, and post-processing rules to obtain an interpretable final ranking of suspicious routes.

---

## Project Overview

The project develops from an initial fully manual pipeline toward a more automated agent-based system.

```mermaid
flowchart LR
    A[Raw datasets provided by Whitehall Reply] --> B[Classical Pipeline]
    A --> C[Multi-Agent Pipeline]

    B --> B1[Manual cleaning]
    B1 --> B2[Manual feature engineering]
    B2 --> B3[Unsupervised anomaly detection]
    B3 --> B4[Consensus voting]
    B4 --> B5[Risk post-processing]

    C --> C1[Cleaning Agent]
    C1 --> C2[Data Agent]
    C2 --> C3[Baseline Agent]
    C3 --> C4[Outlier Detection Agent]
    C4 --> C5[Risk Profiling Agent]
    C5 --> C6[Report Agent]

    B5 --> D[Comparison]
    C6 --> D
    D --> E[Final conclusions]
```

---

## Dataset Description

The analysis uses two datasets provided by Whitehall Reply:

- `ALLARMI.csv`
- `TIPOLOGIA_VIAGGIATORE.csv`

The first dataset contains information related to alarms, routes, airports, years, months, and operational alarm categories.  
The second dataset contains traveller-type information, including route-level details and variables related to passenger categories, document types, inspection outcomes, and alert rates.

Both datasets required extensive preprocessing because they contained heterogeneous formats, textual inconsistencies, missing values, repeated categories, placeholder values, and non-standard representations of numerical and date-related fields.

The final route-level dataset used by the classical pipeline contains:

- **366 routes**
- **30 engineered numerical features**
- route identifiers based on departure and arrival airports
- alarm-related aggregated features
- traveller-related aggregated features
- alert-rate features
- nationality and document-type related indicators
- inspection outcome percentages

---

## [Section 2] Methods

## 2.1 Classical Pipeline

The Classical Pipeline was developed manually and follows a traditional machine learning workflow.

```mermaid
flowchart TD
    A[Load raw datasets] --> B[Initial exploratory analysis]
    B --> C[Column-by-column cleaning]
    C --> D[Standardization of strings and categories]
    D --> E[Date and numerical parsing]
    E --> F[Aggregation at route level]
    F --> G[Feature engineering]
    G --> H[Log transformation]
    H --> I[Standard scaling]
    I --> J[Anomaly detection models]
    J --> K[Consensus voting]
    K --> L[Risk classification]
    L --> M[Priority score and final report]
```

### Data Cleaning

The first part of the notebook performs a detailed cleaning process.  
The main operations include:

- conversion of string columns to lowercase;
- removal of leading and trailing whitespaces;
- normalization of inconsistent categorical values;
- mapping of semantically equivalent labels into common categories;
- parsing and standardization of year and month fields;
- conversion of noisy numerical fields into usable numeric types;
- removal or replacement of placeholder values such as missing, undefined, or non-informative tokens;
- harmonization of airport and country information;
- consistency checks between related columns.

This step is essential because anomaly detection is highly sensitive to data quality. Inconsistent values or wrongly parsed numerical fields may generate artificial anomalies.

---

### Route-Level Feature Engineering

The data was transformed into a route-level representation.  
Each row in the modeling dataset represents a route identified by:

- departure airport;
- arrival airport.

For each route, the pipeline computes aggregated features such as:

- total alarms closed;
- total generated alarms;
- total relevant alarms;
- total negative outcomes;
- total investigated travellers;
- total alerted travellers;
- total available flights;
- total investigated flights;
- total travellers entered into the system;
- alert rate;
- nationality-specific alert rates;
- document-type alert rates;
- percentages of different inspection outcomes.

The final modeling matrix contains **30 numerical features**.

---

### Transformation and Scaling

The engineered features are highly skewed and zero-inflated. Many routes have zero values for several alarm-related variables, while a few routes show much higher volumes.

To reduce the impact of extreme values, the Classical Pipeline applies:

```python
X_log = np.log1p(X)
```

This transformation compresses large values while preserving zero values.

After the logarithmic transformation, the features are scaled using:

```python
StandardScaler()
```

The resulting feature matrix has shape:

```text
(366, 30)
```

with mean approximately equal to 0 and standard deviation approximately equal to 1.

---

## 2.2 Baseline Construction

Since the available data is aggregated at route level and does not contain a sufficiently long time series, the pipeline builds a **cross-sectional baseline** across all routes.

The global distribution of each feature is used as the reference for identifying abnormal behavior.  
For example, the global baseline for `tasso_allarme` is:

| Statistic | Value |
|---|---:|
| Median alert rate | 0.1750 |
| 75th percentile | 0.2500 |
| 90th percentile | 0.4722 |
| 2× median threshold | 0.3501 |
| 3× median threshold | 0.5251 |

The 3× median threshold is later used during post-processing to identify high-risk routes based on alert rate.

---

## 2.3 Anomaly Detection Models

The Classical Pipeline applies three anomaly detection methods:

| Method | Type | Role in the pipeline |
|---|---|---|
| Isolation Forest | Tree-based unsupervised anomaly detection | Detects globally isolated observations |
| Local Outlier Factor | Density-based unsupervised anomaly detection | Detects locally sparse observations |
| Z-score | Statistical rule-based method | Detects feature-level extreme deviations |

### Isolation Forest

Isolation Forest was configured with:

```python
IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)
```

It detected:

```text
19 anomalous routes out of 366
```

corresponding to:

```text
5.2%
```

This is consistent with the chosen contamination value of 5%.

---

### Local Outlier Factor

Local Outlier Factor was configured with:

```python
LocalOutlierFactor(
    n_neighbors=20,
    contamination=0.05
)
```

It also detected:

```text
19 anomalous routes out of 366
```

corresponding to:

```text
5.2%
```

LOF differs from Isolation Forest because it compares each route with its local neighborhood. This makes it useful for detecting routes that are not globally extreme but are unusual compared with similar routes.

---

### Z-score

The Z-score method flags a route as anomalous if at least one feature has an absolute standardized value greater than 3:

```python
Z_THRESH = 3.0
```

It detected:

```text
137 anomalous routes out of 366
```

corresponding to:

```text
37.4%
```

This result shows that Z-score is much more sensitive than Isolation Forest and LOF.  
The features most frequently exceeding the threshold were:

| Feature | Routes exceeding threshold |
|---|---:|
| `alert_rate_permesso` | 17 |
| `alert_rate_visto` | 17 |
| `alert_rate_afg` | 17 |
| `alert_rate_passaporto` | 15 |
| `alert_rate_alb` | 15 |

The high number of Z-score flags suggests that using Z-score alone would generate too many alerts for practical operational use. For this reason, the final Classical Pipeline uses a consensus mechanism.

---

## 2.4 Consensus Strategy

Each model assigns a binary anomaly flag:

- `1` if the route is anomalous;
- `0` otherwise.

The final anomaly signal is based on the number of votes received by each route.

```mermaid
flowchart TD
    A[Route-level feature matrix] --> B[Isolation Forest]
    A --> C[Local Outlier Factor]
    A --> D[Z-score]

    B --> E[IF anomaly flag]
    C --> F[LOF anomaly flag]
    D --> G[Z-score anomaly flag]

    E --> H[Vote aggregation]
    F --> H
    G --> H

    H --> I{Votes >= 2?}
    I -- Yes --> J[Consensus anomaly]
    I -- No --> K[Non-final anomaly or normal route]
```

The vote distribution was:

| Votes | Number of routes | Interpretation |
|---:|---:|---|
| 0/3 | 216 | Normal routes |
| 1/3 | 126 | Weak anomaly signal |
| 2/3 | 23 | Probable anomaly |
| 3/3 | 1 | Strongest anomaly signal |

The consensus rule is:

```text
A route is a final anomaly if it receives at least 2 votes out of 3.
```

This produced:

```text
24 consensus anomalies
```

Compared with the 137 routes flagged by Z-score alone, the consensus strategy reduces the alert set to a more manageable and more reliable group of routes.

---

## 2.5 Post-Processing and Risk Classification

The raw anomaly flags are not sufficient for operational use.  
For this reason, the Classical Pipeline includes a post-processing phase that assigns risk levels and priority scores.

The risk classification uses:

- anomaly votes;
- alert rate;
- number of investigated travellers;
- absolute number of alarms;
- data quality notes;
- confidence intervals;
- business rules based on operational interpretability.

The risk levels are:

| Risk level | Meaning |
|---|---|
| CRITICAL | Flagged by all three methods |
| HIGH | High alert rate or strong operational signal |
| MEDIUM | Relevant signal, often driven by high volume |
| LOW | Weak or lower-priority signal |

The classification output contains:

| Risk level | Number of routes |
|---|---:|
| CRITICAL | 1 |
| HIGH | 10 |
| MEDIUM | 7 |
| LOW | 6 |

However, not all 24 consensus anomalies are equally reliable.  
The post-processing phase identifies:

- **3 likely false positives**, caused by features unrelated to alert rate;
- **2 incomplete-data routes**, where alert rate is present but supporting traveller records are missing;
- **5 high-alert-rate low-volume routes**, which require caution because the confidence interval is wide.

After excluding unreliable cases, the final report focuses on:

```text
19 reliable routes
```

---

## 2.6 Priority Score

A priority score is computed to rank the reliable anomalous routes.

The score combines:

- **60% alert rate**
- **40% logarithm of absolute alarms**

```text
priority_score = 0.60 * normalized_alert_rate
               + 0.40 * normalized_log_absolute_alarms
```

This score balances two different operational perspectives:

1. routes with very high alert rates;
2. routes with high absolute alarm volume.

A route with a very high alert rate but very low volume may be interesting, but it should be interpreted with caution.  
A route with a lower alert rate but very high volume may be operationally important because it generates more absolute alarms.

---

## 2.7 Multi-Agent Pipeline

The second part of the project implements a Multi-Agent Pipeline.  
The goal is to automate the workflow by assigning different responsibilities to specialized agents.

```mermaid
flowchart TD
    A[Raw CSV files] --> B[Cleaning Helpers]
    B --> C[Pre-Pipeline Column Profiling]
    C --> D[Cleaning Agent]
    D --> E[Data Agent]
    E --> F[Baseline Agent]
    F --> G[Outlier Detection Agent]
    G --> H[Risk Profiling Agent]
    H --> I[Report Agent]
    I --> J[Final Markdown Report]

    K[Supervisor] --> E
    K --> F
    K --> G
    K --> H
    K --> I

    L[Validators] --> K
```

The Multi-Agent Pipeline includes the following components:

### Cleaning Helpers

Reusable functions for:

- accent stripping;
- string normalization;
- missing-value detection;
- type inference;
- robust parsing of noisy values.

### Column Profiling

Before executing the pipeline, each dataset is profiled to understand:

- column names;
- dominant formats;
- missing values;
- likely semantic meaning of each field;
- sample values.

This profiling phase helps the agents reason about the structure of the input datasets.

### Code Executor

The Code Executor receives task instructions and generates executable Python code.  
It is constrained to return only executable Python code, without explanations or markdown.

### Validators

Each agent output is checked by deterministic validators.  
This is a key design choice because it reduces the risk of accepting invalid LLM-generated outputs.

The validators check whether:

- the expected output file exists;
- the file is loadable;
- required columns are present;
- the dataframe is not empty;
- the values satisfy basic consistency rules.

### Supervisor

The Supervisor orchestrates the execution of each agent.

For every task, it:

1. sends the task prompt to the Code Executor;
2. runs the generated code;
3. validates the output;
4. retries if execution or validation fails;
5. stores logs, generated code, validation results, and success status.

```mermaid
sequenceDiagram
    participant S as Supervisor
    participant A as Agent Prompt
    participant C as Code Executor
    participant V as Validator
    participant O as Output Artifact

    S->>A: Build task-specific prompt
    A->>C: Request executable Python code
    C->>O: Execute code & generate artifact

    S->>V: Validate artifact
    V-->>S: Passed / Failed

    alt Validation passed
        S->>S: Proceed to next agent
    else Validation failed
        S->>C: Retry with modified parameters
    end
```

---

## Multi-Agent Components

### Data Agent

The Data Agent filters the cleaned transit datasets based on a natural language query.

In the notebook, the example query is:

```text
mostrami le anomalie per i voli diretti a fiumicino
```

The agent:

- selects the most appropriate dataset;
- identifies the correct arrival-airport column;
- maps the query to the value `fiumicino`;
- filters records related to routes arriving at Fiumicino;
- focuses on alarm-related records;
- writes the result to `scoped_transit_data.csv`.

For the example query, the Data Agent selected the alarm dataset and produced:

```text
139 rows and 24 columns
```

---

### Baseline Agent

The Baseline Agent builds a route-level baseline from the scoped data.

It:

- loads `scoped_transit_data.csv`;
- identifies departure and arrival columns;
- builds a route feature;
- aggregates by route;
- computes total alarms;
- computes number of records;
- computes alert rate;
- computes baseline statistics;
- writes `baseline_data.csv`.

For the Fiumicino query, the Baseline Agent produced:

```text
46 routes and 6 columns
```

---

### Outlier Detection Agent

The Outlier Detection Agent loads the baseline data and computes anomaly signals.

It uses:

- `z_score`;
- `ratio_to_baseline`;
- a combined `anomaly_score`.

It then selects the top 5% most anomalous routes.

For the Fiumicino query, it produced:

```text
2 outliers
```

The detected routes were:

| Route | Total alarms | Records | Alert rate | Z-score | Anomaly score |
|---|---:|---:|---:|---:|---:|
| LGW → FCO | 11 | 11 | 1.0 | 2.9617 | 27.9617 |
| LHR → FCO | 11 | 11 | 1.0 | 2.9617 | 27.9617 |

---

### Risk Profiling Agent

The Risk Profiling Agent converts outliers into risk categories.

For the Fiumicino query, it classified both detected outliers as:

```text
LOW risk
```

This result is important because it shows that the Multi-Agent Pipeline separates **statistical anomaly detection** from **risk prioritization**.  
A route may be statistically unusual but still receive a low operational priority if the scoring logic does not identify it as severe.

---

### Report Agent

The Report Agent generates a final narrative report in markdown format.

The report includes:

- executive summary;
- risk distribution;
- top high-risk routes;
- other monitored routes;
- main anomaly drivers;
- interpretation of the results.

For the example query, the report summarized:

- 2 flagged routes;
- 0 HIGH risk routes;
- 0 MEDIUM risk routes;
- 2 LOW risk routes.

---

## [Section 3] Experimental Design

## Experiment 1 — Classical Pipeline Anomaly Detection

### Purpose

The purpose of this experiment is to evaluate whether a manually designed unsupervised pipeline can identify route-level anomalies from the available operational and traveller-related datasets.

### Baselines

The baseline is the global cross-sectional distribution of all 366 routes.

The anomaly detection methods compared are:

- Isolation Forest;
- Local Outlier Factor;
- Z-score.

### Metrics

Since no reliable ground truth labels are available, the evaluation focuses on unsupervised and operational metrics:

- number of flagged anomalies;
- percentage of flagged anomalies;
- agreement between methods;
- number of consensus anomalies;
- interpretability of flagged routes;
- operational usefulness after post-processing.

---

## Experiment 2 — Consensus Voting

### Purpose

The purpose of this experiment is to reduce false positives and obtain a more robust anomaly set by combining multiple anomaly detection signals.

### Baseline

The main comparison is against each single detector:

- Isolation Forest alone;
- LOF alone;
- Z-score alone.

### Evaluation Logic

A route is considered a final anomaly only if at least two out of three methods flag it.

This allows the pipeline to:

- preserve strong anomaly signals;
- reduce the noise introduced by overly sensitive methods;
- obtain a smaller and more actionable anomaly set.

---

## Experiment 3 — Risk Post-Processing

### Purpose

The purpose of this experiment is to transform raw anomaly flags into operational risk categories.

### Baseline

The baseline is the set of 24 consensus anomalies.

### Evaluation Logic

The post-processing step evaluates:

- alert rate;
- absolute alarms;
- investigated passenger volume;
- anomaly votes;
- confidence intervals;
- data quality notes.

The final output is a ranked set of reliable routes with a priority score.

---

## Experiment 4 — Multi-Agent Pipeline

### Purpose

The purpose of this experiment is to evaluate whether an agent-based system can reproduce parts of the anomaly detection workflow in a more automated and modular way.

### Baseline

The baseline is the Classical Pipeline.

### Evaluation Criteria

The Multi-Agent Pipeline is evaluated in terms of:

- ability to interpret a natural language query;
- ability to select and filter the correct dataset;
- ability to build a route-level baseline;
- ability to detect outliers;
- ability to assign risk levels;
- ability to generate a final textual report;
- robustness through deterministic validation.

---

# Results Section

## [Section 4] Results

This section reports and compares the results obtained from the two anomaly detection approaches developed in the project:

1. the **Classical Pipeline**, based on manually engineered features and multiple unsupervised anomaly detection methods;
2. the **Multi-Agent Pipeline**, based on automated data processing, route-level aggregation, baseline construction, anomaly scoring, risk profiling, and report generation.

The comparison is performed on the full dataset. This is important because earlier agentic experiments were query-driven and focused on a narrower operational scope. The current Multi-Agent results are instead based on the complete available data, making the comparison with the Classical Pipeline more meaningful.

---

## 4.1 Classical Pipeline Results

The Classical Pipeline analyzed:

```text
366 total routes
```

with:

```text
30 engineered numerical features
```

Each route represents a departure-arrival airport pair. The feature matrix was built through manual cleaning, aggregation, feature engineering, logarithmic transformation, and standard scaling.

The main goal of the Classical Pipeline was to identify route-level anomalies using multiple complementary detection methods. Three anomaly signals were computed:

- **Isolation Forest**, to identify routes that are globally isolated in the feature space;
- **Local Outlier Factor**, to identify routes that are unusual compared with their local neighborhood;
- **Z-score**, to identify feature-level extreme deviations.

The individual anomaly detectors produced the following results:

| Method | Anomalies detected | Percentage |
|---|---:|---:|
| Isolation Forest | 19 / 366 | 5.2% |
| Local Outlier Factor | 19 / 366 | 5.2% |
| Z-score | 137 / 366 | 37.4% |

The results show a clear difference in sensitivity between model-based detectors and the statistical Z-score rule.

Isolation Forest and Local Outlier Factor both detected 19 anomalous routes, which corresponds to approximately 5.2% of the dataset. This is consistent with the contamination parameter used during modeling and indicates that both methods behave conservatively.

The Z-score method, instead, detected 137 anomalous routes, corresponding to 37.4% of the dataset. This confirms that Z-score is much more sensitive, especially in a dataset where several features are sparse, skewed, and affected by low-volume route behavior.

```mermaid
xychart-beta
    title "Number of Detected Anomalies by Method"
    x-axis ["Isolation Forest", "LOF", "Z-score"]
    y-axis "Detected anomalies" 0 --> 150
    bar [19, 19, 137]
```

### Interpretation of Individual Detectors

The three detectors provide different perspectives on anomaly detection.

| Detector | Main behavior | Interpretation |
|---|---|---|
| Isolation Forest | Conservative | Captures routes that are globally isolated from the rest of the dataset |
| Local Outlier Factor | Conservative | Captures routes that are locally unusual compared with similar routes |
| Z-score | Highly sensitive | Captures individual feature deviations, including many weak or noisy signals |

The strong difference between Z-score and the other two methods indicates that many routes contain at least one extreme feature value, but not all of them are strong multivariate anomalies.

For this reason, the Classical Pipeline does not rely on a single detector. Instead, it combines the outputs through a consensus mechanism.

---

### Consensus Voting

Each detector assigns a binary anomaly flag to each route:

```text
1 = anomalous
0 = normal
```

The final anomaly score is based on the number of anomaly votes received by each route.

The vote distribution was:

| Number of votes | Routes | Interpretation |
|---:|---:|---|
| 0 | 216 | No anomaly signal |
| 1 | 126 | Weak anomaly signal |
| 2 | 23 | Probable anomaly |
| 3 | 1 | Strong anomaly signal |

```mermaid
xychart-beta
    title "Anomaly Vote Distribution"
    x-axis ["0 votes", "1 vote", "2 votes", "3 votes"]
    y-axis "Routes" 0 --> 230
    bar [216, 126, 23, 1]
```

The consensus rule was defined as:

```text
A route is considered a final anomaly if it receives at least 2 votes out of 3.
```

This produced:

```text
24 final consensus anomalies
```

The consensus approach reduced the anomaly set from:

```text
137 Z-score flags → 24 consensus anomalies
```

This reduction is one of the most important outcomes of the Classical Pipeline. It shows that combining multiple detectors helps reduce noise and avoids treating every feature-level deviation as an operationally relevant anomaly.

---

### Classical Pipeline Summary

| Result | Value |
|---|---:|
| Total routes analyzed | 366 |
| Engineered features | 30 |
| Isolation Forest anomalies | 19 |
| LOF anomalies | 19 |
| Z-score anomalies | 137 |
| Consensus anomalies | 24 |
| Consensus threshold | At least 2 out of 3 votes |

The Classical Pipeline therefore provides a broad but controlled anomaly detection framework. It captures many possible abnormal behaviors while using consensus voting to filter out weaker signals.

---

## 4.2 Risk Classification Results

The 24 consensus anomalies were further analyzed through a post-processing and risk classification step.

The objective of this phase was to transform raw anomaly flags into operationally interpretable risk levels. This is necessary because an anomaly detection model can identify statistically unusual routes, but statistical unusualness is not always equivalent to operational risk.

The post-processing step considered several factors:

- number of anomaly votes;
- alert rate;
- absolute number of alarms;
- number of investigated travellers;
- data completeness;
- confidence and reliability of the signal;
- possible low-volume effects;
- interpretability of the anomaly drivers.

The 24 consensus anomalies were classified as follows:

| Risk level | Routes |
|---|---:|
| CRITICAL | 1 |
| HIGH | 10 |
| MEDIUM | 7 |
| LOW | 6 |

```mermaid
pie title Risk Level Distribution among Consensus Anomalies
    "CRITICAL" : 1
    "HIGH" : 10
    "MEDIUM" : 7
    "LOW" : 6
```

The risk distribution shows that most consensus anomalies are not simply low-level statistical deviations. A large portion of the final anomaly set falls into the CRITICAL or HIGH categories, meaning that the consensus mechanism successfully preserves relevant routes while reducing the noise introduced by Z-score alone.

---

### Data-Quality Filtering

After assigning risk levels, the Classical Pipeline applied an additional reliability filter.

After data-quality filtering:

```text
19 reliable routes
```

were retained for the final operational report.

The post-processing step excluded or marked with caution the following cases:

| Issue type | Routes |
|---|---:|
| Likely false positives | 3 |
| Incomplete data | 2 |
| High rate but very low volume | 5 |

These categories are important because anomaly detection on operational data is sensitive to both volume and data quality.

A route may appear anomalous because it has a very high alert rate, but if the number of observations is very small, the estimate may be unstable. Similarly, routes with incomplete supporting information may be statistically interesting but less reliable for operational decision-making.

---

### Risk Classification Interpretation

The risk classification adds an operational layer on top of the statistical anomaly detection layer.

| Risk level | Meaning |
|---|---|
| CRITICAL | Strongest anomaly signal, usually supported by all detectors or extreme operational indicators |
| HIGH | Strong anomaly signal with relevant operational evidence |
| MEDIUM | Meaningful deviation, often linked to volume or partial anomaly evidence |
| LOW | Weak or lower-priority signal, useful mainly for monitoring |

This step makes the final output more usable because it separates routes that require immediate attention from routes that should simply be monitored.

---

## 4.3 Main Classical Pipeline Findings

The Classical Pipeline produced several important findings.

### 1. Z-score is highly sensitive

The Z-score method detected:

```text
137 anomalous routes
```

This is much higher than the number of anomalies detected by Isolation Forest and Local Outlier Factor.

This behavior is expected because Z-score flags a route when at least one feature exceeds a statistical threshold. In a dataset with 30 features, sparse values, and skewed route distributions, many routes may exceed the threshold for at least one variable.

As a result, Z-score is useful for identifying feature-level deviations, but it is too sensitive to be used alone for final operational decisions.

---

### 2. Isolation Forest and LOF are more selective

Both Isolation Forest and Local Outlier Factor detected:

```text
19 anomalous routes
```

This indicates that the two model-based methods are more conservative.

Isolation Forest focuses on global isolation, while LOF focuses on local density differences. Their similar anomaly counts suggest that both methods identify a small set of routes that are structurally different from the majority of the dataset.

---

### 3. Consensus voting improves reliability

The consensus strategy produced:

```text
24 final anomalies
```

This final set is much smaller than the Z-score output and more interpretable than any single-detector result.

Consensus voting improves reliability because a route must be confirmed by at least two independent anomaly signals before being selected as a final anomaly.

---

### 4. Risk post-processing is necessary

The Classical Pipeline shows that raw anomaly flags are not sufficient.

A route may be statistically anomalous for several reasons:

- high alert rate;
- high absolute alarm volume;
- rare feature pattern;
- low data volume;
- incomplete supporting records;
- isolated but operationally weak signal.

For this reason, post-processing is essential to distinguish between statistical anomalies and operationally relevant anomalies.

---

### 5. High alert rate does not always mean high reliability

Some routes have very high alert rates but very low investigated volume.

In these cases, the alert rate may be unstable because it is calculated on a small number of observations. These routes should not automatically be treated as high-risk without further validation.

---

### 6. High-volume routes can be operationally important even with moderate rates

Some medium-risk routes may not have the highest alert rate, but they may generate a large number of absolute alarms.

From an operational perspective, these routes can be important because they may consume more resources or indicate repeated patterns across many observations.

---

### Classical Pipeline Final Assessment

Overall, the Classical Pipeline is strong in terms of:

- methodological rigor;
- feature richness;
- transparency;
- interpretability;
- robustness through consensus;
- ability to detect both strong and subtle anomalies.

Its main limitation is that it requires significant manual effort and careful post-processing.

---

## 4.4 Multi-Agent Pipeline Results

The Multi-Agent Pipeline was executed on the **full dataset**, ensuring that its results can be compared with the Classical Pipeline on the same overall scope.

The objective of the Multi-Agent Pipeline is different from the Classical Pipeline. Instead of manually defining every step of the workflow, the Multi-Agent system automates the main phases of the anomaly detection process through specialized agents.

The workflow includes:

| Step | Description |
|---|---|
| Data Agent | Selects, filters, and structures relevant alarm-related and traveller-related records |
| Baseline Agent | Builds route-level aggregates and computes population-level baseline statistics |
| Outlier Detection Agent | Computes anomaly signals such as z-score, ratio-to-baseline, and anomaly score |
| Risk Profiling Agent | Assigns risk levels based on anomaly severity and ranking |
| Report Agent | Generates the final anomaly detection report in markdown format |

The updated Multi-Agent Pipeline identified:

```text
11 anomalous route-level groups
```

The risk distribution was:

| Risk level | Routes |
|---|---:|
| HIGH | 2 |
| MEDIUM | 2 |
| LOW | 7 |

```mermaid
pie title Multi-Agent Risk Distribution
    "HIGH" : 2
    "MEDIUM" : 2
    "LOW" : 7
```

The 11 anomalies were selected using a population-level baseline, z-score normalization, ratio-to-baseline comparison, and hybrid filtering logic combining top-ranked deviations with a confidence floor.

---

### Multi-Agent High-Risk Routes

The Multi-Agent Pipeline identified 2 high-risk routes.

| Route | Events | Baseline mean | Z-score | Ratio to baseline | Anomaly score | Risk score |
|---|---:|---:|---:|---:|---:|---:|
| TIA → BGY | 25,936 | 88 | 9.51 | 294.00x | 302.51 | 100.0 |
| TIA → BLQ | 30,750 | 134 | 11.31 | 228.00x | 238.31 | 71.8 |

These routes show the strongest deviations from the population baseline.

The route **TIA → BGY** shows an extremely high ratio to baseline, with 25,936 events compared with an average baseline of 88. This corresponds to a 294-fold increase over the baseline and receives the highest risk score.

The route **TIA → BLQ** records 30,750 events against a baseline mean of 134. Although its ratio is lower than TIA → BGY, its z-score is higher, confirming a very strong statistical deviation.

These two routes should be prioritized for operational review because they combine high event volume, high ratio-to-baseline values, and strong z-score signals.

---

### Multi-Agent Medium-Risk Routes

The Multi-Agent Pipeline identified 2 medium-risk routes.

| Route | Events | Baseline mean | Z-score | Ratio to baseline | Anomaly score | Risk score |
|---|---:|---:|---:|---:|---:|---:|
| TIA → FCO | 14,655 | 66 | 5.30 | 222.00x | 226.30 | 66.5 |
| TIA → TSF | 12,993 | 76 | 4.68 | 170.00x | 173.68 | 43.4 |

These routes show strong deviations from baseline but are ranked below the high-risk routes.

The route **TIA → FCO** is especially relevant because it combines a high ratio-to-baseline value with a strong z-score. It does not reach the highest risk category but remains operationally important.

The route **TIA → TSF** also presents a significant deviation, with 12,993 events against a baseline mean of 76. Its risk score is lower, but the route still deserves monitoring and potential follow-up.

---

### Multi-Agent Low-Risk Routes

The Multi-Agent Pipeline identified 7 low-risk routes.

| Route | Events | Baseline mean | Z-score | Ratio to baseline | Anomaly score | Risk score |
|---|---:|---:|---:|---:|---:|---:|
| TIA → CTA | 4,577 | 34 | 1.54 | 132.00x | 132.54 | 25.3 |
| TIA → BRI | 5,725 | 47 | 1.97 | 120.00x | 120.97 | 20.2 |
| STN → BGY | 10,160 | 97 | 3.62 | 104.00x | 106.62 | 13.9 |
| LHR → LIN | 13,131 | 135 | 1.59 | 97.00x | 97.59 | 10.0 |
| LGW → MXP | 103,254 | 1,214 | 13.52 | 85.00x | 97.52 | 9.9 |
| TIA → TRN | 8,599 | 107 | 3.04 | 80.00x | 82.04 | 3.1 |
| TIA → GOA | 5,515 | 74 | 1.89 | 74.00x | 74.89 | 0.0 |

These routes are not ignored, but they are not assigned immediate high-priority status.

Some low-risk routes show large absolute volumes or high ratios, but their final risk scores are lower because the risk profiling logic considers multiple factors, including relative ranking and severity thresholds.

For example, **LGW → MXP** has the largest absolute event count among the low-risk routes and a very high z-score. However, its ratio-to-baseline and final risk score place it below the more critical TIA-related deviations.

This illustrates how the Multi-Agent Pipeline separates statistical anomaly strength from operational prioritization.

---

### Multi-Agent Pipeline Summary

| Result | Value |
|---|---:|
| Total anomalies detected | 11 |
| High-risk routes | 2 |
| Medium-risk routes | 2 |
| Low-risk routes | 7 |
| Main detection signals | Z-score, ratio-to-baseline, anomaly score |
| Main selection logic | Hybrid top-K ranking and confidence floor |

The Multi-Agent Pipeline is more selective than the Classical Pipeline. It focuses on the most extreme baseline deviations and produces a compact set of routes for review.

---

## 4.5 Classical vs Multi-Agent Comparison

The two pipelines are now compared on the same overall dataset scope.

| Dimension | Classical Pipeline | Multi-Agent Pipeline |
|---|---|---|
| Scope | Full dataset | Full dataset |
| Total routes / groups analyzed | 366 routes | Full route-level groups |
| Feature representation | 30 engineered numerical features | Aggregated volume-based route metrics |
| Detection methods | Isolation Forest, LOF, Z-score | Z-score, ratio-to-baseline, anomaly score |
| Selection strategy | Consensus voting | Hybrid filtering and ranking |
| Raw anomaly sensitivity | High due to Z-score | Lower due to filtering |
| Final anomaly set | 24 consensus anomalies | 11 selected anomalies |
| Risk profiling | Detailed post-processing | Automated risk assignment |
| Interpretability | High | High |
| Automation | Lower | Higher |
| Manual effort | High | Lower once configured |
| Robustness | Strong due to consensus | Stronger if validators and thresholds are well designed |
| Main strength | Broad and robust anomaly discovery | Selective and operationally focused detection |
| Main weakness | Time-consuming and manually designed | Lower coverage of subtle multivariate anomalies |

---

### Quantitative Comparison

| Metric | Classical Pipeline | Multi-Agent Pipeline |
|---|---:|---:|
| Total routes analyzed | 366 | Full dataset |
| Raw statistical anomalies | 137 | 11 |
| Final anomalies | 24 | 11 |
| High / Critical risk routes | 11 | 2 |
| Medium risk routes | 7 | 2 |
| Low risk routes | 6 | 7 |

The Classical Pipeline identifies more anomalies overall. This is expected because it uses multiple detection methods and a richer feature space.

The Multi-Agent Pipeline identifies fewer anomalies because it applies stricter filtering and focuses on the most extreme deviations from baseline.

---

### Risk Distribution Comparison

| Risk level | Classical Pipeline | Multi-Agent Pipeline |
|---|---:|---:|
| CRITICAL | 1 | 0 |
| HIGH | 10 | 2 |
| MEDIUM | 7 | 2 |
| LOW | 6 | 7 |
| Total | 24 | 11 |

```mermaid
xychart-beta
    title "Final Anomalies by Risk Level"
    x-axis ["Critical", "High", "Medium", "Low"]
    y-axis "Routes" 0 --> 12
    bar [1, 10, 7, 6]
```

```mermaid
xychart-beta
    title "Multi-Agent Anomalies by Risk Level"
    x-axis ["High", "Medium", "Low"]
    y-axis "Routes" 0 --> 8
    bar [2, 2, 7]
```

The Classical Pipeline has a broader distribution across the higher risk classes, while the Multi-Agent Pipeline concentrates most detected routes in the low-risk category.

This suggests that the Multi-Agent system is not simply replicating the Classical Pipeline. It is applying a different selection strategy that emphasizes extreme deviations but then prioritizes only a small subset as high or medium risk.

---

### Detection Behavior Comparison

The Classical Pipeline captures several types of anomalies:

- routes that are globally isolated in the full feature space;
- routes that are locally unusual compared with similar routes;
- routes with extreme feature-level values;
- routes supported by multiple independent anomaly signals.

The Multi-Agent Pipeline mainly captures:

- extreme deviations from a population-level baseline;
- unusually high event volumes;
- high ratio-to-baseline values;
- strongly ranked route-level outliers.

This means that the Classical Pipeline is more suitable for discovering a wide anomaly space, while the Multi-Agent Pipeline is more suitable for producing a concise operational alert list.

---

### Coverage vs Selectivity

The two approaches reflect a trade-off between coverage and selectivity.

| Objective | Better suited pipeline | Reason |
|---|---|---|
| Discover many possible anomalies | Classical Pipeline | Uses multiple detectors and richer features |
| Reduce alert fatigue | Multi-Agent Pipeline | Produces a smaller anomaly set |
| Capture multivariate patterns | Classical Pipeline | Uses 30 engineered features |
| Automate repeated analysis | Multi-Agent Pipeline | Agentic workflow can generate outputs automatically |
| Explain final risk levels | Both | Both include risk interpretation, but with different logic |
| Operational triage | Multi-Agent Pipeline | Focuses on fewer, ranked deviations |
| Methodological validation | Classical Pipeline | More controlled and transparent |

---

## 4.6 Interpretation of the Comparison

The comparison shows that the Classical Pipeline and the Multi-Agent Pipeline are not interchangeable. They are complementary tools designed around different priorities.

The Classical Pipeline is designed for analytical completeness. It builds a rich feature matrix, applies multiple anomaly detectors, and uses consensus voting to identify robust final anomalies. This makes it strong for methodological validation and for discovering subtle patterns that may not be visible through simple aggregate metrics.

The Multi-Agent Pipeline is designed for automation and operational usability. It processes the data through specialized agents, computes baseline deviations, ranks anomalous route groups, assigns risk levels, and generates a structured report. This makes it strong for repeatable monitoring and rapid anomaly review.

---

### Main Interpretation

The Classical Pipeline detected:

```text
24 final consensus anomalies
```

The Multi-Agent Pipeline detected:

```text
11 anomalous route-level groups
```

This difference should not be interpreted as a contradiction. It reflects a methodological difference.

The Classical Pipeline has broader coverage because it combines different types of anomaly detection signals.

The Multi-Agent Pipeline is more selective because it focuses on the most extreme deviations according to its baseline and ranking logic.

---

### Practical Meaning

From a practical perspective:

- the Classical Pipeline is better when the goal is to understand the full anomaly landscape;
- the Multi-Agent Pipeline is better when the goal is to produce a short and actionable list of suspicious routes;
- the Classical Pipeline is more suitable for research and validation;
- the Multi-Agent Pipeline is more suitable for automation and operational monitoring.

---

### Strengths of the Classical Pipeline

The main strengths of the Classical Pipeline are:

- rich feature engineering;
- multiple anomaly detection perspectives;
- consensus-based robustness;
- transparent manual design;
- detailed post-processing;
- better coverage of subtle anomaly patterns.

Its main weakness is that it requires more manual effort and is less immediately reusable for interactive analysis.

---

### Strengths of the Multi-Agent Pipeline

The main strengths of the Multi-Agent Pipeline are:

- automated execution;
- modular agent-based structure;
- compact anomaly output;
- strong interpretability of baseline deviations;
- lower manual effort once configured;
- suitability for repeated operational use.

Its main weakness is that it may miss subtle multivariate anomalies that are not expressed as extreme aggregate deviations.

---

### Final Interpretation

The most important conclusion is that the two approaches should be combined rather than treated as alternatives.

A strong future version of the system would use:

- the feature richness of the Classical Pipeline;
- the consensus voting logic of the Classical Pipeline;
- the automation and modularity of the Multi-Agent Pipeline;
- the reporting capabilities of the Multi-Agent Pipeline.

This would allow the system to preserve methodological rigor while becoming more scalable, automated, and operationally useful.

---

### Final Takeaway

The final takeaway is:

```text
Classical Pipeline = coverage, rigor, and robustness
Multi-Agent Pipeline = selectivity, automation, and operational usability
```

The Classical Pipeline is the stronger tool for discovering and validating anomalies.

The Multi-Agent Pipeline is the stronger tool for automating anomaly detection and generating concise operational reports.

Together, they provide a complete framework for route-level anomaly detection on airport transit data.



## [Section 5] Conclusions

This project shows that anomaly detection on airport transit data requires both statistical modeling and careful post-processing. The Classical Pipeline demonstrates that different anomaly detection methods can produce very different levels of sensitivity: Isolation Forest and LOF detect a small and controlled set of anomalies, while Z-score identifies many more feature-level deviations. The consensus strategy provides a practical compromise by selecting only routes flagged by at least two methods, reducing the anomaly set from 137 Z-score flags to 24 consensus anomalies. After additional data-quality filtering, 19 reliable routes are retained for operational interpretation.

The Multi-Agent Pipeline demonstrates that the same type of workflow can be partially automated through specialized agents, deterministic validators, and a supervisor mechanism. The agentic system can interpret a natural language query, filter the relevant data, build a route-level baseline, detect outliers, assign risk categories, and generate a narrative report. This makes the approach promising for interactive analysis and repeated operational use.

Overall, the main takeaway is that the Classical Pipeline offers greater methodological control and interpretability, while the Multi-Agent Pipeline offers greater modularity and automation. A strong future direction would be to combine the two approaches: use the robust feature engineering and consensus logic of the Classical Pipeline inside the automated structure of the Multi-Agent Pipeline.

---

## Limitations and Future Work

The main limitations of the project are:

- the absence of a reliable ground-truth label for anomalies;
- the limited temporal window available in the data;
- the need to rely on unsupervised evaluation criteria;
- the sensitivity of some results to low-volume routes;
- the possibility of false positives caused by rare but not necessarily risky feature patterns;
- the current difference in scope between the full Classical Pipeline and the query-driven Multi-Agent Pipeline.

Future work could include:

- collecting a longer historical time window;
- introducing time-series baselines and seasonal decomposition;
- validating detected anomalies with domain experts;
- adding supervised labels if confirmed anomaly cases become available;
- integrating the Classical Pipeline's consensus logic into the Multi-Agent Pipeline;
- improving the Risk Profiling Agent with confidence intervals and data-quality flags;
- extending the Gradio interface for interactive exploration;
- generating all final README figures automatically from the notebook.

---

## Repository Structure

```text
.
├── main.ipynb
├── README.md
├── data/
│   └── raw/
│       ├── ALLARMI.csv
│       └── TIPOLOGIA_VIAGGIATORE.csv
├── output/
│   ├── scoped_transit_data.csv
│   ├── baseline_data.csv
│   ├── outliers.csv
│   ├── risk_report.csv
│   └── transit_anomaly_report.md
└── requirements.txt
```

---

## Reproducibility

To reproduce the project:

1. Clone the repository.
2. Place the raw datasets in `data/raw/`.
3. Install the required dependencies.
4. Run `main.ipynb` from top to bottom.
5. Ensure that all generated figures are saved in the `images/` folder.
6. Verify that the output artifacts are created correctly.

Example installation:

```bash
pip install -r requirements.txt
```

# API Key

This project requires a Mistral API key to run the Multi-Agent Pipeline.

For the purpose of evaluation, the API key is provided below:

```bash
MISTRAL_API_KEY=6H9hgqBwYfQSjKp37F5zr1TWnyMTYitV
```

To use it locally, set it as an environment variable:

```bash
export MISTRAL_API_KEY=6H9hgqBwYfQSjKp37F5zr1TWnyMTYitV
```



Main Python libraries used:

- `pandas`
- `numpy`
- `scipy`
- `scikit-learn`
- `matplotlib`
- `seaborn`
- `gradio`
- `python-dotenv`
- `openai`

---

## Notes on Academic Integrity