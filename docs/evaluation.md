# Evaluation

ClickAdvisor reports several separate quality surfaces. They should not be merged
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

## 4. Risk Labeling DS Experiment

The risk-labeling experiment evaluates whether SQL text, structural features,
rule-derived features, and measured replay metrics can predict a coarse
`low` / `medium` / `high` risk label for triage.

It is not a replacement for the deterministic rule engine. Most labels are
`rule_only`, so the learned model is partly a compact approximation of current
rule behavior plus measured-metric signal.

Current dataset:

| Item | Value |
|---|---:|
| Records | 20 235 |
| Measured-ok records | 9 837 |
| Final low / medium / high | 4 253 / 14 285 / 1 697 |
| `rule_only` / `measured_only` / `both` | 14 693 / 4 635 / 907 |
| Feature rows | 20 235 |
| Numeric features | 115 |

Current baseline ladder:

| Model | CV macro-F1 | Test macro-F1 | Holdout macro-F1 |
|---|---:|---:|---:|
| dummy_most_frequent | 0.275 +/- 0.000 | 0.276 | 0.278 |
| dummy_stratified | 0.328 +/- 0.009 | 0.342 | 0.335 |
| tfidf_logistic_regression | 0.864 +/- 0.011 | 0.869 | 0.882 |
| structured_rule_logistic_regression | 0.827 +/- 0.004 | 0.822 | 0.837 |
| random_forest_all_features | 0.938 +/- 0.006 | 0.938 | 0.949 |
| catboost_tabular | 0.873 +/- 0.008 | 0.871 | 0.871 |

Important holdout slices for Random Forest:

| Slice | Records | Macro-F1 | High recall |
|---|---:|---:|---:|
| all_holdout | 3 039 | 0.949 | 0.887 |
| rule_only | 2 235 | 0.970 | 0.990 |
| measured_only | 672 | 0.595 | 0.785 |
| both | 132 | 0.975 | 1.000 |

The `measured_only` drop is the key sanity check: it shows where ML has less
rule-derived signal to inherit. The `both` result shows the strongest core,
where static rules and measured replay agree.

Artifacts:

- `data/ml/expert_dataset/eda/ds_report.md`
- `docs/experiments/risk_labeling_ds_summary.md`
- `eval/results/risk_baseline_ladder_current/metrics.json`
- `data/ml/expert_dataset/eda/risk_error_analysis/error_analysis.md`

## 5. Workload Analyzer Prototype

`chadvisor workload` is evaluated as a product prototype, not as a learned
ranking model yet. It reads sanitized `system.query_log` CSV exports, groups
normalized queries, runs representative queries through the deterministic rule
engine, and ranks top opportunities by rule severity plus observed resource
metrics.

Current smoke command:

```bash
poetry run chadvisor workload \
  --query-log examples/query_log_sample.csv \
  --output-format markdown \
  --top-n 3
```

The sample report surfaces three normalized query groups and ranks a `FINAL` +
leading-wildcard pattern first with rule IDs `D-003`, `D-004`, `D-005`, `D-007`,
and `R-102`.

This surface still needs ranking metrics such as Precision@K and NDCG@K before
it should be presented as a validated impact-ranking model.

## Reproducibility Notes

- Synthetic dataset: `benchmark/cases/synthetic_expanded`
- Split metadata: `benchmark/splits/synthetic_expanded_v1.yaml`
- Context metadata: benchmark cases may declare `context_type`, inline
  `schema_ddl`, and structured `environment` objects.
- Classifier script: `scripts/eval/ablation_classifiers.py`
- Retrieval script: `scripts/eval/ablation_embeddings.py`
- Risk-label DS scripts: `scripts/lab/`
- Workload prototype sample: `examples/query_log_sample.csv`
- Benchmark runner: `scripts/eval/run_benchmark.py`

Remote LLMs are not part of these metrics. They may assist development or call
ClickAdvisor through MCP, but they do not produce the trusted finding set.
