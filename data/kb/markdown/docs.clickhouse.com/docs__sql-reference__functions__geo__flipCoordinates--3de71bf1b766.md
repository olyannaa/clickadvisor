# Flipping Coordinates \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- [Geometry](/docs/sql-reference/functions/geo)- Flip Coordinates
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/geo/flipCoordinates.md)# Flipping Coordinates

## flipCoordinates[​](#flipcoordinates "Direct link to flipCoordinates")


The `flipCoordinates` function swaps the coordinates of a point, ring, polygon, or multipolygon. This is useful, for example, when converting between coordinate systems where the order of latitude and longitude differs.



```
flipCoordinates(coordinates)

```

### Input Parameters[​](#input-parameters "Direct link to Input Parameters")


- `coordinates` — A tuple representing a point `(x, y)`, or an array of such tuples representing a ring, polygon, or multipolygon. Supported input types include:
	- [**Point**](/docs/sql-reference/data-types/geo#point): A tuple `(x, y)` where `x` and `y` are [Float64](/docs/sql-reference/data-types/float) values.
	- [**Ring**](/docs/sql-reference/data-types/geo#ring): An array of points `[(x1, y1), (x2, y2), ...]`.
	- [**Polygon**](/docs/sql-reference/data-types/geo#polygon): An array of rings `[ring1, ring2, ...]`, where each ring is an array of points.
	- [**Multipolygon**](/docs/sql-reference/data-types/geo#multipolygon): An array of polygons `[polygon1, polygon2, ...]`.


### Returned Value[​](#returned-value "Direct link to Returned Value")


The function returns the input with the coordinates flipped. For example:


- A point `(x, y)` becomes `(y, x)`.
- A ring `[(x1, y1), (x2, y2)]` becomes `[(y1, x1), (y2, x2)]`.
- Nested structures like polygons and multipolygons are processed recursively.


### Examples[​](#examples "Direct link to Examples")


#### Example 1: Flipping a Single Point[​](#example-1 "Direct link to Example 1: Flipping a Single Point")



```
SELECT flipCoordinates((10, 20)) AS flipped_point

```


```
┌─flipped_point─┐
│ (20,10)       │
└───────────────┘

```

#### Example 2: Flipping an Array of Points (Ring)[​](#example-2 "Direct link to Example 2: Flipping an Array of Points (Ring)")



```
SELECT flipCoordinates([(10, 20), (30, 40)]) AS flipped_ring

```


```
┌─flipped_ring──────────────┐
│ [(20,10),(40,30)]         │
└───────────────────────────┘

```

#### Example 3: Flipping a Polygon[​](#example-3 "Direct link to Example 3: Flipping a Polygon")



```
SELECT flipCoordinates([[(10, 20), (30, 40)], [(50, 60), (70, 80)]]) AS flipped_polygon

```


```
┌─flipped_polygon──────────────────────────────┐
│ [[(20,10),(40,30)],[(60,50),(80,70)]]        │
└──────────────────────────────────────────────┘

```

#### Example 4: Flipping a Multipolygon[​](#example-4 "Direct link to Example 4: Flipping a Multipolygon")



```
SELECT flipCoordinates([[[10, 20], [30, 40]], [[50, 60], [70, 80]]]) AS flipped_multipolygon

```


```
┌─flipped_multipolygon──────────────────────────────┐
│ [[[20,10],[40,30]],[[60,50],[80,70]]]             │
└───────────────────────────────────────────────────┘

```
[PreviousGeo](/docs/sql-reference/functions/geo)[NextGeographical Coordinates](/docs/sql-reference/functions/geo/coordinates)- [flipCoordinates](#flipcoordinates)
	- [Input Parameters](#input-parameters)- [Returned Value](#returned-value)- [Examples](#examples)
Was this page helpful?
