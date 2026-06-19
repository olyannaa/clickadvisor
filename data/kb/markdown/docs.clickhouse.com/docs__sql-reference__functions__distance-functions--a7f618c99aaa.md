# Distance functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Distance
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/distance-functions.md)# Distance functions

## L1Distance[​](#L1Distance "Direct link to L1Distance")


Introduced in: v21\.11\.0


Calculates the distance between two points (the elements of the vectors are the coordinates) in `L1` space (1\-norm ([taxicab geometry](https://en.wikipedia.org/wiki/Taxicab_geometry) distance)).


**Syntax**



```
L1Distance(vector1, vector2)

```

**Aliases**: `distanceL1`


**Arguments**


- `vector1` — First vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)
- `vector2` — Second vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the 1\-norm distance. For `Array` inputs, returns `Float32` if the least common supertype of the element types is `Float32` or `BFloat16`, otherwise `Float64`. For `Tuple` inputs, the return type follows the arithmetic result type of the element\-wise operations (integer types are preserved). [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT L1Distance((1, 2), (2, 3))

```


```
┌─L1Distance((1, 2), (2, 3))─┐
│                          2 │
└────────────────────────────┘

```

## L1Norm[​](#L1Norm "Direct link to L1Norm")


Introduced in: v21\.11\.0


Calculates the sum of absolute elements of a vector.


**Syntax**



```
L1Norm(vector)

```

**Aliases**: `normL1`


**Arguments**


- `vector` — Vector or tuple of numeric values. [`Array(T)`](/docs/sql-reference/data-types/array) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the L1\-norm or [taxicab geometry](https://en.wikipedia.org/wiki/Taxicab_geometry) distance. [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Examples**


**Basic usage**



```
SELECT L1Norm((1, 2))

```


```
┌─L1Norm((1, 2))─┐
│              3 │
└────────────────┘

```

## L1Normalize[​](#L1Normalize "Direct link to L1Normalize")


Introduced in: v21\.11\.0


Calculates the unit vector of a given vector (the elements of the tuple are the coordinates) in `L1` space ([taxicab geometry](https://en.wikipedia.org/wiki/Taxicab_geometry)).


**Syntax**



```
L1Normalize(tuple)

```

**Aliases**: `normalizeL1`


**Arguments**


- `tuple` — A tuple of numeric values. [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the unit vector. [`Tuple(Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT L1Normalize((1, 2))

```


```
┌─L1Normalize((1, 2))─────────────────────┐
│ (0.3333333333333333,0.6666666666666666) │
└─────────────────────────────────────────┘

```

## L2Distance[​](#L2Distance "Direct link to L2Distance")


Introduced in: v21\.11\.0


Calculates the distance between two points (the elements of the vectors are the coordinates) in Euclidean space ([Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance)).


**Syntax**



```
L2Distance(vector1, vector2)

```

**Aliases**: `distanceL2`


**Arguments**


- `vector1` — First vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)
- `vector2` — Second vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the 2\-norm distance. For `Array` inputs, returns `Float32` if the least common supertype of the element types is `Float32` or `BFloat16`, otherwise `Float64`. For `Tuple` inputs, always returns `Float64`. [`Float*`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT L2Distance((1, 2), (2, 3))

```


```
┌─L2Distance((1, 2), (2, 3))─┐
│         1.4142135623730951 │
└────────────────────────────┘

```

## L2DistanceTransposed[​](#L2DistanceTransposed "Direct link to L2DistanceTransposed")


Introduced in: v25\.10\.0


Calculates the approximate distance between two points (the values of the vectors are the coordinates) in Euclidean space ([Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance)).


**Syntax**



```
L2DistanceTransposed(vector1, vector2, p)

```

**Aliases**: `distanceL2Transposed`


**Arguments**


- `vectors` — Vectors. [`QBit(T, UInt64)`](/docs/sql-reference/data-types/qbit)
- `reference` — Reference vector. [`Array(T)`](/docs/sql-reference/data-types/array)
- `p` — Number of bits from each vector element to use in the distance calculation (1 to element bit\-width). The quantization level controls the precision\-speed trade\-off. Using fewer bits results in faster I/O and calculations with reduced accuracy, while using more bits increases accuracy at the cost of performance. [`UInt`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the approximate 2\-norm distance. Always returns `Float64`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
CREATE TABLE qbit (id UInt32, vec QBit(Float64, 2)) ENGINE = Memory;
INSERT INTO qbit VALUES (1, [0, 1]);
SELECT L2DistanceTransposed(vec, array(1, 2), 16) FROM qbit;

```


```
┌─L2DistanceTransposed([0, 1], [1, 2], 16)─┐
│                       1.4142135623730951 │
└──────────────────────────────────────────┘

```

## L2Norm[​](#L2Norm "Direct link to L2Norm")


Introduced in: v21\.11\.0


Calculates the square root of the sum of the squares of the vector elements.


**Syntax**



```
L2Norm(vector)

```

**Aliases**: `normL2`


**Arguments**


- `vector` — Vector or tuple of numeric values. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the L2\-norm or [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance). [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT L2Norm((1, 2))

```


```
┌───L2Norm((1, 2))─┐
│ 2.23606797749979 │
└──────────────────┘

```

## L2Normalize[​](#L2Normalize "Direct link to L2Normalize")


Introduced in: v21\.11\.0


Calculates the unit vector of a given vector (the elements of the tuple are the coordinates) in Euclidean space (using [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance)).


**Syntax**



```
L2Normalize(tuple)

```

**Aliases**: `normalizeL2`


**Arguments**


- `tuple` — A tuple of numeric values. [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the unit vector. [`Tuple(Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT L2Normalize((3, 4))

```


```
┌─L2Normalize((3, 4))─┐
│ (0.6,0.8)           │
└─────────────────────┘

```

## L2SquaredDistance[​](#L2SquaredDistance "Direct link to L2SquaredDistance")


Introduced in: v22\.7\.0


Calculates the sum of the squares of the difference between the corresponding elements of two vectors.


**Syntax**



```
L2SquaredDistance(vector1, vector2)

```

**Aliases**: `distanceL2Squared`


**Arguments**


- `vector1` — First vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)
- `vector2` — Second vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the sum of the squares of the differences between the corresponding elements of two vectors. For `Array` inputs, returns `Float32` if the least common supertype of the element types is `Float32` or `BFloat16`, otherwise `Float64`. For `Tuple` inputs, the return type follows the arithmetic result type of the element\-wise operations (integer types are preserved). [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT L2SquaredDistance([1, 2, 3], [0, 0, 0])

```


```
┌─L2SquaredDis⋯ [0, 0, 0])─┐
│                       14 │
└──────────────────────────┘

```

## L2SquaredNorm[​](#L2SquaredNorm "Direct link to L2SquaredNorm")


Introduced in: v22\.7\.0


Calculates the square root of the sum of the squares of the vector elements (the [`L2Norm`](#L2Norm)) squared.


**Syntax**



```
L2SquaredNorm(vector)

```

**Aliases**: `normL2Squared`


**Arguments**


- `vector` — Vector or tuple of numeric values. [`Array(T)`](/docs/sql-reference/data-types/array) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the L2\-norm squared. [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Examples**


**Basic usage**



```
SELECT L2SquaredNorm((1, 2))

```


```
┌─L2SquaredNorm((1, 2))─┐
│                     5 │
└───────────────────────┘

```

## LinfDistance[​](#LinfDistance "Direct link to LinfDistance")


Introduced in: v21\.11\.0


Calculates the distance between two points (the elements of the vectors are the coordinates) in `L_{inf}` space ([maximum norm](https://en.wikipedia.org/wiki/Norm_(mathematics)#Maximum_norm_(special_case_of:_infinity_norm,_uniform_norm,_or_supremum_norm))).


**Syntax**



```
LinfDistance(vector1, vector2)

```

**Aliases**: `distanceLinf`


**Arguments**


- `vector1` — First vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)
- `vector2` — Second vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the infinity\-norm distance. For `Array` inputs, returns `Float32` if the least common supertype of the element types is `Float32` or `BFloat16`, otherwise `Float64`. For `Tuple` inputs, always returns `Float64`. [`Float*`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT LinfDistance((1, 2), (2, 3))

```


```
┌─LinfDistance((1, 2), (2, 3))─┐
│                            1 │
└──────────────────────────────┘

```

## LinfNorm[​](#LinfNorm "Direct link to LinfNorm")


Introduced in: v21\.11\.0


Calculates the maximum of absolute elements of a vector.


**Syntax**



```
LinfNorm(vector)

```

**Aliases**: `normLinf`


**Arguments**


- `vector` — Vector or tuple of numeric values. [`Array(T)`](/docs/sql-reference/data-types/array) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the Linf\-norm or the maximum absolute value. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT LinfNorm((1, -2))

```


```
┌─LinfNorm((1, -2))─┐
│                 2 │
└───────────────────┘

```

## LinfNormalize[​](#LinfNormalize "Direct link to LinfNormalize")


Introduced in: v21\.11\.0


Calculates the unit vector of a given vector (the elements of the tuple are the coordinates) in `L_{inf}` space (using [maximum norm](https://en.wikipedia.org/wiki/Norm_(mathematics)#Maximum_norm_(special_case_of:_infinity_norm,_uniform_norm,_or_supremum_norm))).


**Syntax**



```
LinfNormalize(tuple)

```

**Aliases**: `normalizeLinf`


**Arguments**


- `tuple` — A tuple of numeric values. [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the unit vector. [`Tuple(Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT LinfNormalize((3, 4))

```


```
┌─LinfNormalize((3, 4))─┐
│ (0.75,1)              │
└───────────────────────┘

```

## LpDistance[​](#LpDistance "Direct link to LpDistance")


Introduced in: v21\.11\.0


Calculates the distance between two points (the elements of the vectors are the coordinates) in `Lp` space ([p\-norm distance](https://en.wikipedia.org/wiki/Norm_(mathematics)#p-norm)).


**Syntax**



```
LpDistance(vector1, vector2, p)

```

**Aliases**: `distanceLp`


**Arguments**


- `vector1` — First vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)
- `vector2` — Second vector. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)
- `p` — The power. Possible values: real number from `[1; inf)`. [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the p\-norm distance. For `Array` inputs, returns `Float32` if the least common supertype of the element types is `Float32` or `BFloat16`, otherwise `Float64`. For `Tuple` inputs, always returns `Float64`. [`Float*`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT LpDistance((1, 2), (2, 3), 3)

```


```
┌─LpDistance((1, 2), (2, 3), 3)─┐
│            1.2599210498948732 │
└───────────────────────────────┘

```

## LpNorm[​](#LpNorm "Direct link to LpNorm")


Introduced in: v21\.11\.0


Calculates the p\-norm of a vector, which is the p\-th root of the sum of the p\-th powers of the absolute elements of its elements.


Special cases:


- When p\=1, it's equivalent to L1Norm (Manhattan distance).
- When p\=2, it's equivalent to L2Norm (Euclidean distance).
- When p\=∞, it's equivalent to LinfNorm (maximum norm).


**Syntax**



```
LpNorm(vector, p)

```

**Aliases**: `normLp`


**Arguments**


- `vector` — Vector or tuple of numeric values. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)
- `p` — The power. Possible values are real numbers in the range `[1; inf)`. [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the [Lp\-norm](https://en.wikipedia.org/wiki/Norm_(mathematics)#p-norm). [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT LpNorm((1, -2), 2)

```


```
┌─LpNorm((1, -2), 2)─┐
│   2.23606797749979 │
└────────────────────┘

```

## LpNormalize[​](#LpNormalize "Direct link to LpNormalize")


Introduced in: v21\.11\.0


Calculates the unit vector of a given vector (the elements of the tuple are the coordinates) in `Lp` space (using [p\-norm](https://en.wikipedia.org/wiki/Norm_(mathematics)#p-norm)).


**Syntax**



```
LpNormalize(tuple, p)

```

**Aliases**: `normalizeLp`


**Arguments**


- `tuple` — A tuple of numeric values. [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `p` — The power. Possible values are any number in the range range from `[1; inf)`. [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the unit vector. [`Tuple(Float64)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT LpNormalize((3, 4), 5)

```


```
┌─LpNormalize((3, 4), 5)──────────────────┐
│ (0.7187302630182624,0.9583070173576831) │
└─────────────────────────────────────────┘

```

## cosineDistance[​](#cosineDistance "Direct link to cosineDistance")


Introduced in: v21\.11\.0


Calculates the [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_distance) between two vectors (the elements of the tuples are the coordinates). The smaller the returned value is, the more similar are the vectors.


**Syntax**



```
cosineDistance(vector1, vector2)

```

**Aliases**: `distanceCosine`


**Arguments**


- `vector1` — First tuple. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)
- `vector2` — Second tuple. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(T)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the cosine distance (one minus the cosine similarity). For `Array` inputs, returns `Float32` if the least common supertype of the element types is `Float32` or `BFloat16`, otherwise `Float64`. For `Tuple` inputs, always returns `Float64`. [`Float*`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT cosineDistance((1, 2), (2, 3));

```


```
┌─cosineDistance((1, 2), (2, 3))─┐
│           0.007722123286332261 │
└────────────────────────────────┘

```

## cosineDistanceTransposed[​](#cosineDistanceTransposed "Direct link to cosineDistanceTransposed")


Introduced in: v26\.1\.0


Calculates the approximate [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_distance) between two points (the values of the vectors are the coordinates). The smaller the returned value is, the more similar are the vectors.


**Syntax**



```
cosineDistanceTransposed(vector1, vector2, p)

```

**Aliases**: `distanceCosineTransposed`


**Arguments**


- `vectors` — Vectors. [`QBit(T, UInt64)`](/docs/sql-reference/data-types/qbit)
- `reference` — Reference vector. [`Array(T)`](/docs/sql-reference/data-types/array)
- `p` — Number of bits from each vector element to use in the distance calculation (1 to element bit\-width). The quantization level controls the precision\-speed trade\-off. Using fewer bits results in faster I/O and calculations with reduced accuracy, while using more bits increases accuracy at the cost of performance. [`UInt`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the approximate cosine distance (one minus the cosine similarity). Always returns Float64\. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
CREATE TABLE qbit (id UInt32, vec QBit(Float64, 2)) ENGINE = Memory;
INSERT INTO qbit VALUES (1, [0, 1]);
SELECT cosineDistanceTransposed(vec, array(1, 2), 16) FROM qbit;

```


```
┌─cosineDistanceTransposed([0, 1], [1, 2], 16)─┐
│                          0.10557281085638826 │
└──────────────────────────────────────────────┘

```
[PreviousDates and time](/docs/sql-reference/functions/date-time-functions)[NextEmbedded dictionary](/docs/sql-reference/functions/ym-dict-functions)- [L1Distance](#L1Distance)- [L1Norm](#L1Norm)- [L1Normalize](#L1Normalize)- [L2Distance](#L2Distance)- [L2DistanceTransposed](#L2DistanceTransposed)- [L2Norm](#L2Norm)- [L2Normalize](#L2Normalize)- [L2SquaredDistance](#L2SquaredDistance)- [L2SquaredNorm](#L2SquaredNorm)- [LinfDistance](#LinfDistance)- [LinfNorm](#LinfNorm)- [LinfNormalize](#LinfNormalize)- [LpDistance](#LpDistance)- [LpNorm](#LpNorm)- [LpNormalize](#LpNormalize)- [cosineDistance](#cosineDistance)- [cosineDistanceTransposed](#cosineDistanceTransposed)
Was this page helpful?
