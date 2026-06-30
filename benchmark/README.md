# ClickAdvisor Benchmark

`/benchmark/` contains the curated evaluation corpus and metadata contracts used
to score ClickAdvisor over time.

## Purpose

The benchmark answers a narrow question:

- given a query and limited context, does ClickAdvisor detect the right problem,
  fire the right rule family, and communicate the right trust tier?

It is not a query replay harness and it is not a measured-speedup leaderboard.
Runtime impact is reported separately through planner estimates such as
`EXPLAIN ESTIMATE`.

## Current state

The repository includes 20 validated synthetic cases under
`benchmark/cases/synthetic/`. They target the implemented rule and detector
families and are used by:

```bash
poetry run python scripts/eval/run_benchmark.py
```

The repository also includes an expanded generated synthetic dataset:

- `benchmark/cases/synthetic_expanded/`: 222 deterministic cases, including
  SQL-only, schema-aware, and env-aware rule probes
- `benchmark/splits/synthetic_expanded_v1.yaml`: fixed 80/20 train/test split
  for the original 180-case ML dataset
- `scripts/benchmark/generate_synthetic_dataset.py`: reproducible generator

The expanded dataset exists to avoid presenting a suspicious metric on only 20
hand-authored probes. It contains positive variations for implemented rules,
targeted backlog-closure probes for `D-*`, `E-*`, and `R-101+`, multi-label
overlaps where the current analyzer really emits several findings, and
negative queries where no implemented rule should fire.

Run the expanded benchmark:

```bash
poetry run python scripts/eval/run_benchmark.py \
  --cases-dir benchmark/cases/synthetic_expanded \
  --mode strict
```

Regenerate it deterministically:

```bash
poetry run python scripts/benchmark/generate_synthetic_dataset.py --overwrite
```

Retrieval experiments reuse these synthetic cases as query prompts and expected
rule labels:

```bash
poetry run python scripts/eval/ablation_embeddings.py
```

## Planned scope

The benchmark is expected to grow beyond the generated 180-case synthetic set
with manually reviewed real-query cases made up
of:

- TPC-H query seeds
- ClickBench query seeds
- selected JOIN-heavy JOB cases
- synthetic targeted cases for individual rule families
- manually curated GitHub issue cases from real-world ClickHouse performance
  discussions

The raw count of YAML files may exceed the final scored set because some cases
remain unlabelled or exploratory until reviewed with DBA experts.

## Sources

- TPC-H
- ClickBench
- Join Order Benchmark (JOB)
- synthetic hand-authored rule probes
- manually curated GitHub issues

## Labeling methodology

Important constraint:

- final `known_issues` and `expected_rules_to_fire` labels are expert work and
  should be reviewed manually with DBA input before being treated as ground
  truth

Synthetic cases in v1.0 are validated for implemented rules. Broader source
corpora remain seed material until labelled.

## Case structure

Each benchmark case is a YAML document validated against `benchmark/SCHEMA.yaml`.

Core fields:

- `case_id`
- `source`
- `sql`
- `schema_files`
- `schema_ddl` for inline schema-aware cases
- `environment` for env-aware cases
- `context_type`: `sql-only`, `schema-aware`, `env-aware`, or `explain-aware`
- `known_issues`
- `expected_rules_to_fire`
- `expected_improvement`
- `synthetic_explain_path`
- `notes`

## Current folder roles

- `cases/tpch/`: TPC-H query seeds
- `cases/clickbench/`: ClickBench query seeds
- `cases/job/`: selected JOIN-heavy JOB seeds
- `cases/synthetic/`: 20 validated targeted rule cases
- `cases/synthetic_expanded/`: 222 rule-regression cases with negative examples,
  fixed split metadata for the original generated subset, and targeted
  schema/env-aware probes for newly implemented rules
- `cases/github-issues/`: placeholder for manually curated issue-derived cases

## Validation

Run:

```bash
poetry run python scripts/benchmark/validate_cases.py
```

This checks schema compliance across all YAML cases before they are consumed by
evaluation tooling.
