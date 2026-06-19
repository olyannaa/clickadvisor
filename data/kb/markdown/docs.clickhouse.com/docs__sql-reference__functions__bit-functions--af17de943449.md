# Bit Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Bit
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/bit-functions.md)# Bit Functions

Bit functions work for any pair of types from `UInt8`, `UInt16`, `UInt32`, `UInt64`, `Int8`, `Int16`, `Int32`, `Int64`, `Float32`, or `Float64`. Some functions support `String` and `FixedString` types.


The result type is an integer with bits equal to the maximum bits of its arguments. If at least one of the arguments is signed, the result is a signed number. If an argument is a floating\-point number, it is cast to Int64\.


## bitAnd[​](#bitAnd "Direct link to bitAnd")


Introduced in: v1\.1\.0


Performs bitwise AND operation between two values.


**Syntax**



```
bitAnd(a, b)

```

**Arguments**


- `a` — First value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `b` — Second value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the result of bitwise operation `a AND b`


**Examples**


**Usage example**



```
CREATE TABLE bits
(
    `a` UInt8,
    `b` UInt8
)
ENGINE = Memory;

INSERT INTO bits VALUES (0, 0), (0, 1), (1, 0), (1, 1);

SELECT
    a,
    b,
    bitAnd(a, b)
FROM bits

```


```
┌─a─┬─b─┬─bitAnd(a, b)─┐
│ 0 │ 0 │            0 │
│ 0 │ 1 │            0 │
│ 1 │ 0 │            0 │
│ 1 │ 1 │            1 │
└───┴───┴──────────────┘

```

## bitCount[​](#bitCount "Direct link to bitCount")


Introduced in: v20\.3\.0


Calculates the number of bits set to one in the binary representation of a number.


**Syntax**



```
bitCount(x)

```

**Arguments**


- `x` — An integer or float value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the number of bits set to one in `x`. [`UInt8`](/docs/sql-reference/data-types/int-uint).


