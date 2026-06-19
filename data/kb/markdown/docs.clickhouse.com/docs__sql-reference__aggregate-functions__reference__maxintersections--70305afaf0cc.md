# maxIntersections \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- maxIntersections
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/maxIntersections.md)# maxIntersections

## maxIntersections[​](#maxIntersections "Direct link to maxIntersections")


Introduced in: v20\.1\.0


Aggregate function that calculates the maximum number of times that a group of intervals intersects each other (if all the intervals intersect at least once).


**Syntax**



```
maxIntersections(start_column, end_column)

```

**Arguments**


- `start_column` — A numeric column that represents the start of each interval. If `start_column` is `NULL` or 0 then the interval will be skipped. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `end_column` — A numeric column that represents the end of each interval. If `end_column` is `NULL` or 0 then the interval will be skipped. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the maximum number of intersected intervals. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Calculating maximum intersections**



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

SELECT maxIntersections(start, end) FROM my_events;

```


```
┌─maxIntersections(start, end)─┐
│                            3 │
└──────────────────────────────┘

```
[Previousmax](/docs/sql-reference/aggregate-functions/reference/max)[NextmaxIntersectionsPosition](/docs/sql-reference/aggregate-functions/reference/maxintersectionsposition)- [maxIntersections](#maxIntersections)
Was this page helpful?
