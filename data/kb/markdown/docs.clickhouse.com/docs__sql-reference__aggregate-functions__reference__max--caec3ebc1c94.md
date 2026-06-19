# max \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- max
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/max.md)# max

## max[​](#max "Direct link to max")


Introduced in: v1\.1\.0


Aggregate function that calculates the maximum across a group of values.


**Syntax**



```
max(column)

```

**Arguments**


- `column` — Column name or expression. [`Any`](/docs/sql-reference/data-types)


**Returned value**


The maximum value across the group with type equal to that of the input. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Simple max example**



```
CREATE TABLE employees (name String, salary UInt32) ENGINE = Memory;
INSERT INTO employees VALUES ('Alice', 3000), ('Bob', 4000), ('Charlie', 3500);

SELECT max(salary) FROM employees;

```


```
┌─max(salary)─┐
│        4000 │
└─────────────┘

```

**Max with GROUP BY**



```
CREATE TABLE sales (department String, revenue UInt32) ENGINE = Memory;
INSERT INTO sales VALUES ('Engineering', 100000), ('Engineering', 120000), ('Marketing', 80000), ('Marketing', 90000);

SELECT department, max(revenue) FROM sales GROUP BY department ORDER BY department;

```


```
┌─department──┬─max(revenue)─┐
│ Engineering │       120000 │
│ Marketing   │        90000 │
└─────────────┴──────────────┘

```

**Note about non\-aggregate maximum**



```
-- If you need non-aggregate function to choose a maximum of two values, see greatest():
SELECT greatest(a, b) FROM table;

```

[PreviousmannWhitneyUTest](/docs/sql-reference/aggregate-functions/reference/mannwhitneyutest)[NextmaxIntersections](/docs/sql-reference/aggregate-functions/reference/maxintersections)- [max](#max)
Was this page helpful?
