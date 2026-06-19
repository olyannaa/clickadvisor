# What's new in ClickStack \- April 2026


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# What's new in ClickStack \- April 2026

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_white_add9f20d0f.png&w=96&q=75)[The ClickStack Team](/authors/the-clickstack-team)May 19, 2026 · 17 minutes readWelcome to the April edition of What's New in ClickStack.


April was a release focused on tightening the core experience across querying, alerting, and dashboards.


SQL\-powered alerts landed this month, rounding out the SQL\-native observability workflow we [started building last month](https://clickhouse.com/blog/whats-new-in-clickstack-march-2026#sql-charts-with-grafana-style-macros). You can now move from writing queries and building dashboards directly into alerting, without switching query languages or maintaining separate rule pipelines.


Under the hood, we also redesigned the default logs schema around ClickHouse's text index. Combined with a follow\-up optimization for map attribute filtering, this delivers up to Nx faster performance in our benchmarks for common search and filtering workloads.


Autocomplete also got a major overhaul. Metadata discovery now runs through materialized\-view rollups behind the scenes, making suggestions feel substantially faster and more responsive, especially on larger datasets.


Heatmaps are now a first\-class chart type available anywhere in dashboards, instead of being limited to Event Deltas. This makes it much easier to visualize latency distributions, density, and outliers directly alongside the rest of your operational views.


Alongside the larger changes, April also included a long list of quality\-of\-life improvements across alerting, table layouts, pie charts, and per\-series number formatting.


## Open House [\#](/blog/whats-new-in-clickstack-april-2026#open-house)


If you're attending [Open House](https://clickhouse.com/openhouse/san-francisco), we'll also have a dedicated observability track this year with talks from several ClickStack developers and contributors, alongside customer sessions from teams covering how they're running observability workloads on ClickHouse in production.


If you can't make it live, all sessions will be recorded and published afterward.


## Contributing [\#](/blog/whats-new-in-clickstack-april-2026#contributing)


As always, thank you to our open source contributors and users whose feedback continues to shape ClickStack.


If code contributions are not your thing, we welcome documentation improvements, ideas, feature suggestions, bug reports, and general feedback via the [repository](https://github.com/hyperdxio/hyperdx/tree/v2). Every contribution, big or small, helps make the stack better for the entire community.

### Get started today

Interested in seeing how ClickHouse works on your observability data? Get started with Managed ClickStack in ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?intent=o11y&loc=blog-cta-647-get-started-today-sign-up&utm_blogctaid=647)## Alerts on raw SQL charts [\#](/blog/whats-new-in-clickstack-april-2026#alerts-on-raw-sql-charts)


SQL alerting introduces a first\-class way to express observability logic that doesn't fit inside a query builder. Users can now build charts and alerts directly from arbitrary ClickHouse SQL queries, unlocking more advanced analysis directly inside the ClickStack UI.


Static thresholding works fine until teams start doing anything even slightly statistical. Rolling baselines, percentile drift, grouped anomaly checks, or historical comparisons all become awkward once the alert itself is constrained by a UI model. In practice, many users ended up pushing advanced alerting logic into external systems or custom pipelines despite already storing the data in ClickHouse.


SQL alerting builds directly on the [SQL charting support introduced last month](https://clickhouse.com/blog/whats-new-in-clickstack-march-2026#sql-charts-with-grafana-style-macros). Once arbitrary SQL could be expressed in dashboards and visualizations, extending this into alerting became a natural next step.


SQL queries for alerts can be used to compute rolling baselines over previous intervals, calculate standard deviation bands, and compare current behavior against historical trends. Beyond this, queries can encapsulate even more complex conditions. For example, queries can emit `1` only when something becomes anomalous. The alert itself then becomes extremely simple: trigger when the query returns `1`, with the query capturing the conditions.


ClickHouse window functions make these kinds of workflows straightforward to express. For example, this query builds a rolling statistical baseline for error volume and returns `1` whenever the current interval deviates significantly from recent historical behavior.



```

```
1WITH buckets AS (
2  SELECT
3    $__timeInterval(Timestamp) AS ts,
4    count() AS bucket_count
5  FROM $__sourceTable
6  WHERE Timestamp >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
7                     - toIntervalSecond($__interval_s * 30)
8    AND Timestamp < fromUnixTimestamp64Milli({endDateMilliseconds:Int64})
9    AND SeverityText = 'error'
10    AND $__filters
11  GROUP BY ts
12  ORDER BY ts
13  WITH FILL STEP toIntervalSecond($__interval_s)
14),
15baselines AS (
16  SELECT
17    ts,
18    bucket_count,
19    avg(bucket_count) OVER (
20      ORDER BY ts ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
21    ) AS rolling_avg,
22    stddevPop(bucket_count) OVER (
23      ORDER BY ts ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
24    ) AS rolling_stddev
25  FROM buckets
26)
27SELECT
28  ts,
29  if(bucket_count > rolling_avg + 2 * rolling_stddev, 1, 0) AS anomaly
30FROM baselines
31WHERE rolling_avg IS NOT NULL
32  AND ts >= fromUnixTimestamp64Milli({startDateMilliseconds:Int64})
33ORDER BY ts ASC;
```

```

![](/uploads/clickstack_apr2026_image2_6ceaa5360e.png)
Alerts also support the same `$__filters`, `$__sourceTable`, and `{intervalSeconds:Int64}` macros already used by SQL visualizations, including Grafana\-compatible interval handling. This means alert queries automatically inherit the dashboard and source filter context without additional wiring.


For a deeper walkthrough of rolling baselines, anomaly detection patterns, and supported macros, see the dedicated [SQL Charting and Alerting](https://clickhouse.com/blog/clickstack-sql-charting-and-alerting) post. Full macro and parameter documentation is also available in the [alerts documentation](https://clickhouse.com/docs/use-cases/observability/clickstack/alerts).


## A new default logs schema [\#](/blog/whats-new-in-clickstack-april-2026#a-new-default-logs-schema)


After benchmarking and profiling common observability workloads, we redesigned the default `otel_logs` schema used by ClickStack.


We originally started this work while profiling a handful of recurring query patterns that kept showing up in benchmarks and production traces. After a while, it became clear the issue was no longer isolated to settings tuning. The default schema itself needed another pass, particularly around indexing strategy and ordering layout.



> We'll be covering the benchmarking process, tooling, and methodology in more detail separately, including some of the internal benchmarking utilities we may eventually open source. We'll also be [discussing the work at Open House](https://clickhouse.com/openhouse/san-francisco) for users interested in the deeper storage and indexing details behind the changes.


The new schema:



```

```
1CREATE TABLE IF NOT EXISTS otel_logs
2(
3  `Timestamp` DateTime64(9) CODEC(Delta(8), ZSTD(1)),
4  `TraceId` String CODEC(ZSTD(1)),
5  `SpanId` String CODEC(ZSTD(1)),
6  `TraceFlags` UInt8,
7  `SeverityText` LowCardinality(String) CODEC(ZSTD(1)),
8  `SeverityNumber` UInt8,
9  `ServiceName` LowCardinality(String) CODEC(ZSTD(1)),
10  `Body` String CODEC(ZSTD(1)),
11  `ResourceSchemaUrl` LowCardinality(String) CODEC(ZSTD(1)),
12  `ResourceAttributes` Map(LowCardinality(String), String) CODEC(ZSTD(1)),
13  `ScopeSchemaUrl` LowCardinality(String) CODEC(ZSTD(1)),
14  `ScopeName` String CODEC(ZSTD(1)),
15  `ScopeVersion` LowCardinality(String) CODEC(ZSTD(1)),
16  `ScopeAttributes` Map(LowCardinality(String), String) CODEC(ZSTD(1)),
17  `LogAttributes` Map(LowCardinality(String), String) CODEC(ZSTD(1)),
18  `EventName` String CODEC(ZSTD(1)),
19  `__hdx_materialized_k8s.cluster.name` LowCardinality(String) MATERIALIZED
20      ResourceAttributes['k8s.cluster.name'] CODEC(ZSTD(1)),
21  -- ... seven more __hdx_materialized_* columns omitted for brevity
22  INDEX idx_trace_id          TraceId                       TYPE text(tokenizer = 'array'),
23  INDEX idx_res_attr_key      mapKeys(ResourceAttributes)   TYPE text(tokenizer = 'array'),
24  INDEX idx_res_attr_value    mapValues(ResourceAttributes) TYPE text(tokenizer = 'array'),
25  INDEX idx_scope_attr_key    mapKeys(ScopeAttributes)      TYPE text(tokenizer = 'array'),
26  INDEX idx_scope_attr_value  mapValues(ScopeAttributes)    TYPE text(tokenizer = 'array'),
27  INDEX idx_log_attr_key      mapKeys(LogAttributes)        TYPE text(tokenizer = 'array'),
28  INDEX idx_log_attr_value    mapValues(LogAttributes)      TYPE text(tokenizer = 'array'),
29  INDEX idx_lower_body        lower(Body)                   TYPE text(tokenizer = 'splitByNonAlpha')
30)
31ENGINE = MergeTree
32PARTITION BY toDate(Timestamp)
33ORDER BY (toStartOfFiveMinutes(Timestamp), ServiceName, Timestamp)
34TTL toDateTime(Timestamp) + INTERVAL 14 DAYS
35SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1,
36         enable_block_number_column = 1, enable_block_offset_column = 1;
```

```

The primary key is now `(toStartOfFiveMinutes(Timestamp), ServiceName, Timestamp)`. The previous schema carried both `Timestamp` and a secondary `TimestampTime DateTime DEFAULT toDateTime(Timestamp)` column, with the latter used in the ordering key to improve pruning at second\-level granularity.


With the new five\-minute bucket layout, that extra column is no longer necessary and has been removed entirely. The coarser leading bucket keeps [adjacent log rows physically grouped](https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes) for common time\-range queries while still allowing efficient pruning during scans.


The skip indices strategy has changed significantly as well. Previous schemas relied primarily on `bloom_filter` indexes over attribute maps alongside a `tokenbf_v1` index on the `Body` column. The new schema instead adopts [ClickHouse's Full\-text index](https://clickhouse.com/docs/engines/table-engines/mergetree-family/textindexes) across both keys and values for `ResourceAttributes`, `ScopeAttributes`, and `LogAttributes`, while a dedicated text index using the `splitByNonAlpha` tokenizer now covers `lower(Body)`.


In our benchmarks, the `text` index consistently outperformed the previous bloom\-filter approach for search\-oriented workloads while adding minimal ingest overhead. These new indexes also enable the attribute\-search optimizations covered in the following section.



> For users running ClickHouse versions prior to 26\.2, where full\-text search indexes became generally available, ClickStack automatically falls back to a compatibility schema variant using `bloom_filter` and `tokenbf_v1` indexes while preserving UI compatibility and the same query semantics.


Across all of our sample queries, the new schema improves performance by over 70%.


![](/uploads/clickstack_apr2026_image3_75d23f60fd.png)
Most of the query performance improvements occurred exactly where we expected them: text search, attribute filtering, and mixed search\-and\-filter workloads. Insert overhead remained broadly comparable to the previous schema, which was our primary concern going into the benchmarks.


Users looking to adopt the new schema should follow our [existing guide](https://clickhouse.com/docs/use-cases/observability/clickstack/performance_tuning#changing-the-primary-key) for modifying primary keys, as the same migration process applies here.


## Direct\-read optimization for OpenTelemetry attribute maps [\#](/blog/whats-new-in-clickstack-april-2026#direct-read-optimization-for-opentelemetry-attribute-maps)


A very common observability query pattern is filtering logs by attributes such as `http.status_code = 500` or `k8s.namespace.name = payments`.


In the default OpenTelemetry schema for ClickStack, these attributes live inside map columns such as `LogAttributes`, `ResourceAttributes`, and `ScopeAttributes`. Filters on these columns become queries like:



```

```
1LogAttributes['http.status_code'] = '500'
```

```

or



```

```
1ResourceAttributes['k8s.namespace.name'] = 'payments'
```

```

This flexible schema design is one of the reasons OpenTelemetry works well across heterogeneous workloads, but it also creates a challenge for query execution. ClickHouse needs an efficient way to determine which [granules](https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes#data-is-organized-into-granules-for-parallel-data-processing) may contain a given attribute key or value before reading and unpacking the underlying map data itself.


Earlier versions of the schema relied mostly on a bloom filter over map keys and values. This helped avoid unnecessary reads, but search\-heavy attribute queries still meant more I/O and slower queries.


The new schema enables a new attribute\-search path based on ClickHouse's text index. When enabled, values inside `ResourceAttributes`, `ScopeAttributes`, and `LogAttributes` are indexed using `text(tokenizer = 'array')`. This performs significantly better in our benchmarks for search\-heavy attribute filtering workloads.


One complication here is that the query shape does not directly match the indexed expression. The index is built over `mapValues(LogAttributes)`, while the filter itself is expressed as a keyed map lookup. That still gives ClickHouse useful pruning information, but not enough to fully resolve the predicate from the index alone.


To avoid that mismatch, we added an alternate indexed representation for attribute maps. Each map is flattened into an array of `key=value` strings with a corresponding `text(tokenizer = 'array')` index.



```

```
1LogAttributes['http.status_code'] = '500'
```

```

can be rewritten as:



```

```
1has(LogAttributeItems, 'http.status_code=500')
```

```

This shape aligns exactly with the array tokenizer, allowing ClickHouse to evaluate the predicate from the index without unpacking the original map column. In our internal benchmarks, attribute filters that hit this path ran between 1\.4 and 10 times faster than the equivalent map\-subscript query.


![](/uploads/clickstack_apr2026_image4_3a6ff9ed6c.png)
*The green bar represents the performance of queries related to autocomplete for the previous implementation. The yellow bar represents the equivalent performance for the direct\-read optimization.*


ClickStack now detects when a source has a compatible companion column for one of its OTel attribute maps and automatically rewrites matching attribute predicates. Users do not need to change their queries, and attributes still appear in the search bar as before.


For now, this optimization is opt\-in rather than part of the default schema. The companion column currently needs to be declared as `MATERIALIZED` for the direct\-read path to engage, which adds storage overhead. A ClickHouse fix allowing `ALIAS` columns to work the same way has already been merged and backported as far as 26\.2\. Once that ships, we expect to enable this feature by default without adding storage cost.


Users who want to enable the materialized path today can do so with a pair of `ALTER` statements per attribute map. The example below shows `ResourceAttributes`; the same pattern applies to `ScopeAttributes` and `LogAttributes`.



```

```
1ALTER TABLE otel_logs
2  ADD COLUMN ResourceAttributeItems Array(String)
3  MATERIALIZED arrayMap(
4    (arr) -> concat(arr.1, '=', arr.2),
5    CAST(ResourceAttributes, 'Array(Tuple(String, String))')
6  )
7  CODEC(ZSTD(1));
8
9ALTER TABLE otel_logs
10  ADD INDEX idx_res_attr_items ResourceAttributeItems
11  TYPE text(tokenizer = 'array');
```

```

Once the column and index exist, a Lucene query such as `ResourceAttributes.k8s.namespace.name:"payments"` is automatically translated by ClickStack into a `has(ResourceAttributeItems, 'k8s.namespace.name=payments')` predicate against the indexed companion column, rather than a map lookup against `ResourceAttributes` itself.


## Faster and richer autocomplete [\#](/blog/whats-new-in-clickstack-april-2026#faster-and-richer-autocomplete)


Previously, autocomplete queried the live `otel_logs` and `otel_traces` tables directly to discover attribute keys and values. That approach was simple, but it scaled poorly once datasets became large enough that suggestion lookups started competing with normal query workloads.

Loading video...The new implementation moves autocomplete to materialized view rollups created alongside the primary OTel tables. Rather than scanning live observability data for suggestions, ClickStack now maintains compact metadata tables specifically for autocomplete lookups.


Each source table gets two materialized views — `{table}_kv_rollup_15m` stores key/value frequencies in fifteen\-minute buckets, while `{table}_key_rollup_15m` stores aggregated key\-level counts derived from the same data. The UI uses these tables directly for autocomplete suggestions and ranking.


Sources now expose a `metadataMaterializedViews` configuration describing the rollup tables and bucket interval.


![](/uploads/clickstack_apr2026_image5_372b43bb36.png)
During source discovery, ClickStack automatically checks for compatible rollups and wires them into autocomplete if available. The default Docker, Helm, and embedded deployments already create these views automatically.


The rollup combines all three OTel attribute maps alongside a handful of commonly queried native columns:



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



> To try this yourself, head to our [demo environment](https://play-clickstack.clickhouse.com) and add a heatmap tile to a dashboard against the OpenTelemetry demo dataset.


## Alerting improvements [\#](/blog/whats-new-in-clickstack-april-2026#alerting-improvements)


Beyond SQL alerting, April also included several smaller alerting improvements requested by users. These changes are fairly incremental, but together they make the alerting workflow noticeably more flexible and less constrained by the editor itself.


### More threshold types [\#](/blog/whats-new-in-clickstack-april-2026#more-threshold-types)


The threshold selector now supports the [full set of comparison operators](https://clickhouse.com/docs/use-cases/observability/clickstack/alerts): `>`, `≥`, `<`, `≤`, `=`, `≠`, alongside `BETWEEN` and `NOT BETWEEN` for range\-based checks.


Equality and range operators also make a few common patterns easier to express directly, including heartbeat monitoring, fixed\-capacity checks, and alerts that operate within an expected upper and lower bound.


Notification rendering was updated alongside the operator changes. Alert messages now describe the evaluated condition directly, rather than resorting to generic comparison wording. For example, a notification now reads "3 errors found, which equals the threshold of 3 errors" rather than the older "3 found, expected not equal to 3".


![](/uploads/clickstack_apr2026_image7_35075d95dc.png)
### Alert history and acknowledge in the editor [\#](/blog/whats-new-in-clickstack-april-2026#alert-history-and-acknowledge-in-the-editor)


The alert editor now includes the same history and acknowledge/silence controls that previously only existed on the dedicated alerts page. Users can see when an alert last fired, inspect the value that triggered it, and silence or acknowledge the alert directly from the editor without switching views.


### Alert execution errors in the UI [\#](/blog/whats-new-in-clickstack-april-2026#alert-execution-errors-in-the-ui)


Previously, if an alert query failed to compile or a webhook returned a non\-2xx response, the alert would simply stop producing history entries. In many cases, there was no obvious indication in the UI that execution had failed at all.


The latest execution error is now persisted and surfaced in the alerts UI with an error indicator and expandable message details. This makes it possible to distinguish between an alert that simply has not fired recently and one that is actively failing to execute.


![](/uploads/clickstack_apr2026_image8_a509bebc50.png)
## Smaller things [\#](/blog/whats-new-in-clickstack-april-2026#smaller-things)


A few smaller changes also landed this month that are less visible individually, but remove a surprising amount of friction from day\-to\-day use.


### Pie chart legend [\#](/blog/whats-new-in-clickstack-april-2026#pie-chart-legend)


Pie charts now include a scrollable legend showing the slice color, label, and value for each segment. The legend is capped at 40% of the chart width to avoid overwhelming the chart, and it automatically scrolls once the number of slices exceeds the available space. Slice values also respect the chart's configured number formatting rules.


![](/uploads/clickstack_apr2026_image9_4583638af8.png)
### Per\-series number formats [\#](/blog/whats-new-in-clickstack-april-2026#per-series-number-formats)


Number formatting was previously configured at the chart level, meaning that every series in a line, bar, or table chart used the same units and suffixes. Series can now define their own `numberFormat` independently, while the chart\-level format remains as a fallback.

Loading video...The change also carries through to the external dashboards API, so dashboards created or updated programmatically support the same per\-series formatting behavior.


### Group\-by columns on the left of tables [\#](/blog/whats-new-in-clickstack-april-2026#group-by-columns-on-the-left-of-tables)


Table charts now support a display option that moves group\-by columns to the left of the table, rather than rendering all series columns first. This is mainly useful for wider tables where grouping keys would otherwise end up pushed far off\-screen behind a large number of metric columns.


The default layout remains unchanged, but users can now flip the ordering within each table to make the data easier to scan.

Loading video...Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
