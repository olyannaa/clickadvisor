# Window Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- Window functions
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/window-functions/index.md)# Window Functions

Window functions let you perform calculations across a set of rows that are related to the current row.
Some of the calculations that you can do are similar to those that can be done with an aggregate function, but a window function doesn't cause rows to be grouped into a single output \- the individual rows are still returned.


## Standard window functions[​](#standard-window-functions "Direct link to Standard window functions")


ClickHouse supports the standard grammar for defining windows and window functions. The table below indicates whether a feature is currently supported.




| Feature Supported?| ad hoc window specification (`count(*) over (partition by id order by time desc)`) ✅| expressions involving window functions, e.g. `(count(*) over ()) / 2)` ✅| `WINDOW` clause (`select ... from table window w as (partition by id)`) ✅| `ROWS` frame ✅| `RANGE` frame ✅ (the default)| `INTERVAL` syntax for `DateTime` `RANGE OFFSET` frame ❌ (specify the number of seconds instead (`RANGE` works with any numeric type).)| `GROUPS` frame ❌| Calculating aggregate functions over a frame (`sum(value) over (order by time)`) ✅ (All aggregate functions are supported)| `rank()`, `dense_rank()`, `row_number()` ✅ Alias: `denseRank()`| `percent_rank()` ✅ Efficiently computes the relative standing of a value within a partition in a dataset. This function effectively replaces the more verbose and computationally intensive manual SQL calculation expressed as `ifNull((rank() OVER(PARTITION BY x ORDER BY y) - 1) / nullif(count(1) OVER(PARTITION BY x) - 1, 0), 0)` Alias: `percentRank()`| `cume_dist()` ✅ Computes the cumulative distribution of a value within a group of values. Returns the percentage of rows with values less than or equal to the current row's value.| `lag/lead(value, offset)` ✅  You can also use one of the following workarounds: 1\) `any(value) over (.... rows between <offset> preceding and <offset> preceding)`, or `following` for `lead`  2\) `lagInFrame/leadInFrame`, which are analogous, but respect the window frame. To get behavior identical to `lag/lead`, use `rows between unbounded preceding and unbounded following`| ntile(buckets) ✅  Specify window like, (partition by x order by y rows between unbounded preceding and unbounded following). | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


## ClickHouse\-specific window functions[​](#clickhouse-specific-window-functions "Direct link to ClickHouse-specific window functions")


There is also the following ClickHouse specific window function:


### nonNegativeDerivative(metric\_column, timestamp\_column\[, INTERVAL X UNITS])[​](#nonnegativederivativemetric_column-timestamp_column-interval-x-units "Direct link to nonNegativeDerivative(metric_column, timestamp_column[, INTERVAL X UNITS])")


Finds non\-negative derivative for given `metric_column` by `timestamp_column`.
`INTERVAL` can be omitted, default is `INTERVAL 1 SECOND`.
The computed value is the following for each row:


- `0` for 1st row,
- metrici−metrici−1timestampi−timestampi−1∗interval{\\text{metric}\_i \- \\text{metric}\_{i\-1} \\over \\text{timestamp}\_i \- \\text{timestamp}\_{i\-1}} \* \\text{interval}timestampi​−timestampi−1​metrici​−metrici−1​​∗interval for ithi\_{th}ith​ row.


## Syntax[​](#syntax "Direct link to Syntax")



```
aggregate_function (column_name)
  OVER ([[PARTITION BY grouping_column] [ORDER BY sorting_column] 
        [ROWS or RANGE expression_to_bound_rows_within_the_group]] | [window_name])
FROM table_name
WINDOW window_name as ([
  [PARTITION BY grouping_column]
  [ORDER BY sorting_column]
  [ROWS or RANGE expression_to_bound_rows_within_the_group]
])

```

- `PARTITION BY` \- defines how to break a resultset into groups.
- `ORDER BY` \- defines how to order rows inside the group during calculation aggregate\_function.
- `ROWS or RANGE` \- defines bounds of a frame, aggregate\_function is calculated within a frame.
- `WINDOW` \- allows multiple expressions to use the same window definition.



