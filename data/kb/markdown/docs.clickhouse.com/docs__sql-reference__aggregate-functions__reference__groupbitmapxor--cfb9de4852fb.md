# groupBitmapXor \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupBitmapXor
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupBitmapXor.md)# groupBitmapXor

## groupBitmapXor[​](#groupBitmapXor "Direct link to groupBitmapXor")


Introduced in: v20\.1\.0


Calculates the XOR of a bitmap column and returns it's cardinality.
If suffix combinator [`-State`](/docs/sql-reference/aggregate-functions/combinators#-state) is added, then it returns a bitmap object.


**Syntax**



```
groupBitmapXor(expr)
groupBitmapXorState(expr)

```

**Arguments**


- `expr` — Expression that results in an `AggregateFunction(groupBitmap, UInt*)` type. [`AggregateFunction(groupBitmap, UInt*)`](/docs/sql-reference/data-types/aggregatefunction)


**Returned value**


Returns a count of type `UInt64`, or a bitmap object when using `-State`. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE bitmap_column_expr_test2
(
    tag_id String,
    z AggregateFunction(groupBitmap, UInt32)
)
ENGINE = MergeTree
ORDER BY tag_id;

INSERT INTO bitmap_column_expr_test2 VALUES ('tag1', bitmapBuild(cast([1,2,3,4,5,6,7,8,9,10] AS Array(UInt32))));
INSERT INTO bitmap_column_expr_test2 VALUES ('tag2', bitmapBuild(cast([6,7,8,9,10,11,12,13,14,15] AS Array(UInt32))));
INSERT INTO bitmap_column_expr_test2 VALUES ('tag3', bitmapBuild(cast([2,4,6,8,10,12] AS Array(UInt32))));

SELECT groupBitmapXor(z) FROM bitmap_column_expr_test2 WHERE like(tag_id, 'tag%');

```


```
┌─groupBitmapXor(z)─┐
│              10   │
└───────────────────┘

```

**Using \-State combinator**



```
SELECT arraySort(bitmapToArray(groupBitmapXorState(z))) FROM bitmap_column_expr_test2 WHERE like(tag_id, 'tag%');

```


```
┌─arraySort(bitmapToArray(groupBitmapXorState(z)))─┐
│ [1, 3, 5, 6, 8, 10, 11, 13, 14, 15]              │
└──────────────────────────────────────────────────┘

```
[PreviousgroupBitmapOr](/docs/sql-reference/aggregate-functions/reference/groupbitmapor)[NextgroupConcat](/docs/sql-reference/aggregate-functions/reference/groupconcat)- [groupBitmapXor](#groupBitmapXor)
Was this page helpful?
