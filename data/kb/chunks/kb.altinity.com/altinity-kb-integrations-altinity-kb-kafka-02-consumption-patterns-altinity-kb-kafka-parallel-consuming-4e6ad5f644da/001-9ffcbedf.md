---
source: kb.altinity.com
url: https://github.com/Altinity/altinityknowledgebase/commit/fde5b9e9f6579a89f6b9ec2f41821d880733aacb
topic: kafka-parallel-consuming-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 1
---

# Kafka parallel consuming \| Altinity® Knowledge Base for ClickHouse®

1. [Integrations](/altinity-kb-integrations/)
2. [Kafka engine](/altinity-kb-integrations/altinity-kb-kafka/)
3. [Consumption Patterns](/altinity-kb-integrations/altinity-kb-kafka/02-consumption-patterns/)
4. Kafka parallel consuming
# Kafka parallel consuming

For very large topics when you need more parallelism (especially on the insert side) you may use several tables with the same pipeline (pre ClickHouse® 20\.9\) or enable `kafka_thread_per_consumer` (after 20\.9\).

```
kafka_num_consumers = N,
kafka_thread_per_consumer=1

```
Notes:

- the inserts will happen in parallel (without that setting inserts happen linearly)
- enough partitions are needed.
- `kafka_num_consumers` is limited by number of physical cores (half of vCPUs). `kafka_disable_num_consumers_limit` can be used to override the limit.
- `background_message_broker_schedule_pool_size` is 16 by default, you may need to increase if using more than 16 consumers

Before increasing `kafka_num_consumers` with keeping `kafka_thread_per_consumer=0` may improve consumption \& parsing speed, but flushing \& committing still happens by a single thread there (so inserts are linear).

Last modified 2026\.03\.12: [Restructure Kafka KB sections and refresh named\-collection guidance (fde5b9e)](https://github.com/Altinity/altinityknowledgebase/commit/fde5b9e9f6579a89f6b9ec2f41821d880733aacb)
