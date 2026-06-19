# sumWithOverflow \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- sumWithOverflow
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/sumWithOverflow.md)# sumWithOverflow

## sumWithOverflow[​](#sumWithOverflow "Direct link to sumWithOverflow")


Introduced in: v1\.1\.0


Computes a sum of numeric values, using the same data type for the result as for the input parameters.
If the sum exceeds the maximum value for this data type, it is calculated with overflow.


**Syntax**



```
sumWithOverflow(num)

```

**Arguments**


- `num` — Column of numeric values. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)


**Returned value**


The sum of the values. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)


**Examples**


**Demonstrating overflow behavior with UInt16**



```
CREATE TABLE employees
(
    id UInt32,
    name String,
    monthly_salary UInt16 -- selected so that the sum of values produces an overflow
)
ENGINE = Memory;

INSERT INTO employees VALUES
    (1, 'John', 20000),
    (2, 'Jane', 18000),
    (3, 'Bob', 12000),
    (4, 'Alice', 10000),
    (5, 'Charlie', 8000);

-- Query for the total amount of the employee salaries using the sum and sumWithOverflow functions and show their types using the toTypeName function
-- For the sum function the resulting type is UInt64, big enough to contain the sum, whilst for sumWithOverflow the resulting type remains as UInt16.

SELECT
    sum(monthly_salary) AS no_overflow,
    sumWithOverflow(monthly_salary) AS overflow,
    toTypeName(no_overflow),
    toTypeName(overflow)
FROM employees;

```


```
┌─no_overflow─┬─overflow─┬─toTypeName(no_overflow)─┬─toTypeName(overflow)─┐
│       68000 │     2464 │ UInt64                  │ UInt16               │
└─────────────┴──────────┴─────────────────────────┴──────────────────────┘

```
[PrevioussumMap](/docs/sql-reference/aggregate-functions/reference/summap)[NexttheilsU](/docs/sql-reference/aggregate-functions/reference/theilsu)- [sumWithOverflow](#sumWithOverflow)
Was this page helpful?
