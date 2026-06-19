---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/type-conversion-functions.md)#
topic: type-conversion-functions-clickhouse-docs
ch_version_introduced: '123.45'
last_updated: '2026-06-12'
chunk_index: 65
total_chunks_in_doc: 72
---

type UInt256, otherwise `0` if the conversion is unsuccessful. [`UInt256`](/docs/sql-reference/data-types/int-uint) **Examples** **Usage example** ``` SELECT toUInt256OrZero('256'), toUInt256OrZero('abc') FORMAT Vertical ``` ``` Row 1: ────── toUInt256OrZero('256'): 256 toUInt256OrZero('abc'): 0 ``` ## toUInt32[​](#toUInt32 "Direct link to toUInt32") Introduced in: v1\.1\.0

Converts an input value to a value of type [`UInt32`](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.

Supported arguments:

- Values or string representations of type (U)Int\*.
- Values of type Float\*.

Unsupported arguments:

- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt32('0xc0fe');`.

NoteIf the input value cannot be represented within the bounds of [`UInt32`](/docs/sql-reference/data-types/int-uint), the result over or under flows.
This is not considered an error.
For example: `SELECT toUInt32(4294967296) == 0;`

NoteThe function uses [rounding towards zero](https://en.wikipedia.org/wiki/Rounding#Rounding_towards_zero), meaning it truncates fractional digits of numbers.

See also:

- [`toUInt32OrZero`](#toUInt32OrZero).
- [`toUInt32OrNull`](#toUInt32OrNull).
- [`toUInt32OrDefault`](#toUInt32OrDefault).

**Syntax**

```
toUInt32(expr)

```

**Arguments**

- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)

**Returned value**

Returns a 32\-bit unsigned integer value. [`UInt32`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Usage example**

```
SELECT
    toUInt32(32),
    toUInt32(32.32),
    toUInt32('32')
FORMAT Vertical

```

```
Row 1:
──────
toUInt32(32):    32
toUInt32(32.32): 32
toUInt32('32'):  32

```

## toUInt32OrDefault[​](#toUInt32OrDefault "Direct link to toUInt32OrDefault")

Introduced in: v21\.11\.0

Like [`toUInt32`](#toUInt32), this function converts an input value to a value of type [UInt32](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.

**Syntax**

```
toUInt32OrDefault(expr[, default])

```

**Arguments**

- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`UInt32`](/docs/sql-reference/data-types/int-uint)

**Returned value**

Returns a value of type UInt32 if successful, otherwise returns the default value if passed, or 0 if not. [`UInt32`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Successful conversion**

```
SELECT toUInt32OrDefault('32', CAST('0', 'UInt32'))

```

```
32

```

**Failed conversion**

```
SELECT toUInt32OrDefault('abc', CAST('0', 'UInt32'))

```

```
0

```

## toUInt32OrNull[​](#toUInt32OrNull "Direct link to toUInt32OrNull")

Introduced in: v1\.1\.0

Like [`toUInt32`](#toUInt32), this function converts an input value to a value of type [`UInt32`](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.

Supported arguments:

- String representations of (U)Int8/16/32/128/256\.

Unsupported arguments (return `NULL`):
