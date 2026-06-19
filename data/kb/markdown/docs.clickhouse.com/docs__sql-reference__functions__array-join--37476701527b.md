# arrayJoin function \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- arrayJoin
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/array-join.md)# arrayJoin function

This is a very unusual function.


Normal functions do not change a set of rows, but just change the values in each row (map).
Aggregate functions compress a set of rows (fold or reduce).
The `arrayJoin` function takes each row and generates a set of rows (unfold).


This function takes an array as an argument, and propagates the source row to multiple rows for the number of elements in the array.
All the values in columns are simply copied, except the values in the column where this function is applied; it is replaced with the corresponding array value.


NoteIf the array is empty, `arrayJoin` produces no rows.
To return a single row containing the default value of the array type, you can wrap it with [emptyArrayToSingle](/docs/sql-reference/functions/array-functions#emptyArrayToSingle), for example: `arrayJoin(emptyArrayToSingle(...))`.


For example:



```
SELECT arrayJoin([1, 2, 3] AS src) AS dst, 'Hello', src

```


```
┌─dst─┬─\'Hello\'─┬─src─────┐
│   1 │ Hello     │ [1,2,3] │
│   2 │ Hello     │ [1,2,3] │
│   3 │ Hello     │ [1,2,3] │
└─────┴───────────┴─────────┘

```

The `arrayJoin` function affects all sections of the query, including the `WHERE` section. Notice in that the result of the query below is `2`, even though the subquery returned 1 row.



```
SELECT sum(1) AS impressions
FROM
(
    SELECT ['Istanbul', 'Berlin', 'Babruysk'] AS cities
)
WHERE arrayJoin(cities) IN ['Istanbul', 'Berlin'];

```


```
┌─impressions─┐
│           2 │
└─────────────┘

```

A query can use multiple `arrayJoin` functions. In this case, the transformation is performed multiple times and the rows are multiplied.
For example:



```
SELECT
    sum(1) AS impressions,
    arrayJoin(cities) AS city,
    arrayJoin(browsers) AS browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Babruysk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
GROUP BY
    2,
    3

```


```
┌─impressions─┬─city─────┬─browser─┐
│           2 │ Istanbul │ Chrome  │
│           1 │ Istanbul │ Firefox │
│           2 │ Berlin   │ Chrome  │
│           1 │ Berlin   │ Firefox │
│           2 │ Babruysk │ Chrome  │
│           1 │ Babruysk │ Firefox │
└─────────────┴──────────┴─────────┘

```

### Best practice[​](#important-note "Direct link to Best practice")


Using multiple `arrayJoin` with same expression may not produce expected results due to the elimination of common subexpressions.
In those cases, consider modifying repeated array expressions with extra operations that do not affect the join result. For example, `arrayJoin(arraySort(arr))`, `arrayJoin(arrayConcat(arr, []))`


Example:



```
SELECT
    arrayJoin(dice) AS first_throw,
    /* arrayJoin(dice) as second_throw */ -- is technically correct, but will annihilate result set
    arrayJoin(arrayConcat(dice, [])) AS second_throw -- intentionally changed expression to force re-evaluation
FROM (
    SELECT [1, 2, 3, 4, 5, 6] AS dice
);

```

Note the [`ARRAY JOIN`](/docs/sql-reference/statements/select/array-join) syntax in the SELECT query, which provides broader possibilities.
`ARRAY JOIN` allows you to convert multiple arrays with the same number of elements at a time.


Example:



```
SELECT
    sum(1) AS impressions,
    city,
    browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Babruysk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
ARRAY JOIN
    cities AS city,
    browsers AS browser
GROUP BY
    2,
    3

```


```
┌─impressions─┬─city─────┬─browser─┐
│           1 │ Istanbul │ Firefox │
│           1 │ Berlin   │ Chrome  │
│           1 │ Babruysk │ Chrome  │
└─────────────┴──────────┴─────────┘

```

Or you can use [`Tuple`](/docs/sql-reference/data-types/tuple)


Example:



```
SELECT
    sum(1) AS impressions,
    (arrayJoin(arrayZip(cities, browsers)) AS t).1 AS city,
    t.2 AS browser
FROM
(
    SELECT
        ['Istanbul', 'Berlin', 'Babruysk'] AS cities,
        ['Firefox', 'Chrome', 'Chrome'] AS browsers
)
GROUP BY
    2,
    3

```


```
┌─impressions─┬─city─────┬─browser─┐
│           1 │ Istanbul │ Firefox │
│           1 │ Berlin   │ Chrome  │
│           1 │ Babruysk │ Chrome  │
└─────────────┴──────────┴─────────┘

```

The name `arrayJoin` in ClickHouse comes from its conceptual similarity to the JOIN operation, but applied to arrays within a single row. While traditional JOINs combine rows from different tables, `arrayJoin` "joins" each element of an array in a row, producing multiple rows \- one for each array element \- while duplicating the other column values. ClickHouse also provides the [`ARRAY JOIN`](/docs/sql-reference/statements/select/array-join) clause syntax, which makes this relationship to traditional JOIN operations even more explicit by using familiar SQL JOIN terminology. This process is also referred to as "unfolding" the array, but the term "join" is used in both the function name and clause because it resembles joining the table with the array elements, effectively expanding the dataset in a way similar to a JOIN operation.

[PreviousArrays](/docs/sql-reference/functions/array-functions)[NextBit](/docs/sql-reference/functions/bit-functions)- [Best practice](#important-note)
Was this page helpful?
