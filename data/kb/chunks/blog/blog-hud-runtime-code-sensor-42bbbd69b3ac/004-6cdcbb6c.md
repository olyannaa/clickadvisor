---
source: blog
url: https://www.hud.io/
topic: how-hud-is-building-the-first-runtime-code-sensor-with-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 6
---

partial state while Node.js coordinated enrichment, matching telemetry with metadata once it arrived. It worked well enough to get the product to market, but it came with overhead. Before long, network round\-trips and memory pressure started to show.

“We had built a pretty complex architecture around other technologies,” Almog says. “As we added more customers and usage scaled, we realized we can count on ClickHouse for more pieces of the puzzle, and we redesigned enrichment to run inside ClickHouse. This eliminated coordination overhead and gave us a cleaner, faster pipeline.”

The breakthrough came when Hud pulled enrichment into ClickHouse itself. Using [Null engine tables](https://clickhouse.com/docs/engines/table-engines/special/null) and [dictionaries](https://clickhouse.com/docs/sql-reference/dictionaries), they made enrichment in\-memory and declarative. Then, with [ReplacingMergeTree tables](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree), they added a queue\-like buffer so telemetry could be ingested right away and joined with metadata once available, with outdated rows expiring automatically. The buffer was especially critical because telemetry often arrived before the corresponding metadata, and Hud needed a way to reconcile the two streams without losing data.

In the new ingestion pipeline, telemetry flows into raw tables, passes through enrichment logic, and is either committed directly or held briefly in a buffer until metadata arrives. Metadata is written into live and archival MergeTree tables with defined retention windows, giving Hud both speed and historical depth.

![User Story Hud Issue 1197.jpg](/uploads/User_Story_Hud_Issue_1197_3bc8fa0f3e.jpg)
“We had to employ some sophisticated techniques to make it work,” Ilan says. “It’s a pretty unique solution.”

Almog calls the rearchitecture “a really big step in the way of supporting scale.” By consolidating ingestion and enrichment inside ClickHouse, she says, the team “drastically improved the scale, stability, and latency of our system.”

## Impact across the board [\#](/blog/hud-runtime-code-sensor#impact-across-the-board)

Today, Hud ingests hundreds of megabytes per second of raw JSON, which compresses down to tens of MB/s once stored in ClickHouse. Their ClickHouse Cloud deployment holds more than 11 terabytes of telemetry data.

Even at this scale, engineers can query function\-level telemetry across deployments and detect degradations within minutes of a release. The ability to track changes against baselines, rather than relying on thresholds, makes detections more accurate and actionable.
