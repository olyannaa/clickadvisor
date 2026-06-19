# Polygon dictionaries \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- LAYOUT- Polygon
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/layouts/polygon.md)# Polygon dictionaries

The `polygon` (`POLYGON`) dictionary is optimized for point\-in\-polygon queries, essentially "reverse geocoding" lookups.
Given a coordinate (latitude/longitude), it efficiently finds which polygon/region (from a set of many polygons, such as country or region boundaries) contains that point.
It's well\-suited for mapping location coordinates to their containing region.



Example of configuring a polygon dictionary:


TipIf you are using a dictionary with ClickHouse Cloud please use the DDL query option to create your dictionaries, and create your dictionary as user `default`.
Also, verify the list of supported dictionary sources in the [Cloud Compatibility guide](/docs/whats-new/cloud-compatibility).


- DDL- Configuration file


```
CREATE DICTIONARY polygon_dict_name (
    key Array(Array(Array(Array(Float64)))),
    name String,
    value UInt64
)
PRIMARY KEY key
LAYOUT(POLYGON(STORE_POLYGON_KEY_COLUMN 1))
...

```

```
<dictionary>
    <structure>
        <key>
            <attribute>
                <name>key</name>
                <type>Array(Array(Array(Array(Float64))))</type>
            </attribute>
        </key>

        <attribute>
            <name>name</name>
            <type>String</type>
            <null_value></null_value>
        </attribute>

        <attribute>
            <name>value</name>
            <type>UInt64</type>
            <null_value>0</null_value>
        </attribute>
    </structure>

    <layout>
        <polygon>
            <store_polygon_key_column>1</store_polygon_key_column>
        </polygon>
    </layout>

    ...
</dictionary>

```

  

When configuring the polygon dictionary, the key must have one of two types:


- A simple polygon. It is an array of points.
- MultiPolygon. It is an array of polygons. Each polygon is a two\-dimensional array of points. The first element of this array is the outer boundary of the polygon, and subsequent elements specify areas to be excluded from it.


Points can be specified as an array or a tuple of their coordinates. In the current implementation, only two\-dimensional points are supported.


The user can upload their own data in all formats supported by ClickHouse.


There are 3 types of [in\-memory storage](/docs/sql-reference/statements/create/dictionary/layouts/#storing-dictionaries-in-memory) available:




| Layout Description| `POLYGON_SIMPLE` Naive implementation. A linear pass through all polygons is made for each query, checking membership without additional indexes.| `POLYGON_INDEX_EACH` A separate index is built for each polygon, allowing fast membership checks in most cases (optimized for geographical regions). A grid is superimposed on the area, recursively dividing cells into 16 equal parts. Division stops when recursion depth reaches `MAX_DEPTH` or a cell crosses no more than `MIN_INTERSECTIONS` polygons.| `POLYGON_INDEX_CELL` Also creates the grid described above with the same options. For each leaf cell, an index is built on all polygon pieces that fall into it, allowing fast query responses.| `POLYGON` Synonym for `POLYGON_INDEX_CELL`. | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Dictionary queries are carried out using standard [functions](/docs/sql-reference/functions/ext-dict-functions) for working with dictionaries.
An important difference is that here the keys will be the points for which you want to find the polygon containing them.


**Example**


Example of working with the dictionary defined above:



```
CREATE TABLE points (
    x Float64,
    y Float64
)
...
SELECT tuple(x, y) AS key, dictGet(dict_name, 'name', key), dictGet(dict_name, 'value', key) FROM points ORDER BY x, y;

```

As a result of executing the last command for each point in the 'points' table, a minimum area polygon containing this point will be found, and the requested attributes will be output.


**Example**


You can read columns from polygon dictionaries via SELECT query, just turn on the `store_polygon_key_column = 1` in the dictionary configuration or corresponding DDL\-query.



```
CREATE TABLE polygons_test_table
(
    key Array(Array(Array(Tuple(Float64, Float64)))),
    name String
) ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO polygons_test_table VALUES ([[[(3, 1), (0, 1), (0, -1), (3, -1)]]], 'Value');

CREATE DICTIONARY polygons_test_dictionary
(
    key Array(Array(Array(Tuple(Float64, Float64)))),
    name String
)
PRIMARY KEY key
SOURCE(CLICKHOUSE(TABLE 'polygons_test_table'))
LAYOUT(POLYGON(STORE_POLYGON_KEY_COLUMN 1))
LIFETIME(0);

SELECT * FROM polygons_test_dictionary;

```


```
┌─key─────────────────────────────┬─name──┐
│ [[[(3,1),(0,1),(0,-1),(3,-1)]]] │ Value │
└─────────────────────────────────┴───────┘

```
[Previousip\_trie](/docs/sql-reference/statements/create/dictionary/layouts/ip-trie)[NextRegexp Tree](/docs/sql-reference/statements/create/dictionary/layouts/regexp-tree)Was this page helpful?
