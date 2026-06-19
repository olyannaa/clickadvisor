---
source: blog
url: https://www.dash0.com/blog/opentelemetry-native-the-future-of-observability#what-does-an-open-telemetry-native-observability-tool-look-like
topic: building-an-observability-solution-with-clickhouse-at-dash0
ch_version_introduced: '0.100000'
last_updated: '2026-06-12'
chunk_index: 10
total_chunks_in_doc: 14
---

| xargs -0 printf '%s\n' | clickhouse-benchmark --cumulative --user otel --password otel --host localhost --port 9000 -i 10 2>&1 | tee --append "${OUTPUT_FILENAME}" sleep 5 done done done ``` By running these benchmarks, we observed several noteworthy things:

- Compression ratio of tables "traces2", "traces3" and "traces4" were all pretty similar but not as good as the original table
- The "traces5" table (with `ORDER BY (xxh3(SpanId) % 256, ResourceHash, Timestamp)` is by far the fastest for sampling, as it can efficiently skip lots of granules to scan. But compared to the original "traces" table, it also scores very badly for any normal queries without sampling
- The “traces4” table slightly outperformed the “traces2” and “traces3” setups, but not by much
- Depending on the exact query, sampling on query time\-frames below 12 \- 24 hours did not result in much time shaved off the query duration

With these results, we decided to go with a sorting key of `ResourceHash, toStartOfHour(Timestamp), xxh3(SpanId)`. We also found a secondary `minmax` index on `Timestamp`, made the biggest difference to the query performance. It's also why the regular table performs so well and simultaneously explains why "traces5" performed so poorly, i.e. timestamps were too divided.

### Other learnings [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#other-learnings)

Finally, we’ll quickly go over a few other learnings that might not seem obvious, but could make a substantial difference.

#### Usage of indices [\#](/blog/building-an-observability-solution-with-clickhouse-at-dash0#usage-of-indices)

Data skipping indexes can significantly reduce the number of granules ClickHouse needs to read, but their effectiveness depends on using compatible clauses and functions. More specifically, the different Bloom Filter types [support different functions](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree#functions-support). And while Bloom filters work well for positive matches, they cannot be used for optimizing negative matches.

When indexing `Map` contents, you can create indexes like:

```

```
INDEX idx_attr_key mapKeys(Attributes) TYPE bloom_filter(0.01) GRANULARITY 1
```

```

However, query syntax matters significantly \- especially when testing for key existence in the Map type:

- `has(Attributes, 'some_key')` will correctly utilize this Bloom Filter
- `Attributes['some_key'] = ''` (empty string) will not use the index. An intentional empty value is the same as a key not existing. These cases cannot be differentiated, and a bloom filter cannot be used for the latter.
