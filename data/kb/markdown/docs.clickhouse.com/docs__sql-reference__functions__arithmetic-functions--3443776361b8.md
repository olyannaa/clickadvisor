# Arithmetic Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Arithmetic
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/arithmetic-functions.md)# Arithmetic Functions

## Overview[​](#overview "Direct link to Overview")


Arithmetic functions work for any two operands of type `UInt8`, `UInt16`, `UInt32`, `UInt64`, `Int8`, `Int16`, `Int32`, `Int64`, `Float32`, or `Float64`.


Before performing the operation, both operands are cast to the result type. The result type is determined as follows (unless specified
differently in the function documentation below):


- If both operands are up to 32 bits wide, the size of the result type will be the size of the next bigger type following the bigger of the
two operands (integer size promotion). For example, `UInt8 + UInt16 = UInt32` or `Float32 * Float32 = Float64`.
- If one of the operands has 64 or more bits, the size of the result type will be the same size as the bigger of the two operands. For
example, `UInt32 + UInt128 = UInt128` or `Float32 * Float64 = Float64`.
- If one of the operands is signed, the result type will also be signed, otherwise it will be unsigned. For example, `UInt32 * Int32 = Int64` or `UInt32 * UInt32 = UInt64`.


These rules make sure that the result type will be the smallest type which can represent all possible results. While this introduces a risk
of overflows around the value range boundary, it ensures that calculations are performed quickly using the maximum native integer width of
64 bit. This behavior also guarantees compatibility with many other databases which provide 64 bit integers (BIGINT) as the biggest integer
type.


Example:



```
SELECT toTypeName(0), toTypeName(0 + 0), toTypeName(0 + 0 + 0), toTypeName(0 + 0 + 0 + 0)

```


```
┌─toTypeName(0)─┬─toTypeName(plus(0, 0))─┬─toTypeName(plus(plus(0, 0), 0))─┬─toTypeName(plus(plus(plus(0, 0), 0), 0))─┐
│ UInt8         │ UInt16                 │ UInt32                          │ UInt64                                   │
└───────────────┴────────────────────────┴─────────────────────────────────┴──────────────────────────────────────────┘

```

Overflows are produced the same way as in C\+\+.


## abs[​](#abs "Direct link to abs")


Introduced in: v1\.1\.0


Calculates the absolute value of `x`. Has no effect if `x` is of an unsigned type. If `x` is of a signed type, it returns an unsigned number.


**Syntax**



```
abs(x)

```

**Arguments**


- `x` — Value to get the absolute value of


**Returned value**


The absolute value of `x`


**Examples**


**Usage example**



```
SELECT abs(-0.5)

```


```
0.5

```

## avg2[​](#avg2 "Direct link to avg2")


Introduced in: v25\.11\.0


Computes and returns the average value of the provided arguments.
Supports numerical and temporal types.


**Syntax**



```
avg2(x1, x2])

```

**Arguments**


- `x1, x2]` — Accepts two values for averaging.


**Returned value**


Returns the average value of the provided arguments, promoted to the largest compatible type.


**Examples**


**Numeric types**



```
SELECT avg2(toUInt8(3), 1.0) AS result, toTypeName(result) AS type;
-- The type returned is a Float64 as the UInt8 must be promoted to 64 bit for the comparison.

```


```
┌─result─┬─type────┐
│      2 │ Float64 │
└────────┴─────────┘

```

**Decimal types**



```
SELECT avg2(toDecimal32(1, 2), 2) AS result, toTypeName(result) AS type;

```


```
┌─result─┬─type──────────┐
│    1.5 │ Decimal(9, 2) │
└────────┴───────────────┘

```

**Date types**



```
SELECT avg2(toDate('2025-01-01'), toDate('2025-01-05')) AS result, toTypeName(result) AS type;

```


```
┌─────result─┬─type─┐
│ 2025-01-03 │ Date │
└────────────┴──────┘

```

**DateTime types**



```
SELECT avg2(toDateTime('2025-01-01 00:00:00'), toDateTime('2025-01-03 12:00:00')) AS result, toTypeName(result) AS type;

```


