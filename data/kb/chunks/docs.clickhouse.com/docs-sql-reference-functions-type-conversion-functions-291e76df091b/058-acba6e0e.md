---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/type-conversion-functions.md)#
topic: type-conversion-functions-clickhouse-docs
ch_version_introduced: '123.45'
last_updated: '2026-06-12'
chunk_index: 58
total_chunks_in_doc: 72
---

string terminators. This function is useful for processing C\-style strings or binary data where null bytes mark the end of meaningful content. **Syntax** ``` toStringCutToZero(s) ``` **Arguments** - `s` — String or FixedString to process. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)

**Returned value**

Returns a String containing the characters before the first null byte. [`String`](/docs/sql-reference/data-types/string)

**Examples**

**Usage example**

```
SELECT
    toStringCutToZero('hello'),
    toStringCutToZero('hello\0world')

```

```
┌─toStringCutToZero('hello')─┬─toStringCutToZero('hello\\0world')─┐
│ hello                      │ hello                             │
└────────────────────────────┴───────────────────────────────────┘

```

## toTime[​](#toTime "Direct link to toTime")

Introduced in: v1\.1\.0

Converts an input value to type [Time](/docs/sql-reference/data-types/time).
Supports conversion from String, FixedString, DateTime, or numeric types representing seconds since midnight.

**Syntax**

```
toTime(x)

```

**Arguments**

- `x` — Input value to convert. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)

**Returned value**

Returns the converted value. [`Time`](/docs/sql-reference/data-types/time)

**Examples**

**String to Time conversion**

```
SELECT toTime('14:30:25')

```

```
14:30:25

```

**DateTime to Time conversion**

```
SELECT toTime(toDateTime('2025-04-15 14:30:25'))

```

```
14:30:25

```

**Integer to Time conversion**

```
SELECT toTime(52225)

```

```
14:30:25

```

## toTime64[​](#toTime64 "Direct link to toTime64")

Introduced in: v25\.6\.0

Converts an input value to type [Time64](/docs/sql-reference/data-types/time64).
Supports conversion from String, FixedString, DateTime64, or numeric types representing microseconds since midnight.
Provides microsecond precision for time values.

**Syntax**

```
toTime64(x)

```

**Arguments**

- `x` — Input value to convert. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`DateTime64`](/docs/sql-reference/data-types/datetime64) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)

**Returned value**

Returns the converted input value with microsecond precision. [`Time64(6)`](/docs/sql-reference/data-types/time64)

**Examples**

**String to Time64 conversion**

```
SELECT toTime64('14:30:25.123456')

```

```
14:30:25.123456

```

**DateTime64 to Time64 conversion**

```
SELECT toTime64(toDateTime64('2025-04-15 14:30:25.123456', 6))

```

```
14:30:25.123456

```

**Integer to Time64 conversion**

```
SELECT toTime64(52225123456)

```

```
14:30:25.123456

```

## toTime64OrNull[​](#toTime64OrNull "Direct link to toTime64OrNull")

Introduced in: v25\.6\.0

Converts an input value to a value of type `Time64` but returns `NULL` in case of an error.
Like [`toTime64`](#toTime64) but returns `NULL` instead of throwing an exception on conversion errors.

See also:

- [`toTime64`](#toTime64)
- [`toTime64OrZero`](#toTime64OrZero)

**Syntax**

```
toTime64OrNull(x)

```

**Arguments**

- `x` — A string representation of a time with subsecond precision. [`String`](/docs/sql-reference/data-types/string)

**Returned value**

Returns a Time64 value if successful, otherwise `NULL`. [`Time64`](/docs/sql-reference/data-types/time64) or [`NULL`](/docs/sql-reference/syntax#null)

**Examples**

**Usage example**

```
SELECT toTime64OrNull('12:30:45.123'), toTime64OrNull('invalid')

```

```
┌─toTime64OrNull('12:30:45.123')─┬─toTime64OrNull('invalid')─┐
│                   12:30:45.123 │                      ᴺᵁᴸᴸ │
└────────────────────────────────┴───────────────────────────┘

```

## toTime64OrZero[​](#toTime64OrZero "Direct link to toTime64OrZero")

Introduced in: v25\.6\.0