```
      PARTITION
┌─────────────────┐  <-- UNBOUNDED PRECEDING (BEGINNING of the PARTITION)
│                 │
│                 │
│=================│  <-- N PRECEDING  <─┐
│      N ROWS     │                     │  F
│  Before CURRENT │                     │  R
│~~~~~~~~~~~~~~~~~│  <-- CURRENT ROW    │  A
│     M ROWS      │                     │  M
│   After CURRENT │                     │  E
│=================│  <-- M FOLLOWING  <─┘
│                 │
│                 │
└─────────────────┘  <--- UNBOUNDED FOLLOWING (END of the PARTITION)

```

### Functions[​](#functions "Direct link to Functions")


These functions can be used only as a window function.


- [`row_number()`](/docs/sql-reference/window-functions/row_number) \- Number the current row within its partition starting from 1\.
- [`first_value(x)`](/docs/sql-reference/window-functions/first_value) \- Return the first value evaluated within its ordered frame.
- [`last_value(x)`](/docs/sql-reference/window-functions/last_value) \- Return the last value evaluated within its ordered frame.
- [`nth_value(x, offset)`](/docs/sql-reference/window-functions/nth_value) \- Return the first non\-NULL value evaluated against the nth row (offset) in its ordered frame.
- [`rank()`](/docs/sql-reference/window-functions/rank) \- Rank the current row within its partition with gaps.
- [`dense_rank()`](/docs/sql-reference/window-functions/dense_rank) \- Rank the current row within its partition without gaps.
- [`lagInFrame(x)`](/docs/sql-reference/window-functions/lagInFrame) \- Return a value evaluated at the row that is at a specified physical offset row before the current row within the ordered frame.
- [`leadInFrame(x)`](/docs/sql-reference/window-functions/leadInFrame) \- Return a value evaluated at the row that is offset rows after the current row within the ordered frame.


## Examples[​](#examples "Direct link to Examples")


Let's have a look at some examples of how window functions can be used.


### Numbering rows[​](#numbering-rows "Direct link to Numbering rows")



```
CREATE TABLE salaries
(
    `team` String,
    `player` String,
    `salary` UInt32,
    `position` String
)
Engine = Memory;

INSERT INTO salaries FORMAT Values
    ('Port Elizabeth Barbarians', 'Gary Chen', 195000, 'F'),
    ('New Coreystad Archdukes', 'Charles Juarez', 190000, 'F'),
    ('Port Elizabeth Barbarians', 'Michael Stanley', 150000, 'D'),
    ('New Coreystad Archdukes', 'Scott Harrison', 150000, 'D'),
    ('Port Elizabeth Barbarians', 'Robert George', 195000, 'M');

```


```
SELECT
    player,
    salary,
    row_number() OVER (ORDER BY salary ASC) AS row
FROM salaries;

```


```
┌─player──────────┬─salary─┬─row─┐
│ Michael Stanley │ 150000 │   1 │
│ Scott Harrison  │ 150000 │   2 │
│ Charles Juarez  │ 190000 │   3 │
│ Gary Chen       │ 195000 │   4 │
│ Robert George   │ 195000 │   5 │
└─────────────────┴────────┴─────┘

```


```
SELECT
    player,
    salary,
    row_number() OVER (ORDER BY salary ASC) AS row,
    rank() OVER (ORDER BY salary ASC) AS rank,
    dense_rank() OVER (ORDER BY salary ASC) AS denseRank
FROM salaries;

```


```
┌─player──────────┬─salary─┬─row─┬─rank─┬─denseRank─┐
│ Michael Stanley │ 150000 │   1 │    1 │         1 │
│ Scott Harrison  │ 150000 │   2 │    1 │         1 │
│ Charles Juarez  │ 190000 │   3 │    3 │         2 │
│ Gary Chen       │ 195000 │   4 │    4 │         3 │
│ Robert George   │ 195000 │   5 │    4 │         3 │
└─────────────────┴────────┴─────┴──────┴───────────┘

```

### Aggregation functions[​](#aggregation-functions "Direct link to Aggregation functions")


Compare each player's salary to the average for their team.



```
SELECT
    player,
    salary,
    team,
    avg(salary) OVER (PARTITION BY team) AS teamAvg,
    salary - teamAvg AS diff
FROM salaries;

```


