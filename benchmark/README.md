# ClickAdvisor Benchmark

`/benchmark/` contains the curated evaluation corpus and the metadata contracts
used to score ClickAdvisor over time.

## Purpose

The benchmark exists to answer a narrow question:

- given a query and limited context, does ClickAdvisor detect the right problem,
  fire the right rule family, and communicate the right trust tier?

It is not primarily a query replay harness and it is not a measured-speedup
leaderboard.

## Planned scope

The benchmark is expected to converge toward roughly 100-150 tracked cases made
up of:

- TPC-H query seeds
- ClickBench query seeds
- selected JOIN-heavy JOB cases
- synthetic targeted cases for individual rule families
- manually curated GitHub issue cases from real-world ClickHouse performance
  discussions

The raw count of YAML files may exceed the final scored set because some cases
will remain unlabelled or exploratory until reviewed with DBA experts.

## Sources

- TPC-H
- ClickBench
- Join Order Benchmark (JOB)
- synthetic hand-authored rule probes
- manually curated GitHub issues

## Labeling methodology

Important constraint:

- final `known_issues` and `expected_rules_to_fire` labels are expert work and
  must be reviewed manually with DBA input

This repository step provides source queries and structural templates only. It
does not claim benchmark truth for the unresolved labels.

## Case structure

Each benchmark case is a YAML document validated against `benchmark/SCHEMA.yaml`.

Core fields:

- `case_id`
- `source`
- `sql`
- `schema_files`
- `known_issues`
- `expected_rules_to_fire`
- `expected_improvement`
- `synthetic_explain_path`
- `notes`

## Current folder roles

- `cases/tpch/`: TPC-H query seeds
- `cases/clickbench/`: ClickBench query seeds
- `cases/job/`: selected JOIN-heavy JOB seeds
- `cases/synthetic/`: empty targeted scaffolds for rule-focused testing
- `cases/github-issues/`: future manually curated real-world issue cases

## Validation

Run:

```bash
python scripts/benchmark/validate_cases.py
```

This checks schema compliance across all YAML cases before they are consumed by
evaluation tooling.
