---
source: blog
url: https://clickhouse.com/blog/hifis-migration-from-bigquery-to-clickhouse
topic: clickhouse-vs-bigquery-using-clickhouse-to-serve-real-time-queries-on-top-of-bigquery-data
ch_version_introduced: '22.712'
last_updated: '2026-06-12'
chunk_index: 17
total_chunks_in_doc: 20
---

60 MONTH DELETE SETTINGS ttl_only_drop_parts=1 ``` Note that partitioning can both [positively and negatively impact queries](https://medium.com/datadenys/using-partitions-in-clickhouse-3ea0decb89c4) and should be more considered a data management feature than a tool for optimizing query performance. ## Running Queries in ClickHouse [\#](/blog/clickhouse-bigquery-migrating-data-for-realtime-queries#running-queries-in-clickhouse)

This dataset warrants an entire blog on possible queries. The author of the [etherium\-etl tool](https://github.com/blockchain-etl/ethereum-etl) used to load this data into BigQuery [has published](https://evgemedvedev.medium.com/) an excellent list of blogs focused on insights with respect to this dataset. In a later blog, we’ll cover these queries and show how they can be converted to ClickHouse syntax, and how some can be significantly accelerated. For now, we present a few of the simpler queries to get started.

### Ether supply by day [\#](/blog/clickhouse-bigquery-migrating-data-for-realtime-queries#ether-supply-by-day)

The original BigQuery query, documented as part of [Awesome BigQuery views](https://github.com/blockchain-etl/awesome-bigquery-views/blob/master/ethereum/ether-supply-by-day.sql) and discussed [here](https://medium.com/google-cloud/how-to-query-ether-supply-in-bigquery-90f8ae795a8), executes in 6 seconds. The optimized ClickHouse query runs in 0\.009s, a big difference when comparing ClickHouse to BigQuery.

![ether_supply.png](/uploads/ether_supply_26efdd3501.png)

```
ALTER TABLE traces ADD PROJECTION trace_type_projection (
                    SELECT trace_type,
                    toStartOfDay(block_timestamp) as date, sum(value) as value GROUP BY trace_type, date
                    )
ALTER TABLE traces MATERIALIZE PROJECTION trace_type_projection

WITH ether_emitted_by_date AS
    (
        SELECT
            date,
            sum(value) AS value
        FROM traces
        WHERE trace_type IN ('genesis', 'reward')
        GROUP BY toStartOfDay(block_timestamp) AS date
    )
SELECT
    date,
    sum(value) OVER (ORDER BY date ASC) / power(10, 18) AS supply
FROM ether_emitted_by_date

┌────────────────date─┬────────────supply─┐
│ 1970-01-01 00:00:00 │ 72009990.49948001 │
│ 2015-07-30 00:00:00 │ 72049301.59323001 │
│ 2015-07-31 00:00:00 │    72085493.31198 │
│ 2015-08-01 00:00:00 │    72113195.49948 │
│ 2015-08-02 00:00:00 │    72141422.68698 │
...

3 rows in set. Elapsed: 0.009 sec. Processed 11.43 thousand rows, 509.00 KB (1.23 million rows/s., 54.70 MB/s.)

```

[![](/uploads/ether_supply_console_a873b69514.png)](/uploads/ether_supply_console_a873b69514.png)

Note that this query has been [optimized with a projection](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-multiple#option-3-projections) \- one of the many tools in ClickHouse we can use to optimize for a specific workload.

### Average Ether costs over time [\#](/blog/clickhouse-bigquery-migrating-data-for-realtime-queries#average-ether-costs-over-time)

Extracted from the [most popular notebook](https://www.kaggle.com/code/mrisdal/visualizing-average-ether-costs-over-time) for this dataset on Kaggle. We originally rewrote this query to include a left anti\-join, although this [doesn’t appear to be required](https://gist.github.com/gingerwizard/f3f6f7bcec5bf6ba62763b75e4385c89). The more optimized version of the query is therefore used:

![avg_ether_costs.png](/uploads/avg_ether_costs_a5b3a447ff.png)
