# Functions for Working with H3 Indexes \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- [Geometry](/docs/sql-reference/functions/geo)- H3 Indexes
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/geo/h3.md)# Functions for Working with H3 Indexes

## H3 Index[​](#h3-index "Direct link to H3 Index")


[H3](https://h3geo.org/) is a geographical indexing system where the Earth's surface is divided into a grid of even hexagonal cells. This system is hierarchical, i. e. each hexagon on the top level ("parent") can be split into seven even but smaller ones ("children"), and so on.


The level of the hierarchy is called `resolution` and can receive a value from `0` till `15`, where `0` is the `base` level with the largest and coarsest cells.


A latitude and longitude pair can be transformed to a 64\-bit H3 index, identifying a grid cell.


The H3 index is used primarily for bucketing locations and other geospatial manipulations.


The full description of the H3 system is available at [the Uber Engineering site](https://www.uber.com/blog/h3/).


## h3IsValid[​](#h3isvalid "Direct link to h3IsValid")


Verifies whether the number is a valid [H3](#h3-index) index.


**Syntax**



```
h3IsValid(h3index)

```

**Parameter**


- `h3index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned values**


- 1 — The number is a valid H3 index. [UInt8](/docs/sql-reference/data-types/int-uint).
- 0 — The number is not a valid H3 index. [UInt8](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3IsValid(630814730351855103) AS h3IsValid;

```


```
┌─h3IsValid─┐
│         1 │
└───────────┘

```

## h3GetResolution[​](#h3getresolution "Direct link to h3GetResolution")


Defines the resolution of the given [H3](#h3-index) index.


**Syntax**



```
h3GetResolution(h3index)

```

**Parameter**


- `h3index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned values**


- Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).
- If the index is not valid, the function returns a random value. Use [h3IsValid](#h3isvalid) to verify the index. [UInt8](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3GetResolution(639821929606596015) AS resolution;

```


```
┌─resolution─┐
│         14 │
└────────────┘

```

## h3EdgeAngle[​](#h3edgeangle "Direct link to h3EdgeAngle")


Calculates the average length of an [H3](#h3-index) hexagon edge in grades.


**Syntax**



```
h3EdgeAngle(resolution)

```

**Parameter**


- `resolution` — Index resolution. [UInt8](/docs/sql-reference/data-types/int-uint). Range: `[0, 15]`.


**Returned values**


- The average length of an [H3](#h3-index) hexagon edge in grades. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3EdgeAngle(10) AS edgeAngle;

```


```
┌───────h3EdgeAngle(10)─┐
│ 0.0005927224846720883 │
└───────────────────────┘

```

## h3EdgeLengthM[​](#h3edgelengthm "Direct link to h3EdgeLengthM")


Calculates the average length of an [H3](#h3-index) hexagon edge in meters.


**Syntax**



```
h3EdgeLengthM(resolution)

```

**Parameter**


- `resolution` — Index resolution. [UInt8](/docs/sql-reference/data-types/int-uint). Range: `[0, 15]`.


**Returned values**


- The average edge length of an [H3](#h3-index) hexagon in meters. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3EdgeLengthM(15) AS edgeLengthM;

```


```
┌─edgeLengthM─┐
│ 0.509713273 │
└─────────────┘

```

## h3EdgeLengthKm[​](#h3edgelengthkm "Direct link to h3EdgeLengthKm")


Calculates the average length of an [H3](#h3-index) hexagon edge in kilometers.


**Syntax**



```
h3EdgeLengthKm(resolution)

```

**Parameter**


- `resolution` — Index resolution. [UInt8](/docs/sql-reference/data-types/int-uint). Range: `[0, 15]`.


**Returned values**


- The average length of an [H3](#h3-index) hexagon edge in kilometers. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3EdgeLengthKm(15) AS edgeLengthKm;

```


```
┌─edgeLengthKm─┐
│  0.000509713 │
└──────────────┘

```

## geoToH3[​](#geotoh3 "Direct link to geoToH3")


Returns [H3](#h3-index) point index `(lat, lon)` with specified resolution.


**Syntax**



```
geoToH3(lat, lon, resolution)

```

**Arguments**


- `lat` — Latitude. [Float64](/docs/sql-reference/data-types/float).
- `lon` — Longitude. [Float64](/docs/sql-reference/data-types/float).
- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned values**


- Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).
- 0 in case of error. [UInt64](/docs/sql-reference/data-types/int-uint).


Note: In ClickHouse v25\.4 or older, `geoToH3()` takes values in order `(lon, lat)`. As per ClickHouse v25\.5, the input values are in order `(lat, lon)`. The previous behaviour can be restored using setting `geotoh3_argument_order = 'lon_lat'`.


**Example**



```
SELECT geoToH3(55.71290588, 37.79506683, 15) AS h3Index;

```


```
┌────────────h3Index─┐
│ 644325524701193974 │
└────────────────────┘

```

## h3ToGeo[​](#h3togeo "Direct link to h3ToGeo")


Returns the centroid latitude and longitude corresponding to the provided [H3](#h3-index) index.


**Syntax**



```
h3ToGeo(h3Index)

```

**Arguments**


- `h3Index` — H3 Index. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned values**


- A tuple consisting of two values: `tuple(lat,lon)`. `lat` — Latitude. [Float64](/docs/sql-reference/data-types/float). `lon` — Longitude. [Float64](/docs/sql-reference/data-types/float).


Note: In ClickHouse v24\.12 or older, `h3ToGeo()` returns values in order `(lon, lat)`. As per ClickHouse v25\.1, the returned values are in order `(lat, lon)`. The previous behaviour can be restored using setting `h3togeo_lon_lat_result_order = true`.


**Example**



```
SELECT h3ToGeo(644325524701193974) AS coordinates;

```


```
┌─coordinates───────────────────────────┐
│ (55.71290243145668,37.79506616830252) │
└───────────────────────────────────────┘

```

## h3ToGeoBoundary[​](#h3togeoboundary "Direct link to h3ToGeoBoundary")


Returns array of pairs `(lat, lon)`, which corresponds to the boundary of the provided H3 index.


**Syntax**



```
h3ToGeoBoundary(h3Index)

```

**Arguments**


- `h3Index` — H3 Index. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned values**


- Array of pairs '(lat, lon)'. [Array](/docs/sql-reference/data-types/array)([Float64](/docs/sql-reference/data-types/float), [Float64](/docs/sql-reference/data-types/float)).


**Example**



```
SELECT h3ToGeoBoundary(644325524701193974) AS coordinates;

```


```
┌─h3ToGeoBoundary(599686042433355775)────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [(37.2713558667319,-121.91508032705622),(37.353926450852256,-121.8622232890249),(37.42834118609435,-121.92354999630156),(37.42012867767779,-122.03773496427027),(37.33755608435299,-122.090428929044),(37.26319797461824,-122.02910130919001)] │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## h3kRing[​](#h3kring "Direct link to h3kRing")


Lists all the [H3](#h3-index) hexagons in the raduis of `k` from the given hexagon in random order.


**Syntax**



```
h3kRing(h3index, k)

```

**Arguments**


- `h3index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).
- `k` — Radius. [integer](/docs/sql-reference/data-types/int-uint)


**Returned values**


- Array of H3 indexes. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
SELECT arrayJoin(h3kRing(644325529233966508, 1)) AS h3index;

```


```
┌────────────h3index─┐
│ 644325529233966508 │
│ 644325529233966497 │
│ 644325529233966510 │
│ 644325529233966504 │
│ 644325529233966509 │
│ 644325529233966355 │
│ 644325529233966354 │
└────────────────────┘

```

## h3PolygonToCells[​](#h3polygontocells "Direct link to h3PolygonToCells")


Returns the hexagons (at specified resolution) contained by the provided geometry, either ring or (multi\-)polygon.


**Syntax**



```
h3PolygonToCells(geometry, resolution)

```

**Arguments**


- `geometry` can be one of the following [Geo Data Types](/docs/sql-reference/data-types/geo) or their underlying primitive types:
	- [Ring](/docs/sql-reference/data-types/geo#ring)
	- [Polygon](/docs/sql-reference/data-types/geo#polygon)
	- [MultiPolygon](/docs/sql-reference/data-types/geo#multipolygon)
- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned values**


- Array of the contained H3\-indexes. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
SELECT h3PolygonToCells([(-122.4089866999972145,37.813318999983238),(-122.3544736999993603,37.7198061999978478),(-122.4798767000009008,37.8151571999998453)], 7) AS h3index;

```


```
┌────────────h3index─┐
│ 608692970769612799 │
│ 608692971927240703 │
│ 608692970585063423 │
│ 608692970819944447 │
│ 608692970719281151 │
│ 608692970752835583 │
│ 608692972027903999 │
└────────────────────┘

```

## h3GetBaseCell[​](#h3getbasecell "Direct link to h3GetBaseCell")


Returns the base cell number of the [H3](#h3-index) index.


**Syntax**



```
h3GetBaseCell(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Hexagon base cell number. [UInt8](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3GetBaseCell(612916788725809151) AS basecell;

```


```
┌─basecell─┐
│       12 │
└──────────┘

```

## h3HexAreaM2[​](#h3hexaream2 "Direct link to h3HexAreaM2")


Returns average hexagon area in square meters at the given resolution.


**Syntax**



```
h3HexAreaM2(resolution)

```

**Parameter**


- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Area in square meters. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3HexAreaM2(13) AS area;

```


```
┌─area─┐
│ 43.9 │
└──────┘

```

## h3HexAreaKm2[​](#h3hexareakm2 "Direct link to h3HexAreaKm2")


Returns average hexagon area in square kilometers at the given resolution.


**Syntax**



```
h3HexAreaKm2(resolution)

```

**Parameter**


- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Area in square kilometers. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3HexAreaKm2(13) AS area;

```


```
┌──────area─┐
│ 0.0000439 │
└───────────┘

```

## h3IndexesAreNeighbors[​](#h3indexesareneighbors "Direct link to h3IndexesAreNeighbors")


Returns whether or not the provided [H3](#h3-index) indexes are neighbors.


**Syntax**



```
h3IndexesAreNeighbors(index1, index2)

```

**Arguments**


- `index1` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).
- `index2` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- `1` — Indexes are neighbours. [UInt8](/docs/sql-reference/data-types/int-uint).
- `0` — Indexes are not neighbours. [UInt8](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3IndexesAreNeighbors(617420388351344639, 617420388352655359) AS n;

```


```
┌─n─┐
│ 1 │
└───┘

```

## h3ToChildren[​](#h3tochildren "Direct link to h3ToChildren")


Returns an array of child indexes for the given [H3](#h3-index) index.


**Syntax**



```
h3ToChildren(index, resolution)

```

**Arguments**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).
- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned values**


- Array of the child H3\-indexes. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
SELECT h3ToChildren(599405990164561919, 6) AS children;

```


```
┌─children───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [603909588852408319,603909588986626047,603909589120843775,603909589255061503,603909589389279231,603909589523496959,603909589657714687] │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## h3ToParent[​](#h3toparent "Direct link to h3ToParent")


Returns the parent (coarser) index containing the given [H3](#h3-index) index.


**Syntax**



```
h3ToParent(index, resolution)

```

**Arguments**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).
- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Parent H3 index. [UInt64](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3ToParent(599405990164561919, 3) AS parent;

```


```
┌─────────────parent─┐
│ 590398848891879423 │
└────────────────────┘

```

## h3ToString[​](#h3tostring "Direct link to h3ToString")


Converts the `H3Index` representation of the index to the string representation.



```
h3ToString(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- String representation of the H3 index. [String](/docs/sql-reference/data-types/string).


**Example**



```
SELECT h3ToString(617420388352917503) AS h3_string;

```


```
┌─h3_string───────┐
│ 89184926cdbffff │
└─────────────────┘

```

## stringToH3[​](#stringtoh3 "Direct link to stringToH3")


Converts the string representation to the `H3Index` (UInt64\) representation.


**Syntax**



```
stringToH3(index_str)

```

**Parameter**


- `index_str` — String representation of the H3 index. [String](/docs/sql-reference/data-types/string).


**Returned value**


- Hexagon index number. Returns 0 on error. [UInt64](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT stringToH3('89184926cc3ffff') AS index;

```


```
┌──────────────index─┐
│ 617420388351344639 │
└────────────────────┘

```

## h3GetResolution[​](#h3getresolution-1 "Direct link to h3GetResolution")


Returns the resolution of the [H3](#h3-index) index.


**Syntax**



```
h3GetResolution(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3GetResolution(617420388352917503) AS res;

```


```
┌─res─┐
│   9 │
└─────┘

```

## h3IsResClassIII[​](#h3isresclassiii "Direct link to h3IsResClassIII")


Returns whether [H3](#h3-index) index has a resolution with Class III orientation.


**Syntax**



```
h3IsResClassIII(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- `1` — Index has a resolution with Class III orientation. [UInt8](/docs/sql-reference/data-types/int-uint).
- `0` — Index doesn't have a resolution with Class III orientation. [UInt8](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3IsResClassIII(617420388352917503) AS res;

```


```
┌─res─┐
│   1 │
└─────┘

```

## h3IsPentagon[​](#h3ispentagon "Direct link to h3IsPentagon")


Returns whether this [H3](#h3-index) index represents a pentagonal cell.


**Syntax**



```
h3IsPentagon(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- `1` — Index represents a pentagonal cell. [UInt8](/docs/sql-reference/data-types/int-uint).
- `0` — Index doesn't represent a pentagonal cell. [UInt8](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3IsPentagon(644721767722457330) AS pentagon;

```


```
┌─pentagon─┐
│        0 │
└──────────┘

```

## h3GetFaces[​](#h3getfaces "Direct link to h3GetFaces")


Returns icosahedron faces intersected by a given [H3](#h3-index) index.


**Syntax**



```
h3GetFaces(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned values**


- Array containing icosahedron faces intersected by a given H3 index. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
SELECT h3GetFaces(599686042433355775) AS faces;

```


```
┌─faces─┐
│ [7]   │
└───────┘

```

## h3CellAreaM2[​](#h3cellaream2 "Direct link to h3CellAreaM2")


Returns the exact area of a specific cell in square meters corresponding to the given input H3 index.


**Syntax**



```
h3CellAreaM2(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Cell area in square meters. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3CellAreaM2(579205133326352383) AS area;

```


```
┌───────────────area─┐
│ 4106166334463.9233 │
└────────────────────┘

```

## h3CellAreaRads2[​](#h3cellarearads2 "Direct link to h3CellAreaRads2")


Returns the exact area of a specific cell in square radians corresponding to the given input H3 index.


**Syntax**



```
h3CellAreaRads2(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Cell area in square radians. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3CellAreaRads2(579205133326352383) AS area;

```


```
┌────────────────area─┐
│ 0.10116268528089567 │
└─────────────────────┘

```

## h3ToCenterChild[​](#h3tocenterchild "Direct link to h3ToCenterChild")


Returns the center child (finer) [H3](#h3-index) index contained by given [H3](#h3-index) at the given resolution.


**Syntax**



```
h3ToCenterChild(index, resolution)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).
- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned values**


- [H3](#h3-index) index of the center child contained by given [H3](#h3-index) at the given resolution. [UInt64](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3ToCenterChild(577023702256844799,1) AS centerToChild;

```


```
┌──────centerToChild─┐
│ 581496515558637567 │
└────────────────────┘

```

## h3ExactEdgeLengthM[​](#h3exactedgelengthm "Direct link to h3ExactEdgeLengthM")


Returns the exact edge length of the unidirectional edge represented by the input h3 index in meters.


**Syntax**



```
h3ExactEdgeLengthM(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Exact edge length in meters. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3ExactEdgeLengthM(1310277011704381439) AS exactEdgeLengthM;;

```


```
┌───exactEdgeLengthM─┐
│ 195449.63163407316 │
└────────────────────┘

```

## h3ExactEdgeLengthKm[​](#h3exactedgelengthkm "Direct link to h3ExactEdgeLengthKm")


Returns the exact edge length of the unidirectional edge represented by the input h3 index in kilometers.


**Syntax**



```
h3ExactEdgeLengthKm(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Exact edge length in kilometers. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3ExactEdgeLengthKm(1310277011704381439) AS exactEdgeLengthKm;;

```


```
┌──exactEdgeLengthKm─┐
│ 195.44963163407317 │
└────────────────────┘

```

## h3ExactEdgeLengthRads[​](#h3exactedgelengthrads "Direct link to h3ExactEdgeLengthRads")


Returns the exact edge length of the unidirectional edge represented by the input h3 index in radians.


**Syntax**



```
h3ExactEdgeLengthRads(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Exact edge length in radians. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3ExactEdgeLengthRads(1310277011704381439) AS exactEdgeLengthRads;;

```


```
┌──exactEdgeLengthRads─┐
│ 0.030677980118976447 │
└──────────────────────┘

```

## h3NumHexagons[​](#h3numhexagons "Direct link to h3NumHexagons")


Returns the number of unique H3 indices at the given resolution.


**Syntax**



```
h3NumHexagons(resolution)

```

**Parameter**


- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Number of H3 indices. [Int64](/docs/sql-reference/data-types/int-uint).


**Example**



```
SELECT h3NumHexagons(3) AS numHexagons;

```


```
┌─numHexagons─┐
│       41162 │
└─────────────┘

```

## h3PointDistM[​](#h3pointdistm "Direct link to h3PointDistM")


Returns the "great circle" or "haversine" distance between pairs of GeoCoord points (latitude/longitude) pairs in meters.


**Syntax**



```
h3PointDistM(lat1, lon1, lat2, lon2)

```

**Arguments**


- `lat1`, `lon1` — Latitude and Longitude of point1 in degrees. [Float64](/docs/sql-reference/data-types/float).
- `lat2`, `lon2` — Latitude and Longitude of point2 in degrees. [Float64](/docs/sql-reference/data-types/float).


**Returned values**


- Haversine or great circle distance in meters.[Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3PointDistM(-10.0 ,0.0, 10.0, 0.0) AS h3PointDistM;

```


```
┌──────h3PointDistM─┐
│ 2223901.039504589 │
└───────────────────┘

```

## h3PointDistKm[​](#h3pointdistkm "Direct link to h3PointDistKm")


Returns the "great circle" or "haversine" distance between pairs of GeoCoord points (latitude/longitude) pairs in kilometers.


**Syntax**



```
h3PointDistKm(lat1, lon1, lat2, lon2)

```

**Arguments**


- `lat1`, `lon1` — Latitude and Longitude of point1 in degrees. [Float64](/docs/sql-reference/data-types/float).
- `lat2`, `lon2` — Latitude and Longitude of point2 in degrees. [Float64](/docs/sql-reference/data-types/float).


**Returned values**


- Haversine or great circle distance in kilometers. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3PointDistKm(-10.0 ,0.0, 10.0, 0.0) AS h3PointDistKm;

```


```
┌─────h3PointDistKm─┐
│ 2223.901039504589 │
└───────────────────┘

```

## h3PointDistRads[​](#h3pointdistrads "Direct link to h3PointDistRads")


Returns the "great circle" or "haversine" distance between pairs of GeoCoord points (latitude/longitude) pairs in radians.


**Syntax**



```
h3PointDistRads(lat1, lon1, lat2, lon2)

```

**Arguments**


- `lat1`, `lon1` — Latitude and Longitude of point1 in degrees. [Float64](/docs/sql-reference/data-types/float).
- `lat2`, `lon2` — Latitude and Longitude of point2 in degrees. [Float64](/docs/sql-reference/data-types/float).


**Returned values**


- Haversine or great circle distance in radians. [Float64](/docs/sql-reference/data-types/float).


**Example**



```
SELECT h3PointDistRads(-10.0 ,0.0, 10.0, 0.0) AS h3PointDistRads;

```


```
┌────h3PointDistRads─┐
│ 0.3490658503988659 │
└────────────────────┘

```

## h3GetRes0Indexes[​](#h3getres0indexes "Direct link to h3GetRes0Indexes")


Returns an array of all the resolution 0 H3 indexes.


**Syntax**



```
h3GetRes0Indexes()

```

**Returned values**


- Array of all the resolution 0 H3 indexes. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
SELECT h3GetRes0Indexes AS indexes ;

```


```
┌─indexes─────────────────────────────────────┐
│ [576495936675512319,576531121047601151,....]│
└─────────────────────────────────────────────┘

```

## h3GetPentagonIndexes[​](#h3getpentagonindexes "Direct link to h3GetPentagonIndexes")


Returns all the pentagon H3 indexes at the specified resolution.


**Syntax**



```
h3GetPentagonIndexes(resolution)

```

**Parameter**


- `resolution` — Index resolution. Range: `[0, 15]`. [UInt8](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Array of all pentagon H3 indexes. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
SELECT h3GetPentagonIndexes(3) AS indexes;

```


```
┌─indexes────────────────────────────────────────────────────────┐
│ [590112357393367039,590464201114255359,590816044835143679,...] │
└────────────────────────────────────────────────────────────────┘

```

## h3Line[​](#h3line "Direct link to h3Line")


Returns the line of indices between the two indices that are provided.


**Syntax**



```
h3Line(start,end)

```

**Parameter**


- `start` — Hexagon index number that represents a starting point. [UInt64](/docs/sql-reference/data-types/int-uint).
- `end` — Hexagon index number that represents an ending point. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


Array of h3 indexes representing the line of indices between the two provided indices. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
 SELECT h3Line(590080540275638271,590103561300344831) AS indexes;

```


```
┌─indexes────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [590080540275638271,590080471556161535,590080883873021951,590106516237844479,590104385934065663,590103630019821567,590103561300344831] │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## h3Distance[​](#h3distance "Direct link to h3Distance")


Returns the distance in grid cells between the two indices that are provided.


**Syntax**



```
h3Distance(start,end)

```

**Parameter**


- `start` — Hexagon index number that represents a starting point. [UInt64](/docs/sql-reference/data-types/int-uint).
- `end` — Hexagon index number that represents an ending point. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Number of grid cells. [Int64](/docs/sql-reference/data-types/int-uint).


Returns a negative number if finding the distance fails.


**Example**



```
 SELECT h3Distance(590080540275638271,590103561300344831) AS distance;

```


```
┌─distance─┐
│        7 │
└──────────┘

```

## h3HexRing[​](#h3hexring "Direct link to h3HexRing")


Returns the indexes of the hexagonal ring centered at the provided origin h3Index and length k.


Returns 0 if no pentagonal distortion was encountered.


**Syntax**



```
h3HexRing(index, k)

```

**Parameter**


- `index` — Hexagon index number that represents the origin. [UInt64](/docs/sql-reference/data-types/int-uint).
- `k` — Distance. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned values**


- Array of H3 indexes. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
 SELECT h3HexRing(590080540275638271, toUInt16(1)) AS hexRing;

```


```
┌─hexRing─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [590080815153545215,590080471556161535,590080677714591743,590077585338138623,590077447899185151,590079509483487231] │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## h3GetUnidirectionalEdge[​](#h3getunidirectionaledge "Direct link to h3GetUnidirectionalEdge")


Returns a unidirectional edge H3 index based on the provided origin and destination and returns 0 on error.


**Syntax**



```
h3GetUnidirectionalEdge(originIndex, destinationIndex)

```

**Parameter**


- `originIndex` — Origin Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).
- `destinationIndex` — Destination Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Unidirectional Edge Hexagon Index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Example**



```
 SELECT h3GetUnidirectionalEdge(599686042433355775, 599686043507097599) AS edge;

```


```
┌────────────────edge─┐
│ 1248204388774707199 │
└─────────────────────┘

```

## h3UnidirectionalEdgeIsValid[​](#h3unidirectionaledgeisvalid "Direct link to h3UnidirectionalEdgeIsValid")


Determines if the provided H3Index is a valid unidirectional edge index. Returns 1 if it's a unidirectional edge and 0 otherwise.


**Syntax**



```
h3UnidirectionalEdgeisValid(index)

```

**Parameter**


- `index` — Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- 1 — The H3 index is a valid unidirectional edge. [UInt8](/docs/sql-reference/data-types/int-uint).
- 0 — The H3 index is not a valid unidirectional edge. [UInt8](/docs/sql-reference/data-types/int-uint).


**Example**



```
 SELECT h3UnidirectionalEdgeIsValid(1248204388774707199) AS validOrNot;

```


```
┌─validOrNot─┐
│          1 │
└────────────┘

```

## h3GetOriginIndexFromUnidirectionalEdge[​](#h3getoriginindexfromunidirectionaledge "Direct link to h3GetOriginIndexFromUnidirectionalEdge")


Returns the origin hexagon index from the unidirectional edge H3Index.


**Syntax**



```
h3GetOriginIndexFromUnidirectionalEdge(edge)

```

**Parameter**


- `edge` — Hexagon index number that represents a unidirectional edge. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Origin Hexagon Index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Example**



```
 SELECT h3GetOriginIndexFromUnidirectionalEdge(1248204388774707197) AS origin;

```


```
┌─────────────origin─┐
│ 599686042433355773 │
└────────────────────┘

```

## h3GetDestinationIndexFromUnidirectionalEdge[​](#h3getdestinationindexfromunidirectionaledge "Direct link to h3GetDestinationIndexFromUnidirectionalEdge")


Returns the destination hexagon index from the unidirectional edge H3Index.


**Syntax**



```
h3GetDestinationIndexFromUnidirectionalEdge(edge)

```

**Parameter**


- `edge` — Hexagon index number that represents a unidirectional edge. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Destination Hexagon Index number. [UInt64](/docs/sql-reference/data-types/int-uint).


**Example**



```
 SELECT h3GetDestinationIndexFromUnidirectionalEdge(1248204388774707197) AS destination;

```


```
┌────────destination─┐
│ 599686043507097597 │
└────────────────────┘

```

## h3GetIndexesFromUnidirectionalEdge[​](#h3getindexesfromunidirectionaledge "Direct link to h3GetIndexesFromUnidirectionalEdge")


Returns the origin and destination hexagon indexes from the given unidirectional edge H3Index.


**Syntax**



```
h3GetIndexesFromUnidirectionalEdge(edge)

```

**Parameter**


- `edge` — Hexagon index number that represents a unidirectional edge. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


A tuple consisting of two values `tuple(origin,destination)`:


- `origin` — Origin Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).
- `destination` — Destination Hexagon index number. [UInt64](/docs/sql-reference/data-types/int-uint).


Returns `(0,0)` if the provided input is not valid.


**Example**



```
 SELECT h3GetIndexesFromUnidirectionalEdge(1248204388774707199) AS indexes;

```


```
┌─indexes─────────────────────────────────┐
│ (599686042433355775,599686043507097599) │
└─────────────────────────────────────────┘

```

## h3GetUnidirectionalEdgesFromHexagon[​](#h3getunidirectionaledgesfromhexagon "Direct link to h3GetUnidirectionalEdgesFromHexagon")


Provides all of the unidirectional edges from the provided H3Index.


**Syntax**



```
h3GetUnidirectionalEdgesFromHexagon(index)

```

**Parameter**


- `index` — Hexagon index number that represents a unidirectional edge. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


Array of h3 indexes representing each unidirectional edge. [Array](/docs/sql-reference/data-types/array)([UInt64](/docs/sql-reference/data-types/int-uint)).


**Example**



```
 SELECT h3GetUnidirectionalEdgesFromHexagon(1248204388774707199) AS edges;

```


```
┌─edges─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [1248204388774707199,1320261982812635135,1392319576850563071,1464377170888491007,1536434764926418943,1608492358964346879] │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## h3GetUnidirectionalEdgeBoundary[​](#h3getunidirectionaledgeboundary "Direct link to h3GetUnidirectionalEdgeBoundary")


Returns the coordinates defining the unidirectional edge.


**Syntax**



```
h3GetUnidirectionalEdgeBoundary(index)

```

**Parameter**


- `index` — Hexagon index number that represents a unidirectional edge. [UInt64](/docs/sql-reference/data-types/int-uint).


**Returned value**


- Array of pairs '(lon, lat)'. [Array](/docs/sql-reference/data-types/array)([Float64](/docs/sql-reference/data-types/float), [Float64](/docs/sql-reference/data-types/float)).


**Example**



```
 SELECT h3GetUnidirectionalEdgeBoundary(1248204388774707199) AS boundary;

```


```
┌─boundary────────────────────────────────────────────────────────────────────────┐
│ [(37.42012867767779,-122.03773496427027),(37.33755608435299,-122.090428929044)] │
└─────────────────────────────────────────────────────────────────────────────────┘

```
[PreviousGeometry](/docs/sql-reference/functions/geo/geometry)[NextPolygons](/docs/sql-reference/functions/geo/polygons)- [H3 Index](#h3-index)- [h3IsValid](#h3isvalid)- [h3GetResolution](#h3getresolution)- [h3EdgeAngle](#h3edgeangle)- [h3EdgeLengthM](#h3edgelengthm)- [h3EdgeLengthKm](#h3edgelengthkm)- [geoToH3](#geotoh3)- [h3ToGeo](#h3togeo)- [h3ToGeoBoundary](#h3togeoboundary)- [h3kRing](#h3kring)- [h3PolygonToCells](#h3polygontocells)- [h3GetBaseCell](#h3getbasecell)- [h3HexAreaM2](#h3hexaream2)- [h3HexAreaKm2](#h3hexareakm2)- [h3IndexesAreNeighbors](#h3indexesareneighbors)- [h3ToChildren](#h3tochildren)- [h3ToParent](#h3toparent)- [h3ToString](#h3tostring)- [stringToH3](#stringtoh3)- [h3GetResolution](#h3getresolution-1)- [h3IsResClassIII](#h3isresclassiii)- [h3IsPentagon](#h3ispentagon)- [h3GetFaces](#h3getfaces)- [h3CellAreaM2](#h3cellaream2)- [h3CellAreaRads2](#h3cellarearads2)- [h3ToCenterChild](#h3tocenterchild)- [h3ExactEdgeLengthM](#h3exactedgelengthm)- [h3ExactEdgeLengthKm](#h3exactedgelengthkm)- [h3ExactEdgeLengthRads](#h3exactedgelengthrads)- [h3NumHexagons](#h3numhexagons)- [h3PointDistM](#h3pointdistm)- [h3PointDistKm](#h3pointdistkm)- [h3PointDistRads](#h3pointdistrads)- [h3GetRes0Indexes](#h3getres0indexes)- [h3GetPentagonIndexes](#h3getpentagonindexes)- [h3Line](#h3line)- [h3Distance](#h3distance)- [h3HexRing](#h3hexring)- [h3GetUnidirectionalEdge](#h3getunidirectionaledge)- [h3UnidirectionalEdgeIsValid](#h3unidirectionaledgeisvalid)- [h3GetOriginIndexFromUnidirectionalEdge](#h3getoriginindexfromunidirectionaledge)- [h3GetDestinationIndexFromUnidirectionalEdge](#h3getdestinationindexfromunidirectionaledge)- [h3GetIndexesFromUnidirectionalEdge](#h3getindexesfromunidirectionaledge)- [h3GetUnidirectionalEdgesFromHexagon](#h3getunidirectionaledgesfromhexagon)- [h3GetUnidirectionalEdgeBoundary](#h3getunidirectionaledgeboundary)
Was this page helpful?
