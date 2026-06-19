---
source: kb.altinity.com
url: http://altinity.com/
topic: altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 203
total_chunks_in_doc: 478
---

, 0))) WHERE NOT ignore(throwIf(if((uptime() < 120), 1 + sleep(3), 0))) ``` 120 seconds should be enough for loading all MVs. Using an intermediate Null table is also preferable because it’s easier to make any changes with MVs:

- drop the dummy\_MV to stop consuming
- make any changes to transforming MVs by drop/recreate
- create dummy\_MV again to resume consuming

The fix for correctly starting multiple MVs will be available from 25\.5 version \- <https://github.com/ClickHouse/ClickHouse/pull/72123>

# 4\.9\.2\.4 \- Rewind / fast\-forward / replay

Rewind / fast\-forward / replay- Step 1: Detach Kafka tables in ClickHouse®
```
DETACH TABLE db.kafka_table_name ON CLUSTER '{cluster}';

```
- Step 2: `kafka-consumer-groups.sh --bootstrap-server kafka:9092 --topic topic:0,1,2 --group id1 --reset-offsets --to-latest --execute`
	- More samples: <https://gist.github.com/filimonov/1646259d18b911d7a1e8745d6411c0cc>
- Step 3: Attach Kafka tables back
```
ATTACH TABLE db.kafka_table_name ON CLUSTER '{cluster}';

```

See also these configuration settings:

```
<kafka>
  <auto_offset_reset>smallest</auto_offset_reset>
</kafka>

```
### About Offset Consuming

When a consumer joins the consumer group, the broker will check if it has a committed offset. If that is the case, then it will start from the latest offset. Both ClickHouse and librdKafka documentation state that the default value for `auto_offset_reset` is largest (or `latest` in new Kafka versions) but it is not, if the consumer is new:

[https://github.com/ClickHouse/ClickHouse/blob/f171ad93bcb903e636c9f38812b6aaf0ab045b04/src/Storages/Kafka/StorageKafka.cpp\#L506](https://github.com/ClickHouse/ClickHouse/blob/f171ad93bcb903e636c9f38812b6aaf0ab045b04/src/Storages/Kafka/StorageKafka.cpp#L506)

 `conf.set("auto.offset.reset", "earliest");     // If no offset stored for this group, read all messages from the start`

If there is no offset stored or it is out of range, for that particular consumer group, the consumer will start consuming from the beginning (`earliest`), and if there is some offset stored then it should use the `latest`.
The log retention policy influences which offset values correspond to the `earliest` and `latest` configurations. Consider a scenario where a topic has a retention policy set to 1 hour. Initially, you produce 5 messages, and then, after an hour, you publish 5 more messages. In this case, the latest offset will remain unchanged from the previous example. However, due to Kafka removing the earlier messages, the earliest available offset will not be 0; instead, it will be 5\.

# 4\.9\.3 \- Schema and Formats

Schema inference and format\-specific integration details.# 4\.9\.3\.1 \- Inferring Schema from AvroConfluent Messages in Kafka for ClickHouse®
