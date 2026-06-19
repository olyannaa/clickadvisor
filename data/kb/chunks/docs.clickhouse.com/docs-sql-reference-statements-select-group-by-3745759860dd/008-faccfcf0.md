---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/select/group-by.md)#
topic: group-by-clause-clickhouse-docs
ch_version_introduced: '0.5'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 9
---

is switched on by the [optimize\_aggregation\_in\_order](/docs/operations/settings/settings#optimize_aggregation_in_order) setting. Such optimization reduces memory usage during aggregation, but in some cases may slow down the query execution. ### GROUP BY in External Memory[​](#group-by-in-external-memory "Direct link to GROUP BY in External Memory")

You can enable dumping temporary data to the disk to restrict memory usage during `GROUP BY`.
The [max\_bytes\_before\_external\_group\_by](/docs/operations/settings/settings#max_bytes_before_external_group_by) setting determines the threshold RAM consumption for dumping `GROUP BY` temporary data to the file system. If set to 0 (the default), it is disabled.
Alternatively, you can set [max\_bytes\_ratio\_before\_external\_group\_by](/docs/operations/settings/settings#max_bytes_ratio_before_external_group_by), which allows to use `GROUP BY` in external memory only once the query reaches certain threshold of used memory.

When using `max_bytes_before_external_group_by`, we recommend that you set `max_memory_usage` about twice as high (or `max_bytes_ratio_before_external_group_by=0.5`). This is necessary because there are two stages to aggregation: reading the data and forming intermediate data (1\) and merging the intermediate data (2\). Dumping data to the file system can only occur during stage 1\. If the temporary data wasn't dumped, then stage 2 might require up to the same amount of memory as in stage 1\.

For example, if [max\_memory\_usage](/docs/operations/settings/settings#max_memory_usage) was set to 10000000000 and you want to use external aggregation, it makes sense to set `max_bytes_before_external_group_by` to 10000000000, and `max_memory_usage` to 20000000000\. When external aggregation is triggered (if there was at least one dump of temporary data), maximum consumption of RAM is only slightly more than `max_bytes_before_external_group_by`.

With distributed query processing, external aggregation is performed on remote servers. In order for the requester server to use only a small amount of RAM, set `distributed_aggregation_memory_efficient` to 1\.

When merging data flushed to the disk, as well as when merging results from remote servers when the `distributed_aggregation_memory_efficient` setting is enabled, consumes up to `1/256 * the_number_of_threads` from the total amount of RAM.

When external aggregation is enabled, if there was less than `max_bytes_before_external_group_by` of data (i.e. data was not flushed), the query runs just as fast as without external aggregation. If any temporary data was flushed, the run time will be several times longer (approximately three times).
