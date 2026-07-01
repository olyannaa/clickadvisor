# Risk Labeling DS Summary

This experiment evaluates whether SQL text, AST/structural features,
rule-derived features, and measured replay metrics can predict a coarse
`low` / `medium` / `high` risk label for triage.

It does not replace the deterministic rule engine.

## Dataset

- Records: 20 235
- Final labels: `low` 4 253, `medium` 14 285, `high` 1 697
- Measured-ok records: 9 837
- Feature rows: 20 235
- Numeric features: 115
- Rule-id vocabulary: 54
- Split: group-aware train/test/holdout

Artifacts:

- `data/ml/expert_dataset/queries.jsonl`
- `data/ml/expert_dataset/features/features.jsonl`
- `data/ml/expert_dataset/splits/risk_split_v1.json`
- `data/ml/expert_dataset/eda/ds_report.md`

## Dataset Composition and Limitations

This is a diverse ClickHouse query corpus with replay- and rule-derived weak
risk labels. It is not a DBA-adjudicated production incident dataset.

| Source | Records | Why it is useful | Limitation |
|---|---:|---|---|
| `clickhouse_functional_tests` / `clickhouse_stateless` | 16 845 | Broad SQL grammar, functions, joins, subqueries, edge cases | Functional tests are not real user workloads |
| `clickhouse_performance_tests` | 1 825 | Performance-oriented upstream workload material | Still benchmark/test data, not customer query logs |
| `expert_synthetic_antipatterns` | 1 145 | Explicit anti-patterns and product scenarios | Synthetic by design |
| Other benchmark/project sources | 420 | ClickBench, TPCH/TPCDS, JOB, rule benchmark, bug reproducers | Smaller slices with different semantics |

All 20 235 records use
`label_method = benchmark_expected_rules_plus_feature_weak_labels_v1`. The
labels combine static rule findings with percentile-based measured metrics from
local ClickHouse replay where execution succeeded. This is a valid DS setup for
triage and prioritization research, but the labels should be treated as weak
supervision, not as absolute ground truth.

## Label Sources

`label_source` is the most important methodological fact:

- `rule_only`: 14 693, about 73%
- `measured_only`: 4 635, about 23%
- `both`: 907, about 4%

The ML model mostly learns a compact triage approximation of the rule engine
plus an additional measured-metric signal. This is useful for prioritization and
review queues, but it is not an independent optimizer.

The `both` subset is the most reliable analysis core because static rules and
measured replay agree.

## Baseline Ladder

| Model | CV macro-F1 | Test macro-F1 | Holdout macro-F1 |
|---|---:|---:|---:|
| dummy_most_frequent | 0.275 +/- 0.000 | 0.276 | 0.278 |
| dummy_stratified | 0.328 +/- 0.009 | 0.342 | 0.335 |
| tfidf_logistic_regression | 0.864 +/- 0.011 | 0.869 | 0.882 |
| structured_rule_logistic_regression | 0.827 +/- 0.004 | 0.822 | 0.837 |
| random_forest_all_features | 0.938 +/- 0.006 | 0.938 | 0.949 |
| catboost_tabular | 0.873 +/- 0.008 | 0.871 | 0.871 |

## Holdout Error Analysis

Random Forest has the best overall holdout macro-F1, but the slices tell the
real story:

| Slice | Records | Macro-F1 | High recall |
|---|---:|---:|---:|
| all_holdout | 3 039 | 0.949 | 0.887 |
| rule_only | 2 235 | 0.970 | 0.990 |
| measured_only | 672 | 0.595 | 0.785 |
| both | 132 | 0.975 | 1.000 |

The `measured_only` drop confirms that the headline score is partly driven by
rule-derived features. The `both` result confirms that the model is strongest
where both sources agree.

High-class errors are concentrated in the weaker label-source slices:

- High false negatives: `27`; `26` are `measured_only`.
- High false positives: `32`; `17` are `rule_only` and `13` are
  `measured_only`.
- `both` has only `2` errors over `132` holdout records and `1.000` high recall.

## Learning Curve

The Random Forest risk model was retrained on increasing fractions of the
group-aware train split and evaluated on the same fixed holdout split:

| Train fraction | Train records | Train macro-F1 | Holdout macro-F1 | Holdout high recall |
|---:|---:|---:|---:|---:|
| 0.10 | 1 415 | 0.978 | 0.893 | 0.675 |
| 0.25 | 3 539 | 0.963 | 0.916 | 0.796 |
| 0.50 | 7 078 | 0.970 | 0.934 | 0.850 |
| 0.75 | 10 616 | 0.972 | 0.944 | 0.871 |
| 1.00 | 14 155 | 0.973 | 0.949 | 0.887 |

The holdout curve rises and stabilizes instead of collapsing on the full train
split. This supports the risk-label result as a stable triage experiment while
still showing that train performance is higher than holdout performance.

Product conclusion: ML adds value as triage, prioritization, confidence
grouping, and review-queue ordering. Runtime recommendations remain rule-first.

Full artifacts:

- `eval/results/risk_baseline_ladder_current/summary.md`
- `eval/results/risk_learning_curve_current/summary.md`
- `data/ml/expert_dataset/eda/risk_error_analysis/error_analysis.md`
