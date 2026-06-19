---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/type-conversion-functions.md)#
topic: type-conversion-functions-clickhouse-docs
ch_version_introduced: '123.45'
last_updated: '2026-06-12'
chunk_index: 18
total_chunks_in_doc: 72
---

- `x` — Number of days since the beginning of the Unix Epoch. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) **Returned value** Date. [`Date`](/docs/sql-reference/data-types/date) **Examples** **Usage example** ``` SELECT reinterpretAsDate(65), reinterpretAsDate('A') ```

```
┌─reinterpretAsDate(65)─┬─reinterpretAsDate('A')─┐
│            1970-03-07 │             1970-03-07 │
└───────────────────────┴────────────────────────┘

```

## reinterpretAsDateTime[​](#reinterpretAsDateTime "Direct link to reinterpretAsDateTime")

Introduced in: v1\.1\.0

Reinterprets the input value as a DateTime value (assuming little endian order) which is the number of days since the beginning of the Unix epoch 1970\-01\-01

**Syntax**

```
reinterpretAsDateTime(x)

```

**Arguments**

- `x` — Number of seconds since the beginning of the Unix Epoch. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)

**Returned value**

Date and Time. [`DateTime`](/docs/sql-reference/data-types/datetime)

**Examples**

**Usage example**

```
SELECT reinterpretAsDateTime(65), reinterpretAsDateTime('A')

```

```
┌─reinterpretAsDateTime(65)─┬─reinterpretAsDateTime('A')─┐
│       1970-01-01 01:01:05 │        1970-01-01 01:01:05 │
└───────────────────────────┴────────────────────────────┘

```

## reinterpretAsFixedString[​](#reinterpretAsFixedString "Direct link to reinterpretAsFixedString")

Introduced in: v1\.1\.0

Reinterprets the input value as a fixed string (assuming little endian order).
Null bytes at the end are ignored, for example, the function returns for UInt32 value 255 a string with a single character.

**Syntax**

```
reinterpretAsFixedString(x)

```

**Arguments**

- `x` — Value to reinterpret to string. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)

**Returned value**

Fixed string containing bytes representing `x`. [`FixedString`](/docs/sql-reference/data-types/fixedstring)

**Examples**

**Usage example**

```
SELECT
    reinterpretAsFixedString(toDateTime('1970-01-01 01:01:05')),
    reinterpretAsFixedString(toDate('1970-03-07'))

```

```
┌─reinterpretAsFixedString(toDateTime('1970-01-01 01:01:05'))─┬─reinterpretAsFixedString(toDate('1970-03-07'))─┐
│ A                                                           │ A                                              │
└─────────────────────────────────────────────────────────────┴────────────────────────────────────────────────┘

```

## reinterpretAsFloat32[​](#reinterpretAsFloat32 "Direct link to reinterpretAsFloat32")

Introduced in: v1\.1\.0

Reinterprets the input value as a value of type Float32\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.

**Syntax**

```
reinterpretAsFloat32(x)

```

**Arguments**

- `x` — Value to reinterpret as Float32\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)

**Returned value**

Returns the reinterpreted value `x`. [`Float32`](/docs/sql-reference/data-types/float)

**Examples**

**Usage example**

```
SELECT reinterpretAsUInt32(toFloat32(0.2)) AS x, reinterpretAsFloat32(x)

```

```
┌──────────x─┬─reinterpretAsFloat32(x)─┐
│ 1045220557 │                     0.2 │
└────────────┴─────────────────────────┘

```

## reinterpretAsFloat64[​](#reinterpretAsFloat64 "Direct link to reinterpretAsFloat64")

Introduced in: v1\.1\.0

Reinterprets the input value as a value of type Float64\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.

**Syntax**

```
reinterpretAsFloat64(x)

```

**Arguments**