```
┌─player──────────┬─salary─┬─team──────────────────────┬─teamAvg─┬───diff─┐
│ Charles Juarez  │ 190000 │ New Coreystad Archdukes   │  170000 │  20000 │
│ Scott Harrison  │ 150000 │ New Coreystad Archdukes   │  170000 │ -20000 │
│ Gary Chen       │ 195000 │ Port Elizabeth Barbarians │  180000 │  15000 │
│ Michael Stanley │ 150000 │ Port Elizabeth Barbarians │  180000 │ -30000 │
│ Robert George   │ 195000 │ Port Elizabeth Barbarians │  180000 │  15000 │
└─────────────────┴────────┴───────────────────────────┴─────────┴────────┘

```

Compare each player's salary to the maximum for their team.



```
SELECT
    player,
    salary,
    team,
    max(salary) OVER (PARTITION BY team) AS teamMax,
    salary - teamMax AS diff
FROM salaries;

```


```
┌─player──────────┬─salary─┬─team──────────────────────┬─teamMax─┬───diff─┐
│ Charles Juarez  │ 190000 │ New Coreystad Archdukes   │  190000 │      0 │
│ Scott Harrison  │ 150000 │ New Coreystad Archdukes   │  190000 │ -40000 │
│ Gary Chen       │ 195000 │ Port Elizabeth Barbarians │  195000 │      0 │
│ Michael Stanley │ 150000 │ Port Elizabeth Barbarians │  195000 │ -45000 │
│ Robert George   │ 195000 │ Port Elizabeth Barbarians │  195000 │      0 │
└─────────────────┴────────┴───────────────────────────┴─────────┴────────┘

```

### Partitioning by column[​](#partitioning-by-column "Direct link to Partitioning by column")



```
CREATE TABLE wf_partition
(
    `part_key` UInt64,
    `value` UInt64,
    `order` UInt64    
)
ENGINE = Memory;

INSERT INTO wf_partition FORMAT Values
   (1,1,1), (1,2,2), (1,3,3), (2,0,0), (3,0,0);

SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER (PARTITION BY part_key) AS frame_values
FROM wf_partition
ORDER BY
    part_key ASC,
    value ASC;

┌─part_key─┬─value─┬─order─┬─frame_values─┐
│        1 │     1 │     1 │ [1,2,3]      │   <┐   
│        1 │     2 │     2 │ [1,2,3]      │    │  1-st group
│        1 │     3 │     3 │ [1,2,3]      │   <┘ 
│        2 │     0 │     0 │ [0]          │   <- 2-nd group
│        3 │     0 │     0 │ [0]          │   <- 3-d group
└──────────┴───────┴───────┴──────────────┘

```

### Frame bounding[​](#frame-bounding "Direct link to Frame bounding")



```
CREATE TABLE wf_frame
(
    `part_key` UInt64,
    `value` UInt64,
    `order` UInt64
)
ENGINE = Memory;

INSERT INTO wf_frame FORMAT Values
   (1,1,1), (1,2,2), (1,3,3), (1,4,4), (1,5,5);

```


```
-- Frame is bounded by bounds of a partition (BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER (
        PARTITION BY part_key 
        ORDER BY order ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS frame_values
FROM wf_frame
ORDER BY
    part_key ASC,
    value ASC;
    
┌─part_key─┬─value─┬─order─┬─frame_values─┐
│        1 │     1 │     1 │ [1,2,3,4,5]  │
│        1 │     2 │     2 │ [1,2,3,4,5]  │
│        1 │     3 │     3 │ [1,2,3,4,5]  │
│        1 │     4 │     4 │ [1,2,3,4,5]  │
│        1 │     5 │     5 │ [1,2,3,4,5]  │
└──────────┴───────┴───────┴──────────────┘

```


```
-- short form - no bound expression, no order by,
-- an equalent of `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`
SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER (PARTITION BY part_key) AS frame_values_short,
    groupArray(value) OVER (PARTITION BY part_key
         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS frame_values
FROM wf_frame
ORDER BY
    part_key ASC,
    value ASC;
┌─part_key─┬─value─┬─order─┬─frame_values_short─┬─frame_values─┐
│        1 │     1 │     1 │ [1,2,3,4,5]        │ [1,2,3,4,5]  │
│        1 │     2 │     2 │ [1,2,3,4,5]        │ [1,2,3,4,5]  │
│        1 │     3 │     3 │ [1,2,3,4,5]        │ [1,2,3,4,5]  │
│        1 │     4 │     4 │ [1,2,3,4,5]        │ [1,2,3,4,5]  │
│        1 │     5 │     5 │ [1,2,3,4,5]        │ [1,2,3,4,5]  │
└──────────┴───────┴───────┴────────────────────┴──────────────┘

```


