---
source: kb.altinity.com
url: https://packages.timber.io/vector/0.15.2/vector_0.15.2-1_arm64.deb
topic: transforming-clickhouse-logs-to-ndjson-using-vector-dev-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 2
---

= "basic" auth.user = "vector" auth.password = "vector1234" healthcheck = true table = "clickhouse_logs" encoding.timestamp_format = "unix" buffer.type = "disk" buffer.max_size = 104900000 buffer.when_full = "block" request.in_flight_limit = 20 encoding.only_fields = ["host", "timestamp", "thread_id", "query_id", "severity", "message"] ```

```
select * from default.clickhouse_logs limit 10;
┌───────────────timestamp─┬─host───────┬─thread_id─┬─severity─┬─query_id─┬─message─────────────────────────────────────────────────────
│ 2022-04-21 19:08:13.443 │ clickhouse │ 283155    │ Debug    │          │ HTTP-Session: 13e87050-7824-46b0-9bd5-29469a1b102f Authentic
│ 2022-04-21 19:08:13.443 │ clickhouse │ 283155    │ Debug    │          │ HTTP-Session: 13e87050-7824-46b0-9bd5-29469a1b102f Authentic
│ 2022-04-21 19:08:13.443 │ clickhouse │ 283155    │ Debug    │          │ HTTP-Session: 13e87050-7824-46b0-9bd5-29469a1b102f Creating
│ 2022-04-21 19:08:13.447 │ clickhouse │ 283155    │ Debug    │          │ MemoryTracker: Peak memory usage (for query): 4.00 MiB.
│ 2022-04-21 19:08:13.447 │ clickhouse │ 283155    │ Debug    │          │ HTTP-Session: 13e87050-7824-46b0-9bd5-29469a1b102f Destroyin
│ 2022-04-21 19:08:13.495 │ clickhouse │ 283155    │ Debug    │          │ HTTP-Session: f7eb829f-7b3a-4c43-8a41-a2e6676177fb Authentic
│ 2022-04-21 19:08:13.495 │ clickhouse │ 283155    │ Debug    │          │ HTTP-Session: f7eb829f-7b3a-4c43-8a41-a2e6676177fb Authentic
│ 2022-04-21 19:08:13.495 │ clickhouse │ 283155    │ Debug    │          │ HTTP-Session: f7eb829f-7b3a-4c43-8a41-a2e6676177fb Creating
│ 2022-04-21 19:08:13.496 │ clickhouse │ 283155    │ Debug    │          │ MemoryTracker: Peak memory usage (for query): 4.00 MiB.
│ 2022-04-21 19:08:13.496 │ clickhouse │ 283155    │ Debug    │          │ HTTP-Session: f7eb829f-7b3a-4c43-8a41-a2e6676177fb Destroyin
└─────────────────────────┴────────────┴───────────┴──────────┴──────────┴─────────────────────────────────────────────────────────────

```
Last modified 2024\.08\.13: [Fixed multiple typos here and there (9fb2290\)](https://github.com/Altinity/altinityknowledgebase/commit/9fb2290fbebcd92a3f79a7f321f13960ea89ebec)