```
┌──────────────result─┬─type─────┐
│ 2025-01-02 06:00:00 │ DateTime │
└─────────────────────┴──────────┘

```

**Time64 types**



```
SELECT avg2(toTime64('12:00:00', 0), toTime64('14:00:00', 0)) AS result, toTypeName(result) AS type;

```


```
┌───result─┬─type──────┐
│ 13:00:00 │ Time64(0) │
└──────────┴───────────┘

```

## byteSwap[​](#byteSwap "Direct link to byteSwap")


Introduced in: v23\.10\.0


Reverses the bytes of an integer, i.e. changes its [endianness](https://en.wikipedia.org/wiki/Endianness).


The below example can be worked out in the following manner:


1. Convert the base\-10 integer to its equivalent hexadecimal format in big\-endian format, i.e. 3351772109 \-\> C7 C7 FB CD (4 bytes)
2. Reverse the bytes, i.e. C7 C7 FB CD \-\> CD FB C7 C7
3. Convert the result back to an integer assuming big\-endian, i.e. CD FB C7 C7 \-\> 3455829959
One use case of this function is reversing IPv4s:



```
┌─toIPv4(byteSwap(toUInt32(toIPv4('205.251.199.199'))))─┐
│ 199.199.251.205                                       │
└───────────────────────────────────────────────────────┘

```

**Syntax**



```
byteSwap(x)

```

**Arguments**


- `x` — An integer value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns `x` with bytes reversed. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT byteSwap(3351772109)

```


```
3455829959

```

**8\-bit**



```
SELECT byteSwap(54)

```


```
54

```

**16\-bit**



```
SELECT byteSwap(4135)

```


```
10000

```

**32\-bit**



```
SELECT byteSwap(3351772109)

```


```
3455829959

```

**64\-bit**



```
SELECT byteSwap(123294967295)

```


```
18439412204227788800

```

## divide[​](#divide "Direct link to divide")


Introduced in: v1\.1\.0


Calculates the quotient of two values `a` and `b`. The result type is always [Float64](/docs/sql-reference/data-types/float).
Integer division is provided by the `intDiv` function.


NoteDivision by `0` returns `inf`, `-inf`, or `nan`.


**Syntax**



```
divide(x, y)

```

**Arguments**


- `x` — Dividend \- `y` — Divisor


**Returned value**


The quotient of x and y


**Examples**


**Dividing two numbers**



```
SELECT divide(25,5) AS quotient, toTypeName(quotient)

```


```
5 Float64

```

**Dividing by zero**



```
SELECT divide(25,0)

```


```
inf

```

## divideDecimal[​](#divideDecimal "Direct link to divideDecimal")


Introduced in: v22\.12\.0


Performs division on two decimals. Result value will be of type [Decimal256](/docs/sql-reference/data-types/decimal).
Result scale can be explicitly specified by `result_scale` argument (const Integer in range `[0, 76]`). If not specified, the result scale is the max scale of given arguments.


NoteThese function work significantly slower than usual `divide`.
In case you don't really need controlled precision and/or need fast computation, consider using [divide](#divide).


**Syntax**



```
divideDecimal(x, y[, result_scale])

```

**Arguments**


- `x` — First value: [Decimal](/docs/sql-reference/data-types/decimal). \- `y` — Second value: [Decimal](/docs/sql-reference/data-types/decimal). \- `result_scale` — Scale of result. Type [Int/UInt](/docs/sql-reference/data-types/int-uint).


**Returned value**


The result of division with given scale. [`Decimal256`](/docs/sql-reference/data-types/decimal)


**Examples**


**Example 1**



```
divideDecimal(toDecimal256(-12, 0), toDecimal32(2.1, 1), 10)

```


```
┌─divideDecimal(toDecimal256(-12, 0), toDecimal32(2.1, 1), 10)─┐
│                                                -5.7142857142 │
└──────────────────────────────────────────────────────────────┘

```

**Example 2**



```
SELECT toDecimal64(-12, 1) / toDecimal32(2.1, 1);
SELECT toDecimal64(-12, 1) as a, toDecimal32(2.1, 1) as b, divideDecimal(a, b, 1), divideDecimal(a, b, 5);

```


```
┌─divide(toDecimal64(-12, 1), toDecimal32(2.1, 1))─┐
│                                             -5.7 │
└──────────────────────────────────────────────────┘
┌───a─┬───b─┬─divideDecimal(toDecimal64(-12, 1), toDecimal32(2.1, 1), 1)─┬─divideDecimal(toDecimal64(-12, 1), toDecimal32(2.1, 1), 5)─┐
│ -12 │ 2.1 │                                                       -5.7 │                                                   -5.71428 │
└─────┴─────┴────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────┘

```

## divideOrNull[​](#divideOrNull "Direct link to divideOrNull")


Introduced in: v25\.5\.0


Same as `divide` but returns NULL when dividing by zero.


**Syntax**



```
divideOrNull(x, y)

```

**Arguments**


- `x` — Dividend \- `y` — Divisor


**Returned value**


The quotient of x and y, or NULL.


**Examples**


**Dividing by zero**



```
SELECT divideOrNull(25, 0)

```


```
\N

```

## gcd[​](#gcd "Direct link to gcd")


Introduced in: v1\.1\.0


Returns the greatest common divisor of two values a and b.


An exception is thrown when dividing by zero or when dividing a minimal
negative number by minus one.


**Syntax**



```
gcd(x, y)

```

**Arguments**


- `x` — First integer \- `y` — Second integer


**Returned value**


The greatest common divisor of `x` and `y`.


**Examples**


**Usage example**



```
SELECT gcd(12, 18)

```


```
6

```

## ifNotFinite[​](#ifNotFinite "Direct link to ifNotFinite")


Introduced in: v20\.3\.0


Checks whether a floating point value is finite.


You can get a similar result by using the [ternary operator](/docs/sql-reference/functions/conditional-functions#if): `isFinite(x) ? x : y`.


**Syntax**



```
ifNotFinite(x,y)

```

**Arguments**


- `x` — Value to check if infinite. [`Float*`](/docs/sql-reference/data-types/float)
- `y` — Fallback value. [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


- `x` if `x` is finite.
- `y` if `x` is not finite.


**Examples**


**Usage example**



```
SELECT 1/0 AS infimum, ifNotFinite(infimum,42)

```


```
inf  42

```

## intDiv[​](#intDiv "Direct link to intDiv")


Introduced in: v1\.1\.0


Performs an integer division of two values `x` by `y`. In other words it
computes the quotient rounded down to the next smallest integer.


The result has the same width as the dividend (the first parameter).


An exception is thrown when dividing by zero, when the quotient does not fit
in the range of the dividend, or when dividing a minimal negative number by minus one.


**Syntax**



```
intDiv(x, y)

```

**Arguments**


- `x` — Left hand operand. \- `y` — Right hand operand.


**Returned value**


Result of integer division of `x` and `y`


**Examples**


**Integer division of two floats**



```
SELECT intDiv(toFloat64(1), 0.001) AS res, toTypeName(res)

```


```
┌──res─┬─toTypeName(intDiv(toFloat64(1), 0.001))─┐
│ 1000 │ Int64                                   │
└──────┴─────────────────────────────────────────┘

```

**Quotient does not fit in the range of the dividend**



```
SELECT
intDiv(1, 0.001) AS res,
toTypeName(res)

```


```
Received exception from server (version 23.2.1):
Code: 153. DB::Exception: Received from localhost:9000. DB::Exception:
Cannot perform integer division, because it will produce infinite or too
large number: While processing intDiv(1, 0.001) AS res, toTypeName(res).
(ILLEGAL_DIVISION)

```

## intDivOrNull[​](#intDivOrNull "Direct link to intDivOrNull")


Introduced in: v25\.5\.0


Same as `intDiv` but returns NULL when dividing by zero or when dividing a
minimal negative number by minus one.


**Syntax**



```
intDivOrNull(x, y)

```

**Arguments**


- `x` — Left hand operand. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `y` — Right hand operand. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Result of integer division of `x` and `y`, or NULL.


**Examples**


**Integer division by zero**



```
SELECT intDivOrNull(1, 0)

```


```
\N

```

**Dividing a minimal negative number by minus 1**



```
SELECT intDivOrNull(-9223372036854775808, -1)

```


```
\N

```

## intDivOrZero[​](#intDivOrZero "Direct link to intDivOrZero")


Introduced in: v1\.1\.0


Same as `intDiv` but returns zero when dividing by zero or when dividing a
minimal negative number by minus one.


**Syntax**



```
intDivOrZero(a, b)

```

**Arguments**


- `a` — Left hand operand. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `b` — Right hand operand. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Result of integer division of a and b, or zero.


**Examples**


**Integer division by zero**



```
SELECT intDivOrZero(1, 0)

```


```
0

```

**Dividing a minimal negative number by minus 1**



```
SELECT intDivOrZero(0.05, -1)

```


```
0

```

## isFinite[​](#isFinite "Direct link to isFinite")


Introduced in: v1\.1\.0


Returns `1` if the Float32 or Float64 argument not infinite and not a `NaN`,
otherwise this function returns `0`.


**Syntax**



```
isFinite(x)

```

**Arguments**


- `x` — Number to check for finiteness. [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


`1` if x is not infinite and not `NaN`, otherwise `0`.


**Examples**


**Test if a number is finite**



```
SELECT isFinite(inf)

```


```
0

```

## isInfinite[​](#isInfinite "Direct link to isInfinite")


Introduced in: v1\.1\.0


Returns `1` if the Float32 or Float64 argument is infinite, otherwise this function returns `0`.
Note that `0` is returned for a `NaN`.


**Syntax**



```
isInfinite(x)

```

**Arguments**


- `x` — Number to check for infiniteness. [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


`1` if x is infinite, otherwise `0` (including for `NaN`).


**Examples**


**Test if a number is infinite**



```
SELECT isInfinite(inf), isInfinite(NaN), isInfinite(10))

