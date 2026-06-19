# groupBitmap \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupBitmap
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupBitmap.md)# groupBitmap

## groupBitmap[​](#groupBitmap "Direct link to groupBitmap")


Introduced in: v20\.1\.0


Creates a bitmap (bit array) from a column of unsigned integers, then returns the count of unique values (cardinality) in that bitmap.
By appending the `-State` combinator suffix, instead of returning the count, it returns the actual [bitmap object](/docs/sql-reference/functions/bitmap-functions).


**Syntax**



```
groupBitmap(expr)
groupBitmapState(expr)

```

**Arguments**


- `expr` — Expression that results in a `UInt*` type. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the count of type UInt64 type, or a bitmap object when using `-State`. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE t (UserID UInt32) ENGINE = Memory;
INSERT INTO t VALUES (1), (1), (2), (3);

SELECT groupBitmap(UserID) AS num FROM t;

```


```
┌─num─┐
│   3 │
└─────┘

```
[PreviousgroupBitXor](/docs/sql-reference/aggregate-functions/reference/groupbitxor)[NextgroupBitmapAnd](/docs/sql-reference/aggregate-functions/reference/groupbitmapand)- [groupBitmap](#groupBitmap)
Was this page helpful?
