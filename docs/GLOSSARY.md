# ClickAdvisor Glossary

This glossary defines key ClickHouse and ClickAdvisor terms that will be used in
future ADRs, rule specs, benchmark descriptions, and user-facing reports.

## A

### AggregatingMergeTree

A MergeTree-family engine optimized for storing aggregate states and merging
them over time. Relevant when advice touches pre-aggregation strategy and
materialized views.

## C

### Cost model

An internal estimation framework used by ClickAdvisor to approximate the impact
of a recommendation. In this project, quality is evaluated primarily through
estimated cost reduction rather than measured runtime speedup.

## D

### Data skipping index

An auxiliary index structure that helps ClickHouse skip reading irrelevant data
blocks. It is distinct from the sparse primary key and can influence pruning
quality for certain predicates.

## E

### `EXPLAIN ESTIMATE`

ClickHouse explain mode that provides estimated read and processing information
without running the query in `ANALYZE` mode. This is a key evidence source for
Tier 2 recommendations.

## G

### Granule

The smallest logical read unit tracked by ClickHouse sparse indexing. A granule
typically contains a range of rows and is the unit over which many pruning
decisions are reasoned about.

In ClickAdvisor, granule-level reasoning matters because poor predicate
alignment can force unnecessary granule reads even when a query appears
selective at the SQL level.

## M


### MCP (Model Context Protocol)

A protocol for exposing local tools to AI-agent clients. ClickAdvisor provides a
stdio MCP server with tools for SQL analysis, JSON analysis, rule listing, and
ClickHouse version detection.

### Mark

A storage pointer associated with a granule in MergeTree-family tables. Marks
allow ClickHouse to jump to approximate positions in column files instead of
scanning from the beginning.

Rules that discuss read amplification, mark ranges, or pruning behavior rely on
this concept.

### Materialized view

A precomputed transformation pipeline in ClickHouse that persists derived data.
It can improve query performance but changes write-time cost and maintenance
complexity.

### MergeTree part

A physical chunk of data stored by a MergeTree-family table. Parts are created
by inserts and merges and are central to understanding storage layout,
compaction state, and read behavior.

Metadata from `system.parts` is one of the main inputs for Tier 2 analysis.

## P

### Partition

A logical grouping of data parts based on the partition key expression. Good
partitioning can reduce the amount of data touched by a query, but poor
partitioning can create fragmentation or operational overhead.

### PREWHERE

A ClickHouse optimization stage that allows early filtering before reading all
requested columns. Proper `PREWHERE` usage can reduce I/O when selective
predicates target a small subset of columns.

ClickAdvisor may recommend predicate movement or query restructuring when it
improves the likelihood of effective `PREWHERE` execution.

### Primary key (sparse)

In ClickHouse MergeTree tables, the primary key is a sparse index over marks,
not a row-level uniqueness constraint in the OLTP sense.

This distinction is critical. A query can "use the primary key" and still read
many rows if predicate alignment with the sort order is poor.

### Projection

A physically stored alternative data layout for a table, designed to accelerate
specific query patterns. Projections can behave like engine-managed
pre-optimizations for frequent access paths.

Projection-aware advice must consider maintenance cost, freshness, and whether
the optimizer can actually use the projection for the target query.

## Q

### Query rewrite

A transformation from one SQL formulation to another. In ClickAdvisor, rewrites
must be labeled by trust tier:

- Tier 1 for formally equivalent transformations
- Tier 2 for cost-based recommendations
- Tier 3 for speculative advisory suggestions with verification

## R


### Retrieval advisory

A documentation-backed advisory layer that retrieves relevant KB chunks from an
embedded Qdrant index. Retrieval findings use `tier="rag"` and provide context,
not proof of rule correctness.

### Read amplification

The mismatch between the amount of data logically needed and the amount of data
physically scanned or loaded. In ClickHouse this is often influenced by sort-key
alignment, partition pruning, mark selectivity, and column access patterns.

### Relational algebra equivalence

A transformation property stating that two query expressions are semantically
equivalent under defined assumptions. This is the basis for Tier 1 rules.

## S

### `system.parts`

A ClickHouse system table exposing metadata about table parts, including size,
row counts, activity state, and storage-level details. It is a foundational
evidence source for understanding MergeTree layout.

### Sort key

The ordering key used by MergeTree-family tables to physically organize data.
It strongly influences sparse-index effectiveness and scan locality.

Sort key alignment is one of the most important engine-specific concepts for
query optimization in ClickHouse.

## T

### Tier 1

The highest-confidence recommendation tier in ClickAdvisor. Tier 1 outputs are
reserved for formally equivalent rewrites supported by explicit assumptions.

### Tier 2

The cost-based recommendation tier. Outputs rely on metadata and estimation
signals such as `EXPLAIN ESTIMATE` and `system.parts`, not purely on algebraic
proof.

### Tier 3

The advisory tier. This is where LLM assistance may contribute candidate ideas
or explanations, but only with mandatory verification before trusted output is
presented.

## V

### Verification

The process of checking whether a candidate recommendation is safe, consistent
with available evidence, and appropriately labeled by trust tier. Verification
is mandatory for materially actionable Tier 3 outputs.

## W

### Wide part / compact part

Storage layouts used by ClickHouse for parts depending on data shape and
configuration. The distinction can affect read behavior, merge costs, and how
storage-level heuristics should be interpreted.

## Working definitions for this project

The glossary will evolve, but several project-level definitions are already
fixed:

- ClickAdvisor is CLI-first
- MVP targets ClickHouse only
- Local-first operation is the default
- LLM usage is optional and mode-gated
- Evaluation focuses on estimated cost reduction plus benchmark precision and
  recall

These definitions should be treated as stable references in future ADRs unless a
new decision explicitly revises them.
