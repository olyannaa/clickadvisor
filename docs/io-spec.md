# ClickAdvisor I/O Specification

This document defines the canonical input and output formats for ClickAdvisor.

The goal of the specification is to make every ingestion path explicit,
machine-checkable, and reproducible in CI and benchmark workflows.

The constraints from the project ADRs apply throughout:

- ClickAdvisor does not read table data
- ClickAdvisor does not run `ANALYZE`
- ClickAdvisor consumes SQL, plans, schema, metadata, settings, and hardware
  context only
- Outputs preserve trust tier semantics

## 1. SQL Input

### Purpose

SQL input is the primary analysis target. It may be supplied as:

- a single `.sql` file
- stdin
- an inline string

### Accepted format

- UTF-8 encoded text
- ClickHouse SQL dialect
- one or more statements separated by semicolons
- comments are allowed and preserved for diagnostics, but analysis is performed
  on the parsed statement tree

### Statement handling rules

- CTEs are allowed and treated as part of the owning statement
- multi-statement files are accepted, but only analyzable statements are passed
  into the rule pipeline
- non-query statements may be parsed for schema context but are not analyzed as
  optimization targets unless a future mode explicitly allows it
- comments are ignored for rewrite logic

### `.sql` file contract

Recommended conventions:

- one primary analyzable query per file for benchmark cases
- optional setup DDL in separate files or clearly separated blocks
- use `;` as delimiter for multi-statement input

### Valid input example

```sql
WITH recent AS (
    SELECT user_id, event_time
    FROM analytics.events
    WHERE event_time >= toDateTime('2026-05-01 00:00:00')
)
SELECT count(DISTINCT user_id)
FROM recent;
```

### Invalid input example

```sql
SELECT count(DISTINCT user_id)
FROM analytics.events
WHERE event_time >=
```

Reason:

- incomplete expression
- parser cannot build a valid AST

### Edge cases

#### CTE chains

Supported as long as the full statement parses in ClickHouse dialect.

#### Multi-statement input

Valid example:

```sql
SET max_threads = 8;
SELECT count() FROM analytics.events;
```

Handling:

- `SET` may be recorded as context
- `SELECT` is the optimization target

#### Comments between tokens

Valid example:

```sql
SELECT
    count(DISTINCT user_id) -- distinct users
FROM analytics.events;
```

Handling:

- comments do not affect semantic analysis
- comments may be preserved in input echo or diagnostics

#### Unsupported dialect constructs

If a file mixes non-ClickHouse SQL that cannot be parsed in ClickHouse dialect,
the file is rejected with a parse error and location hint.

## 2. EXPLAIN Output Input

### Purpose

ClickAdvisor accepts ClickHouse `EXPLAIN` output to enrich Tier 2 and
environment-aware analysis.

### Supported modes

- `EXPLAIN json=1, description=1, header=1 SELECT ...`
- `EXPLAIN PLAN json=1 SELECT ...`
- `EXPLAIN PIPELINE json=1 SELECT ...`
- `EXPLAIN ESTIMATE json=1 SELECT ...`
- `EXPLAIN indexes=1, json=1 SELECT ...`

The preferred transport format is JSON saved as `.json`.

### Canonical wrapper format

ClickAdvisor expects explain artifacts in the following envelope:

```json
{
  "statement_id": "main",
  "explain_kind": "ESTIMATE",
  "generated_at": "2026-05-25T10:20:30Z",
  "clickhouse_version": "25.3.2.5",
  "payload": {
    "Plan": {
      "Node Type": "ReadFromMergeTree",
      "Description": "analytics.events",
      "Plans": []
    }
  }
}
```

### Valid input example

```json
{
  "statement_id": "main",
  "explain_kind": "PLAN",
  "generated_at": "2026-05-25T10:20:30Z",
  "clickhouse_version": "25.3.2.5",
  "payload": {
    "Plan": {
      "Node Type": "Expression",
      "Description": "Projection + Before ORDER BY",
      "Plans": [
        {
          "Node Type": "ReadFromMergeTree",
          "Description": "analytics.events"
        }
      ]
    }
  }
}
```

### Invalid input example

```json
{
  "kind": "PLAN",
  "payload": "read from table"
}
```

Reason:

- required envelope fields missing
- `payload` must preserve structured JSON, not a plain string

### Edge cases

#### PLAN vs PIPELINE vs ESTIMATE

Handling:

- `PLAN` feeds operator-tree reasoning
- `PIPELINE` feeds execution-stage heuristics
- `ESTIMATE` feeds cost-model inference
- `indexes=1` enriches pruning/index visibility

#### Non-JSON EXPLAIN

Plain text explain output is not canonical. It may be supported later through a
best-effort parser, but the current contract expects JSON.

#### Partial or truncated payload

If the JSON parses but required inner nodes are absent, the artifact is accepted
as partial context and marked degraded.

## 3. Schema Input

### Purpose

Schema input communicates table structure, engines, ordering keys, partition
keys, and related DDL context.

### Accepted format

