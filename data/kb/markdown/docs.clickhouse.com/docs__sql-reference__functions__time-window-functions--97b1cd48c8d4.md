# Time window functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Time window
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/time-window-functions.md)# Time window functions


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)
Not supported in ClickHouse Cloud
Time window functions return the inclusive lower and exclusive upper bound of the corresponding window.
The functions for working with [WindowView](/docs/sql-reference/statements/create/view#window-view) are listed below:


## hop[​](#hop "Direct link to hop")


Introduced in: v21\.12\.0


A hopping time window has a fixed duration (`window_interval`) and hops by a specified hop interval (`hop_interval`). If the `hop_interval` is smaller than the `window_interval`, hopping windows are overlapping. Thus, records can be assigned to multiple windows.


Since one record can be assigned to multiple hop windows, the function only returns the bound of the first window when hop function is used without WINDOW VIEW.


**Syntax**



```
hop(time_attr, hop_interval, window_interval[, timezone])

```

**Arguments**


- `time_attr` — Date and time. [`DateTime`](/docs/sql-reference/data-types/datetime)
- `hop_interval` — Positive Hop interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `window_interval` — Positive Window interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the inclusive lower and exclusive upper bound of the corresponding hopping window. [`Tuple(DateTime, DateTime)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Hopping window**



```
SELECT hop(now(), INTERVAL '1' DAY, INTERVAL '2' DAY)

```


```
('2024-07-03 00:00:00','2024-07-05 00:00:00')

```

## hopEnd[​](#hopEnd "Direct link to hopEnd")


Introduced in: v22\.1\.0


Returns the exclusive upper bound of the corresponding hopping window.


Since one record can be assigned to multiple hop windows, the function only returns the bound of the first window when hop function is used without `WINDOW VIEW`.


**Syntax**



```
hopEnd(time_attr, hop_interval, window_interval[, timezone])

```

**Arguments**


- `time_attr` — Date and time. [`DateTime`](/docs/sql-reference/data-types/datetime)
- `hop_interval` — Positive Hop interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `window_interval` — Positive Window interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the exclusive upper bound of the corresponding hopping window. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Hopping window end**



```
SELECT hopEnd(now(), INTERVAL '1' DAY, INTERVAL '2' DAY)

```


```
2024-07-05 00:00:00

```

## hopStart[​](#hopStart "Direct link to hopStart")


Introduced in: v22\.1\.0


Returns the inclusive lower bound of the corresponding hopping window.


Since one record can be assigned to multiple hop windows, the function only returns the bound of the first window when hop function is used without `WINDOW VIEW`.


**Syntax**



```
hopStart(time_attr, hop_interval, window_interval[, timezone])

```

**Arguments**


- `time_attr` — Date and time. [`DateTime`](/docs/sql-reference/data-types/datetime)
- `hop_interval` — Positive Hop interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `window_interval` — Positive Window interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the inclusive lower bound of the corresponding hopping window. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Hopping window start**



```
SELECT hopStart(now(), INTERVAL '1' DAY, INTERVAL '2' DAY)

```


```
2024-07-03 00:00:00

```

## tumble[​](#tumble "Direct link to tumble")


Introduced in: v21\.12\.0


A tumbling time window assigns records to non\-overlapping, continuous windows with a fixed duration (`interval`).


**Syntax**



```
tumble(time_attr, interval[, timezone])

```

**Arguments**


- `time_attr` — Date and time. [`DateTime`](/docs/sql-reference/data-types/datetime)
- `interval` — Window interval in Interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the inclusive lower and exclusive upper bound of the corresponding tumbling window. [`Tuple(DateTime, DateTime)`](/docs/sql-reference/data-types/tuple)


**Examples**


**Tumbling window**



```
SELECT tumble(now(), toIntervalDay('1'))

```


```
('2024-07-04 00:00:00','2024-07-05 00:00:00')

```

## tumbleEnd[​](#tumbleEnd "Direct link to tumbleEnd")


Introduced in: v22\.1\.0


Returns the exclusive upper bound of the corresponding tumbling window.


**Syntax**



```
tumbleEnd(time_attr, interval[, timezone])

```

**Arguments**


- `time_attr` — Date and time. [`DateTime`](/docs/sql-reference/data-types/datetime)
- `interval` — Window interval in Interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the exclusive upper bound of the corresponding tumbling window. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Tumbling window end**



```
SELECT tumbleEnd(now(), toIntervalDay('1'))

```


```
2024-07-05 00:00:00

```

## tumbleStart[​](#tumbleStart "Direct link to tumbleStart")


Introduced in: v22\.1\.0


Returns the inclusive lower bound of the corresponding tumbling window.


**Syntax**



```
tumbleStart(time_attr, interval[, timezone])

```

**Arguments**


- `time_attr` — Date and time. [`DateTime`](/docs/sql-reference/data-types/datetime)
- `interval` — Window interval in Interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the inclusive lower bound of the corresponding tumbling window. [`DateTime`](/docs/sql-reference/data-types/datetime)


**Examples**


**Tumbling window start**



```
SELECT tumbleStart(now(), toIntervalDay('1'))

```


```
2024-07-04 00:00:00

```

## windowID[​](#windowID "Direct link to windowID")


Introduced in: v22\.1\.0


Returns the window identifier of the corresponding tumbling or hopping window.
This function can only be used with `WINDOW VIEW`.


**Syntax**



```
windowID(time_attr, interval[, timezone])

```

**Arguments**


- `time_attr` — Date and time. [`DateTime`](/docs/sql-reference/data-types/datetime)
- `interval` — Window interval in Interval. [`Interval`](/docs/sql-reference/data-types/int-uint)
- `timezone` — Optional. Timezone name. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the window identifier of the corresponding window. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Window ID**



```
SELECT windowID(now(), toIntervalDay('1'))

```


## Related content[​](#related-content "Direct link to Related content")


- [Time\-series use\-case guides](/docs/use-cases/time-series)
[PreviousTimeSeries](/docs/sql-reference/functions/time-series-functions)[NextTuples](/docs/sql-reference/functions/tuple-functions)- [hop](#hop)- [hopEnd](#hopEnd)- [hopStart](#hopStart)- [tumble](#tumble)- [tumbleEnd](#tumbleEnd)- [tumbleStart](#tumbleStart)- [windowID](#windowID)- [Related content](#related-content)
Was this page helpful?
