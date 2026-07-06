# Risk Baseline Ladder

Risk-label baselines are triage models over deterministic rule labels plus measured metric labels. They are not intended to replace the rule engine. Use --feature-policy leakage_aware for a stricter run without explicit rule-derived features and rule-shaped parser flags.

## Cross-Validation Summary

| Model | CV macro-F1 | CV MCC | Test macro-F1 | Test MCC | Holdout macro-F1 | Holdout MCC |
|---|---:|---:|---:|---:|---:|---:|
| dummy_stratified | 0.328 +/- 0.009 | -0.017 +/- 0.015 | 0.342 | 0.004 | 0.335 | 0.007 |
| tfidf_logistic_regression | 0.864 +/- 0.011 | 0.837 +/- 0.012 | 0.869 | 0.839 | 0.882 | 0.856 |
| random_forest_all_features | 0.879 +/- 0.006 | 0.853 +/- 0.008 | 0.890 | 0.863 | 0.900 | 0.873 |

## High-Class Recall

- `dummy_stratified`: test=0.104, holdout=0.062
- `tfidf_logistic_regression`: test=0.869, holdout=0.912
- `random_forest_all_features`: test=0.884, holdout=0.892
