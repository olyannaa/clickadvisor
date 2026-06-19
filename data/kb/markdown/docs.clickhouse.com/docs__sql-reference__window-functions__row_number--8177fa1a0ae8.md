# row\_number \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Window functions](/docs/sql-reference/window-functions)- row\_number
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/window-functions/row_number.md)# row\_number

Numbers the current row within its partition starting from 1\.


**Syntax**



```
row_number (column_name)
  OVER ([[PARTITION BY grouping_column] [ORDER BY sorting_column] 
        [ROWS or RANGE expression_to_bound_rows_withing_the_group]] | [window_name])
FROM table_name
WINDOW window_name as ([[PARTITION BY grouping_column] [ORDER BY sorting_column])

```

For more detail on window function syntax see: [Window Functions \- Syntax](/docs/sql-reference/window-functions#syntax).


**Returned value**


- A number for the current row within its partition. [UInt64](/docs/sql-reference/data-types/int-uint).


**Example**


The following example is based on the example provided in the video instructional [Ranking window functions in ClickHouse](https://youtu.be/Yku9mmBYm_4?si=XIMu1jpYucCQEoXA).



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
SELECT player, salary, 
       row_number() OVER (ORDER BY salary DESC) AS row_number
FROM salaries;

```


```
   ┌─player──────────┬─salary─┬─row_number─┐
1. │ Gary Chen       │ 195000 │          1 │
2. │ Robert George   │ 195000 │          2 │
3. │ Charles Juarez  │ 190000 │          3 │
4. │ Scott Harrison  │ 150000 │          4 │
5. │ Michael Stanley │ 150000 │          5 │
   └─────────────────┴────────┴────────────┘

```
[PreviousWindow Functions](/docs/sql-reference/window-functions)[Nextfirst\_value](/docs/sql-reference/window-functions/first_value)Was this page helpful?