```
-- frame is bounded by the beginning of a partition and the current row
SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER (
        PARTITION BY part_key 
        ORDER BY order ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS frame_values
FROM wf_frame
ORDER BY
    part_key ASC,
    value ASC;

┌─part_key─┬─value─┬─order─┬─frame_values─┐
│        1 │     1 │     1 │ [1]          │
│        1 │     2 │     2 │ [1,2]        │
│        1 │     3 │     3 │ [1,2,3]      │
│        1 │     4 │     4 │ [1,2,3,4]    │
│        1 │     5 │     5 │ [1,2,3,4,5]  │
└──────────┴───────┴───────┴──────────────┘

```


```
-- short form (frame is bounded by the beginning of a partition and the current row)
-- an equalent of `ORDER BY order ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`
SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER (PARTITION BY part_key ORDER BY order ASC) AS frame_values_short,
    groupArray(value) OVER (PARTITION BY part_key ORDER BY order ASC
       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS frame_values
FROM wf_frame
ORDER BY
    part_key ASC,
    value ASC;

┌─part_key─┬─value─┬─order─┬─frame_values_short─┬─frame_values─┐
│        1 │     1 │     1 │ [1]                │ [1]          │
│        1 │     2 │     2 │ [1,2]              │ [1,2]        │
│        1 │     3 │     3 │ [1,2,3]            │ [1,2,3]      │
│        1 │     4 │     4 │ [1,2,3,4]          │ [1,2,3,4]    │
│        1 │     5 │     5 │ [1,2,3,4,5]        │ [1,2,3,4,5]  │
└──────────┴───────┴───────┴────────────────────┴──────────────┘

```


```
-- frame is bounded by the beginning of a partition and the current row, but order is backward
SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER (PARTITION BY part_key ORDER BY order DESC) AS frame_values
FROM wf_frame
ORDER BY
    part_key ASC,
    value ASC;

┌─part_key─┬─value─┬─order─┬─frame_values─┐
│        1 │     1 │     1 │ [5,4,3,2,1]  │
│        1 │     2 │     2 │ [5,4,3,2]    │
│        1 │     3 │     3 │ [5,4,3]      │
│        1 │     4 │     4 │ [5,4]        │
│        1 │     5 │     5 │ [5]          │
└──────────┴───────┴───────┴──────────────┘

```


```
-- sliding frame - 1 PRECEDING ROW AND CURRENT ROW
SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER (
        PARTITION BY part_key 
        ORDER BY order ASC
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    ) AS frame_values
FROM wf_frame
ORDER BY
    part_key ASC,
    value ASC;

┌─part_key─┬─value─┬─order─┬─frame_values─┐
│        1 │     1 │     1 │ [1]          │
│        1 │     2 │     2 │ [1,2]        │
│        1 │     3 │     3 │ [2,3]        │
│        1 │     4 │     4 │ [3,4]        │
│        1 │     5 │     5 │ [4,5]        │
└──────────┴───────┴───────┴──────────────┘

```


```
-- sliding frame - ROWS BETWEEN 1 PRECEDING AND UNBOUNDED FOLLOWING 
SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER (
        PARTITION BY part_key 
        ORDER BY order ASC
        ROWS BETWEEN 1 PRECEDING AND UNBOUNDED FOLLOWING
    ) AS frame_values
FROM wf_frame
ORDER BY
    part_key ASC,
    value ASC;

┌─part_key─┬─value─┬─order─┬─frame_values─┐
│        1 │     1 │     1 │ [1,2,3,4,5]  │
│        1 │     2 │     2 │ [1,2,3,4,5]  │
│        1 │     3 │     3 │ [2,3,4,5]    │
│        1 │     4 │     4 │ [3,4,5]      │
│        1 │     5 │     5 │ [4,5]        │
└──────────┴───────┴───────┴──────────────┘

```


