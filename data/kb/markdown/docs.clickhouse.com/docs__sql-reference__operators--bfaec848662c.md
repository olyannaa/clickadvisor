# Operators \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- Operators
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/operators/index.md)# Operators

ClickHouse transforms operators to their corresponding functions at the query parsing stage according to their priority, precedence, and associativity.


## Access Operators[​](#access-operators "Direct link to Access Operators")


`a[N]` – Access to an element of an array. The `arrayElement(a, N)` function.


`a.N` – Access to a tuple element. The `tupleElement(a, N)` function.


## Numeric Negation Operator[​](#numeric-negation-operator "Direct link to Numeric Negation Operator")


`-a` – The `negate (a)` function.


For tuple negation: [tupleNegate](/docs/sql-reference/functions/tuple-functions#tupleNegate).


## Multiplication and Division Operators[​](#multiplication-and-division-operators "Direct link to Multiplication and Division Operators")


`a * b` – The `multiply (a, b)` function.


For multiplying tuple by number: [tupleMultiplyByNumber](/docs/sql-reference/functions/tuple-functions#tupleMultiplyByNumber), for scalar product: [dotProduct](/docs/sql-reference/functions/array-functions#arrayDotProduct).


`a / b` – The `divide(a, b)` function.


For dividing tuple by number: [tupleDivideByNumber](/docs/sql-reference/functions/tuple-functions#tupleDivideByNumber).


`a % b` – The `modulo(a, b)` function.


## Addition and Subtraction Operators[​](#addition-and-subtraction-operators "Direct link to Addition and Subtraction Operators")


`a + b` – The `plus(a, b)` function.


For tuple addiction: [tuplePlus](/docs/sql-reference/functions/tuple-functions#tuplePlus).


`a - b` – The `minus(a, b)` function.


For tuple subtraction: [tupleMinus](/docs/sql-reference/functions/tuple-functions#tupleMinus).


## Comparison Operators[​](#comparison-operators "Direct link to Comparison Operators")


### equals function[​](#equals-function "Direct link to equals function")


`a = b` – The `equals(a, b)` function.


`a == b` – The `equals(a, b)` function.


### notEquals function[​](#notequals-function "Direct link to notEquals function")


`a != b` – The `notEquals(a, b)` function.


`a <> b` – The `notEquals(a, b)` function.


### lessOrEquals function[​](#lessorequals-function "Direct link to lessOrEquals function")


`a <= b` – The `lessOrEquals(a, b)` function.


### greaterOrEquals function[​](#greaterorequals-function "Direct link to greaterOrEquals function")


`a >= b` – The `greaterOrEquals(a, b)` function.


### less function[​](#less-function "Direct link to less function")


`a < b` – The `less(a, b)` function.


### greater function[​](#greater-function "Direct link to greater function")


`a > b` – The `greater(a, b)` function.


### like function[​](#like-function "Direct link to like function")


`a LIKE b` – The `like(a, b)` function.


### notLike function[​](#notlike-function "Direct link to notLike function")


`a NOT LIKE b` – The `notLike(a, b)` function.


### ilike function[​](#ilike-function "Direct link to ilike function")


`a ILIKE b` – The `ilike(a, b)` function.


### BETWEEN function[​](#between-function "Direct link to BETWEEN function")


`a BETWEEN b AND c` – The same as `a >= b AND a <= c`.


`a NOT BETWEEN b AND c` – The same as `a < b OR a > c`.


### is not distinct from operator (`<=>`)[​](#is-not-distinct-from "Direct link to is-not-distinct-from")


NoteFrom 25\.10 you can use `<=>` in the same way as any other operator.
Before 25\.10 it could only be used in JOIN expressions, for example:
```
CREATE TABLE a (x String) ENGINE = Memory;
INSERT INTO a VALUES ('ClickHouse');

SELECT * FROM a AS a1 JOIN a AS a2 ON a1.x <=> a2.x;

┌─x──────────┬─a2.x───────┐
│ ClickHouse │ ClickHouse │
└────────────┴────────────┘

```



The `<=>` operator is the `NULL`\-safe equality operator, equivalent to `IS NOT DISTINCT FROM`.
It works like the regular equality operator (`=`), but it treats `NULL` values as comparable.
Two `NULL` values are considered equal, and a `NULL` compared to any non\-`NULL` value returns 0 (false) rather than `NULL`.



```
SELECT
  'ClickHouse' <=> NULL,
  NULL <=> NULL

```


```
┌─isNotDistinc⋯use', NULL)─┬─isNotDistinc⋯NULL, NULL)─┐
│                        0 │                        1 │
└──────────────────────────┴──────────────────────────┘

```

## Operators for Working with Strings[​](#operators-for-working-with-strings "Direct link to Operators for Working with Strings")


### OVERLAY[​](#overlay "Direct link to OVERLAY")


- `OVERLAY(string PLACING replacement FROM offset)` \- The `overlay(string, replacement, offset)` function.
- `OVERLAY(string PLACING replacement FROM offset FOR length)` \- The `overlay(string, replacement, offset, length)` function.
- `OVERLAYUTF8(string PLACING replacement FROM offset)` \- The `overlayUTF8(string, replacement, offset)` function.
- `OVERLAYUTF8(string PLACING replacement FROM offset FOR length)` \- The `overlayUTF8(string, replacement, offset, length)` function.


## Operators for Working with Data Sets[​](#operators-for-working-with-data-sets "Direct link to Operators for Working with Data Sets")


See [IN operators](/docs/sql-reference/operators/in) and [EXISTS](/docs/sql-reference/operators/exists) operator.


### in function[​](#in-function "Direct link to in function")


`a IN ...` – The `in(a, b)` function.


### notIn function[​](#notin-function "Direct link to notIn function")


`a NOT IN ...` – The `notIn(a, b)` function.


### globalIn function[​](#globalin-function "Direct link to globalIn function")


`a GLOBAL IN ...` – The `globalIn(a, b)` function.


### globalNotIn function[​](#globalnotin-function "Direct link to globalNotIn function")


`a GLOBAL NOT IN ...` – The `globalNotIn(a, b)` function.


### in subquery function[​](#in-subquery-function "Direct link to in subquery function")


`a = ANY (subquery)` – The `in(a, subquery)` function.


### notIn subquery function[​](#notin-subquery-function "Direct link to notIn subquery function")


`a != ANY (subquery)` – The same as `a NOT IN (SELECT singleValueOrNull(*) FROM subquery)`.


### in subquery function[​](#in-subquery-function-1 "Direct link to in subquery function")


`a = ALL (subquery)` – The same as `a IN (SELECT singleValueOrNull(*) FROM subquery)`.


### notIn subquery function[​](#notin-subquery-function-1 "Direct link to notIn subquery function")


`a != ALL (subquery)` – The `notIn(a, subquery)` function.


**Examples**


Query with ALL:



```
SELECT number AS a FROM numbers(10) WHERE a > ALL (SELECT number FROM numbers(3, 3));

```


```
┌─a─┐
│ 6 │
│ 7 │
│ 8 │
│ 9 │
└───┘

```

Query with ANY:



```
SELECT number AS a FROM numbers(10) WHERE a > ANY (SELECT number FROM numbers(3, 3));

```


```
┌─a─┐
│ 4 │
│ 5 │
│ 6 │
│ 7 │
│ 8 │
│ 9 │
└───┘

```

## Operators for Working with Dates and Times[​](#operators-for-working-with-dates-and-times "Direct link to Operators for Working with Dates and Times")


### EXTRACT[​](#extract "Direct link to EXTRACT")



```
EXTRACT(part FROM date);

```

Extract parts from a given date. For example, you can retrieve a month from a given date, or a second from a time.


The `part` parameter specifies which part of the date to retrieve. The following values are available:


- `SECOND` — The second. Possible values: 0–59\.
- `MINUTE` — The minute. Possible values: 0–59\.
- `HOUR` — The hour. Possible values: 0–23\.
- `DAY` — The day of the month. Possible values: 1–31\.
- `WEEK` — The ISO 8601 week number. Possible values: 1–53\.
- `MONTH` — The number of a month. Possible values: 1–12\.
- `QUARTER` — The quarter. Possible values: 1–4\.
- `YEAR` — The year.
- `EPOCH` — The Unix timestamp (seconds since 1970\-01\-01 00:00:00 UTC). Note: for `DateTime64`, the subsecond part is truncated.
- `DOW` — The day of the week (PostgreSQL\-compatible). 0 \= Sunday, 6 \= Saturday.
- `DOY` — The day of the year. Possible values: 1–366\.
- `ISODOW` — The ISO day of the week. 1 \= Monday, 7 \= Sunday.
- `ISOYEAR` — The ISO 8601 week\-numbering year.
- `CENTURY` — The century. For example, the year 2024 is in the 21st century.
- `DECADE` — The decade (year divided by 10\). For example, the year 2024 has decade 202\.
- `MILLENNIUM` — The millennium. For example, the year 2024 is in the 3rd millennium.


The `part` parameter is case\-insensitive.


The `date` parameter specifies the date or the time to process. The [Date](/docs/sql-reference/data-types/date), [Date32](/docs/sql-reference/data-types/date32), [DateTime](/docs/sql-reference/data-types/datetime), and [DateTime64](/docs/sql-reference/data-types/datetime64) types are supported.


Examples:



```
SELECT EXTRACT(DAY FROM toDate('2017-06-15'));
SELECT EXTRACT(MONTH FROM toDate('2017-06-15'));
SELECT EXTRACT(YEAR FROM toDate('2017-06-15'));
SELECT EXTRACT(EPOCH FROM toDateTime('2024-01-15 12:30:45', 'UTC'));
SELECT EXTRACT(DOW FROM toDate('2024-01-15'));
SELECT EXTRACT(CENTURY FROM toDate('2024-01-01'));

```

In the following example we create a table and insert into it a value with the `DateTime` type.



```
CREATE TABLE test.Orders
(
    OrderId UInt64,
    OrderName String,
    OrderDate DateTime
) ENGINE = MergeTree
ORDER BY ();

```


```
INSERT INTO test.Orders VALUES (1, 'Jarlsberg Cheese', toDateTime('2008-10-11 13:23:44'));

```


```
SELECT
    toYear(OrderDate) AS OrderYear,
    toMonth(OrderDate) AS OrderMonth,
    toDayOfMonth(OrderDate) AS OrderDay,
    toHour(OrderDate) AS OrderHour,
    toMinute(OrderDate) AS OrderMinute,
    toSecond(OrderDate) AS OrderSecond
FROM test.Orders;

```


```
┌─OrderYear─┬─OrderMonth─┬─OrderDay─┬─OrderHour─┬─OrderMinute─┬─OrderSecond─┐
│      2008 │         10 │       11 │        13 │          23 │          44 │
└───────────┴────────────┴──────────┴───────────┴─────────────┴─────────────┘

```

You can see more examples in [tests](https://github.com/ClickHouse/ClickHouse/blob/master/tests/queries/0_stateless/00619_extract.sql).


### INTERVAL[​](#interval "Direct link to INTERVAL")


Creates an [Interval](/docs/sql-reference/data-types/special-data-types/interval)\-type value that should be used in arithmetical operations with [Date](/docs/sql-reference/data-types/date) and [DateTime](/docs/sql-reference/data-types/datetime)\-type values.


Types of intervals:


- `SECOND`
- `MINUTE`
- `HOUR`
- `DAY`
- `WEEK`
- `MONTH`
- `QUARTER`
- `YEAR`


You can also use a string literal when setting the `INTERVAL` value. For example, `INTERVAL 1 HOUR` is identical to the `INTERVAL '1 hour'` or `INTERVAL '1' hour`.


TipIntervals with different types can't be combined. You can't use expressions like `INTERVAL 4 DAY 1 HOUR`. Specify intervals in units that are smaller or equal to the smallest unit of the interval, for example, `INTERVAL 25 HOUR`. You can use consecutive operations, like in the example below.


Examples:



```
SELECT now() AS current_date_time, current_date_time + INTERVAL 4 DAY + INTERVAL 3 HOUR;

```


```
┌───current_date_time─┬─plus(plus(now(), toIntervalDay(4)), toIntervalHour(3))─┐
│ 2020-11-03 22:09:50 │                                    2020-11-08 01:09:50 │
└─────────────────────┴────────────────────────────────────────────────────────┘

```


```
SELECT now() AS current_date_time, current_date_time + INTERVAL '4 day' + INTERVAL '3 hour';

```


```
┌───current_date_time─┬─plus(plus(now(), toIntervalDay(4)), toIntervalHour(3))─┐
│ 2020-11-03 22:12:10 │                                    2020-11-08 01:12:10 │
└─────────────────────┴────────────────────────────────────────────────────────┘

```


```
SELECT now() AS current_date_time, current_date_time + INTERVAL '4' day + INTERVAL '3' hour;

```


```
┌───current_date_time─┬─plus(plus(now(), toIntervalDay('4')), toIntervalHour('3'))─┐
│ 2020-11-03 22:33:19 │                                        2020-11-08 01:33:19 │
└─────────────────────┴────────────────────────────────────────────────────────────┘

```

NoteThe `INTERVAL` syntax or `addDays` function are always preferred. Simple addition or subtraction (syntax like `now() + ...`) doesn't consider time settings. For example, daylight saving time.


Examples:



```
SELECT toDateTime('2014-10-26 00:00:00', 'Asia/Istanbul') AS time, time + 60 * 60 * 24 AS time_plus_24_hours, time + toIntervalDay(1) AS time_plus_1_day;

```


```
┌────────────────time─┬──time_plus_24_hours─┬─────time_plus_1_day─┐
│ 2014-10-26 00:00:00 │ 2014-10-26 23:00:00 │ 2014-10-27 00:00:00 │
└─────────────────────┴─────────────────────┴─────────────────────┘

```

**See Also**


- [Interval](/docs/sql-reference/data-types/special-data-types/interval) data type
- [toInterval](/docs/sql-reference/functions/type-conversion-functions#toIntervalYear) type conversion functions


### Date and Time Addition[​](#date-time-addition "Direct link to Date and Time Addition")


A [Date](/docs/sql-reference/data-types/date) or [Date32](/docs/sql-reference/data-types/date32) value can be added to a [Time](/docs/sql-reference/data-types/time) or [Time64](/docs/sql-reference/data-types/time64) value using the `+` operator. The result is a [DateTime](/docs/sql-reference/data-types/datetime) or [DateTime64](/docs/sql-reference/data-types/datetime64) representing the date at the given time of day. The operation is commutative.


The result type depends on the operand types:




| Left operand Right operand Result type| `Date` `Time` `DateTime`| `Date` `Time64(s)` `DateTime64(s)`| `Date32` `Time` `DateTime64(0)`| `Date32` `Time64(s)` `DateTime64(s)` | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


NoteThe result uses the [session timezone](/docs/operations/settings/settings#session_timezone) (or server default timezone if no session timezone is set). The [`date_time_overflow_behavior`](/docs/operations/settings/formats#date_time_overflow_behavior) setting controls what happens when the result is outside the representable range.


Examples:



```
SET use_legacy_to_time = 0;
SELECT toDate('2024-07-15') + toTime('14:30:25') AS dt, toTypeName(dt);

```


```
┌──────────────────dt─┬─toTypeName(dt)─┐
│ 2024-07-15 14:30:25 │ DateTime       │
└─────────────────────┴────────────────┘

```


```
SELECT toDate('2024-07-15') + toTime64('14:30:25.123456', 6) AS dt, toTypeName(dt);

```


```
┌─────────────────────────dt─┬─toTypeName(dt)─┐
│ 2024-07-15 14:30:25.123456 │ DateTime64(6)  │
└────────────────────────────┴────────────────┘

```


```
SELECT toTime64('23:59:59.999', 3) + toDate32('2024-07-15') AS dt, toTypeName(dt);

```


```
┌──────────────────────dt─┬─toTypeName(dt)─┐
│ 2024-07-15 23:59:59.999 │ DateTime64(3)  │
└─────────────────────────┴────────────────┘

```

## Logical AND Operator[​](#logical-and-operator "Direct link to Logical AND Operator")


Syntax `SELECT a AND b` — calculates logical conjunction of `a` and `b` with the function [and](/docs/sql-reference/functions/logical-functions#and).


## Logical OR Operator[​](#logical-or-operator "Direct link to Logical OR Operator")


Syntax `SELECT a OR b` — calculates logical disjunction of `a` and `b` with the function [or](/docs/sql-reference/functions/logical-functions#or).


## Logical Negation Operator[​](#logical-negation-operator "Direct link to Logical Negation Operator")


Syntax `SELECT NOT a` — calculates logical negation of `a` with the function [not](/docs/sql-reference/functions/logical-functions#not).


## Conditional Operator[​](#conditional-operator "Direct link to Conditional Operator")


`a ? b : c` – The `if(a, b, c)` function.


Note:


The conditional operator calculates the values of b and c, then checks whether condition a is met, and then returns the corresponding value. If `b` or `C` is an [arrayJoin()](/docs/sql-reference/functions/array-join) function, each row will be replicated regardless of the "a" condition.


## Conditional Expression[​](#conditional-expression "Direct link to Conditional Expression")



```
CASE [x]
    WHEN a THEN b
    [WHEN ... THEN ...]
    [ELSE c]
END

```

If `x` is specified, then `transform(x, [a, ...], [b, ...], c)` function is used. Otherwise – `multiIf(a, b, ..., c)`.


If there is no `ELSE c` clause in the expression, the default value is `NULL`.


The `transform` function does not work with `NULL`.


## Concatenation Operator[​](#concatenation-operator "Direct link to Concatenation Operator")


`s1 || s2` – The `concat(s1, s2) function.`


## Lambda Creation Operator[​](#lambda-creation-operator "Direct link to Lambda Creation Operator")


`x -> expr` – The `lambda(x, expr) function.`


The following operators do not have a priority since they are brackets:


## Array Creation Operator[​](#array-creation-operator "Direct link to Array Creation Operator")


`[x1, ...]` – The `array(x1, ...) function.`


## Tuple Creation Operator[​](#tuple-creation-operator "Direct link to Tuple Creation Operator")


`(x1, x2, ...)` – The `tuple(x2, x2, ...) function.`


## Associativity[​](#associativity "Direct link to Associativity")


All binary operators have left associativity. For example, `1 + 2 + 3` is transformed to `plus(plus(1, 2), 3)`.
Sometimes this does not work the way you expect. For example, `SELECT 4 > 2 > 3` will result in 0\.


For efficiency, the `and` and `or` functions accept any number of arguments. The corresponding chains of `AND` and `OR` operators are transformed into a single call of these functions.


## Checking for `NULL`[​](#checking-for-null "Direct link to checking-for-null")


ClickHouse supports the `IS NULL` and `IS NOT NULL` operators.


### IS NULL[​](#is_null "Direct link to IS NULL")


- For [Nullable](/docs/sql-reference/data-types/nullable) type values, the `IS NULL` operator returns:
	- `1`, if the value is `NULL`.
	- `0` otherwise.
- For other values, the `IS NULL` operator always returns `0`.


Can be optimized by enabling the [optimize\_functions\_to\_subcolumns](/docs/operations/settings/settings#optimize_functions_to_subcolumns) setting. With `optimize_functions_to_subcolumns = 1` the function reads only [null](/docs/sql-reference/data-types/nullable#finding-null) subcolumn instead of reading and processing the whole column data. The query `SELECT n IS NULL FROM table` transforms to `SELECT n.null FROM TABLE`.



```
SELECT x+100 FROM t_null WHERE y IS NULL

```


```
┌─plus(x, 100)─┐
│          101 │
└──────────────┘

```

### IS NOT NULL[​](#is_not_null "Direct link to IS NOT NULL")


- For [Nullable](/docs/sql-reference/data-types/nullable) type values, the `IS NOT NULL` operator returns:
	- `0`, if the value is `NULL`.
	- `1` otherwise.
- For other values, the `IS NOT NULL` operator always returns `1`.



```
SELECT * FROM t_null WHERE y IS NOT NULL

```


```
┌─x─┬─y─┐
│ 2 │ 3 │
└───┴───┘

```

Can be optimized by enabling the [optimize\_functions\_to\_subcolumns](/docs/operations/settings/settings#optimize_functions_to_subcolumns) setting. With `optimize_functions_to_subcolumns = 1` the function reads only [null](/docs/sql-reference/data-types/nullable#finding-null) subcolumn instead of reading and processing the whole column data. The query `SELECT n IS NOT NULL FROM table` transforms to `SELECT NOT n.null FROM TABLE`.


## Checking Boolean Values[​](#checking-boolean-values "Direct link to Checking Boolean Values")


ClickHouse supports the `IS TRUE`, `IS FALSE`, `IS UNKNOWN`, `IS NOT TRUE`, `IS NOT FALSE`, and `IS NOT UNKNOWN` operators.
They are used with [Bool](/docs/sql-reference/data-types/boolean) and `Nullable(Bool)` expressions.


- `expr IS TRUE` returns `1` only if `expr` is `true`.
- `expr IS FALSE` returns `1` only if `expr` is `false`.
- `expr IS UNKNOWN` returns `1` only if `expr` is `NULL`.
- `expr IS NOT TRUE` returns `1` if `expr` is `false` or `NULL`.
- `expr IS NOT FALSE` returns `1` if `expr` is `true` or `NULL`.
- `expr IS NOT UNKNOWN` returns `1` if `expr` is not `NULL`.


For boolean expressions, `IS UNKNOWN` is equivalent to `IS NULL`, and `IS NOT UNKNOWN` is equivalent to `IS NOT NULL`.



```
CREATE TABLE t_bool (x Nullable(Bool)) ENGINE = Memory;
INSERT INTO t_bool VALUES (true), (false), (NULL);

SELECT
    x,
    x IS TRUE,
    x IS FALSE,
    x IS UNKNOWN,
    x IS NOT TRUE,
    x IS NOT FALSE,
    x IS NOT UNKNOWN
FROM t_bool;

```
[PreviousUNDROP](/docs/sql-reference/statements/undrop)[NextDistributed DDL](/docs/sql-reference/other/distributed-ddl)- [Access Operators](#access-operators)- [Numeric Negation Operator](#numeric-negation-operator)- [Multiplication and Division Operators](#multiplication-and-division-operators)- [Addition and Subtraction Operators](#addition-and-subtraction-operators)- [Comparison Operators](#comparison-operators)
	- [equals function](#equals-function)- [notEquals function](#notequals-function)- [lessOrEquals function](#lessorequals-function)- [greaterOrEquals function](#greaterorequals-function)- [less function](#less-function)- [greater function](#greater-function)- [like function](#like-function)- [notLike function](#notlike-function)- [ilike function](#ilike-function)- [BETWEEN function](#between-function)- [is not distinct from operator (`<=>`)](#is-not-distinct-from)- [Operators for Working with Strings](#operators-for-working-with-strings)
	- [OVERLAY](#overlay)- [Operators for Working with Data Sets](#operators-for-working-with-data-sets)
	- [in function](#in-function)- [notIn function](#notin-function)- [globalIn function](#globalin-function)- [globalNotIn function](#globalnotin-function)- [in subquery function](#in-subquery-function)- [notIn subquery function](#notin-subquery-function)- [in subquery function](#in-subquery-function-1)- [notIn subquery function](#notin-subquery-function-1)- [Operators for Working with Dates and Times](#operators-for-working-with-dates-and-times)
	- [EXTRACT](#extract)- [INTERVAL](#interval)- [Date and Time Addition](#date-time-addition)- [Logical AND Operator](#logical-and-operator)- [Logical OR Operator](#logical-or-operator)- [Logical Negation Operator](#logical-negation-operator)- [Conditional Operator](#conditional-operator)- [Conditional Expression](#conditional-expression)- [Concatenation Operator](#concatenation-operator)- [Lambda Creation Operator](#lambda-creation-operator)- [Array Creation Operator](#array-creation-operator)- [Tuple Creation Operator](#tuple-creation-operator)- [Associativity](#associativity)- [Checking for `NULL`](#checking-for-null)
	- [IS NULL](#is_null)- [IS NOT NULL](#is_not_null)- [Checking Boolean Values](#checking-boolean-values)
Was this page helpful?
