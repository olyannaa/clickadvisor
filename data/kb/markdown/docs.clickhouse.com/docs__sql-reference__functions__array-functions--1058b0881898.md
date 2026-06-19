# Array Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Arrays
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/array-functions.md)# Array Functions

## array[​](#array "Direct link to array")


Introduced in: v1\.1\.0


Creates an array from the function arguments.


The arguments should be constants and have types that share a common supertype.
At least one argument must be passed, because otherwise it isn't clear which type of array to create.
This means that you can't use this function to create an empty array. To do so, use the `emptyArray*` function.


Use the `[ ]` operator for the same functionality.


**Syntax**



```
array(x1 [, x2, ..., xN])

```

**Arguments**


- `x1` — Constant value of any type T. If only this argument is provided, the array will be of type T. \- `[, x2, ..., xN]` — Additional N constant values sharing a common supertype with `x1`


**Returned value**


Returns an array, where 'T' is the smallest common type out of the passed arguments. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Valid usage**



```
SELECT array(toInt32(1), toUInt16(2), toInt8(3)) AS a, toTypeName(a)

```


```
┌─a───────┬─toTypeName(a)─┐
│ [1,2,3] │ Array(Int32)  │
└─────────┴───────────────┘

```

**Invalid usage**



```
SELECT array(toInt32(5), toDateTime('1998-06-16'), toInt8(5)) AS a, toTypeName(a)

```


```
Received exception from server (version 25.4.3):
Code: 386. DB::Exception: Received from localhost:9000. DB::Exception:
There is no supertype for types Int32, DateTime, Int8 ...

```

## arrayAUCPR[​](#arrayAUCPR "Direct link to arrayAUCPR")


Introduced in: v20\.4\.0


