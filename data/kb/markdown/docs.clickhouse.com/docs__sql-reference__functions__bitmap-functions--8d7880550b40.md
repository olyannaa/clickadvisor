# Bitmap Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Bitmap
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/bitmap-functions.md)# Bitmap Functions

Bitmaps can be constructed in two ways. The first way is constructed by aggregation function groupBitmap with `-State`, the other way is to constructed a bitmap from an Array object.


## bitmapAnd[​](#bitmapAnd "Direct link to bitmapAnd")


Introduced in: v20\.1\.0


Computes the logical conjunction (AND) of two bitmaps.


**Syntax**



```
bitmapAnd(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns a bitmap containing bits present in both input bitmaps [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapToArray(bitmapAnd(bitmapBuild([1, 2, 3]), bitmapBuild([3, 4, 5]))) AS res;

```


```
┌─res─┐
│ [3] │
└─────┘

```

## bitmapAndCardinality[​](#bitmapAndCardinality "Direct link to bitmapAndCardinality")


Introduced in: v20\.1\.0


Returns the cardinality of the logical conjunction (AND) of two bitmaps.


**Syntax**



```
bitmapAndCardinality(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns the number of set bits in the intersection of the two bitmaps [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapAndCardinality(bitmapBuild([1,2,3]), bitmapBuild([3,4,5])) AS res;

```


```
┌─res─┐
│   1 │
└─────┘

```

## bitmapAndnot[​](#bitmapAndnot "Direct link to bitmapAndnot")


Introduced in: v20\.1\.0


Computes the set difference A AND\-NOT B of two bitmaps.


**Syntax**



```
bitmapAndnot(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns a bitmap containing set bits present in the first bitmap but not in the second [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapToArray(bitmapAndnot(bitmapBuild([1, 2, 3]), bitmapBuild([3, 4, 5]))) AS res;

```


```
┌─res────┐
│ [1, 2] │
└────────┘

```

## bitmapAndnotCardinality[​](#bitmapAndnotCardinality "Direct link to bitmapAndnotCardinality")


Introduced in: v20\.1\.0


Returns the cardinality of the AND\-NOT operation of two bitmaps.


**Syntax**



```
bitmapAndnotCardinality(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns the number of set bits in the result of `bitmap1 AND-NOT bitmap2` [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapAndnotCardinality(bitmapBuild([1,2,3]), bitmapBuild([3,4,5])) AS res;

```


```
┌─res─┐
│   2 │
└─────┘

```

## bitmapBuild[​](#bitmapBuild "Direct link to bitmapBuild")


Introduced in: v20\.1\.0


