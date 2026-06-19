# ClickAdvisor

ClickAdvisor is a local-first CLI for ClickHouse query optimization.

It is built for DBA and platform teams that want actionable recommendations,
clear trust boundaries, and no requirement to send customer SQL to an external
service.

The product thesis is simple:

- the core should be a library of mathematically grounded rules
- ClickHouse specifics should matter more than generic SQL folklore
- LLMs may assist, but they must not become the source of truth

Status: early development.

## One-minute overview

ClickAdvisor analyzes a query and its execution context, then explains what is
likely suboptimal and what to change.

Unlike generic AI SQL assistants, it is designed around explicit evidence and
tiered trust:

- Tier 1: formally equivalent rewrites
- Tier 2: cost-based recommendations using ClickHouse metadata
- Tier 3: LLM advisory with mandatory verification

The MVP is intentionally narrow:

- primary interface: CLI
- primary engine: ClickHouse only
- PostgreSQL: backlog
- local-first by default
- useful even with `--llm=none`

The tool works with SQL text, `EXPLAIN` without `ANALYZE`, schema definitions,
metadata, configs, and hardware characteristics.

It does not inspect customer data and it does not rely on replaying queries in a
benchmark harness to appear smart.

## Why this exists

Current SQL advisors often split into two camps.

The first camp is flexible but weakly grounded:

- chat-style assistants that generate plausible SQL advice
- low traceability for why a rewrite is safe
- limited separation between proof, heuristic, and guess

The second camp is safer but shallow:

- lint-like rule checkers
- useful style warnings
- weak adaptation to actual storage and execution context

ClickAdvisor aims for a stricter middle path:

- rigorous when rigor is possible
- cost-aware when proof is not possible
- advisory only when verification is available

That trust contract is the core product differentiation.

## Positioning vs competitors

### vs R-Bot

R-Bot-style tools are helpful as interactive assistants, but they usually do
not present a proof-oriented trust model for SQL rewrites.

ClickAdvisor is more explicit:

- every recommendation should be attributable to a rule, estimator, or
  verification step
- LLM-originated advice is not trusted by default
- the user should always know which tier produced an output

### vs EverSQL

EverSQL helped popularize automated SQL tuning, especially for traditional
relational workloads.

ClickAdvisor differs in two major ways:

- it is ClickHouse-first instead of generic multi-engine by default
- it is built around engine-specific storage and execution semantics

That matters because ClickHouse optimization often depends on:

- sparse primary keys
- granules and marks
- MergeTree part layout
- partition pruning
- projections
- `PREWHERE`
- read amplification

These are not edge details. They are often the real reason a query is fast or
slow.

### vs pganalyze

pganalyze is strong in operational observability and PostgreSQL expertise.

ClickAdvisor is not trying to become a full observability platform in the MVP.

It is intentionally narrower:

- analyze a query
- enrich it with environment context
- classify likely problems
- produce structured optimization advice

The center of gravity is query reasoning, not fleet-wide monitoring.

## Fixed MVP decisions

The following architectural decisions are intentionally locked in:

- CLI is the primary product surface
- ClickHouse is the only supported engine in MVP
- PostgreSQL is a future backlog item
- rule evaluation is tiered into formal, cost-based, and advisory layers
- LLM modes are `--llm=none`, `--llm=local`, and `--llm=remote`
- the tool does not run `ANALYZE`
- the tool does not inspect or export customer data
- success is measured by estimated cost reduction and benchmark precision/recall

If future code conflicts with one of these assumptions, the code should be
considered wrong before it is considered clever.

## What ClickAdvisor analyzes

Inputs are expected to include some combination of:

- SQL text
- `EXPLAIN ESTIMATE` or related non-`ANALYZE` plans
- schema definitions
- `system.parts` and related metadata
- server settings and config fragments
- hardware characteristics relevant to execution

This keeps the product practical for local and regulated deployments while still
providing enough context for engine-aware recommendations.

## What it does not do

The MVP explicitly avoids several tempting directions:

- no generic "works with every database" promise
- no hidden dependence on remote inference
- no direct data scanning for analysis
- no measured-speedup marketing metric as the core quality story
- no attempt to replace DBA review with opaque automation

