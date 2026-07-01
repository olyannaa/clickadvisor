# ClickAdvisor

**Local-first ClickHouse Performance Advisor**

ClickAdvisor finds risky SQL patterns before they cause production incidents.
It runs entirely on your machine — no SQL, DDL, or query context ever leaves your environment.

```bash
# Analyze a single query
chadvisor analyze --sql "SELECT * FROM events FINAL WHERE date > '2024-01-01'"

# Analyze a workload from query_log export
chadvisor workload --query-log query_log.csv --output-format markdown

# Analyze a live ClickHouse instance
chadvisor workload --connect http://localhost:8123 --since 24
```

---

## Why ClickAdvisor

Generic SQL assistants see SQL syntax. ClickAdvisor knows ClickHouse:

- **Deterministic rule engine** — every finding has a `rule_id`, tier, severity, and confidence. No guessing.
- **ClickHouse-specific** — `FINAL`, sparse primary key, marks/parts, `PREWHERE`, `LowCardinality`, distributed joins, MergeTree mutations.
- **Local-first** — your SQL and query logs never touch an external LLM at runtime.
- **MCP-ready** — AI agents (Claude, Cursor, Codex) call ClickAdvisor as a tool, not as a source of truth.
- **Workload-aware** — goes beyond single queries to rank your most expensive query groups by actual resource consumption.

---

## Installation

