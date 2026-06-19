---
source: blog
url: https://rotel.dev/
topic: from-otel-to-rotel-petabyte-scale-tracing-with-4x-greater-throughput
ch_version_introduced: '0.90'
last_updated: '2026-06-12'
chunk_index: 6
total_chunks_in_doc: 20
---

We experimented with a few Kafka configuration options, including message size parameters, but none noticeably improved throughput. Instead, we scaled horizontally by running a second collector instance on the same box (`scale: 2` in our Docker Compose setup).

With two collector processes running, each consuming half the Kafka partitions, the highest throughput we could maintain before saturation was **1\.1M trace spans/sec (69MB/s)**. Past that point the sending queue began to fill and memory usage increased rapidly. When the sending queue was entirely full the Kafka receiver would continue to read messages, but drop them immediately. **This meant that the consumer lag didn’t grow, but we were also losing data!**

CPU on the gateway collector peaked at a little over 83% during the test and appeared to be the limiting factor. ClickHouse CPU sat around 23%.

|  | Rotel | ClickHouse |
| --- | --- | --- |
| CPU | 83\.1% | 23\.8% |


![otel-results.png](/uploads/otel_results_f795e64d32.png)
## Testing Rotel [\#](/blog/otel-to-rotel-petabyte-scaling-tracing-4x-greater-throughput#testing-rotel)

### Set up [\#](/blog/otel-to-rotel-petabyte-scaling-tracing-4x-greater-throughput#set-up-1)

![rotel-pipeline-4.jpg](/uploads/rotel_pipeline_4_792d48f813.jpg)
*You can find the docker\-compose config [here](https://github.com/streamfold/rotel-clickhouse-benchmark/blob/main/docker-compose-rotel.yml)*.

### Results [\#](/blog/otel-to-rotel-petabyte-scaling-tracing-4x-greater-throughput#results-1)

| Rotel | Trace Spans | Trace Spans / Core | ClickHouse Network In (compressed) |
| --- | --- | --- | --- |
| Single Rotel Process | **750 K/sec** | **93\.75 K/sec** | **41 MB/sec** |
| Dual Rotel Processes | **1\.45 M/sec** | **181\.3 K/sec** | **76 MB/sec** |


Rotel has a single receiver loop that pulls messages from Kafka, similar to the OTel collector. This led us to believe we had a **serial processing bottleneck**, which was initially confirmed when we were able to scale to the full instance CPU running two instances of the Rotel process.

With dual Rotel processes, we were able to push up to **1\.45M trace spans/sec (76 MB/sec)**, about a **1\.3x improvement** on total throughput from the OTel collector. Past 1\.45M we noticed Kafka consumer lag slowly increase, implying that we were unable to consume from Kafka fast enough.

At 1\.45M trace spans/sec, CPU on the gateway collector instance became a bottleneck, with ClickHouse CPU rising to about 60%.

|  | Rotel | ClickHouse |
| --- | --- | --- |
| CPU | 91\.3% | 60\.4% |


![rotel-results-1.png](/uploads/rotel_results_1_9946792598.png)
We continued to search for optimization opportunities, which turned our attention to how we were sending JSON column types.
