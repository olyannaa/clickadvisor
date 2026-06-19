# groupArray \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupArray
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupArray.md)# groupArray

## groupArray[​](#groupArray "Direct link to groupArray")


Introduced in: v1\.1\.0


Creates an array of argument values.
Values can be added to the array in any (indeterminate) order.


The second version (with the `max_size` parameter) limits the size of the resulting array to `max_size` elements. For example, `groupArray(1)(x)` is equivalent to `[any(x)]`.


In some cases, you can still rely on the order of execution. This applies to cases when `SELECT` comes from a subquery that uses `ORDER BY` if the subquery result is small enough.


The `groupArray` function will remove `NULL` values from the result.


**Syntax**



```
groupArray(x)
groupArray(max_size)(x)

```

**Aliases**: `array_agg`


**Parameters**


- `max_size` — Optional. Limits the size of the resulting array to `max_size` elements. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Arguments**


- `x` — Argument values to collect into an array. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns an array of argument values. [`Array`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage**



```
SELECT id, groupArray(10)(name) FROM default.ck GROUP BY id;

```


```
┌─id─┬─groupArray(10)(name)─┐
│  1 │ ['zhangsan','lisi']  │
│  2 │ ['wangwu']           │
└────┴──────────────────────┘

```
[PreviousflameGraph](/docs/sql-reference/aggregate-functions/reference/flame_graph)[NextgroupArrayArray](/docs/sql-reference/aggregate-functions/reference/grouparrayarray)- [groupArray](#groupArray)
Was this page helpful?
