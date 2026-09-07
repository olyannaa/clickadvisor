---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Build
topic: build-a-real-time-market-data-app-with-clickhouse-and-massive-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 9
total_chunks_in_doc: 10
---

results quickly without recalculating them each time. Start by creating a destination table to store the 1\-minute OHLCV aggregates. This table will receive the output from the materialized view and provide a structured way to access precomputed results.

```
1-- Create destination table
2CREATE TABLE trades_1min_ohlcv
3(
4    `sym` LowCardinality(String),
5    `z` Enum8('NYSE' = 1, 'AMEX' = 2, 'Nasdaq' = 3),
6    `minute_bucket_ms` UInt64,
7    `open_price_state` AggregateFunction(argMin, Float64, UInt64),
8    `high_price_state` AggregateFunction(max, Float64),
9    `low_price_state` AggregateFunction(min, Float64),
10    `close_price_state` AggregateFunction(argMax, Float64, UInt64),
11    `volume_state` AggregateFunction(sum, UInt64),
12    `trade_count_state` AggregateFunction(count)
13)
14ENGINE = SummingMergeTree
15ORDER BY (sym, minute_bucket_ms);
```
Copy command
The next step is to create the materialized view.

```
1-- Create view
2CREATE MATERIALIZED VIEW trades_1min_ohlcv_mv TO trades_1min_ohlcv
3AS SELECT
4    sym,
5    z,
6    intDiv(t, 60000) * 60000 AS minute_bucket_ms,
7    argMinState(p, t) AS open_price_state,
8    maxState(p) AS high_price_state,
9    minState(p) AS low_price_state,
10    argMaxState(p, t) AS close_price_state,
11    sumState(s) AS volume_state,
12    countState() AS trade_count_state
13FROM trades
14GROUP BY
15    sym,
16    z,
17    minute_bucket_ms;
```
Copy command
Now as each trade insert hits the trades table, the materialized view automatically processes it and updates the corresponding 1\-minute bucket in the destination table.

To view the data, execute this query.

```
1-- Query the table
2SELECT
3    sym,
4    z,
5    minute_bucket_ms,
6    fromUnixTimestamp64Milli(minute_bucket_ms) as minute_timestamp,
7    argMinMerge(open_price_state) AS open_price,
8    maxMerge(high_price_state) AS high_price,
9    minMerge(low_price_state) AS low_price,
10    argMaxMerge(close_price_state) AS close_price,
11    sumMerge(volume_state) AS volume,
12    countMerge(trade_count_state) AS trade_count
13FROM trades_1min_ohlcv
14GROUP BY sym, z, minute_bucket_ms
15ORDER BY sym, z, minute_bucket_ms;
```
Copy command
## Conclusion \#

In this post, we explored how to build a real\-time tick data application using Massive for market data and ClickHouse for fast ingestion and querying. We covered how to stream and structure tick data, manage ingestion performance, and build efficient queries and visualizations.

In this Github [repository](https://github.com/ClickHouse/examples/tree/main/stock-data-demo), you will find a working example of this using React for the visualization layer. While this is a simple example, the same principles would apply when building a production ready application at scale.

---

Share this post
