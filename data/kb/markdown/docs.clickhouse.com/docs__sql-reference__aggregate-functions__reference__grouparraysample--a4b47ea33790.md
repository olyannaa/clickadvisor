# groupArraySample \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupArraySample
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupArraySample.md)# groupArraySample

## groupArraySample[​](#groupArraySample "Direct link to groupArraySample")


Introduced in: v20\.3\.0


Creates an array of sample argument values.
The size of the resulting array is limited to `max_size` elements.
Argument values are selected and added to the array randomly.


**Syntax**



```
groupArraySample(max_size[, seed])(x)

```

**Parameters**


- `max_size` — Maximum size of the resulting array. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `seed` — Optional. Seed for the random number generator. Default value: 123456\. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `x` — Argument (column name or expression). [`Any`](/docs/sql-reference/data-types)


**Arguments**


- `array_column` — Column containing arrays to be aggregated. [`Array`](/docs/sql-reference/data-types/array)


**Returned value**


Array of randomly selected x arguments. [`Array(T)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
CREATE TABLE default.colors (
    id Int32,
    color String
) ENGINE = Memory;

INSERT INTO default.colors VALUES
(1, 'red'),
(2, 'blue'),
(3, 'green'),
(4, 'white'),
(5, 'orange');

SELECT groupArraySample(3)(color) as newcolors FROM default.colors;

```


```
┌─newcolors──────────────────┐
│ ['white','blue','green']   │
└────────────────────────────┘

```

**Example using a seed**



```
-- Query with column name and different seed
SELECT groupArraySample(3, 987654321)(color) as newcolors FROM default.colors;

```


```
┌─newcolors──────────────────┐
│ ['red','orange','green']   │
└────────────────────────────┘

```

**Using an expression as an argument**



```
-- Query with expression as argument
SELECT groupArraySample(3)(concat('light-', color)) as newcolors FROM default.colors;

```


```
┌─newcolors───────────────────────────────────┐
│ ['light-blue','light-orange','light-green'] │
└─────────────────────────────────────────────┘

```
[PreviousgroupArrayMovingSum](/docs/sql-reference/aggregate-functions/reference/grouparraymovingsum)[NextgroupArraySorted](/docs/sql-reference/aggregate-functions/reference/grouparraysorted)- [groupArraySample](#groupArraySample)
Was this page helpful?
