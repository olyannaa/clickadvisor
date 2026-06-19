---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-25-3
ch_version_introduced: '25.3'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 7
---

`s3Cluster` table function: ``` ``` 1SELECT count() 2FROM s3Cluster(default, 'https://clickhouse-public-datasets.s3.amazonaws.com/bluesky/file_{0001..0100}.json.gz', 'JSONAsObject') 3WHERE (json.kind = 'commit') 4AND (json.commit.operation = 'create') 5AND (json.commit.collection = 'app.bsky.feed.post') 6AND (json.commit.record.text LIKE '%🥨%') 7SETTINGS 8 input_format_allow_errors_num = 100, 9 input_format_allow_errors_ratio = 1; ``` ```

Let’s see how long this takes!

```

```
┌─count()─┐
│      69 │
└─────────┘

1 row in set. Elapsed: 16.689 sec. Processed 100.00 million rows, 13.38 GB (5.99 million rows/s., 801.86 MB/s.)
Peak memory usage: 2.06 GiB.
```

```

That’s cut the time down by 4x \- not quite linear, but not too bad!

`…Cluster` functions like [s3Cluster](https://clickhouse.com/docs/sql-reference/table-functions/s3Cluster), [azureBlobStorageCluster](https://clickhouse.com/docs/sql-reference/table-functions/azureBlobStorageCluster), [deltaLakeCluster](https://clickhouse.com/docs/sql-reference/table-functions/deltalakeCluster), [icebergCluster](https://clickhouse.com/docs/sql-reference/table-functions/icebergCluster), and [more](https://clickhouse.com/docs/sql-reference/table-functions) distribute work similarly to [parallel replicas](https://clickhouse.com/docs/deployment-guides/parallel-replicas)—but with a key difference: parallel replicas split work by [granule](https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes#data-is-organized-into-granules-for-parallel-data-processing) ranges, while `…Cluster` functions operate at the file level. We illustrate this below for our example query above with a diagram:

![Blog-release-25.3.001.png](/uploads/Blog_release_25_3_001_e098f3d404.png)
The initiator server—the one receiving the query—resolves the file glob pattern, connects to all other servers, and dynamically dispatches files. The other servers request files from the initiator as they finish processing, repeating until all files are handled. Each server uses N parallel streams (based on its CPU cores) to read and process different ranges within each file. All partial results are then merged and streamed back to the initiator, which assembles the final result. Due to the overhead of coordination and merging partial results, the speedup isn’t always linear.

Starting from 25\.3, you don’t need to call the `…Cluster` versions of remote data access functions to get distributed processing. Instead, ClickHouse will automatically distribute the work when called from a cluster if you have enabled parallel replicas.

If you don’t want distributed processing, you can disable it by setting the following property:

```

```
1SET parallel_replicas_for_cluster_engines = 0;
```

```

## arraySymmetricDifference [\#](/blog/clickhouse-release-25-03#arraysymmetricdifference)

### Contributed by Filipp Abapolov [\#](/blog/clickhouse-release-25-03#contributed-by-filipp-abapolov)

ClickHouse has an extensive collection of array functions that can solve various problems. One such problem is determining which elements in a pair of arrays exist in one array but not the other.

We can work this out by computing the union of the array and then removing any elements that are contained in the intersection of the arrays:
