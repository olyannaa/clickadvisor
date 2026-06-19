# values \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- values
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/values.md)# values

The `Values` table function allows you to create temporary storage which fills
columns with values. It is useful for quick testing or generating sample data.


NoteValues is a case\-insensitive function. I.e. `VALUES` or `values` are both valid.


## Syntax[​](#syntax "Direct link to Syntax")


The basic syntax of the `VALUES` table function is:



```
VALUES([structure,] values...)

```

It is commonly used as:



```
VALUES(
    ['column1_name Type1, column2_name Type2, ...'],
    (value1_row1, value2_row1, ...),
    (value1_row2, value2_row2, ...),
    ...
)

```

## Arguments[​](#arguments "Direct link to Arguments")


- `column1_name Type1, ...` (optional). [String](/docs/sql-reference/data-types/string)
specifying the column names and types. If this argument is omitted columns will
be named as `c1`, `c2`, etc.
- `(value1_row1, value2_row1)`. [Tuples](/docs/sql-reference/data-types/tuple)
containing values of any type.


NoteComma separated tuples can be replaced by single values as well. In this case
each value is taken to be a new row. See the [examples](#examples) section for
details.


## Returned value[​](#returned-value "Direct link to Returned value")


- Returns a temporary table containing the provided values.


## Examples[​](#examples "Direct link to Examples")



```
SELECT *
FROM VALUES(
    'person String, place String',
    ('Noah', 'Paris'),
    ('Emma', 'Tokyo'),
    ('Liam', 'Sydney'),
    ('Olivia', 'Berlin'),
    ('Ilya', 'London'),
    ('Sophia', 'London'),
    ('Jackson', 'Madrid'),
    ('Alexey', 'Amsterdam'),
    ('Mason', 'Venice'),
    ('Isabella', 'Prague')
)

```


```
    ┌─person───┬─place─────┐
 1. │ Noah     │ Paris     │
 2. │ Emma     │ Tokyo     │
 3. │ Liam     │ Sydney    │
 4. │ Olivia   │ Berlin    │
 5. │ Ilya     │ London    │
 6. │ Sophia   │ London    │
 7. │ Jackson  │ Madrid    │
 8. │ Alexey   │ Amsterdam │
 9. │ Mason    │ Venice    │
10. │ Isabella │ Prague    │
    └──────────┴───────────┘

```

`VALUES` can also be used with single values rather than tuples. For example:



```
SELECT *
FROM VALUES(
    'person String',
    'Noah',
    'Emma',
    'Liam',
    'Olivia',
    'Ilya',
    'Sophia',
    'Jackson',
    'Alexey',
    'Mason',
    'Isabella'
)

```


```
    ┌─person───┐
 1. │ Noah     │
 2. │ Emma     │
 3. │ Liam     │
 4. │ Olivia   │
 5. │ Ilya     │
 6. │ Sophia   │
 7. │ Jackson  │
 8. │ Alexey   │
 9. │ Mason    │
10. │ Isabella │
    └──────────┘

```

Or without providing a row specification (`'column1_name Type1, column2_name Type2, ...'`
in the [syntax](#syntax)), in which case the columns are automatically named.


For example:



```
-- tuples as values
SELECT *
FROM VALUES(
    ('Noah', 'Paris'),
    ('Emma', 'Tokyo'),
    ('Liam', 'Sydney'),
    ('Olivia', 'Berlin'),
    ('Ilya', 'London'),
    ('Sophia', 'London'),
    ('Jackson', 'Madrid'),
    ('Alexey', 'Amsterdam'),
    ('Mason', 'Venice'),
    ('Isabella', 'Prague')
)

```


```
    ┌─c1───────┬─c2────────┐
 1. │ Noah     │ Paris     │
 2. │ Emma     │ Tokyo     │
 3. │ Liam     │ Sydney    │
 4. │ Olivia   │ Berlin    │
 5. │ Ilya     │ London    │
 6. │ Sophia   │ London    │
 7. │ Jackson  │ Madrid    │
 8. │ Alexey   │ Amsterdam │
 9. │ Mason    │ Venice    │
10. │ Isabella │ Prague    │
    └──────────┴───────────┘

```


```
-- single values
SELECT *
FROM VALUES(
    'Noah',
    'Emma',
    'Liam',
    'Olivia',
    'Ilya',
    'Sophia',
    'Jackson',
    'Alexey',
    'Mason',
    'Isabella'
)

```


```
    ┌─c1───────┐
 1. │ Noah     │
 2. │ Emma     │
 3. │ Liam     │
 4. │ Olivia   │
 5. │ Ilya     │
 6. │ Sophia   │
 7. │ Jackson  │
 8. │ Alexey   │
 9. │ Mason    │
10. │ Isabella │
    └──────────┘

```

## SQL Standard VALUES Clause[​](#sql-standard-values-clause "Direct link to SQL Standard VALUES Clause")


From version 26\.3, ClickHouse also supports the SQL standard `VALUES` clause as a table expression
in `FROM`, as used in PostgreSQL, MySQL, DuckDB, and SQL Server. This syntax is
rewritten internally to use the `values` table function described above.



```
SELECT * FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) AS t(id, val);

```


```
┌─id─┬─val─┐
│  1 │ a   │
│  2 │ b   │
│  3 │ c   │
└────┴─────┘

```

It can be used in CTEs:



```
WITH cte AS (SELECT * FROM (VALUES (1, 'one'), (2, 'two')) AS t(id, name))
SELECT * FROM cte;

```

And in JOINs:



```
SELECT t1.id, t1.val, t2.val2
FROM (VALUES (1, 'a'), (2, 'b')) AS t1(id, val)
JOIN (VALUES (1, 'x'), (2, 'y')) AS t2(id, val2) ON t1.id = t2.id;

```

NoteColumn aliases after `AS t(col1, col2, ...)` follow the standard SQL syntax for
naming columns of derived tables. If omitted, columns are named `c1`, `c2`, etc.


## See also[​](#see-also "Direct link to See also")


- [Values format](/docs/interfaces/formats/Values)
[PreviousurlCluster](/docs/sql-reference/table-functions/urlCluster)[Nextview](/docs/sql-reference/table-functions/view)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned-value)- [Examples](#examples)- [SQL Standard VALUES Clause](#sql-standard-values-clause)- [See also](#see-also)
Was this page helpful?
