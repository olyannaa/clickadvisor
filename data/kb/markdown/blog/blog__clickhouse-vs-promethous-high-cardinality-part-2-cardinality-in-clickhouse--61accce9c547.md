# ClickHouse vs Prometheus for High Cardinality, Part 2: Cardinality in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse vs Prometheus for High Cardinality, Part 2: Cardinality in ClickHouse

![](/_next/image?url=%2Fuploads%2Frory_94fa39dc2a.png&w=96&q=75)![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Rory Crispin](/authors/rory-crispin) and [Dale McDiarmid](/authors/dale-mcdiarmid)May 15, 2026 · 22 minutes readIn the [previous post](https://clickhouse.com/blog/clickhouse-vs-promethous-high-cardinality-p1-understanding-the-problem), we explored why high cardinality creates challenges for Prometheus and other series\-oriented time\-series databases. We looked at how the underlying storage model, where every unique combination of labels creates an independent time series, introduces memory overhead, write amplification, operational complexity, and query\-time tradeoffs as dimensionality and churn increase.


You’ll often hear us say that ClickHouse is not significantly affected by high cardinality when used for observability workloads. That’s true for the workloads we usually mean, but it needs qualification. ClickHouse still pays for cardinality, mostly at query time rather than during ingestion.


In this post, we'll explore why ClickHouse, and more broadly column\-oriented databases, handle high\-cardinality observability data so differently from systems such as Prometheus.


We'll also cover where this model is weaker than Prometheus. ClickHouse is not a drop\-in Prometheus replacement, and this approach requires a different way of thinking about telemetry, instrumentation, and aggregation.


## Why cardinality is different in ClickHouse [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#why-cardinality-is-different-in-clickhouse)


To understand why high cardinality behaves differently in ClickHouse, we first need to rethink how observability data is modeled. Rather than treating telemetry as millions of independently maintained time series, ClickHouse encourages a shift toward representing metrics as rows in a table containing attributes and measurements that can later be aggregated at query time.


This is often referred to as the "wide events" approach, [popularized by practitioners such as Charity Majors](https://charity.wtf/2022/08/15/live-your-best-life-with-structured-events/). If it helps, you can think of this simply as logs with metrics attached. Let’s first explore how this differs from a traditional Prometheus\-style metric model.


### Metrics as wide events [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#metrics-as-wide-events)


It’s important to emphasize that we are not attempting to directly model Prometheus metrics, metric types, or PromQL semantics inside ClickHouse, although work in this [area is underway](https://github.com/ClickHouse/ClickHouse/pull/102246) and the model certainly has benefits, which we’ll explore later. Instead, the wide events approach encourages a broader shift away from the traditional Prometheus metric model toward an event\-style model for observability data.


In this model, telemetry is represented as timestamped events containing dimensions, attributes, and numeric measurements, rather than as independently maintained time series. Instead of storing a metric as a separate series with its own identity and lifecycle, each event contains contextual attributes alongside one or more numeric measurements. Queries then dynamically aggregate these events into the desired views, rates, summaries, or time buckets at read time.


Importantly, this is often a more relaxed and natural way to produce telemetry. Rather than defining strict metric schemas in advance, applications simply emit structured events with numeric values. A common pattern in ClickHouse observability deployments is to store metrics directly alongside logs using wide event schemas [such as otel\_logs](https://clickhouse.com/docs/use-cases/observability/clickstack/ingesting-data/schemas).


For example, rather than defining multiple separate metrics for response times, request counts, status codes, and hosts, a service might simply emit events like:


```
1logger.Info("request completed",
2    zap.String("host", "host-42"),
3    zap.String("application", "checkout-service"),
4    zap.String("request_path", "/api/payments"),
5    zap.Uint16("status", responseStatus),
6    zap.Uint64("response_time", responseTime),
7    zap.Uint64("size", responseSize),
8)
```
With wide events, the request itself becomes the natural unit of telemetry. All contextual dimensions and measurements remain attached to the same event. In a Prometheus\-style model, the same information would typically be decomposed across multiple metric definitions, counters, gauges, histograms, and label combinations. Once collapsed into aggregates this way, the individual signals are lost and unrecoverable. Wide events invert this: aggregates are derived from the raw events rather than replacing them, so any spike on a graph can be traced back to the exact requests that produced it.

### Get started today

Interested in seeing how ClickHouse works on your observability data? Get started with Managed ClickStack in ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?intent=o11y&loc=blog-cta-636-get-started-today-sign-up&utm_blogctaid=636)### Columnar Storage [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#columnar-storage)


When embracing the wide events model, our initial intuition might be to take inspiration from traditional analytical workloads and model each label as a dedicated column. While this can work well for stable schemas, it is rarely practical in observability and is not a wide event schema. Labels are often dynamic, high cardinality, and unpredictable, making rigid upfront schema definitions difficult to maintain and poorly suited to real\-world telemetry data.


```
1CREATE TABLE metrics
2(
3    `time` DateTime CODEC(Delta(4), ZSTD(3)),
4    `host` LowCardinality(String),
5    `application` LowCardinality(String),
6    `request_path` String,
7    `remote_addr` IPv4,
8    `remote_user` LowCardinality(String),
9    `request_type` LowCardinality(String),
10    `request_protocol` LowCardinality(String),
11    `status` UInt16,
12    `domain_referer` LowCardinality(String),
13    `browser` LowCardinality(String),
14    `device` LowCardinality(String),
15    `response_time` UInt16,
16    `size` Decimal(7, 1)
17)
18ENGINE = MergeTree
19ORDER BY (host, toStartOfMinute(time), status, application, request_path, remote_addr)
```

> The schema above, while optimized with a column per label, isn't realistic in highly dynamic environments where new metrics are frequently added. **This is not a recommended wide event schema.**


To handle this dynamic structure, we recommend the [`Map`](https://clickhouse.com/docs/sql-reference/data-types/map) type for ClickHouse.



> For reasons discussed in depth [in our documentation](https://clickhouse.com/docs/use-cases/observability/clickstack/ingesting-data/schema/map-vs-json), we recommend using the Map type rather than the JSON type for observability workloads.


The Map type stores labels as key\-value pairs, where the key represents the label name and the value represents the label value. Its primary limitation is that all keys and values must share the same type, with the map defined as `Map<String, type>`. In practice, this usually means values are stored as strings. While this is flexible, it can require query\-time casting if values need to be interpreted as numeric or other strongly typed data.


Historically, Map also had an important disadvantage at read time. Reading a single label required reading the entire map structure and all labels associated with it, creating significant I/O overhead. However, recent support for [sharded maps](https://clickhouse.com/blog/clickhouse-release26-03#sharded-map) largely mitigates this issue by allowing more selective access to map contents.


For our earlier example, a table schema for wide events might look like:


```
1CREATE TABLE events
2(
3    `time` DateTime CODEC(Delta(4), ZSTD(3)),
4    `labels` Map(LowCardinality(String), String),
5    `response_time` UInt16 MATERIALIZED toUInt16(labels['response_time']),
6    `host` LowCardinality(String) MATERIALIZED labels['host'],
7    `status` LowCardinality(String) MATERIALIZED labels['status'],
8    `application` LowCardinality(String) MATERIALIZED labels['application'],
9    INDEX idx_labels_keys mapKeys(labels) TYPE text(tokenizer = array),
10    INDEX idx_labels_vals mapValues(labels) TYPE text(tokenizer = array)
11)
12ENGINE = MergeTree
13ORDER BY (host, toStartOfMinute(time), status, application)
14SETTINGS
15    map_serialization_version = 'with_buckets',
16    max_buckets_in_map = 32,
17    map_buckets_strategy = 'sqrt';
18
```
*Note that the settings here force sharding of the map. Further details [here](https://clickhouse.com/docs/sql-reference/data-types/map#bucketed-map-serialization).*



> In principle, this schema is very similar to the one used by [ClickStack for OpenTelemetry logs](https://clickhouse.com/docs/use-cases/observability/clickstack/ingesting-data/schemas#logs), albeit significantly simplified. In ClickStack, resource and scope attributes effectively serve as dynamic label maps.


The schema then exploits the same techniques discussed below, such as text indexes over map keys and values. So rather than thinking in terms of "series objects", ClickHouse simply stores rows of data containing a timestamp, a sharded map of labels, and regular numeric columns for metric values.


We have also [materialized keys from the labels map](https://clickhouse.com/docs/use-cases/observability/clickstack/performance_tuning#materialize-frequently-queried-attributes) that we expect to be filtered on or accessed frequently, so they can exist as dedicated columns on disk. This materialization occurs automatically at insert time and enables ClickHouse to filter, prune, and read these dimensions directly without accessing the labels map at query time, reducing I/O for common access patterns.


The same approach can also be applied to frequently queried numeric values. In the example above, `response_time` is materialized from the map into a dedicated typed column because it is expected to be aggregated regularly. This avoids repeated map access and query\-time casting when computing operations such as `avg(response_time)` or percentile calculations.


Importantly, materialized columns can also be added after data has already been ingested. Newly inserted rows will physically store the materialized column on disk, while older rows can still resolve the value indirectly from the underlying map when queried. For example, if we later decide that `labels['region']` has become a common filter, we could add:


```
1ALTER TABLE events
2ADD COLUMN region LowCardinality(String)
3MATERIALIZED labels['region'];
```
New data will immediately benefit from direct column access, pruning, and improved compression, while historical rows still remain queryable via `region` without requiring a full table rewrite.


Internally, a `Map` is represented as an array of key\-value pairs, with bucketed serialization that distributes keys across multiple independent buckets based on a hash of the label name. This means that queries that read a specific label only need to access the bucket containing that key, rather than the full map structure. Metric columns themselves are stored independently and compressed separately from the labels.


![map_type_clickstack.png](/uploads/map_type_clickstack_0ce07ceb2c.png)

> *① Each insert initially creates a Level 0 part using the default `Map` layout, where keys and values are stored as flat arrays without bucketing. ② Additional inserts create more Level 0 parts in the same format. Since these parts are small, scanning the full key and value arrays is typically inexpensive. ③ During background merges, ClickHouse rewrites the `Map` into bucketed storage by hashing keys into smaller independent buckets. When accessing a key such as `labels['status']`, ClickHouse computes the key hash and reads only the corresponding bucket rather than the full map, significantly reducing read\-time I/O. In practice, this can improve single\-key lookup performance by 2–49× depending on map size.*


Prometheus does the opposite. In Prometheus, each new label combination creates a new series object with its own metadata, chunks, and indexing overhead. In ClickHouse, adding a new combination of label values does not create a new structural object or in\-memory series representation. It simply adds another row containing a different set of label values.
When rows are inserted, they are written to disk as a part, sorted by the target table’s primary key \- in this case, the host, timestamp with a granularity of one minute, status, and application. Codecs can be applied to each column before ZSTD compression to minimize future I/O during reads.

Loading video...To manage the number of parts per table, a background merge job periodically combines smaller parts into larger ones, while preserving the specified sort order, until they reach a configurable compressed size (typically \~150 GB). Over time, this process creates a hierarchical structure of merged parts.


![part_merging.png](/uploads/part_merging_c7cdd2fb3d.png)
At insert time, ClickHouse writes rows, not series objects.


### Benefits of columnar storage [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#benefits-of-columnar-storage)


The column orientation and sorting of the table still provide several important benefits, even when the labels themselves are stored in a Map rather than as fully independent columns.


- **Fast filtering with data pruning** \- A sparse index is built over the table’s sorting key, which in this case consists of commonly filtered dimensions materialized from the label map, followed by the timestamp.


In the example above, labels such as host, status, and application are materialized into dedicated columns and included in the ordering key. Data is stored in parts, with each part divided into granules of roughly 8,000 rows. For each granule, ClickHouse records the first value of the sorting key columns rather than indexing every row, which is why the index is considered sparse.


Because the data is physically ordered by frequently queried dimensions and then by time, rows with similar values are naturally grouped together on disk. This allows ClickHouse to efficiently prune granules when queries filter on common labels such as host, application, status, or a time range. Instead of scanning the entire dataset, it can skip large sections of irrelevant data and read only the granules likely to contain matching rows, significantly reducing I/O and improving query performance.


Secondary indexes over `mapKeys(labels)` and `mapValues(labels)` further complement this. These inverted indexes allow ClickHouse to prune granules even when filtering on labels that are not materialized into dedicated columns, helping retain flexibility for highly dynamic dimensions.
Loading video...- **Compression** \- Even with labels stored inside a Map, ClickHouse still achieves excellent compression for observability workloads. Data is physically ordered by commonly filtered dimensions such as host, status, and application, followed by time. This naturally groups together rows with similar label sets, metric values, and repeated strings, creating strong locality that compression algorithms can exploit effectively.


Materializing frequently queried labels into dedicated columns further improves compression. Since rows with the same values are stored contiguously on disk, dictionary encoding and compression codecs become significantly more effective.


Metric columns that have been materialized, such as `response_time` in the above example, remain fully column\-oriented and are compressed independently using both type\-specific codecs and general\-purpose compression algorithms such as ZSTD. Numeric columns can additionally benefit from [codecs such as Delta](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema) or [Gorilla](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf).


The Map structure itself also compresses effectively. Label keys are highly repetitive across rows, while many label values exhibit strong temporal locality in real workloads \- Use of materialized map labels in the primary key helps with this locality. Combined with sharded map serialization, this allows ClickHouse to maintain strong compression characteristics even with highly dynamic label sets.
- **Reduced I/O** \- Reduced I/O \- Queries only need to read the granules, columns, and map buckets required to satisfy the query. Frequently filtered labels and metrics, such as `host`, `response_time`, and `status` are materialized into dedicated columns, allowing many common queries to avoid accessing the label map entirely. Because these materialized columns are part of the sorting key, ClickHouse can efficiently prune granules before reading metric data.


For labels stored only inside the sharded `Map`, ClickHouse reads only the bucket containing the requested keys rather than the full label structure. This significantly reduces I/O compared to earlier map implementations while preserving the flexibility of dynamic labels.


The schema also defines [inverted indexes](https://clickhouse.com/docs/engines/table-engines/mergetree-family/textindexes) over `mapKeys(labels)` and `mapValues(labels)`. These indexes allow ClickHouse to further prune granules when queries filter on non\-materialized labels, avoiding reads of granules that cannot contain the requested label names or values. This provides efficient filtering even for highly dynamic dimensions such as `container_id` or `pod_id` without requiring every label to become a dedicated column.


Because metric columns are stored independently and contiguously on disk, ClickHouse can also efficiently apply vectorized query execution, reading large batches of values continuously into memory for high analytical throughput.


![text_indices.png](/uploads/text_indices_e6cfb586de.png)
*At query time, the text index uses a layered lookup process to efficiently resolve matching rows without scanning the full dataset, using a sparse index, dictionary blocks and posting listings. For more details, see [our dedicated post](https://clickhouse.com/blog/clickhouse-full-text-search-object-storage).*


[Bloom filter indices](https://clickhouse.com/docs/optimize/skipping-indexes#bloom-filter-types) can also be used for this purpose and may be sufficient for many workloads. In practice, the best choice depends on the label distribution, query patterns, and the selectivity of the applied filters.


- **Analytical aggregations** \- In this model, metrics are represented as numeric columns, such as `response_time`. Aggregations become straightforward and efficient. If we want to compute something like `avg(response_time)`, ClickHouse only needs to read the `response_time` column for the rows that match the query filters. Thanks to the sparse index and secondary filters, the engine can identify the specific granule ranges that satisfy the filters and only read those ranges from disk. Those ranges can be processed in parallel across all CPU cores and servers in a cluster. This gives us effective predicate pushdown at the storage level.


As a result, aggregation performance is not directly tied to cardinality as in a series\-based model. It is more closely related to the number of rows that match the query filters. Only the relevant metric column needs to be read for the matching rows. Filters on high\-cardinality columns are often beneficial because they tend to reduce the number of rows scanned. In contrast, queries with no filters or filters on low\-cardinality columns will typically require more data to be read, which requires parallelized reads for performance.


### Example [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#example)


Consider the earlier `metrics` table. In our example, this stores 5 billion response times and sizes for our application. Some of the columns in this data naturally have high cardinality, and you would avoid using them as labels in any traditional time series database like Prometheus.


```
1SELECT count()
2FROM events
3
4┌────count()─┐
5│ 5339783200 │ -- 5.34 billion
6└────────────┘
7
81 row in set. Elapsed: 0.004 sec.
9
```
The following shows the cardinality of each column, as well as the total cardinality if we were to represent this using a time series model.


```
1SELECT
2    uniq(host),
3    uniq(application),
4    uniq(labels['request_path']),
5    uniq(labels['remote_addr']),
6    uniq(labels['remote_user']),
7    uniq(labels['request_type']),
8    uniq(labels['request_protocol']),
9    uniq(status),
10    uniq(labels['domain_referer']),
11    uniq(labels['browser']),
12    uniq(labels['device'])
13FROM events
14FORMAT Vertical
15
16Row 1:
17──────
18uniq(host):               100
19uniq(application):        1000
20uniq(arrayEl⋯est_path')): 881432
21uniq(arrayEl⋯ote_addr')): 258115
22uniq(arrayEl⋯ote_user')): 995890
23uniq(arrayEl⋯est_type')): 5
24uniq(arrayEl⋯protocol')): 7
25uniq(status):             15
26uniq(arrayEl⋯_referer')): 369
27uniq(arrayEl⋯'browser')): 9
28uniq(arrayEl⋯ 'device')): 11
29
30
31
32SELECT uniq(host, application, labels['request_path'], labels['remote_addr'], labels['remote_user'], labels['request_type'], labels['request_protocol'], status, labels['domain_referer'], labels['browser'], labels['device']) AS total_time_series
33FROM events
34
35┌─total_time_series─┐
36│        5239274309 │ -- 5.24 billion
37└───────────────────┘
38
```
Clearly, the number of time series here is significant, almost the same as the number of rows at 5\.2 billion.



> **Rows are not the same as time series**. You can add many more data points for an existing series, increasing the row count without increasing the number of distinct series. In most datasets, the total number of rows will far exceed the number of time series. In this example, each row even stores two metrics, response time and size, so the relationship between rows, samples, and series is rarely one\-to\-one.


Now consider the following query, which runs in milliseconds executed on a 32\-core machine. It computes an average on the above table for the response time, grouping to 1\-minute intervals, bucketing by the status, and limiting to a specific day:


```
1SELECT
2    toStartOfMinute(time) AS minute,
3    labels['status'] as status,
4    avg(response_time)
5FROM metrics
6WHERE (time >= '2025-02-23 08:00:00') AND (time <= '2025-02-23 12:00:00')
7GROUP BY
8    minute,
9    status
10ORDER BY minute ASC
11
12┌──────────────minute─┬─status─┬─avg(response_time)─┐
13│ 2025-02-23 08:00:00 │ 403    │  5065.290909090909 │
14│ 2025-02-23 08:00:00 │ 500    │  5327.543933054393 │
15│ 2025-02-23 08:00:00 │ 302    │  5119.796687088722 │
16..
17
183084 rows in set. Elapsed: 0.122 sec. Processed 49.21 million rows, 340.04 MB (404.24 million rows/s., 2.79 GB/s.)
19Peak memory usage: 726.64 MiB.
20
```
This is an example of a query that would be challenging to execute in Prometheus. You would need to access many independent series in order to compute this.



> Note that this query computes a simple average over event\-style data, grouped into fixed one\-minute buckets. It is not semantically identical to the earlier `avg_over_time(...[5m])` example. The results may look similar on a chart, but the underlying computation model is different \- see ["When Prometheus still makes sense"](#when-prometheus-still-makes-sense).


Narrowing to fewer "series" reduces the amount of data that needs to be read. For example:


```
1SELECT
2    toStartOfMinute(time) AS minute,
3    avg(response_time)
4FROM events
5WHERE application = '603' AND host = '3' AND status = '200' GROUP BY minute
6ORDER BY minute ASC
7
8┌──────────────minute─┬─avg(response_time)─┐
9│ 2025-01-24 00:00:00 │ 3680.4615384615386 │
10│ 2025-01-24 00:01:00 │  5515.153846153846 │
11..
12
135 rows in set. Elapsed: 0.078 sec. Processed 53.40 million rows, 479.93 MB (681.97 million rows/s., 6.13 GB/s.)
14Peak memory usage: 613.54 MiB.
15
```
In the latter case, we read significantly less data thanks to the inverted index, as reflected in the query execution time. To narrow to a specific series, you would just add filters for all columns.


Metrics can also remain inside the `labels` map and be accessed dynamically at query time when they are not frequently queried enough to justify materialization. While we generally recommend materializing commonly aggregated metrics such as `response_time`, observability workloads often contain many lower\-frequency measurements that are queried only occasionally. In these cases, accessing the metric directly from the map can be perfectly reasonable.


For example, suppose events also contain a `size` attribute representing the response payload size. We may only occasionally want to compute total traffic volume over time. Rather than materializing another dedicated column, we can access and cast the value directly from the map:


```
1SELECT
2    toStartOfMinute(time) AS minute,
3    sum(toDecimal32(labels['size'], 1)) AS total_traffic
4FROM events
5WHERE application = '603'
6GROUP BY minute
7ORDER BY minute ASC
8
9┌──────────────minute─┬─total_traffic─┐
10│ 2025-01-24 00:00:00 │         89167 │
11│ 2025-01-24 00:01:00 │        352724 │
12│ 2025-01-24 00:02:00 │        284684 │
13…
14
154 rows in set. Elapsed: 1.138 sec. Processed 53.31 million rows, 13.60 GB (46.84 million rows/s., 11.95 GB/s.)
16
```
This flexibility is one of the advantages of the wide events model. Frequently queried dimensions and metrics can be materialized into optimized columns, while less common attributes remain dynamically accessible without requiring rigid upfront schema definitions.


## When high cardinality still has a cost in ClickHouse [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#when-high-cardinality-still-has-a-cost-in-clickhouse)


**ClickHouse does not make cardinality free.**


**Some costs move to read time, especially for large GROUP BY operations.**


Suppose we wish to group by the `request_path`. We're now **grouping by a high cardinality column at read time and accessing the map**.


```
1SELECT
2    toStartOfMinute(time) AS minute,
3    labels['request_path'] as request_path,
4    avg(response_time)
5FROM events
6WHERE toDate(time) = '2025-01-24'
7GROUP BY
8    minute,
9    request_path
10ORDER BY minute ASC
11
12-- we'll omit the results :) 
13
140 rows in set. Elapsed: 9.433 sec. Processed 153.23 million rows, 63.85 GB (16.24 million rows/s., 6.77 GB/s.)
15Peak memory usage: 22.82 GiB.
16
```
The cost is visible in both memory usage and elapsed time.


Performant grouping by very high\-cardinality columns does incur memory overhead, since aggregation states must be built in memory. However, ClickHouse supports [spilling to disk when thresholds are exceeded](https://clickhouse.com/docs/sql-reference/statements/select/group-by#group-by-in-external-memory), making these workloads manageable rather than catastrophic. They can even be remarkably performant at high cardinality with controls to limit the memory consumption in exchange for performance:


```
1SELECT
2    toStartOfMinute(time) AS minute,
3    labels['request_path'] as request_path,
4    avg(response_time)
5FROM events
6WHERE toDate(time) = '2025-01-24'
7GROUP BY
8    minute,
9    request_path
10ORDER BY minute ASC
11-- Start external aggregation around 10 GB
12SETTINGS max_bytes_before_external_group_by = 10000000000
13
140 rows in set. Elapsed: 13.930 sec. Processed 153.23 million rows, 63.85 GB (11.00 million rows/s., 4.58 GB/s.)
15Peak memory usage: 9.57 GiB.
16
```
More practically, however, how would you even visualize almost a million distinct lines in an observability dashboard?


If your workload genuinely requires rendering millions of individual series, ClickHouse may not be the ideal tool. But if you need to compute aggregates across those millions of series, such as totals or averages, ClickHouse is extremely well\-suited.


## When ClickHouse makes sense [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#when-clickhouse-makes-sense)


ClickHouse is particularly well\-suited to **event\-style observability data** such as logs and traces enriched with metrics, where high cardinality is natural rather than accidental. It also excels at long\-term trend analysis, SLIs, KPIs, and broader business metrics that require analysis over extended time horizons. Whenever metrics are derived from events and require flexible time\- and dimension\-based aggregation, the columnar model plays to ClickHouse’s strengths.


Importantly, ClickHouse is not structurally impacted by short\-lived, ephemeral dimensions such as `container_id`, `pod_id`, or other dynamically generated identifiers common in modern environments. These are simply column values.


The practical consequence of this is significant. You can store your **full\-fidelity metric data in ClickHouse without needing to aggressively sample, pre\-aggregate, or strip labels** purely to control cardinality. Instead of designing your schema to avoid explosions, you can model your data naturally and let query patterns determine what is read.


## When Prometheus still makes sense [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#when-prometheus-still-makes-sense)


Prometheus absolutely still makes sense in many scenarios, not least because of its broad ecosystem support, mature operational tooling, and deeply integrated alerting capabilities.


It was built around a metrics\-first model where samples are scraped into distinct time series, and it supports multiple metric types: counters, gauges, histograms, and summaries. Each type encodes assumptions about how the data should be interpreted. Counters handle rates and resets. Histograms and summaries support latency and distribution analysis. These semantics are deeply embedded in PromQL and the surrounding ecosystem.


In an event\-style model in ClickHouse, metrics are typically stored as numeric columns on events and aggregated at query time. In practice, these values often behave more like gauges than strict Prometheus\-style counters. Like Prometheus, ClickHouse fundamentally stores numbers (histograms aside), with semantics emerging from query logic rather than the storage layer itself.


Conversely, Prometheus assumes regularly sampled series and provides first\-class semantics for counters, rates, histograms, and range vectors. ClickHouse instead operates over timestamped events, making it better aligned with flexible event\-style aggregation over high\-cardinality observability data rather than strict time\-series semantics.


For highly targeted single\-series lookups and plotting, Prometheus often performs extremely well. Its inverted index resolves label intersections quickly, and reading a single compressed series is efficient. ClickHouse can achieve similar performance when the ordering key aligns with the filter, but it may scan more data in some cases. The difference is rarely dramatic, but this is a scenario where Prometheus is very strong.


Prometheus also works extremely well when cardinality is controlled and predictable. For moderate numbers of long\-lived series, real\-time alerting, and traditional monitoring workflows, it is highly effective. It integrates seamlessly with stacks such as LGTM, where Prometheus and its distributed counterparts, such as Mimir, are first\-class citizens. While distributed systems address scalability concerns, they retain the underlying series\-based model, meaning cardinality still requires deliberate management.


### ClickHouse for Prometheus metrics [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#clickhouse-for-prometheus-metrics)


ClickHouse’s open\-source observability stack, ClickStack, supports Prometheus\-style metrics (Open Telemetry metrics), but it should not be viewed as a drop\-in replacement for Prometheus or for long\-established Prometheus\-compatible systems. The underlying storage and query model are fundamentally different, with ClickStack favoring an event\-oriented approach over a strict time\-series model.


As a result, querying for Prometheus\-style metrics in ClickStack is exposed through higher\-level query builders and abstractions with more limited capabilities than native PromQL today. This is largely due to the complexity of fully reproducing Prometheus semantics, particularly around counters, histograms, range vectors, and the broader PromQL execution model.


If you require mature, battle\-tested PromQL support deeply integrated into dashboards, alerts, and operational workflows, Prometheus remains the obvious choice. That said, PromQL support in ClickHouse continues to evolve, with [recent encouraging developments](https://github.com/ClickHouse/ClickHouse/issues/57545#issuecomment-4246791048). Manually translating complex PromQL queries into SQL can also be non\-trivial, particularly for histograms and range\-vector functions \- but possible with the help of LLMs.


Prometheus remains the better fit for moderate\-cardinality metrics, PromQL\-centric alerting, and targeted series lookups.


## Conclusion [\#](/blog/clickhouse-vs-promethous-high-cardinality-part-2-cardinality-in-clickhouse#conclusion)


High cardinality is not "free" in ClickHouse, but the costs appear in very different places compared to traditional time\-series systems. By shifting from a series\-oriented model to wide events stored in column\-oriented tables, ClickHouse avoids the per\-series write amplification, memory overhead, and operational fragility that make cardinality so challenging in systems such as Prometheus. Instead, the tradeoffs move primarily to query\-time aggregation and data modeling decisions, areas where ClickHouse’s columnar execution model, compression, pruning, and parallelization are particularly strong.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