Builds a bitmap from an unsigned integer array. It is the opposite of function [`bitmapToArray`](/docs/sql-reference/functions/bitmap-functions#bitmapToArray).


**Syntax**



```
bitmapBuild(array)

```

**Arguments**


- `array` — Unsigned integer array. [`Array(UInt*)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns a bitmap from the provided array [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapBuild([1, 2, 3, 4, 5]) AS res, toTypeName(res);

```


```
┌─res─┬─toTypeName(bitmapBuild([1, 2, 3, 4, 5]))─────┐
│     │ AggregateFunction(groupBitmap, UInt8)        │
└─────┴──────────────────────────────────────────────┘

```

## bitmapCardinality[​](#bitmapCardinality "Direct link to bitmapCardinality")


Introduced in: v20\.1\.0


Returns the number of bits set (the cardinality) in the bitmap.


**Syntax**



```
bitmapCardinality(bitmap)

```

**Arguments**


- `bitmap` — Bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns the number of bits set in the bitmap [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapCardinality(bitmapBuild([1, 3, 3, 5, 7, 7])) AS res

```


```
┌─res─┐
│   4 │
└─────┘

```

## bitmapContains[​](#bitmapContains "Direct link to bitmapContains")


Introduced in: v20\.1\.0


Checks if the bitmap contains a specific element.


**Syntax**



```
bitmapContains(bitmap, value)

```

**Arguments**


- `bitmap` — Bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `value` — Element to check for. [(U)Int8/16/32/64](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns `1` if the bitmap contains the specified value, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapContains(bitmapBuild([1, 2, 3]), 2) AS res;

```


```
┌─res─┐
│  1  │
└─────┘

```

## bitmapHasAll[​](#bitmapHasAll "Direct link to bitmapHasAll")


Introduced in: v20\.1\.0


Checks if the first bitmap contains all set bits of the second bitmap.


**Syntax**



```
bitmapHasAll(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns `1` if all set bits of the second bitmap are present in the first bitmap, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapHasAll(bitmapBuild([1, 2, 3]), bitmapBuild([2, 3])) AS res;

```


```
┌─res─┐
│  1  │
└─────┘

```

## bitmapHasAny[​](#bitmapHasAny "Direct link to bitmapHasAny")


Introduced in: v20\.1\.0


Checks if the first bitmap contains any set bits of the second bitmap.


**Syntax**



```
bitmapHasAny(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns `1` if any bits of the second bitmap are present in the first bitmap, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapHasAny(bitmapBuild([1, 2, 3]), bitmapBuild([3, 4, 5])) AS res;

```


```
┌─res─┐
│  1  │
└─────┘

```

## bitmapMax[​](#bitmapMax "Direct link to bitmapMax")


Introduced in: v20\.1\.0


Returns the position of the greatest bit set in a bitmap, or `0` if the bitmap is empty.


**Syntax**



```
bitmapMax(bitmap)

```

**Arguments**


- `bitmap` — Bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns the position of the greatest bit set in the bitmap, otherwise `0` [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapMax(bitmapBuild([1, 2, 3, 4, 5])) AS res;

```


```
┌─res─┐
│   5 │
└─────┘

```

## bitmapMin[​](#bitmapMin "Direct link to bitmapMin")


Introduced in: v20\.1\.0


Returns the position of the smallest bit set in a bitmap. If all bits are unset, or `UINT32_MAX` (`UINT64_MAX` if the bitmap contains more than `2^64` bits).


**Syntax**



```
bitmapMin(bitmap)

```

**Arguments**


- `bitmap` — Bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns the position of the smallest bit set in the bitmap, or `UINT32_MAX`/`UINT64_MAX` [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapMin(bitmapBuild([3, 5, 2, 6])) AS res;

```


```
┌─res─┐
│   2 │
└─────┘

```

## bitmapOr[​](#bitmapOr "Direct link to bitmapOr")


Introduced in: v20\.1\.0


Computes the logical disjunction (OR) of two bitmaps.


**Syntax**



```
bitmapOr(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns a bitmap containing set bits present in either input bitmap [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapToArray(bitmapOr(bitmapBuild([1, 2, 3]), bitmapBuild([3, 4, 5]))) AS res;

```


```
┌─res─────────────┐
│ [1, 2, 3, 4, 5] │
└─────────────────┘

```

## bitmapOrCardinality[​](#bitmapOrCardinality "Direct link to bitmapOrCardinality")


Introduced in: v20\.1\.0


Returns the cardinality of the logical disjunction (OR) of two bitmaps.


**Syntax**



```
bitmapOrCardinality(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns the number of set bits in the union of the two bitmaps [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapOrCardinality(bitmapBuild([1,2,3]), bitmapBuild([3,4,5])) AS res;

```


```
┌─res─┐
│   5 │
└─────┘

```

## bitmapSubsetInRange[​](#bitmapSubsetInRange "Direct link to bitmapSubsetInRange")


Introduced in: v20\.1\.0


Returns a subset of the bitmap, containing only the set bits in the specified range \[start, end). Uses 1\-based indexing.


**Syntax**



```
bitmapSubsetInRange(bitmap, start, end)

```

**Arguments**


- `bitmap` — Bitmap to extract the subset from. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `start` — Start of the range (inclusive). [`UInt*`](/docs/sql-reference/data-types/int-uint) \- `end` — End of the range (exclusive). [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a bitmap containing only the set bits in the specified range [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapToArray(bitmapSubsetInRange(bitmapBuild([1, 2, 3, 4, 5]), 2, 5)) AS res;

```


```
┌─res───────┐
│ [2, 3, 4] │
└───────────┘

```

## bitmapSubsetLimit[​](#bitmapSubsetLimit "Direct link to bitmapSubsetLimit")


Introduced in: v20\.1\.0


Returns a subset of a bitmap from position `range_start` with at most `cardinality_limit` set bits. Uses 1\-based indexing.


**Syntax**



```
bitmapSubsetLimit(bitmap, range_start, cardinality_limit)

```

**Arguments**


- `bitmap` — Bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `range_start` — Start of the range (inclusive). [`UInt32`](/docs/sql-reference/data-types/int-uint) \- `cardinality_limit` — Maximum cardinality of the subset. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a bitmap containing at most `cardinality_limit` set bits, starting from `range_start` [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapToArray(bitmapSubsetLimit(bitmapBuild([1, 5, 3, 2, 8]), 3, 2)) AS res;

```


```
┌─res────┐
│ [5, 3] │
└────────┘

```

## bitmapToArray[​](#bitmapToArray "Direct link to bitmapToArray")


Introduced in: v20\.1\.0


Converts a bitmap to an array of unsigned integers. It is the opposite of function [`bitmapBuild`](/docs/sql-reference/functions/bitmap-functions#bitmapBuild).


**Syntax**



```
bitmapToArray(bitmap)

```

**Arguments**


- `bitmap` — Bitmap to convert. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns an array of unsigned integers contained in the bitmap [`Array(UInt*)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT bitmapToArray(bitmapBuild([1, 2, 3, 4, 5])) AS res;

```


```
┌─res─────────────┐
│ [1, 2, 3, 4, 5] │
└─────────────────┘

```

## bitmapTransform[​](#bitmapTransform "Direct link to bitmapTransform")


Introduced in: v20\.1\.0


Changes up to N bits in a bitmap by swapping specific bit values in `from_array` with corresponding ones in `to_array`.


**Syntax**



```
bitmapTransform(bitmap, from_array, to_array)

```

**Arguments**


- `bitmap` — Bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `from_array` — Array of original set bits to be replaced. [`Array(T)`](/docs/sql-reference/data-types/array). \- `to_array` — Array of new set bits to replace with. [`Array(T)`](/docs/sql-reference/data-types/array).


**Returned value**


Returns a bitmap with elements transformed according to the given mapping [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapToArray(bitmapTransform(bitmapBuild([1, 2, 3, 4, 5]), [2, 4], [20, 40])) AS res;

```


```
┌─res───────────────┐
│ [1, 3, 5, 20, 40] │
└───────────────────┘

```

## bitmapXor[​](#bitmapXor "Direct link to bitmapXor")


Introduced in: v20\.1\.0


Computes the symmetric difference (XOR) of two bitmaps.


**Syntax**



```
bitmapXor(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns a bitmap containing set bits present in either input bitmap, but not in both [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapToArray(bitmapXor(bitmapBuild([1, 2, 3]), bitmapBuild([3, 4, 5]))) AS res;

```


```
┌─res──────────┐
│ [1, 2, 4, 5] │
└──────────────┘

```

## bitmapXorCardinality[​](#bitmapXorCardinality "Direct link to bitmapXorCardinality")


Introduced in: v20\.1\.0


Returns the cardinality of the XOR (symmetric difference) of two bitmaps.


**Syntax**



```
bitmapXorCardinality(bitmap1, bitmap2)

```

**Arguments**


- `bitmap1` — First bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `bitmap2` — Second bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction).


**Returned value**


Returns the number of set bits in the symmetric difference of the two bitmaps [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitmapXorCardinality(bitmapBuild([1,2,3]), bitmapBuild([3,4,5])) AS res;

```


```
┌─res─┐
│   4 │
└─────┘

```

## subBitmap[​](#subBitmap "Direct link to subBitmap")


Introduced in: v21\.9\.0


Returns a subset of the bitmap, starting from position `offset`. The maximum cardinality of the returned bitmap is `cardinality_limit`.


**Syntax**



```
subBitmap(bitmap, offset, cardinality_limit)

```

**Arguments**


- `bitmap` — Bitmap object. [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction). \- `offset` — Number of set bits to skip from the beginning (zero\-based). [`UInt32`](/docs/sql-reference/data-types/int-uint) \- `cardinality_limit` — Maximum number of set bits to include in the subset. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a bitmap containing at most `limit` set bits, starting after skipping `offset` set bits in ascending order [`AggregateFunction(groupBitmap, T)`](/docs/sql-reference/data-types/aggregatefunction)


**Examples**


**Usage example**



```
SELECT bitmapToArray(subBitmap(bitmapBuild([1, 2, 3, 4, 5]), 2, 2)) AS res;

```


```
┌─res────┐
│ [3, 4] │
└────────┘

```
[PreviousBit](/docs/sql-reference/functions/bit-functions)[NextComparison](/docs/sql-reference/functions/comparison-functions)- [bitmapAnd](#bitmapAnd)- [bitmapAndCardinality](#bitmapAndCardinality)- [bitmapAndnot](#bitmapAndnot)- [bitmapAndnotCardinality](#bitmapAndnotCardinality)- [bitmapBuild](#bitmapBuild)- [bitmapCardinality](#bitmapCardinality)- [bitmapContains](#bitmapContains)- [bitmapHasAll](#bitmapHasAll)- [bitmapHasAny](#bitmapHasAny)- [bitmapMax](#bitmapMax)- [bitmapMin](#bitmapMin)- [bitmapOr](#bitmapOr)- [bitmapOrCardinality](#bitmapOrCardinality)- [bitmapSubsetInRange](#bitmapSubsetInRange)- [bitmapSubsetLimit](#bitmapSubsetLimit)- [bitmapToArray](#bitmapToArray)- [bitmapTransform](#bitmapTransform)- [bitmapXor](#bitmapXor)- [bitmapXorCardinality](#bitmapXorCardinality)- [subBitmap](#subBitmap)
Was this page helpful?
