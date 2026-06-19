# argMin \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- argMin
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/argMin.md)# argMin

## argMin[​](#argMin "Direct link to argMin")


Introduced in: v1\.1\.0


Calculates the `arg` value for a minimum `val` value. If there are multiple rows with equal `val` being the maximum, which of the associated `arg` is returned is not deterministic.
Both parts the `arg` and the `min` behave as [aggregate functions](/docs/sql-reference/aggregate-functions), they both [skip `Null`](/docs/sql-reference/aggregate-functions#null-processing) during processing and return not `Null` values if not `Null` values are available.


**See also**


- [Tuple](/docs/sql-reference/data-types/tuple)


**Syntax**



```
argMin(arg, val)

```

**Arguments**


- `arg` — Argument for which to find the maximum value. [`const String`](/docs/sql-reference/data-types/string)
- `val` — The minimum value. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`Tuple`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the `arg` value that corresponds to minimum `val` value. Type matches `arg` type.


**Examples**


**Basic usage**



```
SELECT argMin(user, salary) FROM salary;

```


```
┌─argMin(user, salary)─┐
│ worker               │
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
FROM VALUES((NULL, 0), ('a', 1), ('b', 2), ('c', 2), (NULL, NULL), ('d', NULL));

SELECT argMin(a, b), min(b) FROM test;

```


```
┌─argMin(a, b)─┬─min(b)─┐
│ a            │      0 │
└──────────────┴────────┘

```

**Using Tuple in arguments**



```
SELECT argMin(a, (b, a)), min(tuple(b, a)) FROM test;

```


```
┌─argMin(a, tuple(b, a))─┬─min(tuple(b, a))─┐
│ d                      │ (NULL,NULL)      │
└────────────────────────┴──────────────────┘

```
[PreviousargMax](/docs/sql-reference/aggregate-functions/reference/argmax)[Nextavg](/docs/sql-reference/aggregate-functions/reference/avg)- [argMin](#argMin)
Was this page helpful?
