# uniqCombined \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- uniqCombined
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/uniqCombined.md)# uniqCombined

## uniqCombined[​](#uniqCombined "Direct link to uniqCombined")


Introduced in: v1\.1\.0


Calculates the approximate number of different argument values.
It provides the result deterministically (it does not depend on the query processing order).


NoteSince it uses a 32\-bit hash for non\-String types, the result will have very high error for cardinalities significantly larger than `UINT_MAX` (the error will raise quickly after a few tens of billions of distinct values).
In the case cardinalities are larger than `UINT_MAX`, you should use [`uniqCombined64`](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/uniqcombined64) instead.


Compared to the uniq function, the uniqCombined function:


- Consumes several times less memory
- Calculates with several times higher accuracy
- Usually has slightly lower performance. In some scenarios, uniqCombined can perform better than uniq, for example, with distributed queries that transmit a large number of aggregation states over the network


DetailsImplementation details
This function calculates a hash (64\-bit hash for String and 32\-bit otherwise) for all parameters in the aggregate, then uses it in calculations.
It uses a combination of three algorithms: array, hash table, and HyperLogLog with an error correction table:- For a small number of distinct elements, an array is used
- When the set size is larger, a hash table is used
- For a larger number of elements, HyperLogLog is used, which will occupy a fixed amount of memory



**Syntax**



```
uniqCombined(HLL_precision)(x[, ...])
uniqCombined(x[, ...])

```

**Parameters**


- `HLL_precision` — Optional. The base\-2 logarithm of the number of cells in HyperLogLog. The default value is 17, which is effectively 96 KiB of space (2^17 cells, 6 bits each). Range: \[12, 20]. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Arguments**


- `x` — A variable number of parameters. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a UInt64\-type number representing the approximate number of different argument values. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT uniqCombined(number) FROM numbers(1e6);

```


```
┌─uniqCombined(number)─┐
│              1001148 │
└──────────────────────┘

```

**With custom precision**



```
SELECT uniqCombined(15)(number) FROM numbers(1e5);

```


```
┌─uniqCombined(15)(number)─┐
│                   100768 │
└──────────────────────────┘

```

**See Also**


- [uniq](/docs/sql-reference/aggregate-functions/reference/uniq)
- [uniqCombined64](/docs/sql-reference/aggregate-functions/reference/uniqcombined64)
- [uniqHLL12](/docs/sql-reference/aggregate-functions/reference/uniqhll12)
- [uniqExact](/docs/sql-reference/aggregate-functions/reference/uniqexact)
- [uniqTheta](/docs/sql-reference/aggregate-functions/reference/uniqthetasketch)
[Previousuniq](/docs/sql-reference/aggregate-functions/reference/uniq)[NextuniqCombined64](/docs/sql-reference/aggregate-functions/reference/uniqcombined64)- [uniqCombined](#uniqCombined)
Was this page helpful?
