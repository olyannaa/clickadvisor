# Window functions \| Altinity® Knowledge Base for ClickHouse®


1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. Window functions
# Window functions

#### Resources:

- [Tutorial: ClickHouse® Window Functions](https://altinity.com/blog/clickhouse-window-functions-current-state-of-the-art)
- [Video: Fun with ClickHouse Window Functions](https://www.youtube.com/watch?v=sm_vUdMQz4s)
- [Blog: Battle of the Views: ClickHouse Window View vs. Live View](https://altinity.com/blog/battle-of-the-views-clickhouse-window-view-vs-live-view)

#### How Do I Simulate Window Functions Using Arrays on older versions of ClickHouse?

1. Group with groupArray.
2. Calculate the needed metrics.
3. Ungroup back using arrayJoin.

### NTILE


```
SELECT intDiv((num - 1) - (cnt % 3), 3) AS ntile
FROM
(
    SELECT
        row_number() OVER (ORDER BY number ASC) AS num,
        count() OVER () AS cnt
    FROM numbers(11)
)

┌─ntile─┐
│     0 │
│     0 │
│     0 │
│     0 │
│     0 │
│     1 │
│     1 │
│     1 │
│     2 │
│     2 │
│     2 │
└───────┘

```
Last modified 2024\.07\.29: [Site cleanup, mostly minor changes (3e41a19\)](https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df)
