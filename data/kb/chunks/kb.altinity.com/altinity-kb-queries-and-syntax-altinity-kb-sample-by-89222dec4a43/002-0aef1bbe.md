---
source: kb.altinity.com
url: https://github.com/ClickHouse/ClickHouse/blob/92c937db8b50844c7216d93c5c398d376e82f6c3/src/Storages/MergeTree/MergeTreeDataSelectExecutor.cpp#L355
topic: sample-by-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 2
---

sample keys; SET max\_parallel\_replicas \= 3 - Select from multiple replicas of each shard in parallel; ## SAMPLE emulation via WHERE condition Sometimes, it’s easier to emulate sampling via conditions in WHERE clause instead of using SAMPLE key.

```
SELECT count() FROM table WHERE ... AND cityHash64(some_high_card_key) % 10 = 0; -- Deterministic
SELECT count() FROM table WHERE ... AND rand() % 10 = 0; -- Non-deterministic

```
ClickHouse will read more data from disk compared to an example with a good SAMPLE key, but it’s more universal and can be used if you can’t change table ORDER BY key. (To learn more about ClickHouse internals, [Administrator Training for ClickHouse](https://altinity.com/clickhouse-training/)
is available.)

Last modified 2024\.07\.29: [Site cleanup, mostly minor changes (3e41a19\)](https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df)
