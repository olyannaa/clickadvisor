# Geometric \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- Geo
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/geo.md)# Geometric

ClickHouse supports data types for representing geographical objects — locations, lands, etc.


**See Also**


- [Representing simple geographical features](https://en.wikipedia.org/wiki/GeoJSON).


## Point[​](#point "Direct link to Point")


`Point` is represented by its X and Y coordinates, stored as a [Tuple](/docs/sql-reference/data-types/tuple)([Float64](/docs/sql-reference/data-types/float), [Float64](/docs/sql-reference/data-types/float)).


**Example**



```
CREATE TABLE geo_point (p Point) ENGINE = Memory();
INSERT INTO geo_point VALUES((10, 10));
SELECT p, toTypeName(p) FROM geo_point;

```


```
┌─p───────┬─toTypeName(p)─┐
│ (10,10) │ Point         │
└─────────┴───────────────┘

```

## Ring[​](#ring "Direct link to Ring")


`Ring` is a simple polygon without holes stored as an array of points: [Array](/docs/sql-reference/data-types/array)([Point](#point)).


**Example**



```
CREATE TABLE geo_ring (r Ring) ENGINE = Memory();
INSERT INTO geo_ring VALUES([(0, 0), (10, 0), (10, 10), (0, 10)]);
SELECT r, toTypeName(r) FROM geo_ring;

```


```
┌─r─────────────────────────────┬─toTypeName(r)─┐
│ [(0,0),(10,0),(10,10),(0,10)] │ Ring          │
└───────────────────────────────┴───────────────┘

```

## LineString[​](#linestring "Direct link to LineString")


`LineString` is a line stored as an array of points: [Array](/docs/sql-reference/data-types/array)([Point](#point)).


**Example**



```
CREATE TABLE geo_linestring (l LineString) ENGINE = Memory();
INSERT INTO geo_linestring VALUES([(0, 0), (10, 0), (10, 10), (0, 10)]);
SELECT l, toTypeName(l) FROM geo_linestring;

```


```
┌─r─────────────────────────────┬─toTypeName(r)─┐
│ [(0,0),(10,0),(10,10),(0,10)] │ LineString    │
└───────────────────────────────┴───────────────┘

```

## MultiLineString[​](#multilinestring "Direct link to MultiLineString")


`MultiLineString` is multiple lines stored as an array of `LineString`: [Array](/docs/sql-reference/data-types/array)([LineString](#linestring)).


**Example**



```
CREATE TABLE geo_multilinestring (l MultiLineString) ENGINE = Memory();
INSERT INTO geo_multilinestring VALUES([[(0, 0), (10, 0), (10, 10), (0, 10)], [(1, 1), (2, 2), (3, 3)]]);
SELECT l, toTypeName(l) FROM geo_multilinestring;

```


```
┌─l───────────────────────────────────────────────────┬─toTypeName(l)───┐
│ [[(0,0),(10,0),(10,10),(0,10)],[(1,1),(2,2),(3,3)]] │ MultiLineString │
└─────────────────────────────────────────────────────┴─────────────────┘

```

## Polygon[​](#polygon "Direct link to Polygon")


`Polygon` is a polygon with holes stored as an array of rings: [Array](/docs/sql-reference/data-types/array)([Ring](#ring)). First element of outer array is the outer shape of polygon and all the following elements are holes.


**Example**


This is a polygon with one hole:



```
CREATE TABLE geo_polygon (pg Polygon) ENGINE = Memory();
INSERT INTO geo_polygon VALUES([[(20, 20), (50, 20), (50, 50), (20, 50)], [(30, 30), (50, 50), (50, 30)]]);
SELECT pg, toTypeName(pg) FROM geo_polygon;

```


```
┌─pg────────────────────────────────────────────────────────────┬─toTypeName(pg)─┐
│ [[(20,20),(50,20),(50,50),(20,50)],[(30,30),(50,50),(50,30)]] │ Polygon        │
└───────────────────────────────────────────────────────────────┴────────────────┘

```

## MultiPolygon[​](#multipolygon "Direct link to MultiPolygon")


`MultiPolygon` consists of multiple polygons and is stored as an array of polygons: [Array](/docs/sql-reference/data-types/array)([Polygon](#polygon)).


**Example**


This multipolygon consists of two separate polygons — the first one without holes, and the second with one hole:



```
CREATE TABLE geo_multipolygon (mpg MultiPolygon) ENGINE = Memory();
INSERT INTO geo_multipolygon VALUES([[[(0, 0), (10, 0), (10, 10), (0, 10)]], [[(20, 20), (50, 20), (50, 50), (20, 50)],[(30, 30), (50, 50), (50, 30)]]]);
SELECT mpg, toTypeName(mpg) FROM geo_multipolygon;

```


```
┌─mpg─────────────────────────────────────────────────────────────────────────────────────────────┬─toTypeName(mpg)─┐
│ [[[(0,0),(10,0),(10,10),(0,10)]],[[(20,20),(50,20),(50,50),(20,50)],[(30,30),(50,50),(50,30)]]] │ MultiPolygon    │
└─────────────────────────────────────────────────────────────────────────────────────────────────┴─────────────────┘

```

## Geometry[​](#geometry "Direct link to Geometry")


`Geometry` is a common type for all the types above. It is equivalent to a Variant of those types.


**Example**



```
CREATE TABLE IF NOT EXISTS geo (geom Geometry) ENGINE = Memory();
INSERT INTO geo VALUES ((1, 2));
SELECT * FROM geo;

```


```
   ┌─geom──┐
1. │ (1,2) │
   └───────┘

```


```
CREATE TABLE IF NOT EXISTS geo_dst (geom Geometry) ENGINE = Memory();

CREATE TABLE IF NOT EXISTS geo (geom String, id Int) ENGINE = Memory();
INSERT INTO geo VALUES ('POLYGON((1 0,10 0,10 10,0 10,1 0),(4 4,5 4,5 5,4 5,4 4))', 1);
INSERT INTO geo VALUES ('POINT(0 0)', 2);
INSERT INTO geo VALUES ('MULTIPOLYGON(((1 0,10 0,10 10,0 10,1 0),(4 4,5 4,5 5,4 5,4 4)),((-10 -10,-10 -9,-9 10,-10 -10)))', 3);
INSERT INTO geo VALUES ('LINESTRING(1 0,10 0,10 10,0 10,1 0)', 4);
INSERT INTO geo VALUES ('MULTILINESTRING((1 0,10 0,10 10,0 10,1 0),(4 4,5 4,5 5,4 5,4 4))', 5);
INSERT INTO geo_dst SELECT readWKT(geom) FROM geo ORDER BY id;

SELECT * FROM geo_dst;

```


```
   ┌─geom─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
1. │ [[(1,0),(10,0),(10,10),(0,10),(1,0)],[(4,4),(5,4),(5,5),(4,5),(4,4)]]                                            │
2. │ (0,0)                                                                                                            │
3. │ [[[(1,0),(10,0),(10,10),(0,10),(1,0)],[(4,4),(5,4),(5,5),(4,5),(4,4)]],[[(-10,-10),(-10,-9),(-9,10),(-10,-10)]]] │
4. │ [(1,0),(10,0),(10,10),(0,10),(1,0)]                                                                              │
5. │ [[(1,0),(10,0),(10,10),(0,10),(1,0)],[(4,4),(5,4),(5,5),(4,5),(4,4)]]                                            │
   └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## Related Content[​](#related-content "Direct link to Related Content")


- [Exploring massive, real\-world data sets: 100\+ Years of Weather Records in ClickHouse](https://clickhouse.com/blog/real-world-data-noaa-climate-data)
[PreviousSimpleAggregateFunction](/docs/sql-reference/data-types/simpleaggregatefunction)[NextSpecial Data Types](/docs/sql-reference/data-types/special-data-types)- [Point](#point)- [Ring](#ring)- [LineString](#linestring)- [MultiLineString](#multilinestring)- [Polygon](#polygon)- [MultiPolygon](#multipolygon)- [Geometry](#geometry)- [Related Content](#related-content)
Was this page helpful?
