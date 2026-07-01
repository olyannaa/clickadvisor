# Classifier Ablation

## Snapshot

- Date: 2026-06-30
- Dataset: `benchmark/cases/synthetic_expanded` (`180` cases)
- Split: `benchmark/splits/synthetic_expanded_v1.yaml` (`144` train, `36` test)
- Features: `clickadvisor/ml/features.py`
- Labels: multi-label `expected_rules_to_fire`
- Command:

```bash
poetry run python scripts/eval/ablation_classifiers.py --run-id classifier_ablation_current
```

## Results

| Model | Train F1 macro | Train F1 micro | Test F1 macro | Test F1 micro | Precision | Recall |
|---|---:|---:|---:|---:|---:|---:|
| logistic_regression | 0.908 | 0.868 | 0.678 | 0.870 | 0.667 | 0.704 |
| random_forest | 0.971 | 0.975 | 0.667 | 0.951 | 0.667 | 0.667 |
| catboost | 0.973 | 0.976 | 0.691 | 0.988 | 0.685 | 0.704 |

Results were saved to `eval/results/classifier_ablation_current/`.

## Interpretation

Micro F1 is high because most frequent structural labels are easy to separate
from deterministic AST/text features. Macro F1 is lower because the held-out set
is small and several labels have only one or two positive examples in test.

Random Forest is the strongest baseline in this run, but the train/test gap
shows why these numbers should be reported as synthetic classifier ablation
metrics, not as production generalization claims.

The gap is expected for this specific setup: the split has only `36` test cases,
and rare rule labels may have one or two positives. Tree models can memorize
the training side of this compact benchmark (`train macro-F1` about `0.97`)
while test macro-F1 stays around `0.67`-`0.69`.

## Relationship to Risk-Label Baselines

This experiment must not be compared directly with
`risk_baseline_ladder_current`.

| Experiment | Dataset | Target | Split | What it answers |
|---|---:|---|---|---|
| Classifier ablation | 180 synthetic benchmark cases | multi-label `expected_rules_to_fire` | 144 train / 36 test | Can ML features predict expected rule IDs on a compact rule benchmark? |
| Risk baseline ladder | 20 235 query records | `low` / `medium` / `high` risk | group-aware train/test/holdout | Can SQL/text/rule/measured features triage query risk? |

The classifier ablation gap is a warning about rare-label generalization in the
small rule benchmark. The risk-label holdout score is a separate triage result
with different labels, features, split semantics, and dataset size.
