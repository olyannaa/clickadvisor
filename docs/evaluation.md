# Evaluation Plan

This document defines how ClickAdvisor quality is measured, compared, and
reported.

The evaluation plan follows the architecture and product constraints already
accepted in ADRs:

- trust tiers matter
- cost-model estimates matter more than replay theater
- user utility matters alongside offline benchmark quality

## 1. Evaluation goals

The evaluation framework must answer five questions:

1. Does the system detect the right problem type?
2. Does it fire the right rule with the right tier semantics?
3. Do Tier 2 recommendations correlate with estimated cost reduction?
4. Does the tool help DBA reach diagnosis faster?
5. Is runtime latency acceptable for local and CI usage?

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
- by-tier breakdown

### Average estimated cost reduction for Tier 2

Tier 2 recommendations are not judged by measured speedup. They are judged by
estimated reduction in planner-visible work, such as reduced rows, marks,
projection of lower read volume, or lower expected memory pressure.

Recommended summary statistics:

- mean estimated cost reduction
- median estimated cost reduction
- p25 / p75 distribution

### Time-to-diagnosis in user study

For the DBA user study:

- measure elapsed time from case presentation to correct diagnosis
- compare baseline workflow vs ClickAdvisor-assisted workflow
- record qualitative confidence and trust feedback separately

### Latency

Measure end-to-end latency:

- parse + ingest latency
- analysis latency
- report rendering latency
- total latency by LLM mode (`none`, `local`, `remote`)

Latency should be reported at:

- p50
- p95
- max

## 3. Datasets

### Curated benchmark in `/benchmark/cases/`

Primary benchmark target: approximately 100 hand-curated cases.

This dataset should contain:

- positive and negative rule cases
- multi-issue queries
- degraded-context cases
- environment-sensitive cases
- false-friend cases where a naive rewrite should not trigger

### TPC-H

Use TPC-H query shapes as a secondary general workload reference for:

- join patterns
- aggregation shapes
- subquery behavior

TPC-H is not sufficient on its own, but it is useful as a recognizable external
baseline dataset.

### ClickBench

Use ClickBench for:

- realistic ClickHouse-style analytical queries
- columnar scan pressure patterns
- engine-specific read and aggregation workloads

### JOB Benchmark

Use JOB Benchmark where useful for:

- join-order and subquery-heavy patterns
- robustness checks against broader SQL query structures

Because ClickAdvisor is ClickHouse-first, JOB cases may require adaptation or
careful interpretation rather than literal drop-in use.

## 4. Baselines

### R-Bot

Use the public R-Bot repository and workflow as a comparison point where
possible. The evaluation must document:

- exact commit or release used
- prompt or invocation template
- output normalization strategy

### EverSQL

Use a public endpoint or evaluation-access path only where legally and
operationally permissible. Record:

- request parameters
- returned recommendations
- normalization method for mapping outputs to benchmark labels

### Raw Claude API without rule engine

Use a baseline prompt that gives the same query and context to Claude without
the ClickAdvisor rule engine. This comparison isolates the value of:

- explicit rule tiers
- formal rule matching
- deterministic context handling

Where a remote baseline is used, preserve exact prompt templates in the eval
artifact directory.

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

### Step 3: Run ClickAdvisor

For each case:

- ingest the SQL and context bundle
- run analysis in the target mode
- persist the raw report JSON
- persist a compact summary row for aggregation

### Step 4: Run baselines

For each baseline:

- execute with the same or equivalent input bundle
- normalize outputs into comparable labels
- store raw and normalized outputs separately

### Step 5: Score

Compute:

- per-rule precision/recall
- system-level F1
- Tier 2 cost-reduction aggregates
- latency summaries

### Step 6: User study

For user-study runs:

- randomize case ordering
- measure time-to-diagnosis
- record correctness and confidence
- collect short qualitative notes on trust and usability

### Step 7: Persist results

All evaluation outputs must be saved under:

- `/eval/results/<run_id>/`

Each run directory should contain:

- metadata.json
- system_metrics.json
- per_rule_metrics.json
- latency.json
- baseline_outputs/...
- clickadvisor_outputs/...
- plots/...

The run metadata must include the git snapshot of the utility version used.

## 6. Output tables and graphs

Recommended presentation artifacts:

### F1 vs baselines

- bar chart: ClickAdvisor vs R-Bot vs EverSQL vs raw Claude
- include macro F1 and micro F1

### Per-tier contribution to total findings

- stacked bar chart by tier
- optionally broken down by benchmark subset

### Latency distribution

- histogram or violin plot per LLM mode
- p50/p95 overlays

### User-study results

- box plot for time-to-diagnosis
- correctness rate by workflow
- qualitative theme summary table

### Per-rule performance table

Columns:

- rule_id
- tier
- precision
- recall
- support count
- notes

## 7. Interpretation guidance

- A higher finding count is not inherently better.
- Tier confusion is a quality issue, not just a UI issue.
- Latency should be interpreted together with LLM mode and context richness.
- Average estimated cost reduction should never be presented as measured runtime
  speedup.

## 8. Minimum viable evaluation cadence

Recommended cadence:

- on each major rule batch: run curated benchmark subset
- weekly: run full curated benchmark
- before milestone demo: regenerate baseline comparisons and presentation plots
- before publishing results: rerun user-study summary and verify git snapshot

## 9. Open implementation notes

- Output normalization for external baselines must be explicitly versioned.
- Baseline prompts and adapters should live in source control.
- User-study protocols should be documented before data collection begins.
- Synthetic and curated cases should be labeled separately in analysis.
