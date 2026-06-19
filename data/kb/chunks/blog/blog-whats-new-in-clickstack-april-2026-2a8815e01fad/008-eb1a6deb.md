---
source: blog
url: https://clickhouse.com/blog/whats-new-in-clickstack-march-2026#sql-charts-with-grafana-style-macros
topic: what-s-new-in-clickstack-april-2026
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 10
---

for compatible rollups and wires them into autocomplete if available. The default Docker, Helm, and embedded deployments already create these views automatically. The rollup combines all three OTel attribute maps alongside a handful of commonly queried native columns:

```

```
1CREATE MATERIALIZED VIEW IF NOT EXISTS otel_logs_attr_kv_rollup_15m_mv
2TO otel_logs_kv_rollup_15m
3AS WITH elements AS (
4  SELECT 'ResourceAttributes' AS ColumnIdentifier,
5         toStartOfFifteenMinutes(Timestamp) AS Timestamp,
6         replaceRegexpAll(entry.1, '\[\d+\]', '[*]') AS Key,
7         CAST(entry.2 AS String) AS Value
8  FROM otel_logs ARRAY JOIN ResourceAttributes AS entry
9  UNION ALL
10  SELECT 'LogAttributes' AS ColumnIdentifier, ...
11  FROM otel_logs ARRAY JOIN LogAttributes AS entry
12  UNION ALL
13  SELECT 'ScopeAttributes' AS ColumnIdentifier, ...
14  FROM otel_logs ARRAY JOIN ScopeAttributes AS entry
15  UNION ALL
16  SELECT 'NativeColumn' AS ColumnIdentifier,
17         toStartOfFifteenMinutes(Timestamp) AS Timestamp,
18         'SeverityText' AS Key,
19         CAST(SeverityText AS String) AS Value
20  FROM otel_logs
21  -- similar UNION ALL branches for ServiceName, ScopeName, etc.
22)
23SELECT Timestamp, ColumnIdentifier, Key, Value, count() AS count
24FROM elements
25GROUP BY Timestamp, ColumnIdentifier, Key, Value;
```

```

These rollups mean autocomplete latency drops substantially on larger datasets. As an added bonus, suggestions are now frequency\-ranked, which generally produces better defaults in the dropdown.

## Heatmaps as a first\-class chart type [\#](/blog/whats-new-in-clickstack-april-2026#heatmaps-as-a-first-class-chart-type)

Last month, we [shipped several improvements to Event Deltas](https://clickhouse.com/blog/whats-new-in-clickstack-march-2026#improvements-for-event-deltas), including always\-on baseline distributions, proportional comparison scoring, filter and exclude actions from attribute comparison bars, and deterministic heatmap sampling. One limitation remained, though: the heatmap renderer was available only within the Event Deltas search workflow. If users wanted to visualize latency distributions elsewhere in the product, there was no way to reuse them.

In April, we moved the heatmap renderer into the shared charting system used by dashboards and the chart editor, allowing heatmaps to be available everywhere charts can be created.

From the chart editor, users select the Heatmap tab, define a `WHERE` clause and value expression, and the same distribution view previously limited to Event Deltas can now be added directly to dashboards.

![](/uploads/clickstack_apr2026_image6_bb7af03abf.png)
For Trace sources, ClickStack automatically initializes the chart with a duration expression and `count()` aggregation. The Y\-axis also switches into duration formatting automatically, so labels render as milliseconds, seconds, or minutes instead of raw numeric values.
