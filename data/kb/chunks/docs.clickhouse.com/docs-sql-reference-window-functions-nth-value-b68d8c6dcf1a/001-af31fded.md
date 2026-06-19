---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/window-functions/nth_value.md)#
topic: nth-value-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 1
---

# nth\_value \| ClickHouse Docs

- - [Functions](/docs/sql-reference/functions)- [Window functions](/docs/sql-reference/window-functions)- nth\_value
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/window-functions/nth_value.md)# nth\_value

Returns the first non\-NULL value evaluated against the nth row (offset) in its ordered frame.

**Syntax**

```
nth_value (x, offset)
  OVER ([[PARTITION BY grouping_column] [ORDER BY sorting_column] 
        [ROWS or RANGE expression_to_bound_rows_withing_the_group]] | [window_name])
FROM table_name
WINDOW window_name as ([[PARTITION BY grouping_column] [ORDER BY sorting_column])

```

For more detail on window function syntax see: [Window Functions \- Syntax](/docs/sql-reference/window-functions#syntax).

**Parameters**

- `x` — Column name.
- `offset` — nth row to evaluate current row against.

**Returned value**

- The first non\-NULL value evaluated against the nth row (offset) in its ordered frame.

**Example**

In this example the `nth-value` function is used to find the third\-highest salary from a fictional dataset of salaries of Premier League football players.

```
DROP TABLE IF EXISTS salaries;
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
    ('Port Elizabeth Barbarians', 'Michael Stanley', 100000, 'D'),
    ('New Coreystad Archdukes', 'Scott Harrison', 180000, 'D'),
    ('Port Elizabeth Barbarians', 'Robert George', 195000, 'M'),
    ('South Hampton Seagulls', 'Douglas Benson', 150000, 'M'),
    ('South Hampton Seagulls', 'James Henderson', 140000, 'M');

```

```
SELECT player, salary, nth_value(player,3) OVER(ORDER BY salary DESC) AS third_highest_salary FROM salaries;

```

```
   ┌─player──────────┬─salary─┬─third_highest_salary─┐
1. │ Gary Chen       │ 195000 │                      │
2. │ Robert George   │ 195000 │                      │
3. │ Charles Juarez  │ 190000 │ Charles Juarez       │
4. │ Scott Harrison  │ 180000 │ Charles Juarez       │
5. │ Douglas Benson  │ 150000 │ Charles Juarez       │
6. │ James Henderson │ 140000 │ Charles Juarez       │
7. │ Michael Stanley │ 100000 │ Charles Juarez       │
   └─────────────────┴────────┴──────────────────────┘

```
[Previouslast\_value](/docs/sql-reference/window-functions/last_value)[Nextrank](/docs/sql-reference/window-functions/rank)Was this page helpful?
