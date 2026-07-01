# Project Readiness Against Evaluation Criteria

This document maps the current ClickAdvisor repository to the defense
evaluation criteria. It is intentionally evidence-based: every claim points to
code, tests, data, documentation, or reproducible artifacts.

## Development

Target level: 3.

Evidence:

- Python package managed with Poetry.
- Typed core code checked with `mypy`.
- Linting with `ruff`.
- Unit tests, integration tests, validators, and benchmark checks.
- GitHub Actions CI for lint, type-check, tests, and ClickHouse integration.
- Docker image for Streamable HTTP MCP deployment.
- Local ClickHouse replay environment through Docker Compose.
- Dedicated modules for CLI, rules, retrieval, EXPLAIN, MCP, workload, and ML.

Main commands:

```bash
poetry run ruff check clickadvisor tests scripts
poetry run mypy clickadvisor
poetry run pytest --ignore=tests/integration -q
poetry run python scripts/rules/validate_catalog.py
poetry run python scripts/benchmark/validate_cases.py
```

Assessment: strong level 3 engineering culture. The remaining production gap is
release packaging for public distribution.

## Data Science

Target level: 3.

Evidence:

- Expert SQL dataset: 20 235 records.
- Measured local replay metrics for 9 837 successful queries.
- Rule labels, measured labels, final risk labels, and label-source analysis.
- EDA for measured metrics and label distributions.
- Feature extraction: normalized SQL, structural features, rule-derived
  features, TF-IDF inside baselines.
- Group-aware train/test/holdout split and 5-fold validation.
- Baseline ladder: Dummy, TF-IDF + Logistic Regression, structured/rule LR,
  Random Forest, CatBoost.
- Holdout error analysis by `label_source`, especially `measured_only` and
  `both`.

Key result:

- Random Forest all-features holdout macro-F1: 0.949.
- Measured-only holdout macro-F1: 0.595.
- Both-source holdout macro-F1: 0.975.

Assessment: level 3 DS contour. The important methodological caveat is already
documented: the model is a triage/prioritization layer, not a replacement for
the deterministic rule engine.

## AI Usage

Target level: 3.

Evidence:

- MCP server exposes ClickAdvisor as a local tool for AI clients.
- Local stdio MCP for desktop/IDE workflows.
- Streamable HTTP MCP endpoint for remote-compatible demos.
- AI/MCP workflow documentation explains how agents call deterministic tools
  instead of inventing optimization advice.
- Agent-assisted DS workflow is documented as part of research: data
  preparation, validation, modeling, and review.

Assessment: level 3 if presented as systematic AI-agent usage. The key point is
that AI is an interface and development accelerator, not the trusted runtime
source of recommendations.

## Product Thinking

Target level: high level 2 to level 3.

Evidence:

- Clear target users: DBA, data engineers, backend engineers, BI/dashboard
  owners, platform teams.
- Clear pain: ClickHouse performance incidents, CPU/RAM waste, high latency,
  cloud cost, DBA review time.
- Competitive framing: rule-based SQL antipatterns, DB observability,
  Postgres plan advisors, learned optimizers, LLM/RAG SQL assistants.
- MVP surfaces: CLI, JSON/Markdown reports, MCP, workload analyzer, local
  retrieval, EXPLAIN ESTIMATE.
- Business-impact path: workload-level top-N opportunities and future
  impact-based ranking.

Assessment: product thinking is strong for an MVP. The remaining gap for a full
level 3 product case is external user/market feedback: interviews, expert
evaluation, or real workload feedback from ClickHouse users.
