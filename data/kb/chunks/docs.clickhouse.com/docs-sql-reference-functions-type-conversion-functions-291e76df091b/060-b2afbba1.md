---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/type-conversion-functions.md)#
topic: type-conversion-functions-clickhouse-docs
ch_version_introduced: '123.45'
last_updated: '2026-06-12'
chunk_index: 60
total_chunks_in_doc: 72
---

Supported arguments: - Values or string representations of type (U)Int\*. - Values of type Float\*. Unsupported arguments: - String representations of Float\* values, including `NaN` and `Inf`. - String representations of binary and hexadecimal values, e.g. `SELECT toUInt128('0xc0fe');`.

NoteIf the input value cannot be represented within the bounds of UInt128, the result over or under flows.
This is not considered an error.

See also:

- [`toUInt128OrZero`](#toUInt128OrZero).
- [`toUInt128OrNull`](#toUInt128OrNull).
- [`toUInt128OrDefault`](#toUInt128OrDefault).

**Syntax**

```
toUInt128(expr)

```

**Arguments**

- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)

**Returned value**

Returns a 128\-bit unsigned integer value. [`UInt128`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Usage example**

```
SELECT
    toUInt128(128),
    toUInt128(128.8),
    toUInt128('128')
FORMAT Vertical

```

```
Row 1:
──────
toUInt128(128):   128
toUInt128(128.8): 128
toUInt128('128'): 128

```

## toUInt128OrDefault[​](#toUInt128OrDefault "Direct link to toUInt128OrDefault")

Introduced in: v21\.11\.0

Like [`toUInt128`](#toUInt128), this function converts an input value to a value of type [`UInt128`](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.

**Syntax**

```
toUInt128OrDefault(expr[, default])

```

**Arguments**

- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`UInt128`](/docs/sql-reference/data-types/int-uint)

**Returned value**

Returns a value of type UInt128 if successful, otherwise returns the default value if passed, or 0 if not. [`UInt128`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Successful conversion**

```
SELECT toUInt128OrDefault('128', CAST('0', 'UInt128'))

```

```
128

```

**Failed conversion**

```
SELECT toUInt128OrDefault('abc', CAST('0', 'UInt128'))

```

```
0

```

## toUInt128OrNull[​](#toUInt128OrNull "Direct link to toUInt128OrNull")

Introduced in: v21\.6\.0

Like [`toUInt128`](#toUInt128), this function converts an input value to a value of type [`UInt128`](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.

Supported arguments:

- String representations of (U)Int\*.

Unsupported arguments (return `NULL`):

- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt128OrNull('0xc0fe');`.

NoteIf the input value cannot be represented within the bounds of [`UInt128`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.

See also:

- [`toUInt128`](#toUInt128).
- [`toUInt128OrZero`](#toUInt128OrZero).
- [`toUInt128OrDefault`](#toUInt128OrDefault).

**Syntax**

```
toUInt128OrNull(x)

```

**Arguments**

- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)

**Returned value**

Returns a value of type UInt128, otherwise `NULL` if the conversion is unsuccessful. [`UInt128`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)

**Examples**
