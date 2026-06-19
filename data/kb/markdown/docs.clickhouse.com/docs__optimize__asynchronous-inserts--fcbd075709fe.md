# Asynchronous inserts (async\_insert) \| ClickHouse Docs


- - [Performance and optimizations](/docs/operations/overview)- Asynchronous inserts
[Edit this page](https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/best-practices/asyncinserts.md)# Asynchronous inserts (async\_insert)

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
[PreviousBulk inserts](/docs/optimize/bulk-inserts)[NextAvoid mutations](/docs/optimize/avoid-mutations)- [Choosing a return mode](#choosing-a-return-mode)- [Adaptive async inserts](#adaptive-async-inserts)- [Error handling](#error-handling)- [Deduplication and reliability](#deduplication-and-reliability)- [Enabling asynchronous inserts](#enabling-asynchronous-inserts)- [Flushing buffers on shutdown](#flushing-buffers-on-shutdown)- [Comparison with buffer tables](#comparison-with-buffer-tables)
Was this page helpful?
