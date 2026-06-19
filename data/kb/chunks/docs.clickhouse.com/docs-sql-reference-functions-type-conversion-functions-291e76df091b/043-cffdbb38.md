---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/type-conversion-functions.md)#
topic: type-conversion-functions-clickhouse-docs
ch_version_introduced: '123.45'
last_updated: '2026-06-12'
chunk_index: 43
total_chunks_in_doc: 72
---

[`Float*`](/docs/sql-reference/data-types/float) - `default` — Optional. The default value to return if parsing is unsuccessful. [`Float64`](/docs/sql-reference/data-types/float) **Returned value** Returns a value of type Float64 if successful, otherwise returns the default value if passed or 0 if not. [`Float64`](/docs/sql-reference/data-types/float) **Examples**

**Successful conversion**

```
SELECT toFloat64OrDefault('8', CAST('0', 'Float64'))

```

```
8

```

**Failed conversion**

```
SELECT toFloat64OrDefault('abc', CAST('0', 'Float64'))

```

```
0

```

## toFloat64OrNull[​](#toFloat64OrNull "Direct link to toFloat64OrNull")

Introduced in: v1\.1\.0

Converts an input value to a value of type [Float64](/docs/sql-reference/data-types/float) but returns `NULL` in case of an error.
Like [`toFloat64`](#toFloat64) but returns `NULL` instead of throwing an exception on conversion errors.

Supported arguments:

- Values of type (U)Int\*.
- String representations of (U)Int8/16/32/128/256\.
- Values of type Float\*, including `NaN` and `Inf`.
- String representations of type Float\*, including `NaN` and `Inf` (case\-insensitive).

Unsupported arguments (return `NULL`):

- String representations of binary and hexadecimal values, e.g. `SELECT toFloat64OrNull('0xc0fe');`.
- Invalid string formats.

See also:

- [`toFloat64`](#toFloat64).
- [`toFloat64OrZero`](#toFloat64OrZero).
- [`toFloat64OrDefault`](#toFloat64OrDefault).

**Syntax**

```
toFloat64OrNull(x)

```

**Arguments**

- `x` — A string representation of a number. [`String`](/docs/sql-reference/data-types/string)

**Returned value**

Returns a 64\-bit Float value if successful, otherwise `NULL`. [`Float64`](/docs/sql-reference/data-types/float) or [`NULL`](/docs/sql-reference/syntax#null)

**Examples**

**Usage example**

```
SELECT
    toFloat64OrNull('42.7'),
    toFloat64OrNull('NaN'),
    toFloat64OrNull('abc')
FORMAT Vertical

```

```
Row 1:
──────
toFloat64OrNull('42.7'): 42.7
toFloat64OrNull('NaN'):  nan
toFloat64OrNull('abc'):  \N

```

## toFloat64OrZero[​](#toFloat64OrZero "Direct link to toFloat64OrZero")

Introduced in: v1\.1\.0

Converts an input value to a value of type [Float64](/docs/sql-reference/data-types/float) but returns `0` in case of an error.
Like [`toFloat64`](#toFloat64) but returns `0` instead of throwing an exception on conversion errors.

See also:

- [`toFloat64`](#toFloat64).
- [`toFloat64OrNull`](#toFloat64OrNull).
- [`toFloat64OrDefault`](#toFloat64OrDefault).

**Syntax**

```
toFloat64OrZero(x)

```

**Arguments**

- `x` — A string representation of a number. [`String`](/docs/sql-reference/data-types/string)

**Returned value**

Returns a 64\-bit Float value if successful, otherwise `0`. [`Float64`](/docs/sql-reference/data-types/float)

**Examples**

**Usage example**

```
SELECT
    toFloat64OrZero('42.7'),
    toFloat64OrZero('abc')
FORMAT Vertical

```

```
Row 1:
──────
toFloat64OrZero('42.7'): 42.7
toFloat64OrZero('abc'):  0

```

## toInt128[​](#toInt128 "Direct link to toInt128")

Introduced in: v1\.1\.0

Converts an input value to a value of type [Int128](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.
The function uses rounding towards zero, meaning it truncates fractional digits of numbers.

Supported arguments:

- Values or string representations of type (U)Int\*.
- Values of type Float\*.

Unsupported arguments:

- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt128('0xc0fe');`.