Those constraints keep the system honest and make evaluation more reproducible.

## Quality model

ClickAdvisor should be judged by whether its recommendations are accurate,
useful, and trustworthy.

Primary evaluation axes:

- estimated cost reduction according to the database-oriented cost model
- precision and recall on a curated benchmark of roughly 100 cases
- qualitative usefulness in a DBA user study

Explicit non-goal metric:

- measured speedup from ad hoc live execution

Measured speedup is appealing, but early on it is too noisy and too dependent on
cache state, harness design, hardware, and data distribution to serve as the
primary truth metric.

## Architecture at a glance

The analysis pipeline is split into seven layers:

1. Ingest
2. Context Builder
3. Feature Extractor
4. Problem Classifier
5. Rewrite Engine
6. Environment Adjuster
7. Report Builder

The Rewrite Engine contains three rule tiers:

- Tier 1 for formally equivalent rewrites
- Tier 2 for cost-based recommendations grounded in metadata
- Tier 3 for LLM advisory with mandatory verification

This separation is crucial because it distinguishes:

- proof from estimation
- estimation from narrative
- trusted rewrites from exploratory guidance

## Local-first, not local-only

Local-first means the default workflow should remain useful with no remote
service dependency.

Remote LLM use is optional and explicit.

That is why the CLI exposes three modes:

- `--llm=none`
- `--llm=local`
- `--llm=remote`

The product should still create value in the first mode.

## Repository layout

The repository is structured to keep product code, docs, benchmark assets, and
research material separate:

- `clickadvisor/` application package
- `clickadvisor/core/` core primitives and analysis logic
- `clickadvisor/cli/` Typer-based command-line interface
- `clickadvisor/rules/` reserved for optimization rules
- `clickadvisor/llm/` LLM adapters and verification hooks
- `tests/` unit and property tests
- `data/kb/` knowledge base assets
- `docs/` architecture and reference documentation
- `docs/adr/` future architecture decision records
- `docs/rules/` future rule catalog
- `benchmark/cases/` curated benchmark inputs
- `examples/reports/` report mockups and samples
- `scripts/` utility scripts
- `notes/` working notes

## Initial technical stack

The scaffold is prepared around the following stack:

- Python 3.11+
- Poetry
- `sqlglot` for ClickHouse SQL parsing
- CatBoost for problem classification
- BGE-M3 embeddings
- Qdrant for retrieval
- vLLM or Ollama for local LLM operation
- Anthropic SDK for remote LLM use
- Typer and Rich for the CLI
- pytest and Hypothesis for testing
- testcontainers for ClickHouse integration scenarios
- GitHub Actions for CI

## Development direction

The next iterations should focus on durable product primitives:

- input contracts for SQL and environment context
- first Tier 1 rule implementations with proof notes
- ClickHouse-specific feature extraction
- structured finding and report models
- benchmark cases and regression tests
- retrieval-backed explanation support

The system should grow from trustworthy internals outward, not from surface demo
behavior inward.

## Rule philosophy

Every optimization rule should eventually answer a stable set of questions:

- what exact pattern does it detect
- what evidence does it require
- what recommendation or rewrite does it produce
- under what assumptions is it valid
- which tier owns it
- what caveats or failure modes apply

This approach keeps the project explainable and reviewable as the rule catalog
grows.

## LLM philosophy

LLMs are supporting components, not the engine of record.

They may help with:

- narrative explanation
- candidate idea generation
- retrieval-assisted summarization
- polishing user-facing wording

They may not silently bypass the rule system or collapse the distinction between
proven, estimated, and advisory outputs.

## Current repository status

This repository currently provides:

- package scaffolding
- a minimal Typer CLI entry point
- Poetry project configuration
- baseline CI
- container scaffolding
- architecture documentation
- a ClickHouse glossary for future ADRs and rule specs

It does not yet provide:

- real optimization rules
- ADR documents
- benchmark cases
- report mockups
- integration workflows against a live ClickHouse container

Those will be added in subsequent prompts as the project grows.
