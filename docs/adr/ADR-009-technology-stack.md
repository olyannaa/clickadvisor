# ADR-009: Technology Stack Selection Rationale

## Status

Accepted

## Context

ClickAdvisor needs a stack that supports local ClickHouse SQL analysis,
version-aware rule evaluation, retrieval over documentation, CLI usage, and an
MCP interface for AI-agent workflows. The stack must match what the codebase
actually runs today: deterministic rules first, optional retrieval context, and
no generative LLM execution in the MVP critical path.

The project includes a classical ML problem classifier for evaluation
experiments. Heavy model libraries should stay tied to those scripts and
reports, not become an implied runtime requirement for the rule engine.

## Decision

ClickAdvisor MVP standardizes on:

- Python 3.11+ for implementation and evaluation scripts;
- `sqlglot` for ClickHouse SQL parsing and AST analysis;
- Typer and Rich for the CLI;
- `sentence-transformers` for local embedding models;
- Qdrant embedded mode for local vector retrieval;
- `mcp` for the stdio MCP server;
- `httpx` / `requests` for ClickHouse HTTP API and KB crawling;
- pytest, Hypothesis, Ruff, and mypy for development quality.

The MVP intentionally does not depend on Anthropic, Ollama, vLLM, or other
generative LLM runtimes. CatBoost is used only as a classifier ablation backend
when available in the evaluation environment; Logistic Regression and Random
Forest remain the portable classical baselines.

### Python 3.11+

Python provides the fastest path to combine SQL parsing, CLI development,
retrieval, and future ML experiments in one codebase. Rust and Go remain viable
for future performance-sensitive components, but they would slow down the MVP.

### `sqlglot`

`sqlglot` supports the ClickHouse dialect well enough for AST-based static
analysis. It gives rules a structured representation of functions, predicates,
subqueries, and set operations without maintaining a custom grammar.

### Typer + Rich

Typer keeps the CLI typed and compact; Rich makes terminal reports readable for
DBA workflows. This combination is simpler and more polished than raw `argparse`
for a growing command surface.

### `sentence-transformers`

The retrieval layer uses local sentence-transformer models. The default model is
`intfloat/multilingual-e5-small`; `all-MiniLM-L6-v2` is available as a faster
alternative for English-heavy KB experiments. This matches the implemented
indexer and ablation script.

### Qdrant

Qdrant is used in embedded mode for local vector search over KB chunks. It keeps
retrieval local-first and avoids requiring an external vector database service
for normal development and demos.

### MCP

MCP is selected as the AI-agent integration surface. Claude Desktop, Cursor, and
similar clients can call ClickAdvisor as a tool, while ClickAdvisor keeps its
analysis deterministic and auditable.

## Consequences

The dependency graph becomes easier to defend: every heavy dependency has a
current code path. The project no longer claims internal LLM modes that are not
implemented.

ML classifier dependencies and SOTA/baseline rationale must remain tied to code,
datasets, and evaluation reports. That keeps technical claims tied to
reproducible experiments.

## Alternatives Considered

### Keep planned LLM and CatBoost dependencies before implementation

Rejected because unused dependencies create a visible mismatch between product
claims and code. They make the project look broader but less technically honest.

### Build retrieval on a remote embedding API

Rejected because remote embeddings conflict with the local-first posture and
zero data egress story.

### Remove MCP and expose only CLI

Rejected because MCP is already implemented and is the right way to let AI
agents use the analyzer without putting a generative model inside the analyzer.
