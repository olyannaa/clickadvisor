# Interval \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- [Special Data Types](/docs/sql-reference/data-types/special-data-types)- Interval
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/special-data-types/interval.md)# Interval

The family of data types representing time and date intervals. The resulting types of the [INTERVAL](/docs/sql-reference/operators#interval) operator.


Structure:


- Time interval as an unsigned integer value.
- Type of an interval.


Supported interval types:


- `NANOSECOND`
- `MICROSECOND`
- `MILLISECOND`
- `SECOND`
- `MINUTE`
- `HOUR`
- `DAY`
- `WEEK`
- `MONTH`
- `QUARTER`
- `YEAR`


For each interval type, there is a separate data type. For example, the `DAY` interval corresponds to the `IntervalDay` data type:



```
SELECT toTypeName(INTERVAL 4 DAY)

```


```
┌─toTypeName(toIntervalDay(4))─┐
│ IntervalDay                  │
└──────────────────────────────┘

```

## Usage Remarks[​](#usage-remarks "Direct link to Usage Remarks")


You can use `Interval`\-type values in arithmetical operations with [Date](/docs/sql-reference/data-types/date) and [DateTime](/docs/sql-reference/data-types/datetime)\-type values. For example, you can add 4 days to the current time:



```
SELECT now() AS current_date_time, current_date_time + INTERVAL 4 DAY

```


```
┌───current_date_time─┬─plus(now(), toIntervalDay(4))─┐
│ 2019-10-23 10:58:45 │           2019-10-27 10:58:45 │
└─────────────────────┴───────────────────────────────┘

```

Also it is possible to use multiple intervals simultaneously:



```
SELECT now() AS current_date_time, current_date_time + (INTERVAL 4 DAY + INTERVAL 3 HOUR)

```


```
┌───current_date_time─┬─plus(current_date_time, plus(toIntervalDay(4), toIntervalHour(3)))─┐
│ 2024-08-08 18:31:39 │                                                2024-08-12 21:31:39 │
└─────────────────────┴────────────────────────────────────────────────────────────────────┘

```

And to compare values with different intervals:



```
SELECT toIntervalMicrosecond(3600000000) = toIntervalHour(1);

```


```
┌─less(toIntervalMicrosecond(179999999), toIntervalMinute(3))─┐
│                                                           1 │
└─────────────────────────────────────────────────────────────┘

```

## Mixed\-type Intervals[​](#mixed-type-intervals "Direct link to Mixed-type Intervals")


Intervals of mixed type, e.g. multiple hours and multiple minutes, can be created using `INTERVAL 'value' <from_kind> TO <to_kind>` syntax.
The result is a tuple of two or more intervals.


Supported combinations:




| Syntax String format Example| `YEAR TO MONTH` `Y-M` `INTERVAL '2-6' YEAR TO MONTH`| `DAY TO HOUR` `D H` `INTERVAL '5 12' DAY TO HOUR`| `DAY TO MINUTE` `D H:M` `INTERVAL '5 12:30' DAY TO MINUTE`| `DAY TO SECOND` `D H:M:S` `INTERVAL '5 12:30:45' DAY TO SECOND`| `HOUR TO MINUTE` `H:M` `INTERVAL '1:30' HOUR TO MINUTE`| `HOUR TO SECOND` `H:M:S` `INTERVAL '1:30:45' HOUR TO SECOND`| `MINUTE TO SECOND` `M:S` `INTERVAL '5:30' MINUTE TO SECOND` | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Non\-leading fields are validated per the SQL standard: `MONTH` 0\-11, `HOUR` 0\-23, `MINUTE` 0\-59, `SECOND` 0\-59\.



```
SELECT INTERVAL '1:30' HOUR TO MINUTE;

```


```
┌─(toIntervalHour(1), toIntervalMinute(30))─┐
│ (1,30)                                     │
└────────────────────────────────────────────┘

```

An optional leading `+` or `-` sign applies to all components:



```
SELECT INTERVAL '+1:30' HOUR TO MINUTE;
-- this is equivalent to:
-- SELECT INTERVAL '1:30' HOUR TO MINUTE;

```


```
┌─(toIntervalHour(1), toIntervalMinute(30))─┐
│ (1,30)                                     │
└────────────────────────────────────────────┘

```

## See Also[​](#see-also "Direct link to See Also")


- [INTERVAL](/docs/sql-reference/operators#interval) operator
- [toInterval](/docs/sql-reference/functions/type-conversion-functions#toIntervalYear) type conversion functions
[PreviousNothing](/docs/sql-reference/data-types/special-data-types/nothing)[NextData types binary encoding specification.](/docs/sql-reference/data-types/data-types-binary-encoding)- [Usage Remarks](#usage-remarks)- [Mixed\-type Intervals](#mixed-type-intervals)- [See Also](#see-also)
Was this page helpful?
