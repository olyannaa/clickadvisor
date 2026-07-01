# Risk Error Analysis

- Model: `random_forest_all_features`
- Split: `holdout`
- Holdout records: 3039

## Slice Metrics

| Slice | Records | Macro-F1 | MCC | High precision | High recall | High F1 |
|---|---:|---:|---:|---:|---:|---:|
| all_holdout | 3039 | 0.949 | 0.945 | 0.869 | 0.887 | 0.878 |
| rule_only | 2235 | 0.970 | 0.980 | 0.860 | 0.990 | 0.920 |
| measured_only | 672 | 0.595 | 0.748 | 0.880 | 0.785 | 0.830 |
| both | 132 | 0.975 | 0.939 | 0.875 | 1.000 | 0.933 |
| both_high_core | 14 | 0.333 | 0.000 | 1.000 | 1.000 | 1.000 |

## High False Negatives

- Records: 27
- `by_label_source`: measured_only=26, rule_only=1
- `by_source`: clickhouse_functional_tests=21, clickadvisor_benchmark=2, clickbench=1, job=1, clickhouse_performance_tests=1, expert_synthetic_antipatterns=1
- `by_family`: clickhouse_stateless=21, olap_flat_web_analytics=2, synthetic=2, join_order_benchmark=1, clickhouse_perf_xml=1
- `by_rule_risk_label`: medium=22, low=4, high=1
- `by_measured_risk_label`: high=26, None=1
- `by_predicted_label`: medium=25, low=2

## High False Positives

- Records: 32
- `by_label_source`: rule_only=17, measured_only=13, both=2
- `by_source`: clickhouse_functional_tests=25, clickhouse_performance_tests=4, expert_synthetic_antipatterns=2, clickadvisor_benchmark=1
- `by_family`: clickhouse_stateless=25, clickhouse_perf_xml=5, synthetic=1, olap_flat_web_analytics=1
- `by_rule_risk_label`: medium=17, low=15
- `by_measured_risk_label`: None=16, medium=15, low=1
- `by_predicted_label`: high=32

## Label Source Error Breakdown

- `both`: records=132, errors=2, error_rate=0.015, high_fn=0, high_fp=2
- `measured_only`: records=672, errors=51, error_rate=0.076, high_fn=26, high_fp=13
- `rule_only`: records=2235, errors=21, error_rate=0.009, high_fn=1, high_fp=17

## Top Rules in High FN

- `D-004`: 19
- `<no_rule>`: 4
- `D-003`: 4
- `D-005`: 2
- `R-102`: 2
- `R-020`: 2
- `R-009`: 1
- `R-008`: 1
- `R-042`: 1
- `D-007`: 1

## Top Rules in High FP

- `<no_rule>`: 13
- `D-004`: 12
- `D-012`: 3
- `R-016`: 2
- `D-003`: 2
- `D-013`: 2
- `R-038`: 1
- `R-008`: 1
- `R-020`: 1
- `R-014`: 1
- `D-007`: 1

## Interpretation

- Measured-only holdout macro-F1 is 0.595. This is the key check for whether the model generalizes beyond direct rule-derived labels.
- Both-source holdout macro-F1 is 0.975. This slice is the most reliable core because rule and measured signals agree.
- High false negatives: 27. These are the highest product-risk misses and should be inspected before changing thresholds or model choice.
- High false positives: 32. These show where risk-like features over-prioritize queries whose final label is low or medium.
- Production runtime should remain rule-first. ML is useful for triage, prioritization, and review queues, not as a source of deterministic recommendations.
