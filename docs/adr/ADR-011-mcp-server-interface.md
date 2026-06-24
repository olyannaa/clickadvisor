# ADR-011: MCP Server as Secondary Interface

## Status

Accepted

## Context

The primary ClickAdvisor interaction model remains the CLI. That is still the
best fit for DBA workflows, local-first operation, reproducible CI runs, and
batch-style usage. However, many technically sophisticated users now invoke
specialized tools from assistant-driven environments through the Model Context
Protocol (MCP).

If a DBA already works inside Claude Desktop, Cursor, Continue, or another
MCP-capable client, manually moving SQL between the assistant and a standalone
binary adds friction. Exposing ClickAdvisor through MCP lets the same local rule
engine participate in those workflows without turning the product into an
LLM-only interface.

The key risk is logic drift. MCP must not become a second implementation of the
advisor. It should adapt protocol messages into the existing core pipeline and
return structured text/JSON results.

## Decision

ClickAdvisor includes a stdio MCP server as a secondary interface layered over
the same core analysis engine used by the CLI.

The CLI remains primary. MCP exists to reduce integration friction for users who
already operate in LLM+tooling environments.

The implementation split is:

- `clickadvisor/core/` — analysis models and `AnalysisPipeline`
- `clickadvisor/rules/` — deterministic rule and detector implementations
- `clickadvisor/retrieval/` — optional RAG advisory support
- `clickadvisor/explain/` — optional `EXPLAIN ESTIMATE` impact support
- `clickadvisor/cli/` — primary command-line interface
- `clickadvisor/mcp_server/` — thin MCP protocol adapter

The MCP server exposes tools:

- `analyze_query` — Markdown report for ClickHouse SQL
- `analyze_query_json` — structured JSON for automation
- `list_rules` — rule catalog grouped by tier
- `detect_ch_version` — version detection through ClickHouse HTTP API

The MCP server also exposes prompts:

- `analyze`
- `explain`

`analyze_query` documentation explicitly instructs clients to pass known
ClickHouse versions through `ch_version` and to call `detect_ch_version` first
when the conversation mentions a cluster address.

## Consequences

Users gain a second access path that fits assistant-driven workflows while the
engineering team preserves one source of truth for analysis. The MCP layer can
be tested independently as protocol adaptation, but rule behavior stays in the
core pipeline.

There is added packaging and documentation overhead: the project must support
CLI commands, MCP tools, MCP prompts, and connection examples. This cost is
accepted because the MCP server remains small and local-first.

MCP `analyze_query_json` intentionally omits RAG findings so programmatic
consumers receive deterministic rule findings. Human-oriented `analyze_query`
may include retrieval documentation context when a local `.qdrant_db` exists.

## Alternatives Considered

### Make MCP the only interface

Rejected because CI/CD, shell workflows, and explicit local invocation remain
core DBA use cases.

### Duplicate CLI logic inside MCP

Rejected because duplicated logic would drift and produce inconsistent advice.

### Postpone MCP indefinitely

Rejected because MCP is already a practical workflow surface for target users.
A thin local wrapper gives adoption benefit without compromising architecture.
