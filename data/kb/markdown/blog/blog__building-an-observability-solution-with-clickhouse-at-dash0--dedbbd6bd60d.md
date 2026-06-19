# Building an Observability Solution with ClickHouse at Dash0


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Building an Observability Solution with ClickHouse at Dash0

![](/_next/image?url=%2Fuploads%2Fmiel_donkers_fe4606b713.png&w=96&q=75)Miel DonkersApr 7, 2025 · 22 minutes readThe founding team behind Dash0 has deep roots in Instana, a company known for its innovations in observability tooling. And where Instana, in its early days, heavily relied on Cassandra and ElasticSearch as storage solutions, as the platform evolved, the team transitioned to leveraging ClickHouse as one of its core database technologies. This shift addressed our need for greater efficiency and scalability as both customer demands and feature requirements grew.


![dash0_dashboard.png](/uploads/dash0_dashboard_7bd7a80c83.png)
When we founded Dash0, evaluating ClickHouse as our primary storage solution was a natural first step, especially since two of our founders had worked at ClickHouse helping to build their cloud offering. Fast\-forward to today, where ClickHouse serves as our main storage for all OpenTelemetry data, with PostgreSQL being the only other database used, handling just customer\-specific settings and related data.


In this blog post, I'll share our ClickHouse journey—from initial evaluation through technical implementation details—highlighting the key features that make Dash0 possible.


## Decision phase [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#decision-phase)


