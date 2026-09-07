---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-26-6-clickhouse
ch_version_introduced: '26.6'
last_updated: '2026-09-07'
chunk_index: 8
total_chunks_in_doc: 10
---

by Mikhail Artemenko \# We also have the introduction of streaming queries in experimental mode. You can now write a query that never ends by appending `STREAM`. The query will keep emitting new rows as they are inserted.

To enable this feature, you can use the following setting:

```
1SET enable_streaming_queries = 1;
```
Copy command
And then, we could write the following query that blocks and keep streaming new rows:

```
1SELECT id, msg 
2FROM live_events STREAM;
```
Copy command
As new rows are added to `live_events`, they would be returned by the above query.

This feature can also be used in a more advanced mode with cursors:

```
1SELECT _block_number AS bn, _block_offset AS bo, id, msg
2FROM events STREAM 
3CURSOR {'all': {'block_number': 2, 'block_offset': 0}};
```
Copy command
## PNG output format \#

### Contributed by Maksim Dergousov \#

26\.6 introduces the `PNG` output format, which makes it possible to render query results as an image. It's one row per pixel (r, g, b or v), with implicit or explicitly defined pixel coordinates (x, y). For example:

```
1WITH number DIV 1024 AS y, number MOD 1024 AS x,
2  L2Norm((x - 512, y - 512)) / 512 AS radius, 60 AS stripe_size,
3  round((atan2(x - 512, y - 512) / pi() * 180 + exp(radius) * 90)
4    / stripe_size) * stripe_size AS alpha,
5  radius <= 1 ? abs(1 - (radius - 0.5) * (radius - 0.5) * 4) : 0 AS a,
6  colorOKLCHToSRGB((0.7, 0.15, alpha)) AS rgb
7SELECT rgb.1::UInt8 AS r, rgb.2::UInt8 AS g, rgb.3::UInt8 AS b, a
8FROM numbers(1048576) FORMAT PNG
```
Copy command
![ClickHouse Query Result.png](/_next/image?url=%2Fuploads%2FClick_House_Query_Result_26f12077ea.png&w=2048&q=75)

Off the back of this functionality, Alexey has created [RayTracer](https://github.com/ClickHouse/RayTracer), a path tracer written entirely as ClickHouse SQL queries, rendering straight to PNG.

## Geospatial improvements \#

### Contributed by Mark Needham, Alexey Milovidov, Saarthak Gupta \#

As of ClickHouse 26\.6, you can read a GeoJSON feature collection and it will generate one row per feature:

```
1SELECT id, properties.name, toTypeName(geometry)
2FROM file('places.geojson', GeoJSON);
```
Copy command

| id | properties.name | geometry |
| --- | --- | --- |
| 1 | London | Geometry (Point) |
| 2 | square | Geometry (Polygon) |


Point, LineString, MultiLineString, Polygon, and MultiPolygon are all supported natively.
