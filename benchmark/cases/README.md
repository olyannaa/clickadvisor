# Benchmark Cases

`benchmark/cases/` stores source query cases grouped by origin.

The case directories created in this stage are seed corpora and templates. Many
of them intentionally keep `known_issues` and `expected_rules_to_fire` empty
until expert review is completed.

## Subdirectories

- `tpch/`: 22 seed cases based on TPC-H query texts
- `clickbench/`: seed cases from the ClickBench ClickHouse query set
- `job/`: selected JOIN-heavy cases from JOB Benchmark
- `synthetic/`: targeted rule scaffolds
- `github-issues/`: placeholder for manually curated issue-derived cases

## Validation contract

Every YAML file under these folders should conform to `benchmark/SCHEMA.yaml`.

Validate with:

```bash
python scripts/benchmark/validate_cases.py
```

## Labeling policy

- Keep unresolved labels empty instead of speculative.
- Treat source corpora as raw material, not ground truth.
- Only promote labels into `known_issues` and `expected_rules_to_fire` after
  DBA-backed review.
