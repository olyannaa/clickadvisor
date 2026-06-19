# Functions for Working with Geometry \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- [Geometry](/docs/sql-reference/functions/geo)- Geometry
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/geo/geometry.md)# Functions for Working with Geometry

## Geometry[​](#geometry "Direct link to Geometry")


Geometry functions allow you to calculate perimeter and area for geometric types such as POLYGON, LINESTRING, MULTIPOLYGON, MULTILINESTRING, RING, and POINT. Use geometries in Geometry type. If the input value is `NULL`, all functions below will return 0\.


## perimeterCartesian[​](#perimetercartesian "Direct link to perimeterCartesian")


Calculates the perimeter of the given Geometry object in the Cartesian (flat) coordinate system.


**Syntax**



```
perimeterCartesian(geom)

```

**Arguments**


- `geom` — Geometry object. [Geometry](/docs/sql-reference/data-types/geo).


**Returned values**


- Number — Perimeter of the object in the coordinate system units. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
CREATE TABLE IF NOT EXISTS geo_dst (geom Geometry) ENGINE = Memory();
INSERT INTO geo_dst SELECT readWKT('POLYGON((0 0,1 0,1 1,0 1,0 0))');
SELECT perimeterCartesian(geom) FROM geo_dst;

```


```
┌─perimeterCartesian(geom)─┐
│ 4.0                      │
└──────────────────────────┘

```

## areaCartesian[​](#areacartesian "Direct link to areaCartesian")


Calculates the area of the given Geometry object in the Cartesian coordinate system.


**Syntax**



```
areaCartesian(geom)

```

**Arguments**


- `geom` — Geometry object. [Geometry](/docs/sql-reference/data-types/geo).


**Returned values**


- Number — Area of the object in coordinate system units. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
CREATE TABLE IF NOT EXISTS geo_dst (geom Geometry) ENGINE = Memory();
INSERT INTO geo_dst SELECT readWKT('POLYGON((0 0,1 0,1 1,0 1,0 0))');
SELECT areaCartesian(geom) FROM geo_dst;

```


```
┌─areaCartesian(geom)─┐
│ -1                  │
└─────────────────────┘

```

## perimeterSpherical[​](#perimeterspherical "Direct link to perimeterSpherical")


Calculates the perimeter of a Geometry object on the surface of a sphere.


**Syntax**



```
perimeterSpherical(geom)

```

**Arguments**


- `geom` — Geometry object. [Geometry](/docs/sql-reference/data-types/geo).


**Returned values**


- Number — Perimeter. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
CREATE TABLE IF NOT EXISTS geo_dst (geom Geometry) ENGINE = Memory();
INSERT INTO geo_dst SELECT readWKT('LINESTRING(0 0,1 0,1 1,0 1,0 0)');
SELECT perimeterSpherical(geom) FROM geo_dst;

```


```
┌─perimeterSpherical(geom)─┐
│ 0                        │
└──────────────────────────┘

```

## areaSpherical[​](#areaspherical "Direct link to areaSpherical")


Calculates the area of a Geometry object on the surface of a sphere.


**Syntax**



```
areaSpherical(geom)

```

**Arguments**


- `geom` — Geometry. [Geometry](/docs/sql-reference/data-types/geo).


**Returned values**


- Number — Area. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
CREATE TABLE IF NOT EXISTS geo_dst (geom Geometry) ENGINE = Memory();
INSERT INTO geo_dst SELECT readWKT('POLYGON((0 0,1 0,1 1,0 1,0 0))');
SELECT areaSpherical(geom) FROM geo_dst;

```


```
┌─areaSpherical(geom)────┐
│ -0.0003046096848622019 │
└────────────────────────┘

```
[PreviousGeohash](/docs/sql-reference/functions/geo/geohash)[NextH3 Indexes](/docs/sql-reference/functions/geo/h3)- [Geometry](#geometry)- [perimeterCartesian](#perimetercartesian)- [areaCartesian](#areacartesian)- [perimeterSpherical](#perimeterspherical)- [areaSpherical](#areaspherical)
Was this page helpful?