```
-- row_number does not respect the frame, so rn_1 = rn_2 = rn_3 != rn_4
SELECT
    part_key,
    value,
    order,
    groupArray(value) OVER w1 AS frame_values,
    row_number() OVER w1 AS rn_1,
    sum(1) OVER w1 AS rn_2,
    row_number() OVER w2 AS rn_3,
    sum(1) OVER w2 AS rn_4
FROM wf_frame
WINDOW
    w1 AS (PARTITION BY part_key ORDER BY order DESC),
    w2 AS (
        PARTITION BY part_key 
        ORDER BY order DESC 
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    )
ORDER BY
    part_key ASC,
    value ASC;

┌─part_key─┬─value─┬─order─┬─frame_values─┬─rn_1─┬─rn_2─┬─rn_3─┬─rn_4─┐
│        1 │     1 │     1 │ [5,4,3,2,1]  │    5 │    5 │    5 │    2 │
│        1 │     2 │     2 │ [5,4,3,2]    │    4 │    4 │    4 │    2 │
│        1 │     3 │     3 │ [5,4,3]      │    3 │    3 │    3 │    2 │
│        1 │     4 │     4 │ [5,4]        │    2 │    2 │    2 │    2 │
│        1 │     5 │     5 │ [5]          │    1 │    1 │    1 │    1 │
└──────────┴───────┴───────┴──────────────┴──────┴──────┴──────┴──────┘

```


```
-- first_value and last_value respect the frame
SELECT
    groupArray(value) OVER w1 AS frame_values_1,
    first_value(value) OVER w1 AS first_value_1,
    last_value(value) OVER w1 AS last_value_1,
    groupArray(value) OVER w2 AS frame_values_2,
    first_value(value) OVER w2 AS first_value_2,
    last_value(value) OVER w2 AS last_value_2
FROM wf_frame
WINDOW
    w1 AS (PARTITION BY part_key ORDER BY order ASC),
    w2 AS (PARTITION BY part_key ORDER BY order ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)
ORDER BY
    part_key ASC,
    value ASC;

┌─frame_values_1─┬─first_value_1─┬─last_value_1─┬─frame_values_2─┬─first_value_2─┬─last_value_2─┐
│ [1]            │             1 │            1 │ [1]            │             1 │            1 │
│ [1,2]          │             1 │            2 │ [1,2]          │             1 │            2 │
│ [1,2,3]        │             1 │            3 │ [2,3]          │             2 │            3 │
│ [1,2,3,4]      │             1 │            4 │ [3,4]          │             3 │            4 │
│ [1,2,3,4,5]    │             1 │            5 │ [4,5]          │             4 │            5 │
└────────────────┴───────────────┴──────────────┴────────────────┴───────────────┴──────────────┘

```


```
-- second value within the frame
SELECT
    groupArray(value) OVER w1 AS frame_values_1,
    nth_value(value, 2) OVER w1 AS second_value
FROM wf_frame
WINDOW w1 AS (PARTITION BY part_key ORDER BY order ASC ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)
ORDER BY
    part_key ASC,
    value ASC;

┌─frame_values_1─┬─second_value─┐
│ [1]            │            0 │
│ [1,2]          │            2 │
│ [1,2,3]        │            2 │
│ [1,2,3,4]      │            2 │
│ [2,3,4,5]      │            3 │
└────────────────┴──────────────┘

```


```
-- second value within the frame + Null for missing values
SELECT
    groupArray(value) OVER w1 AS frame_values_1,
    nth_value(toNullable(value), 2) OVER w1 AS second_value
FROM wf_frame
WINDOW w1 AS (PARTITION BY part_key ORDER BY order ASC ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)
ORDER BY
    part_key ASC,
    value ASC;

┌─frame_values_1─┬─second_value─┐
│ [1]            │         ᴺᵁᴸᴸ │
│ [1,2]          │            2 │
│ [1,2,3]        │            2 │
│ [1,2,3,4]      │            2 │
│ [2,3,4,5]      │            3 │
└────────────────┴──────────────┘

```

## Real world examples[​](#real-world-examples "Direct link to Real world examples")


The following examples solve common real\-world problems.


### Maximum/total salary per department[​](#maximumtotal-salary-per-department "Direct link to Maximum/total salary per department")



```
CREATE TABLE employees
(
    `department` String,
    `employee_name` String,
    `salary` Float
)
ENGINE = Memory;

INSERT INTO employees FORMAT Values
   ('Finance', 'Jonh', 200),
   ('Finance', 'Joan', 210),
   ('Finance', 'Jean', 505),
   ('IT', 'Tim', 200),
   ('IT', 'Anna', 300),
   ('IT', 'Elen', 500);

```