NoteThe function does not convert the input value to a larger type ([sign extension](https://en.wikipedia.org/wiki/Sign_extension)).
For example: `bitCount(toUInt8(-1)) = 8`.


**Examples**


**Usage example**



```
SELECT bin(333), bitCount(333);

```


```
┌─bin(333)─────────┬─bitCount(333)─┐
│ 0000000101001101 │             5 │
└──────────────────┴───────────────┘

```

## bitHammingDistance[​](#bitHammingDistance "Direct link to bitHammingDistance")


Introduced in: v21\.1\.0


Returns the [Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance) between the bit representations of two numbers.
Can be used with [`SimHash`](/docs/sql-reference/functions/hash-functions#ngramSimHash) functions for detection of semi\-duplicate strings.
The smaller the distance, the more similar the strings are.


**Syntax**



```
bitHammingDistance(x, y)

```

**Arguments**


- `x` — First number for Hamming distance calculation. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `y` — Second number for Hamming distance calculation. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the hamming distance between `x` and `y` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bitHammingDistance(111, 121);

```


```
┌─bitHammingDistance(111, 121)─┐
│                            3 │
└──────────────────────────────┘

```

## bitNot[​](#bitNot "Direct link to bitNot")


Introduced in: v1\.1\.0


Performs the bitwise NOT operation.


**Syntax**



```
bitNot(a)

```

**Arguments**


- `a` — Value for which to apply bitwise NOT operation. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the result of `~a` i.e `a` with bits flipped.


**Examples**


**Usage example**



```
SELECT
    CAST('5', 'UInt8') AS original,
    bin(original) AS original_binary,
    bitNot(original) AS result,
    bin(bitNot(original)) AS result_binary;

```


```
┌─original─┬─original_binary─┬─result─┬─result_binary─┐
│        5 │ 00000101        │    250 │ 11111010      │
└──────────┴─────────────────┴────────┴───────────────┘

```

## bitOr[​](#bitOr "Direct link to bitOr")


Introduced in: v1\.1\.0


Performs bitwise OR operation between two values.


**Syntax**



```
bitOr(a, b)

```

**Arguments**


- `a` — First value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `b` — Second value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the result of bitwise operation `a OR b`


**Examples**


**Usage example**



```
CREATE TABLE bits
(
    `a` UInt8,
    `b` UInt8
)
ENGINE = Memory;

INSERT INTO bits VALUES (0, 0), (0, 1), (1, 0), (1, 1);

SELECT
    a,
    b,
    bitOr(a, b)
FROM bits;

```


```
┌─a─┬─b─┬─bitOr(a, b)─┐
│ 0 │ 0 │           0 │
│ 0 │ 1 │           1 │
│ 1 │ 0 │           1 │
│ 1 │ 1 │           1 │
└───┴───┴─────────────┘

```

## bitRotateLeft[​](#bitRotateLeft "Direct link to bitRotateLeft")


Introduced in: v1\.1\.0


Rotate bits left by a certain number of positions. Bits that fall off wrap around to the right.


**Syntax**



```
bitRotateLeft(a, N)

```

**Arguments**


- `a` — A value to rotate. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)
- `N` — The number of positions to rotate left. [`UInt8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the rotated value with type equal to that of `a`. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT 99 AS a, bin(a), bitRotateLeft(a, 2) AS a_rotated, bin(a_rotated);

```


```
┌──a─┬─bin(a)───┬─a_rotated─┬─bin(a_rotated)─┐
│ 99 │ 01100011 │       141 │ 10001101       │
└────┴──────────┴───────────┴────────────────┘

```

## bitRotateRight[​](#bitRotateRight "Direct link to bitRotateRight")


Introduced in: v1\.1\.0


Rotate bits right by a certain number of positions. Bits that fall off wrap around to the left.


**Syntax**



```
bitRotateRight(a, N)

```

**Arguments**


- `a` — A value to rotate. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)
- `N` — The number of positions to rotate right. [`UInt8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the rotated value with type equal to that of `a`. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT 99 AS a, bin(a), bitRotateRight(a, 2) AS a_rotated, bin(a_rotated);

```


```
┌──a─┬─bin(a)───┬─a_rotated─┬─bin(a_rotated)─┐
│ 99 │ 01100011 │       216 │ 11011000       │
└────┴──────────┴───────────┴────────────────┘

```

## bitShiftLeft[​](#bitShiftLeft "Direct link to bitShiftLeft")


Introduced in: v1\.1\.0


Shifts the binary representation of a value to the left by a specified number of bit positions.


A `FixedString` or a `String` is treated as a single multibyte value.


Bits of a `FixedString` value are lost as they are shifted out.
On the contrary, a `String` value is extended with additional bytes, so no bits are lost.


**Syntax**



```
bitShiftLeft(a, N)

```

**Arguments**


- `a` — A value to shift. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `N` — The number of positions to shift. [`UInt8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the shifted value with type equal to that of `a`.


**Examples**


**Usage example with binary encoding**



```
SELECT 99 AS a, bin(a), bitShiftLeft(a, 2) AS a_shifted, bin(a_shifted);

```


```
┌──a─┬─bin(99)──┬─a_shifted─┬─bin(bitShiftLeft(99, 2))─┐
│ 99 │ 01100011 │       140 │ 10001100                 │
└────┴──────────┴───────────┴──────────────────────────┘

```

**Usage example with hexadecimal encoding**



```
SELECT 'abc' AS a, hex(a), bitShiftLeft(a, 4) AS a_shifted, hex(a_shifted);

```


```
┌─a───┬─hex('abc')─┬─a_shifted─┬─hex(bitShiftLeft('abc', 4))─┐
│ abc │ 616263     │ &0        │ 06162630                    │
└─────┴────────────┴───────────┴─────────────────────────────┘

```

**Usage example with Fixed String encoding**



```
SELECT toFixedString('abc', 3) AS a, hex(a), bitShiftLeft(a, 4) AS a_shifted, hex(a_shifted);

```


```
┌─a───┬─hex(toFixedString('abc', 3))─┬─a_shifted─┬─hex(bitShiftLeft(toFixedString('abc', 3), 4))─┐
│ abc │ 616263                       │ &0        │ 162630                                        │
└─────┴──────────────────────────────┴───────────┴───────────────────────────────────────────────┘

```

## bitShiftRight[​](#bitShiftRight "Direct link to bitShiftRight")


Introduced in: v1\.1\.0


Shifts the binary representation of a value to the right by a specified number of bit positions.


A `FixedString` or a `String` is treated as a single multibyte value.


Bits of a `FixedString` value are lost as they are shifted out.
On the contrary, a `String` value is extended with additional bytes, so no bits are lost.


**Syntax**



```
bitShiftRight(a, N)

```

**Arguments**


- `a` — A value to shift. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `N` — The number of positions to shift. [`UInt8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the shifted value with type equal to that of `a`.


**Examples**


**Usage example with binary encoding**



```
SELECT 101 AS a, bin(a), bitShiftRight(a, 2) AS a_shifted, bin(a_shifted);

```


```
┌───a─┬─bin(101)─┬─a_shifted─┬─bin(bitShiftRight(101, 2))─┐
│ 101 │ 01100101 │        25 │ 00011001                   │
└─────┴──────────┴───────────┴────────────────────────────┘

```

**Usage example with hexadecimal encoding**



```
SELECT 'abc' AS a, hex(a), bitShiftLeft(a, 4) AS a_shifted, hex(a_shifted);

```


```
┌─a───┬─hex('abc')─┬─a_shifted─┬─hex(bitShiftRight('abc', 12))─┐
│ abc │ 616263     │           │ 0616                          │
└─────┴────────────┴───────────┴───────────────────────────────┘

```

**Usage example with Fixed String encoding**



```
SELECT toFixedString('abc', 3) AS a, hex(a), bitShiftRight(a, 12) AS a_shifted, hex(a_shifted);

```


```
┌─a───┬─hex(toFixedString('abc', 3))─┬─a_shifted─┬─hex(bitShiftRight(toFixedString('abc', 3), 12))─┐
│ abc │ 616263                       │           │ 000616                                          │
└─────┴──────────────────────────────┴───────────┴─────────────────────────────────────────────────┘

```

## bitSlice[​](#bitSlice "Direct link to bitSlice")


Introduced in: v22\.2\.0


Returns a substring starting with the bit from the 'offset' index that is 'length' bits long.


**Syntax**



```
bitSlice(s, offset[, length])

```

**Arguments**


- `s` — The String or Fixed String to slice. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `offset` —
Returns the starting bit position (1\-based indexing).
- Positive values: count from the beginning of the string.
- Negative values: count from the end of the string.


[`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `length` —
Optional. The number of bits to extract.
- Positive values: extract `length` bits.
- Negative values: extract from the offset to `(string_length - |length|)`.
- Omitted: extract from offset to end of string.
- If length is not a multiple of 8, the result is padded with zeros on the right.
[`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns a string containing the extracted bits, represented as a binary sequence. The result is always padded to byte boundaries (multiples of 8 bits) [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT bin('Hello'), bin(bitSlice('Hello', 1, 8));
SELECT bin('Hello'), bin(bitSlice('Hello', 1, 2));
SELECT bin('Hello'), bin(bitSlice('Hello', 1, 9));
SELECT bin('Hello'), bin(bitSlice('Hello', -4, 8));

```


```
┌─bin('Hello')─────────────────────────────┬─bin(bitSlice('Hello', 1, 8))─┐
│ 0100100001100101011011000110110001101111 │ 01001000                     │
└──────────────────────────────────────────┴──────────────────────────────┘
┌─bin('Hello')─────────────────────────────┬─bin(bitSlice('Hello', 1, 2))─┐
│ 0100100001100101011011000110110001101111 │ 01000000                     │
└──────────────────────────────────────────┴──────────────────────────────┘
┌─bin('Hello')─────────────────────────────┬─bin(bitSlice('Hello', 1, 9))─┐
│ 0100100001100101011011000110110001101111 │ 0100100000000000             │
└──────────────────────────────────────────┴──────────────────────────────┘
┌─bin('Hello')─────────────────────────────┬─bin(bitSlice('Hello', -4, 8))─┐
│ 0100100001100101011011000110110001101111 │ 11110000                      │
└──────────────────────────────────────────┴───────────────────────────────┘

```

## bitTest[​](#bitTest "Direct link to bitTest")


Introduced in: v1\.1\.0


Takes any number and converts it into [binary form](https://en.wikipedia.org/wiki/Binary_number), then returns the value of the bit at a specified position. Counting is done right\-to\-left, starting at 0\.


**Syntax**



```
bitTest(a, i)

```

**Arguments**


- `a` — Number to convert. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `i` — Position of the bit to return. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the value of the bit at position `i` in the binary representation of `a` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT bin(2), bitTest(2, 1);

```


```
┌─bin(2)───┬─bitTest(2, 1)─┐
│ 00000010 │             1 │
└──────────┴───────────────┘

```

## bitTestAll[​](#bitTestAll "Direct link to bitTestAll")


Introduced in: v1\.1\.0


Returns result of the [logical conjunction](https://en.wikipedia.org/wiki/Logical_conjunction) (AND operator) of all bits at the given positions.
Counts right\-to\-left, starting at 0\.


The logical AND between two bits is true if and only if both input bits are true.


**Syntax**



```
bitTestAll(a, index1[, index2, ... , indexN])

```

**Arguments**


- `a` — An integer value. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)
- `index1, ...` — One or multiple positions of bits. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the result of the logical conjunction [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example 1**



```
SELECT bitTestAll(43, 0, 1, 3, 5);

```


```
┌─bin(43)──┬─bitTestAll(43, 0, 1, 3, 5)─┐
│ 00101011 │                          1 │
└──────────┴────────────────────────────┘

```

**Usage example 2**



```
SELECT bitTestAll(43, 0, 1, 3, 5, 2);

```


```
┌─bin(43)──┬─bitTestAll(4⋯1, 3, 5, 2)─┐
│ 00101011 │                        0 │
└──────────┴──────────────────────────┘

```

## bitTestAny[​](#bitTestAny "Direct link to bitTestAny")


Introduced in: v1\.1\.0


Returns result of the [logical disjunction](https://en.wikipedia.org/wiki/Logical_disjunction) (OR operator) of all bits at the given positions in a number.
Counts right\-to\-left, starting at 0\.


The logical OR between two bits is true if at least one of the input bits is true.


**Syntax**



```
bitTestAny(a, index1[, index2, ... , indexN])

```

**Arguments**


- `a` — An integer value. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)
- `index1, ...` — One or multiple positions of bits. [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the result of the logical disjunction [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example 1**



```
SELECT bitTestAny(43, 0, 2);

```


```
┌─bin(43)──┬─bitTestAny(43, 0, 2)─┐
│ 00101011 │                    1 │
└──────────┴──────────────────────┘

```

**Usage example 2**



```
SELECT bitTestAny(43, 4, 2);

```


```
┌─bin(43)──┬─bitTestAny(43, 4, 2)─┐
│ 00101011 │                    0 │
└──────────┴──────────────────────┘

```

## bitXor[​](#bitXor "Direct link to bitXor")


Introduced in: v1\.1\.0


Performs bitwise exclusive or (XOR) operation between two values.


**Syntax**



```
bitXor(a, b)

```

**Arguments**


- `a` — First value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `b` — Second value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the result of bitwise operation `a XOR b`


**Examples**


**Usage example**



```
CREATE TABLE bits
(
    `a` UInt8,
    `b` UInt8
)
ENGINE = Memory;

INSERT INTO bits VALUES (0, 0), (0, 1), (1, 0), (1, 1);

SELECT
    a,
    b,
    bitXor(a, b)
FROM bits;

```


```
┌─a─┬─b─┬─bitXor(a, b)─┐
│ 0 │ 0 │            0 │
│ 0 │ 1 │            1 │
│ 1 │ 0 │            1 │
│ 1 │ 1 │            0 │
└───┴───┴──────────────┘

```
[PreviousarrayJoin](/docs/sql-reference/functions/array-join)[NextBitmap](/docs/sql-reference/functions/bitmap-functions)- [bitAnd](#bitAnd)- [bitCount](#bitCount)- [bitHammingDistance](#bitHammingDistance)- [bitNot](#bitNot)- [bitOr](#bitOr)- [bitRotateLeft](#bitRotateLeft)- [bitRotateRight](#bitRotateRight)- [bitShiftLeft](#bitShiftLeft)- [bitShiftRight](#bitShiftRight)- [bitSlice](#bitSlice)- [bitTest](#bitTest)- [bitTestAll](#bitTestAll)- [bitTestAny](#bitTestAny)- [bitXor](#bitXor)
Was this page helpful?
