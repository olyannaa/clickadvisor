# Benchmark Cases

`benchmark/cases/` stores source query cases grouped by origin.

The current v1.0 scored subset is `synthetic/`, which contains 20 validated
rule-focused cases. Other folders are seed corpora and templates; many of them
intentionally keep `known_issues` and `expected_rules_to_fire` empty until expert
review is completed.

## Subdirectories

- `tpch/`: 22 seed cases based on TPC-H query texts
- `clickbench/`: seed cases from the ClickBench ClickHouse query set
- `job/`: selected JOIN-heavy cases from JOB Benchmark
- `synthetic/`: 20 validated targeted rule cases
- `github-issues/`: placeholder for manually curated issue-derived cases

## Validation contract

Every YAML file under these folders should conform to `benchmark/SCHEMA.yaml`.

Validate with:

```bash
poetry run python scripts/benchmark/validate_cases.py
```

## Evaluation

Run the synthetic rule benchmark with:

```bash
poetry run python scripts/eval/run_benchmark.py
```

Run retrieval embedding ablation with:

```bash
poetry run python scripts/eval/ablation_embeddings.py
```

## Labeling policy

- Keep unresolved labels empty instead of speculative.
- Treat source corpora as raw material, not ground truth.
- Only promote labels into `known_issues` and `expected_rules_to_fire` after
  DBA-backed review.
