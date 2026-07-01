# Workload Analyzer

`chadvisor workload` is a prototype for moving ClickAdvisor from single-query
review to workload-level prioritization.

The command reads a sanitized CSV export from `system.query_log`, groups similar
queries by normalized SQL fingerprint, runs the representative query through the
deterministic rule engine, and ranks the groups by rule severity plus observed
resource metrics.

It does not connect to ClickHouse, execute SQL, read result data, or call an
external LLM.

## Input

The CSV should include a query text column and any available metric columns.

Supported query columns:

- `query`
- `sql`
- `normalized_query`

Supported metric columns:

- `query_duration_ms`, `duration_ms`, `elapsed_ms`
- `read_rows`, `rows_read`, `rows`
- `read_bytes`, `bytes_read`, `bytes`
- `memory_usage`, `peak_memory_usage`, `memory_usage_bytes`

Minimal export shape:

```csv
event_time,query,query_duration_ms,read_rows,read_bytes,memory_usage
2026-07-01 10:00:00,"SELECT * FROM events FINAL WHERE message LIKE '%timeout%'",1200,900000,180000000,220000000
```

## Run

```bash
poetry run chadvisor workload \
  --query-log examples/query_log_sample.csv \
  --output-format markdown \
  --top-n 3
```

To save the report:

```bash
poetry run chadvisor workload \
  --query-log examples/query_log_sample.csv \
  --output-format markdown \
  --output workload-report.md
```

JSON output is available for automation:

```bash
poetry run chadvisor workload \
  --query-log examples/query_log_sample.csv \
  --output-format json
```

## Example Output

```text
Top Performance Risks

1. Fingerprint 283ec787aa90fb0a
   Priority: high
   Executions: 2
   Total duration: 2180 ms
   Avg / p95 duration: 1090.0 / 1189 ms
   Read rows / bytes: 1750000 / 350000000
   Max memory: 220000000
   Findings: 5
   Rule IDs: D-003, D-004, D-005, D-007, R-102
```

## Prioritization

The prototype priority score combines:

- deterministic rule severity from ClickAdvisor findings;
- total query duration;
- total read bytes;
- peak memory usage;
- execution count.

This is intentionally conservative. It is a review-queue signal, not a claim
that ClickAdvisor has measured a guaranteed speedup.

## Privacy Boundary

For the safest workflow, export only metadata and normalized SQL. Literals can
be redacted before the CSV reaches ClickAdvisor. The command itself normalizes
literals for grouping, but upstream redaction is still recommended for strict
enterprise environments.

Recommended read-only export columns:

```sql
SELECT
    event_time,
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    memory_usage
FROM system.query_log
WHERE type = 'QueryFinish'
  AND event_time >= now() - INTERVAL 1 DAY
FORMAT CSVWithNames
```

The future production version should add live `--connect`, time windows,
identifier hashing, stricter redaction modes, and ranking metrics such as
Precision@K and NDCG@K.
