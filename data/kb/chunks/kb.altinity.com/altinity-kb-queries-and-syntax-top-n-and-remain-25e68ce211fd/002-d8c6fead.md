---
source: kb.altinity.com
url: https://github.com/Altinity/altinityknowledgebase/commit/37186d24b1effcb362a67f3c0c8a985e21213d60
topic: top-n-remain-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 3
---

999 │ 99945 │ └─────┴───────┘ ┌─k────┬──────res─┐ │ null │ 49000050 │ └──────┴──────────┘ ``` ## Method 2: Using Arrays In this method, we push the top 10 groups into an array and add a special row for the remainder

```
WITH toUInt64(sumIf(sum, isNull(k)) - sumIf(sum, isNotNull(k))) AS total
SELECT
    (arrayJoin(arrayPushBack(groupArrayIf(10)((k, sum), isNotNull(k)), (NULL, total))) AS tpl).1 AS key,
    tpl.2 AS res
FROM
(
    SELECT
        toNullable(k) AS k,
        sum(number) AS sum
    FROM top_with_rest
    GROUP BY k
        WITH CUBE
    ORDER BY sum DESC
    LIMIT 11
)
ORDER BY res ASC

┌─key──┬──────res─┐
│ 990  │    99045 │
│ 991  │    99145 │
│ 992  │    99245 │
│ 993  │    99345 │
│ 994  │    99445 │
│ 995  │    99545 │
│ 996  │    99645 │
│ 997  │    99745 │
│ 998  │    99845 │
│ 999  │    99945 │
│ null │ 49000050 │
└──────┴──────────┘

```
## Method 3: Using Window Functions

Window functions, available from ClickHouse version 21\.1, provide an efficient way to calculate the sum for the top N rows and the remainder.

```
SET allow_experimental_window_functions = 1;

SELECT
    k AS key,
    If(isNotNull(key), sum, toUInt64(sum - wind)) AS res
FROM
(
    SELECT
        *,
        sumIf(sum, isNotNull(k)) OVER () AS wind
    FROM
    (
        SELECT
            toNullable(k) AS k,
            sum(number) AS sum
        FROM top_with_rest
        GROUP BY k
            WITH CUBE
        ORDER BY sum DESC
        LIMIT 11
    )
)
ORDER BY res ASC

┌─key──┬──────res─┐
│ 990  │    99045 │
│ 991  │    99145 │
│ 992  │    99245 │
│ 993  │    99345 │
│ 994  │    99445 │
│ 995  │    99545 │
│ 996  │    99645 │
│ 997  │    99745 │
│ 998  │    99845 │
│ 999  │    99945 │
│ null │ 49000050 │
└──────┴──────────┘

```
Window functions allow efficient summation of the total and top groups in one query.

## Method 4: Using Row Number and Grouping

This approach calculates the row number (rn) for each group and replaces the remaining groups with NULL.
