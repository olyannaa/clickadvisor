<p align="center">
  <img src="docs/demo.png" alt="ClickAdvisor CLI demo" width="760">
</p>

<h1 align="center">ClickAdvisor</h1>

<p align="center">
  Local-first ClickHouse Performance Advisor for SQL, workload review, and AI-agent workflows.
</p>

<p align="center">
  <a href="README.md"><img alt="README Russian" src="https://img.shields.io/badge/README-Русский-2ea44f?style=for-the-badge"></a>
  <a href="README.en.md"><img alt="README English" src="https://img.shields.io/badge/README-English-0969da?style=for-the-badge"></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
  <img alt="ClickHouse" src="https://img.shields.io/badge/ClickHouse-performance%20advisor-ffcc01">
  <img alt="Rules" src="https://img.shields.io/badge/rules-119-brightgreen">
  <img alt="Benchmark" src="https://img.shields.io/badge/benchmark-327%20cases-brightgreen">
  <img alt="MCP" src="https://img.shields.io/badge/MCP-stdio%20%2B%20HTTP-blueviolet">
  <img alt="Local First" src="https://img.shields.io/badge/security-local--first-success">
</p>

ClickAdvisor helps DBAs, data engineers, backend engineers, and platform teams
find risky ClickHouse SQL patterns before production incidents, CPU/RAM waste,
and expensive cloud bills.

It is not a generic SQL chatbot. The trusted runtime is built around a
deterministic ClickHouse rule engine: every finding has a `rule_id`, severity,
tier, confidence, explanation, and rewrite example where the rewrite is safe.
AI is used as an interface through MCP and as a research workflow, not as the
source of production recommendations.

## Contents

