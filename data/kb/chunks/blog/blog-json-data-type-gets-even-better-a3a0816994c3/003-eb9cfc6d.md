---
source: blog
url: https://clickhouse.com/docs/sql-reference/data-types/newjson
topic: making-complex-json-58x-faster-use-3-300x-less-memory-in-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 6
---

objects. Extracting a nested path from such structures using the above approach still requires reading the entire array, which is inefficient for large payloads. To address this, **the advanced format was extended with additional files for subcolumn handling**.

Here each bucket has 6 files:

- **`.structure`** – metadata for each granule: number of rows, list of paths in the granule and offsets in files  `.paths_marks` and  `.substreams_metadata`.
- **`.data`** – the actual path data stored in columnar format per granule, but split into substreams. A single path may have multiple substreams. This structure allows ClickHouse to read only the substreams needed to reconstruct the requested subcolumn, rather than scanning the entire path value.
- **`.paths_marks`** – offsets pointing to the start of each path’s data in the  `.data` file.
- **`.substreams_marks`** – offsets pointing to the start of each path’s substream in the `.data` file.
- **`.substreams`** – list of substreams present for each path in a granule. This may differ across granules (e.g., some arrays may contain objects with different nested fields).
- **`.substreams_metadata`** – for each path, stores offsets in the  `.substreams` and  `.substreams_marks` files, effectively linking a path to its subcolumns and their data locations.

![json_type_update_image8.png](/uploads/json_type_update_image8_min_bad57854bf.png)
When querying the subcolumn of path `key_m1`, ClickHouse first reads data from the `.structure` file and checks if this granule contains the requested path `key_m1`. If not, the granule is skipped entirely. If it does, ClickHouse uses the offset stored in the  `.structure` file to read the corresponding entry in `.substreams_metadata` and obtain the offsets for `key_m1`.

Using the first offset, ClickHouse then reads the list of substreams for this path in the granule. If this list does not include the substreams required for the requested subcolumn, the granule is skipped. If the required substreams are present, ClickHouse uses the second offset to read their positions from `.substreams_marks` and then reads only the data of those substreams from the `.data` file.

After reconstructing the requested subcolumn, ClickHouse proceeds to the next granule.

![json_type_update_image9.png](/uploads/json_type_update_image9_min_11de95296c.png)
This avoids reading the data of unrelated paths and unrelated substreams of the requested path in the granule in memory. This **significantly improves the performance of nested subcolumn reading**.

## Balancing efficiency and compatibility [\#](/blog/json-data-type-gets-even-better#balancing-efficiency-and-compatibility)
