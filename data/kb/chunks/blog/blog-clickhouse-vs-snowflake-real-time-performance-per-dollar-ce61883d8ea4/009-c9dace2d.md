---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Why
topic: why-snowflake-can-t-match-clickhouse-cloud-for-real-time-analytics-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-12'
chunk_index: 9
total_chunks_in_doc: 15
---

HOW WAS PRE\-AGGREGATION LAG MEASURED? (click to expand) **SNOWFLAKE SERIES** The [MV\-lag series](https://github.com/ClickHouse/CostBench/blob/main/full-path-realtime/quotes/snowflake/results/t2/charts/run14/mv_lag_clickhouse_vs_snowflake_wide_summary.json) uses 2,072 active one\-minute [`behind_by` samples](https://github.com/ClickHouse/CostBench/blob/main/full-path-realtime/quotes/snowflake/results/t2/mv_latency_20260811T111856Z.jsonl). Poll timestamps were aligned to raw row count by linear interpolation between 208 active dashboard observations. **SMOOTHING AND READOUTS**

The reported average and maximum come from a centered 61\-sample rolling mean: 1\.372 and 2\.033 minutes, rounded to 1\.4 and 2\.0 minutes. The displayed trend adds a centered 11\-sample rolling mean and shape\-preserving interpolation. Its interactive readout follows that displayed trend at the selected row count.

**CLICKHOUSE BASELINE**

The zero line is a benchmark\-semantic baseline rather than a separately polled provider metric. The raw table and [incremental MV](https://clickhouse.com/docs/resources/support-center/knowledge-base/materialized-views/are-materialized-views-inserted-asynchronously) consume the same flushed insert block, with no independent refresh interval between them.

> ClickHouse kept pre\-aggregations current during ingestion; Snowflake’s refresh lag shifted catch\-up work onto queries.

We examine that extra work in the serving comparison below; first, the next chart accounts for preparation cost.

### Cost of keeping incoming data query\-ready \#

ClickHouse handles ① columnar storage, ② ordering raw data, and ③ ordered pre\-aggregation natively within its engine. Snowflake splits the same work across separately charged services. The chart below compares their accumulated preparation costs.

ClickHouse’s complete ingest service cost $28\.69\. Snowflake’s preparation totaled $79\.42: $53\.15 for Snowpipe Streaming’s columnar storage and ordering (① ②), plus $26\.27 for ordered pre\-aggregation through materialized\-view refresh (③), about 2\.8× as much.

> ClickHouse handled columnar storage, ordering, and pre\-aggregation in one ingest service; Snowflake’s separately charged services cost 2\.8× as much.

Now we follow the prepared raw data and summaries into query serving.

## How ClickHouse Cloud serves queries \#

Ordered raw data lets drill\-downs skip unrelated rows; pre\-aggregations let interactive aggregations combine prepared results instead of recalculating them from individual quotes. The diagram below shows both paths through ClickHouse Cloud’s read service: one node with 16 CPUs and 64 GiB of memory, matching the estimated CPU count of Snowflake’s Small warehouse.

**Drill\-downs:** Queries prune ordered raw data in the [event\-level MergeTree table](https://github.com/ClickHouse/CostBench/blob/6fb94fd628b100db69bc2bf9f8d6f149eec54601/full-path-realtime/quotes/clickhouse-cloud/create.sql#L7). Filtering by symbol, the leading column of its (sym, t) sorting key, lets the read service skip unrelated quotes.

**Interactive aggregations:** Queries read [current pre\-aggregations](https://clickhouse.com/docs/resources/support-center/knowledge-base/materialized-views/are-materialized-views-inserted-asynchronously) from the [AggregatingMergeTree table](https://github.com/ClickHouse/CostBench/blob/6fb94fd628b100db69bc2bf9f8d6f149eec54601/full-path-realtime/quotes/clickhouse-cloud/create.sql#L53), combining prepared counts, sums, minima, and maxima from a much smaller set of daily summary rows. No refresh catch\-up work is needed.
