# ADR-009: Technology Stack Selection Rationale

## Status

Accepted

## Context

ClickAdvisor needs a stack that is practical for rapid iteration, rich enough to
support SQL parsing and machine-learning components, and mature enough to run in
local-first enterprise workflows. The project combines several unusual
requirements in one tool: engine-specific SQL analysis, deterministic rule
evaluation, cost-model reasoning, lightweight classification, optional
retrieval, optional local and remote LLM support, and a CLI-first user
experience. The selected stack must therefore balance ecosystem strength,
implementation speed, deployment reality, and future extensibility.

The decision is not about choosing the most fashionable component in each
category. It is about choosing tools that fit the shape of the product and the
constraints already fixed by other ADRs. In particular, the stack must support:

- Python-centric ML and data tooling
- ClickHouse SQL parsing with good dialect coverage
- small, explainable, tabular classification models
- multilingual retrieval support
- local-first inference options
- ergonomic CLI development

Because the project is in early development, the team also values low ceremony
and fast prototyping. A technically “purer” stack that dramatically slows
implementation or fragments the ecosystem would work against the current stage of
the product.

## Decision

ClickAdvisor standardizes on the following technology stack for the MVP phase:

- Python 3.11
- `sqlglot` for SQL parsing with ClickHouse dialect support
- CatBoost for problem classification
- BGE-M3 for embeddings
- Qdrant for retrieval
- Typer and Rich for the CLI layer
- Ollama for local LLM execution
- Anthropic SDK for remote LLM access

The reasons for each choice, along with the main alternatives considered, are
recorded below.

### Python 3.11

Python 3.11 is selected because it provides the fastest path to combining SQL
tooling, ML components, retrieval libraries, and LLM integrations in one code
base. The surrounding ecosystem for `sqlglot`, CatBoost, embedding pipelines,
and API clients is significantly more mature and composable in Python than in
lower-level alternatives.

Rust and Go were considered. Both were rejected for the MVP because they would
slow down iteration on ML- and LLM-adjacent workflows and would require more
custom glue for parsing, modeling, and experimentation. They remain reasonable
targets for performance-sensitive subcomponents later, but not for the initial
system.

### `sqlglot`

`sqlglot` is selected because it already supports the ClickHouse dialect and
provides a practical AST transformation surface for static SQL analysis and
redaction. It is well suited to a system that needs both rule-oriented rewrite
logic and syntax-aware manipulation of queries.

ANTLR-based custom grammars and generic SQL parsers were considered. They were
rejected because they either increase maintenance burden substantially or do not
offer the same combination of dialect support and rewrite ergonomics for
ClickHouse-specific use.

### CatBoost

CatBoost is selected for the problem classifier because it handles categorical
features well without requiring large one-hot pipelines, works well on tabular
data, and supports relatively compact models that fit the MVP’s lightweight
classification need. This aligns with the planned feature space, which is likely
to mix structural, categorical, and environment-derived signals.

XGBoost and LightGBM were considered. They were rejected because, while strong
general-purpose boosters, they are less convenient for the expected categorical
feature profile and do not offer a clear enough advantage to offset CatBoost’s
fit for this use case.

### BGE-M3

BGE-M3 is selected as the embedding model because it offers strong open
multilingual performance, which matters for a tool whose users, docs, and
internal notes may not be purely English. It provides a credible open baseline
for retrieval tasks without pushing the product toward a closed embedding stack.

OpenAI embeddings and smaller sentence-transformer variants were considered.
Closed remote embeddings were rejected because they conflict with the local-first
posture, and lighter open alternatives were rejected because the project values a
stronger multilingual retrieval baseline from the outset.

### Qdrant

Qdrant is selected for retrieval because it is operationally straightforward,
implemented in Rust, and offers an embedded-friendly story that fits local-first
deployment patterns. It provides a cleaner path for shipping retrieval in a tool
that may need to run entirely on a user-controlled host.

FAISS and Chroma were considered. FAISS was rejected because it is a lower-level
library rather than a convenient end-to-end retrieval store for this workflow.
Chroma was rejected because Qdrant offers a stronger operational fit and clearer
path for local and service modes.

### Typer + Rich

Typer and Rich are selected because together they provide excellent Python CLI
ergonomics with minimal ceremony. Typer makes command definition and help text
clean, while Rich gives the project high-quality terminal rendering for reports,
tables, emphasis, and future diagnostics.

Click and argparse were considered. `argparse` was rejected because it adds more
manual friction for a product expected to grow a polished CLI surface. Raw Click
was rejected because Typer preserves Click’s power while giving a more modern
developer experience and cleaner type-driven command definitions.

### Ollama

Ollama are selected as the local LLM execution backends because they
cover complementary operational needs: vLLM is strong for efficient hosted local
serving, while Ollama is convenient for lightweight developer and workstation
setups. Together they support the `--llm=local` mode without committing the
project to one hosting shape.

llama.cpp-only and custom Transformers runtime paths were considered. They were
rejected for the MVP because they either narrow the operational envelope too
much or increase runtime integration burden relative to the value they provide.

### Anthropic SDK

The Anthropic SDK is selected as the initial remote LLM integration because it
is a direct fit for the chosen remote advisory path and offers a clean Python
integration story. The project may also support OpenAI-compatible remote paths,
but Anthropic is the explicitly recorded baseline.

Building first on generic HTTP wrappers alone was rejected because the MVP
benefits from official client ergonomics and faster iteration. Deferring remote
support entirely was also rejected because some users will prefer remote
advisory capability once redaction is in place.

## Consequences

The selected stack gives the project a coherent Python-first implementation path
with good support for SQL analysis, ML experimentation, retrieval, and CLI UX.
It also keeps the architecture aligned with other ADRs: local-first operation,
explicit LLM modes, and ClickHouse-aware parsing.

There is a tradeoff in dependency weight. Components such as CatBoost, embedding
pipelines, and local LLM backends are non-trivial. The team accepts that because
the stack is chosen for capability fit, not minimal package count. The CLI and
core architecture will need to keep optional components modular so that not
every deployment path bears every dependency cost at runtime.

## Alternatives Considered

### Polyglot stack with Rust core and Python sidecars

This was rejected for the MVP because it would add coordination and integration
cost too early. The project benefits more from fast unified iteration than from
early language-level partitioning.

### Pure remote-AI-oriented stack

This was rejected because it would conflict with the local-first architecture and
would weaken the product’s claim that meaningful functionality exists without
mandatory external inference services.
