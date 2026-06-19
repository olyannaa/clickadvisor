---
source: blog
url: https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/
topic: using-aggregate-combinators-in-clickhouse
ch_version_introduced: '10780.18000793457'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 9
---

![Distinct combinator](/uploads/4_39ec84f26a.png) Once we add `Distinct` to the aggregate function, it will ignore repeated values: ``` SELECT countDistinct(toHour(create_time)) AS hours, avgDistinct(toHour(create_time)) AS avg_hour, avg(toHour(create_time)) AS avg_hour_all FROM payments ┌─hours─┬─avg_hour─┬─avg_hour_all─┐ │ 2 │ 13.5 │ 13.74 │ └───────┴──────────┴──────────────┘ ```

Here, `avg_hour` will be calculated based on the two distinct values only, while `avg_hour_all` will be calculated based on all `100` records in the table.

### Combining `Distinct` and `If` [\#](/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states#combining-distinct-and-if)

As combinators can be combined together, we can use both previous combinators with an `avgDistinctIf` function to address more advanced logic:

```

SELECT avgDistinctIf(toHour(create_time), total_amount > 400) AS avg_hour
FROM payments

┌─avg_hour─┐
│       13 │
└──────────┘


```

This will calculate the average on distinct hour values for records with a `total_amount` value of more than `400`.

## Splitting data into groups before aggregating [\#](/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states#splitting-data-into-groups-before-aggregating)

Instead of min/max analysis, we might want to split our data into groups and calculate figures for each group separately. This can be solved using the [`Resample`](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators/#-resample) combinator.

It takes a column, range (start/stop), and a step that you want to split data on. It then returns an aggregate value for each group:

![Resample combinator](/uploads/5_37b846a84c.png)
Suppose we want to split our `payments` table data based on the `total_amount` from `0` (which is the minimum) to `500` (which is the maximum) with a step of `100`. Then, we want to know how many entries there are in each group as well as the groups average total:

```

SELECT
    countResample(0, 500, 100)(toInt16(total_amount)) AS group_entries,
    avgResample(0, 500, 100)(total_amount, toInt16(total_amount)) AS group_totals
FROM payments
FORMAT Vertical

Row 1:
──────
group_entries: [21,20,24,31,4]
group_totals:  [50.21238123802912,157.32600135803222,246.1433334350586,356.2583834740423,415.2425003051758]


```

Here, the `countResample()` function counts the number of entries in each group, and an `avgResample()` function calculates an average of the `total_amount` for each group. `Resample` combinator accepts column name to split based on as a last argument to the combined function.

Note that the `countResample()` function has only one argument (since `count()` doesn't require arguments at all) and `avgResample()` has two arguments (the first one is the column to calculate average values for). Finally, we had to use `toInt16` to convert `total_amount` to an integer since a `Resample` combinator requires this.

To get the `Resample()` combinators output in a table layout, we can use [`arrayZip()`](https://clickhouse.com/docs/en/sql-reference/functions/array-functions/#arrayzip) and [`arrayJoin()`](https://clickhouse.com/docs/en/sql-reference/functions/array-join/) functions:
