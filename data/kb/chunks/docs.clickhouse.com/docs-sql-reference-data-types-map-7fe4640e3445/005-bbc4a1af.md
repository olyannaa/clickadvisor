---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/map.md)#
topic: map-k-v-clickhouse-docs
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 8
---

`with_buckets` compared to `basic` serialization at various map sizes (10 to 10,000 keys per row). The bucket count was determined by the `sqrt` strategy capped at 32\. The exact numbers depend on key/value types, data distribution, and hardware.

| Operation 10 keys 100 keys 1,000 keys 10,000 keys Notes| **Single key lookup** (`m['key']`) 1\.6–3\.2x faster 4\.5–7\.7x faster 16–39x faster 21–49x faster Reads only one bucket instead of the entire column.| **5 key lookups** \~1x 1\.5–3\.1x faster 2\.9–8\.3x faster 4\.5–6\.7x faster Each key reads its own bucket; some buckets may overlap.| **PREWHERE** (`SELECT m WHERE m['key'] = ...`) 1\.5–3\.0x faster 2\.9–7\.3x faster 5\.3–31x faster 20–45x faster PREWHERE filter reads only one bucket; full map read only for matching rows. Speedup depends on selectivity — fewer matching granules means less full\-map I/O.| **Full map scan** (`SELECT m`) \~2x slower \~2x slower \~2x slower \~2x slower Must read and reassemble all buckets.| **INSERT** 1\.5–2\.5x slower 1\.5–2\.5x slower 1\.5–2\.5x slower 1\.5–2\.5x slower Overhead of hashing keys and writing to multiple substreams. | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


### Recommendations[​](#recommendations "Direct link to Recommendations")