The goal of Dash0 is to be [OpenTelemetry native](https://www.dash0.com/blog/opentelemetry-native-the-future-of-observability#what-does-an-open-telemetry-native-observability-tool-look-like), leveraging the full broadness of information that the OpenTelemetry signals provide:


- **Cross\-Signal Correlation**: Engineers can start with metrics, drill down to relevant traces, and examine associated logs in a single workflow
- **Service Health Monitoring**: The platform preserves OpenTelemetry's semantic conventions to automatically generate meaningful dashboards or create actionable alerts
- **Simplified Troubleshooting**: By maintaining connections between signals, Dash0 significantly reduces mean time to resolution during incidents


These features naturally have certain implications that trickle down to the storage layer:


- Handle and store all the various signals: Metrics, Logs and Spans
- Be able to reference one signal via another, either via Resource attributes or other fields such as via the TraceId and SpanId for a log ([https://opentelemetry.io/docs/specs/otel/logs/\#log\-correlation](https://opentelemetry.io/docs/specs/otel/logs/#log-correlation))
- High cardinality data due to attributes, which are present both on the Resource level and on a signal level


Consolidating all data in a single system makes the most sense for these requirements. This approach enables `JOIN` s directly on the tables to combine various signals and leverages ClickHouse's proven scalability for monitoring workloads.


ClickHouse's columnar architecture excels at handling high\-cardinality data from OpenTelemetry attributes (key\-value pairs that provide additional context and metadata about telemetry data). While attributes can be stored as `Map(String, String)` types, [materialized columns](https://clickhouse.com/docs/en/sql-reference/statements/alter/column#materialize-column) extract [frequently\-queried attributes](https://opentelemetry.io/docs/specs/semconv/) like `service.name` into dedicated columns for faster lookups. Additionally, with the recent addition of [native JSON support](https://clickhouse.com/docs/sql-reference/data-types/newjson), ClickHouse now addresses the storage of complex dynamic structures even more efficiently. This promises the flexibility of Map with the performance of materialized columns, further simplifying configuration.


ClickHouse also provides robust [client libraries for both Java and Golang](https://clickhouse.com/docs/en/integrations/language-clients)—languages essential to our tech stack. While the Dash0 engineering team is well\-versed in Java, Golang is also a natural choice due to the various OpenTelemetry and related libraries and integrations written in this language. For example, the [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/), which we envisioned to use for the processing incoming data, is written in Golang and already includes a [ClickHouse exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/clickhouseexporter/) in its control repository.


## Operating ClickHouse [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#operating-clickhouse)


Beyond the table schemas needed to support Dash0's features (which will be covered further down), we've carefully optimized ClickHouse's operational aspects based on our experience. These optimizations balance maintainability, performance, and cost efficiency. Naturally, we continuously [monitor ClickHouse via Dash0](https://www.dash0.com/hub/integrations/int_clickhouse_cloud/overview) itself as well to ensure it also keeps running smoothly.


### Storage [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#storage)


For any observability platform, data volume grows rapidly with larger customer accounts, making storage costs a critical consideration. This naturally creates tension with query performance requirements. And while perhaps logs and spans may lose relevance after a few weeks, at Dash0 we wanted to preserve metrics for over a year to enable seasonal trend analysis.


With the experience gathered during our tenure at ClickHouse, we implemented a hybrid storage approach combining AWS S3 storage with temporary local storage. A setup that is well [supported by ClickHouse](https://clickhouse.com/docs/en/operations/storing-data). Customer usage patterns show that data from the past 1\-2 days receives the most frequent queries, which aligns with use\-cases like viewing dashboards or incident investigation based on [tracing signals](https://www.dash0.com/distributed-tracing).


Thanks to the high compression rates that ClickHouse manages, the urgency to move data from hot to cold storage is deferred, making 1\-2 days of hot storage easily possible.


Our multi\-tiered disk configuration consists of:


- 1\-2 days local storage
- Data moved to AWS S3
- Local storage for query cache


This query cache allows data retrieved from S3 to remain available locally for some time, accelerating subsequent queries on the same data while reducing S3 GET request costs.


The disk configuration looks something like:



```
<clickhouse>
   <storage_configuration>
       <disks>
           <default>
               <keep_free_space_bytes>536870912</keep_free_space_bytes>
           </default>
           <disk_s3>
               <data_cache_enabled>true</data_cache_enabled>
               <endpoint>...s3 endpoint...</endpoint>
               <type>s3</type>
           </disk_s3>
           <disk_s3_cache>
               <disk>disk_s3</disk>
               <path>/mnt/cache-disk/</path>
               <type>cache</type>
           </disk_s3_cache>
       </disks>
       <policies>
           <s3tiered>
               <move_factor>0.100000</move_factor>
               <volumes>
                   <n_1_hot>
                       <disk>default</disk>
                   </n_1_hot>
                   <n_2_cold>
                       <disk>disk_s3_cache</disk>
                   </n_2_cold>
               </volumes>
           </s3tiered>
       </policies>
   </storage_configuration>
</clickhouse>

```

![Blog_BuildingAnObservabilitySolutionDiagram_202504_V1.0_1 of 4.png](/uploads/Blog_Building_An_Observability_Solution_Diagram_202504_V1_0_1_of_4_894f9553b6.png)
### Ordering in table schemas [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#ordering-in-table-schemas)


Without going fully into the table schemas, the `ORDER BY` , `PARTITION BY` and `TTL` definitions are related to the storage.


The `TTL` clause ensures that ClickHouse moves the data correctly to the S3 disk:



```

```
TTL toDateTime(Timestamp) + INTERVAL 25 HOUR TO VOLUME 'n_2_cold',
   toDateTime(Timestamp) + INTERVAL 13 MONTH DELETE
```

```

The `ORDER BY` clause is important for two reasons:


- Querying the data
- Compression of the data


When designing our ClickHouse schemas, we made strategic trade\-offs with primary key selection. Unlike the [ClickHouse Exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/bb534937e13c605cb3bf3e90c5358d859c5c7b5a/exporter/clickhouseexporter/exporter_logs.go#L160) that uses `service.name` in the primary key for all signals, we generate a hash of all attributes called `ResourceHash` that serves a similar purpose. Our primary key consists of `ResourceHash` followed by the `Timestamp` field.


Placing the `ResourceHash` / `service.name` before the `Timestamp` in the `ORDER BY` clause offers two key advantages:


- **Optimized Filtering**: With OpenTelemetry data, filtering by resource attributes \- and thus `ResourceHash` \- is common when correlating signals.This ordering allows ClickHouse to select fewer marks, reducing the number of records that need to be processed.
- **Better Compression**: Signals from the same service or process typically share similar characteristics \- especially resource attributes, but also e.g. log bodies, and span names. Ordering by `ResourceHash` groups similar data together, significantly improving ClickHouse's compression efficiency compared to `Timestamp` \-first ordering.


There's also a case to be made for reversing the order, first `Timestamp` and then `ResourceHash`. Since all Dash0 queries require a time frame, using first the `Timestamp` would efficiently narrow down the number of records that need to be selected, while a `ResourceHash` / `service.name` might not always be used for filtering. However, we mitigated this concern by using the day (from the `Timestamp`) as `PARTITION BY` key, which ensures ClickHouse only selects those parts within the specified time range for reading.


Although ClickHouse supports multiple primary keys for the same table through [projections](https://clickhouse.com/docs/sql-reference/statements/alter/projection), we opted against this approach due to increased storage costs.


### Replication and sharding [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#replication-and-sharding)


With our ClickHouse cluster setup, we decided, at least for now, to use multiple replicas and only a single shard. While at some point in the future we might still move to a multi\-shard setup, for now this setup is simpler and sufficient for our needs.


With multiple shards, [table migrations need to be executed for every shard individually](https://clickhouse.com/docs/architecture/cluster-deployment). Also, other changes to the cluster are more complex.


## Dash0 functionality on top of ClickHouse [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#dash0-functionality-on-top-of-clickhouse)


In this section we’ll go into the table schemas more, and some of the other ClickHouse features we use to support the Dash0 features.


### Metrics metadata [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#metrics-metadata)


The standard ClickHouse Exporter for the OpenTelemetry Collector stores all metrics information [per record and in separate tables based on metric type](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/d1d4d693eee7f81752c8270f8777fa585a480579/exporter/clickhouseexporter/internal/gauge_metrics.go#L20). This approach is inefficient because:


1. Metadata like `MetricName`, `MetricDescription`, and `MetricUnit` remain consistent across data points. Repeating this data for every data point results in significant data duplication. Even for the attributes per data point, these often share identical or similar attributes (e.g., `http.response.status_code` values of `200` and `500`) and thus could be deduplicated.
2. Map\-type columns for the attributes are slow to process and suboptimal as primary key components
3. Querying for a metric without knowing its type (sum, gauge, histogram, etc) requires searching across five different tables


To address these issues, we adopted a strategy already used by the Prometheus Remote Write library for ClickHouse and also implemented in ClickHouse's own [Time\-Series engine](https://clickhouse.com/docs/en/engines/table-engines/special/time_series#target-tables): storing metadata in a separate table with an ID that references the actual values.


While we still maintain separate tables for different metric types (as they require different column structures), this approach dramatically improves compression. A simplified version of our gauge table looks like this:



```

```
CREATE TABLE IF NOT EXISTS otel.otel_metrics_gauge
(
 `MetricHash` UInt64 Codec(LZ4),
 `StartTimeUnix` DateTime64(9) CODEC(Delta, LZ4),
 `TimeUnix` DateTime64(9) CODEC(Delta, LZ4),
 `Value` Float64 CODEC(LZ4),
)
ENGINE MergeTree
PARTITION BY toDate(TimeUnix)
ORDER BY (MetricHash, TimeUnix)
```

```

The `MetricHash` acts as the join column with the metadata table, further described below.


Since metrics normally are collected at a fixed rate \- for example, every 15 seconds \- the `Delta` compression on the `TimeUnix` column works really well. And also values themselves usually don't change that much ensuring change values are small, resulting in good compression.


The metrics metadata table looks like this:



```

```
CREATE TABLE IF NOT EXISTS otel.otel_metrics_metadata
(
 `TimeUnix` Date CODEC(Delta, LZ4),
 `MetricName` LowCardinality(String) CODEC(LZ4),
 `MetricHash` UInt64 CODEC(LZ4),
 `FirstSeen` SimpleAggregateFunction(min, DateTime64(9)) CODEC(T64, LZ4),
 `LastSeen` SimpleAggregateFunction(max, DateTime64(9)) CODEC(T64, LZ4),
 `ResourceAttributes` SimpleAggregateFunction(anyLast, Map(String, String)) CODEC(LZ4),
 `ResourceSchemaUrl` SimpleAggregateFunction(anyLast, String) CODEC(LZ4),
 `ScopeName` SimpleAggregateFunction(anyLast, String) CODEC(LZ4),
 `ScopeVersion` SimpleAggregateFunction(anyLast, String) CODEC(LZ4),
 `ScopeAttributes` SimpleAggregateFunction(anyLast, Map(String, String)) CODEC(LZ4),
 `ScopeDroppedAttrCount` SimpleAggregateFunction(anyLast, UInt32) CODEC(LZ4),
 `ScopeSchemaUrl` SimpleAggregateFunction(anyLast, String) CODEC(LZ4),
 `MetricDescription` SimpleAggregateFunction(anyLast, String) CODEC(LZ4),
 `MetricUnit` SimpleAggregateFunction(anyLast, String) CODEC(LZ4),
 `MetricAttributes` SimpleAggregateFunction(anyLast, Map(String, String)) CODEC(LZ4),
 `MetricType` SimpleAggregateFunction(anyLast, Enum8('MetricTypeEmpty' = 0, 'MetricTypeGauge' = 1, 'MetricTypeSum' = 2, 'MetricTypeHistogram' = 3, 'MetricTypeExponentialHistogram' = 4, 'MetricTypeSummary' = 5)) CODEC(LZ4),
 `SumAggTemp` SimpleAggregateFunction(anyLast, Enum8('AggregationTemporalityUnspecified' = 0, 'AggregationTemporalityDelta' = 1, 'AggregationTemporalityCumulative' = 2)) CODEC(LZ4),
 `SumIsMonotonic` SimpleAggregateFunction(anyLast, Boolean) CODEC(LZ4),
)
ENGINE = AggregatingMergeTree() PARTITION BY toYYYYMM(TimeUnix)
ORDER BY (TimeUnix, MetricName, MetricHash)
```

```

There's a few things in there that will likely need some explanation :)


One of our most significant design choices is using `AggregatingMergeTree` for our metrics metadata table—the same approach ClickHouse employs for its [Tags table, part of the TimeSeries table engine](https://clickhouse.com/docs/en/engines/table-engines/special/time_series#inner-table-engines). This engine ensures continuous deduplication of data despite constant writes to the table. Since `Resource-`, `Scope-`, and `Metric` attributes rarely change between data points, deduplicating this information significantly reduces the data volume ClickHouse must process when searching by these attributes.


The `MetricHash` field, which encapsulates the most critical attributes and fields, allows us to safely apply the [`anyLast` aggregation](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/anylast) function because we know certain properties (like `ResourceAttributes`) cannot change for the same `MetricHash` value.


Our `FirstSeen` and `LastSeen` columns use `min` and `max` aggregation functions to track when a particular time series was active. This information helps us filter out metrics that weren't present during specific query timeframes, again improving query efficiency.


The same reasoning applies to the choice of using the `TimeUnix` field as part of the `ORDER BY` clause—a design choice that may seem counterintuitive at first. Since we partition metadata by month to keep this information in hot storage longer, without any time\-based field in the primary key, queries might scan metrics for an entire month. By adding `TimeUnix` (`Date` type with day granularity) to the primary key, we reduce the number of matching rows. Because all our queries include time ranges, we can easily include an explicit filter on this `TimeUnix` column alongside the `FirstSeen` and `LastSeen` columns.


Using `AggregatingMergeTree` comes with an important caveat for querying: data merges aren't guaranteed to occur before query execution. This detail is easily overlooked but can lead to incorrect results when queries are not adjusted appropriately. For instance, when no data is received for some time for a specific time series, the `FirstSeen` / `LastSeen` ranges of unmerged records might appear as follows:


![Blog_BuildingAnObservabilitySolutionDiagram_202504_V1.0_2 of 4.png](/uploads/Blog_Building_An_Observability_Solution_Diagram_202504_V1_0_2_of_4_f750fab2b6.png)
Clearly, when not merging records, then *Time Series A* would never get selected even though it was present before and after the queried range. Therefore, when running queries on an `AggregatedMergeTree`, this always needs to be done either using a `GROUP BY` with similar merge functions as on the table definition or using [the FINAL keyword](https://clickhouse.com/docs/en/sql-reference/statements/select/from#final-modifier) with the table (where a simple `GROUP BY` is normally preferred).


### Sampling [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#sampling)


At Dash0, we prioritize data correctness and use sampling selectively. We primarily employ sampling to provide customers with quick initial results for longer\-running queries, while executing the complete query in the background, as used within our [triage feature](https://www.dash0.com/blog/triage-the-quickest-way-to-finding-the-needle-in-the-haystack) which we recently released.


To use the [`SAMPLING` clause](https://clickhouse.com/docs/sql-reference/statements/select/sample) in ClickHouse queries the table schema must be specifically designed to support this. And since the sampling column must be part of the sorting key, this often requires creating new tables rather than modifying existing ones. This presents the main challenge when using sampling: finding the optimal `ORDER BY` clause that works well with both regular or sampled queries.


When implementing sampling, we recommend:


1. Thoroughly benchmarking various options to ensure existing performance doesn't degrade
2. Using `EXPLAIN indexes=1 <query>` to analyze how selection of parts and granules is affected by different table sorting keys and secondary indexes


Another thing that is good to be aware of, is that the potentially sampling rates depend on the type chosen. This can be any type from `UInt8` to `UInt64`. That also means decreasing the number of 'groups' in favour of better ordering, e.g. as `xxh3(SpanId) % 10` to create just 10 groups, does not work. Even if using `UInt8`, ClickHouse assumes 256 ‘groups’ and selecting a 0\.1 sample rate would result in a query `WHERE <sample_column> < 26`, which as you see would still select 100% of the records.


Thus, the type chosen for the column also determines the maximum sample ratio that can be chosen. With `UInt8`, the lowest sample rate is \~ 0\.003\. If you try to go lower, ClickHouse determines it cannot do sampling and instead will scan all records.


#### Our approach [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#our-approach)


Given the sorting key we had and the above information about sampling (some of which we found out during the benchmarking), we had a few different sorting keys in mind that we wanted to evaluate. Our original sorting key for the spans table was `ORDER BY (ResourceHash, Timestamp)`


The `ORDER BY` clauses we thought could work:


- (traces2\) `toStartOfHour(Timestamp), ResourceHash, xxh3(SpanId)`
- (traces3\) `ResourceHash, SpanName, xxh3(SpanId)`
- (traces4\) `ResourceHash, toStartOfHour(Timestamp), xxh3(SpanId)`
- (traces5\) `xxh3(SpanId) % 256, ResourceHash, Timestamp`


For each of these sorting keys, we created a separate table and loaded 3 days of data. We determined we wanted to verify a few things:


- Compression ratio, to ensure storage costs would not dramatically increase for the new schemas
- Query times for existing, so non\-sampled queries
- Query times when using sampling
- Validate primary and secondary (data\-skipping) index usage to cross\-check numbers from previous queries make sense


To easily run the benchmarking (for which `[clickhouse-benchmark](https://clickhouse.com/docs/operations/utilities/clickhouse-benchmark)` works great), we collected some common queries and put them into separate SQL files, such like this one (getting a list of spans ordered by timestamp):



```

```
WITH subtractHours(toDateTime('${QUERY_TS}'), ${QUERY_DURATION} + 1) AS startTime, subtractHours(toDateTime('${QUERY_TS}'), 1) AS endTime
SELECT
    ResourceHash,
    Timestamp,
    SpanAttributes,
    SpanName
FROM ${QUERY_TABLE} ${QUERY_SAMPLE}
WHERE (Timestamp >= startTime) AND (Timestamp <= endTime) AND (ParentSpanId = '')
ORDER BY
    Timestamp ASC
LIMIT 50
FORMAT Null
SETTINGS use_query_cache=false;
```

```

By using variables, which we replace via a script (see below), we can easily run the script for different durations and tables, etc.


Additionally, if using `FORMAT Null` there is no actual data returned by the query. That makes sure when benchmarking we don't include the overhead of sending back data to the client and keep the query duration 'pure' \- essential when comparing sampled to non\-sampled queries.


The script we used to trigger these queries:



```
#!/usr/bin/env bash

TIMESTAMP=$(date +%Y-%m-%d-%H-%M)
RESULTS_FOLDER="results"
mkdir -p ${RESULTS_FOLDER}

# Some fields replaced in the scripts
QUERY_TS=$(date --utc +'%F %H:%M:%S')

for DURATION in "1" "12" "24" "72"; do

  for FILE in *.sql; do

	for TABLE in traces traces2 "traces2 SAMPLE 0.01"; do

	  OUTPUT_FILENAME="${FILE#queries/}"
	  OUTPUT_FILENAME="${OUTPUT_FILENAME%.sql}"
	  OUTPUT_FILENAME="${RESULTS_FOLDER}/${TIMESTAMP}-${OUTPUT_FILENAME}-${DURATION}h-${TABLE}.txt"

	  echo "##################################################"
	  echo "Running benchmark for ${FILE} and table ${TABLE}"

	  # Need to export the template variables otherwise not available in the subshell
	  export QUERY_TABLE=${TABLE%%SAMPLE*}
	  export QUERY_SAMPLE=${TABLE#$QUERY_TABLE}
	  export QUERY_DURATION=${DURATION}
	  export QUERY_TS
	  QUERY=$(envsubst < ${FILE})

	  # Print the query also to the OUT_FILE to have it for reference
	  echo -e "Query:\n\n${QUERY}\n\n" | tee "${OUTPUT_FILENAME}"

	  # Remove all linebreaks from the query, but add one at the end for ClickHouse
	  echo "${QUERY}" | tr '\n' ' ' | xargs -0 printf '%s\n' | clickhouse-benchmark --cumulative --user otel --password otel  --host localhost --port 9000 -i 10 2>&1 | tee --append "${OUTPUT_FILENAME}"

	  sleep 5
	done
  done
done

```

By running these benchmarks, we observed several noteworthy things:


- Compression ratio of tables "traces2", "traces3" and "traces4" were all pretty similar but not as good as the original table
- The "traces5" table (with `ORDER BY (xxh3(SpanId) % 256, ResourceHash, Timestamp)` is by far the fastest for sampling, as it can efficiently skip lots of granules to scan. But compared to the original "traces" table, it also scores very badly for any normal queries without sampling
- The “traces4” table slightly outperformed the “traces2” and “traces3” setups, but not by much
- Depending on the exact query, sampling on query time\-frames below 12 \- 24 hours did not result in much time shaved off the query duration


With these results, we decided to go with a sorting key of `ResourceHash, toStartOfHour(Timestamp), xxh3(SpanId)`. We also found a secondary `minmax` index on `Timestamp`, made the biggest difference to the query performance. It's also why the regular table performs so well and simultaneously explains why "traces5" performed so poorly, i.e. timestamps were too divided.


### Other learnings [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#other-learnings)


Finally, we’ll quickly go over a few other learnings that might not seem obvious, but could make a substantial difference.


#### Usage of indices [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#usage-of-indices)


Data skipping indexes can significantly reduce the number of granules ClickHouse needs to read, but their effectiveness depends on using compatible clauses and functions. More specifically, the different Bloom Filter types [support different functions](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree#functions-support). And while Bloom filters work well for positive matches, they cannot be used for optimizing negative matches.


When indexing `Map` contents, you can create indexes like:



```

```
INDEX idx_attr_key mapKeys(Attributes) TYPE bloom_filter(0.01) GRANULARITY 1
```

```

However, query syntax matters significantly \- especially when testing for key existence in the Map type:


- `has(Attributes, 'some_key')` will correctly utilize this Bloom Filter
- `Attributes['some_key'] = ''` (empty string) will not use the index. An intentional empty value is the same as a key not existing. These cases cannot be differentiated, and a bloom filter cannot be used for the latter.


To ensure your queries leverage available indexes, prefix them with `EXPLAIN indexes=1 <query>`. The below output clearly shows which indexes are being used and which parts of your query aren't taking advantage of available optimizations.


The `EXPLAIN` query when only looking for `Attributes['error']` values when the value is not empty (effectively the same as a key existence check):



```

```
EXPLAIN indexes = 1
SELECT Attributes['error']
FROM logs
WHERE (toDateTime(Timestamp) >= subtractMinutes(now(), 10)) AND (NOT ((Attributes['error']) = ''))

Query id: 6b792380-5937-4cb7-9617-c846a4543895

┌─explain──────────────────────────────────────────────────────────────────────┐
│ Expression ((Project names + Projection))                                    │
│   Expression                                                                 │
│     ReadFromMergeTree (logs)                                                 │
│       PrimaryKey                                                             │
│         Keys:                                                                │
│           Timestamp                                                          │
│         Condition: and((toDateTime(Timestamp) in [1741693620, +Inf)))        │
│         Parts: 11/11                                                         │
│         Granules: 3030/6868                                                  │
│       Skip                                                                   │
│         Name: idx_timestamp                                                  │
│         Description: minmax GRANULARITY 1                                    │
│         Parts: 9/11                                                          │
│         Granules: 1715/3030                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

```

The `idx_attr_key` index is not used here. Conversely, if we modify the query to use an additional has(Attributes, ‘error’) clause, the index will be exploited:



```

```
EXPLAIN indexes = 1
SELECT Attributes['error']
FROM logs
WHERE (toDateTime(Timestamp) >= subtractMinutes(now(), 10)) 
  AND (NOT ((Attributes['error']) = '')) 
  AND has(Attributes, 'error')

Query id: a5a6181f-9359-49d7-ab78-921e1cc64c86

┌─explain──────────────────────────────────────────────────────────────────────┐
│ Expression ((Project names + Projection))                                    │
│   Expression                                                                 │
│     ReadFromMergeTree (logs)                                                 │
│       PrimaryKey                                                             │
│         Keys:                                                                │
│           Timestamp                                                          │
│         Condition: and((toDateTime(Timestamp) in [1741693620, +Inf)))        │
│         Parts: 11/11                                                         │
│         Granules: 3030/6868                                                  │
│       Skip                                                                   │
│         Name: idx_timestamp                                                  │
│         Description: minmax GRANULARITY 1                                    │
│         Parts: 9/11                                                          │
│         Granules: 1715/3030                                                  │
│       Skip                                                                   │
│         Name: idx_attr_key                                                   │
│         Description: bloom_filter GRANULARITY 1                              │
│         Parts: 8/9                                                           │
│         Granules: 279/1715                                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

```

Regularly checking index usage helps maintain query performance as your table schemas and access patterns evolve.


#### JOINs and sub selects [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#joins-and-sub-selects)


When working with ClickHouse, at the time of writing, it's generally best to minimize JOINs whenever possible (although the ClickHouse team is heavily investing in this area, so stay tuned!) In most scenarios, ClickHouse performs better with sub\-selects rather than JOINs. However, when JOINs are needed, consider these recommendations:


- **Use the correct type of JOIN**. If a value on the left\-hand side matches multiple values on the right\-hand side, the JOIN will return multiple rows \- the so\-called cartesian product. If your use case doesn't need all matches from the right\-hand side but just any single match, you can use `ANY` JOINs (e.g. `LEFT ANY JOIN`). They are faster and use less memory than regular JOINs. Consult ClickHouse's documentation and blog articles for guidance on selecting optimal JOIN types.
- **Reduce the sizes of JOINed tables.** The runtime and memory consumption of JOINs grows proportionally with the sizes of the left and right tables. To reduce the amount of processed data by the JOIN, add additional filter conditions in the `WHERE` or `JOIN ON` clauses of the query. ClickHouse pushes filter conditions as deep as possible down in the query plan, usually before JOINs. If the filters are not pushed down automatically (confirm with `EXPLAIN`), rewrite one side of the JOIN as a sub\-query to force pushdown. You can also try including relevant filters directly in the JOIN condition to reduce the data volume e.g. `JOIN … ON a.ServiceName = b.ServiceName AND b.Timestamp > startTime AND b.Timestamp < endTime` . The ClickHouse team is investing in supporting automatic predicate pushdown, so this advice is subject to change.
- **Default values as no\-match markers in outer JOINs**. Left/right/full outer joins include all values from the left/right/both tables. If no join partner is found in the other table for some value, ClickHouse replaces the join partner with a special marker. The SQL standard mandates that databases use NULL as such a marker. In ClickHouse, this requires wrapping the result column in Nullable, creating an additional memory and performance overhead. As an alternative, you can configure the setting `join_use_nulls = 0` and use the default value of the result column data type as a marker.



> As the ClickHouse team invests heavily in JOIN performance, we expect the above recommendations to change and become redundant. Always check the documentation and release posts for the latest improvements.


## Conclusion [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#conclusion)


Dash0's implementation of ClickHouse as the foundational storage layer for our OpenTelemetry\-native observability platform demonstrates the power of a thoughtful database architecture. By leveraging ClickHouse's columnar structure, compression capabilities, and flexible schema design, we've created a system that efficiently handles high\-cardinality telemetry data while maintaining performance at scale. Our approach of implementing strategic primary keys and carefully designing aggregation strategies has proven critical to achieving both speed and storage efficiency.


The operational decisions around storage tiers, and implementation wise the choices for sampling strategies, indexing techniques, and JOIN optimizations reflect our commitment to combine performance with supporting high data volume and cardinality. These engineering choices stem from deep expertise with both observability systems and ClickHouse itself. As we continue to evolve Dash0, the foundation provided by ClickHouse gives us confidence that our platform can scale with our customers' growing observability needs while maintaining the query performance necessary for effective system monitoring and troubleshooting.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