```
SELECT
    department,
    employee_name AS emp,
    salary,
    max_salary_per_dep,
    total_salary_per_dep,
    round((salary / total_salary_per_dep) * 100, 2) AS `share_per_dep(%)`
FROM
(
    SELECT
        department,
        employee_name,
        salary,
        max(salary) OVER wndw AS max_salary_per_dep,
        sum(salary) OVER wndw AS total_salary_per_dep
    FROM employees
    WINDOW wndw AS (
        PARTITION BY department
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    )
    ORDER BY
        department ASC,
        employee_name ASC
);

┌─department─┬─emp──┬─salary─┬─max_salary_per_dep─┬─total_salary_per_dep─┬─share_per_dep(%)─┐
│ Finance    │ Jean │    505 │                505 │                  915 │            55.19 │
│ Finance    │ Joan │    210 │                505 │                  915 │            22.95 │
│ Finance    │ Jonh │    200 │                505 │                  915 │            21.86 │
│ IT         │ Anna │    300 │                500 │                 1000 │               30 │
│ IT         │ Elen │    500 │                500 │                 1000 │               50 │
│ IT         │ Tim  │    200 │                500 │                 1000 │               20 │
└────────────┴──────┴────────┴────────────────────┴──────────────────────┴──────────────────┘

```

### Cumulative sum[​](#cumulative-sum "Direct link to Cumulative sum")



```
CREATE TABLE warehouse
(
    `item` String,
    `ts` DateTime,
    `value` Float
)
ENGINE = Memory

INSERT INTO warehouse VALUES
    ('sku38', '2020-01-01', 9),
    ('sku38', '2020-02-01', 1),
    ('sku38', '2020-03-01', -4),
    ('sku1', '2020-01-01', 1),
    ('sku1', '2020-02-01', 1),
    ('sku1', '2020-03-01', 1);

```


```
SELECT
    item,
    ts,
    value,
    sum(value) OVER (PARTITION BY item ORDER BY ts ASC) AS stock_balance
FROM warehouse
ORDER BY
    item ASC,
    ts ASC;

┌─item──┬──────────────────ts─┬─value─┬─stock_balance─┐
│ sku1  │ 2020-01-01 00:00:00 │     1 │             1 │
│ sku1  │ 2020-02-01 00:00:00 │     1 │             2 │
│ sku1  │ 2020-03-01 00:00:00 │     1 │             3 │
│ sku38 │ 2020-01-01 00:00:00 │     9 │             9 │
│ sku38 │ 2020-02-01 00:00:00 │     1 │            10 │
│ sku38 │ 2020-03-01 00:00:00 │    -4 │             6 │
└───────┴─────────────────────┴───────┴───────────────┘

```

### Moving / sliding average (per 3 rows)[​](#moving--sliding-average-per-3-rows "Direct link to Moving / sliding average (per 3 rows)")



```
CREATE TABLE sensors
(
    `metric` String,
    `ts` DateTime,
    `value` Float
)
ENGINE = Memory;

insert into sensors values('cpu_temp', '2020-01-01 00:00:00', 87),
                          ('cpu_temp', '2020-01-01 00:00:01', 77),
                          ('cpu_temp', '2020-01-01 00:00:02', 93),
                          ('cpu_temp', '2020-01-01 00:00:03', 87),
                          ('cpu_temp', '2020-01-01 00:00:04', 87),
                          ('cpu_temp', '2020-01-01 00:00:05', 87),
                          ('cpu_temp', '2020-01-01 00:00:06', 87),
                          ('cpu_temp', '2020-01-01 00:00:07', 87);

```


```
SELECT
    metric,
    ts,
    value,
    avg(value) OVER (
        PARTITION BY metric 
        ORDER BY ts ASC 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_temp
FROM sensors
ORDER BY
    metric ASC,
    ts ASC;

┌─metric───┬──────────────────ts─┬─value─┬───moving_avg_temp─┐
│ cpu_temp │ 2020-01-01 00:00:00 │    87 │                87 │
│ cpu_temp │ 2020-01-01 00:00:01 │    77 │                82 │
│ cpu_temp │ 2020-01-01 00:00:02 │    93 │ 85.66666666666667 │
│ cpu_temp │ 2020-01-01 00:00:03 │    87 │ 85.66666666666667 │
│ cpu_temp │ 2020-01-01 00:00:04 │    87 │                89 │
│ cpu_temp │ 2020-01-01 00:00:05 │    87 │                87 │
│ cpu_temp │ 2020-01-01 00:00:06 │    87 │                87 │
│ cpu_temp │ 2020-01-01 00:00:07 │    87 │                87 │
└──────────┴─────────────────────┴───────┴───────────────────┘

```