- [Capabilities](#capabilities)
- [Quick start](#quick-start)
- [Single-query advisor](#single-query-advisor)
- [Workload analyzer](#workload-analyzer)
- [MCP](#mcp)
- [Data Science and ML](#data-science-and-ml)
- [Evaluation](#evaluation)
- [Security](#security)
- [Documentation](#documentation)

## Capabilities

| Surface | Capability |
|---|---|
| SQL advisor | Analyze one ClickHouse SQL query through CLI, JSON, Markdown, or MCP |
| Rule engine | 119 ClickHouse-specific rules, detectors, and environment checks |
| Workload analyzer | `system.query_log` CSV/live analysis, normalized fingerprints, top-N risks |
| EXPLAIN ESTIMATE | Planner rows/marks comparison without executing user queries |
| MCP server | Local stdio MCP and Streamable HTTP MCP for remote-compatible demos |
| Local retrieval | Embedded Qdrant KB over ClickHouse docs, Altinity KB, blog/release notes |
| DS/ML lab | Expert dataset, EDA, features, group split, baselines, error analysis |

## Why this matters for ClickHouse

ClickHouse can execute analytical queries extremely fast, but performance
depends on engine details: MergeTree, sparse primary keys, marks/parts, `FINAL`,
skip indexes, `PREWHERE`, materialized views, distributed execution,
memory/thread settings, and the actual workload.

ClickAdvisor solves a practical problem: it does not “guess an optimization”.
It produces a verifiable ClickHouse-specific signal that can be reviewed by a
DBA, used in CI, passed to an AI agent through MCP, or turned into a workload
review queue.

## Quick start

```bash
git clone https://github.com/olyannaa/clickadvisor.git
cd clickadvisor
poetry install
poetry run chadvisor analyze --sql query.sql
```

Docker:

```bash
docker build -t clickadvisor .
docker run --rm -p 8000:8000 clickadvisor
```

By default, the Docker image starts a lightweight Streamable HTTP MCP endpoint
at `/mcp`. The image is meant for demo/deploy use and does not install heavy
ML/retrieval dependencies.

## Single-query advisor

```bash
poetry run chadvisor analyze \
  --sql query.sql \
  --ch-version 25.3 \
  --output-format markdown \
  --no-retrieval
```

Example risky query:

```sql
SELECT
    e.country,
    COUNT(DISTINCT e.user_id) AS unique_users,
    sumIf(e.revenue, e.status = 'paid') AS paid_revenue
FROM
(
    SELECT *
    FROM events FINAL
    WHERE message LIKE '%timeout%'
      AND (country = 'RU' OR country = 'KZ' OR country = 'BY')
) AS e
JOIN users AS u
    ON toUInt64(e.user_id) = u.id
GROUP BY e.country
HAVING e.country = 'RU'
ORDER BY paid_revenue DESC;
```

For this query, ClickAdvisor returns 10 findings, including:

- `R-001`: `COUNT(DISTINCT user_id)` -> `uniqExact(user_id)`;
- `R-002`: approximate distinct with `uniq` when acceptable;
- `D-005` / `R-102`: leading wildcard search and skip-index/search strategy;
- `D-007`: expensive `FINAL` on MergeTree;
- `D-011`, `R-008`, `R-020`: type casts around JOIN/filter keys;
- `R-011`: non-aggregate `HAVING` can move to `WHERE`;
- `R-014`: expensive `GROUP BY` over a string column.

<p align="center">
  <img src="docs/assets/readme-example-output.svg" alt="ClickAdvisor markdown report example" width="780">
</p>

## Workload analyzer

CSV export from `system.query_log`:

```bash
poetry run chadvisor workload \
  --query-log examples/query_log_sample.csv \
  --output-format markdown \
  --top-n 3
```

Live read-only mode through the ClickHouse HTTP API:

```bash
poetry run chadvisor workload \
  --connect http://localhost:8123 \
  --user default \
  --password secret \
  --since 24h \
  --output-format markdown \
  --top-n 10
```

`workload` groups similar queries by normalized fingerprint, computes
executions, total/avg/p95 latency, read rows/bytes, and memory usage, then runs
representative SQL through the rule engine and builds a top-N DBA review queue.

Example top risk from the sample:

```text
Priority: high
Executions: 2
Total duration: 2180 ms
Read bytes: 350000000
Rule IDs: D-003, D-004, D-005, D-007, R-102
Normalized SQL: select * from events final where message like ?
```

More details: [docs/workload.md](docs/workload.md).

## MCP

Local stdio MCP for Claude Desktop, Cursor, Zed, and other MCP clients:

```bash
poetry run chadvisor mcp-server
```

Public MCP endpoint for testing without a local install:

```text
https://clickadvisor-mcp-production.up.railway.app/mcp
```

Claude / Anthropic API can connect to the remote MCP server as a URL-based
server:

```text
Claude / Claude Desktop:
Customize -> Connectors -> Add custom connector
Name: ClickAdvisor
URL:  https://clickadvisor-mcp-production.up.railway.app/mcp
```

Claude Code:

```bash
claude mcp add --transport http clickadvisor \
  https://clickadvisor-mcp-production.up.railway.app/mcp
```

Anthropic API:

```json
{
  "mcp_servers": [
    {
      "type": "url",
      "name": "clickadvisor",
      "url": "https://clickadvisor-mcp-production.up.railway.app/mcp"
    }
  ]
}
```

Available MCP tools:

| Tool | Purpose |
|---|---|
| `analyze_query` | Markdown report for ClickHouse SQL |
| `analyze_query_json` | Structured JSON for automation |
| `list_rules` | Registered rule catalog |
| `detect_ch_version` | ClickHouse version detection through HTTP API |

If you open `/mcp` in a browser, you may see `Not Acceptable: Client must
accept text/event-stream`. That is expected: the endpoint is for MCP clients,
not a regular HTML page.

More details:

- [docs/MCP.md](docs/MCP.md)
- [docs/mcp-deployment.md](docs/mcp-deployment.md)
- [docs/ai-mcp-workflow.md](docs/ai-mcp-workflow.md)

## Schema, EXPLAIN, and environment

```bash
poetry run chadvisor analyze \
  --sql query.sql \
  --schema schema.sql \
  --explain explain.json \
  --environment environment.json
```

Environment context includes settings, hardware, cluster, and workload facts
for `E-*` rules and selected Tier 2 advisory rules:

```json
{
  "settings": {
    "max_threads": 64,
    "max_memory_usage": 90000000000,
    "join_use_nulls": true
  },
  "hardware": {
    "cpu_cores": 16,
    "ram_bytes": 128000000000,
    "disk_type": "hdd"
  },
  "workload": {
    "interactive_queries": true,
    "large_join": true,
    "bulk_inserts": true
  },
  "cluster": {
    "shards": 4,
    "replicas": 2
  }
}
```

EXPLAIN ESTIMATE:

```bash
poetry run chadvisor analyze \
  --sql query.sql \
  --connect http://localhost:8123 \
  --ch-user default \
  --ch-password secret \
  --explain-estimate
```

ClickAdvisor runs only `EXPLAIN ESTIMATE`; it does not execute the user query
and does not read result data.

## Data Science and ML

The DS layer is not meant to replace the rule engine. Its job is to formalize
quality, compare approaches, expose limitations, and prepare a
triage/prioritization layer.

Expert dataset:

| Metric | Value |
|---|---:|
| SQL records | 20 235 |
| Real / synthetic | 19 090 / 1 145 |
| Successful local replay records | 9 837 |
| Final labels | low 4 253 / medium 14 285 / high 1 697 |
| Numeric feature count | 115 |
| Rule vocabulary | 54 |

Key label-source fact:

| Label source | Records | Interpretation |
|---|---:|---|
| `rule_only` | 14 693 | model mostly learns a compressed rule-engine signal |
| `measured_only` | 4 635 | independent signal from latency/read/memory metrics |
| `both` | 907 | strongest core where static and measured signals agree |

Baseline ladder:

| Model | CV macro-F1 | Holdout macro-F1 |
|---|---:|---:|
| Dummy most frequent | 0.275 +/- 0.000 | 0.278 |
| Dummy stratified | 0.328 +/- 0.009 | 0.335 |
| TF-IDF + Logistic Regression | 0.864 +/- 0.011 | 0.882 |
| Structural/rule LR | 0.827 +/- 0.004 | 0.837 |
| Random Forest all features | 0.938 +/- 0.006 | 0.949 |
| CatBoost tabular | 0.873 +/- 0.008 | 0.871 |

Random Forest holdout error analysis:

| Slice | Records | Macro-F1 | High recall |
|---|---:|---:|---:|
| all_holdout | 3 039 | 0.949 | 0.887 |
| rule_only | 2 235 | 0.970 | 0.990 |
| measured_only | 672 | 0.595 | 0.785 |
| both | 132 | 0.975 | 1.000 |

Conclusion: ML is useful for triage, confidence grouping, and review queue
ordering, but production recommendations remain rule-first.

More details:

- [docs/evaluation.md](docs/evaluation.md)
- [docs/experiments/risk_labeling_ds_summary.md](docs/experiments/risk_labeling_ds_summary.md)
- [data/ml/expert_dataset/eda/ds_report.md](data/ml/expert_dataset/eda/ds_report.md)

## Evaluation

| Evaluation surface | Data | Result |
|---|---|---:|
| Rule detection | 222 synthetic/schema/env cases | precision 1.000 / recall 1.000 / F1 1.000 |
| Retrieval | 20 query -> docs pairs | best MRR@3 0.517 |
| Risk-label DS | 20 235 SQL records | RF holdout macro-F1 0.949 |
| Workload prototype | sample query_log CSV | normalized groups + top-N risk report |

Reproducible checks:

```bash
poetry run ruff check clickadvisor tests scripts
poetry run mypy clickadvisor
poetry run pytest --ignore=tests/integration -q
poetry run python scripts/rules/validate_catalog.py
poetry run python scripts/benchmark/validate_cases.py
poetry run python scripts/eval/run_benchmark.py --cases-dir benchmark/cases/synthetic_expanded --mode strict
```

## Security

ClickAdvisor can run inside a company network, CI/CD, or an engineer's local
environment without sending SQL, DDL, EXPLAIN, environment context, or
`query_log` data to external LLM/API services.

What ClickAdvisor may read:

- SQL text;
- optional schema DDL;
- optional EXPLAIN output;
- optional environment JSON;
- sanitized `system.query_log` CSV or read-only live metadata;
- `SELECT version()` for version detection;
- `EXPLAIN ESTIMATE` only when explicitly requested.

What it does not do by default:

- does not execute user SQL for speedup measurement;
- does not read result data;
- does not run `ANALYZE`;
- does not apply DDL/mutations;
- does not make hidden remote LLM calls.

More details: [docs/security-local-first.md](docs/security-local-first.md).

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Evaluation](docs/evaluation.md)
- [Workload Analyzer](docs/workload.md)
- [MCP](docs/MCP.md)
- [MCP Deployment](docs/mcp-deployment.md)
- [Security / Local-First](docs/security-local-first.md)
- [Rule Catalog](docs/rules/README.md)

## License

MIT
