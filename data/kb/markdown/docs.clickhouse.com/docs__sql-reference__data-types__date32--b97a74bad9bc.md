# Date32 \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- Date32
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/date32.md)# Date32

A date. Supports the date range same with [DateTime64](/docs/sql-reference/data-types/datetime64). Stored as a signed 32\-bit integer in native byte order with the value representing the days since `1900-01-01`. **Important!** 0 represents `1970-01-01`, and negative values represent the days before `1970-01-01`.


**Examples**


Creating a table with a `Date32`\-type column and inserting data into it:



```
CREATE TABLE dt32
(
    `timestamp` Date32,
    `event_id` UInt8
)
ENGINE = TinyLog;

```


```
-- Parse Date
-- - from string,
-- - from 'small' integer interpreted as number of days since 1970-01-01, and
-- - from 'big' integer interpreted as number of seconds since 1970-01-01.
INSERT INTO dt32 VALUES ('2100-01-01', 1), (47482, 2), (4102444800, 3);

SELECT * FROM dt32;

```


```
┌──timestamp─┬─event_id─┐
│ 2100-01-01 │        1 │
│ 2100-01-01 │        2 │
│ 2100-01-01 │        3 │
└────────────┴──────────┘

```

**See Also**


- [toDate32](/docs/sql-reference/functions/type-conversion-functions#toDate32)
- [toDate32OrZero](/docs/sql-reference/functions/type-conversion-functions#toDate32OrZero)
- [toDate32OrNull](/docs/sql-reference/functions/type-conversion-functions#toDate32OrNull)
[PreviousDate](/docs/sql-reference/data-types/date)[NextTime](/docs/sql-reference/data-types/time)Was this page helpful?
