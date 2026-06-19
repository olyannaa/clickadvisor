# timeSeriesGroupArray \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- timeSeriesGroupArray
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/timeSeriesGroupArray.md)# timeSeriesGroupArray

## timeSeriesGroupArray[​](#timeSeriesGroupArray "Direct link to timeSeriesGroupArray")


Introduced in: v25\.8\.0


Sorts time series data by timestamp in ascending order.


NoteThis function is experimental, enable it by setting `allow_experimental_ts_to_grid_aggregate_function=true`.


**Syntax**



```
timeSeriesGroupArray(timestamp, value)

```

**Arguments**


- `timestamp` — Timestamp of the sample. [`DateTime`](/docs/sql-reference/data-types/datetime) or [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `value` — Value of the time series corresponding to the timestamp. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Returned value**


Returns an array of tuples `(timestamp, value)` sorted by timestamp in ascending order. If there are multiple values for the same timestamp then the function chooses the greatest of these values. [`Array(Tuple(T1, T2))`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage with individual values**



```
WITH
    [110, 120, 130, 140, 140, 100]::Array(UInt32) AS timestamps,
    [1, 6, 8, 17, 19, 5]::Array(Float32) AS values
SELECT timeSeriesGroupArray(timestamp, value)
FROM
(
    SELECT
        arrayJoin(arrayZip(timestamps, values)) AS ts_and_val,
        ts_and_val.1 AS timestamp,
        ts_and_val.2 AS value
);

```


```
┌─timeSeriesGroupArray(timestamp, value)───────────────┐
│ [(100, 5), (110, 1), (120, 6), (130, 8), (140, 19)]  │
└──────────────────────────────────────────────────────┘

```

**Passing multiple samples of timestamps and values as arrays of equal size**



```
WITH
    [110, 120, 130, 140, 140, 100]::Array(UInt32) AS timestamps,
    [1, 6, 8, 17, 19, 5]::Array(Float32) AS values
SELECT timeSeriesGroupArray(timestamps, values);

```


```
┌─timeSeriesGroupArray(timestamps, values)──────────────┐
│ [(100, 5), (110, 1), (120, 6), (130, 8), (140, 19)]   │
└───────────────────────────────────────────────────────┘

```
[PrevioustimeSeriesDerivToGrid](/docs/sql-reference/aggregate-functions/reference/timeSeriesDerivToGrid)[NexttimeSeriesInstantDeltaToGrid](/docs/sql-reference/aggregate-functions/reference/timeSeriesInstantDeltaToGrid)- [timeSeriesGroupArray](#timeSeriesGroupArray)
Was this page helpful?
