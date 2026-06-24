# Evaluation Plan

This document defines how ClickAdvisor quality is measured, compared, and
reported for v1.0 and later releases.

ClickAdvisor has three evaluation surfaces:

1. deterministic rule quality
2. retrieval advisory quality
3. integration quality for CLI, EXPLAIN ESTIMATE, and MCP

## 1. Evaluation goals

The evaluation framework must answer these questions:

1. Does the system detect the right problem type?
2. Does it fire the right rule with the right tier semantics?
3. Does version filtering suppress rules that should not apply?
4. Does retrieval return documentation that helps explain the fired rules?
5. Does EXPLAIN ESTIMATE produce conservative before/after impact summaries?
6. Are CLI and MCP interfaces behaviorally consistent?
7. Is runtime latency acceptable for local and CI usage?

## 2. Primary metrics

### Per-rule precision and recall

For each rule in scope:

- precision = true positive matches / all matches emitted for the rule
- recall = true positive matches / all benchmark cases where the rule should
  have fired

This is the main unit for rule-catalog evolution because it reveals which rules
are trustworthy and which ones over-trigger or under-trigger.

### System-level F1

Aggregate F1 is measured over problem-type detection and overall finding
quality.

Recommended reporting:

- macro F1 across problem categories
- micro F1 across all benchmark cases
- by-tier breakdown (`1A`, `1B`, `1C`, `detector`)

Current synthetic benchmark command:

```bash
poetry run python scripts/eval/run_benchmark.py
```

The curated 20-case synthetic benchmark currently targets perfect rule coverage
in lenient mode, where additional valid detector findings are not penalized.

### Retrieval MRR@3

Retrieval quality is measured by mean reciprocal rank at 3 (`MRR@3`) over
synthetic benchmark cases.

Command:

```bash
poetry run python scripts/eval/ablation_embeddings.py
```

The ablation script:

- compares `multilingual-e5-small`, `all-MiniLM-L6-v2`, and
  `paraphrase-multilingual-MiniLM-L12-v2`
- indexes the first 2000 KB chunks for fast local comparison
- reports model size, MRR@3, elapsed time, and a recommendation
- removes temporary `.qdrant_ablation_*` directories after the run

Latest documented 500-chunk result used for ADR-013:

| Model | Size | MRR@3 | Notes |
|---|---:|---:|---|
| `multilingual-e5-small` | 117 MB | 0.38 | default, multilingual |
| `all-MiniLM-L6-v2` | 80 MB | 0.53 | best on English-heavy KB |
| `paraphrase-multilingual-MiniLM-L12-v2` | 420 MB | 0.30 | multilingual, larger |

The default remains multilingual E5 because future KB sources and user queries
include Russian. See `docs/adr/ADR-013-embedding-model-selection.md`.

### EXPLAIN ESTIMATE impact quality

For recommendations with rewrites, ClickAdvisor can attach planner-estimated
impact:

- rows reduction factor
- marks reduction factor
- rows reduction percentage

This is not a measured runtime speedup. It should be interpreted as a
planner-visible work estimate. Regression tests cover parser and comparator
behavior under `tests/explain/`.

### MCP integration correctness

The MCP server is tested as a protocol adaptation layer:

- `analyze_query` returns Markdown containing rule findings
- `analyze_query_json` returns structured JSON findings
- `list_rules` returns grouped rule catalog text
- `detect_ch_version` returns either a version or a useful failure message
- `list_prompts` exposes `analyze` and `explain`

Command:

```bash
poetry run pytest tests/test_mcp_server.py -v
```

### Latency

Measure end-to-end latency for:

- parse + rule analysis
- retrieval advisory with existing `.qdrant_db`
- EXPLAIN ESTIMATE with reachable ClickHouse HTTP endpoint
- MCP tool call overhead

Latency should be reported at:

- p50
- p95
- max

## 3. Datasets

### Curated benchmark in `/benchmark/cases/`

Primary benchmark target: approximately 100 hand-curated cases.

Current v1.0 synthetic subset: 20 validated cases under
`benchmark/cases/synthetic/`.

This dataset should contain:

- positive and negative rule cases
- multi-issue queries
- degraded-context cases
- environment-sensitive cases
- false-friend cases where a naive rewrite should not trigger

### Knowledge base chunks in `/data/kb/chunks/`

Retrieval evaluation uses chunked documentation and KB material. The repository
currently contains roughly 8804 chunks. Fast ablation indexes 2000 chunks; full
index experiments are expected to improve MRR@3.

### TPC-H, ClickBench, JOB Benchmark

These remain secondary reference workloads for future broader validation:

- TPC-H for recognizable analytical query shapes
- ClickBench for ClickHouse-style scans and aggregations
- JOB for join/subquery robustness after ClickHouse adaptation

## 4. Baselines

### Raw LLM without rule engine

Use a baseline prompt that gives the same query and context to an LLM without
ClickAdvisor. This isolates the value of deterministic rules, version filtering,
and explicit tiers.

### R-Bot / EverSQL

Where legally and operationally permissible, compare against external advisors.
Record exact commit, endpoint, invocation template, and output normalization.

Remote baselines must not receive private customer data.

## 5. Reproducible procedure

### Step 1: Freeze the code snapshot

Before each benchmark run, record:

- git commit SHA
- dirty/clean working tree state
- analyzer version
- dependency lock snapshot

### Step 2: Freeze the benchmark selection

Record:

- case IDs included
- dataset source
- ClickHouse version used for metadata generation
- any environment overlays
- KB chunk count and embedding model for retrieval experiments

### Step 3: Run ClickAdvisor

For each case:

- ingest SQL and optional context bundle
- run analysis in the target mode
- persist raw report JSON
- persist compact summary rows for aggregation

### Step 4: Run retrieval ablations when relevant

For each embedding model:

- build a temporary Qdrant index
- query synthetic cases
- score MRR@3
- persist model name, size, chunk count, and elapsed time

### Step 5: Run baselines

For each baseline:

- execute with same or equivalent input bundle
- normalize outputs into comparable labels
- store raw and normalized outputs separately

### Step 6: Score

Compute:

- per-rule precision/recall
- system-level F1
- retrieval MRR@3
- EXPLAIN ESTIMATE impact summaries
- latency summaries

### Step 7: Persist results

All evaluation outputs should be saved under:

```text
/eval/results/<run_id>/
```

Each run directory should contain:

- `metadata.json`
- `system_metrics.json`
- `per_rule_metrics.json`
- `retrieval_metrics.json` when applicable
- `latency.json`
- `baseline_outputs/`
- `clickadvisor_outputs/`

## 6. Interpretation guidance

- A higher finding count is not inherently better.
- Tier confusion is a quality issue, not just a UI issue.
- Retrieval findings are documentation context, not proof of correctness.
- EXPLAIN ESTIMATE reductions are estimates, not runtime speedups.
- Latency should be interpreted together with retrieval and ClickHouse endpoint
  availability.

## 7. Minimum viable evaluation cadence

Recommended cadence:

- on each major rule batch: run curated benchmark subset
- before release: run `pytest -k 'not test_detect_version'`
- before retrieval changes: run embedding ablation on the current KB slice
- before MCP changes: run `tests/test_mcp_server.py`
- before milestone demo: regenerate benchmark and ablation tables
