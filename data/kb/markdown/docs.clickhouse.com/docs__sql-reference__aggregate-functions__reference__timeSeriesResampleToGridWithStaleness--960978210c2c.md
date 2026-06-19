# timeSeriesResampleToGridWithStaleness \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- timeSeriesResampleToGridWithStaleness
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/timeSeriesResampleToGridWithStaleness.md)# timeSeriesResampleToGridWithStaleness

## timeSeriesResampleToGridWithStaleness[​](#timeSeriesResampleToGridWithStaleness "Direct link to timeSeriesResampleToGridWithStaleness")


Introduced in: v25\.6\.0


Aggregate function that takes time series data as pairs of timestamps and values and re\-samples this data to a regular time grid described by start timestamp, end timestamp and step. For each point on the grid the most recent (within the specified time window) sample is chosen.


Alias: `timeSeriesLastToGrid`.


NoteThis function is experimental, enable it by setting `allow_experimental_ts_to_grid_aggregate_function=true`.


**Syntax**



```
timeSeriesResampleToGridWithStaleness(start_timestamp, end_timestamp, grid_step, staleness_window)(timestamp, value)

```

**Aliases**: `timeSeriesLastToGrid`


**Parameters**


- `start_timestamp` — Specifies start of the grid. [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`DateTime`](/docs/sql-reference/data-types/datetime)
- `end_timestamp` — Specifies end of the grid. [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`DateTime`](/docs/sql-reference/data-types/datetime)
- `grid_step` — Specifies step of the grid in seconds. [`UInt32`](/docs/sql-reference/data-types/int-uint)
- `staleness_window` — Specifies the maximum staleness of the most recent sample in seconds. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Arguments**


- `timestamp` — Timestamp of the sample. Can be individual values or arrays. [`UInt32`](/docs/sql-reference/data-types/int-uint) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`Array(UInt32)`](/docs/sql-reference/data-types/array) or [`Array(DateTime)`](/docs/sql-reference/data-types/array)
- `value` — Value of the time series corresponding to the timestamp. Can be individual values or arrays. [`Float*`](/docs/sql-reference/data-types/float) or [`Array(Float*)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns time series values re\-sampled to the specified grid. The returned array contains one value for each time grid point. The value is NULL if there is no sample for a particular grid point. [`Array(Nullable(Float64))`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage with individual timestamp\-value pairs**



```
WITH
    -- NOTE: the gap between 140 and 190 is to show how values are filled for ts = 150, 165, 180 according to staleness window parameter
    [110, 120, 130, 140, 190, 200, 210, 220, 230]::Array(DateTime) AS timestamps,
    [1, 1, 3, 4, 5, 5, 8, 12, 13]::Array(Float32) AS values, -- array of values corresponding to timestamps above
    90 AS start_ts,       -- start of timestamp grid
    90 + 120 AS end_ts,   -- end of timestamp grid
    15 AS step_seconds,   -- step of timestamp grid
    30 AS window_seconds  -- "staleness" window
SELECT timeSeriesResampleToGridWithStaleness(start_ts, end_ts, step_seconds, window_seconds)(timestamp, value)
FROM
(
    -- This subquery converts arrays of timestamps and values into rows of `timestamp`, `value`
    SELECT
        arrayJoin(arrayZip(timestamps, values)) AS ts_and_val,
        ts_and_val.1 AS timestamp,
        ts_and_val.2 AS value
);

```


```
┌─timeSeriesResampleToGridWithStaleness(start_ts, end_ts, step_seconds, window_seconds)(timestamp, value)─┐
│ [NULL,NULL,1,3,4,4,NULL,5,8]                                                                           │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

**Using array arguments**



```
WITH
    [110, 120, 130, 140, 190, 200, 210, 220, 230]::Array(DateTime) AS timestamps,
    [1, 1, 3, 4, 5, 5, 8, 12, 13]::Array(Float32) AS values,
    90 AS start_ts,
    90 + 120 AS end_ts,
    15 AS step_seconds,
    30 AS window_seconds
SELECT timeSeriesResampleToGridWithStaleness(start_ts, end_ts, step_seconds, window_seconds)(timestamps, values);

```


```
┌─timeSeriesResampleToGridWithStaleness(start_ts, end_ts, step_seconds, window_seconds)(timestamps, values)─┐
│ [NULL,NULL,1,3,4,4,NULL,5,8]                                                                             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘

```
[PrevioustimeSeriesRateToGrid](/docs/sql-reference/aggregate-functions/reference/timeSeriesRateToGrid)[NexttimeSeriesResetsToGrid](/docs/sql-reference/aggregate-functions/reference/timeSeriesResetsToGrid)- [timeSeriesResampleToGridWithStaleness](#timeSeriesResampleToGridWithStaleness)
Was this page helpful?