**Requirements:** Python 3.11+, [Poetry](https://python-poetry.org/)

```bash
git clone https://github.com/olyannaa/clickadvisor.git
cd clickadvisor
poetry install
poetry run chadvisor --help
```

For live mode, add `httpx`:
```bash
poetry install --extras live
```

---

## Three modes of use

### 1 — Single query analysis

```bash
chadvisor analyze \
  --sql "SELECT countDistinct(user_id) FROM events WHERE toDate(ts) = today()" \
  --schema schema.sql \
  --format markdown
```

Example output:

```
## ClickAdvisor findings

### D-007 · high · Function on filter column
`toDate(ts)` wraps the primary key column. ClickHouse cannot use the sparse index.
→ Rewrite: `WHERE ts >= today() AND ts < today() + INTERVAL 1 DAY`

### R-102 · medium · Exact COUNT DISTINCT on high-cardinality column
Consider `uniq(user_id)` if an approximate result is acceptable (~2% error).
Exact `countDistinct` materializes all values in memory.
```

### 2 — Workload analysis (CSV mode)

Export a sanitized snapshot from ClickHouse:

```sql
SELECT
    query, query_duration_ms, read_rows, read_bytes, memory_usage,
    event_time, user, query_kind
FROM system.query_log
WHERE type = 'QueryFinish'
  AND event_time >= now() - INTERVAL 24 HOUR
FORMAT CSVWithNames
```

```bash
chadvisor workload \
  --query-log query_log.csv \
  --top-n 5 \
  --output-format markdown \
  --output report.md
```

Example output:

```
# ClickHouse workload risk report

## #1 · Dashboard fingerprint 8f3a… · RISK: HIGH
Executions/day: 1 240  |  Avg latency: 3.4 s  |  P95: 18.2 s
Total read/day: 2.8 TB  |  Total CPU time: 4.7 h

Findings:
  D-007 · high   · Function on filter column
  D-003 · high   · FINAL on large table (est. 2× scan overhead)
  R-102 · medium · Exact COUNT DISTINCT

→ DBA actions: verify FINAL necessity, inspect selected marks, test range rewrite
```

### 3 — Live mode

Connect directly to a running ClickHouse instance:

```bash
chadvisor workload \
  --connect http://localhost:8123 \
  --user default \
  --since 24 \
  --top-n 10 \
  --output-format markdown
```

ClickAdvisor reads `system.query_log` for the last N hours, groups queries by normalized fingerprint, ranks by total resource cost, and runs the full rule engine on each group.

> **Security note:** Only `SELECT` queries from `system.query_log` are read. No data is written. Credentials stay local.

---

## MCP integration

ClickAdvisor exposes a [Model Context Protocol](https://modelcontextprotocol.io/) server so AI agents can call it as a trusted tool — not generate advice themselves.

```
AI agent (Claude / Cursor / Codex)
        │
        │  MCP tool call: analyze_sql(sql, schema)
        ▼
ClickAdvisor rule engine   ←── deterministic, local, no LLM
        │
        │  structured findings: rule_id, severity, rewrite example
        ▼
AI agent presents findings to the user
```

The agent gets structured, explainable findings. It never invents ClickHouse advice.

### Option A — Remote MCP server (for demos and team use)

Connect Claude Desktop or any MCP client to the public instance:

```json
{
  "mcpServers": {
    "clickadvisor": {
      "transport": "sse",
      "url": "https://clickadvisor-mcp.up.railway.app/sse"
    }
  }
}
```

No installation needed. The remote server runs the rule engine only — your SQL is processed in memory and never stored.

### Option B — Local MCP server (for enterprise / NDA environments)

Run the server on your own machine in one command:

```bash
docker run -p 8000:8000 ghcr.io/olyannaa/clickadvisor-mcp:latest
```

Then add to Claude Desktop config:

```json
{
  "mcpServers": {
    "clickadvisor": {
      "transport": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

Or via stdio (no Docker required):

```json
{
  "mcpServers": {
    "clickadvisor": {
      "command": "poetry",
      "args": ["run", "python", "-m", "clickadvisor.mcp_server"],
      "cwd": "/path/to/clickadvisor"
    }
  }
}
```

### Available MCP tools

| Tool | Description |
|------|-------------|
| `analyze_sql` | Analyze a single SQL query |
| `analyze_with_schema` | Analyze SQL with DDL context |
| `analyze_workload_csv` | Analyze query_log CSV export |
| `list_rules` | List all available rules with descriptions |
| `explain_finding` | Get detailed explanation for a rule_id |

---

## Architecture

```
SQL / DDL / EXPLAIN / query_log
            │
            ▼
  ┌─────────────────────────┐
  │  Deterministic rule     │  ← trusted core, no LLM
  │  engine                 │
  │  · 40+ ClickHouse rules │
  │  · rule_id / tier /     │
  │    severity / confidence│
  └────────────┬────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
  CLI/JSON  Markdown    MCP server
  reports   reports     (SSE / stdio)
               │
               ▼
      Workload analyzer
      · fingerprint grouping
      · resource aggregation
      · top-N DBA review queue
               │
               ▼
       DS experiment layer
       · risk classification
       · triage / prioritization
       · method comparison
```

LLMs are used as **interface and automation** (MCP, research pipelines) — never as the source of performance findings.

---

## Data Science layer

ClickAdvisor includes a research layer that formalizes evaluation quality and prepares impact-based prioritization.

**Dataset:** 20 235 ClickHouse SQL queries from ClickBench, TPC-H, TPC-DS, SSB, ClickHouse functional tests, and open-source projects. Each query carries:
- `rule_findings` — deterministic rule engine output
- `measured_metrics` — `read_rows`, `query_duration_ms`, `memory_usage` from local replay
- `final_risk_label` — reconciled `low / medium / high` from both signals
- `label_source` — `rule_only / measured_only / both`

**Baseline results (holdout):**

| Model | Macro-F1 |
|-------|----------|
| Dummy (majority) | 0.278 |
| TF-IDF + Logistic Regression | 0.882 |
| Structured + Rule features + LR | 0.837 |
| **Random Forest (all features)** | **0.949** |
| CatBoost | 0.871 |

**Key finding:** RF F1=0.949 overall, but on `measured_only` subset (no rule signal) it drops to F1=0.595. This confirms that the rule engine is the production runtime — ML adds value as a triage and prioritization layer, not as a replacement.

Full experiment report: [`docs/experiments/risk_labeling_ds_summary.md`](docs/experiments/risk_labeling_ds_summary.md)

---

## Rule catalog

ClickAdvisor covers six risk families:

| Family | Examples |
|--------|---------|
| MergeTree & pruning | `FINAL`, functions on PK columns, bad partition pruning, missing `PREWHERE` |
| Aggregation & cardinality | `COUNT(DISTINCT)`, high-cardinality `GROUP BY`, memory-heavy aggregate states |
| Joins & distributed | Casts around join keys, large right-side joins, distributed join overhead |
| Schema design | `LowCardinality` candidates, `Nullable` overuse, oversized integer types |
| Settings & environment | `max_threads` vs CPU, `max_memory_usage`, async insert settings |
| Safety & operations | Mutations on large tables, `DELETE` without `WHERE`, `OPTIMIZE FINAL` misuse |

Each rule has: rule card · positive/negative tests · benchmark case · tier · confidence.

Browse the catalog: [`clickadvisor/rules/`](clickadvisor/rules/)

---

## Security & local-first posture

ClickAdvisor is designed for environments where SQL, DDL, and query logs are sensitive:

- **No external calls at runtime** — the rule engine is pure Python, offline by default.
- **MCP server processes in memory** — no query storage, no logging of SQL content.
- **Live mode** — reads `system.query_log` with a read-only user, no writes.
- **query_log export** — literals can be redacted before export; the rule engine works on normalized fingerprints.
- **LLM is optional** — agents use MCP to call ClickAdvisor; the LLM never generates trusted findings.

For strict environments: run the Docker image on-premise with no outbound network access.

Full security doc: [`docs/security-local-first.md`](docs/security-local-first.md)

---

## Roadmap

- [x] Single-query advisor (CLI + MCP)
- [x] Workload advisor — CSV mode
- [x] Live mode (`--connect`)
- [x] DS risk classification layer
- [ ] `EXPLAIN`-based before/after comparator
- [ ] ClickHouse Cloud / Altinity integration
- [ ] Impact ranking by `read_bytes × executions_per_day`
- [ ] Workload diff between time windows (before/after deploy)

---

## Development

```bash
# Run tests
poetry run pytest --ignore=tests/integration -q

# Type check
poetry run mypy clickadvisor

# Lint
poetry run ruff check clickadvisor tests scripts

# Validate rule catalog
poetry run python scripts/rules/validate_catalog.py

# Run benchmark suite
poetry run python scripts/eval/run_benchmark.py \
  --cases-dir benchmark/cases/synthetic_expanded \
  --mode strict
```

---

## License

MIT © 2024 olyannaa
