# Functions for Working with UUIDs \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- UUIDs
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/uuid-functions.md)# Functions for working with UUIDs


## UUIDv7 generation[​](#uuidv7-generation "Direct link to UUIDv7 generation")


The generated UUID contains a 48\-bit timestamp in Unix milliseconds, followed by version "7" (4 bits), a counter (42 bits) to distinguish UUIDs within a millisecond (including a variant field "2", 2 bits), and a random field (32 bits).
For any given timestamp (`unix_ts_ms`), the counter starts at a random value and is incremented by 1 for each new UUID until the timestamp changes. In case the counter overflows, the timestamp field is incremented by 1 and the counter is reset to a random new start value.
The UUID generation functions guarantee that the counter field within a timestamp increments monotonically across all function invocations in concurrently running threads and queries.



```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
|                           unix_ts_ms                          |
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
|          unix_ts_ms           |  ver  |   counter_high_bits   |
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
|var|                   counter_low_bits                        |
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
|                            rand_b                             |
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘

```

## Snowflake ID generation[​](#snowflake-id-generation "Direct link to Snowflake ID generation")


The generated Snowflake ID contains the current Unix timestamp in milliseconds (41 \+ 1 top zero bits), followed by a machine id (10 bits), and a counter (12 bits) to distinguish IDs within a millisecond. For any given timestamp (`unix_ts_ms`), the counter starts at 0 and is incremented by 1 for each new Snowflake ID until the timestamp changes. In case the counter overflows, the timestamp field is incremented by 1 and the counter is reset to 0\.


NoteThe generated Snowflake IDs are based on the UNIX epoch 1970\-01\-01\. While no standard or recommendation exists for the epoch of Snowflake IDs, implementations in other systems may use a different epoch, e.g. Twitter/X (2010\-11\-04\) or Mastodon (2015\-01\-01\).



```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
|0|                         timestamp                           |
├─┼                 ┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
|                   |     machine_id    |    machine_seq_num    |
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘

```

## UUIDNumToString[​](#UUIDNumToString "Direct link to UUIDNumToString")


Introduced in: v1\.1\.0


Takes a binary representation of a UUID, with its format optionally specified by `variant` (`Big-endian` by default), and returns a string containing 36 characters in text format.


**Syntax**



```
UUIDNumToString(binary[, variant])

```

**Arguments**


