# Selecting an insert strategy \| ClickHouse Docs


- - [Best practices](/docs/best-practices)- Selecting an insert strategy
[Edit this page](https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/selecting_an_insert_strategy.md)# Selecting an insert strategy

Efficient data ingestion forms the basis of high\-performance ClickHouse deployments. Selecting the right insert strategy can dramatically impact throughput, cost, and reliability. This section outlines best practices, tradeoffs, and configuration options to help you make the right decision for your workload.


NoteThe following assumes you're pushing data to ClickHouse via a client. If you're pulling data into ClickHouse e.g. using built in table functions such as [s3](/docs/sql-reference/table-functions/s3) and [gcs](/docs/sql-reference/table-functions/gcs), we recommend our guide ["Optimizing for S3 Insert and Read Performance"](/docs/integrations/s3/performance).


## Synchronous inserts by default[​](#synchronous-inserts-by-default "Direct link to Synchronous inserts by default")


By default, inserts into ClickHouse are synchronous. Each insert query immediately creates a storage part on disk, including metadata and indexes.


Use synchronous inserts if you can batch the data client sideIf not, see [Asynchronous inserts](#asynchronous-inserts) below.


We briefly review ClickHouse's MergeTree insert mechanics below:


![Insert processes](/docs/assets/ideal-img/insert_process.53ab361.48.png)
#### Client\-side steps[​](#client-side-steps "Direct link to Client-side steps")


For optimal performance, data must be ① [batched](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#data-needs-to-be-batched-for-optimal-performance), making batch size the **first decision**.


ClickHouse stores inserted data on disk, [ordered](/docs/guides/best-practices/sparse-primary-indexes#data-is-stored-on-disk-ordered-by-primary-key-columns) by the table's primary key columns. The **second decision** is whether to ② pre\-sort the data before transmission to the server. If a batch arrives pre\-sorted by primary key columns, ClickHouse can [skip](https://github.com/ClickHouse/ClickHouse/blob/94ce8e95404e991521a5608cd9d636ff7269743d/src/Storages/MergeTree/MergeTreeDataWriter.cpp#L595) the ⑩ sorting step, speeding up ingestion.


If the data to be ingested has no predefined format, the **key decision** is choosing a format. ClickHouse supports inserting data in [over 70 formats](/docs/interfaces/formats). However, when using the ClickHouse command\-line client or programming language clients, this choice is often handled automatically. If needed, this automatic selection can also be overridden explicitly.


The next **major decision** is ④ whether to compress data before transmission to the ClickHouse server. Compression reduces transfer size and improves network efficiency, leading to faster data transfers and lower bandwidth usage, especially for large datasets.


The data is ⑤ transmitted to a ClickHouse network interface—either the [native](/docs/interfaces/tcp) or [HTTP](/docs/interfaces/http) interface (which we [compare](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient#clickhouse-client-defaults) later in this post).


#### Server\-side steps[​](#server-side-steps "Direct link to Server-side steps")


After ⑥ receiving the data, ClickHouse ⑦ decompresses it if compression was used, then ⑧ parses it from the originally sent format.


Using the values from that formatted data and the target table's [DDL](/docs/sql-reference/statements/create/table) statement, ClickHouse ⑨ builds an in\-memory [block](/docs/development/architecture#block) in the MergeTree format, ⑩ [sorts](/docs/parts#what-are-table-parts-in-clickhouse) rows by the primary key columns if they're not already pre\-sorted, ⑪ creates a [sparse primary index](/docs/guides/best-practices/sparse-primary-indexes), ⑫ applies [per\-column compression](/docs/parts#what-are-table-parts-in-clickhouse), and ⑬ writes the data as a new ⑭ [data part](/docs/parts) to disk.


### Batch inserts if synchronous[​](#batch-inserts-if-synchronous "Direct link to Batch inserts if synchronous")


The above mechanics illustrate a constant overhead regardless of the insert size, making batch size the single most important optimization for ingest throughput. Batching inserts reduce the overhead as a proportion of total insert time and improves processing efficiency.


We recommend inserting data in batches of at least 1,000 rows, and ideally between 10,000–100,000 rows. Fewer, larger inserts reduce the number of parts written, minimize merge load, and lower overall system resource usage.


**For a synchronous insert strategy to be effective this client\-side batching is required.**


If you're unable to batch data client\-side, ClickHouse supports asynchronous inserts that shift batching to the server ([see Asynchronous inserts](/docs/best-practices/selecting-an-insert-strategy#asynchronous-inserts)).


TipRegardless of the size of your inserts, we recommend keeping the number of insert queries around one insert query per second. The reason for this recommendation is that the created parts are merged to larger parts in the background (in order to optimize your data for read queries), and sending too many insert queries per second can lead to situations where the background merging can't keep up with the number of new parts. However, you can use a higher rate of insert queries per second when you use asynchronous inserts (see [Asynchronous inserts](/docs/best-practices/selecting-an-insert-strategy#asynchronous-inserts)).


### Ensure idempotent retries[​](#ensure-idempotent-retries "Direct link to Ensure idempotent retries")


Synchronous inserts are also **idempotent**. When using MergeTree engines, ClickHouse will deduplicate inserts by default. This protects against ambiguous failure cases, such as:


- The insert succeeded but the client never received an acknowledgment due to a network interruption.
- The insert failed server\-side and timed out.


In both cases, it's safe to **retry the insert** — as long as the batch contents and order remain identical. For this reason, it's critical that clients retry consistently, without modifying or reordering data.


### Choose the right insert target[​](#choose-the-right-insert-target "Direct link to Choose the right insert target")


For sharded clusters, you have two options:


- Insert directly into a **MergeTree** or **ReplicatedMergeTree** table. This is the most efficient option when the client can perform load balancing across shards. With `internal_replication = true`, ClickHouse handles replication transparently.
- Insert into a [Distributed table](/docs/engines/table-engines/special/distributed). This allows clients to send data to any node and let ClickHouse forward it to the correct shard. This is simpler but slightly less performant due to the extra forwarding step. `internal_replication = true` is still recommended.


**In ClickHouse Cloud all nodes read and write to the same single shard. Inserts are automatically balanced across nodes. You can simply send inserts to the exposed endpoint.**


### Choose the right format[​](#choose-the-right-format "Direct link to Choose the right format")


Choosing the right input format is crucial for efficient data ingestion in ClickHouse. With over 70 supported formats, selecting the most performant option can significantly impact insert speed, CPU and memory usage, and overall system efficiency.


While flexibility is useful for data engineering and file\-based imports, **applications should prioritize performance\-oriented formats**:


- **Native format** (recommended): Most efficient. Column\-oriented, minimal parsing required server\-side. Used by default in Go and Python clients.
- **RowBinary**: Efficient row\-based format, ideal if columnar transformation is hard client\-side. Used by the Java client.
- **JSONEachRow**: Easy to use but expensive to parse. Suitable for low\-volume use cases or quick integrations.


### Use compression[​](#use-compression "Direct link to Use compression")


Compression plays a critical role in reducing network overhead, speeding up inserts, and lowering storage costs in ClickHouse. Used effectively, it enhances ingestion performance without requiring changes to data format or schema.


Compressing insert data reduces the size of the payload sent over the network, minimizing bandwidth usage and accelerating transmission.


For inserts, compression is especially effective when used with the Native format, which already matches ClickHouse's internal columnar storage model. In this setup, the server can efficiently decompress and directly store the data with minimal transformation.


#### Use LZ4 for speed, ZSTD for compression ratio[​](#use-lz4-for-speed-zstd-for-compression-ratio "Direct link to Use LZ4 for speed, ZSTD for compression ratio")


ClickHouse supports several compression codecs during data transmission. Two common options are:


- **LZ4**: Fast and lightweight. It reduces data size significantly with minimal CPU overhead, making it ideal for high\-throughput inserts and default in most ClickHouse clients.
- **ZSTD**: Higher compression ratio but more CPU\-intensive. It's useful when network transfer costs are high—such as in cross\-region or cloud provider scenarios—though it increases client\-side compute and server\-side decompression time slightly.


Best practice: Use LZ4 unless you have constrained bandwidth or incur data egress costs — then consider ZSTD.


NoteIn tests from the [FastFormats benchmark](https://clickhouse.com/blog/clickhouse-input-format-matchup-which-is-fastest-most-efficient), LZ4\-compressed Native inserts reduced data size by more than 50%, cutting ingestion time from 150s to 131s for a 5\.6 GiB dataset. Switching to ZSTD compressed the same dataset down to 1\.69 GiB, but increased server\-side processing time slightly.


#### Compression reduces resource usage[​](#compression-reduces-resource-usage "Direct link to Compression reduces resource usage")


Compression not only reduces network traffic—it also improves CPU and memory efficiency on the server. With compressed data, ClickHouse receives fewer bytes and spends less time parsing large inputs. This benefit is especially important when ingesting from multiple concurrent clients, such as in observability scenarios.


The impact of compression on CPU and memory is modest for LZ4, and moderate for ZSTD. Even under load, server\-side efficiency improves due to the reduced data volume.


**Combining compression with batching and an efficient input format (like Native) yields the best ingestion performance.**


When using the native interface (e.g. [clickhouse\-client](/docs/interfaces/cli)), LZ4 compression is enabled by default. You can optionally switch to ZSTD via settings.


With the [HTTP interface](/docs/interfaces/http), use the Content\-Encoding header to apply compression (e.g. Content\-Encoding: lz4\). The entire payload must be compressed before sending.


### Pre\-sort if low cost[​](#pre-sort-if-low-cost "Direct link to Pre-sort if low cost")


Pre\-sorting data by primary key before insertion can improve ingestion efficiency in ClickHouse, particularly for large batches.


When data arrives pre\-sorted, ClickHouse can skip or simplify the internal sorting step during part creation, reducing CPU usage and accelerating the insert process. Pre\-sorting also improves compression efficiency, since similar values are grouped together—enabling codecs like LZ4 or ZSTD to achieve a better compression ratio. This is especially beneficial when combined with large batch inserts and compression, as it reduces both the processing overhead and the amount of data transferred.


**That said, pre\-sorting is an optional optimization—not a requirement.** ClickHouse sorts data highly efficiently using parallel processing, and in many cases, server\-side sorting is faster or more convenient than pre\-sorting client\-side.


**We recommend pre\-sorting only if the data is already nearly ordered or if client\-side resources (CPU, memory) are sufficient and underutilized.** In latency\-sensitive or high\-throughput use cases, such as observability, where data arrives out of order or from many agents, it's often better to skip pre\-sorting and rely on ClickHouse's built\-in performance.


## Asynchronous inserts[​](#asynchronous-inserts "Direct link to Asynchronous inserts")


Asynchronous inserts in ClickHouse provide a powerful alternative when client\-side batching isn't feasible. This is especially valuable in observability workloads, where hundreds or thousands of agents send data continuously—logs, metrics, traces—often in small, real\-time payloads. Buffering data client\-side in these environments increases complexity, requiring a centralized queue to ensure sufficiently large batches can be sent.


NoteSending many small batches in synchronous mode isn't recommended, leading to many parts being created. This will lead to poor query performance and ["too many part"](/docs/knowledgebase/exception-too-many-parts) errors.


Asynchronous inserts shift batching responsibility from the client to the server by writing incoming data to an in\-memory buffer, then flushing it to storage based on configurable thresholds. This approach significantly reduces part creation overhead, lowers CPU usage, and ensures ingestion remains efficient—even under high concurrency.


The core behavior is controlled via the [`async_insert`](/docs/operations/settings/settings#async_insert) setting.


![Async inserts](/docs/assets/ideal-img/async_inserts.da52804.48.png)
Asynchronous inserts are supported over both the HTTP and native TCP interfaces.


When enabled (`async_insert = 1`), inserts are buffered and only written to disk once one of the flush conditions is met:


- The buffer reaches a specified data size ([`async_insert_max_data_size`](/docs/operations/settings/settings#async_insert_max_data_size), default 100 MiB).
- A time threshold elapses ([`async_insert_busy_timeout_ms`](/docs/operations/settings/settings#async_insert_busy_timeout_max_ms), default 200 ms or 1000 ms on Cloud).
- A maximum number of insert queries accumulate ([`async_insert_max_query_number`](/docs/operations/settings/settings#async_insert_max_query_number), default 450\).


Whichever threshold is reached first triggers the flush.


This batching process is invisible to clients and helps ClickHouse efficiently merge insert traffic from multiple sources. However, until a flush occurs, the data can't be queried. Importantly, there are multiple buffers per insert shape and settings combination, and in clusters, buffers are maintained per node—enabling fine\-grained control across multi\-tenant environments. Insert mechanics are otherwise identical to those described for [synchronous inserts](/docs/best-practices/selecting-an-insert-strategy#synchronous-inserts-by-default).


### Choosing a return mode[​](#choosing-a-return-mode "Direct link to Choosing a return mode")


The behavior of asynchronous inserts is further refined using the [`wait_for_async_insert`](/docs/operations/settings/settings#wait_for_async_insert) setting.


When set to 1 (the default), ClickHouse only acknowledges the insert after the data is successfully flushed to disk. This ensures strong durability guarantees and makes error handling straightforward: if something goes wrong during the flush, the error is returned to the client. This mode is recommended for most production scenarios, especially when insert failures must be tracked reliably.


[Benchmarks](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse) show it scales well with concurrency—whether you're running 200 or 500 clients—thanks to adaptive inserts and stable part creation behavior.


Setting `wait_for_async_insert = 0` enables "fire\-and\-forget" mode. Here, the server acknowledges the insert as soon as the data is buffered, without waiting for it to reach storage.


This offers ultra\-low\-latency inserts and maximal throughput, ideal for high\-velocity, low\-criticality data. However, this comes with trade\-offs: there's no guarantee the data will be persisted, errors only surface during flush, and there is no dead\-letter queue for failed inserts — tracing failures requires inspecting server logs and system tables after the fact. Use this mode only if your workload can tolerate data loss.


[Benchmarks also demonstrate](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse) substantial part reduction and lower CPU usage when buffer flushes are infrequent (e.g. every 30 seconds), but the risk of silent failure remains.


Our strong recommendation is to use `async_insert=1,wait_for_async_insert=1` if using asynchronous inserts. Using `wait_for_async_insert=0` is very risky because your INSERT client may not be aware if there are errors, and also can cause potential overload if your client continues to write quickly in a situation where the ClickHouse server needs to slow down the writes and create some backpressure to ensure reliability of the service.


### Adaptive async inserts[​](#adaptive-async-inserts "Direct link to Adaptive async inserts")


Since version 24\.2, ClickHouse uses adaptive flush timeouts by default ([`async_insert_use_adaptive_busy_timeout`](/docs/operations/settings/settings#async_insert_use_adaptive_busy_timeout)). Instead of a fixed flush interval, the timeout dynamically adjusts between a minimum ([`async_insert_busy_timeout_min_ms`](/docs/operations/settings/settings#async_insert_busy_timeout_min_ms), default 50 ms) and maximum ([`async_insert_busy_timeout_max_ms`](/docs/operations/settings/settings#async_insert_busy_timeout_max_ms), default 200 ms or 1000 ms on Cloud) based on incoming data rate.


When data arrives frequently, the timeout stays closer to the minimum to flush sooner and reduce end\-to\-end latency. When data is sparse, it grows toward the maximum to accumulate larger batches. This is especially useful in default mode (`wait_for_async_insert=1`), where a fixed high timeout would force clients to block for the full interval even when data is ready to flush.


### Error handling[​](#error-handling "Direct link to Error handling")


Schema validation and data parsing happen during buffer flush, not when the insert is received. If any row in an insert query has a parsing or type error, **none of the data from that query is flushed** — the entire query's payload is rejected. In default mode (`wait_for_async_insert=1`), the error is returned to the client. In fire\-and\-forget mode, errors are written to server logs and the [`system.asynchronous_inserts`](/docs/operations/system-tables/asynchronous_inserts) table.


Each flush creates at least one part per distinct partition key value in the buffer. Even for tables without a partition key, a single flush can produce multiple parts if the buffered data exceeds [`max_insert_block_size`](/docs/operations/settings/settings#max_insert_block_size) (default \~1 million rows).


NoteDespite using async inserts, you can still encounter ["too many parts"](/docs/knowledgebase/exception-too-many-parts) errors if the partitioning key has high cardinality.


### Deduplication and reliability[​](#deduplication-and-reliability "Direct link to Deduplication and reliability")


By default, ClickHouse performs automatic deduplication for synchronous inserts, which makes retries safe in failure scenarios. However, this is disabled for asynchronous inserts unless explicitly enabled (this shouldn't be enabled if you have dependent materialized views — [see issue](https://github.com/ClickHouse/ClickHouse/issues/66003)).


In practice, if deduplication is turned on and the same insert is retried — due to, for instance, a timeout or network drop — ClickHouse can safely ignore the duplicate. This helps maintain idempotency and avoids double\-writing data.


### Enabling asynchronous inserts[​](#enabling-asynchronous-inserts "Direct link to Enabling asynchronous inserts")


Asynchronous inserts can be enabled for a particular user, or for a specific query:


- Enabling asynchronous inserts at the user level. This example uses the user `default`, if you create a different user then substitute that username:



```
ALTER USER default SETTINGS async_insert = 1

```
- You can specify the asynchronous insert settings by using the SETTINGS clause of insert queries:



```
INSERT INTO YourTable SETTINGS async_insert=1, wait_for_async_insert=1 VALUES (...)

```
- You can also specify asynchronous insert settings as connection parameters when using a ClickHouse programming language client.


As an example, this is how you can do that within a JDBC connection string when you use the ClickHouse Java JDBC driver for connecting to ClickHouse Cloud:



```
"jdbc:ch://HOST.clickhouse.cloud:8443/?user=default&password=PASSWORD&ssl=true&custom_http_params=async_insert=1,wait_for_async_insert=1"

```


NoteAsynchronous inserts don't apply to `INSERT INTO ... SELECT` queries. When the insert contains a `SELECT` clause, the query is always executed synchronously regardless of the `async_insert` setting.


### Flushing buffers on shutdown[​](#flushing-buffers-on-shutdown "Direct link to Flushing buffers on shutdown")


To flush all pending async insert buffers — for example, during a graceful shutdown or before maintenance — run:



```
SYSTEM FLUSH ASYNC INSERT QUEUE

```

This ensures any buffered data is written to storage before the server stops.


### Comparison with buffer tables[​](#comparison-with-buffer-tables "Direct link to Comparison with buffer tables")


Asynchronous inserts are the modern replacement for [Buffer tables](/docs/engines/table-engines/special/buffer). Key differences:


- **No DDL changes required.** Async inserts are transparent — you enable a setting, not create additional tables.
- **Per\-shape buffering.** Async inserts maintain separate buffers per unique query shape and settings combination, enabling granular flush policies. Buffer tables use a single buffer per target table.
- **Durability.** In default mode (`wait_for_async_insert=1`), data is confirmed on disk before the client receives acknowledgment. Buffer tables behave like fire\-and\-forget — buffered data is lost on crash.
- **Cluster behavior.** In clusters, async insert buffers are maintained per node. Buffer tables require explicit creation on each node.


## Choose an interface—HTTP or native[​](#choose-an-interface "Direct link to Choose an interface—HTTP or native")


### Native[​](#choose-an-interface-native "Direct link to Native")


ClickHouse offers two main interfaces for data ingestion: the **native interface** and the **HTTP interface**—each with trade\-offs between performance and flexibility. The native interface, used by [clickhouse\-client](/docs/interfaces/cli) and select language clients like Go and C\+\+, is purpose\-built for performance. It always transmits data in ClickHouse's highly efficient Native format, supports block\-wise compression with LZ4 or ZSTD, and minimizes server\-side processing by offloading work such as parsing and format conversion to the client.


It even enables client\-side computation of MATERIALIZED and DEFAULT column values, allowing the server to skip these steps entirely. This makes the native interface ideal for high\-throughput ingestion scenarios where efficiency is critical.


### HTTP[​](#choose-an-interface-http "Direct link to HTTP")


Unlike many traditional databases, ClickHouse also supports an HTTP interface. **This, by contrast, prioritizes compatibility and flexibility.** It allows data to be sent in [any supported format](/docs/integrations/data-formats)—including JSON, CSV, Parquet, and others—and is widely supported across most ClickHouse clients, including Python, Java, JavaScript, and Rust.


This is often preferable to ClickHouse's native protocol as it allows traffic to be easily switched with load balancers. We expect small differences in insert performance with the native protocol, which incurs a little less overhead.


However, it lacks the native protocol's deeper integration and can't perform client\-side optimizations like materialized value computation or automatic conversion to Native format. While HTTP inserts can still be compressed using standard HTTP headers (e.g. `Content-Encoding: lz4`), the compression is applied to the entire payload rather than individual data blocks. This interface is often preferred in environments where protocol simplicity, load balancing, or broad format compatibility is more important than raw performance.


For a more detailed description of these interfaces see [here](/docs/interfaces/overview).

[PreviousChoosing a partitioning key](/docs/best-practices/choosing-a-partitioning-key)[NextData skipping indices](/docs/best-practices/use-data-skipping-indices-where-appropriate)- [Synchronous inserts by default](#synchronous-inserts-by-default)
	- [Batch inserts if synchronous](#batch-inserts-if-synchronous)- [Ensure idempotent retries](#ensure-idempotent-retries)- [Choose the right insert target](#choose-the-right-insert-target)- [Choose the right format](#choose-the-right-format)- [Use compression](#use-compression)- [Pre\-sort if low cost](#pre-sort-if-low-cost)- [Asynchronous inserts](#asynchronous-inserts)
	- [Choosing a return mode](#choosing-a-return-mode)- [Adaptive async inserts](#adaptive-async-inserts)- [Error handling](#error-handling)- [Deduplication and reliability](#deduplication-and-reliability)- [Enabling asynchronous inserts](#enabling-asynchronous-inserts)- [Flushing buffers on shutdown](#flushing-buffers-on-shutdown)- [Comparison with buffer tables](#comparison-with-buffer-tables)- [Choose an interface—HTTP or native](#choose-an-interface)
	- [Native](#choose-an-interface-native)- [HTTP](#choose-an-interface-http)
Was this page helpful?
