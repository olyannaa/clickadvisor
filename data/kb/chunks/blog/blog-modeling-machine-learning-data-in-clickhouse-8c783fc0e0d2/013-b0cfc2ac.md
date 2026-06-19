---
source: blog
url: https://clickhouse.com/blog/transforming-ad-tech-how-cognitiv-uses-clickhouse-to-build-better-machine-learning-models
topic: modeling-machine-learning-data-in-olap-databases
ch_version_introduced: '7.886'
last_updated: '2026-06-12'
chunk_index: 13
total_chunks_in_doc: 20
---

the intermediate state of the aggregation, which the target feature table can merge together. This requires our feature table to use the [AggregatingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree) with appropriate `AggregateFunction` types. We provide an example below for a "per feature" table `number_unique_ips_per_hour.`

```
CREATE TABLE number_unique_ips_per_hour
(
  Entity String,
  EventTime DateTime64,
  -- the AggregateFunction merges states produced by the view
  Value AggregateFunction(uniqExact, UInt32)
)
ENGINE = AggregatingMergeTree
ORDER BY (Entity, EventTime)

CREATE MATERIALIZED VIEW number_unique_ips_per_hour_mv TO number_unique_ips_per_hour AS
SELECT
   domain(URL) AS Entity,
   toStartOfHour(EventTime) AS EventTime,
   -- our view uses the -State suffix to generate intermediate states
   uniqExactState(ClientIP) AS Value
FROM predict_bounce_subset
GROUP BY
   Entity,
   EventTime

```

As new rows are inserted into the `predict_bounce_subset` table, our `number_unique_ips_per_hour` feature table will be updated.

When querying `number_unique_ips_per_hour`, we must either use the `FINAL` clause or `GROUP BY Entity, EventTime` to ensure aggregation states are merged along with the [`-Merge`](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators#-merge) variant of the aggregation function (in this case, `uniqExact`). As shown this below, this alters the query used to fetch entities \- see [here](https://clickhouse.com/docs/en/materialized-view#a-more-complex-example) for further details.

```
-- Select entities for a single domain
SELECT
   EventTime,
   Entity,
   uniqExactMerge(Value) AS Value
FROM number_unique_ips_per_hour
WHERE Entity = 'smeshariki.ru'
GROUP BY
   Entity,
   EventTime
ORDER BY EventTime DESC LIMIT 5

┌───────────────EventTime─┬─Entity────────┬─Value─┐
│ 2013-07-31 23:00:00.000 │ smeshariki.ru │  3810 │
│ 2013-07-31 22:00:00.000 │ smeshariki.ru │  3895 │
│ 2013-07-31 21:00:00.000 │ smeshariki.ru │  4053 │
│ 2013-07-31 20:00:00.000 │ smeshariki.ru │  3893 │
│ 2013-07-31 19:00:00.000 │ smeshariki.ru │  3926 │
└─────────────────────────┴───────────────┴───────┘

5 rows in set. Elapsed: 0.491 sec. Processed 8.19 thousand rows, 1.28 MB (16.67 thousand rows/s., 2.61 MB/s.)
Peak memory usage: 235.93 MiB.

```

While a little more complex, intermediate aggregation states allow us to use the above table to generate features for different times. For example, we could compute the number of unique IPs per domain per day from the above table using [this query](https://pastila.nl/?021fe212/fe019875509a4475994130627bae9798#rIizu/2ZAJI1h66cUUX/bQ==), something we couldn't do with our original feature table.

Users may notice that our subset table `predict_bounce_subset` is being updated with a materialized view already, which in turn has Materialized views attached to it. As shown below, this means our Materialized views are effectively "chained". For more examples of chaining Materialized views, see [here](https://clickhouse.com/blog/chaining-materialized-views).

![chained_mvs.png](/uploads/chained_mvs_4878676d59.png)
### Updating per entity feature tables [\#](/blog/modeling-machine-learning-data-in-clickhouse#updating-per-entity-feature-tables)