- `binary` — Binary representation of a UUID. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)
- `variant` — Variant as specified by [RFC4122](https://datatracker.ietf.org/doc/html/rfc4122#section-4.1.1). 1 \= `Big-endian` (default), 2 \= `Microsoft`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the UUID as a string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    'a/<@];!~p{jTj={)' AS bytes,
    UUIDNumToString(toFixedString(bytes, 16)) AS uuid

```


```
┌─bytes────────────┬─uuid─────────────────────────────────┐
│ a/<@];!~p{jTj={) │ 612f3c40-5d3b-217e-707b-6a546a3d7b29 │
└──────────────────┴──────────────────────────────────────┘

```

**Microsoft variant**



```
SELECT
    '@</a;]~!p{jTj={)' AS bytes,
    UUIDNumToString(toFixedString(bytes, 16), 2) AS uuid

```


```
┌─bytes────────────┬─uuid─────────────────────────────────┐
│ @</a;]~!p{jTj={) │ 612f3c40-5d3b-217e-707b-6a546a3d7b29 │
└──────────────────┴──────────────────────────────────────┘

```

## UUIDStringToNum[​](#UUIDStringToNum "Direct link to UUIDStringToNum")


Introduced in: v1\.1\.0


Accepts a string containing 36 characters in the format `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`, and returns a [FixedString(16\)](/docs/sql-reference/data-types/fixedstring) as its binary representation, with its format optionally specified by `variant` (`Big-endian` by default).


**Syntax**



```
UUIDStringToNum(string[, variant = 1])

```

**Arguments**


- `string` — A string or fixed\-string of 36 characters) [`String`](/docs/sql-reference/data-types/string) or [`FixedString(36)`](/docs/sql-reference/data-types/fixedstring)
- `variant` — Variant as specified by [RFC4122](https://datatracker.ietf.org/doc/html/rfc4122#section-4.1.1). 1 \= `Big-endian` (default), 2 \= `Microsoft`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the binary representation of `string`. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT
    '612f3c40-5d3b-217e-707b-6a546a3d7b29' AS uuid,
    UUIDStringToNum(uuid) AS bytes

```


```
┌─uuid─────────────────────────────────┬─bytes────────────┐
│ 612f3c40-5d3b-217e-707b-6a546a3d7b29 │ a/<@];!~p{jTj={) │
└──────────────────────────────────────┴──────────────────┘

```

**Microsoft variant**



```
SELECT
    '612f3c40-5d3b-217e-707b-6a546a3d7b29' AS uuid,
    UUIDStringToNum(uuid, 2) AS bytes

```


```
┌─uuid─────────────────────────────────┬─bytes────────────┐
│ 612f3c40-5d3b-217e-707b-6a546a3d7b29 │ @</a;]~!p{jTj={) │
└──────────────────────────────────────┴──────────────────┘

```

## UUIDToNum[​](#UUIDToNum "Direct link to UUIDToNum")


Introduced in: v24\.5\.0


Accepts a [UUID](/docs/sql-reference/data-types/uuid) and returns its binary representation as a [FixedString(16\)](/docs/sql-reference/data-types/fixedstring), with its format optionally specified by `variant` (`Big-endian` by default).
This function replaces calls to two separate functions `UUIDStringToNum(toString(uuid))` so no intermediate conversion from UUID to string is required to extract bytes from a UUID.


**Syntax**



```
UUIDToNum(uuid[, variant = 1])

```

**Arguments**


- `uuid` — UUID. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `variant` — Variant as specified by [RFC4122](https://datatracker.ietf.org/doc/html/rfc4122#section-4.1.1). 1 \= `Big-endian` (default), 2 \= `Microsoft`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a binary representation of the UUID. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT
    toUUID('612f3c40-5d3b-217e-707b-6a546a3d7b29') AS uuid,
    UUIDToNum(uuid) AS bytes

```


```
┌─uuid─────────────────────────────────┬─bytes────────────┐
│ 612f3c40-5d3b-217e-707b-6a546a3d7b29 │ a/<@];!~p{jTj={) │
└──────────────────────────────────────┴──────────────────┘

```

**Microsoft variant**



```
SELECT
    toUUID('612f3c40-5d3b-217e-707b-6a546a3d7b29') AS uuid,
    UUIDToNum(uuid, 2) AS bytes

```


```
┌─uuid─────────────────────────────────┬─bytes────────────┐
│ 612f3c40-5d3b-217e-707b-6a546a3d7b29 │ @</a;]~!p{jTj={) │
└──────────────────────────────────────┴──────────────────┘

```

## UUIDv7ToDateTime[​](#UUIDv7ToDateTime "Direct link to UUIDv7ToDateTime")


Introduced in: v24\.5\.0


Returns the timestamp component of a UUID version 7\.


**Syntax**



```
UUIDv7ToDateTime(uuid[, timezone])

```

**Arguments**


- `uuid` — A UUID version 7\. [`String`](/docs/sql-reference/data-types/string)
- `timezone` — Optional. [Timezone name](/docs/operations/server-configuration-parameters/settings#timezone) for the returned value. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a timestamp with milliseconds precision. If the UUID is not a valid version 7 UUID, it returns `1970-01-01 00:00:00.000`. [`DateTime64(3)`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT UUIDv7ToDateTime(toUUID('018f05c9-4ab8-7b86-b64e-c9f03fbd45d1'))

```


```
┌─UUIDv7ToDateTime(toUUID('018f05c9-4ab8-7b86-b64e-c9f03fbd45d1'))─┐
│                                          2024-04-22 15:30:29.048 │
└──────────────────────────────────────────────────────────────────┘

```

**With timezone**



```
SELECT UUIDv7ToDateTime(toUUID('018f05c9-4ab8-7b86-b64e-c9f03fbd45d1'), 'America/New_York')

```


```
┌─UUIDv7ToDateTime(toUUID('018f05c9-4ab8-7b86-b64e-c9f03fbd45d1'), 'America/New_York')─┐
│                                                             2024-04-22 11:30:29.048 │
└─────────────────────────────────────────────────────────────────────────────────────┘

```

## dateTime64ToSnowflake[​](#dateTime64ToSnowflake "Direct link to dateTime64ToSnowflake")


Introduced in: v21\.10\.0


Deprecated feature
NoteThis function is deprecated and can only be used if setting [`allow_deprecated_snowflake_conversion_functions`](/docs/operations/settings/settings#allow_deprecated_snowflake_conversion_functions) is enabled.
The function will be removed at some point in future.Please use function [dateTime64ToSnowflakeID](#dateTime64ToSnowflakeID) instead.




Converts a [DateTime64](/docs/sql-reference/data-types/datetime64) to the first [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) at the giving time.


**Syntax**



```
dateTime64ToSnowflake(value)

```

**Arguments**


- `value` — Date with time. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Returned value**


Returns the input value converted as the first Snowflake ID at that time. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH toDateTime64('2021-08-15 18:57:56.492', 3, 'Asia/Shanghai') AS dt64 SELECT dateTime64ToSnowflake(dt64);

```


```
┌─dateTime64ToSnowflake(dt64)─┐
│         1426860704886947840 │
└─────────────────────────────┘

```

## dateTime64ToSnowflakeID[​](#dateTime64ToSnowflakeID "Direct link to dateTime64ToSnowflakeID")


Introduced in: v24\.6\.0


Converts a [DateTime64](/docs/sql-reference/data-types/datetime64) value to the first [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) at the giving time.


**Syntax**



```
dateTime64ToSnowflakeID(value[, epoch])

```

**Arguments**


- `value` — Date with time. [`DateTime64`](/docs/sql-reference/data-types/datetime64)
- `epoch` — Epoch of the Snowflake ID in milliseconds since 1970\-01\-01\. Defaults to 0 (1970\-01\-01\). For the Twitter/X epoch (2015\-01\-01\), provide 1288834974657\. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Input value converted to [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**simple**



```
SELECT dateTime64ToSnowflakeID(toDateTime64('2021-08-15 18:57:56', 3, 'Asia/Shanghai'))

```


```
6832626394434895872

```

## dateTimeToSnowflake[​](#dateTimeToSnowflake "Direct link to dateTimeToSnowflake")


Introduced in: v21\.10\.0


Deprecated feature
NoteThis function is deprecated and can only be used if setting [`allow_deprecated_snowflake_conversion_functions`](/docs/operations/settings/settings#allow_deprecated_snowflake_conversion_functions) is enabled.
The function will be removed at some point in future.Please use function [dateTimeToSnowflakeID](#dateTimeToSnowflakeID) instead.




Converts a [DateTime](/docs/sql-reference/data-types/datetime) value to the first [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) at the giving time.


**Syntax**



```
dateTimeToSnowflake(value)

```

**Arguments**


- `value` — Date with time. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Returns the input value as the first Snowflake ID at that time. [`Int64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
WITH toDateTime('2021-08-15 18:57:56', 'Asia/Shanghai') AS dt SELECT dateTimeToSnowflake(dt);

```


```
┌─dateTimeToSnowflake(dt)─┐
│     1426860702823350272 │
└─────────────────────────┘

```

## dateTimeToSnowflakeID[​](#dateTimeToSnowflakeID "Direct link to dateTimeToSnowflakeID")


Introduced in: v24\.6\.0


Converts a [DateTime](/docs/sql-reference/data-types/datetime) value to the first [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) at the giving time.


**Syntax**



```
dateTimeToSnowflakeID(value[, epoch])

```

**Arguments**


- `value` — Date with time. [`DateTime`](/docs/sql-reference/data-types/datetime)
- `epoch` — Epoch of the Snowflake ID in milliseconds since 1970\-01\-01\. Defaults to 0 (1970\-01\-01\). For the Twitter/X epoch (2015\-01\-01\), provide 1288834974657\. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Input value converted to [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**simple**



```
SELECT dateTimeToSnowflakeID(toDateTime('2021-08-15 18:57:56', 'Asia/Shanghai'))

```


```
6832626392367104000

```

## dateTimeToUUIDv7[​](#dateTimeToUUIDv7 "Direct link to dateTimeToUUIDv7")


Introduced in: v25\.8\.0


Converts a [DateTime](/docs/sql-reference/data-types/datetime) value to a [UUIDv7](https://en.wikipedia.org/wiki/UUID#Version_7) at the given time.


See section ["UUIDv7 generation"](#uuidv7-generation) for details on UUID structure, counter management, and concurrency guarantees.


NoteAs of September 2025, version 7 UUIDs are in draft status and their layout may change in future.


**Syntax**



```
dateTimeToUUIDv7(value)

```

**Arguments**


- `value` — Date with time. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Returned value**


Returns a UUIDv7\. [`UUID`](/docs/sql-reference/data-types/uuid)


**Examples**


**Usage example**



```
SELECT dateTimeToUUIDv7(toDateTime('2021-08-15 18:57:56', 'Asia/Shanghai'));

```


```
┌─dateTimeToUUIDv7(toDateTime('2021-08-15 18:57:56', 'Asia/Shanghai'))─┐
│ 018f05af-f4a8-778f-beee-1bedbc95c93b                                   │
└─────────────────────────────────────────────────────────────────────────┘

```

**multiple UUIDs for the same timestamp**



```
SELECT dateTimeToUUIDv7(toDateTime('2021-08-15 18:57:56'));
SELECT dateTimeToUUIDv7(toDateTime('2021-08-15 18:57:56'));

```


```
┌─dateTimeToUUIDv7(t⋯08-15 18:57:56'))─┐
│ 017b4b2d-7720-76ed-ae44-bbcc23a8c550 │
└──────────────────────────────────────┘
┌─dateTimeToUUIDv7(t⋯08-15 18:57:56'))─┐
│ 017b4b2d-7720-76ed-ae44-bbcf71ed0fd3 │
└──────────────────────────────────────┘

```

## generateSnowflakeID[​](#generateSnowflakeID "Direct link to generateSnowflakeID")


Introduced in: v24\.6\.0


Generates a [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID).


Function `generateSnowflakeID` guarantees that the counter field within a timestamp increments monotonically across all function invocations in concurrently running threads and queries.


See section ["Snowflake ID generation"](#snowflake-id-generation) for implementation details.


**Syntax**



```
generateSnowflakeID([expr, [machine_id]])

```

**Arguments**


- `expr` — An arbitrary [expression](/docs/sql-reference/syntax#expressions) used to bypass [common subexpression elimination](/docs/sql-reference/functions/overview#common-subexpression-elimination) if the function is called multiple times in a query. The value of the expression has no effect on the returned Snowflake ID. Optional. \- `machine_id` — A machine ID, the lowest 10 bits are used. [Int64](/docs/sql-reference/data-types/int-uint). Optional.


**Returned value**


Returns the Snowflake ID. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE tab (id UInt64)
ENGINE = MergeTree()
ORDER BY tuple();

INSERT INTO tab SELECT generateSnowflakeID();

SELECT * FROM tab;

```


```
┌──────────────────id─┐
│ 7199081390080409600 │
└─────────────────────┘

```

**Multiple Snowflake IDs generated per row**



```
SELECT generateSnowflakeID(1), generateSnowflakeID(2);

```


```
┌─generateSnowflakeID(1)─┬─generateSnowflakeID(2)─┐
│    7199081609652224000 │    7199081609652224001 │
└────────────────────────┴────────────────────────┘

```

**With expression and a machine ID**



```
SELECT generateSnowflakeID('expr', 1);

```


```
┌─generateSnowflakeID('expr', 1)─┐
│            7201148511606784002 │
└────────────────────────────────┘

```

## generateUUIDv4[​](#generateUUIDv4 "Direct link to generateUUIDv4")


Introduced in: v1\.1\.0


Generates a [version 4](https://tools.ietf.org/html/rfc4122#section-4.4) [UUID](/docs/sql-reference/data-types/uuid).


**Syntax**



```
generateUUIDv4([expr])

```

**Arguments**


- `expr` — Optional. An arbitrary expression used to bypass [common subexpression elimination](/docs/sql-reference/functions/overview#common-subexpression-elimination) if the function is called multiple times in a query. The value of the expression has no effect on the returned UUID.


**Returned value**


Returns a UUIDv4\. [`UUID`](/docs/sql-reference/data-types/uuid)


**Examples**


**Usage example**



```
SELECT generateUUIDv4(number) FROM numbers(3);

```


```
┌─generateUUIDv4(number)───────────────┐
│ fcf19b77-a610-42c5-b3f5-a13c122f65b6 │
│ 07700d36-cb6b-4189-af1d-0972f23dc3bc │
│ 68838947-1583-48b0-b9b7-cf8268dd343d │
└──────────────────────────────────────┘

```

**Common subexpression elimination**



```
SELECT generateUUIDv4(1), generateUUIDv4(1);

```


```
┌─generateUUIDv4(1)────────────────────┬─generateUUIDv4(2)────────────────────┐
│ 2d49dc6e-ddce-4cd0-afb8-790956df54c1 │ 2d49dc6e-ddce-4cd0-afb8-790956df54c1 │
└──────────────────────────────────────┴──────────────────────────────────────┘

```

## generateUUIDv7[​](#generateUUIDv7 "Direct link to generateUUIDv7")


Introduced in: v24\.5\.0


Generates a [version 7](https://datatracker.ietf.org/doc/html/draft-peabody-dispatch-new-uuid-format-04) [UUID](/docs/sql-reference/data-types/uuid).


See section ["UUIDv7 generation"](#uuidv7-generation) for details on UUID structure, counter management, and concurrency guarantees.


NoteAs of September 2025, version 7 UUIDs are in draft status and their layout may change in future.


**Syntax**



```
generateUUIDv7([expr])

```

**Arguments**


- `expr` — Optional. An arbitrary expression used to bypass [common subexpression elimination](/docs/sql-reference/functions/overview#common-subexpression-elimination) if the function is called multiple times in a query. The value of the expression has no effect on the returned UUID. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a UUIDv7\. [`UUID`](/docs/sql-reference/data-types/uuid)


**Examples**


**Usage example**



```
SELECT generateUUIDv7(number) FROM numbers(3);

```


```
┌─generateUUIDv7(number)───────────────┐
│ 019947fb-5766-7ed0-b021-d906f8f7cebb │
│ 019947fb-5766-7ed0-b021-d9072d0d1e07 │
│ 019947fb-5766-7ed0-b021-d908dca2cf63 │
└──────────────────────────────────────┘

```

**Common subexpression elimination**



```
SELECT generateUUIDv7(1), generateUUIDv7(1);

```


```
┌─generateUUIDv7(1)────────────────────┬─generateUUIDv7(1)────────────────────┐
│ 019947ff-0f87-7d88-ace0-8b5b3a66e0c1 │ 019947ff-0f87-7d88-ace0-8b5b3a66e0c1 │
└──────────────────────────────────────┴──────────────────────────────────────┘

```

## snowflakeIDToDateTime[​](#snowflakeIDToDateTime "Direct link to snowflakeIDToDateTime")


Introduced in: v24\.6\.0


Returns the timestamp component of a [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) as a value of type [DateTime](/docs/sql-reference/data-types/datetime).


**Syntax**



```
snowflakeIDToDateTime(value[, epoch[, time_zone]])

```

**Arguments**


- `value` — Snowflake ID. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `epoch` — Optional. Epoch of the Snowflake ID in milliseconds since 1970\-01\-01\. Defaults to 0 (1970\-01\-01\). For the Twitter/X epoch (2015\-01\-01\), provide 1288834974657\. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. [Timezone](/docs/operations/server-configuration-parameters/settings#timezone). The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the timestamp component of `value`. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT snowflakeIDToDateTime(7204436857747984384) AS res

```


```
┌─────────────────res─┐
│ 2024-06-06 10:59:58 │
└─────────────────────┘

```

## snowflakeIDToDateTime64[​](#snowflakeIDToDateTime64 "Direct link to snowflakeIDToDateTime64")


Introduced in: v24\.6\.0


Returns the timestamp component of a [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) as a value of type [DateTime64](/docs/sql-reference/data-types/datetime64).


**Syntax**



```
snowflakeIDToDateTime64(value[, epoch[, time_zone]])

```

**Arguments**


- `value` — Snowflake ID. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `epoch` — Optional. Epoch of the Snowflake ID in milliseconds since 1970\-01\-01\. Defaults to 0 (1970\-01\-01\). For the Twitter/X epoch (2015\-01\-01\), provide 1288834974657\. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. [Timezone](/docs/operations/server-configuration-parameters/settings#timezone). The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the timestamp component of `value` as a `DateTime64` with scale \= 3, i.e. millisecond precision. [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT snowflakeIDToDateTime64(7204436857747984384) AS res

```


```
┌─────────────────res─┐
│ 2024-06-06 10:59:58 │
└─────────────────────┘

```

## snowflakeToDateTime[​](#snowflakeToDateTime "Direct link to snowflakeToDateTime")


Introduced in: v21\.10\.0


Deprecated feature
NoteThis function is deprecated and can only be used if setting [`allow_deprecated_snowflake_conversion_functions`](/docs/operations/settings/settings#allow_deprecated_snowflake_conversion_functions) is enabled.
The function will be removed at some point in future.Please use function [`snowflakeIDToDateTime`](#snowflakeIDToDateTime) instead.




Extracts the timestamp component of a [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) in [DateTime](/docs/sql-reference/data-types/datetime) format.


**Syntax**



```
snowflakeToDateTime(value[, time_zone])

```

**Arguments**


- `value` — Snowflake ID. [`Int64`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. [Timezone](/docs/operations/server-configuration-parameters/settings#timezone). The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the timestamp component of `value`. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Usage example**



```
SELECT snowflakeToDateTime(CAST('1426860702823350272', 'Int64'), 'UTC');

```


```
┌─snowflakeToDateTime(CAST('1426860702823350272', 'Int64'), 'UTC')─┐
│                                              2021-08-15 10:57:56 │
└──────────────────────────────────────────────────────────────────┘

```

## snowflakeToDateTime64[​](#snowflakeToDateTime64 "Direct link to snowflakeToDateTime64")


Introduced in: v21\.10\.0


Deprecated feature
NoteThis function is deprecated and can only be used if setting [`allow_deprecated_snowflake_conversion_functions`](/docs/operations/settings/settings#allow_deprecated_snowflake_conversion_functions) is enabled.
The function will be removed at some point in future.Please use function [`snowflakeIDToDateTime64`](#snowflakeIDToDateTime64) instead.




Extracts the timestamp component of a [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID) in [DateTime64](/docs/sql-reference/data-types/datetime64) format.


**Syntax**



```
snowflakeToDateTime64(value[, time_zone])

```

**Arguments**


- `value` — Snowflake ID. [`Int64`](/docs/sql-reference/data-types/int-uint)
- `time_zone` — Optional. [Timezone](/docs/operations/server-configuration-parameters/settings#timezone). The function parses `time_string` according to the timezone. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the timestamp component of `value`. [`DateTime64(3)`](/docs/sql-reference/data-types/datetime64)


**Examples**


**Usage example**



```
SELECT snowflakeToDateTime64(CAST('1426860802823350272', 'Int64'), 'UTC');

```


```
┌─snowflakeToDateTime64(CAST('1426860802823350272', 'Int64'), 'UTC')─┐
│                                            2021-08-15 10:58:19.841 │
└────────────────────────────────────────────────────────────────────┘

```

## toUUIDOrDefault[​](#toUUIDOrDefault "Direct link to toUUIDOrDefault")


Introduced in: v21\.1\.0


Converts a String value to UUID type. If the conversion fails, returns a default UUID value instead of throwing an error.


This function attempts to parse a string of 36 characters in the standard UUID format (xxxxxxxx\-xxxx\-xxxx\-xxxx\-xxxxxxxxxxxx).
If the string cannot be converted to a valid UUID, the function returns the provided default UUID value.


**Syntax**



```
toUUIDOrDefault(string, default)

```

**Arguments**


- `string` — String of 36 characters or FixedString(36\) to be converted to UUID. \- `default` — UUID value to be returned if the first argument cannot be converted to UUID type.


**Returned value**


Returns the converted UUID if successful, or the default UUID if conversion fails. [`UUID`](/docs/sql-reference/data-types/uuid)


**Examples**


**Successful conversion returns the parsed UUID**



```
SELECT toUUIDOrDefault('61f0c404-5cb3-11e7-907b-a6006ad3dba0', toUUID('59f0c404-5cb3-11e7-907b-a6006ad3dba0'));

```


```
┌─toUUIDOrDefault('61f0c404-5cb3-11e7-907b-a6006ad3dba0', toUUID('59f0c404-5cb3-11e7-907b-a6006ad3dba0'))─┐
│ 61f0c404-5cb3-11e7-907b-a6006ad3dba0                                                                     │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

**Failed conversion returns the default UUID**



```
SELECT toUUIDOrDefault('-----61f0c404-5cb3-11e7-907b-a6006ad3dba0', toUUID('59f0c404-5cb3-11e7-907b-a6006ad3dba0'));

```


```
┌─toUUIDOrDefault('-----61f0c404-5cb3-11e7-907b-a6006ad3dba0', toUUID('59f0c404-5cb3-11e7-907b-a6006ad3dba0'))─┐
│ 59f0c404-5cb3-11e7-907b-a6006ad3dba0                                                                          │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## toUUIDOrNull[​](#toUUIDOrNull "Direct link to toUUIDOrNull")


Introduced in: v20\.12\.0


Converts an input value to a value of type `UUID` but returns `NULL` in case of an error.


Like [`toUUID`](/docs/sql-reference/functions/type-conversion-functions#toUUID) but returns `NULL` instead of throwing an exception on conversion errors.


Supported arguments:


- String representations of UUID in standard format (8\-4\-4\-4\-12 hexadecimal digits).
- String representations of UUID without hyphens (32 hexadecimal digits).


Unsupported arguments (return `NULL`):


- Invalid string formats.
- Non\-string types.
- Malformed UUIDs.


**Syntax**



```
toUUIDOrNull(x)

```

**Arguments**


- `x` — A string representation of a UUID. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a UUID value if successful, otherwise `NULL`. [`UUID`](/docs/sql-reference/data-types/uuid) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage examples**



```
SELECT
    toUUIDOrNull('550e8400-e29b-41d4-a716-446655440000') AS valid_uuid,
    toUUIDOrNull('invalid-uuid') AS invalid_uuid

```


```
┌─valid_uuid───────────────────────────┬─invalid_uuid─┐
│ 550e8400-e29b-41d4-a716-446655440000 │         ᴺᵁᴸᴸ │
└──────────────────────────────────────┴──────────────┘

```
[PreviousURLs](/docs/sql-reference/functions/url-functions)[NextWebAssembly UDFs](/docs/sql-reference/functions/wasm_udf)- [UUIDv7 generation](#uuidv7-generation)- [Snowflake ID generation](#snowflake-id-generation)- [UUIDNumToString](#UUIDNumToString)- [UUIDStringToNum](#UUIDStringToNum)- [UUIDToNum](#UUIDToNum)- [UUIDv7ToDateTime](#UUIDv7ToDateTime)- [dateTime64ToSnowflake](#dateTime64ToSnowflake)- [dateTime64ToSnowflakeID](#dateTime64ToSnowflakeID)- [dateTimeToSnowflake](#dateTimeToSnowflake)- [dateTimeToSnowflakeID](#dateTimeToSnowflakeID)- [dateTimeToUUIDv7](#dateTimeToUUIDv7)- [generateSnowflakeID](#generateSnowflakeID)- [generateUUIDv4](#generateUUIDv4)- [generateUUIDv7](#generateUUIDv7)- [snowflakeIDToDateTime](#snowflakeIDToDateTime)- [snowflakeIDToDateTime64](#snowflakeIDToDateTime64)- [snowflakeToDateTime](#snowflakeToDateTime)- [snowflakeToDateTime64](#snowflakeToDateTime64)- [toUUIDOrDefault](#toUUIDOrDefault)- [toUUIDOrNull](#toUUIDOrNull)
Was this page helpful?
