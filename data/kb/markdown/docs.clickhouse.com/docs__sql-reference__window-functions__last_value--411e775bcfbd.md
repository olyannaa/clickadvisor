# last\_value \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Window functions](/docs/sql-reference/window-functions)- last\_value
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/window-functions/last_value.md)# last\_value

Returns the last value evaluated within its ordered frame. By default, NULL arguments are skipped, however the `RESPECT NULLS` modifier can be used to override this behaviour.


**Syntax**



```
last_value (column_name) [[RESPECT NULLS] | [IGNORE NULLS]]
  OVER ([[PARTITION BY grouping_column] [ORDER BY sorting_column] 
        [ROWS or RANGE expression_to_bound_rows_withing_the_group]] | [window_name])
FROM table_name
WINDOW window_name as ([[PARTITION BY grouping_column] [ORDER BY sorting_column])

```

Alias: `anyLast`.


NoteUsing the optional modifier `RESPECT NULLS` after `first_value(column_name)` will ensure that `NULL` arguments are not skipped.
See [NULL processing](/docs/sql-reference/aggregate-functions#null-processing) for more information.Alias: `lastValueRespectNulls`




For more detail on window function syntax see: [Window Functions \- Syntax](/docs/sql-reference/window-functions#syntax).


**Returned value**


- The last value evaluated within its ordered frame.


**Example**


In this example the `last_value` function is used to find the lowest paid footballer from a fictional dataset of salaries of Premier League football players.



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

INSERT INTO salaries FORMAT VALUES
    ('Port Elizabeth Barbarians', 'Gary Chen', 196000, 'F'),
    ('New Coreystad Archdukes', 'Charles Juarez', 190000, 'F'),
    ('Port Elizabeth Barbarians', 'Michael Stanley', 100000, 'D'),
    ('New Coreystad Archdukes', 'Scott Harrison', 180000, 'D'),
    ('Port Elizabeth Barbarians', 'Robert George', 195000, 'M'),
    ('South Hampton Seagulls', 'Douglas Benson', 150000, 'M'),
    ('South Hampton Seagulls', 'James Henderson', 140000, 'M');

```


```
SELECT player, salary,
       last_value(player) OVER (ORDER BY salary DESC RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS lowest_paid_player
FROM salaries;

```


```
   ┌─player──────────┬─salary─┬─lowest_paid_player─┐
1. │ Gary Chen       │ 196000 │ Michael Stanley    │
2. │ Robert George   │ 195000 │ Michael Stanley    │
3. │ Charles Juarez  │ 190000 │ Michael Stanley    │
4. │ Scott Harrison  │ 180000 │ Michael Stanley    │
5. │ Douglas Benson  │ 150000 │ Michael Stanley    │
6. │ James Henderson │ 140000 │ Michael Stanley    │
7. │ Michael Stanley │ 100000 │ Michael Stanley    │
   └─────────────────┴────────┴────────────────────┘

```
[Previousfirst\_value](/docs/sql-reference/window-functions/first_value)[Nextnth\_value](/docs/sql-reference/window-functions/nth_value)Was this page helpful?
