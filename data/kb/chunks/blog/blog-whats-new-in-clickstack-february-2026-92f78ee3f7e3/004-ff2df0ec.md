---
source: blog
url: https://github.com/AdityaPimpalkar
topic: what-s-new-in-clickstack-february-26
ch_version_introduced: '0.99'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 10
---

'error' 22 GROUP BY ServiceName 23 ) 24SELECT 25 coalesce(Traces.ServiceName, Errors.ServiceName) AS ServiceName, 26 avg_duration, 27 p99_duration, 28 error_log_count 29FROM Traces 30FULL OUTER JOIN Errors 31 ON Traces.ServiceName = Errors.ServiceName 32ORDER BY ServiceName 33LIMIT 200; ``` ``` ![](/uploads/clickstack_feb2026_image4_27bbe951f5.png)

> In raw SQL mode, users select just a connection. There's no need to specify a data source, unlike the Query Builder, with users free to query across multiple data sources at once.

Or consider a lightweight service map style view. A self JOIN on spans can show request counts between service pairs, total errors, and percentage error rates (also available visually within [our service map feature](https://clickhouse.com/blog/whats-new-in-clickstack-november-2025#service-maps)). This kind of relationship analysis would be extremely difficult to model coherently in a visual builder, but is straightforward in SQL:

```

```
1WITH
2  ServerSpans AS (
3    SELECT TraceId AS traceId,
4           SpanId AS spanId,
5           ServiceName AS serviceName,
6           ParentSpanId AS parentSpanId,
7           StatusCode AS statusCode
8    FROM otel_v2.otel_traces
9    WHERE SpanKind IN ('Server', 'Consumer', 'SPAN_KIND_SERVER', 'SPAN_KIND_CONSUMER') AND
10     Timestamp >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
11      AND Timestamp < fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
12  ),
13  ClientSpans AS (
14    SELECT TraceId AS traceId,
15           SpanId AS spanId,
16           ServiceName AS serviceName,
17           ParentSpanId AS parentSpanId,
18           StatusCode AS statusCode
19    FROM otel_v2.otel_traces
20    WHERE SpanKind IN ('Client', 'Producer', 'SPAN_KIND_CLIENT', 'SPAN_KIND_PRODUCER') AND 
21    Timestamp >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
22      AND Timestamp <= fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
23  )
24SELECT
25  ServerSpans.serviceName AS serverServiceName,
26  ClientSpans.serviceName AS clientServiceName,
27  count(*) * 10 AS requestCount,
28  countIf(ServerSpans.statusCode = 'Error') AS error_count,
29  round(error_count / requestCount, 3) AS `% error count`
30FROM ServerSpans
31LEFT JOIN ClientSpans
32  ON ServerSpans.traceId = ClientSpans.traceId
33  AND ServerSpans.parentSpanId = ClientSpans.spanId
34WHERE ClientSpans.serviceName IS NULL
35   OR ServerSpans.serviceName != ClientSpans.serviceName
36GROUP BY serverServiceName, clientServiceName
37ORDER BY serverServiceName, clientServiceName;
```

```

![](/uploads/clickstack_feb2026_image6_5a88b2c3c7.png)
This is the first step toward combining the simplicity of guided builders with the full expressiveness of SQL, giving advanced users the freedom to unlock everything ClickHouse can do. Stay tuned over the following months to see SQL being exposed in other visualizations.

## Metric Attribute Explorer [\#](/blog/whats-new-in-clickstack-february-2026#metric-attribute-explorer)
