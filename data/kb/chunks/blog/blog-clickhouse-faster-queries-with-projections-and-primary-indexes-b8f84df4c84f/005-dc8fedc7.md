---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Super
topic: super-charging-your-clickhouse-queries-clickhouse
ch_version_introduced: '0.044'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 12
---

less data from disk but is applying an additional optimization. The query is: - Filtering rows for town \= ‘London’ - Ordering the matching rows by price descending - Getting the top 3 rows For this, normally, ClickHouse:

- uses the primary index for selecting blocks that potentially contain ‘London’ rows and streams these rows from disk
- orders these rows in main memory by price
- streams the top 3 rows as the result to the caller

But, because the ‘London’ rows on disk are stored already ordered by price (see the table DDL’s ORDER BY clause), ClickHouse can just skip the resorting in main memory.

And ClickHouse can do short\-circuiting. All ClickHouse has to do, is to stream the selected blocks of rows from disk in reverse order, and once three matching (town \= ‘London’) rows have been streamed, the query is done.

This is exactly what the [`optimize_read_in_order`](https://clickhouse.com/docs/en/operations/settings/settings/#optimize_read_in_order) optimization is doing in this case \- preventing resorting of the rows and enabling short\-circuiting.

This optimization is enabled by default, and when we inspect the logical query plan of the query via [EXPLAIN](https://clickhouse.com/company/events/query-performance-introspection), we can see ReadType: InReverseOrder at the bottom of the plan:

```

EXPLAIN actions = 1
SELECT
    county,
    price
FROM uk_price_paid_oby_town_price
WHERE town = 'LONDON'
ORDER BY price DESC
LIMIT 3


 Expression (Projection)
 Actions: INPUT :: 0 -> price UInt32 : 0
          INPUT :: 1 -> county LowCardinality(String) : 1
 Positions: 1 0
   Limit (preliminary LIMIT (without OFFSET))
   Limit 3
   Offset 0
     Sorting (Sorting for ORDER BY)
     Prefix sort description: price DESC
     Result sort description: price DESC
     Limit 3
       Expression (Before ORDER BY)
       Actions: INPUT :: 0 -> price UInt32 : 0
                INPUT :: 1 -> county LowCardinality(String) : 1
       Positions: 0 1
         Filter (WHERE)
         Filter column: equals(town, 'LONDON') (removed)
         Actions: INPUT :: 0 -> price UInt32 : 0
                  INPUT : 1 -> town LowCardinality(String) : 1
                  INPUT :: 2 -> county LowCardinality(String) : 2
                  COLUMN Const(String) -> 'LONDON' String : 3
                  FUNCTION equals(town :: 1, 'LONDON' :: 3) -> equals(town, 'LONDON') LowCardinality(UInt8) : 4
         Positions: 0 2 4
           ReadFromMergeTree (default.uk_price_paid_oby_town_price)
           ReadType: InReverseOrder
           Parts: 6
           Granules: 267

27 rows in set. Elapsed: 0.002 sec.
 [✎](https://sql.clickhouse.com?query_id=5INADD1EKJOHLERC8VMGAP)

```
