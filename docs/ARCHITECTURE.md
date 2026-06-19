# ClickAdvisor Architecture

This document describes the high-level architecture for the ClickAdvisor MVP.

The system is intentionally CLI-first, ClickHouse-first, and local-first. Its
job is to analyze SQL plus execution context and produce recommendations with an
explicit trust tier.

## Design constraints

- Primary interface is CLI
- MVP supports ClickHouse only
- LLM usage is optional and mode-gated
- No `ANALYZE` execution and no customer data inspection
- Recommendations must preserve tier attribution

## Layered pipeline

ClickAdvisor is organized into seven functional layers.

### 1. Ingest

Responsible for collecting the user-provided SQL and static environment inputs.

Inputs may include:

- raw SQL text
- schema definitions
- `EXPLAIN` output without `ANALYZE`
- table metadata and `system.parts` snapshots
- server settings and config fragments
- hardware characteristics relevant to execution heuristics

The Ingest layer normalizes these sources into a stable internal contract.

### 2. Context Builder

Builds the analysis context from heterogeneous inputs.

Responsibilities:

- reconcile SQL text with available schema metadata
- map storage-level context to referenced tables
- attach engine settings and environment constraints
- mark missing evidence so downstream layers can degrade gracefully

This layer should make uncertainty explicit instead of guessing.

### 3. Feature Extractor

Derives machine- and rule-consumable features from SQL and environment context.

Typical feature families:

- AST structure from `sqlglot`
- predicate placement and pushdown opportunities
- projection, partition, and primary-key alignment
- join shape and aggregation patterns
- read amplification and pruning indicators
- settings or hardware-sensitive hints

### 4. Problem Classifier

Classifies likely optimization issues based on extracted features.

The classifier is not the final authority on rewrites. It is a routing and
prioritization component that helps decide which rule families or analyses to
run next.

Likely implementation direction:

- CatBoost-based supervised classifier
- interpretable feature importance where useful
- probability outputs used for ranking, not for proof

### 5. Rewrite Engine

The Rewrite Engine is the core decision layer and is split into three tiers.

#### Tier 1: formally equivalent

This tier contains mathematically grounded rewrites derived from relational
algebra and ClickHouse-safe invariants.

Properties:

- semantic equivalence is required
- assumptions must be explicit
- output should cite the exact rule identity

#### Tier 2: cost-based

This tier proposes changes that are not purely algebraic but can be justified
through ClickHouse-aware cost signals.

Evidence sources include:

- `EXPLAIN ESTIMATE`
- `system.parts`
- table shape and storage metadata
- environment characteristics

Outputs from this tier are framed as estimates, not proofs.

#### Tier 3: LLM advisory

This tier can generate hypotheses, explanations, or candidate rewrites.

Hard constraint:

- every materially actionable suggestion must be verified before surfacing as
  trusted advice

The LLM may run in one of three modes:

- `--llm=none`
- `--llm=local`
- `--llm=remote`

### 6. Environment Adjuster

Adjusts rankings and wording based on deployment reality.

Examples:

- down-rank advice that conflicts with available evidence
- reflect hardware-sensitive tradeoffs
- annotate when recommendations depend on missing metadata
- adapt suggestions to settings that may disable a technique

This layer prevents technically true advice from becoming operationally naive.

### 7. Report Builder

Produces the final CLI-facing analysis artifact.

The report should make the trust contract obvious:

- what issue was detected
- which tier produced the advice
- what evidence supported it
- what rewrite or action is recommended
- what assumptions or caveats apply

## End-to-end flow

```text
+-------------------+
|  User SQL / CLI   |
+---------+---------+
          |
          v
+-------------------+
|      Ingest       |
+---------+---------+
          |
          v
+-------------------+
|  Context Builder  |
+---------+---------+
          |
          v
+-------------------+
| Feature Extractor |
+---------+---------+
          |
          v
+-------------------+
| Problem Classifier|
+---------+---------+
          |
          v
+-------------------+
|  Rewrite Engine   |
|-------------------|
| Tier 1: Formal    |
| Tier 2: Cost      |
| Tier 3: LLM+Verify|
+---------+---------+
          |
          v
+-------------------+
|Environment Adjust.|
+---------+---------+
          |
          v
+-------------------+
|  Report Builder   |
+---------+---------+
          |
          v
+-------------------+
| CLI Output Report |
+-------------------+
```

## Architectural implications

This architecture intentionally separates:

- proof from estimation
- estimation from narration
- analysis from presentation

That separation is essential for trust. A DBA should be able to distinguish a
proven rewrite from a plausible suggestion without reverse-engineering the tool.

## Future evolution

Likely extensions after MVP scaffolding:

- rule catalog with proof notes
- benchmark harness for curated optimization cases
- retrieval-backed documentation references
- richer report formats and diff views
- optional web wrapper around the CLI core
