# groupArrayIntersect \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupArrayIntersect
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupArrayIntersect.md)# groupArrayIntersect

## groupArrayIntersect[​](#groupArrayIntersect "Direct link to groupArrayIntersect")


Introduced in: v24\.2\.0


Return an intersection of given arrays (Return all items of arrays, that are in all given arrays).


**Syntax**



```
groupArrayIntersect(x)

```

**Arguments**


- `x` — Argument (column name or expression). [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns an array that contains elements that are in all arrays. [`Array`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
-- Create table with Memory engine
CREATE TABLE numbers (
    a Array(Int32)
) ENGINE = Memory;

-- Insert sample data
INSERT INTO numbers VALUES
    ([1,2,4]),
    ([1,5,2,8,-1,0]),
    ([1,5,7,5,8,2]);

SELECT groupArrayIntersect(a) AS intersection FROM numbers;

```


```
┌─intersection──────┐
│ [1, 2]            │
└───────────────────┘

```
[PreviousgroupArrayInsertAt](/docs/sql-reference/aggregate-functions/reference/grouparrayinsertat)[NextgroupArrayLast](/docs/sql-reference/aggregate-functions/reference/grouparraylast)- [groupArrayIntersect](#groupArrayIntersect)
Was this page helpful?
