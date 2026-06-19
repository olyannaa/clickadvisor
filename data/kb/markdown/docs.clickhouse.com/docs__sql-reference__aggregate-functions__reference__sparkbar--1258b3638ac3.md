# sparkbar \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- sparkbar
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/sparkbar.md)# sparkbar

## sparkbar[​](#sparkbar "Direct link to sparkbar")


Introduced in: v21\.11\.0


The function plots a frequency histogram for values `x` and the repetition rate `y` of these values over the interval `[min_x, max_x]`.
Repetitions for all `x` falling into the same bucket are averaged, so data should be pre\-aggregated.
Negative repetitions are ignored.


If no interval is specified, then the minimum `x` is used as the interval start, and the maximum `x` — as the interval end.
Otherwise, values outside the interval are ignored.


**Syntax**



```
sparkbar(buckets[, min_x, max_x])(x, y)

```

**Aliases**: `sparkBar`


**Parameters**


- `buckets` — The number of segments. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `min_x` — Optional. The interval start. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `max_x` — Optional. The interval end. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Arguments**


- `x` — The field with values. [`const String`](/docs/sql-reference/data-types/string)
- `y` — The field with the frequency of values. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the frequency histogram. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Without interval specification**



```
CREATE TABLE spark_bar_data (`value` Int64, `event_date` Date) ENGINE = MergeTree ORDER BY event_date;

INSERT INTO spark_bar_data VALUES (1,'2020-01-01'), (3,'2020-01-02'), (4,'2020-01-02'), (-3,'2020-01-02'), (5,'2020-01-03'), (2,'2020-01-04'), (3,'2020-01-05'), (7,'2020-01-06'), (6,'2020-01-07'), (8,'2020-01-08'), (2,'2020-01-11');

SELECT sparkbar(9)(event_date, cnt) FROM (SELECT sum(value) AS cnt, event_date FROM spark_bar_data GROUP BY event_date);

```


```
┌─sparkbar(9)(event_date, cnt)─┐
│ ▂▅▂▃▆█  ▂                    │
└──────────────────────────────┘

```

**With interval specification**



```
SELECT sparkbar(9, toDate('2020-01-01'), toDate('2020-01-10'))(event_date, cnt) FROM (SELECT sum(value) AS cnt, event_date FROM spark_bar_data GROUP BY event_date);

```


```
┌─sparkbar(9, toDate('2020-01-01'), toDate('2020-01-10'))(event_date, cnt)─┐
│ ▂▅▂▃▇▆█                                                                  │
└──────────────────────────────────────────────────────────────────────────┘

```
[PreviousskewSamp](/docs/sql-reference/aggregate-functions/reference/skewsamp)[NextstddevPop](/docs/sql-reference/aggregate-functions/reference/stddevpop)- [sparkbar](#sparkbar)
Was this page helpful?
