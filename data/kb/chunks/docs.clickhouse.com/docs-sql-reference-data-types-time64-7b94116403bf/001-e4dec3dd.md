---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/time64.md)#
topic: time64-clickhouse-docs
ch_version_introduced: '59.999999999'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 2
---

# Time64 \| ClickHouse Docs

- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- Time64
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/time64.md)# Time64

Data type `Time64` represents a time\-of\-day with fractional seconds.
It has no calendar date components (day, month, year).
The `precision` parameter defines the number of fractional digits and therefore the tick size.

Tick size (precision): 10\-precision seconds. Valid range: 0\..9\. Common choices are 3 (milliseconds), 6 (microseconds), and 9 (nanoseconds).

**Syntax:**

```
Time64(precision)

```

Internally, `Time64` stores a signed 64\-bit decimal (Decimal64\) number of fractional seconds.
The tick resolution is determined by the `precision` parameter.
Time zones are not supported: specifying a time zone with `Time64` will throw an error.

Unlike `DateTime64`, `Time64` does not store a date component.
See also [`Time`](/docs/sql-reference/data-types/time).

Text representation range: \[\-999:59:59\.000, 999:59:59\.999] for `precision = 3`. In general, the minimum is `-999:59:59` and the maximum is `999:59:59` with up to `precision` fractional digits (for `precision = 9`, the minimum is `-999:59:59.999999999`).

## Implementation details[​](#implementation-details "Direct link to Implementation details")

**Representation**.
Signed `Decimal64` value counting fractional second with `precision` fractional digits.

**Normalization**.
When parsing strings to `Time64`, the time components are normalized and not validated.
For example, `25:70:70` is interpreted as `26:11:10`.

**Negative values**.
Leading minus signs are supported and preserved.
Negative values typically arise from arithmetic operations on `Time64` values.
For `Time64`, negative inputs are preserved for both text (e.g., `'-01:02:03.123'`) and numeric inputs (e.g., `-3723.123`).

**Saturation**.
The time\-of\-day component is capped to the range \[\-999:59:59\.xxx, 999:59:59\.xxx] when converting to components or serialising to text.
The stored numeric value may exceed this range; however, any component extraction (hours, minutes, seconds) and textual representation use the saturated value.

**Time zones**.
`Time64` does not support time zones.
Specifying a time zone when creating a `Time64` type or value throws an error.
Likewise, attempts to apply or change the time zone on `Time64` columns is not supported and results in an error.

## Examples[​](#examples "Direct link to Examples")

1. Creating a table with a `Time64`\-type column and inserting data into it:

```
CREATE TABLE tab64
(
    `event_id` UInt8,
    `time` Time64(3)
)
ENGINE = TinyLog;

```

```
-- Parse Time64
-- - from string,
-- - from a number of seconds since 00:00:00 (fractional part according to precision).
INSERT INTO tab64 VALUES (1, '14:30:25'), (2, 52225.123), (3, '14:30:25');

SELECT * FROM tab64 ORDER BY event_id;

```
