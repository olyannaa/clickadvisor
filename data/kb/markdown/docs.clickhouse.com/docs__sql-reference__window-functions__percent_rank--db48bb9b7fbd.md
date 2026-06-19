# percent\_rank \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Window functions](/docs/sql-reference/window-functions)- percent\_rank
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/window-functions/percent_rank.md)# percent\_rank

returns the relative rank (i.e. percentile) of rows within a window partition.


**Syntax**


Alias: `percentRank` (case\-sensitive)



```
percent_rank ()
  OVER ([[PARTITION BY grouping_column] [ORDER BY sorting_column]
        [RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING]] | [window_name])
FROM table_name
WINDOW window_name as ([PARTITION BY grouping_column] [ORDER BY sorting_column] RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)

```

The default and required window frame definition is `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.


For more detail on window function syntax see: [Window Functions \- Syntax](/docs/sql-reference/window-functions#syntax).


**Example**



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
    ('Port Elizabeth Barbarians', 'Robert George', 195000, 'M'),
    ('South Hampton Seagulls', 'Douglas Benson', 150000, 'M'),
    ('South Hampton Seagulls', 'James Henderson', 140000, 'M');

```


```
SELECT player, salary,
       percent_rank() OVER (ORDER BY salary DESC) AS percent_rank
FROM salaries;

```


```

   ┌─player──────────┬─salary─┬───────percent_rank─┐
1. │ Gary Chen       │ 195000 │                  0 │
2. │ Robert George   │ 195000 │                  0 │
3. │ Charles Juarez  │ 190000 │ 0.3333333333333333 │
4. │ Michael Stanley │ 150000 │                0.5 │
5. │ Scott Harrison  │ 150000 │                0.5 │
6. │ Douglas Benson  │ 150000 │                0.5 │
7. │ James Henderson │ 140000 │                  1 │
   └─────────────────┴────────┴────────────────────┘


```
[Previousdense\_rank](/docs/sql-reference/window-functions/dense_rank)[Nextlag](/docs/sql-reference/window-functions/lag)Was this page helpful?
