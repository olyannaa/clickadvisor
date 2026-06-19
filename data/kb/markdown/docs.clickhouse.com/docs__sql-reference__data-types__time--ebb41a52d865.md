# Time \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- Time
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/time.md)# Time

Data type `Time` represents a time with hour, minute, and second components.
It is independent of any calendar date and is suitable for values which do not need day, months and year components.


Syntax:



```
Time

```

Text representation range: \[\-999:59:59, 999:59:59].


Resolution: 1 second.


## Implementation details[​](#implementation-details "Direct link to Implementation details")


**Representation and Performance**.
Data type `Time` internally stores a signed 32\-bit integer that encodes the seconds.
Values of type `Time` and `DateTime` have the same byte size and thus comparable performance.


**Normalization**.
When parsing strings to `Time`, the time components are normalized and not validated.
For example, `25:70:70` is interpreted as `26:11:10`.


**Negative values**.
Leading minus signs are supported and preserved.
Negative values typically arise from arithmetic operations on `Time` values.
For `Time` type, negative inputs are preserved for both text (e.g., `'-01:02:03'`) and numeric inputs (e.g., `-3723`).


**Saturation**.
The time\-of\-day component is capped to the range \[\-999:59:59, 999:59:59].
Values with hours beyond 999 (or below \-999\) are represented and round\-tripped via text as `999:59:59` (or `-999:59:59`).


**Time zones**.
`Time` does not support time zones, i.e. `Time` value are interpreted without regional context.
Specifying a time zone for `Time` as a type parameter or during value creation throws an error.
Likewise, attempts to apply or change the time zone on `Time` columns are not supported and result in an error.
`Time` values are not silently reinterpreted under different time zones.


## Examples[​](#examples "Direct link to Examples")


**1\.** Creating a table with a `Time`\-type column and inserting data into it:



```
CREATE TABLE tab
(
    `event_id` UInt8,
    `time` Time
)
ENGINE = TinyLog;

```


```
-- Parse Time
-- - from string,
-- - from integer interpreted as number of seconds since 00:00:00.
INSERT INTO tab VALUES (1, '14:30:25'), (2, 52225);

SELECT * FROM tab ORDER BY event_id;

```


```
   ┌─event_id─┬──────time─┐
1. │        1 │ 14:30:25 │
2. │        2 │ 14:30:25 │
   └──────────┴───────────┘

```

**2\.** Filtering on `Time` values



```
SET use_legacy_to_time = 0;
SELECT * FROM tab WHERE time = toTime('14:30:25')

```


```
   ┌─event_id─┬──────time─┐
1. │        1 │ 14:30:25 │
2. │        2 │ 14:30:25 │
   └──────────┴───────────┘

```

`Time` column values can be filtered using a string value in `WHERE` predicate. It will be converted to `Time` automatically:



```
SELECT * FROM tab WHERE time = '14:30:25'

```


```
   ┌─event_id─┬──────time─┐
1. │        1 │ 14:30:25 │
2. │        2 │ 14:30:25 │
   └──────────┴───────────┘

```

**3\.** Inspecting the resulting type:



```
SELECT CAST('14:30:25' AS Time) AS column, toTypeName(column) AS type

```


```
   ┌────column─┬─type─┐
1. │ 14:30:25 │ Time │
   └───────────┴──────┘

```

## Addition with Date[​](#addition-with-date "Direct link to Addition with Date")


A [Time](/docs/sql-reference/data-types/time) value can be added to a [Date](/docs/sql-reference/data-types/date) or [Date32](/docs/sql-reference/data-types/date32) value to produce a [DateTime](/docs/sql-reference/data-types/datetime) or [DateTime64](/docs/sql-reference/data-types/datetime64):



```
SET use_legacy_to_time = 0;
SELECT toDate('2024-07-15') + toTime('14:30:25') as datetime;

```


```
   ┌────────────datetime─┐
1. │ 2024-07-15 14:30:25 │
   └─────────────────────┘

```

See [Date and Time Addition](/docs/sql-reference/operators#date-time-addition) for details on all supported combinations and result types.


## See Also[​](#see-also "Direct link to See Also")


- [Type conversion functions](/docs/sql-reference/functions/type-conversion-functions)
- [Functions for working with dates and times](/docs/sql-reference/functions/date-time-functions)
- [Functions for working with arrays](/docs/sql-reference/functions/array-functions)
- [The `date_time_input_format` setting](/docs/operations/settings/formats#date_time_input_format)
- [The `date_time_output_format` setting](/docs/operations/settings/formats#date_time_output_format)
- [The `timezone` server configuration parameter](/docs/operations/server-configuration-parameters/settings#timezone)
- [The `session_timezone` setting](/docs/operations/settings/settings#session_timezone)
- [The `DateTime` data type](/docs/sql-reference/data-types/datetime)
- [The `Date` data type](/docs/sql-reference/data-types/date)
[PreviousDate32](/docs/sql-reference/data-types/date32)[NextDateTime](/docs/sql-reference/data-types/datetime)- [Implementation details](#implementation-details)- [Examples](#examples)- [Addition with Date](#addition-with-date)- [See Also](#see-also)
Was this page helpful?
