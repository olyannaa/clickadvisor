# Risk Labeling DS Report

## Dataset State

- Records: 20 235
- Final labels: `low` 4 253, `medium` 14 285, `high` 1 697
- Measured-ok records: 9 837
- Feature rows: 20 235
- Numeric feature count: 115
- Rule-id vocabulary: 54
- Split: group-aware `train` 14 155, `test` 3 041, `holdout` 3 039

## Critical Methodology Note

`label_source` is strongly skewed:

- `rule_only`: 14 693, about 73%
- `measured_only`: 4 635, about 23%
- `both`: 907, about 4%

This means the ML task is not an independent replacement for ClickAdvisor's
deterministic rule engine. The model mostly learns a compressed triage layer
over rule-engine decisions, with an additional measured-metric signal from local
ClickHouse replay.

That is still useful: the model can rank, triage, and generalize rough risk
signals. It should not become the source of production recommendations. Runtime
recommendations must continue to come from deterministic rules with explicit
`rule_id`, tier, severity, and explanation.

The `both` subset is the highest-confidence analysis core: these 907 records are
confirmed by both static rule findings and measured replay thresholds. Use this
subset first for high-class error analysis and examples.

## Measured Thresholds

The measured signal is based on successful local replay records only. Latency
and memory are heavy-tailed, so `memory_usage` uses non-zero P90 rather than the
all-record P90, which is zero.

- `low`: `read_rows <= 1` and `query_duration_ms <= 0`
- `high`: `read_rows > 10` or `query_duration_ms > 1` or `memory_usage > 46674914`
- `medium`: ok records between low and high thresholds
- non-ok measured records use rule-only final labels

## Feature Groups

SQL text:

- normalized SQL with literals replaced
- character length
- token length
- TF-IDF tokens and bigrams are fitted inside baseline runs

Structural:

- `has_select_star`, `has_final`, `has_limit`, `has_prewhere`
- `has_order_by`, `has_group_by_high_card`
- `join_count`, `subquery_count`, `function_on_filter`
- `distinct_count`, `aggregation_count`
- existing AST/text features from `clickadvisor.ml.features.QueryFeatureExtractor`

Rule-derived:

- `rule_findings_count`
- `rule_max_severity`
- `rule_max_tier`
- binary presence of each observed `rule_id`

## Split Strategy

The split is created before model training and prevents near-duplicate leakage
by grouping on:

`source::family::origin.parent_sql_hash_or_sql_hash`

Outer split:

- train: 14 155 records
- test: 3 041 records
- holdout: 3 039 records

Group leakage:

- train/test overlap: 0
- train/holdout overlap: 0
- test/holdout overlap: 0

Validation:

- 5-fold `StratifiedGroupKFold` inside train
- stratification target: `final_risk_label`
- group key: same source/family/parent hash key

## Baseline Ladder

Artifacts:

- `eval/results/risk_baseline_ladder_current/metrics.json`
- `eval/results/risk_baseline_ladder_current/metrics.csv`
- `eval/results/risk_baseline_ladder_current/summary.md`

| Model | CV macro-F1 | Test macro-F1 | Holdout macro-F1 | Test high recall | Holdout high recall |
|---|---:|---:|---:|---:|---:|
| dummy_most_frequent | 0.275 +/- 0.000 | 0.276 | 0.278 | 0.000 | 0.000 |
| dummy_stratified | 0.328 +/- 0.009 | 0.342 | 0.335 | 0.104 | 0.062 |
| tfidf_logistic_regression | 0.864 +/- 0.011 | 0.869 | 0.882 | 0.869 | 0.912 |
| structured_rule_logistic_regression | 0.827 +/- 0.004 | 0.822 | 0.837 | 0.656 | 0.696 |
| random_forest_all_features | 0.938 +/- 0.006 | 0.938 | 0.949 | 0.846 | 0.887 |
| catboost_tabular | 0.873 +/- 0.008 | 0.871 | 0.871 | 0.788 | 0.804 |

## Interpretation

The gap between dummy baselines and learned models confirms that the labels have
learnable structure. The strong random-forest result is expected because the
feature matrix includes rule-derived signals, including binary rule presence.
This is useful for triage but also confirms the methodology note above: the ML
surface is learning a compact model of current labeling logic, not discovering a
fully independent risk oracle.

The next useful work is not to chase a larger headline score. The next useful
work is high-class error analysis:

- inspect false negatives for `high`
- inspect false positives from measured-only labels
- evaluate the `both` subset separately as the reliable high-risk core
- consider a companion binary task: `high` vs `low/medium`
- keep class weighting enabled in future baselines

## Holdout Error Analysis

Artifacts:

- `data/ml/expert_dataset/eda/risk_error_analysis/error_analysis.json`
- `data/ml/expert_dataset/eda/risk_error_analysis/error_analysis.md`
- `data/ml/expert_dataset/eda/risk_error_analysis/holdout_predictions.csv`

The error analysis retrains `random_forest_all_features` on the train split and
evaluates only on holdout.

| Slice | Records | Macro-F1 | MCC | High precision | High recall | High F1 |
|---|---:|---:|---:|---:|---:|---:|
| all_holdout | 3 039 | 0.949 | 0.945 | 0.869 | 0.887 | 0.878 |
| rule_only | 2 235 | 0.970 | 0.980 | 0.860 | 0.990 | 0.920 |
| measured_only | 672 | 0.595 | 0.748 | 0.880 | 0.785 | 0.830 |
| both | 132 | 0.975 | 0.939 | 0.875 | 1.000 | 0.933 |
| both_high_core | 14 | 0.333 | 0.000 | 1.000 | 1.000 | 1.000 |

The key sanity check is `measured_only`: macro-F1 drops to 0.595. This confirms
that the 0.949 all-holdout score is partly driven by rule-derived features
learning the current rule-label mapping. That is an expected and useful result,
but it must be interpreted as triage quality rather than independent risk
discovery.

The `both` subset behaves differently: macro-F1 is 0.975, and high recall is
1.000. This supports the core thesis that the model is most reliable where
static rules and measured replay agree.

High false negatives:

- Records: 27
- By label source: `measured_only` 26, `rule_only` 1
- By measured label: `high` 26, `None` 1
- Predicted as: `medium` 25, `low` 2
- Top rules/no-rule markers: `D-004` 19, `<no_rule>` 4, `D-003` 4

These are the highest product-risk misses. Almost all of them are measured-only
high records, so the rule engine did not provide a strong enough high-risk
signal for the model to inherit.

High false positives:

- Records: 32
- By label source: `rule_only` 17, `measured_only` 13, `both` 2
- By measured label: `None` 16, `medium` 15, `low` 1
- Top rules/no-rule markers: `<no_rule>` 13, `D-004` 12, `D-012` 3

These show where risk-like structural/text patterns over-prioritize records
whose final label is low or medium, including records with no successful
measured replay.

Rule-family breakdown on holdout errors:

- detectors: 40 errors, including 22 high FN and 18 high FP
- no-rule records: 32 errors, including 4 high FN and 13 high FP
- rewrite rules: 10 errors, including 5 high FN and 5 high FP

Operational conclusion: production runtime should remain rule-first. The ML
layer adds value as prioritization, review queue ordering, confidence grouping,
and high-risk triage. It should not generate production recommendations without
the deterministic rule engine and explicit rule explanations.
