# Type conversion functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Type conversion
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/type-conversion-functions.md)# Type conversion functions

## Common issues with data conversion[​](#common-issues-with-data-conversion "Direct link to Common issues with data conversion")


ClickHouse generally uses the [same behavior as C\+\+ programs](https://en.cppreference.com/w/cpp/language/implicit_conversion).


`to<type>` functions and [cast](#CAST) behave differently in some cases, for example in case of [LowCardinality](/docs/sql-reference/data-types/lowcardinality): [cast](#CAST) removes [LowCardinality](/docs/sql-reference/data-types/lowcardinality) trait `to<type>` functions don't. The same with [Nullable](/docs/sql-reference/data-types/nullable), this behaviour is not compatible with SQL standard, and it can be changed using [cast\_keep\_nullable](/docs/operations/settings/settings#cast_keep_nullable) setting.


NoteBe aware of potential data loss if values of a datatype are converted to a smaller datatype (for example from `Int64` to `Int32`) or between
incompatible datatypes (for example from `String` to `Int`). Make sure to check carefully if the result is as expected.


Example:



```
SELECT
    toTypeName(toLowCardinality('') AS val) AS source_type,
    toTypeName(toString(val)) AS to_type_result_type,
    toTypeName(CAST(val, 'String')) AS cast_result_type

┌─source_type────────────┬─to_type_result_type────┬─cast_result_type─┐
│ LowCardinality(String) │ LowCardinality(String) │ String           │
└────────────────────────┴────────────────────────┴──────────────────┘

SELECT
    toTypeName(toNullable('') AS val) AS source_type,
    toTypeName(toString(val)) AS to_type_result_type,
    toTypeName(CAST(val, 'String')) AS cast_result_type

┌─source_type──────┬─to_type_result_type─┬─cast_result_type─┐
│ Nullable(String) │ Nullable(String)    │ String           │
└──────────────────┴─────────────────────┴──────────────────┘

SELECT
    toTypeName(toNullable('') AS val) AS source_type,
    toTypeName(toString(val)) AS to_type_result_type,
    toTypeName(CAST(val, 'String')) AS cast_result_type
SETTINGS cast_keep_nullable = 1

┌─source_type──────┬─to_type_result_type─┬─cast_result_type─┐
│ Nullable(String) │ Nullable(String)    │ Nullable(String) │
└──────────────────┴─────────────────────┴──────────────────┘

```

## Notes on `toString` functions[​](#to-string-functions "Direct link to to-string-functions")


The `toString` family of functions allows for converting between numbers, strings (but not fixed strings), dates, and dates with times.
All of these functions accept one argument.


- When converting to or from a string, the value is formatted or parsed using the same rules as for the TabSeparated format (and almost all other text formats). If the string can't be parsed, an exception is thrown and the request is canceled.
- When converting dates to numbers or vice versa, the date corresponds to the number of days since the beginning of the Unix epoch.
- When converting dates with times to numbers or vice versa, the date with time corresponds to the number of seconds since the beginning of the Unix epoch.
- The `toString` function of the `DateTime` argument can take a second String argument containing the name of the time zone, for example: `Europe/Amsterdam`. In this case, the time is formatted according to the specified time zone.


## Notes on `toDate`/`toDateTime` functions[​](#to-date-and-date-time-functions "Direct link to to-date-and-date-time-functions")


The date and date\-with\-time formats for the `toDate`/`toDateTime` functions are defined as follows:



```
YYYY-MM-DD
YYYY-MM-DD hh:mm:ss

```

As an exception, if converting from UInt32, Int32, UInt64, or Int64 numeric types to Date, and if the number is greater than or equal to 65536, the number is interpreted as a Unix timestamp (and not as the number of days) and is rounded to the date.
This allows support for the common occurrence of writing `toDate(unix_timestamp)`, which otherwise would be an error and would require writing the more cumbersome `toDate(toDateTime(unix_timestamp))`.


Conversion between a date and a date with time is performed the natural way: by adding a null time or dropping the time.


Conversion between numeric types uses the same rules as assignments between different numeric types in C\+\+.


**Example**



```
SELECT
    now() AS ts,
    time_zone,
    toString(ts, time_zone) AS str_tz_datetime
FROM system.time_zones
WHERE time_zone LIKE 'Europe%'
LIMIT 10

```


```
┌──────────────────ts─┬─time_zone─────────┬─str_tz_datetime─────┐
│ 2023-09-08 19:14:59 │ Europe/Amsterdam  │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Andorra    │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Astrakhan  │ 2023-09-08 23:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Athens     │ 2023-09-08 22:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Belfast    │ 2023-09-08 20:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Belgrade   │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Berlin     │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Bratislava │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Brussels   │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Bucharest  │ 2023-09-08 22:14:59 │
└─────────────────────┴───────────────────┴─────────────────────┘

```

Also see the [`toUnixTimestamp`](/docs/sql-reference/functions/date-time-functions#toUnixTimestamp) function.


## CAST[​](#CAST "Direct link to CAST")


Introduced in: v1\.1\.0


Converts a value to a specified data type.
Unlike the reinterpret function, CAST tries to generate the same value in the target type.
If that is not possible, an exception is raised.


**Syntax**



```
CAST(x, T)
or CAST(x AS T)
or x::T

```

**Arguments**


- `x` — A value of any type. [`Any`](/docs/sql-reference/data-types)
- `T` — The target data type. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the converted value with the target data type. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Basic usage**



```
SELECT CAST(42, 'String')

```


```
┌─CAST(42, 'String')─┐
│ 42                 │
└────────────────────┘

```

**Using AS syntax**



```
SELECT CAST('2025-01-01' AS Date)

```


```
┌─CAST('2025-01-01', 'Date')─┐
│                 2025-01-01 │
└────────────────────────────┘

```

**Using :: syntax**



```
SELECT '123'::UInt32

```


```
┌─CAST('123', 'UInt32')─┐
│                   123 │
└───────────────────────┘

```

## DATE[​](#DATE "Direct link to DATE")


Introduced in: v21\.2\.0


Converts the argument to the Date data type. This is a MySQL compatibility alias for `toDate`. It behaves the same as `toDate`.


**Syntax**



```
DATE(expr)

```

**Arguments**


- `expr` — The value to convert. [`String`](/docs/sql-reference/data-types/string) or [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Returns a Date value. [`Date`](/docs/sql-reference/data-types/date)


**Examples**


**Basic usage**



```
SELECT DATE('2023-01-01')

```


```
2023-01-01

```

## accurateCast[​](#accurateCast "Direct link to accurateCast")


Introduced in: v1\.1\.0


Converts a value to a specified data type. Unlike [`CAST`](#CAST), `accurateCast` performs stricter type checking and throws an exception if the conversion would result in a loss of data precision or if the conversion is not possible.


This function is safer than regular `CAST` as it prevents precision loss and invalid conversions.


**Syntax**



```
accurateCast(x, T)

```

**Arguments**


- `x` — A value to convert. [`Any`](/docs/sql-reference/data-types)
- `T` — The target data type name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the converted value with the target data type. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Successful conversion**



```
SELECT accurateCast(42, 'UInt16')

```


```
┌─accurateCast(42, 'UInt16')─┐
│                        42 │
└───────────────────────────┘

```

**String to number**



```
SELECT accurateCast('123.45', 'Float64')

```


```
┌─accurateCast('123.45', 'Float64')─┐
│                            123.45 │
└───────────────────────────────────┘

```

## accurateCastOrDefault[​](#accurateCastOrDefault "Direct link to accurateCastOrDefault")


Introduced in: v21\.1\.0


Converts a value to a specified data type.
Like [`accurateCast`](#accurateCast), but returns a default value instead of throwing an exception if the conversion cannot be performed accurately.


If a default value is provided as the second argument, it must be of the target type.
If no default value is provided, the default value of the target type is used.


**Syntax**



```
accurateCastOrDefault(x, T[, default_value])

```

**Arguments**


- `x` — A value to convert. [`Any`](/docs/sql-reference/data-types)
- `T` — The target data type name. [`const String`](/docs/sql-reference/data-types/string)
- `default_value` — Optional. Default value to return if conversion fails. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the converted value with the target data type, or the default value if conversion is not possible. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Successful conversion**



```
SELECT accurateCastOrDefault(42, 'String')

```


```
┌─accurateCastOrDefault(42, 'String')─┐
│ 42                                  │
└─────────────────────────────────────┘

```

**Failed conversion with explicit default**



```
SELECT accurateCastOrDefault('abc', 'UInt32', 999::UInt32)

```


```
┌─accurateCastOrDefault('abc', 'UInt32', 999)─┐
│                                         999 │
└─────────────────────────────────────────────┘

```

**Failed conversion with implicit default**



```
SELECT accurateCastOrDefault('abc', 'UInt32')

```


```
┌─accurateCastOrDefault('abc', 'UInt32')─┐
│                                      0 │
└────────────────────────────────────────┘

```

## accurateCastOrNull[​](#accurateCastOrNull "Direct link to accurateCastOrNull")


Introduced in: v1\.1\.0


Converts a value to a specified data type.
Like [`accurateCast`](#accurateCast), but returns `NULL` instead of throwing an exception if the conversion cannot be performed accurately.


This function combines the safety of [`accurateCast`](#accurateCast) with graceful error handling.


**Syntax**



```
accurateCastOrNull(x, T)

```

**Arguments**


- `x` — A value to convert. [`Any`](/docs/sql-reference/data-types)
- `T` — The target data type name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the converted value with the target data type, or `NULL` if conversion is not possible. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Successful conversion**



```
SELECT accurateCastOrNull(42, 'String')

```


```
┌─accurateCastOrNull(42, 'String')─┐
│ 42                               │
└──────────────────────────────────┘

```

**Failed conversion returns NULL**



```
SELECT accurateCastOrNull('abc', 'UInt32')

```


```
┌─accurateCastOrNull('abc', 'UInt32')─┐
│                                ᴺᵁᴸᴸ │
└─────────────────────────────────────┘

```

## formatRow[​](#formatRow "Direct link to formatRow")


Introduced in: v20\.7\.0


Converts arbitrary expressions into a string via given format.


NoteIf the format contains a suffix/prefix, it will be written in each row.
Only row\-based formats are supported in this function.


**Syntax**



```
formatRow(format, x, y, ...)

```

**Arguments**


- `format` — Text format. For example, CSV, TSV. [`String`](/docs/sql-reference/data-types/string)
- `x, y, ...` — Expressions. [`Any`](/docs/sql-reference/data-types)


**Returned value**


A formatted string. (for text formats it's usually terminated with the new line character). [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic usage**



```
SELECT formatRow('CSV', number, 'good')
FROM numbers(3)

```


```
┌─formatRow('CSV', number, 'good')─┐
│ 0,"good"
                         │
│ 1,"good"
                         │
│ 2,"good"
                         │
└──────────────────────────────────┘

```

**With custom format**



```
SELECT formatRow('CustomSeparated', number, 'good')
FROM numbers(3)
SETTINGS format_custom_result_before_delimiter='<prefix>\n', format_custom_result_after_delimiter='<suffix>'

```


```
┌─formatRow('CustomSeparated', number, 'good')─┐
│ <prefix>
0    good
<suffix>                   │
│ <prefix>
1    good
<suffix>                   │
│ <prefix>
2    good
<suffix>                   │
└──────────────────────────────────────────────┘

```

## formatRowNoNewline[​](#formatRowNoNewline "Direct link to formatRowNoNewline")


Introduced in: v20\.7\.0


Same as [`formatRow`](#formatRow), but trims the newline character of each row.


Converts arbitrary expressions into a string via given format, but removes any trailing newline characters from the result.


**Syntax**



```
formatRowNoNewline(format, x, y, ...)

```

**Arguments**


- `format` — Text format. For example, CSV, TSV. [`String`](/docs/sql-reference/data-types/string)
- `x, y, ...` — Expressions. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a formatted string with newlines removed. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic usage**



```
SELECT formatRowNoNewline('CSV', number, 'good')
FROM numbers(3)

```


```
┌─formatRowNoNewline('CSV', number, 'good')─┐
│ 0,"good"                                  │
│ 1,"good"                                  │
│ 2,"good"                                  │
└───────────────────────────────────────────┘

```

## fromUnixTimestamp64Micro[​](#fromUnixTimestamp64Micro "Direct link to fromUnixTimestamp64Micro")


Introduced in: v20\.5\.0


Converts a Unix timestamp in microseconds to a `DateTime64` value with microsecond precision.


The input value is treated as a Unix timestamp with microsecond precision (number of microseconds since 1970\-01\-01 00:00:00 UTC).


**Syntax**



```
fromUnixTimestamp64Micro(value[, timezone])

```

**Arguments**


- `value` — Unix timestamp in microseconds. [`Int64`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone for the returned value. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a `DateTime64` value with microsecond precision. [`DateTime64(6)`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT fromUnixTimestamp64Micro(1640995200123456)

```


```
┌─fromUnixTimestamp64Micro(1640995200123456)─┐
│                 2022-01-01 00:00:00.123456 │
└────────────────────────────────────────────┘

```

## fromUnixTimestamp64Milli[​](#fromUnixTimestamp64Milli "Direct link to fromUnixTimestamp64Milli")


Introduced in: v20\.5\.0


Converts a Unix timestamp in milliseconds to a `DateTime64` value with millisecond precision.


The input value is treated as a Unix timestamp with millisecond precision (number of milliseconds since 1970\-01\-01 00:00:00 UTC).


**Syntax**



```
fromUnixTimestamp64Milli(value[, timezone])

```

**Arguments**


- `value` — Unix timestamp in milliseconds. [`Int64`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone for the returned value. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


A `DateTime64` value with millisecond precision. [`DateTime64(3)`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT fromUnixTimestamp64Milli(1640995200123)

```


```
┌─fromUnixTimestamp64Milli(1640995200123)─┐
│                 2022-01-01 00:00:00.123 │
└─────────────────────────────────────────┘

```

## fromUnixTimestamp64Nano[​](#fromUnixTimestamp64Nano "Direct link to fromUnixTimestamp64Nano")


Introduced in: v20\.5\.0


Converts a Unix timestamp in nanoseconds to a [`DateTime64`](/docs/sql-reference/data-types/datetime64) value with nanosecond precision.


The input value is treated as a Unix timestamp with nanosecond precision (number of nanoseconds since 1970\-01\-01 00:00:00 UTC).


NotePlease note that the input value is treated as a UTC timestamp, not the timezone of the input value.


**Syntax**



```
fromUnixTimestamp64Nano(value[, timezone])

```

**Arguments**


- `value` — Unix timestamp in nanoseconds. [`Int64`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone for the returned value. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a `DateTime64` value with nanosecond precision. [`DateTime64(9)`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT fromUnixTimestamp64Nano(1640995200123456789)

```


```
┌─fromUnixTimestamp64Nano(1640995200123456789)─┐
│                2022-01-01 00:00:00.123456789 │
└──────────────────────────────────────────────┘

```

## fromUnixTimestamp64Second[​](#fromUnixTimestamp64Second "Direct link to fromUnixTimestamp64Second")


Introduced in: v24\.12\.0


Converts a Unix timestamp in seconds to a `DateTime64` value with second precision.


The input value is treated as a Unix timestamp with second precision (number of seconds since 1970\-01\-01 00:00:00 UTC).


**Syntax**



```
fromUnixTimestamp64Second(value[, timezone])

```

**Arguments**


- `value` — Unix timestamp in seconds. [`Int64`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone for the returned value. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a `DateTime64` value with second precision. [`DateTime64(0)`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT fromUnixTimestamp64Second(1640995200)

```


```
┌─fromUnixTimestamp64Second(1640995200)─┐
│                   2022-01-01 00:00:00 │
└───────────────────────────────────────┘

```

## parseDateTime[​](#parseDateTime "Direct link to parseDateTime")


Introduced in: v23\.3\.0


Parses a date and time string according to a MySQL date format string.


This function is the inverse of [`formatDateTime`](/docs/sql-reference/functions/date-time-functions).
It parses a String argument using a format String. Returns a DateTime type.


**Syntax**



```
parseDateTime(time_string, format[, timezone])

```

**Aliases**: `TO_UNIXTIME`


**Arguments**


- `time_string` — String to be parsed into DateTime. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a DateTime parsed from the input string according to the MySQL style format string. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTime('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')

```


```
┌─parseDateTime('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')─┐
│                                       2025-01-04 23:00:00 │
└───────────────────────────────────────────────────────────┘

```

## parseDateTime32BestEffort[​](#parseDateTime32BestEffort "Direct link to parseDateTime32BestEffort")


Introduced in: v20\.9\.0


Converts a string representation of a date and time to the [`DateTime`](/docs/sql-reference/data-types/datetime) data type.


The function parses [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601), [RFC 1123 \- 5\.2\.14 RFC\-822 Date and Time Specification](https://tools.ietf.org/html/rfc1123#page-55), ClickHouse's and some other date and time formats.


**Syntax**



```
parseDateTime32BestEffort(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` as a `DateTime`. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTime32BestEffort('23/10/2025 12:12:57')
AS parseDateTime32BestEffort

```


```
┌─parseDateTime32BestEffort─┐
│       2025-10-23 12:12:57 │
└───────────────────────────┘

```

**With timezone**



```
SELECT parseDateTime32BestEffort('Sat, 18 Aug 2025 07:22:16 GMT', 'Asia/Istanbul')
AS parseDateTime32BestEffort

```


```
┌─parseDateTime32BestEffort─┐
│       2025-08-18 10:22:16 │
└───────────────────────────┘

```

**Unix timestamp**



```
SELECT parseDateTime32BestEffort('1284101485')
AS parseDateTime32BestEffort

```


```
┌─parseDateTime32BestEffort─┐
│       2015-07-07 12:04:41 │
└───────────────────────────┘

```

## parseDateTime32BestEffortOrNull[​](#parseDateTime32BestEffortOrNull "Direct link to parseDateTime32BestEffortOrNull")


Introduced in: v20\.9\.0


Same as [`parseDateTime32BestEffort`](#parseDateTime32BestEffort) except that it returns `NULL` when it encounters a date format that cannot be processed.


**Syntax**



```
parseDateTime32BestEffortOrNull(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a `DateTime` object parsed from the string, or `NULL` if the parsing fails. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT
    parseDateTime32BestEffortOrNull('23/10/2025 12:12:57') AS valid,
    parseDateTime32BestEffortOrNull('invalid date') AS invalid

```


```
┌─valid───────────────┬─invalid─┐
│ 2025-10-23 12:12:57 │    ᴺᵁᴸᴸ │
└─────────────────────┴─────────┘

```

## parseDateTime32BestEffortOrZero[​](#parseDateTime32BestEffortOrZero "Direct link to parseDateTime32BestEffortOrZero")


Introduced in: v20\.9\.0


Same as [`parseDateTime32BestEffort`](#parseDateTime32BestEffort) except that it returns a zero date or a zero date time when it encounters a date format that cannot be processed.


**Syntax**



```
parseDateTime32BestEffortOrZero(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a `DateTime` object parsed from the string, or zero date (`1970-01-01 00:00:00`) if the parsing fails. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT
    parseDateTime32BestEffortOrZero('23/10/2025 12:12:57') AS valid,
    parseDateTime32BestEffortOrZero('invalid date') AS invalid

```


```
┌─valid───────────────┬─invalid─────────────┐
│ 2025-10-23 12:12:57 │ 1970-01-01 00:00:00 │
└─────────────────────┴─────────────────────┘

```

## parseDateTime64[​](#parseDateTime64 "Direct link to parseDateTime64")


Introduced in: v24\.11\.0


Parses a date and time string with sub\-second precision according to a MySQL date format string.


This function is the inverse of [`formatDateTime`](/docs/sql-reference/functions/date-time-functions) for DateTime64\.
It parses a String argument using a format String. Returns a DateTime64 type which can represent dates from 1900 to 2299 with sub\-second precision.


**Syntax**



```
parseDateTime64(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime64\. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a DateTime64 parsed from the input string according to the MySQL style format string. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT parseDateTime64('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')

```


```
┌─parseDateTime64('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')─┐
│                                       2025-01-04 23:00:00.123       │
└─────────────────────────────────────────────────────────────────────┘

```

## parseDateTime64BestEffort[​](#parseDateTime64BestEffort "Direct link to parseDateTime64BestEffort")


Introduced in: v20\.1\.0


Same as [`parseDateTimeBestEffort`](#parseDateTimeBestEffort) function but also parse milliseconds and microseconds and returns [`DateTime64`](/docs/sql-reference/data-types/datetime64) data type.


**Syntax**



```
parseDateTime64BestEffort(time_string[, precision[, time_zone]])

```

**Arguments**


- `time_string` — String containing a date or date with time to convert. [`String`](/docs/sql-reference/data-types/string)
- `precision` — Optional. Required precision. `3` for milliseconds, `6` for microseconds. Default: `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. Timezone. The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` converted to the [`DateTime64`](/docs/sql-reference/data-types/datetime64) data type. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT parseDateTime64BestEffort('2025-01-01') AS a, toTypeName(a) AS t
UNION ALL
SELECT parseDateTime64BestEffort('2025-01-01 01:01:00.12346') AS a, toTypeName(a) AS t
UNION ALL
SELECT parseDateTime64BestEffort('2025-01-01 01:01:00.12346',6) AS a, toTypeName(a) AS t
UNION ALL
SELECT parseDateTime64BestEffort('2025-01-01 01:01:00.12346',3,'Asia/Istanbul') AS a, toTypeName(a) AS t
FORMAT PrettyCompactMonoBlock

```


```
┌──────────────────────────a─┬─t──────────────────────────────┐
│ 2025-01-01 01:01:00.123000 │ DateTime64(3)                  │
│ 2025-01-01 00:00:00.000000 │ DateTime64(3)                  │
│ 2025-01-01 01:01:00.123460 │ DateTime64(6)                  │
│ 2025-12-31 22:01:00.123000 │ DateTime64(3, 'Asia/Istanbul') │
└────────────────────────────┴────────────────────────────────┘

```

## parseDateTime64BestEffortOrNull[​](#parseDateTime64BestEffortOrNull "Direct link to parseDateTime64BestEffortOrNull")


Introduced in: v20\.1\.0


Same as [`parseDateTime64BestEffort`](#parseDateTime64BestEffort) except that it returns `NULL` when it encounters a date format that cannot be processed.


**Syntax**



```
parseDateTime64BestEffortOrNull(time_string[, precision[, time_zone]])

```

**Arguments**


- `time_string` — String containing a date or date with time to convert. [`String`](/docs/sql-reference/data-types/string)
- `precision` — Optional. Required precision. `3` for milliseconds, `6` for microseconds. Default: `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. Timezone. The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` converted to [`DateTime64`](/docs/sql-reference/data-types/datetime64), or `NULL` if the input cannot be parsed. [`DateTime64`](/docs/sql-reference/data-types/datetime64) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT parseDateTime64BestEffortOrNull('2025-01-01 01:01:00.123') AS valid,
       parseDateTime64BestEffortOrNull('invalid') AS invalid

```


```
┌─valid───────────────────┬─invalid─┐
│ 2025-01-01 01:01:00.123 │    ᴺᵁᴸᴸ │
└─────────────────────────┴─────────┘

```

## parseDateTime64BestEffortOrZero[​](#parseDateTime64BestEffortOrZero "Direct link to parseDateTime64BestEffortOrZero")


Introduced in: v20\.1\.0


Same as [`parseDateTime64BestEffort`](#parseDateTime64BestEffort) except that it returns zero date or zero date time when it encounters a date format that cannot be processed.


**Syntax**



```
parseDateTime64BestEffortOrZero(time_string[, precision[, time_zone]])

```

**Arguments**


- `time_string` — String containing a date or date with time to convert. [`String`](/docs/sql-reference/data-types/string)
- `precision` — Optional. Required precision. `3` for milliseconds, `6` for microseconds. Default: `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. Timezone. The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` converted to [`DateTime64`](/docs/sql-reference/data-types/datetime64), or zero date/datetime (`1970-01-01 00:00:00.000`) if the input cannot be parsed. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT parseDateTime64BestEffortOrZero('2025-01-01 01:01:00.123') AS valid,
       parseDateTime64BestEffortOrZero('invalid') AS invalid

```


```
┌─valid───────────────────┬─invalid─────────────────┐
│ 2025-01-01 01:01:00.123 │ 1970-01-01 00:00:00.000 │
└─────────────────────────┴─────────────────────────┘

```

## parseDateTime64BestEffortUS[​](#parseDateTime64BestEffortUS "Direct link to parseDateTime64BestEffortUS")


Introduced in: v22\.8\.0


Same as [`parseDateTime64BestEffort`](#parseDateTime64BestEffort), except that this function prefers US date format (`MM/DD/YYYY` etc.) in case of ambiguity.


**Syntax**



```
parseDateTime64BestEffortUS(time_string [, precision [, time_zone]])

```

**Arguments**


- `time_string` — String containing a date or date with time to convert. [`String`](/docs/sql-reference/data-types/string)
- `precision` — Optional. Required precision. `3` for milliseconds, `6` for microseconds. Default: `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. Timezone. The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` converted to [`DateTime64`](/docs/sql-reference/data-types/datetime64) using US date format preference for ambiguous cases. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT parseDateTime64BestEffortUS('02/10/2025 12:30:45.123') AS us_format,
       parseDateTime64BestEffortUS('15/08/2025 10:15:30.456') AS fallback_to_standard

```


```
┌─us_format───────────────┬─fallback_to_standard────┐
│ 2025-02-10 12:30:45.123 │ 2025-08-15 10:15:30.456 │
└─────────────────────────┴─────────────────────────┘

```

## parseDateTime64BestEffortUSOrNull[​](#parseDateTime64BestEffortUSOrNull "Direct link to parseDateTime64BestEffortUSOrNull")


Introduced in: v22\.8\.0


Same as [`parseDateTime64BestEffort`](#parseDateTime64BestEffort), except that this function prefers US date format (`MM/DD/YYYY` etc.) in case of ambiguity and returns `NULL` when it encounters a date format that cannot be processed.


**Syntax**



```
parseDateTime64BestEffortUSOrNull(time_string[, precision[, time_zone]])

```

**Arguments**


- `time_string` — String containing a date or date with time to convert. [`String`](/docs/sql-reference/data-types/string)
- `precision` — Optional. Required precision. `3` for milliseconds, `6` for microseconds. Default: `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. Timezone. The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` converted to [`DateTime64`](/docs/sql-reference/data-types/datetime64) using US format preference, or `NULL` if the input cannot be parsed. [`DateTime64`](/docs/sql-reference/data-types/datetime64) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT parseDateTime64BestEffortUSOrNull('02/10/2025 12:30:45.123') AS valid_us,
       parseDateTime64BestEffortUSOrNull('invalid') AS invalid

```


```
┌─valid_us────────────────┬─invalid─┐
│ 2025-02-10 12:30:45.123 │    ᴺᵁᴸᴸ │
└─────────────────────────┴─────────┘

```

## parseDateTime64BestEffortUSOrZero[​](#parseDateTime64BestEffortUSOrZero "Direct link to parseDateTime64BestEffortUSOrZero")


Introduced in: v22\.8\.0


Same as [`parseDateTime64BestEffort`](#parseDateTime64BestEffort), except that this function prefers US date format (`MM/DD/YYYY` etc.) in case of ambiguity and returns zero date or zero date time when it encounters a date format that cannot be processed.


**Syntax**



```
parseDateTime64BestEffortUSOrZero(time_string [, precision [, time_zone]])

```

**Arguments**


- `time_string` — String containing a date or date with time to convert. [`String`](/docs/sql-reference/data-types/string)
- `precision` — Optional. Required precision. `3` for milliseconds, `6` for microseconds. Default: `3`. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. Timezone. The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` converted to [`DateTime64`](/docs/sql-reference/data-types/datetime64) using US format preference, or zero date/datetime (`1970-01-01 00:00:00.000`) if the input cannot be parsed. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT parseDateTime64BestEffortUSOrZero('02/10/2025 12:30:45.123') AS valid_us,
       parseDateTime64BestEffortUSOrZero('invalid') AS invalid

```


```
┌─valid_us────────────────┬─invalid─────────────────┐
│ 2025-02-10 12:30:45.123 │ 1970-01-01 00:00:00.000 │
└─────────────────────────┴─────────────────────────┘

```

## parseDateTime64InJodaSyntax[​](#parseDateTime64InJodaSyntax "Direct link to parseDateTime64InJodaSyntax")


Introduced in: v24\.10\.0


Parses a date and time string with sub\-second precision according to a Joda date format string.


This function is the inverse of [`formatDateTimeInJodaSyntax`](/docs/sql-reference/functions/date-time-functions#formatDateTimeInJodaSyntax) for DateTime64\.
It parses a String argument using a Joda\-style format String. Returns a DateTime64 type which can represent dates from 1900 to 2299 with sub\-second precision.


Refer to [Joda Time documentation](https://joda-time.sourceforge.net/apidocs/org/joda/time/format/DateTimeFormat.html) for the format patterns.


**Syntax**



```
parseDateTime64InJodaSyntax(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime64\. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string in Joda syntax specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a DateTime64 parsed from the input string according to the Joda style format string. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT parseDateTime64InJodaSyntax('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')

```


```
┌─parseDateTime64InJodaSyntax('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')─┐
│                                                          2025-01-04 23:00:00.123   │
└────────────────────────────────────────────────────────────────────────────────────┘

```

## parseDateTime64InJodaSyntaxOrNull[​](#parseDateTime64InJodaSyntaxOrNull "Direct link to parseDateTime64InJodaSyntaxOrNull")


Introduced in: v24\.10\.0


Same as [`parseDateTime64InJodaSyntax`](#parseDateTime64InJodaSyntax) but returns `NULL` when it encounters an unparsable date format.


**Syntax**



```
parseDateTime64InJodaSyntaxOrNull(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime64\. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string in Joda syntax specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns DateTime64 parsed from input string, or NULL if parsing fails. [`Nullable(DateTime64)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Usage example**



```
SELECT parseDateTime64InJodaSyntaxOrNull('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')

```


```
┌─parseDateTime64InJodaSyntaxOrNull('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')─┐
│                                                             2025-01-04 23:00:00.123      │
└──────────────────────────────────────────────────────────────────────────────────────────┘

```

## parseDateTime64InJodaSyntaxOrZero[​](#parseDateTime64InJodaSyntaxOrZero "Direct link to parseDateTime64InJodaSyntaxOrZero")


Introduced in: v24\.10\.0


Same as [`parseDateTime64InJodaSyntax`](#parseDateTime64InJodaSyntax) but returns zero date when it encounters an unparsable date format.


**Syntax**



```
parseDateTime64InJodaSyntaxOrZero(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime64\. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string in Joda syntax specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns DateTime64 parsed from input string, or zero DateTime64 if parsing fails. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT parseDateTime64InJodaSyntaxOrZero('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')

```


```
┌─parseDateTime64InJodaSyntaxOrZero('2025-01-04 23:00:00.123', 'yyyy-MM-dd HH:mm:ss.SSS')─┐
│                                                              2025-01-04 23:00:00.123     │
└──────────────────────────────────────────────────────────────────────────────────────────┘

```

## parseDateTime64OrNull[​](#parseDateTime64OrNull "Direct link to parseDateTime64OrNull")


Introduced in: v24\.11\.0


Same as [`parseDateTime64`](#parseDateTime64) but returns `NULL` when it encounters an unparsable date format.


**Syntax**



```
parseDateTime64OrNull(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime64\. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns DateTime64 parsed from input string, or NULL if parsing fails. [`Nullable(DateTime64)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Usage example**



```
SELECT parseDateTime64OrNull('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')

```


```
┌─parseDateTime64OrNull('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')─┐
│                                            2025-01-04 23:00:00.123        │
└───────────────────────────────────────────────────────────────────────────┘

```

## parseDateTime64OrZero[​](#parseDateTime64OrZero "Direct link to parseDateTime64OrZero")


Introduced in: v24\.11\.0


Same as [`parseDateTime64`](#parseDateTime64) but returns zero date when it encounters an unparsable date format.


**Syntax**



```
parseDateTime64OrZero(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime64\. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns DateTime64 parsed from input string, or zero DateTime64 if parsing fails. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT parseDateTime64OrZero('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')

```


```
┌─parseDateTime64OrZero('2025-01-04 23:00:00.123', '%Y-%m-%d %H:%i:%s.%f')─┐
│                                             2025-01-04 23:00:00.123       │
└───────────────────────────────────────────────────────────────────────────┘

```

## parseDateTimeBestEffort[​](#parseDateTimeBestEffort "Direct link to parseDateTimeBestEffort")


Introduced in: v1\.1\.0


Converts a date and time in the String representation to DateTime data type.
The function parses [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html), [RFC 1123 \- 5\.2\.14 RFC\-822](https://datatracker.ietf.org/doc/html/rfc822) Date and Time Specification, ClickHouse's and some other date and time formats.


Supported non\-standard formats:


- A string containing 9\..10 digit unix timestamp.
- A string with a date and a time component: `YYYYMMDDhhmmss`, `DD/MM/YYYY hh:mm:ss`, `DD-MM-YY hh:mm`, `YYYY-MM-DD hh:mm:ss`, etc.
- A string with a date, but no time component: `YYYY`, `YYYYMM`, `YYYY*MM`, `DD/MM/YYYY`, `DD-MM-YY` etc.
- A string with a day and time: `DD`, `DD hh`, `DD hh:mm`. In this case `MM` is substituted by `01`.
- A string that includes the date and time along with time zone offset information: `YYYY-MM-DD hh:mm:ss ±h:mm`, etc.
- A syslog timestamp: `Mmm dd hh:mm:ss`. For example, `Jun 9 14:20:32`.


For all of the formats with separator the function parses months names expressed by their full name or by the first three letters of a month name.
If the year is not specified, it is considered to be equal to the current year.


**Syntax**



```
parseDateTimeBestEffort(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` as a `DateTime`. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTimeBestEffort('23/10/2025 12:12:57') AS parseDateTimeBestEffort

```


```
┌─parseDateTimeBestEffort─┐
│     2025-10-23 12:12:57 │
└─────────────────────────┘

```

**With timezone**



```
SELECT parseDateTimeBestEffort('Sat, 18 Aug 2025 07:22:16 GMT', 'Asia/Istanbul') AS parseDateTimeBestEffort

```


```
┌─parseDateTimeBestEffort─┐
│     2025-08-18 10:22:16 │
└─────────────────────────┘

```

**Unix timestamp**



```
SELECT parseDateTimeBestEffort('1735689600') AS parseDateTimeBestEffort

```


```
┌─parseDateTimeBestEffort─┐
│     2025-01-01 00:00:00 │
└─────────────────────────┘

```

## parseDateTimeBestEffortOrNull[​](#parseDateTimeBestEffortOrNull "Direct link to parseDateTimeBestEffortOrNull")


Introduced in: v1\.1\.0


The same as [`parseDateTimeBestEffort`](#parseDateTimeBestEffort) except that it returns `NULL` when it encounters a date format that cannot be processed.
The function parses [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601), [RFC 1123 \- 5\.2\.14 RFC\-822 Date and Time Specification](https://tools.ietf.org/html/rfc1123#page-55), ClickHouse's and some other date and time formats.


Supported non\-standard formats:


- A string containing 9\..10 digit unix timestamp.
- A string with a date and a time component: `YYYYMMDDhhmmss`, `DD/MM/YYYY hh:mm:ss`, `DD-MM-YY hh:mm`, `YYYY-MM-DD hh:mm:ss`, etc.
- A string with a date, but no time component: `YYYY`, `YYYYMM`, `YYYY*MM`, `DD/MM/YYYY`, `DD-MM-YY` etc.
- A string with a day and time: `DD`, `DD hh`, `DD hh:mm`. In this case `MM` is substituted by `01`.
- A string that includes the date and time along with time zone offset information: `YYYY-MM-DD hh:mm:ss ±h:mm`, etc.
- A syslog timestamp: `Mmm dd hh:mm:ss`. For example, `Jun 9 14:20:32`.


For all of the formats with separator the function parses months names expressed by their full name or by the first three letters of a month name.
If the year is not specified, it is considered to be equal to the current year.


**Syntax**



```
parseDateTimeBestEffortOrNull(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` as a DateTime, or `NULL` if the input cannot be parsed. [`DateTime`](/docs/sql-reference/data-types/datetime) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT parseDateTimeBestEffortOrNull('23/10/2025 12:12:57') AS valid,
       parseDateTimeBestEffortOrNull('invalid') AS invalid

```


```
┌─valid───────────────┬─invalid─┐
│ 2025-10-23 12:12:57 │    ᴺᵁᴸᴸ │
└─────────────────────┴─────────┘

```

## parseDateTimeBestEffortOrZero[​](#parseDateTimeBestEffortOrZero "Direct link to parseDateTimeBestEffortOrZero")


Introduced in: v1\.1\.0


Same as [`parseDateTimeBestEffort`](#parseDateTimeBestEffort) except that it returns a zero date or a zero date time when it encounters a date format that cannot be processed.
The function parses [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601), [RFC 1123 \- 5\.2\.14 RFC\-822 Date and Time Specification](https://tools.ietf.org/html/rfc1123#page-55), ClickHouse's and some other date and time formats.


Supported non\-standard formats:


- A string containing 9\..10 digit unix timestamp.
- A string with a date and a time component: `YYYYMMDDhhmmss`, `DD/MM/YYYY hh:mm:ss`, `DD-MM-YY hh:mm`, `YYYY-MM-DD hh:mm:ss`, etc.
- A string with a date, but no time component: `YYYY`, `YYYYMM`, `YYYY*MM`, `DD/MM/YYYY`, `DD-MM-YY` etc.
- A string with a day and time: `DD`, `DD hh`, `DD hh:mm`. In this case `MM` is substituted by `01`.
- A string that includes the date and time along with time zone offset information: `YYYY-MM-DD hh:mm:ss ±h:mm`, etc.
- A syslog timestamp: `Mmm dd hh:mm:ss`. For example, `Jun 9 14:20:32`.


For all of the formats with separator the function parses months names expressed by their full name or by the first three letters of a month name.
If the year is not specified, it is considered to be equal to the current year.


**Syntax**



```
parseDateTimeBestEffortOrZero(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` as a `DateTime`, or zero date/datetime (`1970-01-01` or `1970-01-01 00:00:00`) if the input cannot be parsed. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTimeBestEffortOrZero('23/10/2025 12:12:57') AS valid,
       parseDateTimeBestEffortOrZero('invalid') AS invalid

```


```
┌─valid───────────────┬─invalid─────────────┐
│ 2025-10-23 12:12:57 │ 1970-01-01 00:00:00 │
└─────────────────────┴─────────────────────┘

```

## parseDateTimeBestEffortUS[​](#parseDateTimeBestEffortUS "Direct link to parseDateTimeBestEffortUS")


Introduced in: v1\.1\.0


This function behaves like [`parseDateTimeBestEffort`](#parseDateTimeBestEffort) for ISO date formats, e.g. `YYYY-MM-DD hh:mm:ss`, and other date formats where the month and date components can be unambiguously extracted, e.g. `YYYYMMDDhhmmss`, `YYYY-MM`, `DD hh`, or `YYYY-MM-DD hh:mm:ss ±h:mm`.
If the month and the date components cannot be unambiguously extracted, e.g. `MM/DD/YYYY`, `MM-DD-YYYY`, or `MM-DD-YY`, it prefers the US date format instead of `DD/MM/YYYY`, `DD-MM-YYYY`, or `DD-MM-YY`.
As an exception to the previous statement, if the month is bigger than 12 and smaller or equal than 31, this function falls back to the behavior of [`parseDateTimeBestEffort`](#parseDateTimeBestEffort), e.g. `15/08/2020` is parsed as `2020-08-15`.


**Syntax**



```
parseDateTimeBestEffortUS(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` as a `DateTime` using US date format preference for ambiguous cases. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTimeBestEffortUS('02/10/2025') AS us_format,
       parseDateTimeBestEffortUS('15/08/2025') AS fallback_to_standard

```


```
┌─us_format───────────┬─fallback_to_standard─┐
│ 2025-02-10 00:00:00 │  2025-08-15 00:00:00 │
└─────────────────────┴──────────────────────┘

```

## parseDateTimeBestEffortUSOrNull[​](#parseDateTimeBestEffortUSOrNull "Direct link to parseDateTimeBestEffortUSOrNull")


Introduced in: v1\.1\.0


Same as [`parseDateTimeBestEffortUS`](#parseDateTimeBestEffortUS) function except that it returns `NULL` when it encounters a date format that cannot be processed.


This function behaves like [`parseDateTimeBestEffort`](#parseDateTimeBestEffort) for ISO date formats, but prefers the US date format for ambiguous cases, with `NULL` return on parsing errors.


**Syntax**



```
parseDateTimeBestEffortUSOrNull(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` as a DateTime using US format preference, or `NULL` if the input cannot be parsed. [`DateTime`](/docs/sql-reference/data-types/datetime) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT parseDateTimeBestEffortUSOrNull('02/10/2025') AS valid_us,
       parseDateTimeBestEffortUSOrNull('invalid') AS invalid

```


```
┌─valid_us────────────┬─invalid─┐
│ 2025-02-10 00:00:00 │    ᴺᵁᴸᴸ │
└─────────────────────┴─────────┘

```

## parseDateTimeBestEffortUSOrZero[​](#parseDateTimeBestEffortUSOrZero "Direct link to parseDateTimeBestEffortUSOrZero")


Introduced in: v1\.1\.0


Same as [`parseDateTimeBestEffortUS`](#parseDateTimeBestEffortUS) function except that it returns zero date (`1970-01-01`) or zero date with time (`1970-01-01 00:00:00`) when it encounters a date format that cannot be processed.


This function behaves like [`parseDateTimeBestEffort`](#parseDateTimeBestEffort) for ISO date formats, but prefers the US date format for ambiguous cases, with zero return on parsing errors.


**Syntax**



```
parseDateTimeBestEffortUSOrZero(time_string[, time_zone])

```

**Arguments**


- `time_string` — String containing a date and time to convert. [`String`](/docs/sql-reference/data-types/string)
- `time_zone` — Optional. Time zone according to which `time_string` is parsed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `time_string` as a `DateTime` using US format preference, or zero date/datetime (`1970-01-01` or `1970-01-01 00:00:00`) if the input cannot be parsed. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTimeBestEffortUSOrZero('02/10/2025') AS valid_us,
       parseDateTimeBestEffortUSOrZero('invalid') AS invalid

```


```
┌─valid_us────────────┬─invalid─────────────┐
│ 2025-02-10 00:00:00 │ 1970-01-01 00:00:00 │
└─────────────────────┴─────────────────────┘

```

## parseDateTimeInJodaSyntax[​](#parseDateTimeInJodaSyntax "Direct link to parseDateTimeInJodaSyntax")


Introduced in: v23\.3\.0


Parses a date and time string according to a Joda date format string.


This function is the inverse of [`formatDateTimeInJodaSyntax`](/docs/sql-reference/functions/date-time-functions#formatDateTimeInJodaSyntax).
It parses a String argument using a Joda\-style format String. Returns a DateTime type.


Refer to [Joda Time documentation](https://joda-time.sourceforge.net/apidocs/org/joda/time/format/DateTimeFormat.html) for the format patterns.


**Syntax**



```
parseDateTimeInJodaSyntax(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string in Joda syntax specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a DateTime parsed from the input string according to the Joda style format string. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTimeInJodaSyntax('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')

```


```
┌─parseDateTimeInJodaSyntax('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')─┐
│                                                      2025-01-04 23:00:00 │
└──────────────────────────────────────────────────────────────────────────┘

```

## parseDateTimeInJodaSyntaxOrNull[​](#parseDateTimeInJodaSyntaxOrNull "Direct link to parseDateTimeInJodaSyntaxOrNull")


Introduced in: v23\.3\.0


Same as [`parseDateTimeInJodaSyntax`](#parseDateTimeInJodaSyntax) but returns `NULL` when it encounters an unparsable date format.


**Syntax**



```
parseDateTimeInJodaSyntaxOrNull(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string in Joda syntax specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns DateTime parsed from input string, or NULL if parsing fails. [`Nullable(DateTime)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Usage example**



```
SELECT parseDateTimeInJodaSyntaxOrNull('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')

```


```
┌─parseDateTimeInJodaSyntaxOrNull('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')─┐
│                                                         2025-01-04 23:00:00    │
└────────────────────────────────────────────────────────────────────────────────┘

```

## parseDateTimeInJodaSyntaxOrZero[​](#parseDateTimeInJodaSyntaxOrZero "Direct link to parseDateTimeInJodaSyntaxOrZero")


Introduced in: v23\.3\.0


Same as [`parseDateTimeInJodaSyntax`](#parseDateTimeInJodaSyntax) but returns zero date when it encounters an unparsable date format.


**Syntax**



```
parseDateTimeInJodaSyntaxOrZero(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string in Joda syntax specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns DateTime parsed from input string, or zero DateTime if parsing fails. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTimeInJodaSyntaxOrZero('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')

```


```
┌─parseDateTimeInJodaSyntaxOrZero('2025-01-04 23:00:00', 'yyyy-MM-dd HH:mm:ss')─┐
│                                                          2025-01-04 23:00:00   │
└────────────────────────────────────────────────────────────────────────────────┘

```

## parseDateTimeOrNull[​](#parseDateTimeOrNull "Direct link to parseDateTimeOrNull")


Introduced in: v23\.3\.0


Same as [`parseDateTime`](#parseDateTime) but returns `NULL` when it encounters an unparsable date format.


**Syntax**



```
parseDateTimeOrNull(time_string, format[, timezone])

```

**Aliases**: `str_to_date`


**Arguments**


- `time_string` — String to be parsed into DateTime. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns DateTime parsed from input string, or NULL if parsing fails. [`Nullable(DateTime)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Usage example**



```
SELECT parseDateTimeOrNull('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')

```


```
┌─parseDateTimeOrNull('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')─┐
│                                            2025-01-04 23:00:00  │
└─────────────────────────────────────────────────────────────────┘

```

## parseDateTimeOrZero[​](#parseDateTimeOrZero "Direct link to parseDateTimeOrZero")


Introduced in: v23\.3\.0


Same as [`parseDateTime`](#parseDateTime) but returns zero date when it encounters an unparsable date format.


**Syntax**



```
parseDateTimeOrZero(time_string, format[, timezone])

```

**Arguments**


- `time_string` — String to be parsed into DateTime. [`String`](/docs/sql-reference/data-types/string)
- `format` — Format string specifying how to parse time\_string. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. Timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns DateTime parsed from input string, or zero DateTime if parsing fails. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT parseDateTimeOrZero('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')

```


```
┌─parseDateTimeOrZero('2025-01-04+23:00:00', '%Y-%m-%d+%H:%i:%s')─┐
│                                             2025-01-04 23:00:00 │
└─────────────────────────────────────────────────────────────────┘

```

## reinterpret[​](#reinterpret "Direct link to reinterpret")


Introduced in: v1\.1\.0


Uses the same source in\-memory bytes sequence for the provided value `x` and reinterprets it to the destination type.


**Syntax**



```
reinterpret(x, type)

```

**Arguments**


- `x` — Any type. [`Any`](/docs/sql-reference/data-types)
- `type` — Destination type. If it is an array, then the array element type must be a fixed length type. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Destination type value. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Usage example**



```
SELECT reinterpret(toInt8(-1), 'UInt8') AS int_to_uint,
    reinterpret(toInt8(1), 'Float32') AS int_to_float,
    reinterpret('1', 'UInt32') AS string_to_int

```


```
┌─int_to_uint─┬─int_to_float─┬─string_to_int─┐
│         255 │        1e-45 │            49 │
└─────────────┴──────────────┴───────────────┘

```

**Array example**



```
SELECT reinterpret(x'3108b4403108d4403108b4403108d440', 'Array(Float32)') AS string_to_array_of_Float32

```


```
┌─string_to_array_of_Float32─┐
│ [5.626,6.626,5.626,6.626]  │
└────────────────────────────┘

```

## reinterpretAsDate[​](#reinterpretAsDate "Direct link to reinterpretAsDate")


Introduced in: v1\.1\.0


Reinterprets the input value as a Date value (assuming little endian order) which is the number of days since the beginning of the Unix epoch 1970\-01\-01


**Syntax**



```
reinterpretAsDate(x)

```

**Arguments**


- `x` — Number of days since the beginning of the Unix Epoch. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Date. [`Date`](/docs/sql-reference/data-types/date)


**Examples**


**Usage example**



```
SELECT reinterpretAsDate(65), reinterpretAsDate('A')

```


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


- `x` — Value to reinterpret as Float64\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT reinterpretAsUInt64(toFloat64(0.2)) AS x, reinterpretAsFloat64(x)

```


```
┌───────────────────x─┬─reinterpretAsFloat64(x)─┐
│ 4596373779694328218 │                     0.2 │
└─────────────────────┴─────────────────────────┘

```

## reinterpretAsInt128[​](#reinterpretAsInt128 "Direct link to reinterpretAsInt128")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type Int128\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsInt128(x)

```

**Arguments**


- `x` — Value to reinterpret as Int128\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`Int128`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt64(257) AS x,
    toTypeName(x),
    reinterpretAsInt128(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ Int64         │ 257 │ Int128          │
└─────┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsInt16[​](#reinterpretAsInt16 "Direct link to reinterpretAsInt16")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type Int16\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsInt16(x)

```

**Arguments**


- `x` — Value to reinterpret as Int16\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`Int16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt8(257) AS x,
    toTypeName(x),
    reinterpretAsInt16(x) AS res,
    toTypeName(res)

```


```
┌─x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 1 │ Int8          │   1 │ Int16           │
└───┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsInt256[​](#reinterpretAsInt256 "Direct link to reinterpretAsInt256")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type Int256\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsInt256(x)

```

**Arguments**


- `x` — Value to reinterpret as Int256\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`Int256`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt128(257) AS x,
    toTypeName(x),
    reinterpretAsInt256(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ Int128        │ 257 │ Int256          │
└─────┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsInt32[​](#reinterpretAsInt32 "Direct link to reinterpretAsInt32")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type Int32\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsInt32(x)

```

**Arguments**


- `x` — Value to reinterpret as Int32\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt16(257) AS x,
    toTypeName(x),
    reinterpretAsInt32(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ Int16         │ 257 │ Int32           │
└─────┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsInt64[​](#reinterpretAsInt64 "Direct link to reinterpretAsInt64")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type Int64\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsInt64(x)

```

**Arguments**


- `x` — Value to reinterpret as Int64\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt32(257) AS x,
    toTypeName(x),
    reinterpretAsInt64(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ Int32         │ 257 │ Int64           │
└─────┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsInt8[​](#reinterpretAsInt8 "Direct link to reinterpretAsInt8")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type Int8\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsInt8(x)

```

**Arguments**


- `x` — Value to reinterpret as Int8\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`Int8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt8(257) AS x,
    toTypeName(x),
    reinterpretAsInt8(x) AS res,
    toTypeName(res)

```


```
┌─x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 1 │ UInt8         │   1 │ Int8            │
└───┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsString[​](#reinterpretAsString "Direct link to reinterpretAsString")


Introduced in: v1\.1\.0


Reinterprets the input value as a string (assuming little endian order).
Null bytes at the end are ignored, for example, the function returns for UInt32 value 255 a string with a single character.


**Syntax**



```
reinterpretAsString(x)

```

**Arguments**


- `x` — Value to reinterpret to string. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


String containing bytes representing `x`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    reinterpretAsString(toDateTime('1970-01-01 01:01:05')),
    reinterpretAsString(toDate('1970-03-07'))

```


```
┌─reinterpretAsString(toDateTime('1970-01-01 01:01:05'))─┬─reinterpretAsString(toDate('1970-03-07'))─┐
│ A                                                      │ A                                         │
└────────────────────────────────────────────────────────┴───────────────────────────────────────────┘

```

## reinterpretAsUInt128[​](#reinterpretAsUInt128 "Direct link to reinterpretAsUInt128")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type UInt128\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsUInt128(x)

```

**Arguments**


- `x` — Value to reinterpret as UInt128\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`UInt128`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt64(257) AS x,
    toTypeName(x),
    reinterpretAsUInt128(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ UInt64        │ 257 │ UInt128         │
└─────┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsUInt16[​](#reinterpretAsUInt16 "Direct link to reinterpretAsUInt16")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type UInt16\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsUInt16(x)

```

**Arguments**


- `x` — Value to reinterpret as UInt16\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt8(257) AS x,
    toTypeName(x),
    reinterpretAsUInt16(x) AS res,
    toTypeName(res)

```


```
┌─x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 1 │ UInt8         │   1 │ UInt16          │
└───┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsUInt256[​](#reinterpretAsUInt256 "Direct link to reinterpretAsUInt256")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type UInt256\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsUInt256(x)

```

**Arguments**


- `x` — Value to reinterpret as UInt256\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`UInt256`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt128(257) AS x,
    toTypeName(x),
    reinterpretAsUInt256(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ UInt128       │ 257 │ UInt256         │
└─────┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsUInt32[​](#reinterpretAsUInt32 "Direct link to reinterpretAsUInt32")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type UInt32\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsUInt32(x)

```

**Arguments**


- `x` — Value to reinterpret as UInt32\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt16(257) AS x,
    toTypeName(x),
    reinterpretAsUInt32(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ UInt16        │ 257 │ UInt32          │
└─────┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsUInt64[​](#reinterpretAsUInt64 "Direct link to reinterpretAsUInt64")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type UInt64\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsUInt64(x)

```

**Arguments**


- `x` — Value to reinterpret as UInt64\. [`Int*`](/docs/sql-reference/data-types/int-uint) or [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value of `x`. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt32(257) AS x,
    toTypeName(x),
    reinterpretAsUInt64(x) AS res,
    toTypeName(res)

```


```
┌───x─┬─toTypeName(x)─┬─res─┬─toTypeName(res)─┐
│ 257 │ UInt32        │ 257 │ UInt64          │
└─────┴───────────────┴─────┴─────────────────┘

```

## reinterpretAsUInt8[​](#reinterpretAsUInt8 "Direct link to reinterpretAsUInt8")


Introduced in: v1\.1\.0


Reinterprets the input value as a value of type UInt8\.
Unlike [`CAST`](#CAST), the function does not attempt to preserve the original value \- if the target type is not able to represent the input type, the output is undefined.


**Syntax**



```
reinterpretAsUInt8(x)

```

**Arguments**


- `x` — Value to reinterpret as UInt8\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UUID`](/docs/sql-reference/data-types/uuid) or [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the reinterpreted value `x`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt8(-1) AS val,
    toTypeName(val),
    reinterpretAsUInt8(val) AS res,
    toTypeName(res);

```


```
┌─val─┬─toTypeName(val)─┬─res─┬─toTypeName(res)─┐
│  -1 │ Int8            │ 255 │ UInt8           │
└─────┴─────────────────┴─────┴─────────────────┘

```

## reinterpretAsUUID[​](#reinterpretAsUUID "Direct link to reinterpretAsUUID")


Introduced in: v1\.1\.0


Accepts a 16 byte string and returns a UUID by interpreting each 8\-byte half in little\-endian byte order. If the string isn't long enough, the function works as if the string is padded with the necessary number of null bytes to the end. If the string is longer than 16 bytes, the extra bytes at the end are ignored.


**Syntax**



```
reinterpretAsUUID(fixed_string)

```

**Arguments**


- `fixed_string` — Big\-endian byte string. [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


The UUID type value. [`UUID`](/docs/sql-reference/data-types/uuid)


**Examples**


**String to UUID**



```
SELECT reinterpretAsUUID(reverse(unhex('000102030405060708090a0b0c0d0e0f')))

```


```
┌─reinterpretAsUUID(reverse(unhex('000102030405060708090a0b0c0d0e0f')))─┐
│                                  08090a0b-0c0d-0e0f-0001-020304050607 │
└───────────────────────────────────────────────────────────────────────┘

```

## toBFloat16[​](#toBFloat16 "Direct link to toBFloat16")


Introduced in: v1\.1\.0


Converts an input value to a value of type BFloat16\.
Throws an exception in case of an error.


See also:


- [`toBFloat16OrZero`](#toBFloat16OrZero).
- [`toBFloat16OrNull`](#toBFloat16OrNull).


**Syntax**



```
toBFloat16(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 16\-bit brain\-float value. [`BFloat16`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT
toBFloat16(toFloat32(42.7)),
toBFloat16(toFloat32('42.7')),
toBFloat16('42.7')
FORMAT Vertical;

```


```
toBFloat16(toFloat32(42.7)): 42.5
toBFloat16(t⋯32('42.7')):    42.5
toBFloat16('42.7'):          42.5

```

## toBFloat16OrNull[​](#toBFloat16OrNull "Direct link to toBFloat16OrNull")


Introduced in: v1\.1\.0


Converts a String input value to a value of type BFloat16\.
If the string does not represent a floating point value, the function returns NULL.


Supported arguments:


- String representations of numeric values.


Unsupported arguments (return `NULL`):


- String representations of binary and hexadecimal values.
- Numeric values.


NoteThe function allows a silent loss of precision while converting from the string representation.


See also:


- [`toBFloat16`](#toBFloat16).
- [`toBFloat16OrZero`](#toBFloat16OrZero).


**Syntax**



```
toBFloat16OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Reurns a 16\-bit brain\-float value, otherwise `NULL`. [`BFloat16`](/docs/sql-reference/data-types/float) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toBFloat16OrNull('0x5E'), -- unsupported arguments
       toBFloat16OrNull('12.3'), -- typical use
       toBFloat16OrNull('12.3456789') -- silent loss of precision

```


```
\N
12.25
12.3125

```

## toBFloat16OrZero[​](#toBFloat16OrZero "Direct link to toBFloat16OrZero")


Introduced in: v1\.1\.0


Converts a String input value to a value of type BFloat16\.
If the string does not represent a floating point value, the function returns zero.


Supported arguments:


- String representations of numeric values.


Unsupported arguments (return `0`):


- String representations of binary and hexadecimal values.
- Numeric values.


NoteThe function allows a silent loss of precision while converting from the string representation.


See also:


- [`toBFloat16`](#toBFloat16).
- [`toBFloat16OrNull`](#toBFloat16OrNull).


**Syntax**



```
toBFloat16OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a 16\-bit brain\-float value, otherwise `0`. [`BFloat16`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT toBFloat16OrZero('0x5E'), -- unsupported arguments
       toBFloat16OrZero('12.3'), -- typical use
       toBFloat16OrZero('12.3456789') -- silent loss of precision

```


```
0
12.25
12.3125

```

## toBool[​](#toBool "Direct link to toBool")


Introduced in: v22\.2\.0


Converts an input value to a value of type Bool.


**Syntax**



```
toBool(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string. For strings, accepts 'true' or 'false' (case\-insensitive). [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string) or [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns `true` or `false` based on evaluation of the argument. [`Bool`](/docs/sql-reference/data-types/boolean)


**Examples**


**Usage example**



```
SELECT
    toBool(toUInt8(1)),
    toBool(toInt8(-1)),
    toBool(toFloat32(1.01)),
    toBool('true'),
    toBool('false'),
    toBool('FALSE')
FORMAT Vertical

```


```
toBool(toUInt8(1)):      true
toBool(toInt8(-1)):      true
toBool(toFloat32(1.01)): true
toBool('true'):          true
toBool('false'):         false
toBool('FALSE'):         false

```

## toDate[​](#toDate "Direct link to toDate")


Introduced in: v1\.1\.0


Converts an input value to type [`Date`](/docs/sql-reference/data-types/date).
Supports conversion from String, FixedString, DateTime, or numeric types.


**Syntax**



```
toDate(x)

```

**Arguments**


- `x` — Input value to convert. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the converted input value. [`Date`](/docs/sql-reference/data-types/date)


**Examples**


**String to Date conversion**



```
SELECT toDate('2025-04-15')

```


```
2025-04-15

```

**DateTime to Date conversion**



```
SELECT toDate(toDateTime('2025-04-15 10:30:00'))

```


```
2025-04-15

```

**Integer to Date conversion**



```
SELECT toDate(20297)

```


```
2025-07-28

```

## toDate32[​](#toDate32 "Direct link to toDate32")


Introduced in: v21\.9\.0


Converts the argument to the [Date32](/docs/sql-reference/data-types/date32) data type.
If the value is outside the range, `toDate32` returns the border values supported by [Date32](/docs/sql-reference/data-types/date32).
If the argument is of type [`Date`](/docs/sql-reference/data-types/date), it's bounds are taken into account.


**Syntax**



```
toDate32(expr)

```

**Arguments**


- `expr` — The value to convert. [`String`](/docs/sql-reference/data-types/string) or [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`Date`](/docs/sql-reference/data-types/date)


**Returned value**


Returns a calendar date. [`Date32`](/docs/sql-reference/data-types/date32)


**Examples**


**Within range**



```
SELECT toDate32('2025-01-01') AS value, toTypeName(value)
FORMAT Vertical

```


```
Row 1:
──────
value:           2025-01-01
toTypeName(value): Date32

```

**Outside range**



```
SELECT toDate32('1899-01-01') AS value, toTypeName(value)
FORMAT Vertical

```


```
Row 1:
──────
value:           1900-01-01
toTypeName(value): Date32

```

## toDate32OrDefault[​](#toDate32OrDefault "Direct link to toDate32OrDefault")


Introduced in: v21\.11\.0


Converts the argument to the [Date32](/docs/sql-reference/data-types/date32) data type. If the value is outside the range, `toDate32OrDefault` returns the lower border value supported by [Date32](/docs/sql-reference/data-types/date32). If the argument has [Date](/docs/sql-reference/data-types/date) type, it's borders are taken into account. Returns default value if an invalid argument is received.


**Syntax**



```
toDate32OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Date32`](/docs/sql-reference/data-types/date32)


**Returned value**


Value of type Date32 if successful, otherwise returns the default value if passed or 1900\-01\-01 if not. [`Date32`](/docs/sql-reference/data-types/date32)


**Examples**


**Successful conversion**



```
SELECT toDate32OrDefault('1930-01-01', toDate32('2020-01-01'))

```


```
1930-01-01

```

**Failed conversion**



```
SELECT toDate32OrDefault('xx1930-01-01', toDate32('2020-01-01'))

```


```
2020-01-01

```

## toDate32OrNull[​](#toDate32OrNull "Direct link to toDate32OrNull")


Introduced in: v21\.9\.0


Converts an input value to a value of type Date32 but returns `NULL` if an invalid argument is received.
The same as [`toDate32`](#toDate32) but returns `NULL` if an invalid argument is received.


**Syntax**



```
toDate32OrNull(x)

```

**Arguments**


- `x` — A string representation of a date. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Date32 value if successful, otherwise `NULL`. [`Date32`](/docs/sql-reference/data-types/date32) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toDate32OrNull('2025-01-01'), toDate32OrNull('invalid')

```


```
┌─toDate32OrNull('2025-01-01')─┬─toDate32OrNull('invalid')─┐
│                   2025-01-01 │                      ᴺᵁᴸᴸ │
└──────────────────────────────┴───────────────────────────┘

```

## toDate32OrZero[​](#toDate32OrZero "Direct link to toDate32OrZero")


Introduced in: v21\.9\.0


Converts an input value to a value of type [Date32](/docs/sql-reference/data-types/date32) but returns the lower boundary of [Date32](/docs/sql-reference/data-types/date32) if an invalid argument is received.
The same as [toDate32](#toDate32) but returns lower boundary of [Date32](/docs/sql-reference/data-types/date32) if an invalid argument is received.


See also:


- [`toDate32`](#toDate32)
- [`toDate32OrNull`](#toDate32OrNull)
- [`toDate32OrDefault`](#toDate32OrDefault)


**Syntax**



```
toDate32OrZero(x)

```

**Arguments**


- `x` — A string representation of a date. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Date32 value if successful, otherwise the lower boundary of Date32 (`1900-01-01`). [`Date32`](/docs/sql-reference/data-types/date32)


**Examples**


**Usage example**



```
SELECT toDate32OrZero('2025-01-01'), toDate32OrZero('')

```


```
┌─toDate32OrZero('2025-01-01')─┬─toDate32OrZero('')─┐
│                   2025-01-01 │         1900-01-01 │
└──────────────────────────────┴────────────────────┘

```

## toDateOrDefault[​](#toDateOrDefault "Direct link to toDateOrDefault")


Introduced in: v21\.11\.0


Like [toDate](#toDate) but if unsuccessful, returns a default value which is either the second argument (if specified), or otherwise the lower boundary of [Date](/docs/sql-reference/data-types/date).


**Syntax**



```
toDateOrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Date`](/docs/sql-reference/data-types/date)


**Returned value**


Value of type Date if successful, otherwise returns the default value if passed or 1970\-01\-01 if not. [`Date`](/docs/sql-reference/data-types/date)


**Examples**


**Successful conversion**



```
SELECT toDateOrDefault('2022-12-30')

```


```
2022-12-30

```

**Failed conversion**



```
SELECT toDateOrDefault('', CAST('2023-01-01', 'Date'))

```


```
2023-01-01

```

## toDateOrNull[​](#toDateOrNull "Direct link to toDateOrNull")


Introduced in: v1\.1\.0


Converts an input value to a value of type `Date` but returns `NULL` if an invalid argument is received.
The same as [`toDate`](#toDate) but returns `NULL` if an invalid argument is received.


**Syntax**



```
toDateOrNull(x)

```

**Arguments**


- `x` — A string representation of a date. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Date value if successful, otherwise `NULL`. [`Date`](/docs/sql-reference/data-types/date) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toDateOrNull('2025-12-30'), toDateOrNull('invalid')

```


```
┌─toDateOrNull('2025-12-30')─┬─toDateOrNull('invalid')─┐
│                 2025-12-30 │                   ᴺᵁᴸᴸ │
└────────────────────────────┴────────────────────────┘

```

## toDateOrZero[​](#toDateOrZero "Direct link to toDateOrZero")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`Date`](/docs/sql-reference/data-types/date) but returns the lower boundary of [`Date`](/docs/sql-reference/data-types/date) if an invalid argument is received.
The same as [toDate](#toDate) but returns lower boundary of [`Date`](/docs/sql-reference/data-types/date) if an invalid argument is received.


See also:


- [`toDate`](#toDate)
- [`toDateOrNull`](#toDateOrNull)
- [`toDateOrDefault`](#toDateOrDefault)


**Syntax**



```
toDateOrZero(x)

```

**Arguments**


- `x` — A string representation of a date. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Date value if successful, otherwise the lower boundary of Date (`1970-01-01`). [`Date`](/docs/sql-reference/data-types/date)


**Examples**


**Usage example**



```
SELECT toDateOrZero('2025-12-30'), toDateOrZero('')

```


```
┌─toDateOrZero('2025-12-30')─┬─toDateOrZero('')─┐
│                 2025-12-30 │       1970-01-01 │
└────────────────────────────┴──────────────────┘

```

## toDateTime[​](#toDateTime "Direct link to toDateTime")


Introduced in: v1\.1\.0


Converts an input value to type [DateTime](/docs/sql-reference/data-types/datetime).


NoteIf `expr` is a number, it is interpreted as the number of seconds since the beginning of the Unix Epoch (as Unix timestamp).
If `expr` is a [String](/docs/sql-reference/data-types/string), it may be interpreted as a Unix timestamp or as a string representation of date / date with time.
Thus, parsing of short numbers' string representations (up to 4 digits) is explicitly disabled due to ambiguity, e.g. a string `'1999'` may be both a year (an incomplete string representation of Date / DateTime) or a unix timestamp. Longer numeric strings are allowed.


**Syntax**



```
toDateTime(expr[, time_zone])

```

**Arguments**


- `expr` — The value. [`String`](/docs/sql-reference/data-types/string) or [`Int`](/docs/sql-reference/data-types/int-uint) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)
- `time_zone` — Time zone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a date time. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT toDateTime('2025-01-01 00:00:00'), toDateTime(1735689600, 'UTC')
FORMAT Vertical

```


```
Row 1:
──────
toDateTime('2025-01-01 00:00:00'): 2025-01-01 00:00:00
toDateTime(1735689600, 'UTC'):     2025-01-01 00:00:00

```

## toDateTime32[​](#toDateTime32 "Direct link to toDateTime32")


Introduced in: v20\.9\.0


Converts an input value to type `DateTime`.
Supports conversion from `String`, `FixedString`, `Date`, `Date32`, `DateTime`, or numeric types (`(U)Int*`, `Float*`, `Decimal`).
DateTime32 provides extended range compared to `DateTime`, supporting dates from `1900-01-01` to `2299-12-31`.


**Syntax**



```
toDateTime32(x[, timezone])

```

**Arguments**


- `x` — Input value to convert. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`DateTime64`](/docs/sql-reference/data-types/datetime64)
- `timezone` — Optional. Timezone for the returned `DateTime` value. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the converted input value. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**The value is within the range**



```
SELECT toDateTime64('2025-01-01 00:00:00.000', 3) AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64('20255-01-01 00:00:00.000', 3))─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3)                                          │
└─────────────────────────┴────────────────────────────────────────────────────────┘

```

**As a decimal with precision**



```
SELECT toDateTime64(1735689600.000, 3) AS value, toTypeName(value);
-- without the decimal point the value is still treated as Unix Timestamp in seconds
SELECT toDateTime64(1546300800000, 3) AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64(1735689600.000, 3))─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3)                            │
└─────────────────────────┴──────────────────────────────────────────┘
┌───────────────────value─┬─toTypeName(toDateTime64(1546300800000, 3))─┐
│ 2282-12-31 00:00:00.000 │ DateTime64(3)                              │
└─────────────────────────┴────────────────────────────────────────────┘

```

**With a timezone**



```
SELECT toDateTime64('2025-01-01 00:00:00', 3, 'Asia/Istanbul') AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64('2025-01-01 00:00:00', 3, 'Asia/Istanbul'))─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3, 'Asia/Istanbul')                                      │
└─────────────────────────┴─────────────────────────────────────────────────────────────────────┘

```

## toDateTime64[​](#toDateTime64 "Direct link to toDateTime64")


Introduced in: v20\.1\.0


Converts an input value to a value of type [`DateTime64`](/docs/sql-reference/data-types/datetime64).


**Syntax**



```
toDateTime64(expr, scale[, timezone])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `scale` — Tick size (precision): 10^(\-scale) seconds. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Time zone for the specified `DateTime64` object. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a calendar date and time of day, with sub\-second precision. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**The value is within the range**



```
SELECT toDateTime64('2025-01-01 00:00:00.000', 3) AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64('2025-01-01 00:00:00.000', 3))─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3)                                          │
└─────────────────────────┴────────────────────────────────────────────────────────┘

```

**As decimal with precision**



```
SELECT toDateTime64(1546300800.000, 3) AS value, toTypeName(value);
-- Without the decimal point the value is still treated as Unix Timestamp in seconds
SELECT toDateTime64(1546300800000, 3) AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64(1546300800000, 3))─┐
│ 2282-12-31 00:00:00.000 │ DateTime64(3)                              │
└─────────────────────────┴────────────────────────────────────────────┘

```

**With timezone**



```
SELECT toDateTime64('2025-01-01 00:00:00', 3, 'Asia/Istanbul') AS value, toTypeName(value);

```


```
┌───────────────────value─┬─toTypeName(toDateTime64('2025-01-01 00:00:00', 3, 'Asia/Istanbul'))─┐
│ 2025-01-01 00:00:00.000 │ DateTime64(3, 'Asia/Istanbul')                                      │
└─────────────────────────┴─────────────────────────────────────────────────────────────────────┘

```

## toDateTime64OrDefault[​](#toDateTime64OrDefault "Direct link to toDateTime64OrDefault")


Introduced in: v21\.11\.0


Like [toDateTime64](#toDateTime64), this function converts an input value to a value of type [DateTime64](/docs/sql-reference/data-types/datetime64),
but returns either the default value of [DateTime64](/docs/sql-reference/data-types/datetime64)
or the provided default if an invalid argument is received.


**Syntax**



```
toDateTime64OrDefault(expr, scale[, timezone, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `scale` — Tick size (precision): 10^\-precision seconds. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Time zone. [`String`](/docs/sql-reference/data-types/string)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Returned value**


Value of type DateTime64 if successful, otherwise returns the default value if passed or 1970\-01\-01 00:00:00\.000 if not. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Successful conversion**



```
SELECT toDateTime64OrDefault('1976-10-18 00:00:00.30', 3)

```


```
1976-10-18 00:00:00.300

```

**Failed conversion**



```
SELECT toDateTime64OrDefault('1976-10-18 00:00:00 30', 3, 'UTC', toDateTime64('2001-01-01 00:00:00.00',3))

```


```
2000-12-31 23:00:00.000

```

## toDateTime64OrNull[​](#toDateTime64OrNull "Direct link to toDateTime64OrNull")


Introduced in: v20\.1\.0


Converts an input value to a value of type `DateTime64` but returns `NULL` if an invalid argument is received.
The same as `toDateTime64` but returns `NULL` if an invalid argument is received.


**Syntax**



```
toDateTime64OrNull(x)

```

**Arguments**


- `x` — A string representation of a date with time and subsecond precision. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a DateTime64 value if successful, otherwise `NULL`. [`DateTime64`](/docs/sql-reference/data-types/datetime64) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toDateTime64OrNull('2025-12-30 13:44:17.123'), toDateTime64OrNull('invalid')

```


```
┌─toDateTime64OrNull('2025-12-30 13:44:17.123')─┬─toDateTime64OrNull('invalid')─┐
│                         2025-12-30 13:44:17.123 │                          ᴺᵁᴸᴸ │
└─────────────────────────────────────────────────┴───────────────────────────────┘

```

## toDateTime64OrZero[​](#toDateTime64OrZero "Direct link to toDateTime64OrZero")


Introduced in: v20\.1\.0


Converts an input value to a value of type [DateTime64](/docs/sql-reference/data-types/datetime64) but returns the lower boundary of [DateTime64](/docs/sql-reference/data-types/datetime64) if an invalid argument is received.
The same as [toDateTime64](#toDateTime64) but returns lower boundary of [DateTime64](/docs/sql-reference/data-types/datetime64) if an invalid argument is received.


See also:


- [toDateTime64](#toDateTime64).
- [toDateTime64OrNull](#toDateTime64OrNull).
- [toDateTime64OrDefault](#toDateTime64OrDefault).


**Syntax**



```
toDateTime64OrZero(x)

```

**Arguments**


- `x` — A string representation of a date with time and subsecond precision. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a DateTime64 value if successful, otherwise the lower boundary of DateTime64 (`1970-01-01 00:00:00.000`). [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT toDateTime64OrZero('2025-12-30 13:44:17.123'), toDateTime64OrZero('invalid')

```


```
┌─toDateTime64OrZero('2025-12-30 13:44:17.123')─┬─toDateTime64OrZero('invalid')─┐
│                         2025-12-30 13:44:17.123 │             1970-01-01 00:00:00.000 │
└─────────────────────────────────────────────────┴─────────────────────────────────────┘

```

## toDateTimeOrDefault[​](#toDateTimeOrDefault "Direct link to toDateTimeOrDefault")


Introduced in: v21\.11\.0


Like [toDateTime](#toDateTime) but if unsuccessful, returns a default value which is either the third argument (if specified), or otherwise the lower boundary of [DateTime](/docs/sql-reference/data-types/datetime).


**Syntax**



```
toDateTimeOrDefault(expr[, timezone, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `timezone` — Optional. Time zone. [`String`](/docs/sql-reference/data-types/string)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Value of type DateTime if successful, otherwise returns the default value if passed or 1970\-01\-01 00:00:00 if not. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Successful conversion**



```
SELECT toDateTimeOrDefault('2022-12-30 13:44:17')

```


```
2022-12-30 13:44:17

```

**Failed conversion**



```
SELECT toDateTimeOrDefault('', 'UTC', CAST('2023-01-01', 'DateTime(\'UTC\')'))

```


```
2023-01-01 00:00:00

```

## toDateTimeOrNull[​](#toDateTimeOrNull "Direct link to toDateTimeOrNull")


Introduced in: v1\.1\.0


Converts an input value to a value of type `DateTime` but returns `NULL` if an invalid argument is received.
The same as [`toDateTime`](#toDateTime) but returns `NULL` if an invalid argument is received.


**Syntax**



```
toDateTimeOrNull(x)

```

**Arguments**


- `x` — A string representation of a date with time. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a `DateTime` value if successful, otherwise `NULL`. [`DateTime`](/docs/sql-reference/data-types/datetime) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toDateTimeOrNull('2025-12-30 13:44:17'), toDateTimeOrNull('invalid')

```


```
┌─toDateTimeOrNull('2025-12-30 13:44:17')─┬─toDateTimeOrNull('invalid')─┐
│                     2025-12-30 13:44:17 │                        ᴺᵁᴸᴸ │
└─────────────────────────────────────────┴─────────────────────────────┘

```

## toDateTimeOrZero[​](#toDateTimeOrZero "Direct link to toDateTimeOrZero")


Introduced in: v1\.1\.0


Converts an input value to a value of type [DateTime](/docs/sql-reference/data-types/datetime) but returns the lower boundary of [DateTime](/docs/sql-reference/data-types/datetime) if an invalid argument is received.
The same as [toDateTime](#toDateTime) but returns lower boundary of [DateTime](/docs/sql-reference/data-types/datetime) if an invalid argument is received.


**Syntax**



```
toDateTimeOrZero(x)

```

**Arguments**


- `x` — A string representation of a date with time. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a DateTime value if successful, otherwise the lower boundary of DateTime (`1970-01-01 00:00:00`). [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT toDateTimeOrZero('2025-12-30 13:44:17'), toDateTimeOrZero('invalid')

```


```
┌─toDateTimeOrZero('2025-12-30 13:44:17')─┬─toDateTimeOrZero('invalid')─┐
│                     2025-12-30 13:44:17 │         1970-01-01 00:00:00 │
└─────────────────────────────────────────┴─────────────────────────────┘

```

## toDecimal128[​](#toDecimal128 "Direct link to toDecimal128")


Introduced in: v18\.12\.0


Converts an input value to a value of type [`Decimal(38, S)`](/docs/sql-reference/data-types/decimal) with scale of `S`.
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments:


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values, e.g. `SELECT toDecimal128('0xc0fe', 1);`.


NoteAn overflow can occur if the value of `expr` exceeds the bounds of `Decimal128`:`(-1*10^(38 - S), 1*10^(38 - S))`.
Excessive digits in a fraction are discarded (not rounded).
Excessive digits in the integer part will lead to an exception.


NoteConversions drop extra digits and could operate in an unexpected way when working with Float32/Float64 inputs as the operations are performed using floating point instructions.
For example: `toDecimal128(1.15, 2)` is equal to `1.14` because 1\.15 \* 100 in floating point is 114\.99\.
You can use a String input so the operations use the underlying integer type: `toDecimal128('1.15', 2) = 1.15`


**Syntax**



```
toDecimal128(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 38, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type `Decimal(38, S)` [`Decimal128(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Usage example**



```
SELECT
    toDecimal128(99, 1) AS a, toTypeName(a) AS type_a,
    toDecimal128(99.67, 2) AS b, toTypeName(b) AS type_b,
    toDecimal128('99.67', 3) AS c, toTypeName(c) AS type_c
FORMAT Vertical

```


```
Row 1:
──────
a:      99
type_a: Decimal(38, 1)
b:      99.67
type_b: Decimal(38, 2)
c:      99.67
type_c: Decimal(38, 3)

```

## toDecimal128OrDefault[​](#toDecimal128OrDefault "Direct link to toDecimal128OrDefault")


Introduced in: v21\.11\.0


Like [`toDecimal128`](#toDecimal128), this function converts an input value to a value of type [Decimal(38, S)](/docs/sql-reference/data-types/decimal) but returns the default value in case of an error.


**Syntax**



```
toDecimal128OrDefault(expr, S[, default])

```

**Arguments**


- `expr` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)
- `S` — Scale parameter between 0 and 38, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `default` — Optional. The default value to return if parsing to type Decimal128(S) is unsuccessful. [`Decimal128(S)`](/docs/sql-reference/data-types/decimal)


**Returned value**


Value of type Decimal(38, S) if successful, otherwise returns the default value if passed or 0 if not. [`Decimal128(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Successful conversion**



```
SELECT toDecimal128OrDefault(toString(1/42), 18)

```


```
0.023809523809523808

```

**Failed conversion**



```
SELECT toDecimal128OrDefault('Inf', 0, CAST('-1', 'Decimal128(0)'))

```


```
-1

```

## toDecimal128OrNull[​](#toDecimal128OrNull "Direct link to toDecimal128OrNull")


Introduced in: v20\.1\.0


Converts an input value to a value of type [`Decimal(38, S)`](/docs/sql-reference/data-types/decimal) but returns `NULL` in case of an error.
Like [`toDecimal128`](#toDecimal128) but returns `NULL` instead of throwing an exception on conversion errors.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments (return `NULL`):


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values.
- Values that exceed the bounds of `Decimal128`:`(-1*10^(38 - S), 1*10^(38 - S))`.


See also:


- [`toDecimal128`](#toDecimal128).
- [`toDecimal128OrZero`](#toDecimal128OrZero).
- [`toDecimal128OrDefault`](#toDecimal128OrDefault).


**Syntax**



```
toDecimal128OrNull(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 38, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Decimal(38, S) value if successful, otherwise `NULL`. [`Decimal128(S)`](/docs/sql-reference/data-types/decimal) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toDecimal128OrNull('42.7', 2), toDecimal128OrNull('invalid', 2)

```


```
┌─toDecimal128OrNull('42.7', 2)─┬─toDecimal128OrNull('invalid', 2)─┐
│                         42.70 │                             ᴺᵁᴸᴸ │
└───────────────────────────────┴──────────────────────────────────┘

```

## toDecimal128OrZero[​](#toDecimal128OrZero "Direct link to toDecimal128OrZero")


Introduced in: v20\.1\.0


Converts an input value to a value of type [Decimal(38, S)](/docs/sql-reference/data-types/decimal) but returns `0` in case of an error.
Like [`toDecimal128`](#toDecimal128) but returns `0` instead of throwing an exception on conversion errors.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments (return `0`):


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values.


NoteIf the input value exceeds the bounds of `Decimal128`:`(-1*10^(38 - S), 1*10^(38 - S))`, the function returns `0`.


**Syntax**



```
toDecimal128OrZero(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 38, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Decimal(38, S) value if successful, otherwise `0`. [`Decimal128(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Basic usage**



```
SELECT toDecimal128OrZero('42.7', 2), toDecimal128OrZero('invalid', 2)

```


```
┌─toDecimal128OrZero('42.7', 2)─┬─toDecimal128OrZero('invalid', 2)─┐
│                         42.70 │                             0.00 │
└───────────────────────────────┴──────────────────────────────────┘

```

## toDecimal256[​](#toDecimal256 "Direct link to toDecimal256")


Introduced in: v20\.8\.0


Converts an input value to a value of type [`Decimal(76, S)`](/docs/sql-reference/data-types/decimal) with scale of `S`. Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments:


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values, e.g. `SELECT toDecimal256('0xc0fe', 1);`.


NoteAn overflow can occur if the value of `expr` exceeds the bounds of `Decimal256`:`(-1*10^(76 - S), 1*10^(76 - S))`.
Excessive digits in a fraction are discarded (not rounded).
Excessive digits in the integer part will lead to an exception.


NoteConversions drop extra digits and could operate in an unexpected way when working with Float32/Float64 inputs as the operations are performed using floating point instructions.
For example: `toDecimal256(1.15, 2)` is equal to `1.14` because 1\.15 \* 100 in floating point is 114\.99\.
You can use a String input so the operations use the underlying integer type: `toDecimal256('1.15', 2) = 1.15`


**Syntax**



```
toDecimal256(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 76, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type `Decimal(76, S)`. [`Decimal256(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Usage example**



```
SELECT
    toDecimal256(99, 1) AS a, toTypeName(a) AS type_a,
    toDecimal256(99.67, 2) AS b, toTypeName(b) AS type_b,
    toDecimal256('99.67', 3) AS c, toTypeName(c) AS type_c
FORMAT Vertical

```


```
Row 1:
──────
a:      99
type_a: Decimal(76, 1)
b:      99.67
type_b: Decimal(76, 2)
c:      99.67
type_c: Decimal(76, 3)

```

## toDecimal256OrDefault[​](#toDecimal256OrDefault "Direct link to toDecimal256OrDefault")


Introduced in: v21\.11\.0


Like [`toDecimal256`](#toDecimal256), this function converts an input value to a value of type [Decimal(76, S)](/docs/sql-reference/data-types/decimal) but returns the default value in case of an error.


**Syntax**



```
toDecimal256OrDefault(expr, S[, default])

```

**Arguments**


- `expr` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)
- `S` — Scale parameter between 0 and 76, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `default` — Optional. The default value to return if parsing to type Decimal256(S) is unsuccessful. [`Decimal256(S)`](/docs/sql-reference/data-types/decimal)


**Returned value**


Value of type Decimal(76, S) if successful, otherwise returns the default value if passed or 0 if not. [`Decimal256(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Successful conversion**



```
SELECT toDecimal256OrDefault(toString(1/42), 76)

```


```
0.023809523809523808

```

**Failed conversion**



```
SELECT toDecimal256OrDefault('Inf', 0, CAST('-1', 'Decimal256(0)'))

```


```
-1

```

## toDecimal256OrNull[​](#toDecimal256OrNull "Direct link to toDecimal256OrNull")


Introduced in: v20\.8\.0


Converts an input value to a value of type [`Decimal(76, S)`](/docs/sql-reference/data-types/decimal) but returns `NULL` in case of an error.
Like [`toDecimal256`](#toDecimal256) but returns `NULL` instead of throwing an exception on conversion errors.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments (return `NULL`):


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values.
- Values that exceed the bounds of `Decimal256`: `(-1 * 10^(76 - S), 1 * 10^(76 - S))`.


See also:


- [`toDecimal256`](#toDecimal256).
- [`toDecimal256OrZero`](#toDecimal256OrZero).
- [`toDecimal256OrDefault`](#toDecimal256OrDefault).


**Syntax**



```
toDecimal256OrNull(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 76, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Decimal(76, S) value if successful, otherwise `NULL`. [`Decimal256(S)`](/docs/sql-reference/data-types/decimal) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toDecimal256OrNull('42.7', 2), toDecimal256OrNull('invalid', 2)

```


```
┌─toDecimal256OrNull('42.7', 2)─┬─toDecimal256OrNull('invalid', 2)─┐
│                         42.70 │                             ᴺᵁᴸᴸ │
└───────────────────────────────┴──────────────────────────────────┘

```

## toDecimal256OrZero[​](#toDecimal256OrZero "Direct link to toDecimal256OrZero")


Introduced in: v20\.8\.0


Converts an input value to a value of type [Decimal(76, S)](/docs/sql-reference/data-types/decimal) but returns `0` in case of an error.
Like [`toDecimal256`](#toDecimal256) but returns `0` instead of throwing an exception on conversion errors.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments (return `0`):


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values.


NoteIf the input value exceeds the bounds of `Decimal256`:`(-1*10^(76 - S), 1*10^(76 - S))`, the function returns `0`.


See also:


- [`toDecimal256`](#toDecimal256).
- [`toDecimal256OrNull`](#toDecimal256OrNull).
- [`toDecimal256OrDefault`](#toDecimal256OrDefault).


**Syntax**



```
toDecimal256OrZero(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 76, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Decimal(76, S) value if successful, otherwise `0`. [`Decimal256(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Usage example**



```
SELECT toDecimal256OrZero('42.7', 2), toDecimal256OrZero('invalid', 2)

```


```
┌─toDecimal256OrZero('42.7', 2)─┬─toDecimal256OrZero('invalid', 2)─┐
│                         42.70 │                             0.00 │
└───────────────────────────────┴──────────────────────────────────┘

```

## toDecimal32[​](#toDecimal32 "Direct link to toDecimal32")


Introduced in: v18\.12\.0


Converts an input value to a value of type [`Decimal(9, S)`](/docs/sql-reference/data-types/decimal) with scale of `S`. Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments:


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values, e.g. `SELECT toDecimal32('0xc0fe', 1);`.


NoteAn overflow can occur if the value of `expr` exceeds the bounds of `Decimal32`:`(-1*10^(9 - S), 1*10^(9 - S))`.
Excessive digits in a fraction are discarded (not rounded).
Excessive digits in the integer part will lead to an exception.


NoteConversions drop extra digits and could operate in an unexpected way when working with Float32/Float64 inputs as the operations are performed using floating point instructions.
For example: `toDecimal32(1.15, 2)` is equal to `1.14` because 1\.15 \* 100 in floating point is 114\.99\.
You can use a String input so the operations use the underlying integer type: `toDecimal32('1.15', 2) = 1.15`


**Syntax**



```
toDecimal32(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 9, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type `Decimal(9, S)` [`Decimal32(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Usage example**



```
SELECT
    toDecimal32(2, 1) AS a, toTypeName(a) AS type_a,
    toDecimal32(4.2, 2) AS b, toTypeName(b) AS type_b,
    toDecimal32('4.2', 3) AS c, toTypeName(c) AS type_c
FORMAT Vertical

```


```
Row 1:
──────
a:      2
type_a: Decimal(9, 1)
b:      4.2
type_b: Decimal(9, 2)
c:      4.2
type_c: Decimal(9, 3)

```

## toDecimal32OrDefault[​](#toDecimal32OrDefault "Direct link to toDecimal32OrDefault")


Introduced in: v21\.11\.0


Like [`toDecimal32`](#toDecimal32), this function converts an input value to a value of type [Decimal(9, S)](/docs/sql-reference/data-types/decimal) but returns the default value in case of an error.


**Syntax**



```
toDecimal32OrDefault(expr, S[, default])

```

**Arguments**


- `expr` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)
- `S` — Scale parameter between 0 and 9, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `default` — Optional. The default value to return if parsing to type Decimal32(S) is unsuccessful. [`Decimal32(S)`](/docs/sql-reference/data-types/decimal)


**Returned value**


Value of type Decimal(9, S) if successful, otherwise returns the default value if passed or 0 if not. [`Decimal32(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Successful conversion**



```
SELECT toDecimal32OrDefault(toString(0.0001), 5)

```


```
0.0001

```

**Failed conversion**



```
SELECT toDecimal32OrDefault('Inf', 0, CAST('-1', 'Decimal32(0)'))

```


```
-1

```

## toDecimal32OrNull[​](#toDecimal32OrNull "Direct link to toDecimal32OrNull")


Introduced in: v20\.1\.0


Converts an input value to a value of type [`Decimal(9, S)`](/docs/sql-reference/data-types/decimal) but returns `NULL` in case of an error.
Like [`toDecimal32`](#toDecimal32) but returns `NULL` instead of throwing an exception on conversion errors.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments (return `NULL`):


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values.
- Values that exceed the bounds of `Decimal32`:`(-1*10^(9 - S), 1*10^(9 - S))`.


See also:


- [`toDecimal32`](#toDecimal32).
- [`toDecimal32OrZero`](#toDecimal32OrZero).
- [`toDecimal32OrDefault`](#toDecimal32OrDefault).


**Syntax**



```
toDecimal32OrNull(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 9, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Decimal(9, S) value if successful, otherwise `NULL`. [`Decimal32(S)`](/docs/sql-reference/data-types/decimal) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toDecimal32OrNull('42.7', 2), toDecimal32OrNull('invalid', 2)

```


```
┌─toDecimal32OrNull('42.7', 2)─┬─toDecimal32OrNull('invalid', 2)─┐
│                        42.70 │                            ᴺᵁᴸᴸ │
└──────────────────────────────┴─────────────────────────────────┘

```

## toDecimal32OrZero[​](#toDecimal32OrZero "Direct link to toDecimal32OrZero")


Introduced in: v20\.1\.0


Converts an input value to a value of type [Decimal(9, S)](/docs/sql-reference/data-types/decimal) but returns `0` in case of an error.
Like [`toDecimal32`](#toDecimal32) but returns `0` instead of throwing an exception on conversion errors.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments (return `0`):


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values.


NoteIf the input value exceeds the bounds of `Decimal32`:`(-1*10^(9 - S), 1*10^(9 - S))`, the function returns `0`.


**Syntax**



```
toDecimal32OrZero(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 9, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Decimal(9, S) value if successful, otherwise `0`. [`Decimal32(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Usage example**



```
SELECT toDecimal32OrZero('42.7', 2), toDecimal32OrZero('invalid', 2)

```


```
┌─toDecimal32OrZero('42.7', 2)─┬─toDecimal32OrZero('invalid', 2)─┐
│                        42.70 │                            0.00 │
└──────────────────────────────┴─────────────────────────────────┘

```

## toDecimal64[​](#toDecimal64 "Direct link to toDecimal64")


Introduced in: v18\.12\.0


Converts an input value to a value of type [`Decimal(18, S)`](/docs/sql-reference/data-types/decimal) with scale of `S`.
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments:


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values, e.g. `SELECT toDecimal64('0xc0fe', 1);`.


NoteAn overflow can occur if the value of `expr` exceeds the bounds of `Decimal64`:`(-1*10^(18 - S), 1*10^(18 - S))`.
Excessive digits in a fraction are discarded (not rounded).
Excessive digits in the integer part will lead to an exception.


NoteConversions drop extra digits and could operate in an unexpected way when working with Float32/Float64 inputs as the operations are performed using floating point instructions.
For example: `toDecimal64(1.15, 2)` is equal to `1.14` because 1\.15 \* 100 in floating point is 114\.99\.
You can use a String input so the operations use the underlying integer type: `toDecimal64('1.15', 2) = 1.15`


**Syntax**



```
toDecimal64(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 18, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a decimal value. [`Decimal(18, S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Usage example**



```
SELECT
    toDecimal64(2, 1) AS a, toTypeName(a) AS type_a,
    toDecimal64(4.2, 2) AS b, toTypeName(b) AS type_b,
    toDecimal64('4.2', 3) AS c, toTypeName(c) AS type_c
FORMAT Vertical

```


```
Row 1:
──────
a:      2.0
type_a: Decimal(18, 1)
b:      4.20
type_b: Decimal(18, 2)
c:      4.200
type_c: Decimal(18, 3)

```

## toDecimal64OrDefault[​](#toDecimal64OrDefault "Direct link to toDecimal64OrDefault")


Introduced in: v21\.11\.0


Like [`toDecimal64`](#toDecimal64), this function converts an input value to a value of type [Decimal(18, S)](/docs/sql-reference/data-types/decimal) but returns the default value in case of an error.


**Syntax**



```
toDecimal64OrDefault(expr, S[, default])

```

**Arguments**


- `expr` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)
- `S` — Scale parameter between 0 and 18, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `default` — Optional. The default value to return if parsing to type Decimal64(S) is unsuccessful. [`Decimal64(S)`](/docs/sql-reference/data-types/decimal)


**Returned value**


Value of type Decimal(18, S) if successful, otherwise returns the default value if passed or 0 if not. [`Decimal64(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Successful conversion**



```
SELECT toDecimal64OrDefault(toString(0.0001), 18)

```


```
0.0001

```

**Failed conversion**



```
SELECT toDecimal64OrDefault('Inf', 0, CAST('-1', 'Decimal64(0)'))

```


```
-1

```

## toDecimal64OrNull[​](#toDecimal64OrNull "Direct link to toDecimal64OrNull")


Introduced in: v20\.1\.0


Converts an input value to a value of type [Decimal(18, S)](/docs/sql-reference/data-types/decimal) but returns `NULL` in case of an error.
Like [`toDecimal64`](#toDecimal64) but returns `NULL` instead of throwing an exception on conversion errors.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments (return `NULL`):


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values.
- Values that exceed the bounds of `Decimal64`:`(-1*10^(18 - S), 1*10^(18 - S))`.


See also:


- [`toDecimal64`](#toDecimal64).
- [`toDecimal64OrZero`](#toDecimal64OrZero).
- [`toDecimal64OrDefault`](#toDecimal64OrDefault).


**Syntax**



```
toDecimal64OrNull(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 18, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Decimal(18, S) value if successful, otherwise `NULL`. [`Decimal64(S)`](/docs/sql-reference/data-types/decimal) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toDecimal64OrNull('42.7', 2), toDecimal64OrNull('invalid', 2)

```


```
┌─toDecimal64OrNull('42.7', 2)─┬─toDecimal64OrNull('invalid', 2)─┐
│                        42.70 │                            ᴺᵁᴸᴸ │
└──────────────────────────────┴─────────────────────────────────┘

```

## toDecimal64OrZero[​](#toDecimal64OrZero "Direct link to toDecimal64OrZero")


Introduced in: v20\.1\.0


Converts an input value to a value of type [Decimal(18, S)](/docs/sql-reference/data-types/decimal) but returns `0` in case of an error.
Like [`toDecimal64`](#toDecimal64) but returns `0` instead of throwing an exception on conversion errors.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values or string representations of type Float\*.


Unsupported arguments (return `0`):


- Values or string representations of Float\* values `NaN` and `Inf` (case\-insensitive).
- String representations of binary and hexadecimal values.


NoteIf the input value exceeds the bounds of `Decimal64`:`(-1*10^(18 - S), 1*10^(18 - S))`, the function returns `0`.


See also:


- [`toDecimal64`](#toDecimal64).
- [`toDecimal64OrNull`](#toDecimal64OrNull).
- [`toDecimal64OrDefault`](#toDecimal64OrDefault).


**Syntax**



```
toDecimal64OrZero(expr, S)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)
- `S` — Scale parameter between 0 and 18, specifying how many digits the fractional part of a number can have. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a Decimal(18, S) value if successful, otherwise `0`. [`Decimal64(S)`](/docs/sql-reference/data-types/decimal)


**Examples**


**Usage example**



```
SELECT toDecimal64OrZero('42.7', 2), toDecimal64OrZero('invalid', 2)

```


```
┌─toDecimal64OrZero('42.7', 2)─┬─toDecimal64OrZero('invalid', 2)─┐
│                        42.70 │                            0.00 │
└──────────────────────────────┴─────────────────────────────────┘

```

## toDecimalString[​](#toDecimalString "Direct link to toDecimalString")


Introduced in: v23\.3\.0


Converts a numeric value to a String with specified number of fractional digits.


The function rounds the input value to the specified number of decimal places. If the input value has fewer fractional
digits than requested, the result is padded with zeros to achieve the exact number of fractional digits specified.


**Syntax**



```
toDecimalString(number, scale)

```

**Arguments**


- `number` — The numeric value to convert to a string. Can be any numeric type (Int, UInt, Float, Decimal). [`Int8`](/docs/sql-reference/data-types/int-uint) or [`Int16`](/docs/sql-reference/data-types/int-uint) or [`Int32`](/docs/sql-reference/data-types/int-uint) or [`Int64`](/docs/sql-reference/data-types/int-uint) or [`UInt8`](/docs/sql-reference/data-types/int-uint) or [`UInt16`](/docs/sql-reference/data-types/int-uint) or [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`UInt64`](/docs/sql-reference/data-types/int-uint) or [`Float32`](/docs/sql-reference/data-types/float) or [`Float64`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `scale` — The number of digits to display in the fractional part. The result will be rounded if necessary. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a String representation of the number with exactly the specified number of fractional digits. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Round and format a number**



```
SELECT toDecimalString(2.1456, 2)

```


```
┌─toDecimalString(2.1456, 2)─┐
│ 2.15                       │
└────────────────────────────┘

```

**Pad with zeros**



```
SELECT toDecimalString(5, 3)

```


```
┌─toDecimalString(5, 3)─┐
│ 5.000                 │
└───────────────────────┘

```

**Different numeric types**



```
SELECT toDecimalString(CAST(123.456 AS Decimal(10,3)), 2) AS decimal_val,
       toDecimalString(CAST(42.7 AS Float32), 4) AS float_val

```


```
┌─decimal_val─┬─float_val─┐
│ 123.46      │ 42.7000   │
└─────────────┴───────────┘

```

## toFixedString[​](#toFixedString "Direct link to toFixedString")


Introduced in: v1\.1\.0


Converts a [`String`](/docs/sql-reference/data-types/string) argument to a [`FixedString(N)`](/docs/sql-reference/data-types/fixedstring) type (a string of fixed length N).


If the string has fewer bytes than N, it is padded with null bytes to the right.
If the string has more bytes than N, an exception is thrown.


**Syntax**



```
toFixedString(s, N)

```

**Arguments**


- `s` — String to convert. [`String`](/docs/sql-reference/data-types/string)
- `N` — Length of the resulting FixedString. [`const UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a FixedString of length N. [`FixedString(N)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT toFixedString('foo', 8) AS s;

```


```
┌─s─────────────┐
│ foo\0\0\0\0\0 │
└───────────────┘

```

## toFloat32[​](#toFloat32 "Direct link to toFloat32")


Introduced in: v1\.1\.0


Converts an input value to a value of type [Float32](/docs/sql-reference/data-types/float).
Throws an exception in case of an error.


Supported arguments:


- Values of type (U)Int\*.
- String representations of (U)Int8/16/32/128/256\.
- Values of type Float\*, including `NaN` and `Inf`.
- String representations of Float\*, including `NaN` and `Inf` (case\-insensitive).


Unsupported arguments:


- String representations of binary and hexadecimal values, e.g. `SELECT toFloat32('0xc0fe');`.


See also:


- [`toFloat32OrZero`](#toFloat32OrZero).
- [`toFloat32OrNull`](#toFloat32OrNull).
- [`toFloat32OrDefault`](#toFloat32OrDefault).


**Syntax**



```
toFloat32(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 32\-bit floating point value. [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT
    toFloat32(42.7),
    toFloat32('42.7'),
    toFloat32('NaN')
FORMAT Vertical

```


```
Row 1:
──────
toFloat32(42.7):   42.7
toFloat32('42.7'): 42.7
toFloat32('NaN'):  nan

```

## toFloat32OrDefault[​](#toFloat32OrDefault "Direct link to toFloat32OrDefault")


Introduced in: v21\.11\.0


Like [`toFloat32`](#toFloat32), this function converts an input value to a value of type [Float32](/docs/sql-reference/data-types/float) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toFloat32OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Float32`](/docs/sql-reference/data-types/float)


**Returned value**


Returns a value of type Float32 if successful, otherwise returns the default value if passed or 0 if not. [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**Successful conversion**



```
SELECT toFloat32OrDefault('8', CAST('0', 'Float32'))

```


```
8

```

**Failed conversion**



```
SELECT toFloat32OrDefault('abc', CAST('0', 'Float32'))

```


```
0

```

## toFloat32OrNull[​](#toFloat32OrNull "Direct link to toFloat32OrNull")


Introduced in: v1\.1\.0


Converts an input value to a value of type [Float32](/docs/sql-reference/data-types/float) but returns `NULL` in case of an error.
Like [`toFloat32`](#toFloat32) but returns `NULL` instead of throwing an exception on conversion errors.


Supported arguments:


- Values of type (U)Int\*.
- String representations of (U)Int8/16/32/128/256\.
- Values of type Float\*, including `NaN` and `Inf`.
- String representations of Float\*, including `NaN` and `Inf` (case\-insensitive).


Unsupported arguments (return `NULL`):


- String representations of binary and hexadecimal values, e.g. `SELECT toFloat32OrNull('0xc0fe');`.
- Invalid string formats.


See also:


- [`toFloat32`](#toFloat32).
- [`toFloat32OrZero`](#toFloat32OrZero).
- [`toFloat32OrDefault`](#toFloat32OrDefault).


**Syntax**



```
toFloat32OrNull(x)

```

**Arguments**


- `x` — A string representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a 32\-bit Float value if successful, otherwise `NULL`. [`Float32`](/docs/sql-reference/data-types/float) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toFloat32OrNull('42.7'),
    toFloat32OrNull('NaN'),
    toFloat32OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toFloat32OrNull('42.7'): 42.7
toFloat32OrNull('NaN'):  nan
toFloat32OrNull('abc'):  \N

```

## toFloat32OrZero[​](#toFloat32OrZero "Direct link to toFloat32OrZero")


Introduced in: v1\.1\.0


Converts an input value to a value of type [Float32](/docs/sql-reference/data-types/float) but returns `0` in case of an error.
Like [`toFloat32`](#toFloat32) but returns `0` instead of throwing an exception on conversion errors.


See also:


- [`toFloat32`](#toFloat32).
- [`toFloat32OrNull`](#toFloat32OrNull).
- [`toFloat32OrDefault`](#toFloat32OrDefault).


**Syntax**



```
toFloat32OrZero(x)

```

**Arguments**


- `x` — A string representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a 32\-bit Float value if successful, otherwise `0`. [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT
    toFloat32OrZero('42.7'),
    toFloat32OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toFloat32OrZero('42.7'): 42.7
toFloat32OrZero('abc'):  0

```

## toFloat64[​](#toFloat64 "Direct link to toFloat64")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`Float64`](/docs/sql-reference/data-types/float).
Throws an exception in case of an error.


Supported arguments:


- Values of type (U)Int\*.
- String representations of (U)Int8/16/32/128/256\.
- Values of type Float\*, including `NaN` and `Inf`.
- String representations of type Float\*, including `NaN` and `Inf` (case\-insensitive).


Unsupported arguments:


- String representations of binary and hexadecimal values, e.g. `SELECT toFloat64('0xc0fe');`.


See also:


- [`toFloat64OrZero`](#toFloat64OrZero).
- [`toFloat64OrNull`](#toFloat64OrNull).
- [`toFloat64OrDefault`](#toFloat64OrDefault).


**Syntax**



```
toFloat64(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 64\-bit floating point value. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT
    toFloat64(42.7),
    toFloat64('42.7'),
    toFloat64('NaN')
FORMAT Vertical

```


```
Row 1:
──────
toFloat64(42.7):   42.7
toFloat64('42.7'): 42.7
toFloat64('NaN'):  nan

```

## toFloat64OrDefault[​](#toFloat64OrDefault "Direct link to toFloat64OrDefault")


Introduced in: v21\.11\.0


Like [`toFloat64`](#toFloat64), this function converts an input value to a value of type [Float64](/docs/sql-reference/data-types/float) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toFloat64OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Float64`](/docs/sql-reference/data-types/float)


**Returned value**


Returns a value of type Float64 if successful, otherwise returns the default value if passed or 0 if not. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


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


NoteIf the input value cannot be represented within the bounds of Int128, the result over or under flows.
This is not considered an error.


See also:


- [`toInt128OrZero`](#toInt128OrZero).
- [`toInt128OrNull`](#toInt128OrNull).
- [`toInt128OrDefault`](#toInt128OrDefault).


**Syntax**



```
toInt128(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 128\-bit integer value. [`Int128`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt128(-128),
    toInt128(-128.8),
    toInt128('-128')
FORMAT Vertical

```


```
Row 1:
──────
toInt128(-128):   -128
toInt128(-128.8): -128
toInt128('-128'): -128

```

## toInt128OrDefault[​](#toInt128OrDefault "Direct link to toInt128OrDefault")


Introduced in: v21\.11\.0


Like [`toInt128`](#toInt128), this function converts an input value to a value of type [Int128](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toInt128OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Int128`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type Int128 if successful, otherwise returns the default value if passed, or 0 if not. [`Int128`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toInt128OrDefault('-128', CAST('-1', 'Int128'))

```


```
-128

```

**Failed conversion**



```
SELECT toInt128OrDefault('abc', CAST('-1', 'Int128'))

```


```
-1

```

## toInt128OrNull[​](#toInt128OrNull "Direct link to toInt128OrNull")


Introduced in: v20\.8\.0


Like [`toInt128`](#toInt128), this function converts an input value to a value of type [Int128](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt128OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int128](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt128`](#toInt128).
- [`toInt128OrZero`](#toInt128OrZero).
- [`toInt128OrDefault`](#toInt128OrDefault).


**Syntax**



```
toInt128OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type Int128, otherwise `NULL` if the conversion is unsuccessful. [`Int128`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toInt128OrNull('-128'),
    toInt128OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt128OrNull('-128'): -128
toInt128OrNull('abc'):  \N

```

## toInt128OrZero[​](#toInt128OrZero "Direct link to toInt128OrZero")


Introduced in: v20\.8\.0


Converts an input value to type [Int128](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.
Like [`toInt128`](#toInt128) but returns `0` instead of throwing an exception.


See also:


- [`toInt128`](#toInt128).
- [`toInt128OrNull`](#toInt128OrNull).
- [`toInt128OrDefault`](#toInt128OrDefault).


**Syntax**



```
toInt128OrZero(x)

```

**Arguments**


- `x` — Input value to convert. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Returns the converted input value, otherwise `0` if conversion fails. [`Int128`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT toInt128OrZero('123')

```


```
123

```

**Failed conversion returns zero**



```
SELECT toInt128OrZero('abc')

```


```
0

```

## toInt16[​](#toInt16 "Direct link to toInt16")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`Int16`](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt16('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int16](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.
For example: `SELECT toInt16(32768) == -32768;`.


NoteThe function uses [rounding towards zero](https://en.wikipedia.org/wiki/Rounding#Rounding_towards_zero), meaning it truncates fractional digits of numbers.


See also:


- [`toInt16OrZero`](#toInt16OrZero).
- [`toInt16OrNull`](#toInt16OrNull).
- [`toInt16OrDefault`](#toInt16OrDefault).


**Syntax**



```
toInt16(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 16\-bit integer value. [`Int16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt16(-16),
    toInt16(-16.16),
    toInt16('-16')
FORMAT Vertical

```


```
Row 1:
──────
toInt16(-16):    -16
toInt16(-16.16): -16
toInt16('-16'):  -16

```

## toInt16OrDefault[​](#toInt16OrDefault "Direct link to toInt16OrDefault")


Introduced in: v21\.11\.0


Like [`toInt16`](#toInt16), this function converts an input value to a value of type [Int16](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toInt16OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Int16`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type Int16 if successful, otherwise returns the default value if passed, or 0 if not. [`Int16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toInt16OrDefault('-16', CAST('-1', 'Int16'))

```


```
-16

```

**Failed conversion**



```
SELECT toInt16OrDefault('abc', CAST('-1', 'Int16'))

```


```
-1

```

## toInt16OrNull[​](#toInt16OrNull "Direct link to toInt16OrNull")


Introduced in: v1\.1\.0


Like [`toInt16`](#toInt16), this function converts an input value to a value of type [Int16](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt16OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int16](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt16`](#toInt16).
- [`toInt16OrZero`](#toInt16OrZero).
- [`toInt16OrDefault`](#toInt16OrDefault).


**Syntax**



```
toInt16OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type `Int16`, otherwise `NULL` if the conversion is unsuccessful. [`Int16`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toInt16OrNull('-16'),
    toInt16OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt16OrNull('-16'): -16
toInt16OrNull('abc'): \N

```

## toInt16OrZero[​](#toInt16OrZero "Direct link to toInt16OrZero")


Introduced in: v1\.1\.0


Like [`toInt16`](#toInt16), this function converts an input value to a value of type [Int16](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `0`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt16OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int16](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt16`](#toInt16).
- [`toInt16OrNull`](#toInt16OrNull).
- [`toInt16OrDefault`](#toInt16OrDefault).


**Syntax**



```
toInt16OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type Int16, otherwise `0` if the conversion is unsuccessful. [`Int16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt16OrZero('16'),
    toInt16OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt16OrZero('16'): 16
toInt16OrZero('abc'): 0

```

## toInt256[​](#toInt256 "Direct link to toInt256")


Introduced in: v1\.1\.0


Converts an input value to a value of type [Int256](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.
The function uses rounding towards zero, meaning it truncates fractional digits of numbers.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt256('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of Int256, the result over or under flows.
This is not considered an error.


See also:


- [`toInt256OrZero`](#toInt256OrZero).
- [`toInt256OrNull`](#toInt256OrNull).
- [`toInt256OrDefault`](#toInt256OrDefault).


**Syntax**



```
toInt256(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 256\-bit integer value. [`Int256`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt256(-256),
    toInt256(-256.256),
    toInt256('-256')
FORMAT Vertical

```


```
Row 1:
──────
toInt256(-256):     -256
toInt256(-256.256): -256
toInt256('-256'):   -256

```

## toInt256OrDefault[​](#toInt256OrDefault "Direct link to toInt256OrDefault")


Introduced in: v21\.11\.0


Like [`toInt256`](#toInt256), this function converts an input value to a value of type [Int256](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toInt256OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Int256`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type Int256 if successful, otherwise returns the default value if passed, or 0 if not. [`Int256`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toInt256OrDefault('-256', CAST('-1', 'Int256'))

```


```
-256

```

**Failed conversion**



```
SELECT toInt256OrDefault('abc', CAST('-1', 'Int256'))

```


```
-1

```

## toInt256OrNull[​](#toInt256OrNull "Direct link to toInt256OrNull")


Introduced in: v20\.8\.0


Like [`toInt256`](#toInt256), this function converts an input value to a value of type [Int256](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt256OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int256](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt256`](#toInt256).
- [`toInt256OrZero`](#toInt256OrZero).
- [`toInt256OrDefault`](#toInt256OrDefault).


**Syntax**



```
toInt256OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type Int256, otherwise `NULL` if the conversion is unsuccessful. [`Int256`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toInt256OrNull('-256'),
    toInt256OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt256OrNull('-256'): -256
toInt256OrNull('abc'):  \N

```

## toInt256OrZero[​](#toInt256OrZero "Direct link to toInt256OrZero")


Introduced in: v20\.8\.0


Converts an input value to type [Int256](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.
Like [`toInt256`](#toInt256) but returns `0` instead of throwing an exception.


See also:


- [`toInt256`](#toInt256).
- [`toInt256OrNull`](#toInt256OrNull).
- [`toInt256OrDefault`](#toInt256OrDefault).


**Syntax**



```
toInt256OrZero(x)

```

**Arguments**


- `x` — Input value to convert. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Returns the converted input value, otherwise `0` if conversion fails. [`Int256`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT toInt256OrZero('123')

```


```
123

```

**Failed conversion returns zero**



```
SELECT toInt256OrZero('abc')

```


```
0

```

## toInt32[​](#toInt32 "Direct link to toInt32")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`Int32`](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt32('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int32](/docs/sql-reference/data-types/int-uint), the result over or under flows.
This is not considered an error.
For example: `SELECT toInt32(2147483648) == -2147483648;`


NoteThe function uses [rounding towards zero](https://en.wikipedia.org/wiki/Rounding#Rounding_towards_zero), meaning it truncates fractional digits of numbers.


See also:


- [`toInt32OrZero`](#toInt32OrZero).
- [`toInt32OrNull`](#toInt32OrNull).
- [`toInt32OrDefault`](#toInt32OrDefault).


**Syntax**



```
toInt32(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 32\-bit integer value. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt32(-32),
    toInt32(-32.32),
    toInt32('-32')
FORMAT Vertical

```


```
Row 1:
──────
toInt32(-32):    -32
toInt32(-32.32): -32
toInt32('-32'):  -32

```

## toInt32OrDefault[​](#toInt32OrDefault "Direct link to toInt32OrDefault")


Introduced in: v21\.11\.0


Like [`toInt32`](#toInt32), this function converts an input value to a value of type [Int32](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toInt32OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type Int32 if successful, otherwise returns the default value if passed or 0 if not. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toInt32OrDefault('-32', CAST('-1', 'Int32'))

```


```
-32

```

**Failed conversion**



```
SELECT toInt32OrDefault('abc', CAST('-1', 'Int32'))

```


```
-1

```

## toInt32OrNull[​](#toInt32OrNull "Direct link to toInt32OrNull")


Introduced in: v1\.1\.0


Like [`toInt32`](#toInt32), this function converts an input value to a value of type [Int32](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt32OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int32](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt32`](#toInt32).
- [`toInt32OrZero`](#toInt32OrZero).
- [`toInt32OrDefault`](#toInt32OrDefault).


**Syntax**



```
toInt32OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type Int32, otherwise `NULL` if the conversion is unsuccessful. [`Int32`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toInt32OrNull('-32'),
    toInt32OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt32OrNull('-32'): -32
toInt32OrNull('abc'): \N

```

## toInt32OrZero[​](#toInt32OrZero "Direct link to toInt32OrZero")


Introduced in: v1\.1\.0


Like [`toInt32`](#toInt32), this function converts an input value to a value of type [Int32](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `0`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt32OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int32](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt32`](#toInt32).
- [`toInt32OrNull`](#toInt32OrNull).
- [`toInt32OrDefault`](#toInt32OrDefault).


**Syntax**



```
toInt32OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type Int32, otherwise `0` if the conversion is unsuccessful. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt32OrZero('32'),
    toInt32OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt32OrZero('32'): 32
toInt32OrZero('abc'): 0

```

## toInt64[​](#toInt64 "Direct link to toInt64")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`Int64`](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt64('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int64](/docs/sql-reference/data-types/int-uint), the result over or under flows.
This is not considered an error.
For example: `SELECT toInt64(9223372036854775808) == -9223372036854775808;`


NoteThe function uses [rounding towards zero](https://en.wikipedia.org/wiki/Rounding#Rounding_towards_zero), meaning it truncates fractional digits of numbers.


See also:


- [`toInt64OrZero`](#toInt64OrZero).
- [`toInt64OrNull`](#toInt64OrNull).
- [`toInt64OrDefault`](#toInt64OrDefault).


**Syntax**



```
toInt64(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. Supported: values or string representations of type (U)Int\*, values of type Float\*. Unsupported: string representations of Float\* values including NaN and Inf, string representations of binary and hexadecimal values. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 64\-bit integer value. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt64(-64),
    toInt64(-64.64),
    toInt64('-64')
FORMAT Vertical

```


```
Row 1:
──────
toInt64(-64):    -64
toInt64(-64.64): -64
toInt64('-64'):  -64

```

## toInt64OrDefault[​](#toInt64OrDefault "Direct link to toInt64OrDefault")


Introduced in: v21\.11\.0


Like [`toInt64`](#toInt64), this function converts an input value to a value of type [Int64](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toInt64OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type Int64 if successful, otherwise returns the default value if passed, or 0 if not. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toInt64OrDefault('-64', CAST('-1', 'Int64'))

```


```
-64

```

**Failed conversion**



```
SELECT toInt64OrDefault('abc', CAST('-1', 'Int64'))

```


```
-1

```

## toInt64OrNull[​](#toInt64OrNull "Direct link to toInt64OrNull")


Introduced in: v1\.1\.0


Like [`toInt64`](#toInt64), this function converts an input value to a value of type [Int64](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt64OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int64](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt64`](#toInt64).
- [`toInt64OrZero`](#toInt64OrZero).
- [`toInt64OrDefault`](#toInt64OrDefault).


**Syntax**



```
toInt64OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type Int64, otherwise `NULL` if the conversion is unsuccessful. [`Int64`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toInt64OrNull('-64'),
    toInt64OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt64OrNull('-64'): -64
toInt64OrNull('abc'): \N

```

## toInt64OrZero[​](#toInt64OrZero "Direct link to toInt64OrZero")


Introduced in: v1\.1\.0


Converts an input value to type [Int64](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.
Like [`toInt64`](#toInt64) but returns `0` instead of throwing an exception.


See also:


- [`toInt64`](#toInt64).
- [`toInt64OrNull`](#toInt64OrNull).
- [`toInt64OrDefault`](#toInt64OrDefault).


**Syntax**



```
toInt64OrZero(x)

```

**Arguments**


- `x` — Input value to convert. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Returns the converted input value, otherwise `0` if conversion fails. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT toInt64OrZero('123')

```


```
123

```

**Failed conversion returns zero**



```
SELECT toInt64OrZero('abc')

```


```
0

```

## toInt8[​](#toInt8 "Direct link to toInt8")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`Int8`](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt8('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int8](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.
For example: `SELECT toInt8(128) == -128;`.


NoteThe function uses [rounding towards zero](https://en.wikipedia.org/wiki/Rounding#Rounding_towards_zero), meaning it truncates fractional digits of numbers.


See also:


- [`toInt8OrZero`](#toInt8OrZero).
- [`toInt8OrNull`](#toInt8OrNull).
- [`toInt8OrDefault`](#toInt8OrDefault).


**Syntax**



```
toInt8(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns an 8\-bit integer value. [`Int8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt8(-8),
    toInt8(-8.8),
    toInt8('-8')
FORMAT Vertical

```


```
Row 1:
──────
toInt8(-8):   -8
toInt8(-8.8): -8
toInt8('-8'): -8

```

## toInt8OrDefault[​](#toInt8OrDefault "Direct link to toInt8OrDefault")


Introduced in: v21\.11\.0


Like [`toInt8`](#toInt8), this function converts an input value to a value of type [Int8](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toInt8OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`Int8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type Int8 if successful, otherwise returns the default value if passed, or 0 if not. [`Int8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toInt8OrDefault('-8', CAST('-1', 'Int8'))

```


```
-8

```

**Failed conversion**



```
SELECT toInt8OrDefault('abc', CAST('-1', 'Int8'))

```


```
-1

```

## toInt8OrNull[​](#toInt8OrNull "Direct link to toInt8OrNull")


Introduced in: v1\.1\.0


Like [`toInt8`](#toInt8), this function converts an input value to a value of type [Int8](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt8OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int8](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt8`](#toInt8).
- [`toInt8OrZero`](#toInt8OrZero).
- [`toInt8OrDefault`](#toInt8OrDefault).


**Syntax**



```
toInt8OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type Int8, otherwise `NULL` if the conversion is unsuccessful. [`Int8`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toInt8OrNull('-8'),
    toInt8OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt8OrNull('-8'):  -8
toInt8OrNull('abc'): \N

```

## toInt8OrZero[​](#toInt8OrZero "Direct link to toInt8OrZero")


Introduced in: v1\.1\.0


Like [`toInt8`](#toInt8), this function converts an input value to a value of type [Int8](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `0`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toInt8OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [Int8](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toInt8`](#toInt8).
- [`toInt8OrNull`](#toInt8OrNull).
- [`toInt8OrDefault`](#toInt8OrDefault).


**Syntax**



```
toInt8OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type Int8, otherwise `0` if the conversion is unsuccessful. [`Int8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toInt8OrZero('8'),
    toInt8OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toInt8OrZero('8'): 8
toInt8OrZero('abc'): 0

```

## toInterval[​](#toInterval "Direct link to toInterval")


Introduced in: v25\.4\.0


Creates an Interval value from a numeric value and a unit string.


This function provides a unified way to create intervals of different types (seconds, minutes, hours, days, weeks, months, quarters, years)
from a single function by specifying the unit as a string argument. The unit string is case\-insensitive.


This is equivalent to calling type\-specific functions like `toIntervalSecond`, `toIntervalMinute`, `toIntervalDay`, etc.,
but allows the unit to be specified dynamically as a string parameter.


**Syntax**



```
toInterval(value, unit)

```

**Arguments**


- `value` — The numeric value representing the number of units. Can be any numeric type. [`Int8`](/docs/sql-reference/data-types/int-uint) or [`Int16`](/docs/sql-reference/data-types/int-uint) or [`Int32`](/docs/sql-reference/data-types/int-uint) or [`Int64`](/docs/sql-reference/data-types/int-uint) or [`UInt8`](/docs/sql-reference/data-types/int-uint) or [`UInt16`](/docs/sql-reference/data-types/int-uint) or [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`UInt64`](/docs/sql-reference/data-types/int-uint) or [`Float32`](/docs/sql-reference/data-types/float) or [`Float64`](/docs/sql-reference/data-types/float)
- `unit` — The unit of time. Must be a constant string. Valid values: 'nanosecond', 'microsecond', 'millisecond', 'second', 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an Interval value of the specified type. The result type depends on the unit: IntervalNanosecond, IntervalMicrosecond, IntervalMillisecond, IntervalSecond, IntervalMinute, IntervalHour, IntervalDay, IntervalWeek, IntervalMonth, IntervalQuarter, or IntervalYear. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Create intervals with different units**



```
SELECT
    toInterval(5, 'second') AS seconds,
    toInterval(3, 'day') AS days,
    toInterval(2, 'month') AS months

```


```
┌─seconds─┬─days─┬─months─┐
│ 5       │ 3    │ 2      │
└─────────┴──────┴────────┘

```

**Use intervals in date arithmetic**



```
SELECT
    now() AS current_time,
    now() + toInterval(1, 'hour') AS one_hour_later,
    now() - toInterval(7, 'day') AS week_ago

```


```
┌─────────current_time─┬──one_hour_later─────┬────────────week_ago─┐
│ 2025-01-04 10:30:00  │ 2025-01-04 11:30:00 │ 2024-12-28 10:30:00 │
└──────────────────────┴─────────────────────┴─────────────────────┘

```

**Dynamic interval creation**



```
SELECT toDate('2025-01-01') + toInterval(number, 'day') AS dates
FROM numbers(5)

```


```
┌──────dates─┐
│ 2025-01-01 │
│ 2025-01-02 │
│ 2025-01-03 │
│ 2025-01-04 │
│ 2025-01-05 │
└────────────┘

```

## toIntervalDay[​](#toIntervalDay "Direct link to toIntervalDay")


Introduced in: v1\.1\.0


Returns an interval of `n` days of data type [`IntervalDay`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalDay(n)

```

**Arguments**


- `n` — Number of days. Integer numbers or string representations thereof, and float numbers. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` days. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDate('2025-06-15') AS date,
    toIntervalDay(5) AS interval_to_days
SELECT date + interval_to_days AS result

```


```
┌─────result─┐
│ 2025-06-20 │
└────────────┘

```

## toIntervalHour[​](#toIntervalHour "Direct link to toIntervalHour")


Introduced in: v1\.1\.0


Returns an interval of `n` hours of data type [`IntervalHour`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalHour(n)

```

**Arguments**


- `n` — Number of hours. Integer numbers or string representations thereof, and float numbers. [`Int*`](/docs/sql-reference/data-types/int-uint) or [`UInt*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` hours. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDate('2025-06-15') AS date,
    toIntervalHour(12) AS interval_to_hours
SELECT date + interval_to_hours AS result

```


```
┌──────────────result─┐
│ 2025-06-15 12:00:00 │
└─────────────────────┘

```

## toIntervalMicrosecond[​](#toIntervalMicrosecond "Direct link to toIntervalMicrosecond")


Introduced in: v22\.6\.0


Returns an interval of `n` microseconds of data type [`IntervalMicrosecond`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalMicrosecond(n)

```

**Arguments**


- `n` — Number of microseconds. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` microseconds. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDateTime('2025-06-15') AS date,
    toIntervalMicrosecond(30) AS interval_to_microseconds
SELECT date + interval_to_microseconds AS result

```


```
┌─────────────────────result─┐
│ 2025-06-15 00:00:00.000030 │
└────────────────────────────┘

```

## toIntervalMillisecond[​](#toIntervalMillisecond "Direct link to toIntervalMillisecond")


Introduced in: v22\.6\.0


Returns an interval of `n` milliseconds of data type [IntervalMillisecond](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalMillisecond(n)

```

**Arguments**


- `n` — Number of milliseconds. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` milliseconds. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDateTime('2025-06-15') AS date,
    toIntervalMillisecond(30) AS interval_to_milliseconds
SELECT date + interval_to_milliseconds AS result

```


```
┌──────────────────result─┐
│ 2025-06-15 00:00:00.030 │
└─────────────────────────┘

```

## toIntervalMinute[​](#toIntervalMinute "Direct link to toIntervalMinute")


Introduced in: v1\.1\.0


Returns an interval of `n` minutes of data type [`IntervalMinute`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalMinute(n)

```

**Arguments**


- `n` — Number of minutes. Integer numbers or string representations thereof, and float numbers. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` minutes. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDate('2025-06-15') AS date,
    toIntervalMinute(12) AS interval_to_minutes
SELECT date + interval_to_minutes AS result

```


```
┌──────────────result─┐
│ 2025-06-15 00:12:00 │
└─────────────────────┘

```

## toIntervalMonth[​](#toIntervalMonth "Direct link to toIntervalMonth")


Introduced in: v1\.1\.0


Returns an interval of `n` months of data type [`IntervalMonth`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalMonth(n)

```

**Arguments**


- `n` — Number of months. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` months. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDate('2025-06-15') AS date,
    toIntervalMonth(1) AS interval_to_month
SELECT date + interval_to_month AS result

```


```
┌─────result─┐
│ 2025-07-15 │
└────────────┘

```

## toIntervalNanosecond[​](#toIntervalNanosecond "Direct link to toIntervalNanosecond")


Introduced in: v22\.6\.0


Returns an interval of `n` nanoseconds of data type [`IntervalNanosecond`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalNanosecond(n)

```

**Arguments**


- `n` — Number of nanoseconds. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` nanoseconds. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDateTime('2025-06-15') AS date,
    toIntervalNanosecond(30) AS interval_to_nanoseconds
SELECT date + interval_to_nanoseconds AS result

```


```
┌────────────────────────result─┐
│ 2025-06-15 00:00:00.000000030 │
└───────────────────────────────┘

```

## toIntervalQuarter[​](#toIntervalQuarter "Direct link to toIntervalQuarter")


Introduced in: v1\.1\.0


Returns an interval of `n` quarters of data type [`IntervalQuarter`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalQuarter(n)

```

**Arguments**


- `n` — Number of quarters. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` quarters. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDate('2025-06-15') AS date,
    toIntervalQuarter(1) AS interval_to_quarter
SELECT date + interval_to_quarter AS result

```


```
┌─────result─┐
│ 2025-09-15 │
└────────────┘

```

## toIntervalSecond[​](#toIntervalSecond "Direct link to toIntervalSecond")


Introduced in: v1\.1\.0


Returns an interval of `n` seconds of data type [`IntervalSecond`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalSecond(n)

```

**Arguments**


- `n` — Number of seconds. Integer numbers or string representations thereof, and float numbers. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` seconds. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDate('2025-06-15') AS date,
    toIntervalSecond(30) AS interval_to_seconds
SELECT date + interval_to_seconds AS result

```


```
┌──────────────result─┐
│ 2025-06-15 00:00:30 │
└─────────────────────┘

```

## toIntervalWeek[​](#toIntervalWeek "Direct link to toIntervalWeek")


Introduced in: v1\.1\.0


Returns an interval of `n` weeks of data type [`IntervalWeek`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalWeek(n)

```

**Arguments**


- `n` — Number of weeks. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` weeks. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDate('2025-06-15') AS date,
    toIntervalWeek(1) AS interval_to_week
SELECT date + interval_to_week AS result

```


```
┌─────result─┐
│ 2025-06-22 │
└────────────┘

```

## toIntervalYear[​](#toIntervalYear "Direct link to toIntervalYear")


Introduced in: v1\.1\.0


Returns an interval of `n` years of data type [`IntervalYear`](/docs/sql-reference/data-types/special-data-types/interval).


**Syntax**



```
toIntervalYear(n)

```

**Arguments**


- `n` — Number of years. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an interval of `n` years. [`Interval`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH
    toDate('2024-06-15') AS date,
    toIntervalYear(1) AS interval_to_year
SELECT date + interval_to_year AS result

```


```
┌─────result─┐
│ 2025-06-15 │
└────────────┘

```

## toLowCardinality[​](#toLowCardinality "Direct link to toLowCardinality")


Introduced in: v18\.12\.0


Converts the input argument to the [LowCardinality](/docs/sql-reference/data-types/lowcardinality) version of same data type.


TipTo convert from the `LowCardinality` data type to a regular data type, use the [CAST](#CAST) function.
For example: `CAST(x AS String)`.


**Syntax**



```
toLowCardinality(expr)

```

**Arguments**


- `expr` — Expression resulting in one of the supported data types. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Date`](/docs/sql-reference/data-types/date) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns the input value converted to the `LowCardinality` data type. [`LowCardinality`](/docs/sql-reference/data-types/lowcardinality)


**Examples**


**Usage example**



```
SELECT toLowCardinality('1')

```


```
┌─toLowCardinality('1')─┐
│ 1                     │
└───────────────────────┘

```

## toString[​](#toString "Direct link to toString")


Introduced in: v1\.1\.0


Converts values to their string representation.
For DateTime arguments, the function can take a second String argument containing the name of the time zone.


**Syntax**



```
toString(value[, timezone])

```

**Arguments**


- `value` — Value to convert to string. [`Any`](/docs/sql-reference/data-types)
- `timezone` — Optional. Timezone name for DateTime conversion. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string representation of the input value. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    now() AS ts,
    time_zone,
    toString(ts, time_zone) AS str_tz_datetime
FROM system.time_zones
WHERE time_zone LIKE 'Europe%'
LIMIT 10

```


```
┌──────────────────ts─┬─time_zone─────────┬─str_tz_datetime─────┐
│ 2023-09-08 19:14:59 │ Europe/Amsterdam  │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Andorra    │ 2023-09-08 21:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Astrakhan  │ 2023-09-08 23:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Athens     │ 2023-09-08 22:14:59 │
│ 2023-09-08 19:14:59 │ Europe/Belfast    │ 2023-09-08 20:14:59 │
└─────────────────────┴───────────────────┴─────────────────────┘

```

## toStringCutToZero[​](#toStringCutToZero "Direct link to toStringCutToZero")


Introduced in: v1\.1\.0


Accepts a [String](/docs/sql-reference/data-types/string) or [FixedString](/docs/sql-reference/data-types/fixedstring) argument and returns a String that contains a copy of the original string truncated at the first null byte.


Null bytes (\\0\) are considered as string terminators.
This function is useful for processing C\-style strings or binary data where null bytes mark the end of meaningful content.


**Syntax**



```
toStringCutToZero(s)

```

**Arguments**


- `s` — String or FixedString to process. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


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


Converts an input value to a value of type Time64 but returns `00:00:00.000` in case of an error.
Like [`toTime64`](#toTime64) but returns `00:00:00.000` instead of throwing an exception on conversion errors.


**Syntax**



```
toTime64OrZero(x)

```

**Arguments**


- `x` — A string representation of a time with subsecond precision. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Time64 value if successful, otherwise `00:00:00.000`. [`Time64`](/docs/sql-reference/data-types/time64)


**Examples**


**Usage example**



```
SELECT toTime64OrZero('12:30:45.123'), toTime64OrZero('invalid')

```


```
┌─toTime64OrZero('12:30:45.123')─┬─toTime64OrZero('invalid')─┐
│                   12:30:45.123 │             00:00:00.000 │
└────────────────────────────────┴──────────────────────────┘

```

## toTimeOrNull[​](#toTimeOrNull "Direct link to toTimeOrNull")


Introduced in: v1\.1\.0


Converts an input value to a value of type Time but returns `NULL` in case of an error.
Like [`toTime`](#toTime) but returns `NULL` instead of throwing an exception on conversion errors.


See also:


- [`toTime`](#toTime)
- [`toTimeOrZero`](#toTimeOrZero)


**Syntax**



```
toTimeOrNull(x)

```

**Arguments**


- `x` — A string representation of a time. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Time value if successful, otherwise `NULL`. [`Time`](/docs/sql-reference/data-types/time) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT toTimeOrNull('12:30:45'), toTimeOrNull('invalid')

```


```
┌─toTimeOrNull('12:30:45')─┬─toTimeOrNull('invalid')─┐
│                 12:30:45 │                    ᴺᵁᴸᴸ │
└──────────────────────────┴─────────────────────────┘

```

## toTimeOrZero[​](#toTimeOrZero "Direct link to toTimeOrZero")


Introduced in: v1\.1\.0


Converts an input value to a value of type Time but returns `00:00:00` in case of an error.
Like toTime but returns `00:00:00` instead of throwing an exception on conversion errors.


**Syntax**



```
toTimeOrZero(x)

```

**Arguments**


- `x` — A string representation of a time. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Time value if successful, otherwise `00:00:00`. [`Time`](/docs/sql-reference/data-types/time)


**Examples**


**Usage example**



```
SELECT toTimeOrZero('12:30:45'), toTimeOrZero('invalid')

```


```
┌─toTimeOrZero('12:30:45')─┬─toTimeOrZero('invalid')─┐
│                 12:30:45 │                00:00:00 │
└──────────────────────────┴─────────────────────────┘

```

## toUInt128[​](#toUInt128 "Direct link to toUInt128")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`UInt128`](/docs/sql-reference/functions/type-conversion-functions#toUInt128).
Throws an exception in case of an error.
The function uses rounding towards zero, meaning it truncates fractional digits of numbers.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt128('0xc0fe');`.


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


**Usage example**



```
SELECT
    toUInt128OrNull('128'),
    toUInt128OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt128OrNull('128'): 128
toUInt128OrNull('abc'): \N

```

## toUInt128OrZero[​](#toUInt128OrZero "Direct link to toUInt128OrZero")


Introduced in: v1\.1\.0


Like [`toUInt128`](#toUInt128), this function converts an input value to a value of type [`UInt128`](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `0`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt128OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt128`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt128`](#toUInt128).
- [`toUInt128OrNull`](#toUInt128OrNull).
- [`toUInt128OrDefault`](#toUInt128OrDefault).


**Syntax**



```
toUInt128OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt128, otherwise `0` if the conversion is unsuccessful. [`UInt128`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt128OrZero('128'),
    toUInt128OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt128OrZero('128'): 128
toUInt128OrZero('abc'): 0

```

## toUInt16[​](#toUInt16 "Direct link to toUInt16")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`UInt16`](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt16('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt16`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.
For example: `SELECT toUInt16(65536) == 0;`.


NoteThe function uses [rounding towards zero](https://en.wikipedia.org/wiki/Rounding#Rounding_towards_zero), meaning it truncates fractional digits of numbers.


See also:


- [`toUInt16OrZero`](#toUInt16OrZero).
- [`toUInt16OrNull`](#toUInt16OrNull).
- [`toUInt16OrDefault`](#toUInt16OrDefault).


**Syntax**



```
toUInt16(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 16\-bit unsigned integer value. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt16(16),
    toUInt16(16.16),
    toUInt16('16')
FORMAT Vertical

```


```
Row 1:
──────
toUInt16(16):    16
toUInt16(16.16): 16
toUInt16('16'):  16

```

## toUInt16OrDefault[​](#toUInt16OrDefault "Direct link to toUInt16OrDefault")


Introduced in: v21\.11\.0


Like [`toUInt16`](#toUInt16), this function converts an input value to a value of type [UInt16](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toUInt16OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type UInt16 if successful, otherwise returns the default value if passed, or 0 if not. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toUInt16OrDefault('16', CAST('0', 'UInt16'))

```


```
16

```

**Failed conversion**



```
SELECT toUInt16OrDefault('abc', CAST('0', 'UInt16'))

```


```
0

```

## toUInt16OrNull[​](#toUInt16OrNull "Direct link to toUInt16OrNull")


Introduced in: v1\.1\.0


Like [`toUInt16`](#toUInt16), this function converts an input value to a value of type [`UInt16`](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int8/16/32/128/256\.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt16OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt16`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt16`](#toUInt16).
- [`toUInt16OrZero`](#toUInt16OrZero).
- [`toUInt16OrDefault`](#toUInt16OrDefault).


**Syntax**



```
toUInt16OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type `UInt16`, otherwise `NULL` if the conversion is unsuccessful. [`UInt16`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toUInt16OrNull('16'),
    toUInt16OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt16OrNull('16'):  16
toUInt16OrNull('abc'): \N

```

## toUInt16OrZero[​](#toUInt16OrZero "Direct link to toUInt16OrZero")


Introduced in: v1\.1\.0


Like [`toUInt16`](#toUInt16), this function converts an input value to a value of type [`UInt16`](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int8/16/32/128/256\.


Unsupported arguments (return `0`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt16OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt16`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt16`](#toUInt16).
- [`toUInt16OrNull`](#toUInt16OrNull).
- [`toUInt16OrDefault`](#toUInt16OrDefault).


**Syntax**



```
toUInt16OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt16, otherwise `0` if the conversion is unsuccessful. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt16OrZero('16'),
    toUInt16OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt16OrZero('16'):  16
toUInt16OrZero('abc'): 0

```

## toUInt256[​](#toUInt256 "Direct link to toUInt256")


Introduced in: v1\.1\.0


Converts an input value to a value of type UInt256\.
Throws an exception in case of an error.
The function uses rounding towards zero, meaning it truncates fractional digits of numbers.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt256('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of UInt256, the result over or under flows.
This is not considered an error.


See also:


- [`toUInt256OrZero`](#toUInt256OrZero).
- [`toUInt256OrNull`](#toUInt256OrNull).
- [`toUInt256OrDefault`](#toUInt256OrDefault).


**Syntax**



```
toUInt256(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 256\-bit unsigned integer value. [`UInt256`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt256(256),
    toUInt256(256.256),
    toUInt256('256')
FORMAT Vertical

```


```
Row 1:
──────
toUInt256(256):     256
toUInt256(256.256): 256
toUInt256('256'):   256

```

## toUInt256OrDefault[​](#toUInt256OrDefault "Direct link to toUInt256OrDefault")


Introduced in: v21\.11\.0


Like [`toUInt256`](#toUInt256), this function converts an input value to a value of type [UInt256](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toUInt256OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`UInt256`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type UInt256 if successful, otherwise returns the default value if passed, or 0 if not. [`UInt256`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toUInt256OrDefault('-256', CAST('0', 'UInt256'))

```


```
0

```

**Failed conversion**



```
SELECT toUInt256OrDefault('abc', CAST('0', 'UInt256'))

```


```
0

```

## toUInt256OrNull[​](#toUInt256OrNull "Direct link to toUInt256OrNull")


Introduced in: v20\.8\.0


Like [`toUInt256`](#toUInt256), this function converts an input value to a value of type [`UInt256`](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt256OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt256`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt256`](#toUInt256).
- [`toUInt256OrZero`](#toUInt256OrZero).
- [`toUInt256OrDefault`](#toUInt256OrDefault).


**Syntax**



```
toUInt256OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt256, otherwise `NULL` if the conversion is unsuccessful. [`UInt256`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toUInt256OrNull('256'),
    toUInt256OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt256OrNull('256'): 256
toUInt256OrNull('abc'): \N

```

## toUInt256OrZero[​](#toUInt256OrZero "Direct link to toUInt256OrZero")


Introduced in: v20\.8\.0


Like [`toUInt256`](#toUInt256), this function converts an input value to a value of type [`UInt256`](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `0`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt256OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt256`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt256`](#toUInt256).
- [`toUInt256OrNull`](#toUInt256OrNull).
- [`toUInt256OrDefault`](#toUInt256OrDefault).


**Syntax**



```
toUInt256OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt256, otherwise `0` if the conversion is unsuccessful. [`UInt256`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt256OrZero('256'),
    toUInt256OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt256OrZero('256'): 256
toUInt256OrZero('abc'): 0

```

## toUInt32[​](#toUInt32 "Direct link to toUInt32")


Introduced in: v1\.1\.0


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


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt32OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt32`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt32`](#toUInt32).
- [`toUInt32OrZero`](#toUInt32OrZero).
- [`toUInt32OrDefault`](#toUInt32OrDefault).


**Syntax**



```
toUInt32OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type `UInt32`, otherwise `NULL` if the conversion is unsuccessful. [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toUInt32OrNull('32'),
    toUInt32OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt32OrNull('32'):  32
toUInt32OrNull('abc'): \N

```

## toUInt32OrZero[​](#toUInt32OrZero "Direct link to toUInt32OrZero")


Introduced in: v1\.1\.0


Like [`toUInt32`](#toUInt32), this function converts an input value to a value of type [`UInt32`](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int8/16/32/128/256\.


Unsupported arguments (return `0`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt32OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt32`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt32`](#toUInt32).
- [`toUInt32OrNull`](#toUInt32OrNull).
- [`toUInt32OrDefault`](#toUInt32OrDefault).


**Syntax**



```
toUInt32OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt32, otherwise `0` if the conversion is unsuccessful. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt32OrZero('32'),
    toUInt32OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt32OrZero('32'):  32
toUInt32OrZero('abc'): 0

```

## toUInt64[​](#toUInt64 "Direct link to toUInt64")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`UInt64`](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported types:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt64('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt64`](/docs/sql-reference/data-types/int-uint), the result over or under flows.
This is not considered an error.
For example: `SELECT toUInt64(18446744073709551616) == 0;`


NoteThe function uses [rounding towards zero](https://en.wikipedia.org/wiki/Rounding#Rounding_towards_zero), meaning it truncates fractional digits of numbers.


See also:


- [`toUInt64OrZero`](#toUInt64OrZero).
- [`toUInt64OrNull`](#toUInt64OrNull).
- [`toUInt64OrDefault`](#toUInt64OrDefault).


**Syntax**



```
toUInt64(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns a 64\-bit unsigned integer value. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt64(64),
    toUInt64(64.64),
    toUInt64('64')
FORMAT Vertical

```


```
Row 1:
──────
toUInt64(64):    64
toUInt64(64.64): 64
toUInt64('64'):  64

```

## toUInt64OrDefault[​](#toUInt64OrDefault "Direct link to toUInt64OrDefault")


Introduced in: v21\.11\.0


Like [`toUInt64`](#toUInt64), this function converts an input value to a value of type [UInt64](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toUInt64OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type UInt64 if successful, otherwise returns the default value if passed, or 0 if not. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toUInt64OrDefault('64', CAST('0', 'UInt64'))

```


```
64

```

**Failed conversion**



```
SELECT toUInt64OrDefault('abc', CAST('0', 'UInt64'))

```


```
0

```

## toUInt64OrNull[​](#toUInt64OrNull "Direct link to toUInt64OrNull")


Introduced in: v1\.1\.0


Like [`toUInt64`](#toUInt64), this function converts an input value to a value of type [`UInt64`](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `NULL`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt64OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt64`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt64`](#toUInt64).
- [`toUInt64OrZero`](#toUInt64OrZero).
- [`toUInt64OrDefault`](#toUInt64OrDefault).


**Syntax**



```
toUInt64OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt64, otherwise `NULL` if the conversion is unsuccessful. [`UInt64`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toUInt64OrNull('64'),
    toUInt64OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt64OrNull('64'):  64
toUInt64OrNull('abc'): \N

```

## toUInt64OrZero[​](#toUInt64OrZero "Direct link to toUInt64OrZero")


Introduced in: v1\.1\.0


Like [`toUInt64`](#toUInt64), this function converts an input value to a value of type [`UInt64`](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int\*.


Unsupported arguments (return `0`):


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt64OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt64`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt64`](#toUInt64).
- [`toUInt64OrNull`](#toUInt64OrNull).
- [`toUInt64OrDefault`](#toUInt64OrDefault).


**Syntax**



```
toUInt64OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt64, otherwise `0` if the conversion is unsuccessful. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt64OrZero('64'),
    toUInt64OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt64OrZero('64'):  64
toUInt64OrZero('abc'): 0

```

## toUInt8[​](#toUInt8 "Direct link to toUInt8")


Introduced in: v1\.1\.0


Converts an input value to a value of type [`UInt8`](/docs/sql-reference/data-types/int-uint).
Throws an exception in case of an error.


Supported arguments:


- Values or string representations of type (U)Int\*.
- Values of type Float\*.


Unsupported arguments:


- String representations of Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt8('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [UInt8](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.
For example: `SELECT toUInt8(256) == 0;`.


NoteThe function uses [rounding towards zero](https://en.wikipedia.org/wiki/Rounding#Rounding_towards_zero), meaning it truncates fractional digits of numbers.


See also:


- [`toUInt8OrZero`](#toUInt8OrZero).
- [`toUInt8OrNull`](#toUInt8OrNull).
- [`toUInt8OrDefault`](#toUInt8OrDefault).


**Syntax**



```
toUInt8(expr)

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression)


**Returned value**


Returns an 8\-bit unsigned integer value. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt8(8),
    toUInt8(8.8),
    toUInt8('8')
FORMAT Vertical

```


```
Row 1:
──────
toUInt8(8):   8
toUInt8(8.8): 8
toUInt8('8'): 8

```

## toUInt8OrDefault[​](#toUInt8OrDefault "Direct link to toUInt8OrDefault")


Introduced in: v21\.11\.0


Like [`toUInt8`](#toUInt8), this function converts an input value to a value of type [UInt8](/docs/sql-reference/data-types/int-uint) but returns the default value in case of an error.
If no `default` value is passed then `0` is returned in case of an error.


**Syntax**



```
toUInt8OrDefault(expr[, default])

```

**Arguments**


- `expr` — Expression returning a number or a string representation of a number. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)
- `default` — Optional. The default value to return if parsing is unsuccessful. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a value of type UInt8 if successful, otherwise returns the default value if passed, or 0 if not. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Successful conversion**



```
SELECT toUInt8OrDefault('8', CAST('0', 'UInt8'))

```


```
8

```

**Failed conversion**



```
SELECT toUInt8OrDefault('abc', CAST('0', 'UInt8'))

```


```
0

```

## toUInt8OrNull[​](#toUInt8OrNull "Direct link to toUInt8OrNull")


Introduced in: v1\.1\.0


Like [`toUInt8`](#toUInt8), this function converts an input value to a value of type [`UInt8`](/docs/sql-reference/data-types/int-uint) but returns `NULL` in case of an error.


Supported arguments:


- String representations of (U)Int8/16/32/128/256\.


Unsupported arguments (return `NULL`):


- String representations of ordinary Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt8OrNull('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt8`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt8`](#toUInt8).
- [`toUInt8OrZero`](#toUInt8OrZero).
- [`toUInt8OrDefault`](#toUInt8OrDefault).


**Syntax**



```
toUInt8OrNull(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt8, otherwise `NULL` if the conversion is unsuccessful. [`UInt8`](/docs/sql-reference/data-types/int-uint) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
SELECT
    toUInt8OrNull('42'),
    toUInt8OrNull('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt8OrNull('42'):  42
toUInt8OrNull('abc'): \N

```

## toUInt8OrZero[​](#toUInt8OrZero "Direct link to toUInt8OrZero")


Introduced in: v1\.1\.0


Like [`toUInt8`](#toUInt8), this function converts an input value to a value of type [`UInt8`](/docs/sql-reference/data-types/int-uint) but returns `0` in case of an error.


Supported arguments:


- String representations of (U)Int8/16/32/128/256\.


Unsupported arguments (return `0`):


- String representations of ordinary Float\* values, including `NaN` and `Inf`.
- String representations of binary and hexadecimal values, e.g. `SELECT toUInt8OrZero('0xc0fe');`.


NoteIf the input value cannot be represented within the bounds of [`UInt8`](/docs/sql-reference/data-types/int-uint), overflow or underflow of the result occurs.
This is not considered an error.


See also:


- [`toUInt8`](#toUInt8).
- [`toUInt8OrNull`](#toUInt8OrNull).
- [`toUInt8OrDefault`](#toUInt8OrDefault).


**Syntax**



```
toUInt8OrZero(x)

```

**Arguments**


- `x` — A String representation of a number. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a value of type UInt8, otherwise `0` if the conversion is unsuccessful. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT
    toUInt8OrZero('-8'),
    toUInt8OrZero('abc')
FORMAT Vertical

```


```
Row 1:
──────
toUInt8OrZero('-8'):  0
toUInt8OrZero('abc'): 0

```

## toUUID[​](#toUUID "Direct link to toUUID")


Introduced in: v1\.1\.0


Converts a String value to a UUID value.


**Syntax**



```
toUUID(string)

```

**Arguments**


- `string` — UUID as a string. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns a UUID from the string representation of the UUID. [`UUID`](/docs/sql-reference/data-types/uuid)


**Examples**


**Usage example**



```
SELECT toUUID('61f0c404-5cb3-11e7-907b-a6006ad3dba0') AS uuid

```


```
┌─────────────────────────────────uuid─┐
│ 61f0c404-5cb3-11e7-907b-a6006ad3dba0 │
└──────────────────────────────────────┘

```

## toUUIDOrZero[​](#toUUIDOrZero "Direct link to toUUIDOrZero")


Introduced in: v20\.12\.0


Converts an input value to a value of type [UUID](/docs/sql-reference/data-types/uuid) but returns zero UUID in case of an error.
Like [`toUUID`](/docs/sql-reference/functions/type-conversion-functions#toUUID) but returns zero UUID (`00000000-0000-0000-0000-000000000000`) instead of throwing an exception on conversion errors.


Supported arguments:


- String representations of UUID in standard format (8\-4\-4\-4\-12 hexadecimal digits).
- String representations of UUID without hyphens (32 hexadecimal digits).


Unsupported arguments (return zero UUID):


- Invalid string formats.
- Non\-string types.


**Syntax**



```
toUUIDOrZero(x)

```

**Arguments**


- `x` — A string representation of a UUID. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a UUID value if successful, otherwise zero UUID (`00000000-0000-0000-0000-000000000000`). [`UUID`](/docs/sql-reference/data-types/uuid)


**Examples**


**Usage example**



```
SELECT
    toUUIDOrZero('550e8400-e29b-41d4-a716-446655440000') AS valid_uuid,
    toUUIDOrZero('invalid-uuid') AS invalid_uuid

```


```
┌─valid_uuid───────────────────────────┬─invalid_uuid─────────────────────────┐
│ 550e8400-e29b-41d4-a716-446655440000 │ 00000000-0000-0000-0000-000000000000 │
└──────────────────────────────────────┴──────────────────────────────────────┘

```

## toUnixTimestamp64Micro[​](#toUnixTimestamp64Micro "Direct link to toUnixTimestamp64Micro")


Introduced in: v20\.5\.0


Converts a [`DateTime64`](/docs/sql-reference/data-types/datetime64) to a [`Int64`](/docs/sql-reference/data-types/int-uint) value with fixed microsecond precision.
The input value is scaled up or down appropriately depending on its precision.


NoteThe output value is relative to UTC, not to the timezone of the input value.


**Syntax**



```
toUnixTimestamp64Micro(value)

```

**Arguments**


- `value` — DateTime64 value with any precision. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Returned value**


Returns a Unix timestamp in microseconds. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH toDateTime64('2025-02-13 23:31:31.011123', 6, 'UTC') AS dt64
SELECT toUnixTimestamp64Micro(dt64);

```


```
┌─toUnixTimestamp64Micro(dt64)─┐
│               1739489491011123 │
└────────────────────────────────┘

```

## toUnixTimestamp64Milli[​](#toUnixTimestamp64Milli "Direct link to toUnixTimestamp64Milli")


Introduced in: v20\.5\.0


Converts a [`DateTime64`](/docs/sql-reference/data-types/datetime64) to a [`Int64`](/docs/sql-reference/data-types/int-uint) value with fixed millisecond precision.
The input value is scaled up or down appropriately depending on its precision.


NoteThe output value is relative to UTC, not to the timezone of the input value.


**Syntax**



```
toUnixTimestamp64Milli(value)

```

**Arguments**


- `value` — DateTime64 value with any precision. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Returned value**


Returns a Unix timestamp in milliseconds. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH toDateTime64('2025-02-13 23:31:31.011', 3, 'UTC') AS dt64
SELECT toUnixTimestamp64Milli(dt64);

```


```
┌─toUnixTimestamp64Milli(dt64)─┐
│                1739489491011 │
└──────────────────────────────┘

```

## toUnixTimestamp64Nano[​](#toUnixTimestamp64Nano "Direct link to toUnixTimestamp64Nano")


Introduced in: v20\.5\.0


Converts a [`DateTime64`](/docs/sql-reference/data-types/datetime64) to a [`Int64`](/docs/sql-reference/functions/type-conversion-functions#toInt64) value with fixed nanosecond precision.
The input value is scaled up or down appropriately depending on its precision.


NoteThe output value is relative to UTC, not to the timezone of the input value.


**Syntax**



```
toUnixTimestamp64Nano(value)

```

**Arguments**


- `value` — DateTime64 value with any precision. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Returned value**


Returns a Unix timestamp in nanoseconds. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH toDateTime64('2025-02-13 23:31:31.011123456', 9, 'UTC') AS dt64
SELECT toUnixTimestamp64Nano(dt64);

```


```
┌─toUnixTimestamp64Nano(dt64)────┐
│            1739489491011123456 │
└────────────────────────────────┘

```

## toUnixTimestamp64Second[​](#toUnixTimestamp64Second "Direct link to toUnixTimestamp64Second")


Introduced in: v24\.12\.0


Converts a [`DateTime64`](/docs/sql-reference/data-types/datetime64) to a [`Int64`](/docs/sql-reference/data-types/int-uint) value with fixed second precision.
The input value is scaled up or down appropriately depending on its precision.


NoteThe output value is relative to UTC, not to the timezone of the input value.


**Syntax**



```
toUnixTimestamp64Second(value)

```

**Arguments**


- `value` — DateTime64 value with any precision. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Returned value**


Returns a Unix timestamp in seconds. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH toDateTime64('2025-02-13 23:31:31.011', 3, 'UTC') AS dt64
SELECT toUnixTimestamp64Second(dt64);

```


```
┌─toUnixTimestamp64Second(dt64)─┐
│                    1739489491 │
└───────────────────────────────┘

```
[PreviousMaps](/docs/sql-reference/functions/tuple-map-functions)[NextUDF](/docs/sql-reference/functions/udf)- [Common issues with data conversion](#common-issues-with-data-conversion)- [Notes on `toString` functions](#to-string-functions)- [Notes on `toDate`/`toDateTime` functions](#to-date-and-date-time-functions)- [CAST](#CAST)- [DATE](#DATE)- [accurateCast](#accurateCast)- [accurateCastOrDefault](#accurateCastOrDefault)- [accurateCastOrNull](#accurateCastOrNull)- [formatRow](#formatRow)- [formatRowNoNewline](#formatRowNoNewline)- [fromUnixTimestamp64Micro](#fromUnixTimestamp64Micro)- [fromUnixTimestamp64Milli](#fromUnixTimestamp64Milli)- [fromUnixTimestamp64Nano](#fromUnixTimestamp64Nano)- [fromUnixTimestamp64Second](#fromUnixTimestamp64Second)- [parseDateTime](#parseDateTime)- [parseDateTime32BestEffort](#parseDateTime32BestEffort)- [parseDateTime32BestEffortOrNull](#parseDateTime32BestEffortOrNull)- [parseDateTime32BestEffortOrZero](#parseDateTime32BestEffortOrZero)- [parseDateTime64](#parseDateTime64)- [parseDateTime64BestEffort](#parseDateTime64BestEffort)- [parseDateTime64BestEffortOrNull](#parseDateTime64BestEffortOrNull)- [parseDateTime64BestEffortOrZero](#parseDateTime64BestEffortOrZero)- [parseDateTime64BestEffortUS](#parseDateTime64BestEffortUS)- [parseDateTime64BestEffortUSOrNull](#parseDateTime64BestEffortUSOrNull)- [parseDateTime64BestEffortUSOrZero](#parseDateTime64BestEffortUSOrZero)- [parseDateTime64InJodaSyntax](#parseDateTime64InJodaSyntax)- [parseDateTime64InJodaSyntaxOrNull](#parseDateTime64InJodaSyntaxOrNull)- [parseDateTime64InJodaSyntaxOrZero](#parseDateTime64InJodaSyntaxOrZero)- [parseDateTime64OrNull](#parseDateTime64OrNull)- [parseDateTime64OrZero](#parseDateTime64OrZero)- [parseDateTimeBestEffort](#parseDateTimeBestEffort)- [parseDateTimeBestEffortOrNull](#parseDateTimeBestEffortOrNull)- [parseDateTimeBestEffortOrZero](#parseDateTimeBestEffortOrZero)- [parseDateTimeBestEffortUS](#parseDateTimeBestEffortUS)- [parseDateTimeBestEffortUSOrNull](#parseDateTimeBestEffortUSOrNull)- [parseDateTimeBestEffortUSOrZero](#parseDateTimeBestEffortUSOrZero)- [parseDateTimeInJodaSyntax](#parseDateTimeInJodaSyntax)- [parseDateTimeInJodaSyntaxOrNull](#parseDateTimeInJodaSyntaxOrNull)- [parseDateTimeInJodaSyntaxOrZero](#parseDateTimeInJodaSyntaxOrZero)- [parseDateTimeOrNull](#parseDateTimeOrNull)- [parseDateTimeOrZero](#parseDateTimeOrZero)- [reinterpret](#reinterpret)- [reinterpretAsDate](#reinterpretAsDate)- [reinterpretAsDateTime](#reinterpretAsDateTime)- [reinterpretAsFixedString](#reinterpretAsFixedString)- [reinterpretAsFloat32](#reinterpretAsFloat32)- [reinterpretAsFloat64](#reinterpretAsFloat64)- [reinterpretAsInt128](#reinterpretAsInt128)- [reinterpretAsInt16](#reinterpretAsInt16)- [reinterpretAsInt256](#reinterpretAsInt256)- [reinterpretAsInt32](#reinterpretAsInt32)- [reinterpretAsInt64](#reinterpretAsInt64)- [reinterpretAsInt8](#reinterpretAsInt8)- [reinterpretAsString](#reinterpretAsString)- [reinterpretAsUInt128](#reinterpretAsUInt128)- [reinterpretAsUInt16](#reinterpretAsUInt16)- [reinterpretAsUInt256](#reinterpretAsUInt256)- [reinterpretAsUInt32](#reinterpretAsUInt32)- [reinterpretAsUInt64](#reinterpretAsUInt64)- [reinterpretAsUInt8](#reinterpretAsUInt8)- [reinterpretAsUUID](#reinterpretAsUUID)- [toBFloat16](#toBFloat16)- [toBFloat16OrNull](#toBFloat16OrNull)- [toBFloat16OrZero](#toBFloat16OrZero)- [toBool](#toBool)- [toDate](#toDate)- [toDate32](#toDate32)- [toDate32OrDefault](#toDate32OrDefault)- [toDate32OrNull](#toDate32OrNull)- [toDate32OrZero](#toDate32OrZero)- [toDateOrDefault](#toDateOrDefault)- [toDateOrNull](#toDateOrNull)- [toDateOrZero](#toDateOrZero)- [toDateTime](#toDateTime)- [toDateTime32](#toDateTime32)- [toDateTime64](#toDateTime64)- [toDateTime64OrDefault](#toDateTime64OrDefault)- [toDateTime64OrNull](#toDateTime64OrNull)- [toDateTime64OrZero](#toDateTime64OrZero)- [toDateTimeOrDefault](#toDateTimeOrDefault)- [toDateTimeOrNull](#toDateTimeOrNull)- [toDateTimeOrZero](#toDateTimeOrZero)- [toDecimal128](#toDecimal128)- [toDecimal128OrDefault](#toDecimal128OrDefault)- [toDecimal128OrNull](#toDecimal128OrNull)- [toDecimal128OrZero](#toDecimal128OrZero)- [toDecimal256](#toDecimal256)- [toDecimal256OrDefault](#toDecimal256OrDefault)- [toDecimal256OrNull](#toDecimal256OrNull)- [toDecimal256OrZero](#toDecimal256OrZero)- [toDecimal32](#toDecimal32)- [toDecimal32OrDefault](#toDecimal32OrDefault)- [toDecimal32OrNull](#toDecimal32OrNull)- [toDecimal32OrZero](#toDecimal32OrZero)- [toDecimal64](#toDecimal64)- [toDecimal64OrDefault](#toDecimal64OrDefault)- [toDecimal64OrNull](#toDecimal64OrNull)- [toDecimal64OrZero](#toDecimal64OrZero)- [toDecimalString](#toDecimalString)- [toFixedString](#toFixedString)- [toFloat32](#toFloat32)- [toFloat32OrDefault](#toFloat32OrDefault)- [toFloat32OrNull](#toFloat32OrNull)- [toFloat32OrZero](#toFloat32OrZero)- [toFloat64](#toFloat64)- [toFloat64OrDefault](#toFloat64OrDefault)- [toFloat64OrNull](#toFloat64OrNull)- [toFloat64OrZero](#toFloat64OrZero)- [toInt128](#toInt128)- [toInt128OrDefault](#toInt128OrDefault)- [toInt128OrNull](#toInt128OrNull)- [toInt128OrZero](#toInt128OrZero)- [toInt16](#toInt16)- [toInt16OrDefault](#toInt16OrDefault)- [toInt16OrNull](#toInt16OrNull)- [toInt16OrZero](#toInt16OrZero)- [toInt256](#toInt256)- [toInt256OrDefault](#toInt256OrDefault)- [toInt256OrNull](#toInt256OrNull)- [toInt256OrZero](#toInt256OrZero)- [toInt32](#toInt32)- [toInt32OrDefault](#toInt32OrDefault)- [toInt32OrNull](#toInt32OrNull)- [toInt32OrZero](#toInt32OrZero)- [toInt64](#toInt64)- [toInt64OrDefault](#toInt64OrDefault)- [toInt64OrNull](#toInt64OrNull)- [toInt64OrZero](#toInt64OrZero)- [toInt8](#toInt8)- [toInt8OrDefault](#toInt8OrDefault)- [toInt8OrNull](#toInt8OrNull)- [toInt8OrZero](#toInt8OrZero)- [toInterval](#toInterval)- [toIntervalDay](#toIntervalDay)- [toIntervalHour](#toIntervalHour)- [toIntervalMicrosecond](#toIntervalMicrosecond)- [toIntervalMillisecond](#toIntervalMillisecond)- [toIntervalMinute](#toIntervalMinute)- [toIntervalMonth](#toIntervalMonth)- [toIntervalNanosecond](#toIntervalNanosecond)- [toIntervalQuarter](#toIntervalQuarter)- [toIntervalSecond](#toIntervalSecond)- [toIntervalWeek](#toIntervalWeek)- [toIntervalYear](#toIntervalYear)- [toLowCardinality](#toLowCardinality)- [toString](#toString)- [toStringCutToZero](#toStringCutToZero)- [toTime](#toTime)- [toTime64](#toTime64)- [toTime64OrNull](#toTime64OrNull)- [toTime64OrZero](#toTime64OrZero)- [toTimeOrNull](#toTimeOrNull)- [toTimeOrZero](#toTimeOrZero)- [toUInt128](#toUInt128)- [toUInt128OrDefault](#toUInt128OrDefault)- [toUInt128OrNull](#toUInt128OrNull)- [toUInt128OrZero](#toUInt128OrZero)- [toUInt16](#toUInt16)- [toUInt16OrDefault](#toUInt16OrDefault)- [toUInt16OrNull](#toUInt16OrNull)- [toUInt16OrZero](#toUInt16OrZero)- [toUInt256](#toUInt256)- [toUInt256OrDefault](#toUInt256OrDefault)- [toUInt256OrNull](#toUInt256OrNull)- [toUInt256OrZero](#toUInt256OrZero)- [toUInt32](#toUInt32)- [toUInt32OrDefault](#toUInt32OrDefault)- [toUInt32OrNull](#toUInt32OrNull)- [toUInt32OrZero](#toUInt32OrZero)- [toUInt64](#toUInt64)- [toUInt64OrDefault](#toUInt64OrDefault)- [toUInt64OrNull](#toUInt64OrNull)- [toUInt64OrZero](#toUInt64OrZero)- [toUInt8](#toUInt8)- [toUInt8OrDefault](#toUInt8OrDefault)- [toUInt8OrNull](#toUInt8OrNull)- [toUInt8OrZero](#toUInt8OrZero)- [toUUID](#toUUID)- [toUUIDOrZero](#toUUIDOrZero)- [toUnixTimestamp64Micro](#toUnixTimestamp64Micro)- [toUnixTimestamp64Milli](#toUnixTimestamp64Milli)- [toUnixTimestamp64Nano](#toUnixTimestamp64Nano)- [toUnixTimestamp64Second](#toUnixTimestamp64Second)
Was this page helpful?
