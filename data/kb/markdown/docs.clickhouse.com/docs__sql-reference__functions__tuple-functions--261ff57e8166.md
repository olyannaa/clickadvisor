# Tuple functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Tuples
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/tuple-functions.md)# Tuple functions

NoteThe documentation below is generated from the `system.functions` system table.


## dotProduct[​](#dotProduct "Direct link to dotProduct")


Introduced in: v21\.11\.0


Calculates the [dot product](https://en.wikipedia.org/wiki/Dot_product) (scalar product) of two vectors (tuples or arrays of equal size).
Returns the sum of the products of the corresponding elements.


**Syntax**



```
dotProduct(vector1, vector2)

```

**Aliases**: `scalarProduct`


**Arguments**


- `vector1` — First vector. [`Array(T)`](/docs/sql-reference/data-types/array) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `vector2` — Second vector. Must be the same size as the first vector. [`Array(T)`](/docs/sql-reference/data-types/array) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the dot product of the two vectors. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Examples**


**Basic usage**



```
SELECT dotProduct((1, 2), (3, 4))

```


```
11

```

## flattenTuple[​](#flattenTuple "Direct link to flattenTuple")


Introduced in: v22\.6\.0


Flattens a named and nested tuple.
The elements of the returned tuple are the paths of the input tuple.


**Syntax**



```
flattenTuple(input)

```

**Arguments**


- `input` — Named and nested tuple to flatten. [`Tuple(n1 T1[, n2 T2, ... ])`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns an output tuple whose elements are paths from the original input. [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
CREATE TABLE tab(t Tuple(a UInt32, b Tuple(c String, d UInt32))) ENGINE = MergeTree ORDER BY tuple();
INSERT INTO tab VALUES ((3, ('c', 4)));

SELECT flattenTuple(t) FROM tab;

```


```
┌─flattenTuple(t)┐
│ (3, 'c', 4)    │
└────────────────┘

```

## tuple[​](#tuple "Direct link to tuple")


Introduced in: v1\.1\.0


Returns a tuple by grouping input arguments.


For columns C1, C2, ... with the types T1, T2, ..., it returns a named Tuple(C1 T1, C2 T2, ...) type tuple containing these columns if their names are unique and can be treated as unquoted identifiers, otherwise a Tuple(T1, T2, ...) is returned. There is no cost to execute the function.
Tuples are normally used as intermediate values for an argument of IN operators, or for creating a list of formal parameters of lambda functions. Tuples can't be written to a table.


The function implements the operator `(x, y, ...)`.


**Syntax**



```
tuple([t1[, t2[ ...]])

```

**Arguments**


- None.


**Returned value**


**Examples**


**typical**



```
SELECT tuple(1, 2)

```


```
(1,2)

```

## tupleConcat[​](#tupleConcat "Direct link to tupleConcat")


Introduced in: v23\.8\.0


Combines tuples passed as arguments.


**Syntax**



```
tupleConcat(tuple1[, tuple2, [...]])

```

**Arguments**


- `tupleN` — Arbitrary number of arguments of Tuple type. [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple containing all elements from the input tuples. [`Tuple(T)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Usage example**



```
SELECT tupleConcat((1, 2), ('a',), (true, false))

```


```
(1, 2, 'a', true, false)

```

## tupleDivide[​](#tupleDivide "Direct link to tupleDivide")


Introduced in: v21\.11\.0


Calculates the element\-wise division of two or more tuples of the same size, applied left\-to\-right.


NoteDivision by zero will return `inf`.


**Syntax**



```
tupleDivide(t1, t2[, tN, ...])

```

**Arguments**


- `t1` — First input tuple. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `t2, ..., tN` — One or more further input tuples. All tuples must have the same size. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple containing the element\-wise quotients. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Two tuples**



```
SELECT tupleDivide((1, 2), (2, 3))

```


```
(0.5, 0.6666666666666666)

```

**Three tuples**



```
SELECT tupleDivide((100.0, 60.0), (5.0, 3.0), (2.0, 4.0))

```


```
(10, 5)

```

## tupleDivideByNumber[​](#tupleDivideByNumber "Direct link to tupleDivideByNumber")


Introduced in: v21\.11\.0


Returns a tuple with all elements divided by a number.


NoteDivision by zero will return `inf`.


**Syntax**



```
tupleDivideByNumber(tuple, number)

```

**Arguments**


- `tuple` — Tuple to divide. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `number` — Divider. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a tuple with divided elements. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT tupleDivideByNumber((1, 2), 0.5)

```


```
(2, 4)

```

## tupleElement[​](#tupleElement "Direct link to tupleElement")


Introduced in: v1\.1\.0


Extracts an element from a tuple by index or name.


For access by index, an 1\-based numeric index is expected.
For access by name, the element name can be provided as a string (works only for named tuples).


Negative indexes are supported. In this case, the corresponding element is selected, numbered from the end. For example, `tuple.-1` is the last element in the tuple.


An optional third argument specifies a default value which is returned instead of throwing an exception when the accessed element does not exist.
All arguments must be constants.


This function has zero runtime cost and implements the operators `x.index` and `x.name`.


**Syntax**



```
tupleElement(tuple, index|name[, default_value])

```

**Arguments**


- `tuple` — A tuple or array of tuples. [`Tuple(T)`](/docs/sql-reference/data-types/tuple) or [`Array(Tuple(T))`](/docs/sql-reference/data-types/array)
- `index` — Column index, starting from 1\. [`const UInt8/16/32/64`](/docs/sql-reference/data-types/int-uint)
- `name` — Name of the element. [`const String`](/docs/sql-reference/data-types/string)
- `default_value` — Default value returned when index is out of bounds or element doesn't exist. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the element at the specified index or name. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Index access**



```
SELECT tupleElement((1, 'hello'), 2)

```


```
hello

```

**Negative indexing**



```
SELECT tupleElement((1, 'hello'), -1)

```


```
hello

```

**Named tuple with table**



```
CREATE TABLE example (values Tuple(name String, age UInt32)) ENGINE = Memory;
INSERT INTO example VALUES (('Alice', 30));
SELECT tupleElement(values, 'name') FROM example;

```


```
Alice

```

**With default value**



```
SELECT tupleElement((1, 2), 5, 'not_found')

```


```
not_found

```

**Operator syntax**



```
SELECT (1, 'hello').2

```


```
hello

```

## tupleHammingDistance[​](#tupleHammingDistance "Direct link to tupleHammingDistance")


Introduced in: v21\.1\.0


Returns the [Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance) between two tuples of the same size.


NoteThe result type is determined the same way it is for [Arithmetic functions](/docs/sql-reference/functions/arithmetic-functions), based on the number of elements in the input tuples.
```
SELECT
    toTypeName(tupleHammingDistance(tuple(0), tuple(0))) AS t1,
    toTypeName(tupleHammingDistance((0, 0), (0, 0))) AS t2,
    toTypeName(tupleHammingDistance((0, 0, 0), (0, 0, 0))) AS t3,
    toTypeName(tupleHammingDistance((0, 0, 0, 0), (0, 0, 0, 0))) AS t4,
    toTypeName(tupleHammingDistance((0, 0, 0, 0, 0), (0, 0, 0, 0, 0))) AS t5

```

```
┌─t1────┬─t2─────┬─t3─────┬─t4─────┬─t5─────┐
│ UInt8 │ UInt16 │ UInt32 │ UInt64 │ UInt64 │
└───────┴────────┴────────┴────────┴────────┘

```



**Syntax**



```
tupleHammingDistance(t1, t2)

```

**Arguments**


- `t1` — First tuple. [`Tuple(*)`](/docs/sql-reference/data-types/tuple)
- `t2` — Second tuple. [`Tuple(*)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns the Hamming distance. [`UInt8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT tupleHammingDistance((1, 2, 3), (3, 2, 1))

```


```
2

```

**With MinHash to detect semi\-duplicate strings**



```
SELECT tupleHammingDistance(wordShingleMinHash(string), wordShingleMinHashCaseInsensitive(string)) FROM (SELECT 'ClickHouse is a column-oriented database management system for online analytical processing of queries.' AS string)

```


```
2

```

## tupleIntDiv[​](#tupleIntDiv "Direct link to tupleIntDiv")


Introduced in: v23\.8\.0


Performs element\-wise integer division of two or more tuples of the same size, applied left\-to\-right. Returns a tuple of quotients.
If any tuple contains non\-integer elements, the result is calculated by rounding to the nearest integer for each non\-integer numerator or divisor.
Division by 0 causes an exception to be thrown.


**Syntax**



```
tupleIntDiv(t1, t2[, tN, ...])

```

**Arguments**


- `t1` — First input tuple. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `t2, ..., tN` — One or more further input tuples. All tuples must have the same size. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple of integer quotients. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Two tuples**



```
SELECT tupleIntDiv((15, 10, 5), (5, 5, 5))

```


```
(3, 2, 1)

```

**With decimals**



```
SELECT tupleIntDiv((15, 10, 5), (5.5, 5.5, 5.5))

```


```
(2, 1, 0)

```

**Three tuples**



```
SELECT tupleIntDiv((120, 60), (4, 3), (2, 4))

```


```
(15, 5)

```

## tupleIntDivByNumber[​](#tupleIntDivByNumber "Direct link to tupleIntDivByNumber")


Introduced in: v23\.8\.0


Performs integer division of a tuple of numerators by a given denominator, and returns a tuple of the quotients.
If either of the input parameters contain non\-integer elements then the result is calculated by rounding to the nearest integer for each non\-integer numerator or divisor.
An error will be thrown for division by 0\.


**Syntax**



```
tupleIntDivByNumber(tuple_num, div)

```

**Arguments**


- `tuple_num` — Tuple of numerator values. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `div` — The divisor value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a tuple of the quotients. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT tupleIntDivByNumber((15, 10, 5), 5)

```


```
(3, 2, 1)

```

**With decimals**



```
SELECT tupleIntDivByNumber((15.2, 10.7, 5.5), 5.8)

```


```
(2, 1, 0)

```

## tupleIntDivOrZero[​](#tupleIntDivOrZero "Direct link to tupleIntDivOrZero")


Introduced in: v23\.8\.0


Like [`tupleIntDiv`](#tupleIntDiv), performs element\-wise integer division of two or more tuples of the same size, applied left\-to\-right.
In case of division by 0, returns 0 for that element instead of throwing an exception.
If any tuple contains non\-integer elements, the result is calculated by rounding to the nearest integer for each non\-integer numerator or divisor.


**Syntax**



```
tupleIntDivOrZero(t1, t2[, tN, ...])

```

**Arguments**


- `t1` — First input tuple. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `t2, ..., tN` — One or more further input tuples. All tuples must have the same size. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple of integer quotients, with 0 for any element where the divisor is 0\. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**With zero divisors**



```
SELECT tupleIntDivOrZero((5, 10, 15), (0, 0, 0))

```


```
(0, 0, 0)

```

**Three tuples**



```
SELECT tupleIntDivOrZero((120, 60), (4, 3), (2, 4))

```


```
(15, 5)

```

## tupleIntDivOrZeroByNumber[​](#tupleIntDivOrZeroByNumber "Direct link to tupleIntDivOrZeroByNumber")


Introduced in: v23\.8\.0


Like [`tupleIntDivByNumber`](#tupleIntDivByNumber) it does integer division of a tuple of numerators by a given denominator, and returns a tuple of the quotients.
It does not throw an error for zero divisors, but rather returns the quotient as zero.
If either the tuple or div contain non\-integer elements then the result is calculated by rounding to the nearest integer for each non\-integer numerator or divisor.


**Syntax**



```
tupleIntDivOrZeroByNumber(tuple_num, div)

```

**Arguments**


- `tuple_num` — Tuple of numerator values. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `div` — The divisor value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a tuple of the quotients with `0` for quotients where the divisor is `0`. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT tupleIntDivOrZeroByNumber((15, 10, 5), 5)

```


```
(3, 2, 1)

```

**With zero divisor**



```
SELECT tupleIntDivOrZeroByNumber((15, 10, 5), 0)

```


```
(0, 0, 0)

```

## tupleMinus[​](#tupleMinus "Direct link to tupleMinus")


Introduced in: v21\.11\.0


Calculates the element\-wise difference of two or more tuples of the same size, applied left\-to\-right.


**Syntax**



```
tupleMinus(t1, t2[, tN, ...])

```

**Aliases**: `vectorDifference`


**Arguments**


- `t1` — First input tuple. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `t2, ..., tN` — One or more further input tuples. All tuples must have the same size. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple containing the element\-wise differences. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Two tuples**



```
SELECT tupleMinus((1, 2), (2, 3))

```


```
(-1, -1)

```

**Three tuples**



```
SELECT tupleMinus((10, 10), (3, 4), (2, 1))

```


```
(5, 5)

```

## tupleModulo[​](#tupleModulo "Direct link to tupleModulo")


Introduced in: v23\.8\.0


Returns a tuple of element\-wise remainders from dividing two or more tuples of the same size, applied left\-to\-right.


**Syntax**



```
tupleModulo(t1, t2[, tN, ...])

```

**Arguments**


- `t1` — First input tuple. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `t2, ..., tN` — One or more further input tuples. All tuples must have the same size. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple of element\-wise remainders. An exception is thrown for division by zero. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Two tuples**



```
SELECT tupleModulo((15, 10, 5), (5, 3, 2))

```


```
(0, 1, 1)

```

**Three tuples**



```
SELECT tupleModulo((10, 20), (7, 9), (3, 5))

```


```
(0, 2)

```

## tupleModuloByNumber[​](#tupleModuloByNumber "Direct link to tupleModuloByNumber")


Introduced in: v23\.8\.0


Returns a tuple of the moduli (remainders) of division operations of a tuple and a given divisor.


**Syntax**



```
tupleModuloByNumber(tuple_num, div)

```

**Arguments**


- `tuple_num` — Tuple of numerator elements. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `div` — The divisor value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns tuple of the remainders of division. An error is thrown for division by zero. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT tupleModuloByNumber((15, 10, 5), 2)

```


```
(1, 0, 1)

```

## tupleMultiply[​](#tupleMultiply "Direct link to tupleMultiply")


Introduced in: v21\.11\.0


Calculates the element\-wise product of two or more tuples of the same size.


**Syntax**



```
tupleMultiply(t1, t2[, tN, ...])

```

**Arguments**


- `t1` — First input tuple. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `t2, ..., tN` — One or more further input tuples. All tuples must have the same size. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple containing the element\-wise products. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Two tuples**



```
SELECT tupleMultiply((1, 2), (2, 3))

```


```
(2, 6)

```

**Three tuples**



```
SELECT tupleMultiply((1, 2), (2, 3), (1, 2))

```


```
(2, 12)

```

## tupleMultiplyByNumber[​](#tupleMultiplyByNumber "Direct link to tupleMultiplyByNumber")


Introduced in: v21\.11\.0


Returns a tuple with all elements multiplied by a number.


**Syntax**



```
tupleMultiplyByNumber(tuple, number)

```

**Arguments**


- `tuple` — Tuple to multiply. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `number` — Multiplier. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a tuple with multiplied elements. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT tupleMultiplyByNumber((1, 2), -2.1)

```


```
(-2.1, -4.2)

```

## tupleNames[​](#tupleNames "Direct link to tupleNames")


Introduced in: v24\.8\.0


Converts a tuple into an array of column names. For a tuple in the form `Tuple(a T, b T, ...)`, it returns an array of strings representing the named columns of the tuple. If the tuple elements do not have explicit names, their indices will be used as the column names instead.


**Syntax**



```
tupleNames(tuple)

```

**Arguments**


- None.


**Returned value**


**Examples**


**typical**



```
SELECT tupleNames(tuple(1 as a, 2 as b))

```


```
['a','b']

```

## tupleNegate[​](#tupleNegate "Direct link to tupleNegate")


Introduced in: v21\.11\.0


Calculates the negation of the tuple elements.


**Syntax**



```
tupleNegate(t)

```

**Arguments**


- `t` — Tuple to negate. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple with the result of negation. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT tupleNegate((1, 2))

```


```
(-1, -2)

```

## tuplePlus[​](#tuplePlus "Direct link to tuplePlus")


Introduced in: v21\.11\.0


Calculates the element\-wise sum of two or more tuples of the same size.


**Syntax**



```
tuplePlus(t1, t2[, tN, ...])

```

**Aliases**: `vectorSum`


**Arguments**


- `t1` — First input tuple. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `t2, ..., tN` — One or more further input tuples. All tuples must have the same size. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns a tuple containing the element\-wise sums. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Two tuples**



```
SELECT tuplePlus((1, 2), (2, 3))

```


```
(3, 5)

```

**Three tuples**



```
SELECT tuplePlus((1, 2), (2, 3), (3, 4))

```


```
(6, 9)

```

## tuplePositiveModuloByNumber[​](#tuplePositiveModuloByNumber "Direct link to tuplePositiveModuloByNumber")


Introduced in: v26\.4\.0


Returns a tuple of the positive moduli (remainders) of division operations of a tuple and a given divisor.
Unlike tupleModuloByNumber, the result is always non\-negative.


**Syntax**



```
tuplePositiveModuloByNumber(tuple_num, div)

```

**Arguments**


- `tuple_num` — Tuple of numerator values. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)
- `div` — The divisor value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns a tuple of the non\-negative remainders. [`Tuple((U)Int*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Float*)`](/docs/sql-reference/data-types/tuple) or [`Tuple(Decimal)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Basic usage**



```
SELECT tuplePositiveModuloByNumber((15, 10, 5), 2)

```


```
(1, 0, 1)

```

## tupleToNameValuePairs[​](#tupleToNameValuePairs "Direct link to tupleToNameValuePairs")


Introduced in: v21\.9\.0


Converts a tuple to an array of `(name, value)` pairs.
For example, tuple `Tuple(n1 T1, n2 T2, ...)` is converted to `Array(Tuple('n1', T1), Tuple('n2', T2), ...)`.
All values in the tuple must be of the same type.


**Syntax**



```
tupleToNameValuePairs(tuple)

```

**Arguments**


- `tuple` — Named tuple with any types of values. [`Tuple(n1 T1[, n2 T2, ...])`](/docs/sql-reference/data-types/tuple)


**Returned value**


Returns an array with `(name, value)` pairs. [`Array(Tuple(String, T))`](/docs/sql-reference/data-types/array)


**Examples**


**Named tuple**



```
SELECT tupleToNameValuePairs(tuple(1593 AS user_ID, 2502 AS session_ID))

```


```
[('1', 1593), ('2', 2502)]

```

**Unnamed tuple**



```
SELECT tupleToNameValuePairs(tuple(3, 2, 1))

```


```
[('1', 3), ('2', 2), ('3', 1)]

```

## untuple[​](#untuple "Direct link to untuple")


Performs syntactic substitution of [tuple](/docs/sql-reference/data-types/tuple) elements in the call location.


The names of the result columns are implementation\-specific and subject to change. Do not assume specific column names after `untuple`.


**Syntax**



```
untuple(x)

```

You can use the `EXCEPT` expression to skip columns as a result of the query.


**Arguments**


- `x` — A `tuple` function, column, or tuple of elements. [Tuple](/docs/sql-reference/data-types/tuple).


**Returned value**


- None.


**Examples**


Input table:



```
┌─key─┬─v1─┬─v2─┬─v3─┬─v4─┬─v5─┬─v6────────┐
│   1 │ 10 │ 20 │ 40 │ 30 │ 15 │ (33,'ab') │
│   2 │ 25 │ 65 │ 70 │ 40 │  6 │ (44,'cd') │
│   3 │ 57 │ 30 │ 20 │ 10 │  5 │ (55,'ef') │
│   4 │ 55 │ 12 │  7 │ 80 │ 90 │ (66,'gh') │
│   5 │ 30 │ 50 │ 70 │ 25 │ 55 │ (77,'kl') │
└─────┴────┴────┴────┴────┴────┴───────────┘

```

Example of using a `Tuple`\-type column as the `untuple` function parameter:



```
SELECT untuple(v6) FROM kv;

```


```
┌─_ut_1─┬─_ut_2─┐
│    33 │ ab    │
│    44 │ cd    │
│    55 │ ef    │
│    66 │ gh    │
│    77 │ kl    │
└───────┴───────┘

```

Example of using an `EXCEPT` expression:



```
SELECT untuple((* EXCEPT (v2, v3),)) FROM kv;

```


```
┌─key─┬─v1─┬─v4─┬─v5─┬─v6────────┐
│   1 │ 10 │ 30 │ 15 │ (33,'ab') │
│   2 │ 25 │ 40 │  6 │ (44,'cd') │
│   3 │ 57 │ 10 │  5 │ (55,'ef') │
│   4 │ 55 │ 80 │ 90 │ (66,'gh') │
│   5 │ 30 │ 25 │ 55 │ (77,'kl') │
└─────┴────┴────┴────┴───────────┘

```

## Distance functions[​](#distance-functions "Direct link to Distance functions")


All supported functions are described in [distance functions documentation](/docs/sql-reference/functions/distance-functions).

[PreviousTime window](/docs/sql-reference/functions/time-window-functions)[NextMaps](/docs/sql-reference/functions/tuple-map-functions)- [dotProduct](#dotProduct)- [flattenTuple](#flattenTuple)- [tuple](#tuple)- [tupleConcat](#tupleConcat)- [tupleDivide](#tupleDivide)- [tupleDivideByNumber](#tupleDivideByNumber)- [tupleElement](#tupleElement)- [tupleHammingDistance](#tupleHammingDistance)- [tupleIntDiv](#tupleIntDiv)- [tupleIntDivByNumber](#tupleIntDivByNumber)- [tupleIntDivOrZero](#tupleIntDivOrZero)- [tupleIntDivOrZeroByNumber](#tupleIntDivOrZeroByNumber)- [tupleMinus](#tupleMinus)- [tupleModulo](#tupleModulo)- [tupleModuloByNumber](#tupleModuloByNumber)- [tupleMultiply](#tupleMultiply)- [tupleMultiplyByNumber](#tupleMultiplyByNumber)- [tupleNames](#tupleNames)- [tupleNegate](#tupleNegate)- [tuplePlus](#tuplePlus)- [tuplePositiveModuloByNumber](#tuplePositiveModuloByNumber)- [tupleToNameValuePairs](#tupleToNameValuePairs)- [untuple](#untuple)- [Distance functions](#distance-functions)
Was this page helpful?
