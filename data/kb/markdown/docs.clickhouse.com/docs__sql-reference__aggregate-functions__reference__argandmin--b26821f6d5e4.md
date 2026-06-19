# argAndMin \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- argAndMin
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/argAndMin.md)# argAndMin

## argAndMin[​](#argAndMin "Direct link to argAndMin")


Introduced in: v1\.1\.0


Calculates the `arg` and `val` value for a minimum `val` value.
If there are multiple rows with equal `val` being the minimum, which of the associated `arg` and `val` is returned is not deterministic.
Both parts the `arg` and the `min` behave as [aggregate functions](/docs/sql-reference/aggregate-functions), they both [skip `Null`](/docs/sql-reference/aggregate-functions#null-processing) during processing and return not `Null` values if not `Null` values are available.


NoteThe only difference with `argMin` is that `argAndMin` returns both argument and value.


**See also**


- [argMin](/docs/sql-reference/aggregate-functions/reference/argmin)
- [Tuple](/docs/sql-reference/data-types/tuple)


**Syntax**



```
argAndMin(arg, val)

```

**Arguments**


- `arg` — Argument for which to find the minimum value. [`const String`](/docs/sql-reference/data-types/string)
- `val` — The minimum value. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`Tuple`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple containing the `arg` value that corresponds to minimum `val` value and the minimum `val` value. [`Tuple`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT argAndMin(user, salary) FROM salary;

```


```
┌─argAndMin(user, salary)─┐
│ ('worker',1000)         │
└─────────────────────────┘

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

SELECT argMin(a,b), argAndMin(a, b), min(b) FROM test;

```


```
┌─argMin(a, b)─┬─argAndMin(a, b)─┬─min(b)─┐
│ a            │ ('a',1)         │      0 │
└──────────────┴─────────────────┴────────┘

```

**Using Tuple in arguments**



```
SELECT argAndMin(a, (b, a)), min(tuple(b, a)) FROM test;

```


```
┌─argAndMin(a, (b, a))─┬─min((b, a))─┐
│ ('a',(1,'a'))        │ (0,NULL)    │
└──────────────────────┴─────────────┘

```

**See also**


- [argMin](/docs/sql-reference/aggregate-functions/reference/argmin)
- [Tuple](/docs/sql-reference/data-types/tuple)
[PreviousargAndMax](/docs/sql-reference/aggregate-functions/reference/argandmax)[NextargMax](/docs/sql-reference/aggregate-functions/reference/argmax)- [argAndMin](#argAndMin)
Was this page helpful?