### Moving / sliding average (per 10 seconds)[​](#moving--sliding-average-per-10-seconds "Direct link to Moving / sliding average (per 10 seconds)")



```
SELECT
    metric,
    ts,
    value,
    avg(value) OVER (PARTITION BY metric ORDER BY ts
      RANGE BETWEEN 10 PRECEDING AND CURRENT ROW) AS moving_avg_10_seconds_temp
FROM sensors
ORDER BY
    metric ASC,
    ts ASC;
    
┌─metric───┬──────────────────ts─┬─value─┬─moving_avg_10_seconds_temp─┐
│ cpu_temp │ 2020-01-01 00:00:00 │    87 │                         87 │
│ cpu_temp │ 2020-01-01 00:01:10 │    77 │                         77 │
│ cpu_temp │ 2020-01-01 00:02:20 │    93 │                         93 │
│ cpu_temp │ 2020-01-01 00:03:30 │    87 │                         87 │
│ cpu_temp │ 2020-01-01 00:04:40 │    87 │                         87 │
│ cpu_temp │ 2020-01-01 00:05:50 │    87 │                         87 │
│ cpu_temp │ 2020-01-01 00:06:00 │    87 │                         87 │
│ cpu_temp │ 2020-01-01 00:07:10 │    87 │                         87 │
└──────────┴─────────────────────┴───────┴────────────────────────────┘

```

### Moving / sliding average (per 10 days)[​](#moving--sliding-average-per-10-days "Direct link to Moving / sliding average (per 10 days)")


Temperature is stored with second precision, but using `Range` and `ORDER BY toDate(ts)` we form a frame with the size of 10 units, and because of `toDate(ts)` the unit is a day.



```
CREATE TABLE sensors
(
    `metric` String,
    `ts` DateTime,
    `value` Float
)
ENGINE = Memory;

insert into sensors values('ambient_temp', '2020-01-01 00:00:00', 16),
                          ('ambient_temp', '2020-01-01 12:00:00', 16),
                          ('ambient_temp', '2020-01-02 11:00:00', 9),
                          ('ambient_temp', '2020-01-02 12:00:00', 9),                          
                          ('ambient_temp', '2020-02-01 10:00:00', 10),
                          ('ambient_temp', '2020-02-01 12:00:00', 10),
                          ('ambient_temp', '2020-02-10 12:00:00', 12),                          
                          ('ambient_temp', '2020-02-10 13:00:00', 12),
                          ('ambient_temp', '2020-02-20 12:00:01', 16),
                          ('ambient_temp', '2020-03-01 12:00:00', 16),
                          ('ambient_temp', '2020-03-01 12:00:00', 16),
                          ('ambient_temp', '2020-03-01 12:00:00', 16);

```


```
SELECT
    metric,
    ts,
    value,
    round(avg(value) OVER (PARTITION BY metric ORDER BY toDate(ts) 
       RANGE BETWEEN 10 PRECEDING AND CURRENT ROW),2) AS moving_avg_10_days_temp
FROM sensors
ORDER BY
    metric ASC,
    ts ASC;

┌─metric───────┬──────────────────ts─┬─value─┬─moving_avg_10_days_temp─┐
│ ambient_temp │ 2020-01-01 00:00:00 │    16 │                      16 │
│ ambient_temp │ 2020-01-01 12:00:00 │    16 │                      16 │
│ ambient_temp │ 2020-01-02 11:00:00 │     9 │                    12.5 │
│ ambient_temp │ 2020-01-02 12:00:00 │     9 │                    12.5 │
│ ambient_temp │ 2020-02-01 10:00:00 │    10 │                      10 │
│ ambient_temp │ 2020-02-01 12:00:00 │    10 │                      10 │
│ ambient_temp │ 2020-02-10 12:00:00 │    12 │                      11 │
│ ambient_temp │ 2020-02-10 13:00:00 │    12 │                      11 │
│ ambient_temp │ 2020-02-20 12:00:01 │    16 │                   13.33 │
│ ambient_temp │ 2020-03-01 12:00:00 │    16 │                      16 │
│ ambient_temp │ 2020-03-01 12:00:00 │    16 │                      16 │
│ ambient_temp │ 2020-03-01 12:00:00 │    16 │                      16 │
└──────────────┴─────────────────────┴───────┴─────────────────────────┘

```

