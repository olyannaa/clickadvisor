# Functions for Working with Geohash \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- [Geometry](/docs/sql-reference/functions/geo)- Geohash
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/geo/geohash.md)# Functions for Working with Geohash

## Geohash[​](#geohash "Direct link to Geohash")


[Geohash](https://en.wikipedia.org/wiki/Geohash) is the geocode system, which subdivides Earth's surface into buckets of grid shape and encodes each cell into a short string of letters and digits. It is a hierarchical data structure, so the longer the geohash string is, the more precise the geographic location will be.


If you need to manually convert geographic coordinates to geohash strings, you can use [geohash.org](http://geohash.co/)


## geohashEncode[​](#geohashencode "Direct link to geohashEncode")


Encodes latitude and longitude as a [geohash](#geohash)\-string.


**Syntax**



```
geohashEncode(longitude, latitude, [precision])

```

**Input values**


- `longitude` — Longitude part of the coordinate you want to encode. Floating in range`[-180°, 180°]`. [Float](/docs/sql-reference/data-types/float).
- `latitude` — Latitude part of the coordinate you want to encode. Floating in range `[-90°, 90°]`. [Float](/docs/sql-reference/data-types/float).
- `precision` (optional) — Length of the resulting encoded string. Defaults to `12`. Integer in the range `[1, 12]`. [Int8](/docs/sql-reference/data-types/int-uint).


Note- All coordinate parameters must be of the same type: either `Float32` or `Float64`.
- For the `precision` parameter, any value less than `1` or greater than `12` is silently converted to `12`.

**Returned values**


- Alphanumeric string of the encoded coordinate (modified version of the base32\-encoding alphabet is used). [String](/docs/sql-reference/data-types/string).


**Example**



```
SELECT geohashEncode(-5.60302734375, 42.593994140625, 0) AS res;

```


```
┌─res──────────┐
│ ezs42d000000 │
└──────────────┘

```

## geohashDecode[​](#geohashdecode "Direct link to geohashDecode")


Decodes any [geohash](#geohash)\-encoded string into longitude and latitude.


**Syntax**



```
geohashDecode(hash_str)

```

**Input values**


- `hash_str` — Geohash\-encoded string.


**Returned values**


- Tuple `(longitude, latitude)` of `Float64` values of longitude and latitude. [Tuple](/docs/sql-reference/data-types/tuple)([Float64](/docs/sql-reference/data-types/float))


**Example**



```
SELECT geohashDecode('ezs42') AS res;

```


```
┌─res─────────────────────────────┐
│ (-5.60302734375,42.60498046875) │
└─────────────────────────────────┘

```

## geohashesInBox[​](#geohashesinbox "Direct link to geohashesInBox")


Returns an array of [geohash](#geohash)\-encoded strings of given precision that fall inside and intersect boundaries of given box, basically a 2D grid flattened into array.


**Syntax**



```
geohashesInBox(longitude_min, latitude_min, longitude_max, latitude_max, precision)

```

**Arguments**


- `longitude_min` — Minimum longitude. Range: `[-180°, 180°]`. [Float](/docs/sql-reference/data-types/float).
- `latitude_min` — Minimum latitude. Range: `[-90°, 90°]`. [Float](/docs/sql-reference/data-types/float).
- `longitude_max` — Maximum longitude. Range: `[-180°, 180°]`. [Float](/docs/sql-reference/data-types/float).
- `latitude_max` — Maximum latitude. Range: `[-90°, 90°]`. [Float](/docs/sql-reference/data-types/float).
- `precision` — Geohash precision. Range: `[1, 12]`. [UInt8](/docs/sql-reference/data-types/int-uint).


NoteAll coordinate parameters must be of the same type: either `Float32` or `Float64`.


**Returned values**


- Array of precision\-long strings of geohash\-boxes covering provided area, you should not rely on order of items. [Array](/docs/sql-reference/data-types/array)([String](/docs/sql-reference/data-types/string)).
- `[]` \- Empty array if minimum latitude and longitude values aren't less than corresponding maximum values.


NoteFunction throws an exception if resulting array is over 10'000'000 items long.


**Example**



```
SELECT geohashesInBox(24.48, 40.56, 24.785, 40.81, 4) AS thasos;

```


```
┌─thasos──────────────────────────────────────┐
│ ['sx1q','sx1r','sx32','sx1w','sx1x','sx38'] │
└─────────────────────────────────────────────┘

```
[PreviousGeographical Coordinates](/docs/sql-reference/functions/geo/coordinates)[NextGeometry](/docs/sql-reference/functions/geo/geometry)- [Geohash](#geohash)- [geohashEncode](#geohashencode)- [geohashDecode](#geohashdecode)- [geohashesInBox](#geohashesinbox)
Was this page helpful?