Calculates the area under the precision\-recall (PR) curve.
A precision\-recall curve is created by plotting precision on the y\-axis and recall on the x\-axis across all thresholds.
The resulting value ranges from 0 to 1, with a higher value indicating better model performance.
The PR AUC is particularly useful for imbalanced datasets, providing a clearer comparison of performance compared to ROC AUC on those cases.
For more details, please see [here](https://developers.google.com/machine-learning/glossary#pr-auc-area-under-the-pr-curve), [here](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc#expandable-1) and [here](https://en.wikipedia.org/wiki/Receiver_operating_characteristic#Area_under_the_curve).


**Syntax**



```
arrayAUCPR(scores, labels[, partial_offsets])

```

**Aliases**: `arrayPRAUC`


**Arguments**


- `cores` — Scores prediction model gives. [`Array((U)Int*)`](/docs/sql-reference/data-types/array) or [`Array(Float*)`](/docs/sql-reference/data-types/array)
- `labels` — Labels of samples, usually 1 for positive sample and 0 for negative sample. [`Array((U)Int*)`](/docs/sql-reference/data-types/array) or [`Array(Enum)`](/docs/sql-reference/data-types/array)
- `partial_offsets` —
- Optional. An [`Array(T)`](/docs/sql-reference/data-types/array) of three non\-negative integers for calculating a partial area under the PR curve (equivalent to a vertical band of the PR space) instead of the whole AUC. This option is useful for distributed computation of the PR AUC. The array must contain the following elements \[`higher_partitions_tp`, `higher_partitions_fp`, `total_positives`].
	- `higher_partitions_tp`: The number of positive labels in the higher\-scored partitions.
	- `higher_partitions_fp`: The number of negative labels in the higher\-scored partitions.
	- `total_positives`: The total number of positive samples in the entire dataset.


NoteWhen `arr_partial_offsets` is used, the `arr_scores` and `arr_labels` should be only a partition of the entire dataset, containing an interval of scores.
The dataset should be divided into contiguous partitions, where each partition contains the subset of the data whose scores fall within a specific range.
For example:- One partition could contain all scores in the range \[0, 0\.5\).
- Another partition could contain scores in the range \[0\.5, 1\.0].



**Returned value**


Returns area under the precision\-recall (PR) curve. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT arrayAUCPR([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1]);

```


```
┌─arrayAUCPR([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1])─┐
│                              0.8333333333333333 │
└─────────────────────────────────────────────────┘

```

## arrayAll[​](#arrayAll "Direct link to arrayAll")


Introduced in: v1\.1\.0


Returns `1` if lambda `func(x [, y1, y2, ... yN])` returns true for all elements. Otherwise, it returns `0`.


**Syntax**



```
arrayAll(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `cond1_arr, ...` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1` if the lambda function returns true for all elements, `0` otherwise [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**All elements match**



```
SELECT arrayAll(x, y -> x=y, [1, 2, 3], [1, 2, 3])

```


```
1

```

**Not all elements match**



```
SELECT arrayAll(x, y -> x=y, [1, 2, 3], [1, 1, 1])

```


```
0

```

## arrayAutocorrelation[​](#arrayAutocorrelation "Direct link to arrayAutocorrelation")


Introduced in: v26\.4\.0


Calculates the autocorrelation of an array.
If `max_lag` is provided, calculates correlation only for lags in range `[0, max_lag)`.
If `max_lag` is not provided, calculates for all possible lags.


**Syntax**



```
arrayAutocorrelation(arr, [max_lag])

```

**Arguments**


- `arr` — Array of numbers. [`Array(T)`](/docs/sql-reference/data-types/array)
- `max_lag` — Optional. Maximum number of lags to compute. Must be a non\-negative integer. [`Integer`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of Float64\. Returns NaN if variance is 0\. [`Array(Float64)`](/docs/sql-reference/data-types/array)


**Examples**


**Linear**



```
SELECT arrayAutocorrelation([1, 2, 3, 4, 5]);

```


```
[1, 0.4, -0.1, -0.4, -0.4]

```

**Symmetric**



```
SELECT arrayAutocorrelation([10, 20, 10]);

```


```
[1, -0.6666666666666669, 0.16666666666666674]

```

**Constant**



```
SELECT arrayAutocorrelation([5, 5, 5]);

```


```
[nan, nan, nan]

```

**Limited**



```
SELECT arrayAutocorrelation([1, 2, 3, 4, 5], 2);

```


```
[1, 0.4]

```

## arrayAvg[​](#arrayAvg "Direct link to arrayAvg")


Introduced in: v21\.1\.0


Returns the average of elements in the source array.


If a lambda function `func` is specified, returns the average of elements of the lambda results.


**Syntax**



```
arrayAvg([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — Optional. A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the average of elements in the source array, or the average of elements of the lambda results if provided. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic example**



```
SELECT arrayAvg([1, 2, 3, 4]);

```


```
2.5

```

**Usage with lambda function**



```
SELECT arrayAvg(x, y -> x*y, [2, 3], [2, 3]) AS res;

```


```
6.5

```

## arrayCompact[​](#arrayCompact "Direct link to arrayCompact")


Introduced in: v20\.1\.0


Removes consecutive duplicate elements from an array, including `null` values. The order of values in the resulting array is determined by the order in the source array.


**Syntax**



```
arrayCompact(arr)

```

**Arguments**


- `arr` — An array to remove duplicates from. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array without duplicate values [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayCompact([1, 1, nan, nan, 2, 3, 3, 3]);

```


```
[1,nan,2,3]

```

## arrayConcat[​](#arrayConcat "Direct link to arrayConcat")


Introduced in: v1\.1\.0


Combines arrays passed as arguments.


**Syntax**



```
arrayConcat(arr1 [, arr2, ... , arrN])

```

**Arguments**


- `arr1 [, arr2, ... , arrN]` — N number of arrays to concatenate. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns a single combined array from the provided array arguments. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayConcat([1, 2], [3, 4], [5, 6]) AS res

```


```
[1, 2, 3, 4, 5, 6]

```

## arrayCount[​](#arrayCount "Direct link to arrayCount")


Introduced in: v1\.1\.0


Returns the number of elements for which `func(arr1[i], ..., arrN[i])` returns true.
If `func` is not specified, it returns the number of non\-zero elements in the array.


`arrayCount` is a [higher\-order function](/docs/sql-reference/functions/overview#higher-order-functions).


**Syntax**



```
arrayCount([func, ] arr1, ...)

```

**Arguments**


- `func` — Optional. Function to apply to each element of the array(s). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `arr1, ..., arrN` — N arrays. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the number of elements for which `func` returns true. Otherwise, returns the number of non\-zero elements in the array. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT arrayCount(x -> (x % 2), groupArray(number)) FROM numbers(10)

```


```
5

```

## arrayCumSum[​](#arrayCumSum "Direct link to arrayCumSum")


Introduced in: v1\.1\.0


Returns an array of the partial (running) sums of the elements in the source array. If a lambda function is specified, the sum is computed from applying the lambda to the array elements at each position.


**Syntax**



```
arrayCumSum([func,] arr1[, arr2, ... , arrN])

```

**Arguments**


- `func` — Optional. A lambda function to apply to the array elements at each position. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `arr1` — The source array of numeric values. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[arr2, ..., arrN]` — Optional. Additional arrays of the same size, passed as arguments to the lambda function if specified. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of the partial sums of the elements in the source array. The result type matches the input array's numeric type. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage**



```
SELECT arrayCumSum([1, 1, 1, 1]) AS res

```


```
[1, 2, 3, 4]

```

**With lambda**



```
SELECT arrayCumSum(x -> x * 2, [1, 2, 3]) AS res

```


```
[2, 6, 12]

```

## arrayCumSumNonNegative[​](#arrayCumSumNonNegative "Direct link to arrayCumSumNonNegative")


Introduced in: v18\.12\.0


Returns an array of the partial (running) sums of the elements in the source array, replacing any negative running sum with zero. If a lambda function is specified, the sum is computed from applying the lambda to the array elements at each position.


**Syntax**



```
arrayCumSumNonNegative([func,] arr1[, arr2, ... , arrN])

```

**Arguments**


- `func` — Optional. A lambda function to apply to the array elements at each position. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `arr1` — The source array of numeric values. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[arr2, ..., arrN]` — Optional. Additional arrays of the same size, passed as arguments to the lambda function if specified. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of the partial sums of the elements in the source array, with any negative running sum replaced by zero. The result type matches the input array's numeric type. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage**



```
SELECT arrayCumSumNonNegative([1, 1, -4, 1]) AS res

```


```
[1, 2, 0, 1]

```

**With lambda**



```
SELECT arrayCumSumNonNegative(x -> x * 2, [1, -2, 3]) AS res

```


```
[2, 0, 6]

```

## arrayDifference[​](#arrayDifference "Direct link to arrayDifference")


Introduced in: v1\.1\.0


Calculates an array of differences between adjacent array elements.
The first element of the result array will be 0, the second `arr[1] - arr[0]`, the third `arr[2] - arr[1]`, etc.
The type of elements in the result array are determined by the type inference rules for subtraction (e.g. `UInt8` \- `UInt8` \= `Int16`).


**Syntax**



```
arrayDifference(arr)

```

**Arguments**


- `arr` — Array for which to calculate differences between adjacent elements. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of differences between adjacent array elements [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT arrayDifference([1, 2, 3, 4]);

```


```
[0,1,1,1]

```

**Example of overflow due to result type Int64**



```
SELECT arrayDifference([0, 10000000000000000000]);

```


```
┌─arrayDifference([0, 10000000000000000000])─┐
│ [0,-8446744073709551616]                   │
└────────────────────────────────────────────┘

```

## arrayDistinct[​](#arrayDistinct "Direct link to arrayDistinct")


Introduced in: v1\.1\.0


Returns an array containing only the distinct elements of an array.


**Syntax**



```
arrayDistinct(arr)

```

**Arguments**


- `arr` — Array for which to extract distinct elements. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array containing the distinct elements [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayDistinct([1, 2, 2, 3, 1]);

```


```
[1,2,3]

```

## arrayDotProduct[​](#arrayDotProduct "Direct link to arrayDotProduct")


Introduced in: v23\.5\.0


Returns the dot product of two arrays.


NoteThe sizes of the two vectors must be equal. Arrays and Tuples may also contain mixed element types.


**Syntax**



```
arrayDotProduct(v1, v2)

```

**Arguments**


- `v1` — First vector. [`Array((U)Int* | Float* | Decimal)`](/docs/sql-reference/data-types/array) or [`Tuple((U)Int* | Float* | Decimal)`](/docs/sql-reference/data-types/tuple)
- `v2` — Second vector. [`Array((U)Int* | Float* | Decimal)`](/docs/sql-reference/data-types/array) or [`Tuple((U)Int* | Float* | Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


The dot product of the two vectors.


NoteThe return type is determined by the type of the arguments. If Arrays or Tuples contain mixed element types then the result type is the supertype.


[`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Examples**


**Array example**



```
SELECT arrayDotProduct([1, 2, 3], [4, 5, 6]) AS res, toTypeName(res);

```


```
32    UInt16

```

**Tuple example**



```
SELECT dotProduct((1::UInt16, 2::UInt8, 3::Float32),(4::Int16, 5::Float32, 6::UInt8)) AS res, toTypeName(res);

```


```
32    Float64

```

## arrayElement[​](#arrayElement "Direct link to arrayElement")


Introduced in: v1\.1\.0


Gets the element of the provided array with index `n` where `n` can be any integer type.
If the index falls outside of the bounds of an array, it returns a default value (0 for numbers, an empty string for strings, etc.),
except for arguments of a non\-constant array and a constant index 0\. In this case there will be an error `Array indices are 1-based`.


NoteArrays in ClickHouse are one\-indexed.


Negative indexes are supported. In this case, the corresponding element is selected, numbered from the end. For example, `arr[-1]` is the last item in the array.


Operator `[n]` provides the same functionality.


**Syntax**



```
arrayElement(arr, n)

```

**Arguments**


- `arr` — The array to search. [`Array(T)`](/docs/sql-reference/data-types/array). \- `n` — Position of the element to get. [`(U)Int*`](/docs/sql-reference/data-types/int-uint).


**Returned value**


Returns a single combined array from the provided array arguments [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayElement(arr, 2) FROM (SELECT [1, 2, 3] AS arr)

```


```
2

```

**Negative indexing**



```
SELECT arrayElement(arr, -1) FROM (SELECT [1, 2, 3] AS arr)

```


```
3

```

**Using \[n] notation**



```
SELECT arr[2] FROM (SELECT [1, 2, 3] AS arr)

```


```
2

```

**Index out of array bounds**



```
SELECT arrayElement(arr, 4) FROM (SELECT [1, 2, 3] AS arr)

```


```
0

```

## arrayElementOrNull[​](#arrayElementOrNull "Direct link to arrayElementOrNull")


Introduced in: v1\.1\.0


Gets the element of the provided array with index `n` where `n` can be any integer type.
If the index falls outside of the bounds of an array, `NULL` is returned instead of a default value.


NoteArrays in ClickHouse are one\-indexed.


Negative indexes are supported. In this case, it selects the corresponding element numbered from the end. For example, `arr[-1]` is the last item in the array.


**Syntax**



```
arrayElementOrNull(arrays)

```

**Arguments**


- `arrays` — Arbitrary number of array arguments. [`Array`](/docs/sql-reference/data-types/array)


**Returned value**


Returns a single combined array from the provided array arguments. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayElementOrNull(arr, 2) FROM (SELECT [1, 2, 3] AS arr)

```


```
2

```

**Negative indexing**



```
SELECT arrayElementOrNull(arr, -1) FROM (SELECT [1, 2, 3] AS arr)

```


```
3

```

**Index out of array bounds**



```
SELECT arrayElementOrNull(arr, 4) FROM (SELECT [1, 2, 3] AS arr)

```


```
NULL

```

## arrayEnumerate[​](#arrayEnumerate "Direct link to arrayEnumerate")


Introduced in: v1\.1\.0


Returns the array `[1, 2, 3, ..., length (arr)]`


This function is normally used with the [`ARRAY JOIN`](/docs/sql-reference/statements/select/array-join) clause. It allows counting something just
once for each array after applying `ARRAY JOIN`.
This function can also be used in higher\-order functions. For example, you can use it to get array indexes for elements that match a condition.


**Syntax**



```
arrayEnumerate(arr)

```

**Arguments**


- `arr` — The array to enumerate. [`Array`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the array `[1, 2, 3, ..., length (arr)]`. [`Array(UInt32)`](/docs/sql-reference/data-types/array)


**Examples**


**Basic example with ARRAY JOIN**



```
CREATE TABLE test
(
    `id` UInt8,
    `tag` Array(String),
    `version` Array(String)
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO test VALUES (1, ['release-stable', 'dev', 'security'], ['2.4.0', '2.6.0-alpha', '2.4.0-sec1']);

SELECT
    id,
    tag,
    version,
    seq
FROM test
ARRAY JOIN
    tag,
    version,
    arrayEnumerate(tag) AS seq

```


```
┌─id─┬─tag────────────┬─version─────┬─seq─┐
│  1 │ release-stable │ 2.4.0       │   1 │
│  1 │ dev            │ 2.6.0-alpha │   2 │
│  1 │ security       │ 2.4.0-sec1  │   3 │
└────┴────────────────┴─────────────┴─────┘

```

## arrayEnumerateDense[​](#arrayEnumerateDense "Direct link to arrayEnumerateDense")


Introduced in: v18\.12\.0


Returns an array of the same size as the source array, indicating where each element first appears in the source array.


**Syntax**



```
arrayEnumerateDense(arr)

```

**Arguments**


- `arr` — The array to enumerate. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of the same size as `arr`, indicating where each element first appears in the source array [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayEnumerateDense([10, 20, 10, 30])

```


```
[1,2,1,3]

```

## arrayEnumerateDenseRanked[​](#arrayEnumerateDenseRanked "Direct link to arrayEnumerateDenseRanked")


Introduced in: v20\.1\.0


Returns an array the same size as the source array, indicating where each element first appears in the source array. It allows for enumeration of a multidimensional array with the ability to specify how deep to look inside the array.


**Syntax**



```
arrayEnumerateDenseRanked(clear_depth, arr, max_array_depth)

```

**Arguments**


- `clear_depth` — Enumerate elements at the specified level separately. Must be less than or equal to `max_arr_depth`. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `arr` — N\-dimensional array to enumerate. [`Array(T)`](/docs/sql-reference/data-types/array)
- `max_array_depth` — The maximum effective depth. Must be less than or equal to the depth of `arr`. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array denoting where each element first appears in the source array [`Array`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage**



```
-- With clear_depth=1 and max_array_depth=1, the result is identical to what arrayEnumerateDense would give.

SELECT arrayEnumerateDenseRanked(1,[10, 20, 10, 30],1);

```


```
[1,2,1,3]

```

**Usage with a multidimensional array**



```
-- In this example, arrayEnumerateDenseRanked is used to obtain an array indicating, for each element of the
-- multidimensional array, what its position is among elements of the same value.
-- For the first row of the passed array, [10, 10, 30, 20], the corresponding first row of the result is [1, 1, 2, 3],
-- indicating that 10 is the first number encountered in position 1 and 2, 30 the second number encountered in position 3
-- and 20 is the third number encountered in position 4.
-- For the second row, [40, 50, 10, 30], the corresponding second row of the result is [4,5,1,2], indicating that 40
-- and 50 are the fourth and fifth numbers encountered in position 1 and 2 of that row, that another 10
-- (the first encountered number) is in position 3 and 30 (the second number encountered) is in the last position.

SELECT arrayEnumerateDenseRanked(1,[[10,10,30,20],[40,50,10,30]],2);

```


```
[[1,1,2,3],[4,5,1,2]]

```

**Example with increased clear\_depth**



```
-- Changing clear_depth=2 results in the enumeration occurring separately for each row anew.

SELECT arrayEnumerateDenseRanked(2,[[10,10,30,20],[40,50,10,30]],2);

```


```
[[1, 1, 2, 3], [1, 2, 3, 4]]

```

## arrayEnumerateUniq[​](#arrayEnumerateUniq "Direct link to arrayEnumerateUniq")


Introduced in: v1\.1\.0


Returns an array the same size as the source array, indicating for each element what its position is among elements with the same value.


This function is useful when using `ARRAY JOIN` and aggregation of array elements.


The function can take multiple arrays of the same size as arguments. In this case, uniqueness is considered for tuples of elements in the same positions in all the arrays.


**Syntax**



```
arrayEnumerateUniq(arr1[, arr2, ... , arrN])

```

**Arguments**


- `arr1` — First array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `arr2, ...` — Optional. Additional arrays of the same size for tuple uniqueness. [`Array(UInt32)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array where each element is the position among elements with the same value or tuple. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage**



```
SELECT arrayEnumerateUniq([10, 20, 10, 30]);

```


```
[1, 1, 2, 1]

```

**Multiple arrays**



```
SELECT arrayEnumerateUniq([1, 1, 1, 2, 2, 2], [1, 1, 2, 1, 1, 2]);

```


```
[1,2,1,1,2,1]

```

**ARRAY JOIN aggregation**



```
-- Each goal ID has a calculation of the number of conversions (each element in the Goals nested data structure is a goal that was reached, which we refer to as a conversion)
-- and the number of sessions. Without ARRAY JOIN, we would have counted the number of sessions as sum(Sign). But in this particular case,
-- the rows were multiplied by the nested Goals structure, so in order to count each session one time after this, we apply a condition to the
-- value of the arrayEnumerateUniq(Goals.ID) function.

SELECT
    Goals.ID AS GoalID,
    sum(Sign) AS Reaches,
    sumIf(Sign, num = 1) AS Visits
FROM test.visits
ARRAY JOIN
    Goals,
    arrayEnumerateUniq(Goals.ID) AS num
WHERE CounterID = 160656
GROUP BY GoalID
ORDER BY Reaches DESC
LIMIT 10

```


```
┌──GoalID─┬─Reaches─┬─Visits─┐
│   53225 │    3214 │   1097 │
│ 2825062 │    3188 │   1097 │
│   56600 │    2803 │    488 │
│ 1989037 │    2401 │    365 │
│ 2830064 │    2396 │    910 │
│ 1113562 │    2372 │    373 │
│ 3270895 │    2262 │    812 │
│ 1084657 │    2262 │    345 │
│   56599 │    2260 │    799 │
│ 3271094 │    2256 │    812 │
└─────────┴─────────┴────────┘

```

## arrayEnumerateUniqRanked[​](#arrayEnumerateUniqRanked "Direct link to arrayEnumerateUniqRanked")


Introduced in: v20\.1\.0


Returns an array (or multi\-dimensional array) with the same dimensions as the source array,
indicating for each element what it's position is among elements with the same value.
It allows for enumeration of a multi\-dimensional array with the ability to specify how deep to look inside the array.


**Syntax**



```
arrayEnumerateUniqRanked(clear_depth, arr, max_array_depth)

```

**Arguments**


- `clear_depth` — Enumerate elements at the specified level separately. Positive integer less than or equal to `max_arr_depth`. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `arr` — N\-dimensional array to enumerate. [`Array(T)`](/docs/sql-reference/data-types/array)
- `max_array_depth` — The maximum effective depth. Positive integer less than or equal to the depth of `arr`. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an N\-dimensional array the same size as `arr` with each element showing the position of that element in relation to other elements of the same value. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Example 1**



```
-- With clear_depth=1 and max_array_depth=1, the result of arrayEnumerateUniqRanked
-- is identical to that which arrayEnumerateUniq would give for the same array.

SELECT arrayEnumerateUniqRanked(1, [1, 2, 1], 1);

```


```
[1, 1, 2]

```

**Example 2**



```
-- with clear_depth=1 and max_array_depth=1, the result of arrayEnumerateUniqRanked
-- is identical to that which arrayEnumerateUniqwould give for the same array.

SELECT arrayEnumerateUniqRanked(1, [[1, 2, 3], [2, 2, 1], [3]], 2);", "[[1, 1, 1], [2, 3, 2], [2]]

```


```
[1, 1, 2]

```

**Example 3**



```
-- In this example, arrayEnumerateUniqRanked is used to obtain an array indicating,
-- for each element of the multidimensional array, what its position is among elements
-- of the same value. For the first row of the passed array, [1, 2, 3], the corresponding
-- result is [1, 1, 1], indicating that this is the first time 1, 2 and 3 are encountered.
-- For the second row of the provided array, [2, 2, 1], the corresponding result is [2, 3, 3],
-- indicating that 2 is encountered for a second and third time, and 1 is encountered
-- for the second time. Likewise, for the third row of the provided array [3] the
-- corresponding result is [2] indicating that 3 is encountered for the second time.

SELECT arrayEnumerateUniqRanked(1, [[1, 2, 3], [2, 2, 1], [3]], 2);

```


```
[[1, 1, 1], [2, 3, 2], [2]]

```

**Example 4**



```
-- Changing clear_depth=2, results in elements being enumerated separately for each row.
SELECT arrayEnumerateUniqRanked(2,[[1, 2, 3],[2, 2, 1],[3]], 2);

```


```
[[1, 1, 1], [1, 2, 1], [1]]

```

## arrayExcept[​](#arrayExcept "Direct link to arrayExcept")


Introduced in: v25\.9\.0


Returns an array containing elements from `source` that are not present in `except`, preserving the original order.


This function performs a set difference operation between two arrays. For each element in `source`, it checks if the element exists in `except` (using exact comparison). If not, the element is included in the result.


The operation maintains these properties:


1. Order of elements from `source` is preserved
2. Duplicates in `source` are preserved if they don't exist in `except`
3. NULL is handled as a separate value


**Syntax**



```
arrayExcept(source, except)

```

**Arguments**


- `source` — The source array containing elements to filter. [`Array(T)`](/docs/sql-reference/data-types/array)
- `except` — The array containing elements to exclude from the result. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of the same type as the input array containing elements from `source` that weren't found in `except`. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**basic**



```
SELECT arrayExcept([1, 2, 3, 2, 4], [3, 5])

```


```
[1, 2, 2, 4]

```

**with\_nulls1**



```
SELECT arrayExcept([1, NULL, 2, NULL], [2])

```


```
[1, NULL, NULL]

```

**with\_nulls2**



```
SELECT arrayExcept([1, NULL, 2, NULL], [NULL, 2, NULL])

```


```
[1]

```

**strings**



```
SELECT arrayExcept(['apple', 'banana', 'cherry'], ['banana', 'date'])

```


```
['apple', 'cherry']

```

## arrayExists[​](#arrayExists "Direct link to arrayExists")


Introduced in: v1\.1\.0


Returns `1` if there is at least one element in a source array for which `func(x[, y1, y2, ... yN])` returns true. Otherwise, it returns `0`.


**Syntax**



```
arrayExists(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1` if the lambda function returns true for at least one element, `0` otherwise [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT arrayExists(x, y -> x=y, [1, 2, 3], [0, 0, 0])

```


```
0

```

## arrayFill[​](#arrayFill "Direct link to arrayFill")


Introduced in: v20\.1\.0


The `arrayFill` function sequentially processes a source array from the first element
to the last, evaluating a lambda condition at each position using elements from
the source and condition arrays. When the lambda function evaluates to false at
position i, the function replaces that element with the element at position i\-1
from the current state of the array. The first element is always preserved
regardless of any condition.


**Syntax**



```
arrayFill(func(x [, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x [, y1, ..., yN])` — A lambda function `func(x [, y1, y2, ... yN]) → F(x [, y1, y2, ... yN])` which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Example with single array**



```
SELECT arrayFill(x -> not isNull(x), [1, null, 2, null]) AS res

```


```
[1, 1, 2, 2]

```

**Example with two arrays**



```
SELECT arrayFill(x, y, z -> x > y AND x < z, [5, 3, 6, 2], [4, 7, 1, 3], [10, 2, 8, 5]) AS res

```


```
[5, 5, 6, 6]

```

## arrayFilter[​](#arrayFilter "Direct link to arrayFilter")


Introduced in: v1\.1\.0


Returns an array containing only the elements in the source array for which a lambda function returns true.


**Syntax**



```
arrayFilter(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])]

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns a subset of the source array [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Example 1**



```
SELECT arrayFilter(x -> x LIKE '%World%', ['Hello', 'abc World']) AS res

```


```
['abc World']

```

**Example 2**



```
SELECT
    arrayFilter(
        (i, x) -> x LIKE '%World%',
        arrayEnumerate(arr),
        ['Hello', 'abc World'] AS arr)
    AS res

```


```
[2]

```

## arrayFirst[​](#arrayFirst "Direct link to arrayFirst")


Introduced in: v1\.1\.0


Returns the first element in the source array for which `func(x[, y1, y2, ... yN])` returns true, otherwise it returns a default value.


**Syntax**



```
arrayFirst(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [Lambda function](/docs/sql-reference/functions/overview#arrow-operator-and-lambda). \- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array). \- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array).


**Returned value**


Returns the first element of the source array for which `λ` is true, otherwise returns the default value of `T`.


**Examples**


**Usage example**



```
SELECT arrayFirst(x, y -> x=y, ['a', 'b', 'c'], ['c', 'b', 'a'])

```


```
b

```

**No match**



```
SELECT arrayFirst(x, y -> x=y, [0, 1, 2], [3, 3, 3]) AS res, toTypeName(res)

```


```
0 UInt8

```

## arrayFirstIndex[​](#arrayFirstIndex "Direct link to arrayFirstIndex")


Introduced in: v1\.1\.0


Returns the index of the first element in the source array for which `func(x[, y1, y2, ... yN])` returns true, otherwise it returns '0'.


**Syntax**



```
arrayFirstIndex(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [Lambda function](/docs/sql-reference/functions/overview#arrow-operator-and-lambda). \- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array). \- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array).


**Returned value**


Returns the index of the first element of the source array for which `func` is true, otherwise returns `0` [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT arrayFirstIndex(x, y -> x=y, ['a', 'b', 'c'], ['c', 'b', 'a'])

```


```
2

```

**No match**



```
SELECT arrayFirstIndex(x, y -> x=y, ['a', 'b', 'c'], ['d', 'e', 'f'])

```


```
0

```

## arrayFirstOrNull[​](#arrayFirstOrNull "Direct link to arrayFirstOrNull")


Introduced in: v1\.1\.0


Returns the first element in the source array for which `func(x[, y1, y2, ... yN])` returns true, otherwise it returns `NULL`.


**Syntax**



```
arrayFirstOrNull(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the first element of the source array for which `func` is true, otherwise returns `NULL`.


**Examples**


**Usage example**



```
SELECT arrayFirstOrNull(x, y -> x=y, ['a', 'b', 'c'], ['c', 'b', 'a'])

```


```
b

```

**No match**



```
SELECT arrayFirstOrNull(x, y -> x=y, [0, 1, 2], [3, 3, 3]) AS res, toTypeName(res)

```


```
NULL Nullable(UInt8)

```

## arrayFlatten[​](#arrayFlatten "Direct link to arrayFlatten")


Introduced in: v20\.1\.0


Converts an array of arrays to a flat array.


Function:


- Applies to any depth of nested arrays.
- Does not change arrays that are already flat.


The flattened array contains all the elements from all source arrays.


**Syntax**



```
arrayFlatten(arr)

```

**Aliases**: `flatten`


**Arguments**


- `arr` — A multidimensional array. [`Array(Array(T))`](/docs/sql-reference/data-types/array)


**Returned value**


Returns a flattened array from the multidimensional array [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayFlatten([[[1]], [[2], [3]]]);

```


```
[1, 2, 3]

```

## arrayFold[​](#arrayFold "Direct link to arrayFold")


Introduced in: v23\.10\.0


Applies a lambda function to one or more equally\-sized arrays and collects the result in an accumulator.


**Syntax**



```
arrayFold(λ(acc, x1 [, x2, x3, ... xN]), arr1 [, arr2, arr3, ... arrN], acc)

```

**Arguments**


- `λ(x, x1 [, x2, x3, ... xN])` — A lambda function `λ(acc, x1 [, x2, x3, ... xN]) → F(acc, x1 [, x2, x3, ... xN])` where `F` is an operation applied to `acc` and array values from `x` with the result of `acc` re\-used. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `arr1 [, arr2, arr3, ... arrN]` — N arrays over which to operate. [`Array(T)`](/docs/sql-reference/data-types/array)
- `acc` — Accumulator value with the same type as the return type of the Lambda function.


**Returned value**


Returns the final `acc` value.


**Examples**


**Usage example**



```
SELECT arrayFold(acc,x -> acc + x*2, [1, 2, 3, 4], 3::Int64) AS res;

```


```
23

```

**Fibonacci sequence**



```
SELECT arrayFold(acc, x -> (acc.2, acc.2 + acc.1),range(number),(1::Int64, 0::Int64)).1 AS fibonacci FROM numbers(1,10);

```


```
┌─fibonacci─┐
│         0 │
│         1 │
│         1 │
│         2 │
│         3 │
│         5 │
│         8 │
│        13 │
│        21 │
│        34 │
└───────────┘

```

**Example using multiple arrays**



```
SELECT arrayFold(
(acc, x, y) -> acc + (x * y),
[1, 2, 3, 4],
[10, 20, 30, 40],
0::Int64
) AS res;

```


```
300

```

## arrayIntersect[​](#arrayIntersect "Direct link to arrayIntersect")


Introduced in: v1\.1\.0


Takes multiple arrays and returns an array with elements which are present in all source arrays. The result contains only unique values.


**Syntax**



```
arrayIntersect(arr, arr1, ..., arrN)

```

**Arguments**


- `arrN` — N arrays from which to make the new array. [`Array(T)`](/docs/sql-reference/data-types/array).


**Returned value**


Returns an array with distinct elements that are present in all N arrays [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT
arrayIntersect([1, 2], [1, 3], [2, 3]) AS empty_intersection,
arrayIntersect([1, 2], [1, 3], [1, 4]) AS non_empty_intersection

```


```
┌─empty_intersection─┬─non_empty_intersection─┐
│ []                 │ [1]                    │
└────────────────────┴────────────────────────┘

```

## arrayJaccardIndex[​](#arrayJaccardIndex "Direct link to arrayJaccardIndex")


Introduced in: v23\.7\.0


Returns the [Jaccard index](https://en.wikipedia.org/wiki/Jaccard_index) of two arrays.


**Syntax**



```
arrayJaccardIndex(arr_x, arr_y)

```

**Arguments**


- `arr_x` — First array. [`Array(T)`](/docs/sql-reference/data-types/array)
- `arr_y` — Second array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the Jaccard index of `arr_x` and `arr_y` [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT arrayJaccardIndex([1, 2], [2, 3]) AS res

```


```
0.3333333333333333

```

## arrayJoin[​](#arrayJoin "Direct link to arrayJoin")


Introduced in: v1\.1\.0


The `arrayJoin` function takes a row that contains an array and unfolds it, generating multiple rows – one for each element in the array.
This is in contrast to Regular Functions in ClickHouse which map input values to output values within the same row,
and Aggregate Functions which take a group of rows and "compress" or "reduce" them into a single summary row
(or a single value within a summary row if used with `GROUP BY`).


All the values in the columns are simply copied, except the values in the column where this function is applied;
these are replaced with the corresponding array value.


**Syntax**



```
arrayJoin(arr)

```

**Aliases**: `unnest`


**Arguments**


- `arr` — An array to unfold. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns a set of rows unfolded from `arr`.


**Examples**


**Basic usage**



```
SELECT arrayJoin([1, 2, 3] AS src) AS dst, 'Hello', src

```


```
┌─dst─┬─\'Hello\'─┬─src─────┐
│   1 │ Hello     │ [1,2,3] │
│   2 │ Hello     │ [1,2,3] │
│   3 │ Hello     │ [1,2,3] │
└─────┴───────────┴─────────┘

```

**arrayJoin affects all sections of the query**



```
-- The arrayJoin function affects all sections of the query, including the WHERE section. Notice the result 2, even though the subquery returned 1 row.

SELECT sum(1) AS impressions
FROM
(
    SELECT ['Istanbul', 'Berlin', 'Bobruisk'] AS cities
)
WHERE arrayJoin(cities) IN ['Istanbul', 'Berlin'];

```


```
┌─impressions─┐
│           2 │
└─────────────┘

```

**Using multiple arrayJoin functions**



```
- A query can use multiple arrayJoin functions. In this case, the transformation is performed multiple times and the rows are multiplied.

SELECT
    sum(1) AS impressions,
    arrayJoin(cities) AS city,
    arrayJoin(browsers) AS browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Bobruisk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
GROUP BY
    2,
    3

```


```
┌─impressions─┬─city─────┬─browser─┐
│           2 │ Istanbul │ Chrome  │
│           1 │ Istanbul │ Firefox │
│           2 │ Berlin   │ Chrome  │
│           1 │ Berlin   │ Firefox │
│           2 │ Bobruisk │ Chrome  │
│           1 │ Bobruisk │ Firefox │
└─────────────┴──────────┴─────────┘

```

**Unexpected results due to optimizations**



```
-- Using multiple arrayJoin with the same expression may not produce the expected result due to optimizations.
-- For these cases, consider modifying the repeated array expression with extra operations that do not affect join result.
- e.g. arrayJoin(arraySort(arr)), arrayJoin(arrayConcat(arr, []))

SELECT
    arrayJoin(dice) as first_throw,
    /* arrayJoin(dice) as second_throw */ -- is technically correct, but will annihilate result set
    arrayJoin(arrayConcat(dice, [])) as second_throw -- intentionally changed expression to force re-evaluation
FROM (
    SELECT [1, 2, 3, 4, 5, 6] as dice
);

```


```
┌─first_throw─┬─second_throw─┐
│           1 │            1 │
│           1 │            2 │
│           1 │            3 │
│           1 │            4 │
│           1 │            5 │
│           1 │            6 │
│           2 │            1 │
│           2 │            2 │
│           2 │            3 │
│           2 │            4 │
│           2 │            5 │
│           2 │            6 │
│           3 │            1 │
│           3 │            2 │
│           3 │            3 │
│           3 │            4 │
│           3 │            5 │
│           3 │            6 │
│           4 │            1 │
│           4 │            2 │
│           4 │            3 │
│           4 │            4 │
│           4 │            5 │
│           4 │            6 │
│           5 │            1 │
│           5 │            2 │
│           5 │            3 │
│           5 │            4 │
│           5 │            5 │
│           5 │            6 │
│           6 │            1 │
│           6 │            2 │
│           6 │            3 │
│           6 │            4 │
│           6 │            5 │
│           6 │            6 │
└─────────────┴──────────────┘

```

**Using the ARRAY JOIN syntax**



```
-- Note the ARRAY JOIN syntax in the `SELECT` query below, which provides broader possibilities.
-- ARRAY JOIN allows you to convert multiple arrays with the same number of elements at a time.

SELECT
    sum(1) AS impressions,
    city,
    browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Bobruisk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
ARRAY JOIN
    cities AS city,
    browsers AS browser
GROUP BY
    2,
    3

```


```
┌─impressions─┬─city─────┬─browser─┐
│           1 │ Istanbul │ Firefox │
│           1 │ Berlin   │ Chrome  │
│           1 │ Bobruisk │ Chrome  │
└─────────────┴──────────┴─────────┘

```

**Using Tuple**



```
-- You can also use Tuple

SELECT
    sum(1) AS impressions,
    (arrayJoin(arrayZip(cities, browsers)) AS t).1 AS city,
    t.2 AS browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Bobruisk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
GROUP BY
    2,
    3

```


```
┌─impressions─┬─city─────┬─browser─┐
│           1 │ Istanbul │ Firefox │
│           1 │ Berlin   │ Chrome  │
│           1 │ Bobruisk │ Chrome  │
└─────────────┴──────────┴─────────┘

```

## arrayLast[​](#arrayLast "Direct link to arrayLast")


Introduced in: v1\.1\.0


Returns the last element in the source array for which a lambda `func(x [, y1, y2, ... yN])` returns true, otherwise it returns a default value.


**Syntax**



```
arrayLast(func(x[, y1, ..., yN]), source[, cond1, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [Lambda function](/docs/sql-reference/functions/overview#arrow-operator-and-lambda). \- `source` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array). \- `[, cond1, ... , condN]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array).


**Returned value**


Returns the last element of the source array for which `func` is true, otherwise returns the default value of `T`.


**Examples**


**Usage example**



```
SELECT arrayLast(x, y -> x=y, ['a', 'b', 'c'], ['a', 'b', 'c'])

```


```
c

```

**No match**



```
SELECT arrayFirst(x, y -> x=y, [0, 1, 2], [3, 3, 3]) AS res, toTypeName(res)

```


```
0 UInt8

```

## arrayLastIndex[​](#arrayLastIndex "Direct link to arrayLastIndex")


Introduced in: v1\.1\.0


Returns the index of the last element in the source array for which `func(x[, y1, y2, ... yN])` returns true, otherwise it returns '0'.


**Syntax**



```
arrayLastIndex(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the index of the last element of the source array for which `func` is true, otherwise returns `0` [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT arrayLastIndex(x, y -> x=y, ['a', 'b', 'c'], ['a', 'b', 'c']);

```


```
3

```

**No match**



```
SELECT arrayLastIndex(x, y -> x=y, ['a', 'b', 'c'], ['d', 'e', 'f']);

```


```
0

```

## arrayLastOrNull[​](#arrayLastOrNull "Direct link to arrayLastOrNull")


Introduced in: v1\.1\.0


Returns the last element in the source array for which a lambda `func(x [, y1, y2, ... yN])` returns true, otherwise it returns `NULL`.


**Syntax**



```
arrayLastOrNull(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x [, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [Lambda function](/docs/sql-reference/functions/overview#arrow-operator-and-lambda). \- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array). \- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array).


**Returned value**


Returns the last element of the source array for which `λ` is not true, otherwise returns `NULL`.


**Examples**


**Usage example**



```
SELECT arrayLastOrNull(x, y -> x=y, ['a', 'b', 'c'], ['a', 'b', 'c'])

```


```
c

```

**No match**



```
SELECT arrayLastOrNull(x, y -> x=y, [0, 1, 2], [3, 3, 3]) AS res, toTypeName(res)

```


```
NULL Nullable(UInt8)

```

## arrayLevenshteinDistance[​](#arrayLevenshteinDistance "Direct link to arrayLevenshteinDistance")


Introduced in: v25\.4\.0


Calculates the Levenshtein distance for two arrays.


**Syntax**



```
arrayLevenshteinDistance(from, to)

```

**Arguments**


- `from` — The first array. [`Array(T)`](/docs/sql-reference/data-types/array). \- `to` — The second array. [`Array(T)`](/docs/sql-reference/data-types/array).


**Returned value**


Levenshtein distance between the first and the second arrays. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT arrayLevenshteinDistance([1, 2, 4], [1, 2, 3])

```


```
1

```

## arrayLevenshteinDistanceWeighted[​](#arrayLevenshteinDistanceWeighted "Direct link to arrayLevenshteinDistanceWeighted")


Introduced in: v25\.4\.0


Calculates Levenshtein distance for two arrays with custom weights for each element.
The number of elements for the array and its weights should match.


**Syntax**



```
arrayLevenshteinDistanceWeighted(from, to, from_weights, to_weights)

```

**Arguments**


- `from` — first array. [`Array(T)`](/docs/sql-reference/data-types/array). \- `to` — second array. [`Array(T)`](/docs/sql-reference/data-types/array). \- `from_weights` — weights for the first array. [`Array((U)Int*|Float*)`](/docs/sql-reference/data-types/array)
- `to_weights` — weights for the second array. [`Array((U)Int*|Float*)`](/docs/sql-reference/data-types/array)


**Returned value**


Levenshtein distance between the first and the second arrays with custom weights for each element [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT arrayLevenshteinDistanceWeighted(['A', 'B', 'C'], ['A', 'K', 'L'], [1.0, 2, 3], [3.0, 4, 5])

```


```
14

```

## arrayMap[​](#arrayMap "Direct link to arrayMap")


Introduced in: v1\.1\.0


Returns an array obtained from the original arrays by applying a lambda function to each element.


**Syntax**



```
arrayMap(func, arr)

```

**Arguments**


- `func` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `arr` — N arrays to process. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array from the lambda results [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayMap(x -> (x + 2), [1, 2, 3]) as res;

```


```
[3, 4, 5]

```

**Creating a tuple of elements from different arrays**



```
SELECT arrayMap((x, y) -> (x, y), [1, 2, 3], [4, 5, 6]) AS res

```


```
[(1, 4),(2, 5),(3, 6)]

```

## arrayMax[​](#arrayMax "Direct link to arrayMax")


Introduced in: v21\.1\.0


Returns the maximum element in the source array.


If a lambda function `func` is specified, returns the maximum element of the lambda results.


**Syntax**



```
arrayMax([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — Optional. A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the maximum element in the source array, or the maximum element of the lambda results if provided.


**Examples**


**Basic example**



```
SELECT arrayMax([5, 3, 2, 7]);

```


```
7

```

**Usage with lambda function**



```
SELECT arrayMax(x, y -> x/y, [4, 8, 12, 16], [1, 2, 1, 2]);

```


```
12

```

## arrayMin[​](#arrayMin "Direct link to arrayMin")


Introduced in: v21\.1\.0


Returns the minimum element in the source array.


If a lambda function `func` is specified, returns the minimum element of the lambda results.


**Syntax**



```
arrayMin([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — Optional. A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `cond1_arr, ...` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the minimum element in the source array, or the minimum element of the lambda results if provided.


**Examples**


**Basic example**



```
SELECT arrayMin([5, 3, 2, 7]);

```


```
2

```

**Usage with lambda function**



```
SELECT arrayMin(x, y -> x/y, [4, 8, 12, 16], [1, 2, 1, 2]);

```


```
4

```

## arrayNormalizedGini[​](#arrayNormalizedGini "Direct link to arrayNormalizedGini")


Introduced in: v25\.1\.0


Calculates the normalized Gini coefficient.


**Syntax**



```
arrayNormalizedGini(predicted, label)

```

**Arguments**


- `predicted` — The predicted value. [`Array(T)`](/docs/sql-reference/data-types/array)
- `label` — The actual value. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


A tuple containing the Gini coefficients of the predicted values, the Gini coefficient of the normalized values, and the normalized Gini coefficient (\= the ratio of the former two Gini coefficients) [`Tuple(Float64, Float64, Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT arrayNormalizedGini([0.9, 0.3, 0.8, 0.7],[6, 1, 0, 2]);

```


```
(0.18055555555555558, 0.2638888888888889, 0.6842105263157896)

```

## arrayPartialReverseSort[​](#arrayPartialReverseSort "Direct link to arrayPartialReverseSort")


Introduced in: v23\.2\.0


This function is the same as `arrayReverseSort` but with an additional `limit` argument allowing partial sorting.


TipTo retain only the sorted elements use `arrayResize`.


**Syntax**



```
arrayPartialReverseSort([f,] limit, arr [, arr1, ... ,arrN])

```

**Arguments**


- `f(arr[, arr1, ... ,arrN])` — The lambda function to apply to elements of array `x`. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `limit` — Index value up until which sorting will occur. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `arr` — Array to be sorted. [`Array(T)`](/docs/sql-reference/data-types/array)
- `arr1, ... ,arrN` — N additional arrays, in the case when `f` accepts multiple arguments. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of the same size as the original array where elements in the range `[1..limit]` are sorted
in descending order. The remaining elements `(limit..N]` are in an unspecified order.


**Examples**


**simple\_int**



```
SELECT arrayPartialReverseSort(2, [5, 9, 1, 3])

```


```
[9, 5, 1, 3]

```

**simple\_string**



```
SELECT arrayPartialReverseSort(2, ['expenses','lasso','embolism','gladly'])

```


```
['lasso','gladly','expenses','embolism']

```

**retain\_sorted**



```
SELECT arrayResize(arrayPartialReverseSort(2, [5, 9, 1, 3]), 2)

```


```
[9, 5]

```

**lambda\_simple**



```
SELECT arrayPartialReverseSort((x) -> -x, 2, [5, 9, 1, 3])

```


```
[1, 3, 5, 9]

```

**lambda\_complex**



```
SELECT arrayPartialReverseSort((x, y) -> -y, 1, [0, 1, 2], [1, 2, 3]) as res

```


```
[0, 1, 2]

```

## arrayPartialShuffle[​](#arrayPartialShuffle "Direct link to arrayPartialShuffle")


Introduced in: v23\.2\.0


Returns an array of the same size as the original array where elements in range `[1..limit]` are a random
subset of the original array. Remaining `(limit..n]` shall contain the elements not in `[1..limit]` range in undefined order.
Value of limit shall be in range `[1..n]`. Values outside of that range are equivalent to performing full `arrayShuffle`:


NoteThis function will not materialize constants.The value of `limit` should be in the range `[1..N]`. Values outside of that range are equivalent to performing full [`arrayShuffle`](#arrayShuffle).




**Syntax**



```
arrayPartialShuffle(arr [, limit[, seed]])

```

**Arguments**


- `arr` — The array to shuffle. [`Array(T)`](/docs/sql-reference/data-types/array)
- `seed` — Optional. The seed to be used with random number generation. If not provided, a random one is used. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `limit` — Optional. The number to limit element swaps to, in the range `[1..N]`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Array with elements partially shuffled. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**no\_limit1**



```
SELECT arrayPartialShuffle([1, 2, 3, 4], 0)

```


```
[2, 4, 3, 1]

```

**no\_limit2**



```
SELECT arrayPartialShuffle([1, 2, 3, 4])

```


```
[4, 1, 3, 2]

```

**random\_seed**



```
SELECT arrayPartialShuffle([1, 2, 3, 4], 2)

```


```
[3, 4, 1, 2]

```

**explicit\_seed**



```
SELECT arrayPartialShuffle([1, 2, 3, 4], 2, 41)

```


```
[3, 2, 1, 4]

```

**materialize**



```
SELECT arrayPartialShuffle(materialize([1, 2, 3, 4]), 2, 42), arrayPartialShuffle([1, 2, 3], 2, 42) FROM numbers(10)

```


```
┌─arrayPartial⋯4]), 2, 42)─┬─arrayPartial⋯ 3], 2, 42)─┐
│ [3,2,1,4]                │ [3,2,1]                  │
│ [3,2,1,4]                │ [3,2,1]                  │
│ [4,3,2,1]                │ [3,2,1]                  │
│ [1,4,3,2]                │ [3,2,1]                  │
│ [3,4,1,2]                │ [3,2,1]                  │
│ [1,2,3,4]                │ [3,2,1]                  │
│ [1,4,3,2]                │ [3,2,1]                  │
│ [1,4,3,2]                │ [3,2,1]                  │
│ [3,1,2,4]                │ [3,2,1]                  │
│ [1,3,2,4]                │ [3,2,1]                  │
└──────────────────────────┴──────────────────────────┘

```

## arrayPartialSort[​](#arrayPartialSort "Direct link to arrayPartialSort")


Introduced in: v23\.2\.0


This function is the same as `arraySort` but with an additional `limit` argument allowing partial sorting.


TipTo retain only the sorted elements use `arrayResize`.


**Syntax**



```
arrayPartialSort([f,] limit, arr [, arr1, ... ,arrN])

```

**Arguments**


- `f(arr[, arr1, ... ,arrN])` — The lambda function to apply to elements of array `x`. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `limit` — Index value up until which sorting will occur. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `arr` — Array to be sorted. [`Array(T)`](/docs/sql-reference/data-types/array)
- `arr1, ... ,arrN` — N additional arrays, in the case when `f` accepts multiple arguments. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of the same size as the original array where elements in the range `[1..limit]` are sorted
in ascending order. The remaining elements `(limit..N]` are in an unspecified order.


**Examples**


**simple\_int**



```
SELECT arrayPartialSort(2, [5, 9, 1, 3])

```


```
[1, 3, 5, 9]

```

**simple\_string**



```
SELECT arrayPartialSort(2, ['expenses', 'lasso', 'embolism', 'gladly'])

```


```
['embolism', 'expenses', 'gladly', 'lasso']

```

**retain\_sorted**



```
SELECT arrayResize(arrayPartialSort(2, [5, 9, 1, 3]), 2)

```


```
[1, 3]

```

**lambda\_simple**



```
SELECT arrayPartialSort((x) -> -x, 2, [5, 9, 1, 3])

```


```
[9, 5, 1, 3]

```

**lambda\_complex**



```
SELECT arrayPartialSort((x, y) -> -y, 1, [0, 1, 2], [1, 2, 3]) as res

```


```
[2, 1, 0]

```

## arrayPopBack[​](#arrayPopBack "Direct link to arrayPopBack")


Introduced in: v1\.1\.0


Removes the last element from the array.


**Syntax**



```
arrayPopBack(arr)

```

**Arguments**


- `arr` — The array for which to remove the last element from. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array identical to `arr` but without the last element of `arr` [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayPopBack([1, 2, 3]) AS res;

```


```
[1, 2]

```

## arrayPopFront[​](#arrayPopFront "Direct link to arrayPopFront")


Introduced in: v1\.1\.0


Removes the first item from the array.


**Syntax**



```
arrayPopFront(arr)

```

**Arguments**


- `arr` — The array for which to remove the first element from. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array identical to `arr` but without the first element of `arr` [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayPopFront([1, 2, 3]) AS res;

```


```
[2, 3]

```

## arrayProduct[​](#arrayProduct "Direct link to arrayProduct")


Introduced in: v21\.1\.0


Returns the product of elements in the source array.


If a lambda function `func` is specified, returns the product of elements of the lambda results.


**Syntax**



```
arrayProduct([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — Optional. A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the product of elements in the source array, or the product of elements of the lambda results if provided. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic example**



```
SELECT arrayProduct([1, 2, 3, 4]);

```


```
24

```

**Usage with lambda function**



```
SELECT arrayProduct(x, y -> x+y, [2, 2], [2, 2]) AS res;

```


```
16

```

## arrayPushBack[​](#arrayPushBack "Direct link to arrayPushBack")


Introduced in: v1\.1\.0


Adds one item to the end of the array.


**Syntax**



```
arrayPushBack(arr, x)

```

**Arguments**


- `arr` — The array for which to add value `x` to the end of. [`Array(T)`](/docs/sql-reference/data-types/array)
- `x` —
- Single value to add to the end of the array. [`Array(T)`](/docs/sql-reference/data-types/array).


Note- Only numbers can be added to an array with numbers, and only strings can be added to an array of strings.
- When adding numbers, ClickHouse automatically sets the type of `x` for the data type of the array.
- Can be `NULL`. The function adds a `NULL` element to an array, and the type of array elements converts to `Nullable`.

For more information about the types of data in ClickHouse, see [Data types](/docs/sql-reference/data-types).


**Returned value**


Returns an array identical to `arr` but with an additional value `x` at the end of the array [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayPushBack(['a'], 'b') AS res;

```


```
['a','b']

```

## arrayPushFront[​](#arrayPushFront "Direct link to arrayPushFront")


Introduced in: v1\.1\.0


Adds one element to the beginning of the array.


**Syntax**



```
arrayPushFront(arr, x)

```

**Arguments**


- `arr` — The array for which to add value `x` to the end of. [`Array(T)`](/docs/sql-reference/data-types/array). \- `x` —
- Single value to add to the start of the array. [`Array(T)`](/docs/sql-reference/data-types/array).


Note- Only numbers can be added to an array with numbers, and only strings can be added to an array of strings.
- When adding numbers, ClickHouse automatically sets the type of `x` for the data type of the array.
- Can be `NULL`. The function adds a `NULL` element to an array, and the type of array elements converts to `Nullable`.

For more information about the types of data in ClickHouse, see [Data types](/docs/sql-reference/data-types).


**Returned value**


Returns an array identical to `arr` but with an additional value `x` at the beginning of the array [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayPushFront(['b'], 'a') AS res;

```


```
['a','b']

```

## arrayROCAUC[​](#arrayROCAUC "Direct link to arrayROCAUC")


Introduced in: v20\.4\.0


Calculates the area under the receiver operating characteristic (ROC) curve.
A ROC curve is created by plotting True Positive Rate (TPR) on the y\-axis and False Positive Rate (FPR) on the x\-axis across all thresholds.
The resulting value ranges from zero to one, with a higher value indicating better model performance.


The ROC AUC (also known as simply AUC) is a concept in machine learning.
For more details, please see [here](https://developers.google.com/machine-learning/glossary#pr-auc-area-under-the-pr-curve), [here](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc#expandable-1) and [here](https://en.wikipedia.org/wiki/Receiver_operating_characteristic#Area_under_the_curve).


**Syntax**



```
arrayROCAUC(scores, labels[, scale[, partial_offsets]])

```

**Aliases**: `arrayAUC`


**Arguments**


- `scores` — Scores prediction model gives. [`Array((U)Int*)`](/docs/sql-reference/data-types/array) or [`Array(Float*)`](/docs/sql-reference/data-types/array)
- `labels` — Labels of samples, usually 1 for positive sample and 0 for negative sample. [`Array((U)Int*)`](/docs/sql-reference/data-types/array) or [`Enum`](/docs/sql-reference/data-types/enum)
- `scale` — Optional. Decides whether to return the normalized area. If false, returns the area under the TP (true positives) x FP (false positives) curve instead. Default value: true. [`Bool`](/docs/sql-reference/data-types/boolean)
- `partial_offsets` —
- An array of four non\-negative integers for calculating a partial area under the ROC curve (equivalent to a vertical band of the ROC space) instead of the whole AUC. This option is useful for distributed computation of the ROC AUC. The array must contain the following elements \[`higher_partitions_tp`, `higher_partitions_fp`, `total_positives`, `total_negatives`]. [Array](/docs/sql-reference/data-types/array) of non\-negative [Integers](/docs/sql-reference/data-types/int-uint). Optional.
	- `higher_partitions_tp`: The number of positive labels in the higher\-scored partitions.
	- `higher_partitions_fp`: The number of negative labels in the higher\-scored partitions.
	- `total_positives`: The total number of positive samples in the entire dataset.
	- `total_negatives`: The total number of negative samples in the entire dataset.


NoteWhen `arr_partial_offsets` is used, the `arr_scores` and `arr_labels` should be only a partition of the entire dataset, containing an interval of scores.
The dataset should be divided into contiguous partitions, where each partition contains the subset of the data whose scores fall within a specific range.
For example:- One partition could contain all scores in the range \[0, 0\.5\).
- Another partition could contain scores in the range \[0\.5, 1\.0].



**Returned value**


Returns area under the receiver operating characteristic (ROC) curve. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT arrayROCAUC([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1]);

```


```
0.75

```

## arrayRandomSample[​](#arrayRandomSample "Direct link to arrayRandomSample")


Introduced in: v23\.10\.0


Returns a subset with `samples`\-many random elements of an input array. If `samples` exceeds the size of the input array, the sample size is limited to the size of the array, i.e. all array elements are returned but their order is not guaranteed. The function can handle both flat arrays and nested arrays.


**Syntax**



```
arrayRandomSample(arr, samples)

```

**Arguments**


- `arr` — The input array or multidimensional array from which to sample elements. [`Array(T)`](/docs/sql-reference/data-types/array)
- `samples` — The number of elements to include in the random sample. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


An array containing a random sample of elements from the input array [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayRandomSample(['apple', 'banana', 'cherry', 'date'], 2) as res;

```


```
['cherry','apple']

```

**Using a multidimensional array**



```
SELECT arrayRandomSample([[1, 2], [3, 4], [5, 6]], 2) as res;

```


```
[[3,4],[5,6]]

```

## arrayReduce[​](#arrayReduce "Direct link to arrayReduce")


Introduced in: v1\.1\.0


Applies an aggregate function to array elements and returns its result.
The name of the aggregation function is passed as a string in single quotes `'max'`, `'sum'`.
When using parametric aggregate functions, the parameter is indicated after the function name in parentheses `'uniqUpTo(6)'`.


**Syntax**



```
arrayReduce(agg_f, arr1[, arr2, ... , arrN])

```

**Arguments**


- `agg_f` — The name of an aggregate function which should be a constant. [`String`](/docs/sql-reference/data-types/string)
- `arr1[, arr2, ... , arrN]` — N arrays corresponding to the arguments of `agg_f`. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the result of the aggregate function


**Examples**


**Usage example**



```
SELECT arrayReduce('max', [1, 2, 3]);

```


```
┌─arrayReduce('max', [1, 2, 3])─┐
│                             3 │
└───────────────────────────────┘

```

**Example with aggregate function using multiple arguments**



```
--If an aggregate function takes multiple arguments, then this function must be applied to multiple arrays of the same size.

SELECT arrayReduce('maxIf', [3, 5], [1, 0]);

```


```
┌─arrayReduce('maxIf', [3, 5], [1, 0])─┐
│                                    3 │
└──────────────────────────────────────┘

```

**Example with a parametric aggregate function**



```
SELECT arrayReduce('uniqUpTo(3)', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

```


```
┌─arrayReduce('uniqUpTo(3)', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])─┐
│                                                           4 │
└─────────────────────────────────────────────────────────────┘

```

## arrayReduceInRanges[​](#arrayReduceInRanges "Direct link to arrayReduceInRanges")


Introduced in: v20\.4\.0


Applies an aggregate function to array elements in the given ranges and returns an array containing the result corresponding to each range.
The function will return the same result as multiple `arrayReduce(agg_func, arraySlice(arr1, index, length), ...)`.


**Syntax**



```
arrayReduceInRanges(agg_f, ranges, arr1[, arr2, ... ,arrN])

```

**Arguments**


- `agg_f` — The name of the aggregate function to use. [`String`](/docs/sql-reference/data-types/string)
- `ranges` — The range over which to aggregate. An array of tuples, `(i, r)` containing the index `i` from which to begin from and the range `r` over which to aggregate. [`Array(T)`](/docs/sql-reference/data-types/array) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `arr1[, arr2, ... ,arrN]` — N arrays as arguments to the aggregate function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array containing results of the aggregate function over the specified ranges [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayReduceInRanges(
    'sum',
    [(1, 5), (2, 3), (3, 4), (4, 4)],
    [1000000, 200000, 30000, 4000, 500, 60, 7]
) AS res

```


```
┌─res─────────────────────────┐
│ [1234500,234000,34560,4567] │
└─────────────────────────────┘

```

## arrayRemove[​](#arrayRemove "Direct link to arrayRemove")


Introduced in: v25\.11\.0


Removes all elements equal to a given value from an array.
NULLs are treated as equal.


**Syntax**



```
arrayRemove(arr, elem)

```

**Aliases**: `array_remove`


**Arguments**


- `arr` — Array(T) \- `elem` — T


**Returned value**


Returns a subset of the source array [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Example 1**



```
SELECT arrayRemove([1, 2, 2, 3], 2)

```


```
[1, 3]

```

**Example 2**



```
SELECT arrayRemove(['a', NULL, 'b', NULL], NULL)

```


```
['a', 'b']

```

## arrayResize[​](#arrayResize "Direct link to arrayResize")


Introduced in: v1\.1\.0


Changes the length of the array.


**Syntax**



```
arrayResize(arr, size[, extender])

```

**Arguments**


- `arr` — Array to resize. [`Array(T)`](/docs/sql-reference/data-types/array)
- `size` —
\-The new length of the array.
If `size` is less than the original size of the array, the array is truncated from the right.
If `size` is larger than the initial size of the array, the array is extended to the right with `extender` values or default values for the data type of the array items.
- `extender` — Value to use for extending the array. Can be `NULL`.


**Returned value**


An array of length `size`. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Example 1**



```
SELECT arrayResize([1], 3);

```


```
[1,0,0]

```

**Example 2**



```
SELECT arrayResize([1], 3, NULL);

```


```
[1,NULL,NULL]

```

## arrayReverse[​](#arrayReverse "Direct link to arrayReverse")


Introduced in: v1\.1\.0


Reverses the order of elements of a given array.


NoteFunction `reverse(arr)` performs the same functionality but works on other data\-types
in addition to Arrays.


**Syntax**



```
arrayReverse(arr)

```

**Arguments**


- `arr` — The array to reverse. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of the same size as the original array containing the elements in reverse order [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayReverse([1, 2, 3])

```


```
[3,2,1]

```

## arrayReverseFill[​](#arrayReverseFill "Direct link to arrayReverseFill")


Introduced in: v20\.1\.0


The `arrayReverseFill` function sequentially processes a source array from the last
element to the first, evaluating a lambda condition at each position using elements
from the source and condition arrays. When the condition evaluates to false at
position i, the function replaces that element with the element at position i\+1
from the current state of the array. The last element is always preserved
regardless of any condition.


**Syntax**



```
arrayReverseFill(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array with elements of the source array replaced by the results of the lambda. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Example with a single array**



```
SELECT arrayReverseFill(x -> not isNull(x), [1, null, 2, null]) AS res

```


```
[1, 2, 2, NULL]

```

**Example with two arrays**



```
SELECT arrayReverseFill(x, y, z -> x > y AND x < z, [5, 3, 6, 2], [4, 7, 1, 3], [10, 2, 8, 5]) AS res;

```


```
[5, 6, 6, 2]

```

## arrayReverseSort[​](#arrayReverseSort "Direct link to arrayReverseSort")


Introduced in: v1\.1\.0


Sorts the elements of an array in descending order.
If a function `f` is specified, the provided array is sorted according to the result
of the function applied to the elements of the array, and then the sorted array is reversed.
If `f` accepts multiple arguments, the `arrayReverseSort` function is passed several arrays that
the arguments of `func` will correspond to.


If the array to sort contains `-Inf`, `NULL`, `NaN`, or `Inf` they will be sorted in the following order:


1. `-Inf`
2. `Inf`
3. `NaN`
4. `NULL`


`arrayReverseSort` is a [higher\-order function](/docs/sql-reference/functions/overview#higher-order-functions).


**Syntax**



```
arrayReverseSort([f,] arr [, arr1, ... ,arrN])

```

**Arguments**


- `f(y1[, y2 ... yN])` — The lambda function to apply to elements of array `x`. \- `arr` — An array to be sorted. [`Array(T)`](/docs/sql-reference/data-types/array) \- `arr1, ..., arrN` — Optional. N additional arrays, in the case when `f` accepts multiple arguments.


**Returned value**


Returns the array `x` sorted in descending order if no lambda function is provided, otherwise
it returns an array sorted according to the logic of the provided lambda function, and then reversed. [`Array(T)`](/docs/sql-reference/data-types/array).


**Examples**


**Example 1**



```
SELECT arrayReverseSort((x, y) -> y, [4, 3, 5], ['a', 'b', 'c']) AS res;

```


```
[5,3,4]

```

**Example 2**



```
SELECT arrayReverseSort((x, y) -> -y, [4, 3, 5], [1, 2, 3]) AS res;

```


```
[4,3,5]

```

## arrayReverseSplit[​](#arrayReverseSplit "Direct link to arrayReverseSplit")


Introduced in: v20\.1\.0


Split a source array into multiple arrays. When `func(x[, y1, ..., yN])` returns something other than zero, the array will be split to the right of the element. The array will not be split after the last element.


**Syntax**



```
arrayReverseSplit(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of arrays. [`Array(Array(T))`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayReverseSplit((x, y) -> y, [1, 2, 3, 4, 5], [1, 0, 0, 1, 0]) AS res

```


```
[[1], [2, 3, 4], [5]]

```

## arrayRotateLeft[​](#arrayRotateLeft "Direct link to arrayRotateLeft")


Introduced in: v23\.8\.0


Rotates an array to the left by the specified number of elements. Negative values of `n` are treated as rotating to the right by the absolute value of the rotation.


**Syntax**



```
arrayRotateLeft(arr, n)

```

**Arguments**


- `arr` — The array for which to rotate the elements.[`Array(T)`](/docs/sql-reference/data-types/array). \- `n` — Number of elements to rotate. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint).


**Returned value**


An array rotated to the left by the specified number of elements [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayRotateLeft([1,2,3,4,5,6], 2) as res;

```


```
[3,4,5,6,1,2]

```

**Negative value of n**



```
SELECT arrayRotateLeft([1,2,3,4,5,6], -2) as res;

```


```
[5,6,1,2,3,4]

```

## arrayRotateRight[​](#arrayRotateRight "Direct link to arrayRotateRight")


Introduced in: v23\.8\.0


Rotates an array to the right by the specified number of elements. Negative values of `n` are treated as rotating to the left by the absolute value of the rotation.


**Syntax**



```
arrayRotateRight(arr, n)

```

**Arguments**


- `arr` — The array for which to rotate the elements.[`Array(T)`](/docs/sql-reference/data-types/array). \- `n` — Number of elements to rotate. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint).


**Returned value**


An array rotated to the right by the specified number of elements [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayRotateRight([1,2,3,4,5,6], 2) as res;

```


```
[5,6,1,2,3,4]

```

**Negative value of n**



```
SELECT arrayRotateRight([1,2,3,4,5,6], -2) as res;

```


```
[3,4,5,6,1,2]

```

## arrayShiftLeft[​](#arrayShiftLeft "Direct link to arrayShiftLeft")


Introduced in: v23\.8\.0


Shifts an array to the left by the specified number of elements.
New elements are filled with the provided argument or the default value of the array element type.
If the number of elements is negative, the array is shifted to the right.


**Syntax**



```
arrayShiftLeft(arr, n[, default])

```

**Arguments**


- `arr` — The array for which to shift the elements.[`Array(T)`](/docs/sql-reference/data-types/array). \- `n` — Number of elements to shift.[`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint). \- `default` — Optional. Default value for new elements.


**Returned value**


An array shifted to the left by the specified number of elements [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayShiftLeft([1,2,3,4,5,6], 2) as res;

```


```
[3,4,5,6,0,0]

```

**Negative value of n**



```
SELECT arrayShiftLeft([1,2,3,4,5,6], -2) as res;

```


```
[0,0,1,2,3,4]

```

**Using a default value**



```
SELECT arrayShiftLeft([1,2,3,4,5,6], 2, 42) as res;

```


```
[3,4,5,6,42,42]

```

## arrayShiftRight[​](#arrayShiftRight "Direct link to arrayShiftRight")


Introduced in: v23\.8\.0


Shifts an array to the right by the specified number of elements.
New elements are filled with the provided argument or the default value of the array element type.
If the number of elements is negative, the array is shifted to the left.


**Syntax**



```
arrayShiftRight(arr, n[, default])

```

**Arguments**


- `arr` — The array for which to shift the elements. [`Array(T)`](/docs/sql-reference/data-types/array)
- `n` — Number of elements to shift. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)
- `default` — Optional. Default value for new elements.


**Returned value**


An array shifted to the right by the specified number of elements [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayShiftRight([1, 2, 3, 4, 5, 6], 2) as res;

```


```
[0, 0, 1, 2, 3, 4]

```

**Negative value of n**



```
SELECT arrayShiftRight([1, 2, 3, 4, 5, 6], -2) as res;

```


```
[3, 4, 5, 6, 0, 0]

```

**Using a default value**



```
SELECT arrayShiftRight([1, 2, 3, 4, 5, 6], 2, 42) as res;

```


```
[42, 42, 1, 2, 3, 4]

```

## arrayShingles[​](#arrayShingles "Direct link to arrayShingles")


Introduced in: v24\.1\.0


Generates an array of shingles (similar to ngrams for strings), i.e. consecutive sub\-arrays with a specified length of the input array.


**Syntax**



```
arrayShingles(arr, l)

```

**Arguments**


- `arr` — Array for which to generate an array of shingles. [`Array(T)`](/docs/sql-reference/data-types/array)
- `l` — The length of each shingle. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


An array of generated shingles [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayShingles([1, 2, 3, 4], 3) as res;

```


```
[[1, 2, 3], [2, 3, 4]]

```

## arrayShuffle[​](#arrayShuffle "Direct link to arrayShuffle")


Introduced in: v23\.2\.0


Returns an array of the same size as the original array containing the elements in shuffled order.
Elements are reordered in such a way that each possible permutation of those elements has equal probability of appearance.


NoteThis function will not materialize constants.


**Syntax**



```
arrayShuffle(arr [, seed])

```

**Arguments**


- `arr` — The array to shuffle. [`Array(T)`](/docs/sql-reference/data-types/array)
- `seed (optional)` — Optional. The seed to be used with random number generation. If not provided a random one is used. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Array with elements shuffled [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Example without seed (unstable results)**



```
SELECT arrayShuffle([1, 2, 3, 4]);

```


```
[1,4,2,3]

```

**Example without seed (stable results)**



```
SELECT arrayShuffle([1, 2, 3, 4], 41);

```


```
[3,2,1,4]

```

## arraySimilarity[​](#arraySimilarity "Direct link to arraySimilarity")


Introduced in: v25\.4\.0


Calculates the similarity of two arrays from `0` to `1` based on weighted Levenshtein distance.


**Syntax**



```
arraySimilarity(from, to, from_weights, to_weights)

```

**Arguments**


- `from` — first array [`Array(T)`](/docs/sql-reference/data-types/array)
- `to` — second array [`Array(T)`](/docs/sql-reference/data-types/array)
- `from_weights` — weights for the first array. [`Array((U)Int*|Float*)`](/docs/sql-reference/data-types/array)
- `to_weights` — weights for the second array. [`Array((U)Int*|Float*)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the similarity between `0` and `1` of the two arrays based on the weighted Levenshtein distance [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT arraySimilarity(['A', 'B', 'C'], ['A', 'K', 'L'], [1.0, 2, 3], [3.0, 4, 5]);

```


```
0.2222222222222222

```

## arraySlice[​](#arraySlice "Direct link to arraySlice")


Introduced in: v1\.1\.0


Returns a slice of the array, with `NULL` elements included.


**Syntax**



```
arraySlice(arr, offset [, length])

```

**Arguments**


- `arr` — Array to slice. [`Array(T)`](/docs/sql-reference/data-types/array)
- `offset` — Indent from the edge of the array. A positive value indicates an offset on the left, and a negative value is an indent on the right. Numbering of the array items begins with `1`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `length` — The length of the required slice. If you specify a negative value, the function returns an open slice `[offset, array_length - length]`. If you omit the value, the function returns the slice `[offset, the_end_of_array]`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a slice of the array with `length` elements from the specified `offset` [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arraySlice([1, 2, NULL, 4, 5], 2, 3) AS res;

```


```
[2, NULL, 4]

```

## arraySort[​](#arraySort "Direct link to arraySort")


Introduced in: v1\.1\.0


Sorts the elements of the provided array in ascending order.
If a lambda function `f` is specified, sorting order is determined by the result of
the lambda applied to each element of the array.
If the lambda accepts multiple arguments, the `arraySort` function is passed several
arrays that the arguments of `f` will correspond to.


If the array to sort contains `-Inf`, `NULL`, `NaN`, or `Inf` they will be sorted in the following order:


1. `-Inf`
2. `Inf`
3. `NaN`
4. `NULL`


`arraySort` is a [higher\-order function](/docs/sql-reference/functions/overview#higher-order-functions).


**Syntax**



```
arraySort([f,] arr [, arr1, ... ,arrN])

```

**Arguments**


- `f(y1[, y2 ... yN])` — The lambda function to apply to elements of array `x`. \- `arr` — An array to be sorted. [`Array(T)`](/docs/sql-reference/data-types/array) \- `arr1, ..., arrN` — Optional. N additional arrays, in the case when `f` accepts multiple arguments.


**Returned value**


Returns the array `arr` sorted in ascending order if no lambda function is provided, otherwise
it returns an array sorted according to the logic of the provided lambda function. [`Array(T)`](/docs/sql-reference/data-types/array).


**Examples**


**Example 1**



```
SELECT arraySort([1, 3, 3, 0]);

```


```
[0,1,3,3]

```

**Example 2**



```
SELECT arraySort(['hello', 'world', '!']);

```


```
['!','hello','world']

```

**Example 3**



```
SELECT arraySort([1, nan, 2, NULL, 3, nan, -4, NULL, inf, -inf]);

```


```
[-inf,-4,1,2,3,inf,nan,nan,NULL,NULL]

```

## arraySplit[​](#arraySplit "Direct link to arraySplit")


Introduced in: v20\.1\.0


Split a source array into multiple arrays. When `func(x [, y1, ..., yN])` returns something other than zero, the array will be split to the left of the element. The array will not be split before the first element.


**Syntax**



```
arraySplit(func(x[, y1, ..., yN]), source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`).[Lambda function](/docs/sql-reference/functions/overview#arrow-operator-and-lambda). \- `source_arr` — The source array to split [`Array(T)`](/docs/sql-reference/data-types/array). \- `[, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array).


**Returned value**


Returns an array of arrays [`Array(Array(T))`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arraySplit((x, y) -> y, [1, 2, 3, 4, 5], [1, 0, 0, 1, 0]) AS res

```


```
[[1, 2, 3], [4, 5]]

```

## arraySum[​](#arraySum "Direct link to arraySum")


Introduced in: v21\.1\.0


Returns the sum of elements in the source array.


If a lambda function `func` is specified, returns the sum of elements of the lambda results.


**Syntax**



```
arraySum([func(x[, y1, ..., yN])], source_arr[, cond1_arr, ... , condN_arr])

```

**Arguments**


- `func(x[, y1, ..., yN])` — Optional. A lambda function which operates on elements of the source array (`x`) and condition arrays (`y`). [`Lambda function`](/docs/sql-reference/functions/overview#arrow-operator-and-lambda)
- `source_arr` — The source array to process. [`Array(T)`](/docs/sql-reference/data-types/array)
- `, cond1_arr, ... , condN_arr]` — Optional. N condition arrays providing additional arguments to the lambda function. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the sum of elements in the source array, or the sum of elements of the lambda results if provided.


**Examples**


**Basic example**



```
SELECT arraySum([1, 2, 3, 4]);

```


```
10

```

**Usage with lambda function**



```
SELECT arraySum(x, y -> x+y, [1, 1, 1, 1], [1, 1, 1, 1]);

```


```
8

```

## arraySymmetricDifference[​](#arraySymmetricDifference "Direct link to arraySymmetricDifference")


Introduced in: v25\.4\.0


Takes multiple arrays and returns an array with elements that are not present in all source arrays. The result contains only unique values.


NoteThe symmetric difference of *more than two sets* is [mathematically defined](https://en.wikipedia.org/wiki/Symmetric_difference#n-ary_symmetric_difference)
as the set of all input elements which occur in an odd number of input sets.
In contrast, function `arraySymmetricDifference` simply returns the set of input elements which do not occur in all input sets.


**Syntax**



```
arraySymmetricDifference(arr1, arr2, ... , arrN)

```

**Arguments**


- `arrN` — N arrays from which to make the new array. [`Array(T)`](/docs/sql-reference/data-types/array).


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


All arrays passed must have the same length.


TipIf you want to get a list of unique items in an array, you can use `arrayReduce('groupUniqArray', arr)`.


**Syntax**



```
arrayUniq(arr1[, arr2, ..., arrN])

```

**Arguments**


- `arr1` — Array for which to count the number of unique elements. [`Array(T)`](/docs/sql-reference/data-types/array)
- `[, arr2, ..., arrN]` — Optional. Additional arrays used to count the number of unique tuples of elements at corresponding positions in multiple arrays. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


For a single argument returns the number of unique
elements. For multiple arguments returns the number of unique tuples made from
elements at corresponding positions across the arrays.
[`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Single argument**



```
SELECT arrayUniq([1, 1, 2, 2])

```


```
2

```

**Multiple argument**



```
SELECT arrayUniq([1, 2, 3, 1], [4, 5, 6, 4])

```


```
3

```

## arrayWithConstant[​](#arrayWithConstant "Direct link to arrayWithConstant")


Introduced in: v20\.1\.0


Creates an array of length `length` filled with the constant `x`.


**Syntax**



```
arrayWithConstant(N, x)

```

**Arguments**


- `length` — Number of elements in the array. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `x` — The value of the `N` elements in the array, of any type.


**Returned value**


Returns an Array with `N` elements of value `x`. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayWithConstant(3, 1)

```


```
[1, 1, 1]

```

## arrayZip[​](#arrayZip "Direct link to arrayZip")


Introduced in: v20\.1\.0


Combines multiple arrays into a single array. The resulting array contains the corresponding elements of the source arrays grouped into tuples in the listed order of arguments.


**Syntax**



```
arrayZip(arr1, arr2, ... , arrN)

```

**Arguments**


- `arr1, arr2, ... , arrN` — N arrays to combine into a single array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array with elements from the source arrays grouped in tuples. Data types in the tuple are the same as types of the input arrays and in the same order as arrays are passed [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT arrayZip(['a', 'b', 'c'], [5, 2, 1]);

```


```
[('a', 5), ('b', 2), ('c', 1)]

```

## arrayZipUnaligned[​](#arrayZipUnaligned "Direct link to arrayZipUnaligned")


Introduced in: v20\.1\.0


Combines multiple arrays into a single array, allowing for unaligned arrays (arrays of differing lengths). The resulting array contains the corresponding elements of the source arrays grouped into tuples in the listed order of arguments.


**Syntax**



```
arrayZipUnaligned(arr1, arr2, ..., arrN)

```

**Arguments**


- `arr1, arr2, ..., arrN` — N arrays to combine into a single array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array with elements from the source arrays grouped in tuples. Data types in the tuple are the same as types of the input arrays and in the same order as arrays are passed. [`Array(T)`](/docs/sql-reference/data-types/array) or [`Tuple(T1, T2, ...)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT arrayZipUnaligned(['a'], [1, 2, 3]);

```


```
[('a', 1),(NULL, 2),(NULL, 3)]

```

## countEqual[​](#countEqual "Direct link to countEqual")


Introduced in: v1\.1\.0


Returns the number of elements in the array equal to `x`. Equivalent to `arrayCount(elem -> elem = x, arr)`.


`NULL` elements are handled as separate values.


**Syntax**



```
countEqual(arr, x)

```

**Arguments**


- `arr` — Array to search. [`Array(T)`](/docs/sql-reference/data-types/array)
- `x` — Value in the array to count. Any type.


**Returned value**


Returns the number of elements in the array equal to `x` [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT countEqual([1, 2, NULL, NULL], NULL)

```


```
2

```

## empty[​](#empty "Direct link to empty")


Introduced in: v1\.1\.0


Checks whether the input array is empty.


An array is considered empty if it does not contain any elements.


NoteCan be optimized by enabling the [`optimize_functions_to_subcolumns` setting](/docs/operations/settings/settings#optimize_functions_to_subcolumns). With `optimize_functions_to_subcolumns = 1` the function reads only [size0](/docs/sql-reference/data-types/array#array-size) subcolumn instead of reading and processing the whole array column. The query `SELECT empty(arr) FROM TABLE;` transforms to `SELECT arr.size0 = 0 FROM TABLE;`.


The function also works for Strings or UUIDs.


**Syntax**



```
empty(arr)

```

**Arguments**


- `arr` — Input array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1` for an empty array or `0` for a non\-empty array [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT empty([]);

```


```
1

```

## emptyArrayDate[​](#emptyArrayDate "Direct link to emptyArrayDate")


Introduced in: v1\.1\.0


Returns an empty Date array


**Syntax**



```
emptyArrayDate()

```

**Arguments**


- None.


**Returned value**


An empty Date array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayDate

```


```
[]

```

## emptyArrayDateTime[​](#emptyArrayDateTime "Direct link to emptyArrayDateTime")


Introduced in: v1\.1\.0


Returns an empty DateTime array


**Syntax**



```
emptyArrayDateTime()

```

**Arguments**


- None.


**Returned value**


An empty DateTime array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayDateTime

```


```
[]

```

## emptyArrayFloat32[​](#emptyArrayFloat32 "Direct link to emptyArrayFloat32")


Introduced in: v1\.1\.0


Returns an empty Float32 array


**Syntax**



```
emptyArrayFloat32()

```

**Arguments**


- None.


**Returned value**


An empty Float32 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayFloat32

```


```
[]

```

## emptyArrayFloat64[​](#emptyArrayFloat64 "Direct link to emptyArrayFloat64")


Introduced in: v1\.1\.0


Returns an empty Float64 array


**Syntax**



```
emptyArrayFloat64()

```

**Arguments**


- None.


**Returned value**


An empty Float64 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayFloat64

```


```
[]

```

## emptyArrayInt16[​](#emptyArrayInt16 "Direct link to emptyArrayInt16")


Introduced in: v1\.1\.0


Returns an empty Int16 array


**Syntax**



```
emptyArrayInt16()

```

**Arguments**


- None.


**Returned value**


An empty Int16 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayInt16

```


```
[]

```

## emptyArrayInt32[​](#emptyArrayInt32 "Direct link to emptyArrayInt32")


Introduced in: v1\.1\.0


Returns an empty Int32 array


**Syntax**



```
emptyArrayInt32()

```

**Arguments**


- None.


**Returned value**


An empty Int32 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayInt32

```


```
[]

```

## emptyArrayInt64[​](#emptyArrayInt64 "Direct link to emptyArrayInt64")


Introduced in: v1\.1\.0


Returns an empty Int64 array


**Syntax**



```
emptyArrayInt64()

```

**Arguments**


- None.


**Returned value**


An empty Int64 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayInt64

```


```
[]

```

## emptyArrayInt8[​](#emptyArrayInt8 "Direct link to emptyArrayInt8")


Introduced in: v1\.1\.0


Returns an empty Int8 array


**Syntax**



```
emptyArrayInt8()

```

**Arguments**


- None.


**Returned value**


An empty Int8 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayInt8

```


```
[]

```

## emptyArrayString[​](#emptyArrayString "Direct link to emptyArrayString")


Introduced in: v1\.1\.0


Returns an empty String array


**Syntax**



```
emptyArrayString()

```

**Arguments**


- None.


**Returned value**


An empty String array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayString

```


```
[]

```

## emptyArrayToSingle[​](#emptyArrayToSingle "Direct link to emptyArrayToSingle")


Introduced in: v1\.1\.0


Accepts an empty array and returns a one\-element array that is equal to the default value.


**Syntax**



```
emptyArrayToSingle(arr)

```

**Arguments**


- `arr` — An empty array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


An array with a single value of the Array's default type. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Basic example**



```
CREATE TABLE test (
  a Array(Int32),
  b Array(String),
  c Array(DateTime)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO test VALUES ([], [], []);

SELECT emptyArrayToSingle(a), emptyArrayToSingle(b), emptyArrayToSingle(c) FROM test;

```


```
┌─emptyArrayToSingle(a)─┬─emptyArrayToSingle(b)─┬─emptyArrayToSingle(c)───┐
│ [0]                   │ ['']                  │ ['1970-01-01 01:00:00'] │
└───────────────────────┴───────────────────────┴─────────────────────────┘

```

## emptyArrayUInt16[​](#emptyArrayUInt16 "Direct link to emptyArrayUInt16")


Introduced in: v1\.1\.0


Returns an empty UInt16 array


**Syntax**



```
emptyArrayUInt16()

```

**Arguments**


- None.


**Returned value**


An empty UInt16 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayUInt16

```


```
[]

```

## emptyArrayUInt32[​](#emptyArrayUInt32 "Direct link to emptyArrayUInt32")


Introduced in: v1\.1\.0


Returns an empty UInt32 array


**Syntax**



```
emptyArrayUInt32()

```

**Arguments**


- None.


**Returned value**


An empty UInt32 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayUInt32

```


```
[]

```

## emptyArrayUInt64[​](#emptyArrayUInt64 "Direct link to emptyArrayUInt64")


Introduced in: v1\.1\.0


Returns an empty UInt64 array


**Syntax**



```
emptyArrayUInt64()

```

**Arguments**


- None.


**Returned value**


An empty UInt64 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayUInt64

```


```
[]

```

## emptyArrayUInt8[​](#emptyArrayUInt8 "Direct link to emptyArrayUInt8")


Introduced in: v1\.1\.0


Returns an empty UInt8 array


**Syntax**



```
emptyArrayUInt8()

```

**Arguments**


- None.


**Returned value**


An empty UInt8 array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT emptyArrayUInt8

```


```
[]

```

## has[​](#has "Direct link to has")


Introduced in: v1\.1\.0


Returns whether the array contains the specified element, the map contains the specified key, or the JSON object contains the specified path.


For JSON, nested paths are supported using dot notation (e.g., 'a.b.c').


When the first argument is a constant array and the second argument is a column or expression, `has(constant_array, column)` behaves like `column IN (constant_array)` and can use primary key and data\-skipping indexes for optimization. For example, `has([1, 10, 100], id)` can leverage the primary key index if `id` is part of the `PRIMARY KEY`.


This optimization also applies when the column is wrapped in monotonic functions (e.g., `has([...], toDate(ts))`).


**Syntax**



```
has(haystack, needle)

```

**Arguments**


- `haystack` — The source array, map, or JSON. [`Array`](/docs/sql-reference/data-types/array) or [`Map`](/docs/sql-reference/data-types/map) or [`JSON`](/docs/sql-reference/data-types/newjson)
- `needle` — The value to search for (element in array, key in map, or path string in JSON).


**Returned value**


Returns `1` if the haystack contains the specified needle, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Array basic usage**



```
SELECT has([1, 2, 3], 2)

```


```
1

```

**Array not found**



```
SELECT has([1, 2, 3], 4)

```


```
0

```

**Map basic usage**



```
SELECT has(map('a', 1, 'b', 2), 'b')

```


```
1

```

**JSON path**



```
SELECT has('{"a": {"b": 1}}'::JSON, 'a.b')

```


```
1

```

## hasAll[​](#hasAll "Direct link to hasAll")


Introduced in: v1\.1\.0


Checks whether one array is a subset of another.


- An empty array is a subset of any array.
- `Null` is processed as a value.
- The order of values in both the arrays does not matter.


**Syntax**



```
hasAll(set, subset)

```

**Arguments**


- `set` — Array of any type with a set of elements. [`Array(T)`](/docs/sql-reference/data-types/array)
- `subset` — Array of any type that shares a common supertype with `set` containing elements that should be tested to be a subset of `set`. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


- `1`, if `set` contains all of the elements from `subset`.
- `0`, otherwise.


Raises a `NO_COMMON_TYPE` exception if the set and subset elements do not share a common supertype.


**Examples**


**Empty arrays**



```
SELECT hasAll([], [])

```


```
1

```

**Arrays containing NULL values**



```
SELECT hasAll([1, Null], [Null])

```


```
1

```

**Arrays containing values of a different type**



```
SELECT hasAll([1.0, 2, 3, 4], [1, 3])

```


```
1

```

**Arrays containing String values**



```
SELECT hasAll(['a', 'b'], ['a'])

```


```
1

```

**Arrays without a common type**



```
SELECT hasAll([1], ['a'])

```


```
Raises a NO_COMMON_TYPE exception

```

**Array of arrays**



```
SELECT hasAll([[1, 2], [3, 4]], [[1, 2], [3, 5]])

```


```
0

```

## hasAny[​](#hasAny "Direct link to hasAny")


Introduced in: v1\.1\.0


Checks whether two arrays have intersection by some elements.


- `Null` is processed as a value.
- The order of the values in both of the arrays does not matter.


**Syntax**



```
hasAny(arr_x, arr_y)

```

**Arguments**


- `arr_x` — Array of any type with a set of elements. [`Array(T)`](/docs/sql-reference/data-types/array)
- `arr_y` — Array of any type that shares a common supertype with array `arr_x`. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


- `1`, if `arr_x` and `arr_y` have one similar element at least.
- `0`, otherwise.


Raises a `NO_COMMON_TYPE` exception if any of the elements of the two arrays do not share a common supertype.


**Examples**


**One array is empty**



```
SELECT hasAny([1], [])

```


```
0

```

**Arrays containing NULL values**



```
SELECT hasAny([Null], [Null, 1])

```


```
1

```

**Arrays containing values of a different type**



```
SELECT hasAny([-128, 1., 512], [1])

```


```
1

```

**Arrays without a common type**



```
SELECT hasAny([[1, 2], [3, 4]], ['a', 'c'])

```


```
Raises a `NO_COMMON_TYPE` exception

```

**Array of arrays**



```
SELECT hasAll([[1, 2], [3, 4]], [[1, 2], [1, 2]])

```


```
1

```

## hasSubstr[​](#hasSubstr "Direct link to hasSubstr")


Introduced in: v20\.6\.0


Checks whether all the elements of array2 appear in a array1 in the same exact order.
Therefore, the function will return `1`, if and only if array1 \= prefix \+ array2 \+ suffix.


In other words, the functions will check whether all the elements of array2 are contained in array1 like the `hasAll` function.
In addition, it will check that the elements are observed in the same order in both array1 and array2\.


- The function will return `1` if array2 is empty.
- `Null` is processed as a value. In other words `hasSubstr([1, 2, NULL, 3, 4], [2,3])` will return `0`. However, `hasSubstr([1, 2, NULL, 3, 4], [2,NULL,3])` will return `1`
- The order of values in both the arrays does matter.


Raises a `NO_COMMON_TYPE` exception if any of the elements of the two arrays do not share a common supertype.


**Syntax**



```
hasSubstr(arr1, arr2)

```

**Arguments**


- `arr1` — Array of any type with a set of elements. [`Array(T)`](/docs/sql-reference/data-types/array)
- `arr2` — Array of any type with a set of elements. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1` if array `arr1` contains array `arr2`. Otherwise, returns `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Both arrays are empty**



```
SELECT hasSubstr([], [])

```


```
1

```

**Arrays containing NULL values**



```
SELECT hasSubstr([1, Null], [Null])

```


```
1

```

**Arrays containing values of a different type**



```
SELECT hasSubstr([1.0, 2, 3, 4], [1, 3])

```


```
0

```

**Arrays containing strings**



```
SELECT hasSubstr(['a', 'b'], ['a'])

```


```
1

```

**Arrays with valid ordering**



```
SELECT hasSubstr(['a', 'b' , 'c'], ['a', 'b'])

```


```
1

```

**Arrays with invalid ordering**



```
SELECT hasSubstr(['a', 'b' , 'c'], ['a', 'c'])

```


```
0

```

**Array of arrays**



```
SELECT hasSubstr([[1, 2], [3, 4], [5, 6]], [[1, 2], [3, 4]])

```


```
1

```

**Arrays without a common type**



```
SELECT hasSubstr([1, 2, NULL, 3, 4], ['a'])

```


```
Raises a `NO_COMMON_TYPE` exception

```

## indexOf[​](#indexOf "Direct link to indexOf")


Introduced in: v1\.1\.0


Returns the index of the first element with value 'x' (starting from 1\) if it is in the array.
If the array does not contain the searched\-for value, the function returns `0`.


Elements set to `NULL` are handled as normal values.


**Syntax**



```
indexOf(arr, x)

```

**Arguments**


- `arr` — An array to search in for `x`. [`Array(T)`](/docs/sql-reference/data-types/array)
- `x` — Value of the first matching element in `arr` for which to return an index. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the index (numbered from one) of the first `x` in `arr` if it exists. Otherwise, returns `0`. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic example**



```
SELECT indexOf([5, 4, 1, 3], 3)

```


```
4

```

**Array with nulls**



```
SELECT indexOf([1, 3, NULL, NULL], NULL)

```


```
3

```

## indexOfAssumeSorted[​](#indexOfAssumeSorted "Direct link to indexOfAssumeSorted")


Introduced in: v24\.12\.0


Returns the index of the first element with value 'x' (starting from `1`) if it is in the array.
If the array does not contain the searched\-for value, the function returns `0`.


NoteUnlike the `indexOf` function, this function assumes that the array is sorted in
ascending order. If the array is not sorted, results are undefined.


**Syntax**



```
indexOfAssumeSorted(arr, x)

```

**Arguments**


- `arr` — A sorted array to search. [`Array(T)`](/docs/sql-reference/data-types/array)
- `x` — Value of the first matching element in sorted `arr` for which to return an index. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the index (numbered from one) of the first `x` in `arr` if it exists. Otherwise, returns `0`. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic example**



```
SELECT indexOfAssumeSorted([1, 3, 3, 3, 4, 4, 5], 4)

```


```
5

```

## kql\_array\_sort\_asc[​](#kql_array_sort_asc "Direct link to kql_array_sort_asc")


Introduced in: v23\.10\.0


Sorts one or more arrays in ascending order. The first array is sorted, and subsequent arrays are reordered to match the first array's sorted order. Null values are placed at the end. This is a KQL (Kusto Query Language) compatibility function.


**Syntax**



```
kql_array_sort_asc(array1[, array2, ..., nulls_last])

```

**Arguments**


- `array1` — The array to sort. [`Array(T)`](/docs/sql-reference/data-types/array)
- `array2` — Optional. Additional arrays to reorder according to array1's sort order. [`Array(T)`](/docs/sql-reference/data-types/array)
- `nulls_last` — Optional. A boolean indicating whether nulls should appear last. Default is true. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple of arrays sorted in ascending order. [`Tuple(Array, ...)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT kql_array_sort_asc([3, 1, 2])

```


```
([1, 2, 3])

```

## kql\_array\_sort\_desc[​](#kql_array_sort_desc "Direct link to kql_array_sort_desc")


Introduced in: v23\.10\.0


Sorts one or more arrays in descending order. The first array is sorted, and subsequent arrays are reordered to match the first array's sorted order. Null values are placed at the end. This is a KQL (Kusto Query Language) compatibility function.


**Syntax**



```
kql_array_sort_desc(array1[, array2, ..., nulls_last])

```

**Arguments**


- `array1` — The array to sort. [`Array(T)`](/docs/sql-reference/data-types/array)
- `array2` — Optional additional arrays to reorder according to array1's sort order. [`Array(T)`](/docs/sql-reference/data-types/array)
- `nulls_last` — Optional boolean indicating whether nulls should appear last. Default is true. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a tuple of arrays sorted in descending order. [`Tuple(Array, ...)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT kql_array_sort_desc([3, 1, 2])

```


```
([3, 2, 1])

```

## length[​](#length "Direct link to length")


Introduced in: v1\.1\.0


Calculates the length of a string or array.


- For String or FixedString arguments: calculates the number of bytes in the string.
- For Array arguments: calculates the number of elements in the array.
- If applied to a FixedString argument, the function is a constant expression.


Please note that the number of bytes in a string is not the same as the number of
Unicode "code points" and it is not the same as the number of Unicode "grapheme clusters"
(what we usually call "characters") and it is not the same as the visible string width.


It is ok to have ASCII NULL bytes in strings, and they will be counted as well.


**Syntax**



```
length(x)

```

**Aliases**: `CARDINALITY`, `OCTET_LENGTH`


**Arguments**


- `x` — Value for which to calculate the number of bytes (for String/FixedString) or elements (for Array). [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the number of number of bytes in the String/FixedString `x` / the number of elements in array `x` [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**String example**



```
SELECT length('Hello, world!')

```


```
13

```

**Array example**



```
SELECT length(['Hello', 'world'])

```


```
2

```

**constexpr example**



```
WITH 'hello' || toString(number) AS str
SELECT str,
isConstant(length(str)) AS str_length_is_constant,
isConstant(length(str::FixedString(6))) AS fixed_str_length_is_constant
FROM numbers(3)

```


```
┌─str────┬─str_length_is_constant─┬─fixed_str_length_is_constant─┐
│ hello0 │                      0 │                            1 │
│ hello1 │                      0 │                            1 │
│ hello2 │                      0 │                            1 │
└────────┴────────────────────────┴──────────────────────────────┘

```

**unicode example**



```
SELECT 'ёлка' AS str1, length(str1), lengthUTF8(str1), normalizeUTF8NFKD(str1) AS str2, length(str2), lengthUTF8(str2)

```


```
┌─str1─┬─length(str1)─┬─lengthUTF8(str1)─┬─str2─┬─length(str2)─┬─lengthUTF8(str2)─┐
│ ёлка │            8 │                4 │ ёлка │           10 │                5 │
└──────┴──────────────┴──────────────────┴──────┴──────────────┴──────────────────┘

```

**ascii\_vs\_utf8 example**



```
SELECT 'ábc' AS str, length(str), lengthUTF8(str)

```


```
┌─str─┬─length(str)──┬─lengthUTF8(str)─┐
│ ábc │            4 │               3 │
└─────┴──────────────┴─────────────────┘

```

## notEmpty[​](#notEmpty "Direct link to notEmpty")


Introduced in: v1\.1\.0


Checks whether the input array is non\-empty.


An array is considered non\-empty if it contains at least one element.


NoteCan be optimized by enabling the [`optimize_functions_to_subcolumns`](/docs/operations/settings/settings#optimize_functions_to_subcolumns) setting. With `optimize_functions_to_subcolumns = 1` the function reads only [size0](/docs/sql-reference/data-types/array#array-size) subcolumn instead of reading and processing the whole array column. The query `SELECT notEmpty(arr) FROM table` transforms to `SELECT arr.size0 != 0 FROM TABLE`.


The function also works for Strings or UUIDs.


**Syntax**



```
notEmpty(arr)

```

**Arguments**


- `arr` — Input array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1` for a non\-empty array or `0` for an empty array [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT notEmpty([1,2]);

```


```
1

```

## range[​](#range "Direct link to range")


Introduced in: v1\.1\.0


Returns an array of numbers from `start` to `end - 1` by `step`.


The supported types are:


- `UInt8/16/32/64`
- `Int8/16/32/64]`
- All arguments `start`, `end`, `step` must be one of the above supported types. Elements of the returned array will be a super type of the arguments.
- An exception is thrown if the function returns an array with a total length more than the number of elements specified by setting [`function_range_max_elements_in_block`](/docs/operations/settings/settings#function_range_max_elements_in_block).
- Returns `NULL` if any argument has Nullable(nothing) type. An exception is thrown if any argument has `NULL` value (Nullable(T) type).


**Syntax**



```
range([start, ] end [, step])

```

**Arguments**


- `start` — Optional. The first element of the array. Required if `step` is used. Default value: `0`. \- `end` — Required. The number before which the array is constructed. \- `step` — Optional. Determines the incremental step between each element in the array. Default value: `1`.


**Returned value**


Array of numbers from `start` to `end - 1` by `step`. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT range(5), range(1, 5), range(1, 5, 2), range(-1, 5, 2);

```


```
┌─range(5)────┬─range(1, 5)─┬─range(1, 5, 2)─┬─range(-1, 5, 2)─┐
│ [0,1,2,3,4] │ [1,2,3,4]   │ [1,3]          │ [-1,1,3]        │
└─────────────┴─────────────┴────────────────┴─────────────────┘

```

## replicate[​](#replicate "Direct link to replicate")


Introduced in: v1\.1\.0


Creates an array with a single value.


**Syntax**



```
replicate(x, arr)

```

**Arguments**


- `x` — The value to fill the result array with. [`Any`](/docs/sql-reference/data-types)
- `arr` — An array. [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns an array of the same length as `arr` filled with value `x`. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT replicate(1, ['a', 'b', 'c']);

```


```
┌─replicate(1, ['a', 'b', 'c'])───┐
│ [1, 1, 1]                       │
└─────────────────────────────────┘

```

## reverse[​](#reverse "Direct link to reverse")


Introduced in: v1\.1\.0


Reverses the order of the elements in the input array or the characters in the input string.


**Syntax**



```
reverse(arr | str)

```

**Arguments**


- `arr | str` — The source array or string. [`Array(T)`](/docs/sql-reference/data-types/array) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an array or string with the order of elements or characters reversed.


**Examples**


**Reverse array**



```
SELECT reverse([1, 2, 3, 4]);

```


```
[4, 3, 2, 1]

```

**Reverse string**



```
SELECT reverse('abcd');

```


```
'dcba'

```

## Distance functions[​](#distance-functions "Direct link to Distance functions")


All supported functions are described in [distance functions documentation](/docs/sql-reference/functions/distance-functions).

[PreviousArithmetic](/docs/sql-reference/functions/arithmetic-functions)[NextarrayJoin](/docs/sql-reference/functions/array-join)- [array](#array)- [arrayAUCPR](#arrayAUCPR)- [arrayAll](#arrayAll)- [arrayAutocorrelation](#arrayAutocorrelation)- [arrayAvg](#arrayAvg)- [arrayCompact](#arrayCompact)- [arrayConcat](#arrayConcat)- [arrayCount](#arrayCount)- [arrayCumSum](#arrayCumSum)- [arrayCumSumNonNegative](#arrayCumSumNonNegative)- [arrayDifference](#arrayDifference)- [arrayDistinct](#arrayDistinct)- [arrayDotProduct](#arrayDotProduct)- [arrayElement](#arrayElement)- [arrayElementOrNull](#arrayElementOrNull)- [arrayEnumerate](#arrayEnumerate)- [arrayEnumerateDense](#arrayEnumerateDense)- [arrayEnumerateDenseRanked](#arrayEnumerateDenseRanked)- [arrayEnumerateUniq](#arrayEnumerateUniq)- [arrayEnumerateUniqRanked](#arrayEnumerateUniqRanked)- [arrayExcept](#arrayExcept)- [arrayExists](#arrayExists)- [arrayFill](#arrayFill)- [arrayFilter](#arrayFilter)- [arrayFirst](#arrayFirst)- [arrayFirstIndex](#arrayFirstIndex)- [arrayFirstOrNull](#arrayFirstOrNull)- [arrayFlatten](#arrayFlatten)- [arrayFold](#arrayFold)- [arrayIntersect](#arrayIntersect)- [arrayJaccardIndex](#arrayJaccardIndex)- [arrayJoin](#arrayJoin)- [arrayLast](#arrayLast)- [arrayLastIndex](#arrayLastIndex)- [arrayLastOrNull](#arrayLastOrNull)- [arrayLevenshteinDistance](#arrayLevenshteinDistance)- [arrayLevenshteinDistanceWeighted](#arrayLevenshteinDistanceWeighted)- [arrayMap](#arrayMap)- [arrayMax](#arrayMax)- [arrayMin](#arrayMin)- [arrayNormalizedGini](#arrayNormalizedGini)- [arrayPartialReverseSort](#arrayPartialReverseSort)- [arrayPartialShuffle](#arrayPartialShuffle)- [arrayPartialSort](#arrayPartialSort)- [arrayPopBack](#arrayPopBack)- [arrayPopFront](#arrayPopFront)- [arrayProduct](#arrayProduct)- [arrayPushBack](#arrayPushBack)- [arrayPushFront](#arrayPushFront)- [arrayROCAUC](#arrayROCAUC)- [arrayRandomSample](#arrayRandomSample)- [arrayReduce](#arrayReduce)- [arrayReduceInRanges](#arrayReduceInRanges)- [arrayRemove](#arrayRemove)- [arrayResize](#arrayResize)- [arrayReverse](#arrayReverse)- [arrayReverseFill](#arrayReverseFill)- [arrayReverseSort](#arrayReverseSort)- [arrayReverseSplit](#arrayReverseSplit)- [arrayRotateLeft](#arrayRotateLeft)- [arrayRotateRight](#arrayRotateRight)- [arrayShiftLeft](#arrayShiftLeft)- [arrayShiftRight](#arrayShiftRight)- [arrayShingles](#arrayShingles)- [arrayShuffle](#arrayShuffle)- [arraySimilarity](#arraySimilarity)- [arraySlice](#arraySlice)- [arraySort](#arraySort)- [arraySplit](#arraySplit)- [arraySum](#arraySum)- [arraySymmetricDifference](#arraySymmetricDifference)- [arrayTranspose](#arrayTranspose)- [arrayUnion](#arrayUnion)- [arrayUniq](#arrayUniq)- [arrayWithConstant](#arrayWithConstant)- [arrayZip](#arrayZip)- [arrayZipUnaligned](#arrayZipUnaligned)- [countEqual](#countEqual)- [empty](#empty)- [emptyArrayDate](#emptyArrayDate)- [emptyArrayDateTime](#emptyArrayDateTime)- [emptyArrayFloat32](#emptyArrayFloat32)- [emptyArrayFloat64](#emptyArrayFloat64)- [emptyArrayInt16](#emptyArrayInt16)- [emptyArrayInt32](#emptyArrayInt32)- [emptyArrayInt64](#emptyArrayInt64)- [emptyArrayInt8](#emptyArrayInt8)- [emptyArrayString](#emptyArrayString)- [emptyArrayToSingle](#emptyArrayToSingle)- [emptyArrayUInt16](#emptyArrayUInt16)- [emptyArrayUInt32](#emptyArrayUInt32)- [emptyArrayUInt64](#emptyArrayUInt64)- [emptyArrayUInt8](#emptyArrayUInt8)- [has](#has)- [hasAll](#hasAll)- [hasAny](#hasAny)- [hasSubstr](#hasSubstr)- [indexOf](#indexOf)- [indexOfAssumeSorted](#indexOfAssumeSorted)- [kql\_array\_sort\_asc](#kql_array_sort_asc)- [kql\_array\_sort\_desc](#kql_array_sort_desc)- [length](#length)- [notEmpty](#notEmpty)- [range](#range)- [replicate](#replicate)- [reverse](#reverse)- [Distance functions](#distance-functions)
Was this page helpful?
