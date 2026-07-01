# ClickAdvisor Architecture

ClickAdvisor is a local-first ClickHouse advisor with two interfaces over the
same analysis core:

- `chadvisor` CLI for shell, CI, and DBA workflows
- stdio MCP server for Claude Desktop, Cursor, Continue, Zed, and other agents

The core design principle is that interfaces adapt inputs and outputs only; rule
logic, version filtering, retrieval advisory, and explain impact estimation stay
inside reusable packages.

## Design constraints

- CLI remains the primary interface.
- MCP is a thin secondary interface over the same core.
- ClickHouse is the only supported database engine in v1.0.
- Operation is local-first; no SQL or metadata is sent to external services.
- The tool does not run `ANALYZE` and does not inspect table data.
- Recommendations preserve tier, confidence, and version attribution.
- Retrieval and EXPLAIN ESTIMATE are optional enrichments, never prerequisites
  for deterministic rule findings.

## Runtime packages

```text
clickadvisor/
  cli/            Typer CLI and Rich/JSON/Markdown presentation
  core/           QueryContext, Finding, Report, AnalysisPipeline
  rules/          Deterministic ClickHouse rules and detectors
  retrieval/      Embedding model wrapper, Qdrant indexer, retriever, RAG advisor
  explain/        EXPLAIN ESTIMATE parser, HTTP estimator, before/after comparator
  workload/       sanitized query_log CSV grouping and workload risk prototype
  mcp_server/     stdio MCP tools and prompts over the same pipeline
```

## Analysis pipeline

### 1. Input normalization

CLI and MCP convert user input into `QueryContext`:

- `sql`
- optional `schema_ddl`
- optional `explain_output`
- optional `ch_version`

CLI can also detect `ch_version` from `--connect` using the ClickHouse HTTP API.
MCP exposes the same capability as the `detect_ch_version` tool.

### 2. Rule selection and version filtering

`clickadvisor.rules.registry.get_applicable_rules(ch_version)` returns rules
that apply to the requested ClickHouse version. If the version is unknown, all
rules are allowed and the report records no version skips.

Rule tiers:

- `1A`: formally equivalent rewrites that can be recommended confidently
- `1B`: approximate / opt-in guidance such as approximate aggregation variants
- `1C`: conditional rewrites that depend on context or preconditions
- `detector`: diagnostic signals that do not necessarily produce a rewrite
- `rag`: retrieval-only documentation context, never a primary rule finding

### 3. Rule engine

Each rule receives `QueryContext` and may return a `Finding` with:

- `rule_id`, `rule_name`, `tier`, `severity`
- human description and suggestion
- optional `example_before` / `example_after`
- optional `explain_why`
- optional `impact_estimate`
- optional `rewritten_sql`

Findings are sorted by severity before optional advisory findings are appended.

### 4. EXPLAIN ESTIMATE comparator

When CLI analysis is run with both `--connect` and `--explain-estimate`, the
pipeline receives an `ExplainComparator`. For rule findings with `example_after`
and tier `1A`, `1B`, or `1C`, the comparator executes:

```sql
EXPLAIN ESTIMATE <original SQL>
EXPLAIN ESTIMATE <example_after SQL>
```

The parser supports both default tabular output and `FORMAT JSON`. The comparator
aggregates `rows` and `marks`, then formats a conservative planner-impact string
such as:

```text
Строк до: 1,000,000 | после: 10,000 | сокращение: 100× (оценка планировщика CH)
```

Errors are logged and do not fail the analysis.

### 5. Retrieval advisory

If `.qdrant_db` exists and retrieval is enabled, `RetrievalAdvisor` builds a
semantic query from the primary findings and retrieves relevant KB chunks from
embedded Qdrant.

Key properties:

- default collection: `clickadvisor_kb`
- default embedding model: `multilingual-e5-small`
- optional indexing model: `minilm-l6`
- default retrieval threshold: `0.65`
- score diversity guard: if top-3 scores are effectively identical, only the
  first result is returned and a warning is logged
- RAG findings use `tier="rag"` and are rendered in a separate documentation
  section

Retrieval is advisory context only. It does not change rule correctness.

### 6. Report building

The final `Report` is rendered as:

- Rich console output
- JSON (`report_to_json_dict` / `render_json`)
- Markdown (`render_markdown` / `format_report_markdown`)
- MCP `TextContent`

Console and Markdown keep RAG documentation separate from rule findings. JSON
preserves fields useful for automation, including `impact_estimate` and
`rewritten_sql` when present.

## CLI flow

```text
chadvisor analyze
  ├─ read SQL / schema / explain file
  ├─ detect CH version if --connect and no --ch-version
  ├─ optionally create RetrievalAdvisor if .qdrant_db exists
  ├─ optionally create ExplainComparator if --explain-estimate and --connect
  ├─ run AnalysisPipeline
  └─ render console | json | markdown
```

`chadvisor index-kb` builds the Qdrant retrieval index from `data/kb/chunks/`.
It refuses to overwrite an existing index unless `--reindex` is supplied.

`chadvisor workload` reads a sanitized `system.query_log` CSV export, groups
queries by normalized fingerprint, runs representative SQL through the same rule
engine, and renders a top-N workload risk report.

`chadvisor mcp-server` starts the stdio MCP server.

## MCP flow

The MCP server exposes tools:

- `analyze_query`
- `analyze_query_json`
- `list_rules`
- `detect_ch_version`

It also exposes prompts:

- `analyze`
- `explain`

MCP tools use the same `AnalysisPipeline`. The JSON tool intentionally excludes
RAG findings so downstream automation receives deterministic rule findings.

## Knowledge base and embeddings

The KB pipeline lives under `data/kb/` and `scripts/kb/`:

1. crawl sources into raw artifacts
2. normalize to Markdown
3. chunk into frontmatter-bearing Markdown files
4. index chunks into embedded Qdrant

Embedding model selection is documented in
[`ADR-013`](./adr/ADR-013-embedding-model-selection.md). The default remains
`multilingual-e5-small` for multilingual future KB/query coverage even though
`all-MiniLM-L6-v2` performed best on the current English-heavy ablation.

## Evaluation hooks

- `scripts/eval/run_benchmark.py` evaluates deterministic rule detection on
  synthetic benchmark cases.
- `scripts/eval/ablation_embeddings.py` compares retrieval embedding models via
  MRR@3 over synthetic cases and KB chunks.
- `scripts/lab/` contains the risk-label DS dataset, feature, split, baseline,
  and error-analysis pipeline.
- `chadvisor workload --query-log examples/query_log_sample.csv` smoke-tests the
  workload prototype.
- `tests/explain/` covers EXPLAIN ESTIMATE parsing and comparison.
- `tests/test_mcp_server.py` covers MCP tool and prompt handlers.

## Future evolution

Likely extensions after v1.0:

- full-index retrieval ablation and version-aware retrieval filters
- richer schema-aware rewrite validation
- more Tier 2 cost-model rules using `system.parts` and `EXPLAIN ESTIMATE`
- packaging for published `chadvisor` binary and MCP use without Poetry
- optional UI wrapper that still delegates to the same core pipeline
