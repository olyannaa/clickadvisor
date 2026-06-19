---
source: kb.altinity.com
url: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md>
topic: adjusting-librdkafka-settings-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 2
---

kafka_broker_list = '...', kafka_topic_list = 'foo.bar', kafka_group_name = 'foo.bar.group', kafka.security_protocol = 'SASL_SSL', kafka.sasl_mechanism = 'PLAIN', kafka.sasl_username = '...', kafka.sasl_password = '...', kafka.auto_offset_reset = 'smallest', kafka.ssl_endpoint_identification_algorithm = 'https', kafka.ssl_ca_location = 'probe'; ``` You can verify SQL\-created named collections via:

```
SELECT
    name,
    source,
    create_query
FROM system.named_collections
WHERE name IN ('kafka_preset1', 'kafka_preset2');

```
and remove them with:

```
DROP NAMED COLLECTION kafka_preset1;
DROP NAMED COLLECTION kafka_preset2;

```
The same fragment of code in newer versions:

- [https://github.com/ClickHouse/ClickHouse/blob/d19e24f530c30f002488bc136da78f5fb55aedab/src/Storages/Kafka/StorageKafka.cpp\#L474\-L496](https://github.com/ClickHouse/ClickHouse/blob/d19e24f530c30f002488bc136da78f5fb55aedab/src/Storages/Kafka/StorageKafka.cpp#L474-L496)

Last modified 2026\.03\.12: [Restructure Kafka KB sections and refresh named\-collection guidance (fde5b9e)](https://github.com/Altinity/altinityknowledgebase/commit/fde5b9e9f6579a89f6b9ec2f41821d880733aacb)