```


```
1 0 0

```

## isNaN[​](#isNaN "Direct link to isNaN")


Introduced in: v1\.1\.0


Returns `1` if the Float32 and Float64 argument is `NaN`, otherwise returns `0`.


**Syntax**



```
isNaN(x)

```

**Arguments**


- `x` — Argument to evaluate for if it is `NaN`. [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


`1` if `NaN`, otherwise `0`


**Examples**


**Usage example**



```
SELECT isNaN(NaN)

```


```
1

```

## lcm[​](#lcm "Direct link to lcm")


Introduced in: v1\.1\.0


Returns the least common multiple of two values `x` and `y`.


An exception is thrown when dividing by zero or when dividing a minimal negative number by minus one.


**Syntax**



```
lcm(x, y)

```

**Arguments**


- `x` — First integer. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `y` — Second integer. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the least common multiple of `x` and `y`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT lcm(6, 8)

```


```
24

```

## max2[​](#max2 "Direct link to max2")


Introduced in: v21\.11\.0


Returns the bigger of two numeric values `x` and `y`.


**Syntax**



```
max2(x, y)

```

**Arguments**


- `x` — First value [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `y` — Second value [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the bigger value of `x` and `y`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT max2(-1, 2)

```


```
2

```

## midpoint[​](#midpoint "Direct link to midpoint")


Introduced in: v25\.11\.0


Computes and returns the average value of the provided arguments.
Supports numerical and temporal types.


**Syntax**



```
midpoint(x1[, x2, ...])

```

**Arguments**


- `x1[, x2, ...]` — Accepts a single value or multiple values for averaging.


**Returned value**


Returns the average value of the provided arguments, promoted to the largest compatible type.


**Examples**


**Numeric types**



```
SELECT midpoint(1, toUInt8(3), 0.5) AS result, toTypeName(result) AS type;
-- The type returned is a Float64 as the UInt8 must be promoted to 64 bit for the comparison.

```


```
┌─result─┬─type────┐
│    1.5 │ Float64 │
└────────┴─────────┘

```

**Decimal types**



```
SELECT midpoint(toDecimal32(1.5, 2), toDecimal32(1, 1), 2) AS result, toTypeName(result) AS type;

```


```
┌─result─┬─type──────────┐
│    1.5 │ Decimal(9, 2) │
└────────┴───────────────┘

```

**Date types**



```
SELECT midpoint(toDate('2025-01-01'), toDate('2025-01-05')) AS result, toTypeName(result) AS type;

```


```
┌─────result─┬─type─┐
│ 2025-01-03 │ Date │
└────────────┴──────┘

```

**DateTime types**



```
SELECT midpoint(toDateTime('2025-01-01 00:00:00'), toDateTime('2025-01-03 12:00:00')) AS result, toTypeName(result) AS type;

```


```
┌──────────────result─┬─type─────┐
│ 2025-01-02 06:00:00 │ DateTime │
└─────────────────────┴──────────┘

```

**Time64 types**



```
SELECT midpoint(toTime64('12:00:00', 0), toTime64('14:00:00', 0)) AS result, toTypeName(result) AS type;

```


```
┌───result─┬─type──────┐
│ 13:00:00 │ Time64(0) │
└──────────┴───────────┘

```

## min2[​](#min2 "Direct link to min2")


Introduced in: v21\.11\.0


Returns the smaller of two numeric values `x` and `y`.


**Syntax**



```
min2(x, y)

```

**Arguments**


- `x` — First value [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `y` — Second value [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the smaller value of `x` and `y`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT min2(-1, 2)

```


```
-1

```

## minus[​](#minus "Direct link to minus")


Introduced in: v1\.1\.0


Calculates the difference of two values `a` and `b`. The result is always signed.
Similar to plus, it is possible to subtract an integer from a date or date with time.
Additionally, subtraction between date with time is supported, resulting in the time difference between them.


**Syntax**



```
minus(x, y)

```

**Arguments**


- `x` — Minuend. \- `y` — Subtrahend.


**Returned value**


x minus y


**Examples**


**Subtracting two numbers**



```
SELECT minus(10, 5)

```


```
5

```

**Subtracting an integer and a date**



```
SELECT minus(toDate('2025-01-01'),5)

```


```
2024-12-27

```

## modulo[​](#modulo "Direct link to modulo")


Introduced in: v1\.1\.0


Calculates the remainder of the division of two values a by b.


The result type is an integer if both inputs are integers. If one of the
inputs is a floating\-point number, the result type is Float64\.


The remainder is computed like in C\+\+. Truncated division is used for
negative numbers.


An exception is thrown when dividing by zero or when dividing a minimal
negative number by minus one.


**Syntax**



```
modulo(a, b)

```

**Aliases**: `mod`


**Arguments**


- `a` — The dividend \- `b` — The divisor (modulus)


**Returned value**


The remainder of a % b


**Examples**


**Usage example**



```
SELECT modulo(5, 2)

```


```
1

```

## moduloLegacy[​](#moduloLegacy "Direct link to moduloLegacy")


Introduced in: v1\.1\.0


Calculates the remainder of a division. This is the legacy modulo implementation that uses the C\+\+ `%` operator, which may produce negative results for negative arguments. This function exists for backward compatibility with old table partitioning logic. Use `modulo` or `positiveModulo` for standard behavior.


**Syntax**



```
moduloLegacy(a, b)

```

**Arguments**


- `a` — The dividend. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `b` — The divisor. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the remainder of the division. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Examples**


**Basic usage**



```
SELECT moduloLegacy(10, 3)

```


```
1

```

## moduloOrNull[​](#moduloOrNull "Direct link to moduloOrNull")


Introduced in: v25\.5\.0


Calculates the remainder when dividing `a` by `b`. Similar to function `modulo` except that `moduloOrNull` will return NULL
if the right argument is 0\.


**Syntax**



```
moduloOrNull(x, y)

```

**Aliases**: `modOrNull`


**Arguments**


- `x` — The dividend. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `y` — The divisor (modulus). [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the remainder of the division of `x` by `y`, or null when the divisor is zero.


**Examples**


**moduloOrNull by zero**



```
SELECT moduloOrNull(5, 0)

```


```
\N

```

## moduloOrZero[​](#moduloOrZero "Direct link to moduloOrZero")


Introduced in: v20\.3\.0


Like modulo but returns zero when the divisor is zero, as opposed to an
exception with the modulo function.


**Syntax**



```
moduloOrZero(a, b)

```

**Arguments**


- `a` — The dividend. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `b` — The divisor (modulus). [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the remainder of a % b, or `0` when the divisor is `0`.


**Examples**


**Usage example**



```
SELECT moduloOrZero(5, 0)

```


```
0

```

## multiply[​](#multiply "Direct link to multiply")


Introduced in: v1\.1\.0


Calculates the product of two values `x` and `y`.


**Syntax**



```
multiply(x, y)

```

**Arguments**


- `x` — factor. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `y` — factor. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the product of x and y


**Examples**


**Multiplying two numbers**



```
SELECT multiply(5,5)

```


```
25

```

## multiplyDecimal[​](#multiplyDecimal "Direct link to multiplyDecimal")


Introduced in: v22\.12\.0


Performs multiplication on two decimals. Result value will be of type [Decimal256](/docs/sql-reference/data-types/decimal).
Result scale can be explicitly specified by `result_scale` argument (const Integer in range `[0, 76]`). If not specified, the result scale is the max scale of given arguments.


NoteThese functions work significantly slower than usual `multiply`.
In case you don't really need controlled precision and/or need fast computation, consider using [multiply](#multiply)


**Syntax**



```
multiplyDecimal(a, b[, result_scale])

```

**Arguments**


- `a` — First value. [`Decimal`](/docs/sql-reference/data-types/decimal)
- `b` — Second value. [`Decimal`](/docs/sql-reference/data-types/decimal)
- `result_scale` — Scale of result. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


The result of multiplication with the given scale. Type: [`Decimal256`](/docs/sql-reference/data-types/decimal)


**Examples**


**Usage example**



```
SELECT multiplyDecimal(toDecimal256(-12, 0), toDecimal32(-2.1, 1), 1)

```


```
25.2

```

**Difference with regular multiplication**



```
SELECT multiplyDecimal(toDecimal256(-12, 0), toDecimal32(-2.1, 1), 1)

```


```
┌─multiply(toDecimal64(-12.647, 3), toDecimal32(2.1239, 4))─┐
│                                               -26.8609633 │
└───────────────────────────────────────────────────────────┘
┌─multiplyDecimal(toDecimal64(-12.647, 3), toDecimal32(2.1239, 4))─┐
│                                                         -26.8609 │
└──────────────────────────────────────────────────────────────────┘

```

**Decimal overflow**



```
SELECT
    toDecimal64(-12.647987876, 9) AS a,
    toDecimal64(123.967645643, 9) AS b,
    multiplyDecimal(a, b);
SELECT
    toDecimal64(-12.647987876, 9) AS a,
    toDecimal64(123.967645643, 9) AS b,
    a * b;

```


```
┌─────────────a─┬─────────────b─┬─multiplyDecimal(toDecimal64(-12.647987876, 9), toDecimal64(123.967645643, 9))─┐
│ -12.647987876 │ 123.967645643 │                                                               -1567.941279108 │
└───────────────┴───────────────┴───────────────────────────────────────────────────────────────────────────────┘
Received exception from server (version 22.11.1):
Code: 407. DB::Exception: Received from localhost:9000. DB::Exception: Decimal math overflow:
While processing toDecimal64(-12.647987876, 9) AS a, toDecimal64(123.967645643, 9) AS b, a * b. (DECIMAL_OVERFLOW)

```

## negate[​](#negate "Direct link to negate")


Introduced in: v1\.1\.0


Negates the argument `x`. The result is always signed.


**Syntax**



```
negate(x)

```

**Arguments**


- `x` — The value to negate.


**Returned value**


Returns \-x from x


**Examples**


**Usage example**



```
SELECT negate(10)

```


```
-10

```

## plus[​](#plus "Direct link to plus")


Introduced in: v1\.1\.0


Calculates the sum of two values `x` and `y`. Alias: `x + y` (operator).
It is possible to add an integer and a date or date with time. The former
operation increments the number of days in the date, the latter operation
increments the number of seconds in the date with time.
It is also possible to add a date and a time. Adding a `Date` and a `Time`
produces a `DateTime`. Adding a `Date` and a `Time64`, or a `Date32` and
a `Time` or `Time64`, produces a `DateTime64`.


**Syntax**



```
plus(x, y)

```

**Arguments**


- `x` — Left hand operand. \- `y` — Right hand operand.


**Returned value**


Returns the sum of x and y


**Examples**


**Adding two numbers**



```
SELECT plus(5,5)

```


```
10

```

**Adding an integer and a date**



```
SELECT plus(toDate('2025-01-01'),5)

```


```
2025-01-06

```

**Adding a date and time**



```
SELECT toDate('2025-01-01') + CAST('14:30:25', 'Time')

```


```
2025-01-01 14:30:25

```

## positiveModulo[​](#positiveModulo "Direct link to positiveModulo")


Introduced in: v22\.11\.0


Calculates the remainder when dividing `x` by `y`. Similar to function
`modulo` except that `positiveModulo` always return non\-negative number.


**Syntax**



```
positiveModulo(x, y)

```

**Aliases**: `positive_modulo`, `pmod`


**Arguments**


- `x` — The dividend. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `y` — The divisor (modulus). [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns the difference between `x` and the nearest integer not greater than
`x` divisible by `y`.


**Examples**


**Usage example**



```
SELECT positiveModulo(-1, 10)

```


```
9

```

## positiveModuloOrNull[​](#positiveModuloOrNull "Direct link to positiveModuloOrNull")


Introduced in: v25\.5\.0


Calculates the remainder when dividing `a` by `b`. Similar to function `positiveModulo` except that `positiveModuloOrNull` will return NULL
if the right argument is 0\.


**Syntax**



```
positiveModuloOrNull(x, y)

```

**Aliases**: `positive_modulo_or_null`, `pmodOrNull`


**Arguments**


- `x` — The dividend. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)/[`Float32/64`](/docs/sql-reference/data-types/float). \- `x` — The divisor (modulus). [`(U)Int*`](/docs/sql-reference/data-types/int-uint)/[`Float32/64`](/docs/sql-reference/data-types/float).


**Returned value**


Returns the difference between `x` and the nearest integer not greater than
`x` divisible by `y`, `null` when the divisor is zero.


**Examples**


**positiveModuloOrNull**



```
SELECT positiveModuloOrNull(5, 0)

```


```
\N

```
[PreviousAI](/docs/sql-reference/functions/ai-functions)[NextArrays](/docs/sql-reference/functions/array-functions)- [Overview](#overview)- [abs](#abs)- [avg2](#avg2)- [byteSwap](#byteSwap)- [divide](#divide)- [divideDecimal](#divideDecimal)- [divideOrNull](#divideOrNull)- [gcd](#gcd)- [ifNotFinite](#ifNotFinite)- [intDiv](#intDiv)- [intDivOrNull](#intDivOrNull)- [intDivOrZero](#intDivOrZero)- [isFinite](#isFinite)- [isInfinite](#isInfinite)- [isNaN](#isNaN)- [lcm](#lcm)- [max2](#max2)- [midpoint](#midpoint)- [min2](#min2)- [minus](#minus)- [modulo](#modulo)- [moduloLegacy](#moduloLegacy)- [moduloOrNull](#moduloOrNull)- [moduloOrZero](#moduloOrZero)- [multiply](#multiply)- [multiplyDecimal](#multiplyDecimal)- [negate](#negate)- [plus](#plus)- [positiveModulo](#positiveModulo)- [positiveModuloOrNull](#positiveModuloOrNull)
Was this page helpful?
