# Functions for Working with Geographical Coordinates \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- [Geometry](/docs/sql-reference/functions/geo)- Geographical Coordinates
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/geo/coordinates.md)# Functions for Working with Geographical Coordinates

## greatCircleDistance[​](#greatcircledistance "Direct link to greatCircleDistance")


Calculates the distance between two points on the Earth's surface using [the great\-circle formula](https://en.wikipedia.org/wiki/Great-circle_distance).



```
greatCircleDistance(lon1Deg, lat1Deg, lon2Deg, lat2Deg)

```

**Input parameters**


- `lon1Deg` — Longitude of the first point in degrees. Range: `[-180°, 180°]`.
- `lat1Deg` — Latitude of the first point in degrees. Range: `[-90°, 90°]`.
- `lon2Deg` — Longitude of the second point in degrees. Range: `[-180°, 180°]`.
- `lat2Deg` — Latitude of the second point in degrees. Range: `[-90°, 90°]`.


Positive values correspond to North latitude and East longitude, and negative values correspond to South latitude and West longitude.


**Returned value**


The distance between two points on the Earth's surface, in meters.


Generates an exception when the input parameter values fall outside of the range.


**Example**



```
SELECT greatCircleDistance(55.755831, 37.617673, -55.755831, -37.617673) AS greatCircleDistance

```


```
┌─greatCircleDistance─┐
│            14128352 │
└─────────────────────┘

```

## geoDistance[​](#geodistance "Direct link to geoDistance")


Similar to `greatCircleDistance` but calculates the distance on WGS\-84 ellipsoid instead of sphere. This is more precise approximation of the Earth Geoid.
The performance is the same as for `greatCircleDistance` (no performance drawback). It is recommended to use `geoDistance` to calculate the distances on Earth.


Technical note: for close enough points we calculate the distance using planar approximation with the metric on the tangent plane at the midpoint of the coordinates.



```
geoDistance(lon1Deg, lat1Deg, lon2Deg, lat2Deg)

```

**Input parameters**


- `lon1Deg` — Longitude of the first point in degrees. Range: `[-180°, 180°]`.
- `lat1Deg` — Latitude of the first point in degrees. Range: `[-90°, 90°]`.
- `lon2Deg` — Longitude of the second point in degrees. Range: `[-180°, 180°]`.
- `lat2Deg` — Latitude of the second point in degrees. Range: `[-90°, 90°]`.


Positive values correspond to North latitude and East longitude, and negative values correspond to South latitude and West longitude.


**Returned value**


The distance between two points on the Earth's surface, in meters.


Generates an exception when the input parameter values fall outside of the range.


**Example**



```
SELECT geoDistance(38.8976, -77.0366, 39.9496, -75.1503) AS geoDistance

```


```
┌─geoDistance─┐
│   212458.73 │
└─────────────┘

```

## greatCircleAngle[​](#greatcircleangle "Direct link to greatCircleAngle")


Calculates the central angle between two points on the Earth's surface using [the great\-circle formula](https://en.wikipedia.org/wiki/Great-circle_distance).



```
greatCircleAngle(lon1Deg, lat1Deg, lon2Deg, lat2Deg)

```

**Input parameters**


- `lon1Deg` — Longitude of the first point in degrees.
- `lat1Deg` — Latitude of the first point in degrees.
- `lon2Deg` — Longitude of the second point in degrees.
- `lat2Deg` — Latitude of the second point in degrees.


**Returned value**


The central angle between two points in degrees.


**Example**



```
SELECT greatCircleAngle(0, 0, 45, 0) AS arc

```


```
┌─arc─┐
│  45 │
└─────┘

```

## pointInEllipses[​](#pointinellipses "Direct link to pointInEllipses")


Checks whether the point belongs to at least one of the ellipses.
Coordinates are geometric in the Cartesian coordinate system.



```
pointInEllipses(x, y, x₀, y₀, a₀, b₀,...,xₙ, yₙ, aₙ, bₙ)

```

**Input parameters**


- `x, y` — Coordinates of a point on the plane.
- `xᵢ, yᵢ` — Coordinates of the center of the `i`\-th ellipsis.
- `aᵢ, bᵢ` — Axes of the `i`\-th ellipsis in units of x, y coordinates.


The input parameters must be `2+4⋅n`, where `n` is the number of ellipses.


**Returned values**


`1` if the point is inside at least one of the ellipses; `0`if it is not.


**Example**



```
SELECT pointInEllipses(10., 10., 10., 9.1, 1., 0.9999)

```


```
┌─pointInEllipses(10., 10., 10., 9.1, 1., 0.9999)─┐
│                                               1 │
└─────────────────────────────────────────────────┘

```

## pointInPolygon[​](#pointinpolygon "Direct link to pointInPolygon")


Checks whether the point belongs to the polygon on the plane.



```
pointInPolygon((x, y), [(a, b), (c, d) ...], ...)

```

**Input values**


- `(x, y)` — Coordinates of a point on the plane. Data type — [Tuple](/docs/sql-reference/data-types/tuple) — A tuple of two numbers.
- `[(a, b), (c, d) ...]` — Polygon vertices. Data type — [Array](/docs/sql-reference/data-types/array). Each vertex is represented by a pair of coordinates `(a, b)`. Vertices should be specified in a clockwise or counterclockwise order. The minimum number of vertices is 3\. The polygon must be constant.
- The function supports polygon with holes (cut\-out sections). Data type — [Polygon](/docs/sql-reference/data-types/geo#polygon). Either pass the entire `Polygon` as the second argument, or pass the outer ring first and then each hole as separate additional arguments.
- The function also supports multipolygon. Data type — [MultiPolygon](/docs/sql-reference/data-types/geo#multipolygon). Either pass the entire `MultiPolygon` as the second argument, or list each component polygon as its own argument.


**Returned values**


`1` if the point is inside the polygon, `0` if it is not.
If the point is on the polygon boundary, the function may return either 0 or 1\.


**Example**



```
SELECT pointInPolygon((3., 3.), [(6, 0), (8, 4), (5, 8), (0, 2)]) AS res

```


```
┌─res─┐
│   1 │
└─────┘

```


> **Note**  
> 
> • You can set `validate_polygons = 0` to bypass geometry validation.  
> 
> • `pointInPolygon` assumes every polygon is well\-formed. If the input is self\-intersecting, has mis\-ordered rings, or overlapping edges, results become unreliable—especially for points that sit exactly on an edge, a vertex, or inside a self\-intersection where the notion of "inside" vs. "outside" is undefined.
> • When the polygon argument is constant and the point is expressed using indexed key columns (for example, `pointInPolygon((x, y), constant_polygon)` on a table where `x, y` are part of the `PRIMARY KEY` or covered by a `minmax` index), ClickHouse can use both the primary key and `minmax` data\-skipping indexes to prune irrelevant granules.

[PreviousFlip Coordinates](/docs/sql-reference/functions/geo/flipCoordinates)[NextGeohash](/docs/sql-reference/functions/geo/geohash)- [greatCircleDistance](#greatcircledistance)- [geoDistance](#geodistance)- [greatCircleAngle](#greatcircleangle)- [pointInEllipses](#pointinellipses)- [pointInPolygon](#pointinpolygon)
Was this page helpful?