- one or more `CREATE TABLE` statements
- optional `CREATE VIEW`, `CREATE MATERIALIZED VIEW`, `CREATE DICTIONARY`
- UTF-8 `.sql` text

### Metadata extraction targets

ClickAdvisor extracts, where available:

- database and table name
- engine type
- column names and types
- `ORDER BY`
- `PRIMARY KEY`
- `PARTITION BY`
- `SAMPLE BY`
- TTL clauses
- projections
- settings block

### Valid input example

```sql
CREATE TABLE analytics.events
(
    event_date Date,
    event_time DateTime,
    user_id UInt64,
    event_type LowCardinality(String)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, user_id)
SETTINGS index_granularity = 8192;
```

### Invalid input example

```sql
CREATE TABLE analytics.events
(
    event_date Date
    user_id UInt64
)
ENGINE = MergeTree
ORDER BY (event_date);
```

Reason:

- invalid column list syntax

### Edge cases

#### Multiple table definitions

Allowed. The analyzer matches referenced tables by name.

#### Missing target table DDL

Accepted as degraded context. Tier 1 rules may still run if independent of
schema; Tier 2 and `env` rules may be limited.

#### Non-MergeTree engines

Accepted, but some rules may be suppressed or downgraded if they depend on
MergeTree semantics.

## 4. `hardware.yaml` Input

### Purpose

Hardware input allows environment-aware recommendations such as thread-related
guidance, disk-pressure annotations, and topology-sensitive caveats.

### YAML schema

```yaml
type: object
required:
  - cpu
  - memory
  - disks
  - network
  - cluster_topology
properties:
  cpu:
    type: object
    required: [physical_cores, logical_cores, model]
  memory:
    type: object
    required: [total_gb]
  disks:
    type: array
  network:
    type: object
  cluster_topology:
    type: object
```

### Canonical example

```yaml
cpu:
  model: "AMD EPYC 7R13"
  physical_cores: 32
  logical_cores: 64
  frequency_ghz: 2.45
memory:
  total_gb: 256
  channels: 8
disks:
  - name: "nvme0n1"
    type: "nvme"
    capacity_gb: 1900
    read_mbps: 6400
    write_mbps: 5100
  - name: "sda"
    type: "hdd"
    capacity_gb: 8000
    read_mbps: 240
    write_mbps: 180
network:
  bandwidth_gbps: 25
  intra_az_latency_ms_p50: 0.7
cluster_topology:
  shards: 4
  replicas_per_shard: 2
  distributed_queries: true
```

### Invalid example

```yaml
cpu: "32 cores"
memory: 256
```

Reason:

- wrong types
- missing required sections

### Edge cases

- partial hardware is allowed only if the ingestion mode explicitly supports
  degraded environment analysis
- disks may be heterogeneous
- single-node deployments should still specify `cluster_topology`

## 5. `clickhouse-config.xml` Input

### Purpose

Configuration input captures server settings that affect rule applicability,
pruning behavior, parallelism, joins, and memory policy.

### Parsed sections

ClickAdvisor may parse:

- `/clickhouse/profiles/*`
- `/clickhouse/users/*/profile`
- `/clickhouse/logger`
- `/clickhouse/macros`
- `/clickhouse/merge_tree`
- `/clickhouse/remote_servers`
- `/clickhouse/settings`

### Important extracted settings

Examples include:

- `max_threads`
- `max_memory_usage`
- `max_bytes_before_external_group_by`
- `max_bytes_before_external_sort`
- `join_algorithm`
- `allow_experimental_projection_optimization`
- `use_skip_indexes`
- `max_block_size`
- `max_execution_time`

### Valid input example

```xml
<clickhouse>
  <profiles>
    <default>
      <max_threads>16</max_threads>
      <max_memory_usage>34359738368</max_memory_usage>
      <join_algorithm>auto</join_algorithm>
    </default>
  </profiles>
  <merge_tree>
    <max_suspicious_broken_parts>5</max_suspicious_broken_parts>
  </merge_tree>
</clickhouse>
```

### Invalid input example

```xml
<clickhouse>
  <profiles>
    <default>
      <max_threads>16
    </default>
  </profiles>
</clickhouse>
```

Reason:

- malformed XML

### Edge cases

- multiple profiles may exist; the active one must be identified externally or
  assumed through input metadata
- absent settings are treated as unknown, not defaulted silently
- custom settings may be preserved as opaque metadata

## 6. `stats.json` Input

### Purpose

`stats.json` packages metadata dumps from system tables used for cost-aware and
environment-aware analysis.

### Canonical shape

```json
{
  "captured_at": "2026-05-25T10:30:00Z",
  "clickhouse_version": "25.3.2.5",
  "system.parts": [],
  "system.columns": [],
  "system.tables": []
}
```

### Required per-table payload intent

#### `system.parts`

Important fields:

- `database`
- `table`
- `partition`
- `name`
- `active`
- `rows`
- `bytes_on_disk`
- `data_compressed_bytes`
- `data_uncompressed_bytes`
- `marks`
- `modification_time`

