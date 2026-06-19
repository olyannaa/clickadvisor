# groupArraySorted \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- groupArraySorted
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/groupArraySorted.md)# groupArraySorted

## groupArraySorted[​](#groupArraySorted "Direct link to groupArraySorted")


Introduced in: v24\.2\.0


Returns an array with the first N items in ascending order.


**Syntax**



```
groupArraySorted(N)(column)

```

**Parameters**


- `N` — The number of elements to return. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Arguments**


- `column` — Column for which to group into an array. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns an array with the first N items in ascending order. [`Array`](/docs/sql-reference/data-types/array)


**Examples**


**Getting first 10 numbers**



```
SELECT groupArraySorted(10)(number) FROM numbers(100);

```


```
┌─groupArraySorted(10)(number)─┐
│ [0,1,2,3,4,5,6,7,8,9]        │
└──────────────────────────────┘

```

**String sorting example**



```
SELECT groupArraySorted(5)(str) FROM (SELECT toString(number) AS str FROM numbers(5));

```


```
┌─groupArraySorted(5)(str)─┐
│ ['0','1','2','3','4']    │
└──────────────────────────┘

```
[PreviousgroupArraySample](/docs/sql-reference/aggregate-functions/reference/grouparraysample)[NextgroupBitAnd](/docs/sql-reference/aggregate-functions/reference/groupbitand)- [groupArraySorted](#groupArraySorted)
Was this page helpful?
