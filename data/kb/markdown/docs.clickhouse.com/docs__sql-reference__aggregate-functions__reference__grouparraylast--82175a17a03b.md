# groupArrayLast \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupArrayLast
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupArrayLast.md)# groupArrayLast

## groupArrayLast[​](#groupArrayLast "Direct link to groupArrayLast")


Introduced in: v23\.1\.0


Creates an array of the last argument values.
For example, `groupArrayLast(1)(x)` is equivalent to `[anyLast(x)]`.
In some cases, you can still rely on the order of execution.
This applies to cases when SELECT comes from a subquery that uses ORDER BY if the subquery result is small enough.


**Syntax**



```
groupArrayLast(max_size)(x)

```

**Parameters**


- `max_size` — Maximum size of the resulting array. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Arguments**


- `max_size` — Maximum size of the resulting array. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `x` — Argument (column name or expression). [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns an array of the last argument values. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT groupArrayLast(2)(number+1) numbers FROM numbers(10);

```


```
┌─numbers─┐
│ [9,10]  │
└─────────┘

```

**Comparison with groupArray**



```
-- Compare with groupArray (first values)
SELECT groupArray(2)(number+1) numbers FROM numbers(10);

```


```
┌─numbers─┐
│ [1,2]   │
└─────────┘

```
[PreviousgroupArrayIntersect](/docs/sql-reference/aggregate-functions/reference/grouparrayintersect)[NextgroupArrayMovingAvg](/docs/sql-reference/aggregate-functions/reference/grouparraymovingavg)- [groupArrayLast](#groupArrayLast)
Was this page helpful?