## References[​](#references "Direct link to References")


### GitHub Issues[​](#github-issues "Direct link to GitHub Issues")


The roadmap for the initial support of window functions is [in this issue](https://github.com/ClickHouse/ClickHouse/issues/18097).


All GitHub issues related to window functions have the [comp\-window\-functions](https://github.com/ClickHouse/ClickHouse/labels/comp-window-functions) tag.


### Tests[​](#tests "Direct link to Tests")


These tests contain the examples of the currently supported grammar:


<https://github.com/ClickHouse/ClickHouse/blob/master/tests/performance/window_functions.xml>


<https://github.com/ClickHouse/ClickHouse/blob/master/tests/queries/0_stateless/01591_window_functions.sql>


### Postgres Docs[​](#postgres-docs "Direct link to Postgres Docs")


[https://www.postgresql.org/docs/current/sql\-select.html\#SQL\-WINDOW](https://www.postgresql.org/docs/current/sql-select.html#SQL-WINDOW)


[https://www.postgresql.org/docs/devel/sql\-expressions.html\#SYNTAX\-WINDOW\-FUNCTIONS](https://www.postgresql.org/docs/devel/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)


[https://www.postgresql.org/docs/devel/functions\-window.html](https://www.postgresql.org/docs/devel/functions-window.html)


[https://www.postgresql.org/docs/devel/tutorial\-window.html](https://www.postgresql.org/docs/devel/tutorial-window.html)


### MySQL Docs[​](#mysql-docs "Direct link to MySQL Docs")


[https://dev.mysql.com/doc/refman/8\.0/en/window\-function\-descriptions.html](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html)


[https://dev.mysql.com/doc/refman/8\.0/en/window\-functions\-usage.html](https://dev.mysql.com/doc/refman/8.0/en/window-functions-usage.html)


[https://dev.mysql.com/doc/refman/8\.0/en/window\-functions\-frames.html](https://dev.mysql.com/doc/refman/8.0/en/window-functions-frames.html)


## Related Content[​](#related-content "Direct link to Related Content")


- Blog: [Working with time series data in ClickHouse](https://clickhouse.com/blog/working-with-time-series-data-and-functions-ClickHouse)
- Blog: [Window and array functions for Git commit sequences](https://clickhouse.com/blog/clickhouse-window-array-functions-git-commits)
- Blog: [Getting Data Into ClickHouse \- Part 3 \- Using S3](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3)
[Previousloop](/docs/sql-reference/table-functions/loop)[Nextrow\_number](/docs/sql-reference/window-functions/row_number)- [Standard window functions](#standard-window-functions)- [ClickHouse\-specific window functions](#clickhouse-specific-window-functions)
	- [nonNegativeDerivative(metric\_column, timestamp\_column\[, INTERVAL X UNITS])](#nonnegativederivativemetric_column-timestamp_column-interval-x-units)- [Syntax](#syntax)
	- [Functions](#functions)- [Examples](#examples)
	- [Numbering rows](#numbering-rows)- [Aggregation functions](#aggregation-functions)- [Partitioning by column](#partitioning-by-column)- [Frame bounding](#frame-bounding)- [Real world examples](#real-world-examples)
	- [Maximum/total salary per department](#maximumtotal-salary-per-department)- [Cumulative sum](#cumulative-sum)- [Moving / sliding average (per 3 rows)](#moving--sliding-average-per-3-rows)- [Moving / sliding average (per 10 seconds)](#moving--sliding-average-per-10-seconds)- [Moving / sliding average (per 10 days)](#moving--sliding-average-per-10-days)- [References](#references)
	- [GitHub Issues](#github-issues)- [Tests](#tests)- [Postgres Docs](#postgres-docs)- [MySQL Docs](#mysql-docs)- [Related Content](#related-content)
Was this page helpful?
