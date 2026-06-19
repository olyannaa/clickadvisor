# maxIntersectionsPosition \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- maxIntersectionsPosition
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/maxIntersectionsPosition.md)# maxIntersectionsPosition

## maxIntersectionsPosition[​](#maxIntersectionsPosition "Direct link to maxIntersectionsPosition")


Introduced in: v1\.1\.0


Aggregate function that calculates the positions of the occurrences of the [`maxIntersections`](/docs/sql-reference/aggregate-functions/reference/maxintersections) function.


**Syntax**



```
maxIntersectionsPosition(start_column, end_column)

```

**Arguments**


- `start_column` — A numeric column that represents the start of each interval. If `start_column` is `NULL` or 0 then the interval will be skipped. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `end_column` — A numeric column that represents the end of each interval. If `end_column` is `NULL` or 0 then the interval will be skipped. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the start positions of the maximum number of intersected intervals. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Finding maximum intersections position**



```
CREATE TABLE my_events (
    start UInt32,
    end UInt32
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO my_events VALUES
(1, 3),
(1, 6),
(2, 5),
(3, 7);

SELECT maxIntersectionsPosition(start, end) FROM my_events;

```


```
┌─maxIntersectionsPosition(start, end)─┐
│                                    2 │
└──────────────────────────────────────┘

```
[PreviousmaxIntersections](/docs/sql-reference/aggregate-functions/reference/maxintersections)[NextmaxMap](/docs/sql-reference/aggregate-functions/reference/maxmap)- [maxIntersectionsPosition](#maxIntersectionsPosition)
Was this page helpful?
