---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/array-functions.md)#
topic: array-functions-clickhouse-docs
ch_version_introduced: '25.4'
last_updated: '2026-06-12'
chunk_index: 38
total_chunks_in_doc: 49
---

`arraySymmetricDifference` simply returns the set of input elements which do not occur in all input sets. **Syntax** ``` arraySymmetricDifference(arr1, arr2, ... , arrN) ``` **Arguments** - `arrN` — N arrays from which to make the new array. [`Array(T)`](/docs/sql-reference/data-types/array).

**Returned value**

Returns an array of distinct elements not present in all source arrays [`Array(T)`](/docs/sql-reference/data-types/array)

**Examples**

**Usage example**

```
SELECT
arraySymmetricDifference([1, 2], [1, 2], [1, 2]) AS empty_symmetric_difference,
arraySymmetricDifference([1, 2], [1, 2], [1, 3]) AS non_empty_symmetric_difference;

```

```
┌─empty_symmetric_difference─┬─non_empty_symmetric_difference─┐
│ []                         │ [3,2]                          │
└────────────────────────────┴────────────────────────────────┘

```

## arrayTranspose[​](#arrayTranspose "Direct link to arrayTranspose")

Introduced in: v26\.4\.0

Transposes a two\-dimensional array.

All inner arrays must have the same length.

**Syntax**

```
arrayTranspose(arr)

```

**Arguments**

- `arr` — A two\-dimensional array to transpose. All inner arrays must have the same length. [`Array(Array(T))`](/docs/sql-reference/data-types/array)

**Returned value**

A transposed two\-dimensional array where element `[i][j]` of the result equals element `[j][i]` of the input. [`Array(Array(T))`](/docs/sql-reference/data-types/array)

**Examples**

**Square matrix**

```
SELECT arrayTranspose([[1, 2], [3, 4]])

```

```
[[1, 3], [2, 4]]

```

**Non\-square matrix**

```
SELECT arrayTranspose([[1, 2, 3], [4, 5, 6]])

```

```
[[1, 4], [2, 5], [3, 6]]

```

**String elements**

```
SELECT arrayTranspose([['a', 'b'], ['c', 'd']])

```

```
[['a', 'c'], ['b', 'd']]

```

## arrayUnion[​](#arrayUnion "Direct link to arrayUnion")

Introduced in: v24\.10\.0

Takes multiple arrays and returns an array which contains all elements that are present in one of the source arrays.The result contains only unique values.

**Syntax**

```
arrayUnion(arr1, arr2, ..., arrN)

```

**Arguments**

- `arrN` — N arrays from which to make the new array. [`Array(T)`](/docs/sql-reference/data-types/array)

**Returned value**

Returns an array with distinct elements from the source arrays [`Array(T)`](/docs/sql-reference/data-types/array)

**Examples**

**Usage example**

```
SELECT
arrayUnion([-2, 1], [10, 1], [-2], []) as num_example,
arrayUnion(['hi'], [], ['hello', 'hi']) as str_example,
arrayUnion([1, 3, NULL], [2, 3, NULL]) as null_example

```

```
┌─num_example─┬─str_example────┬─null_example─┐
│ [10,-2,1]   │ ['hello','hi'] │ [3,2,1,NULL] │
└─────────────┴────────────────┴──────────────┘

```

## arrayUniq[​](#arrayUniq "Direct link to arrayUniq")

Introduced in: v1\.1\.0

For a single argument passed, counts the number of different elements in the array.
For multiple arguments passed, it counts the number of different **tuples** made of elements at matching positions across multiple arrays.

For example `SELECT arrayUniq([1,2], [3,4], [5,6])` will form the following tuples:

- Position 1: (1,3,5\)
- Position 2: (2,4,6\)

It will then count the number of unique tuples. In this case `2`.
