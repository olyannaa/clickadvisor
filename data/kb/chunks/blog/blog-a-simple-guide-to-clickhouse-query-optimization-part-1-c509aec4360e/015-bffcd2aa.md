---
source: blog
url: https://clickhouse.com/resources/engineering/clickhouse-query-optimisation-definitive-guide?utm_medium=clickhouse&utm_source=blog&ref=a-simple-guide-to-clickhouse-query-optimization-part-1
topic: a-simple-guide-to-clickhouse-query-optimization-part-1
ch_version_introduced: '0.5'
last_updated: '2026-06-12'
chunk_index: 15
total_chunks_in_doc: 16
---

MiB | We can see significant improvement across the board in execution time and memory used. Query 2 benefits most from the primary key. Let’s have a look at how the query plan generated is different from before.

```
 
```
1EXPLAIN indexes = 1
2SELECT
3    payment_type,
4    COUNT() AS trip_count,
5    formatReadableQuantity(SUM(trip_distance)) AS total_distance,
6    AVG(total_amount) AS total_amount_avg,
7    AVG(tip_amount) AS tip_amount_avg
8FROM nyc_taxi.trips_small_pk
9WHERE (pickup_datetime >= '2009-01-01') AND (pickup_datetime < '2009-04-01')
10GROUP BY payment_type
11ORDER BY trip_count DESC
12
13Query id: 30116a77-ba86-4e9f-a9a2-a01670ad2e15
14
15    ┌─explain──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
16 1. │ Expression ((Projection + Before ORDER BY [lifted up part]))                                                     │
17 2. │   Sorting (Sorting for ORDER BY)                                                                                 │
18 3. │     Expression (Before ORDER BY)                                                                                 │
19 4. │       Aggregating                                                                                                │
20 5. │         Expression (Before GROUP BY)                                                                             │
21 6. │           Expression                                                                                             │
22 7. │             ReadFromMergeTree (nyc_taxi.trips_small_pk)                                                          │
23 8. │             Indexes:                                                                                             │
24 9. │               PrimaryKey                                                                                         │
2510. │                 Keys:                                                                                            │
2611. │                   pickup_datetime                                                                                │
2712. │                 Condition: and((pickup_datetime in (-Inf, 1238543999]), (pickup_datetime in [1230768000, +Inf))) │
2813. │                 Parts: 9/9                                                                                       │
2914. │                 Granules: 5061/40167                                                                             │
30    └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```

Thanks to the primary key, only a subset of the table granules has been selected. This alone greatly improves the query performance since ClickHouse has to process significantly less data.

## Conclusion  [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#conclusion)

ClickHouse is a very performant analytical database and implements a ton of performance optimization to achieve that. However, to unlock the full power of ClickHouse performance, it is necessary to understand how the database works and how you can utilize it best. By leveraging what you learned in this blog, such as identifying your less performant queries and understanding how they can be optimized by applying basic but powerful changes to your data schema, you will see significant improvements in your query performance. 

It is a great place to start if you’re unfamiliar with ClickHouse. However, if you are an experienced ClickHouse user, some of the topics discussed in this blog post might not be news to you. In our next blog, we will cover more advanced topics such as projection, materialized views, and data skipping index. Stay tuned.
