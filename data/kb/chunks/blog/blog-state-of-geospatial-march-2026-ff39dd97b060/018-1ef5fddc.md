---
source: blog
url: https://h3geo.org/
topic: state-of-geospatial-in-clickhouse-in-march-2026
ch_version_introduced: '20.1'
last_updated: '2026-06-12'
chunk_index: 18
total_chunks_in_doc: 22
---

cell boundary as a `Ring` in **(latitude, longitude)** order, so we swap coordinates with `arrayMap` before wrapping as a `Polygon` for `svg()`. We also need to flip the y\-axis since SVG's y increases downward while latitude increases upward.

In the query below, we build a heatmap of the taxi trips with each H3 cell colored by `log(trip count)`, and written to SVG format:

```
WITH cells AS (
    SELECT
        assumeNotNull(geoToH3(pickup_latitude, pickup_longitude, 9)) AS cell,
        count() AS trips
    FROM trips_small
    WHERE pickup_latitude BETWEEN 40.4 AND 40.95
      AND pickup_longitude BETWEEN -74.3 AND -73.7
    GROUP BY cell
    HAVING trips >= 10
),
max_trips AS (SELECT max(log(trips)) AS max_log FROM cells)
SELECT concat(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-74.05 40.58 0.32 0.35" width="650" height="1000" preserveAspectRatio="none">',
    '<rect x="-74.05" y="40.58" width="0.32" height="0.35" fill="#0a1628"/>',
    '<g transform="scale(1,-1) translate(0,-81.51)">',
    arrayStringConcat(groupArray(
        replaceAll(
            svg([arrayMap(p -> (p.2, p.1), h3ToGeoBoundary(cell))]::Polygon),
            'style=""',
            concat('style="fill:rgba(56,139,230,', toString(round(log(trips) / max_log, 3)), ');stroke:none"')
        )
    ), ''),
    '</g></svg>'
)
FROM cells, max_trips
FORMAT TSVRaw;

```

The `FORMAT TSVRaw` at the end outputs the raw string value with no table borders \- without it, ClickHouse wraps the output in `┌─┐` characters that would break the SVG file.

Since the query contains single\-quoted strings, save it to a file (e.g. `h3_heatmap.sql`) and run it with `--queries-file`. Pipe the output to an SVG file and open it in a browser:

```

```
1clickhouse --queries-file h3_heatmap.sql > h3_heatmap.svg
```

```

![NYC taxi pickup density as an H3 hexagonal heatmap](/uploads/h3_nyc_15bdb90bcb.svg)
Manhattan is the bright diagonal strip running northeast to southwest \- its grid is tilted \~29° from true north. Brooklyn spreads to the lower right, Queens to the right, and the two isolated bright clusters are LaGuardia (upper) and JFK (lower) airports.

We can now find the top pickup hotspots by grouping on the H3 cell:

```

```
1SELECT pickup_h3, count() AS trips
2FROM trips_small_h3
3WHERE pickup_h3 != 0
4GROUP BY pickup_h3
5ORDER BY trips DESC
6LIMIT 10;
```

```

```
┌──────────pickup_h3─┬──trips─┐
│ 617733123811311615 │ 168301 │
│ 619056821840379903 │ 136783 │
│ 617733123811835903 │ 122822 │
│ 617733124072407039 │  96570 │
│ 617733150971789311 │  92725 │
│ 617733123872391167 │  92066 │
│ 617733124388552703 │  90773 │
│ 617733123870818303 │  88238 │
│ 617733150972837887 │  83712 │
│ 617733123869507583 │  83588 │
└────────────────────┴────────┘

10 rows in set. Elapsed: 0.033 sec.

```
