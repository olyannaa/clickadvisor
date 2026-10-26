---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-fountain-rebuilt-its-data-plane-on-clickhouse-cloud-to-power-cue-the-frontline-superintelligence-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-26'
chunk_index: 5
total_chunks_in_doc: 8
---

have to backfill the ClickPipe itself, because all the data we need already exists in that single doc field.” Nested arrays arrive as arrays of dynamic values that play nicely with ClickHouse’s [array functions](https://clickhouse.com/docs/sql-reference/functions/array-functions) (`arrayMap`, `arrayJoin`, `arrayFirst`, `arrayLast`).

Most importantly, ClickHouse stores the JSON as a columnar substructure internally rather than reparsing a string on every read. “This is a significant win at scale,” Cecily says. “It saves us a huge amount in both CPU and memory consumption.”

## Incremental materialized views \#

The “heart of the architecture” is how transformation happens. Every materialized view downstream of a CDC source fires the moment ClickPipes writes a batch to the raw table. “It’s like a cascade,” Cecily says. “You make changes in one, it cascades to the next.”

Fountain runs more than 100 models across each of its 15 deployments this way, coding them in dbt and building them directly into ClickHouse. Most land in a [ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) (or a plain [MergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree) for immutable records like transition logs) with the transformation kept deliberately shallow so queries stay fast. “There’s no Dagster, there’s no Airflow, there’s no cron,” Cecily says. “Set it and forget it. The refresh is a property of the storage engine.”

![](/_next/image?url=%2Fuploads%2Ffountain_sep2026_image4_b4ce2d6ae0.png&w=2048&q=75)

*Transformation without orchestration: ClickPipes writes a batch to the raw CDC table, the materialized view fires, and deduplicated rows land in a ReplacingMergeTree, with no scheduler*

That insert\-time model also unlocked the team’s “single biggest performance win.” To answer a common question (“How long did an applicant spend in a given stage?”) they needed each transition’s previous and next timestamps. Instead of running that window function across the whole table at query time, they moved the work into the materialized view, pairing ClickHouse’s [`lagInFrame` function](https://clickhouse.com/docs/sql-reference/window-functions/lagInFrame) with an [`ASOF JOIN`](https://clickhouse.com/docs/sql-reference/statements/select/join#asof-join-usage). `lagInFrame` handles records in the current batch, the `ASOF JOIN` reaches back to what’s already stored, and a [`coalesce`](https://clickhouse.com/docs/sql-reference/functions/functions-for-nulls#coalesce) takes the in\-batch value when it exists, falling back to the stored one otherwise.

Computing it once at insert time on the 838\-million\-row transition table dropped per\-query memory from 778 MiB to 153 MiB, an 80% reduction. Generalized across query shapes, the same pattern yields 60\-98% memory savings. “Move the expensive shape to your incremental materialized view,” Cecily says, summing up the lesson, “and let your query stay cheap.”

## Security and governance \#
