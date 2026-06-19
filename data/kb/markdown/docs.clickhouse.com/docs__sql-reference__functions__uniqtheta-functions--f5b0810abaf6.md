# uniqTheta Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- uniqTheta
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/uniqtheta-functions.md)# uniqTheta Functions

uniqTheta functions work for two uniqThetaSketch objects to do set operation calculations such as ∪ / ∩ / × (union/intersect/not), it is to return a new uniqThetaSketch object contain the result.


A uniqThetaSketch object is to be constructed by aggregation function uniqTheta with \-State.


UniqThetaSketch is a data structure storage of approximate values set.
For more information, see: [Theta Sketch Framework](https://datasketches.apache.org/docs/Theta/ThetaSketches.html#theta-sketch-framework).


## uniqThetaUnion[​](#uniqthetaunion "Direct link to uniqThetaUnion")


Two uniqThetaSketch objects to do union calculation(set operation ∪), the result is a new uniqThetaSketch.



```
uniqThetaUnion(uniqThetaSketch,uniqThetaSketch)

```

**Arguments**


- `uniqThetaSketch` – uniqThetaSketch object.


**Example**



```
SELECT finalizeAggregation(uniqThetaUnion(a, b)) AS a_union_b, finalizeAggregation(a) AS a_cardinality, finalizeAggregation(b) AS b_cardinality
FROM
(SELECT arrayReduce('uniqThetaState',[1,2]) AS a, arrayReduce('uniqThetaState',[2,3,4]) AS b );

```


```
┌─a_union_b─┬─a_cardinality─┬─b_cardinality─┐
│         4 │             2 │             3 │
└───────────┴───────────────┴───────────────┘

```

## uniqThetaIntersect[​](#uniqthetaintersect "Direct link to uniqThetaIntersect")


Two uniqThetaSketch objects to do intersect calculation(set operation ∩), the result is a new uniqThetaSketch.



```
uniqThetaIntersect(uniqThetaSketch,uniqThetaSketch)

```

**Arguments**


- `uniqThetaSketch` – uniqThetaSketch object.


**Example**



```
SELECT finalizeAggregation(uniqThetaIntersect(a, b)) AS a_intersect_b, finalizeAggregation(a) AS a_cardinality, finalizeAggregation(b) AS b_cardinality
FROM
(SELECT arrayReduce('uniqThetaState',[1,2]) AS a, arrayReduce('uniqThetaState',[2,3,4]) AS b );

```


```
┌─a_intersect_b─┬─a_cardinality─┬─b_cardinality─┐
│             1 │             2 │             3 │
└───────────────┴───────────────┴───────────────┘

```

## uniqThetaNot[​](#uniqthetanot "Direct link to uniqThetaNot")


Two uniqThetaSketch objects to do a\_not\_b calculation(set operation ×), the result is a new uniqThetaSketch.



```
uniqThetaNot(uniqThetaSketch,uniqThetaSketch)

```

**Arguments**


- `uniqThetaSketch` – uniqThetaSketch object.


**Example**



```
SELECT finalizeAggregation(uniqThetaNot(a, b)) AS a_not_b, finalizeAggregation(a) AS a_cardinality, finalizeAggregation(b) AS b_cardinality
FROM
(SELECT arrayReduce('uniqThetaState',[2,3,4]) AS a, arrayReduce('uniqThetaState',[1,2]) AS b );

```


```
┌─a_not_b─┬─a_cardinality─┬─b_cardinality─┐
│       2 │             3 │             2 │
└─────────┴───────────────┴───────────────┘

```

**See Also**


- [uniqThetaSketch](/docs/sql-reference/aggregate-functions/reference/uniqthetasketch)
[PreviousULIDs](/docs/sql-reference/functions/ulid-functions)[NextURLs](/docs/sql-reference/functions/url-functions)- [uniqThetaUnion](#uniqthetaunion)- [uniqThetaIntersect](#uniqthetaintersect)- [uniqThetaNot](#uniqthetanot)
Was this page helpful?
