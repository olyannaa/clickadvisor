# Risk Baseline Ladder

Risk-label baselines are triage models over deterministic rule labels plus measured metric labels. They are not intended to replace the rule engine.

## Cross-Validation Summary

| Model | CV macro-F1 | CV MCC | Test macro-F1 | Test MCC | Holdout macro-F1 | Holdout MCC |
|---|---:|---:|---:|---:|---:|---:|
| dummy_most_frequent | 0.275 +/- 0.000 | 0.000 +/- 0.000 | 0.276 | 0.000 | 0.278 | 0.000 |
| dummy_stratified | 0.328 +/- 0.009 | -0.017 +/- 0.015 | 0.342 | 0.004 | 0.335 | 0.007 |
| tfidf_logistic_regression | 0.864 +/- 0.011 | 0.837 +/- 0.012 | 0.869 | 0.839 | 0.882 | 0.856 |
| structured_rule_logistic_regression | 0.827 +/- 0.004 | 0.810 +/- 0.004 | 0.822 | 0.805 | 0.837 | 0.822 |
| random_forest_all_features | 0.938 +/- 0.006 | 0.935 +/- 0.006 | 0.938 | 0.937 | 0.949 | 0.945 |
| catboost_tabular | 0.873 +/- 0.008 | 0.864 +/- 0.010 | 0.871 | 0.859 | 0.871 | 0.862 |

## High-Class Recall

- `dummy_most_frequent`: test=0.000, holdout=0.000
- `dummy_stratified`: test=0.104, holdout=0.062
- `tfidf_logistic_regression`: test=0.869, holdout=0.912
- `structured_rule_logistic_regression`: test=0.656, holdout=0.696
- `random_forest_all_features`: test=0.846, holdout=0.887
- `catboost_tabular`: test=0.788, holdout=0.804
