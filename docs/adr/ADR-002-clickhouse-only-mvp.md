# ADR-002: ClickHouse Only in MVP; PostgreSQL in Backlog

## Status

Accepted

## Context

The project is being developed under a constrained first implementation window.
Within that window, the team must prove that the product can deliver real value
through a combination of engine-aware rule logic, cost-based reasoning, and a
clear trust contract. That kind of proof requires depth, not broad
checklist-style support across multiple databases.

Database optimization is only superficially portable. At the SQL surface,
multiple engines share familiar constructs such as predicates, joins,
aggregations, and projections. But the moment the product needs to explain why a
query is expensive and what change is likely to help, engine-specific storage
and execution details dominate. For ClickHouse, those details include sparse
primary keys, granules, marks, MergeTree parts, partition pruning, projections,
and `PREWHERE` behavior. For PostgreSQL, the relevant mental model shifts toward
different planner behavior, row-store access methods, statistics models,
indexing choices, and observability patterns. A tool that tries to cover both
deeply from the beginning is almost guaranteed to flatten both into generic
advice.

The competitive landscape reinforces this point. PostgreSQL already has mature
adjacent products and a relatively dense ecosystem of query analysis and tuning
guidance, including pganalyze, EverSQL, and pgMustard. That does not make
PostgreSQL unimportant, but it does mean that a new product has less room to be
meaningfully differentiated there in the short term. ClickHouse, by contrast,
has no comparably established advisor product with the positioning ClickAdvisor
is aiming for. The whitespace is larger, but it can only be captured by being
genuinely specific to ClickHouse internals rather than by presenting generic SQL
optimizations with a ClickHouse label.

There is also a product quality risk in a dual-engine MVP. Supporting both
ClickHouse and PostgreSQL from day one would not merely double implementation
load. It would multiply complexity across parsing, feature engineering, rule
taxonomy, metadata adapters, examples, benchmark design, documentation, and test
fixtures. Every architecture choice would be under pressure to abstract early,
even when the right abstraction is not yet known. That tends to produce the
worst of both worlds: a broad but shallow interface that looks extensible yet
encodes neither engine well.

The project does want a story for future extensibility. Long term, the design
should not trap the team in a ClickHouse-only codebase that cannot admit a
second engine. However, “must not preclude extension” is not the same as “must
support multiple engines in the first six weeks.” The right balance is to
architect with boundaries that could support multiple engines later while
deliberately delivering only one real engine in the MVP.

## Decision

ClickAdvisor will support only ClickHouse during the first six weeks of MVP
development.

During this phase, the product, benchmark design, documentation, and rule engine
are all optimized for ClickHouse-specific behavior. The project is explicitly
allowed to use concepts, terminology, heuristics, and metadata contracts that
would not generalize cleanly to PostgreSQL without a separate adapter layer.

PostgreSQL is placed in backlog status.

At most, in the final week of the initial implementation window, the project may
include an optional proof-of-extensibility artifact for PostgreSQL. That artifact
is not full product support. It is limited to demonstrating that the core
architecture can admit another engine through a bounded adapter layer without
rewriting the system. It may take the form of:

- a skeletal dialect or engine abstraction
- a minimal parser or context adapter
- a single placeholder rule path

It must not be represented as production-ready PostgreSQL support.

The product messaging and code organization therefore prioritize:

- ClickHouse-first domain depth
- engine-specific rule semantics
- deliberate postponement of second-engine breadth

## Scope решения: только анализ SQL-кода в MVP

### Decision

MVP фокусируется исключительно на анализе SQL-запросов. Анализ
конфигурации сервера (`config.xml`, `users.xml`) и hardware spec (`CPU`,
`RAM`, диски) выносится в backlog как отдельная фича v2.

### Что убрано из MVP

- Environment rules (`E-001..E-011`)
- Парсинг server config и hardware spec
- Environment Adjuster слой в архитектуре
- CLI флаги `--hardware` и `--config`

### Что остаётся

- Tier 1: 18 формально-эквивалентных rewrite-правил
- Tier 2: 12 cost-based рекомендаций по индексам и проекциям
- Detectors: 13 детекторов антипаттернов
- LLM-агент с RAG по документации CH

### Consequences

Фокус на SQL-анализе даёт более глубокое покрытие главной боли DBA.
Environment rules добавляются в v2 как killer feature после валидации
core-функционала с реальными пользователями.

## Consequences

The strongest consequence is focus. The team can spend the first implementation
window learning and encoding the details that actually matter for ClickHouse
query performance instead of building abstractions for hypothetical portability.
That should improve the quality of Tier 1 and Tier 2 logic, the benchmark
relevance, and the clarity of user-facing explanations.

This decision also sharpens product differentiation. Rather than competing
immediately in the saturated PostgreSQL tooling space, ClickAdvisor can position
itself as the advisor built for a database that is operationally important yet
under-served by optimization tooling. That is strategically useful because it
aligns the technical architecture with a clearer market narrative.

From an implementation perspective, documentation can be more precise. The
glossary, ADRs, rule catalog, and examples are allowed to use ClickHouse-native
terms without constantly generalizing them away. This reduces ambiguity and
makes the system easier to reason about internally.

There is a tradeoff: some potential users may ask early why PostgreSQL is not
also supported, especially because many SQL advisory products start by claiming
multi-engine reach. The project accepts that tradeoff. The intent is to earn the
right to expand by first proving quality in one engine where specificity matters
most.

Another consequence is that future extensibility must be architectural rather
than marketing-driven. The team should still keep engine boundaries visible in
the codebase where it is cheap and honest to do so, but it should not introduce
premature “universal SQL” abstractions that hide real differences between
engines. The proof-of-extensibility, if built, is a discipline tool, not a
feature promise.

## Alternatives Considered

### Support ClickHouse and PostgreSQL from the beginning

This was rejected because it would spread the first six weeks too thin. The
project would be forced to divide effort across two planner models, two metadata
surfaces, two ecosystems, and two sets of benchmark assumptions before either
path had enough depth to demonstrate differentiated value. The likely result
would be generic advice dressed up as multi-engine support.

### Target ANSI SQL only

This was rejected because the most valuable optimization guidance in both
ClickHouse and PostgreSQL is not ANSI-generic. A tool limited to ANSI-common
patterns would miss the storage and execution realities that make the product
useful. For ClickHouse especially, stripping away engine-specific semantics
would remove the very rules that justify building the product at all.
