# Evaluation

ClickAdvisor reports three separate quality surfaces. They should not be merged
into a single headline number because they measure different things.

## 1. Deterministic Rule Detection

The rule engine is fixed code, not a trained model. Its benchmark answers:
"Did the analyzer fire the expected implemented rules on this labeled case?"

Current expanded synthetic run:

```bash
poetry run python scripts/eval/run_benchmark.py \
  --cases-dir benchmark/cases/synthetic_expanded \
  --mode strict
```

Result on 2026-06-30:

| Dataset | Cases | Precision | Recall | F1 | Notes |
|---|---:|---:|---:|---:|---|
| `synthetic_expanded` | 222 | 1.000 | 1.000 | 1.000 | Generated plus targeted SQL/schema/env rule-regression set |
| held-out split only | 36 | 1.000 | 1.000 | 1.000 | `synthetic_expanded_v1.yaml` test IDs |

This is a regression result for deterministic matchers. It should not be
presented as ML generalization.

## 2. ML Classifier Ablation

The classifier is the only surface where F1 measures a learned decision
boundary. It uses AST/SQL features from `clickadvisor/ml/features.py` and
multi-label targets from `expected_rules_to_fire`.

Current command:

```bash
poetry run python scripts/eval/ablation_classifiers.py --run-id classifier_ablation_current
```

Current results:

| Model | Train F1 macro | Train F1 micro | Test F1 macro | Test F1 micro | Precision | Recall |
|---|---:|---:|---:|---:|---:|---:|
| logistic_regression | 0.908 | 0.868 | 0.678 | 0.870 | 0.667 | 0.704 |
| random_forest | 0.971 | 0.975 | 0.667 | 0.951 | 0.667 | 0.667 |
| catboost | 0.973 | 0.976 | 0.691 | 0.988 | 0.685 | 0.704 |

Artifacts:

- `eval/results/classifier_ablation_current/metrics.json`
- `eval/results/classifier_ablation_current/metrics.csv`
- `docs/experiments/classifier_ablation.md`

## 3. Retrieval Ablation

Retrieval quality is measured with `MRR@3` over explicit query-to-document gold
references. A result is relevant only when its URL/path or text matches the
gold reference for one of the expected rules.

Current command:

```bash
poetry run python scripts/eval/ablation_embeddings.py
```

Current results:

| Model | Size | Queries | MRR@3 | Time (s) |
|---|---:|---:|---:|---:|
| multilingual-e5-small (current) | 117 MB | 20 | 0.458 | 17.7 |
| all-MiniLM-L6-v2 | 80 MB | 20 | 0.517 | 10.4 |
| paraphrase-multilingual-MiniLM-L12-v2 | 420 MB | 20 | 0.242 | 12.4 |

Artifacts:

- `eval/results/retrieval_ablation_20260630T124602Z/metrics.json`
- `docs/experiments/retrieval_ablation.md`

## Reproducibility Notes

- Synthetic dataset: `benchmark/cases/synthetic_expanded`
- Split metadata: `benchmark/splits/synthetic_expanded_v1.yaml`
- Context metadata: benchmark cases may declare `context_type`, inline
  `schema_ddl`, and structured `environment` objects.
- Classifier script: `scripts/eval/ablation_classifiers.py`
- Retrieval script: `scripts/eval/ablation_embeddings.py`
- Benchmark runner: `scripts/eval/run_benchmark.py`

Remote LLMs are not part of these metrics. They may assist development or call
ClickAdvisor through MCP, but they do not produce the trusted finding set.
