# argMax \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- argMax
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/argMax.md)# argMax

## argMax[​](#argMax "Direct link to argMax")


Introduced in: v1\.1\.0


Calculates the `arg` value for a maximum `val` value. If there are multiple rows with equal `val` being the maximum, which of the associated `arg` is returned is not deterministic.
Both parts the `arg` and the `max` behave as [aggregate functions](/docs/sql-reference/aggregate-functions), they both [skip `Null`](/docs/sql-reference/aggregate-functions#null-processing) during processing and return not `Null` values if not `Null` values are available.


**See also**


- [Tuple](/docs/sql-reference/data-types/tuple)


**Syntax**



```
argMax(arg, val)

```

**Arguments**


- `arg` — Argument for which to find the maximum value. [`const String`](/docs/sql-reference/data-types/string)
- `val` — The maximum value. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`Tuple`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the `arg` value that corresponds to maximum `val` value. Type matches `arg` type.


**Examples**


**Basic usage**



```
SELECT argMax(user, salary) FROM salary;

```


```
┌─argMax(user, salary)─┐
│ director             │
└──────────────────────┘

```

**Extended example with NULL handling**



```
CREATE TABLE test
(
    a Nullable(String),
    b Nullable(Int64)
)
ENGINE = Memory AS
SELECT *
FROM VALUES(('a', 1), ('b', 2), ('c', 2), (NULL, 3), (NULL, NULL), ('d', NULL));

SELECT argMax(a, b), max(b) FROM test;

```


```
┌─argMax(a, b)─┬─max(b)─┐
│ b            │      3 │
└──────────────┴────────┘

```

**Using Tuple in arguments**



```
SELECT argMax(a, (b,a)) FROM test;

```


```
┌─argMax(a, tuple(b, a))─┐
│ c                      │
└────────────────────────┘

```
[PreviousargAndMin](/docs/sql-reference/aggregate-functions/reference/argandmin)[NextargMin](/docs/sql-reference/aggregate-functions/reference/argmin)- [argMax](#argMax)
Was this page helpful?
