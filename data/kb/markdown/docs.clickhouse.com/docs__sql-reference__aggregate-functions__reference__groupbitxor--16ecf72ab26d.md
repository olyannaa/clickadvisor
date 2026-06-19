# groupBitXor \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupBitXor
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupBitXor.md)# groupBitXor

## groupBitXor[​](#groupBitXor "Direct link to groupBitXor")


Introduced in: v1\.1\.0


Applies bitwise XOR for series of numbers.


**Syntax**



```
groupBitXor(expr)

```

**Aliases**: `BIT_XOR`


**Arguments**


- `expr` — Expression of `(U)Int*` type. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of `(U)Int*` type. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Bitwise XOR example**



```
CREATE TABLE t (num UInt32) ENGINE = Memory;
INSERT INTO t VALUES (44), (28), (13), (85);

-- Test data:
-- binary     decimal
-- 00101100 = 44
-- 00011100 = 28
-- 00001101 = 13
-- 01010101 = 85

SELECT groupBitXor(num) FROM t;

```


```
-- Result:
-- binary     decimal
-- 01101000 = 104

┌─groupBitXor(num)─┐
│              104 │
└──────────────────┘

```
[PreviousgroupBitOr](/docs/sql-reference/aggregate-functions/reference/groupbitor)[NextgroupBitmap](/docs/sql-reference/aggregate-functions/reference/groupbitmap)- [groupBitXor](#groupBitXor)
Was this page helpful?
