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

Product conclusion: ML adds value as triage, prioritization, confidence
grouping, and review-queue ordering. Runtime recommendations remain rule-first.

Full artifacts:

- `eval/results/risk_baseline_ladder_current/summary.md`
- `data/ml/expert_dataset/eda/risk_error_analysis/error_analysis.md`