#### `system.columns`

Important fields:

- `database`
- `table`
- `name`
- `type`
- `default_kind`
- `default_expression`
- `data_compressed_bytes`
- `data_uncompressed_bytes`

#### `system.tables`

Important fields:

- `database`
- `name`
- `engine`
- `total_rows`
- `total_bytes`
- `metadata_modification_time`
- `sorting_key`
- `primary_key`
- `partition_key`

### Valid input example

```json
{
  "captured_at": "2026-05-25T10:30:00Z",
  "clickhouse_version": "25.3.2.5",
  "system.parts": [
    {
      "database": "analytics",
      "table": "events",
      "partition": "202605",
      "name": "all_42_42_0",
      "active": 1,
      "rows": 18422311,
      "bytes_on_disk": 954301224,
      "data_compressed_bytes": 710122334,
      "data_uncompressed_bytes": 4030048177,
      "marks": 2251,
      "modification_time": "2026-05-25 09:15:00"
    }
  ],
  "system.columns": [],
  "system.tables": []
}
```

### Invalid input example

```json
{
  "system.parts": "exported rows"
}
```

Reason:

- wrong top-level types
- missing envelope fields

### Edge cases

- missing `system.columns` or `system.tables` should be treated as degraded
  metadata, not as fatal when `system.parts` is present
- mixed versions of metadata fields should be normalized at ingest
- numeric strings should be coerced only through explicit normalization

## 7. Report Output JSON Schema

### Purpose

The final report is the canonical structured output of ClickAdvisor. Console and
Markdown renderings are derived from this report.

### Top-level schema

```yaml
type: object
required:
  - report_version
  - generated_at
  - analyzer_version
  - llm_mode
  - input_summary
  - findings
  - summary
properties:
  report_version:
    type: string
  generated_at:
    type: string
    format: date-time
  analyzer_version:
    type: string
  llm_mode:
    type: string
    enum: [none, local, remote]
  input_summary:
    type: object
  findings:
    type: array
  summary:
    type: object
```

### Finding variants

#### `rule_match`

Use for rule-backed findings from tiers `1A`, `1B`, `1C`, or `2`.

Required fields:

- `finding_id`
- `finding_type: rule_match`
- `rule_id`
- `tier`
- `title`
- `severity`
- `confidence`
- `statement_ref`
- `evidence`
- `recommendation`

#### `env_suggestion`

Use for environment-sensitive recommendations not expressed as SQL rewrites.

Required fields:

- `finding_id`
- `finding_type: env_suggestion`
- `title`
- `severity`
- `environment_scope`
- `evidence`
- `recommendation`

#### `advisory`

Use for LLM-backed or otherwise advisory outputs.

Required fields:

- `finding_id`
- `finding_type: advisory`
- `tier`
- `title`
- `confidence`
- `verification_required`
- `evidence`
- `recommendation`

### Canonical output example

```json
{
  "report_version": "1.0.0",
  "generated_at": "2026-05-25T10:41:00Z",
  "analyzer_version": "0.1.0",
  "llm_mode": "none",
  "input_summary": {
    "statements_total": 1,
    "target_statements": 1,
    "schema_tables_seen": 1,
    "explain_kinds": ["ESTIMATE"]
  },
  "findings": [
    {
      "finding_id": "F-001",
      "finding_type": "rule_match",
      "rule_id": "R-001",
      "tier": "1A",
      "title": "Use a specialized distinct aggregate",
      "severity": "medium",
      "confidence": 0.98,
      "statement_ref": "main",
      "evidence": {
        "matched_pattern": "count(DISTINCT user_id)",
        "plan_signals": ["ReadFromMergeTree"],
        "metadata_signals": []
      },
      "recommendation": {
        "before_sql": "SELECT count(DISTINCT user_id) FROM analytics.events",
        "after_sql": "SELECT uniqExact(user_id) FROM analytics.events",
        "notes": ["Equivalent under the rule catalog contract."]
      }
    }
  ],
  "summary": {
    "findings_total": 1,
    "by_tier": {
      "1A": 1
    },
    "estimated_cost_reduction": "low_to_medium"
  }
}
```

### Invalid output example

```json
{
  "report_version": "1.0.0",
  "findings": [
    {
      "title": "Maybe faster"
    }
  ]
}
```

Reason:

- missing required envelope fields
- finding type is not specified
- no tier or evidence contract

### Edge cases

#### No findings

Valid output must still include:

- full envelope
- empty `findings`
- summary with `findings_total: 0`

#### Partial context

If some inputs are missing, the report should carry degraded-context notes in
`input_summary` or finding evidence rather than fail silently.

#### Multiple statements

`statement_ref` must identify which SQL statement a finding belongs to.

## 8. Error handling conventions

Across all input formats:

- parse errors should include file, section, and location when available
- unsupported but well-formed input should produce a typed compatibility error
- partial context should degrade analysis rather than fail if the remaining
  inputs are still useful
- fatal errors are reserved for malformed primary inputs, not for optional
  enrichments
