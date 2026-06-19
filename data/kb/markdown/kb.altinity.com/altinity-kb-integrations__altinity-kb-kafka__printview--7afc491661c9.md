# Kafka engine \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-integrations/altinity-kb-kafka/).

# Kafka engine

Kafka engine- 1: [Fundamentals](#pg-e400198f558c9faf55d9584513daae76)
- 1\.1: [Config by provider](#pg-f7ee7badcea9b057d56121c267c25f1a)
- 1\.2: [Kafka engine Virtual columns](#pg-07327efff9edeecb27f65a5e89176c9c)
- 1\.3: [Adjusting librdkafka settings](#pg-8a81f9f3e797d0ac2601d4082c3df433)
- 1\.4: [Kafka main parsing loop](#pg-c1a2582c190b6159a224fe52640906f4)
- 1\.5: [SELECTs from engine\=Kafka](#pg-b99736fda9be9177a70a7f7654a6a7e7)

- 2: [Consumption Patterns](#pg-1aef5848f7918d10501b05101d5969a3)
- 2\.1: [Exactly once semantics](#pg-9910a8e5e716d0d43688ee743d9e9c1d)
- 2\.2: [Kafka parallel consuming](#pg-a07e7499854b2c84724f7a8f8cd0101c)
- 2\.3: [Multiple MVs attached to Kafka table](#pg-acca47b87a726ce66aeb82e3617b2bd0)
- 2\.4: [Rewind / fast\-forward / replay](#pg-b298539c9e9ec1f4b9bbd5c1875468b2)

- 3: [Schema and Formats](#pg-9e2b9ea25a1c89d439f9f29ccf819d6f)
- 3\.1: [Inferring Schema from AvroConfluent Messages in Kafka for ClickHouse®](#pg-150cd8aebb4a61016c1041f0416a3535)

- 4: [Operations and Troubleshooting](#pg-3909b2a297d8df066f87015320efb1ee)
- 4\.1: [Setting the background message broker schedule pool size](#pg-9bb6a1cee0851ed7ac325e716c88c83a)
- 4\.2: [Error handling](#pg-ca5766c73f2f8616908b06c03dfbf630)

## librdkafka changelog

This changelog tracks the librdkafka version bundled with ClickHouse and notable related fixes.


```
git log -- contrib/librdkafka | git name-rev --stdin

```


| **ClickHouse® version** | **librdkafka version** |
| --- | --- |
| 25\.3\+ ([\#63697](https://github.com/ClickHouse/ClickHouse/issues/63697) ) | [2\.8\.0](https://github.com/confluentinc/librdkafka/blob/v2.8.0/CHANGELOG.md) \+ few [fixes](https://gist.github.com/filimonov/ad252aa601d4d99fb57d4d76f14aa2bf) |
| 21\.10\+ ([\#27883](https://github.com/ClickHouse/ClickHouse/pull/27883) ) | [1\.6\.1](https://github.com/edenhill/librdkafka/blob/v1.6.1/CHANGELOG.md) \+ snappy fixes \+ boring ssl \+ illumos\_build fixes \+ edenhill\#3279 fix |
| 21\.6\+ ([\#23874](https://github.com/ClickHouse/ClickHouse/pull/23874) ) | [1\.6\.1](https://github.com/edenhill/librdkafka/blob/v1.6.1/CHANGELOG.md) \+ snappy fixes \+ boring ssl \+ illumos\_build fixes |
| 21\.1\+ ([\#18671](https://github.com/ClickHouse/ClickHouse/pull/18671) ) | [1\.6\.0\-RC3](https://github.com/edenhill/librdkafka/blob/v1.6.0-RC3/CHANGELOG.md) \+ snappy fixes \+ boring ssl |
| 20\.13\+ ([\#18053](https://github.com/ClickHouse/ClickHouse/pull/18053) ) | [1\.5\.0](https://github.com/edenhill/librdkafka/blob/v1.5.0/CHANGELOG.md) \+ msan fixes \+ snappy fixes \+ boring ssl |
| 20\.7\+ ([\#12991](https://github.com/ClickHouse/ClickHouse/pull/12991) ) | [1\.5\.0](https://github.com/edenhill/librdkafka/blob/v1.5.0/CHANGELOG.md) \+ msan fixes |
| 20\.5\+ ([\#11256](https://github.com/ClickHouse/ClickHouse/pull/11256) ) | [1\.4\.2](https://github.com/edenhill/librdkafka/blob/v1.4.2/CHANGELOG.md) |
| 20\.2\+ ([\#9000](https://github.com/ClickHouse/ClickHouse/pull/9000) ) | [1\.3\.0](https://github.com/edenhill/librdkafka/releases?after=v1.4.0-PRE1) |
| 19\.11\+ ([\#5872](https://github.com/ClickHouse/ClickHouse/pull/5872) ) | [1\.1\.0](https://github.com/edenhill/librdkafka/releases?after=v1.1.0-selfstatic-test12) |
| 19\.5\+ ([\#4799](https://github.com/ClickHouse/ClickHouse/pull/4799) ) | [1\.0\.0](https://github.com/edenhill/librdkafka/releases?after=v1.0.1-RC1) |
| 19\.1\+ ([\#4025](https://github.com/ClickHouse/ClickHouse/pull/4025) ) | 1\.0\.0\-RC5 |
| v1\.1\.54382\+ ([\#2276](https://github.com/ClickHouse/ClickHouse/pull/2276) ) | [0\.11\.4](https://github.com/edenhill/librdkafka/releases?after=v0.11.4-adminapi-post1) |

# 1 \- Fundamentals

Core Kafka engine behavior and query semantics in ClickHouse.# 1\.1 \- Config by provider

Kafka engine configuration examples grouped by managed Kafka provider.Sometimes the consumer group needs to be explicitly allowed in the broker UI config.

Read [Adjusting librdkafka settings](./altinity-kb-adjusting-librdkafka-settings/)
first, then apply the provider\-specific settings below.

### Amazon MSK \| SASL/SCRAM


```
<yandex>
  <kafka>
    <security_protocol>sasl_ssl</security_protocol>
    <!-- Depending on your broker config you may need to uncomment below sasl_mechanism -->
    <!-- <sasl_mechanism>SCRAM-SHA-512</sasl_mechanism> -->
    <sasl_username>root</sasl_username>
    <sasl_password>toor</sasl_password>
  </kafka>
</yandex>

```
- [Broker ports detail](https://docs.aws.amazon.com/msk/latest/developerguide/port-info.html)
- [Read here more](https://leftjoin.ru/blog/data-engineering/clickhouse-as-a-consumer-to-amazon-msk/)
(Russian language)

### on\-prem / self\-hosted Kafka broker


```
<yandex>
  <kafka>
    <security_protocol>sasl_ssl</security_protocol>
    <sasl_mechanism>SCRAM-SHA-512</sasl_mechanism>
    <sasl_username>root</sasl_username>
    <sasl_password>toor</sasl_password>
    <!-- fullchain cert here -->
    <ssl_ca_location>/path/to/cert/fullchain.pem</ssl_ca_location>
  </kafka>
</yandex>

```
### Inline Kafka certs

To connect to some Kafka cloud services you may need to use certificates.

If needed they can be converted to pem format and inlined into ClickHouse® config.xml
Example:


```
<kafka>
<ssl_key_pem><![CDATA[
  RSA Private-Key: (3072 bit, 2 primes)
    ....
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
]]></ssl_key_pem>
<ssl_certificate_pem><![CDATA[
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
]]></ssl_certificate_pem>
</kafka>

```
See

- [https://help.aiven.io/en/articles/489572\-getting\-started\-with\-aiven\-kafka](https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka)
- [https://stackoverflow.com/questions/991758/how\-to\-get\-pem\-file\-from\-key\-and\-crt\-files](https://stackoverflow.com/questions/991758/how-to-get-pem-file-from-key-and-crt-files)

### Azure Event Hub

See <https://github.com/ClickHouse/ClickHouse/issues/12609>

### Confluent Cloud / Google Cloud


```
<yandex>
  <kafka>
    <auto_offset_reset>smallest</auto_offset_reset>
    <security_protocol>SASL_SSL</security_protocol>
    <!-- older broker versions may need this below, for newer versions ignore -->
    <!-- <ssl_endpoint_identification_algorithm>https</ssl_endpoint_identification_algorithm> -->
    <sasl_mechanism>PLAIN</sasl_mechanism>
    <sasl_username>username</sasl_username>
    <sasl_password>password</sasl_password>
    <!-- Same as above here ignore if newer broker version -->
    <!-- <ssl_ca_location>probe</ssl_ca_location> -->
  </kafka>
</yandex>

```
- [https://docs.confluent.io/cloud/current/client\-apps/config\-client.html](https://docs.confluent.io/cloud/current/client-apps/config-client.html)
- [https://cloud.google.com/managed\-service\-for\-apache\-kafka/docs/authentication\-kafka](https://cloud.google.com/managed-service-for-apache-kafka/docs/authentication-kafka)
# 1\.2 \- Kafka engine Virtual columns

Kafka virtual columns## Kafka engine virtual columns (built\-in)

[From the Kafka engine docs](https://clickhouse.com/docs/engines/table-engines/integrations/kafka?utm_source=chatgpt.com#virtual-columns)
, the supported virtual columns are:

- `_topic` — Kafka topic (LowCardinality(String))
- `_key` — message key (String)
- `_offset` — message offset (UInt64\)
- `_timestamp` — message timestamp (Nullable(DateTime))
- `_timestamp_ms` — timestamp with millisecond precision (Nullable(DateTime64(3\)))
- `_partition` — partition (UInt64\)
- `_headers.name` — header keys (Array(String))
- `_headers.value` — header values (Array(String))

Extra virtual columns when you enable parse\-error streaming:

If you set `kafka_handle_error_mode='stream'`, ClickHouse adds:

- `_raw_message` — the raw message that failed to parse (String)
- `_error` — the exception message from parsing failure (String)

Note: `_raw_message` and `_error` are populated only when parsing fails; otherwise they’re empty.

We can use these columns in a materialized view like this for example:

# 1\.3 \- Adjusting librdkafka settings

Adjusting librdkafka settings- To set rdkafka options \- add to `<kafka>` section in `config.xml` or preferably use a separate file in `config.d/`:
	- <https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md>

Some random example using SSL certificates to authenticate:


```
<yandex>
    <kafka>
        <max_poll_interval_ms>60000</max_poll_interval_ms>
        <session_timeout_ms>60000</session_timeout_ms>
        <heartbeat_interval_ms>10000</heartbeat_interval_ms>
        <reconnect_backoff_ms>5000</reconnect_backoff_ms>
        <reconnect_backoff_max_ms>60000</reconnect_backoff_max_ms>
        <request_timeout_ms>20000</request_timeout_ms>
        <retry_backoff_ms>500</retry_backoff_ms>
        <message_max_bytes>20971520</message_max_bytes>
        <debug>all</debug><!-- only to get the errors -->
        <security_protocol>SSL</security_protocol>
        <ssl_ca_location>/etc/clickhouse-server/ssl/kafka-ca-qa.crt</ssl_ca_location>
        <ssl_certificate_location>/etc/clickhouse-server/ssl/client_clickhouse_client.pem</ssl_certificate_location>
        <ssl_key_location>/etc/clickhouse-server/ssl/client_clickhouse_client.key</ssl_key_location>
        <ssl_key_password>pass</ssl_key_password>
    </kafka>
</yandex>

```
## Authentication / connectivity

Sometimes the consumer group needs to be explicitly allowed in the broker UI config.

Use general Kafka/librdkafka settings from this page first, then apply provider\-specific options from [Config by provider](./config-by-provider/)
.

### Kerberos

- [https://clickhouse.tech/docs/en/engines/table\-engines/integrations/kafka/\#kafka\-kerberos\-support](https://clickhouse.tech/docs/en/engines/table-engines/integrations/kafka/#kafka-kerberos-support)
- <https://github.com/ClickHouse/ClickHouse/blob/master/tests/integration/test_storage_kerberized_kafka/configs/kafka.xml>


```
  <!-- Kerberos-aware Kafka -->
  <kafka>
    <security_protocol>SASL_PLAINTEXT</security_protocol>
    <sasl_kerberos_keytab>/home/kafkauser/kafkauser.keytab</sasl_kerberos_keytab>
    <sasl_kerberos_principal>kafkauser/kafkahost@EXAMPLE.COM</sasl_kerberos_principal>
  </kafka>

```
## How to test connection settings

Use kafkacat utility \- it internally uses same library to access Kafla as ClickHouse itself and allows easily to test different settings.


```
kafkacat -b my_broker:9092 -C -o -10 -t my_topic \ (Google cloud and on-prem use 9092 port)
   -X security.protocol=SASL_SSL  \
   -X sasl.mechanisms=PLAIN \
   -X sasl.username=uerName \
   -X sasl.password=Password

```
## Different configurations for different tables?


> Is there some more documentation how to use this multiconfiguration for Kafka ?

The whole logic is here:
[https://github.com/ClickHouse/ClickHouse/blob/da4856a2be035260708fe2ba3ffb9e437d9b7fef/src/Storages/Kafka/StorageKafka.cpp\#L466\-L475](https://github.com/ClickHouse/ClickHouse/blob/da4856a2be035260708fe2ba3ffb9e437d9b7fef/src/Storages/Kafka/StorageKafka.cpp#L466-L475)

So it load the main config first, after that it load (with overwrites) the configs for all topics, **listed in `kafka_topic_list` of the table**.

Also since v21\.12 it’s possible to use more straightforward way using named\_collections:
<https://github.com/ClickHouse/ClickHouse/pull/31691>

So you can write a config file something like this:


```
<clickhouse>
 <named_collections>
  <kafka_preset1>
   <kafka_broker_list>kafka1:19092</kafka_broker_list>
   <kafka_topic_list>conf</kafka_topic_list>
   <kafka_group_name>conf</kafka_group_name>
  </kafka_preset1>
 </named_collections>
</clickhouse>


<clickhouse>
    <named_collections>
        <kafka_preset2>
            <kafka_broker_list>...</kafka_broker_list>
            <kafka_topic_list>foo.bar</kafka_topic_list>
            <kafka_group_name>foo.bar.group</kafka_group_name>
            <kafka>
                <security_protocol>...</security_protocol>
                <sasl_mechanism>...</sasl_mechanism>
                <sasl_username>...</sasl_username>
                <sasl_password>...</sasl_password>
                <auto_offset_reset>smallest</auto_offset_reset>
                <ssl_endpoint_identification_algorithm>https</ssl_endpoint_identification_algorithm>
                <ssl_ca_location>probe</ssl_ca_location>
            </kafka>
        </kafka_preset2>
    </named_collections>
</clickhouse>

```
And after execute:


```
CREATE TABLE test.kafka (key UInt64, value UInt64) ENGINE = Kafka(kafka_preset1, kafka_format='CSV');

```
The same named collections can be created with SQL from v24\.2\+:


```
CREATE NAMED COLLECTION kafka_preset1 AS
    kafka_broker_list = 'kafka1:19092',
    kafka_topic_list = 'conf',
    kafka_group_name = 'conf';

```

```
CREATE NAMED COLLECTION kafka_preset2 AS
    kafka_broker_list = '...',
    kafka_topic_list = 'foo.bar',
    kafka_group_name = 'foo.bar.group',
    kafka.security_protocol = 'SASL_SSL',
    kafka.sasl_mechanism = 'PLAIN',
    kafka.sasl_username = '...',
    kafka.sasl_password = '...',
    kafka.auto_offset_reset = 'smallest',
    kafka.ssl_endpoint_identification_algorithm = 'https',
    kafka.ssl_ca_location = 'probe';

```
You can verify SQL\-created named collections via:


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
# 1\.4 \- Kafka main parsing loop

Kafka main parsing loopOne of the threads from scheduled\_pool (pre ClickHouse® 20\.9\) / `background_message_broker_schedule_pool` (after 20\.9\) do that in infinite loop:

1. Batch poll (time limit: `kafka_poll_timeout_ms` 500ms, messages limit: `kafka_poll_max_batch_size` 65536\)
2. Parse messages.
3. If we don’t have enough data (rows limit: `kafka_max_block_size` 1048576\) or time limit reached (`kafka_flush_interval_ms` 7500ms) \- continue polling (goto p.1\)
4. Write a collected block of data to MV
5. Do commit (commit after write \= at\-least\-once).

On any error, during that process, Kafka client is restarted (leading to rebalancing \- leave the group and get back in few seconds).

![Kafka batching](/assets/128942286.png)

## Important settings

These usually should not be adjusted:

- `kafka_poll_max_batch_size` \= max\_block\_size (65536\)
- `kafka_poll_timeout_ms` \= stream\_poll\_timeout\_ms (500ms)

You may want to adjust those depending on your scenario:

- `kafka_flush_interval_ms` \= stream\_poll\_timeout\_ms (7500ms)
- `kafka_max_block_size` \= max\_insert\_block\_size / kafka\_num\_consumers (for the single consumer: 1048576\)

## See also

<https://github.com/ClickHouse/ClickHouse/pull/11388>

## Disable at\-least\-once delivery

`kafka_commit_every_batch` \= 1 will change the loop logic mentioned above. Consumed batch committed to the Kafka and the block of rows send to Materialized Views only after that. It could be resembled as at\-most\-once delivery mode as prevent duplicate creation but allow loss of data in case of failures.

# 1\.5 \- SELECTs from engine\=Kafka

SELECTs from engine\=Kafka## Question

What will happen, if we would run SELECT query from working Kafka table with MV attached? Would data showed in SELECT query appear later in MV destination table?

## Answer

1. Most likely SELECT query would show nothing.
2. If you lucky enough and something would show up, those rows **wouldn’t appear** in MV destination table.

So it’s not recommended to run SELECT queries on working Kafka tables.

In case of debug it’s possible to use another Kafka table with different `consumer_group`, so it wouldn’t affect your main pipeline.

# 2 \- Consumption Patterns

Message consumption models, replay patterns, and delivery semantics.# 2\.1 \- Exactly once semantics

Exactly once semanticsEOS consumer (isolation.level\=read\_committed) is enabled by default since librdkafka 1\.2\.0, so for ClickHouse® \- since 20\.2

See:

- [edenhill/librdkafka@6b2a155](https://github.com/edenhill/librdkafka/commit/6b2a1552ac2a4ea09d915015183f268dd2df96e6)
- [9de5dff](https://github.com/ClickHouse/ClickHouse/commit/9de5dffb5c97eb93545ae25eaf87ec195a590148)

BUT: while EOS semantics will guarantee you that no duplicates will happen on the Kafka side (i.e. even if you produce the same messages few times it will be consumed once), but ClickHouse as a Kafka client can currently guarantee only at\-least\-once. And in some corner cases (connection lost etc) you can get duplicates.

We need to have something like transactions on ClickHouse side to be able to avoid that. Adding something like simple transactions is in plans for Y2022\.

## block\-aggregator by eBay

Block Aggregator is a data loader that subscribes to Kafka topics, aggregates the Kafka messages into blocks that follow the ClickHouse’s table schemas, and then inserts the blocks into ClickHouse. Block Aggregator provides exactly\-once delivery guarantee to load data from Kafka to ClickHouse. Block Aggregator utilizes Kafka’s metadata to keep track of blocks that are intended to send to ClickHouse, and later uses this metadata information to deterministically re\-produce ClickHouse blocks for re\-tries in case of failures. The identical blocks are guaranteed to be deduplicated by ClickHouse.

[eBay/block\-aggregator](https://github.com/eBay/block-aggregator)

# 2\.2 \- Kafka parallel consuming

Kafka parallel consumingFor very large topics when you need more parallelism (especially on the insert side) you may use several tables with the same pipeline (pre ClickHouse® 20\.9\) or enable `kafka_thread_per_consumer` (after 20\.9\).


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

# 2\.3 \- Multiple MVs attached to Kafka table

How Multiple MVs attached to Kafka table consume and how they are affected by kafka\_num\_consumers/kafka\_thread\_per\_consumerKafka Consumer is a thread inside the Kafka Engine table that is visible by Kafka monitoring tools like kafka\-consumer\-groups and in Clickhouse in system.kafka\_consumers table.

Having multiple consumers increases ingesting parallelism and can significantly speed up event processing. However, it comes with a trade\-off: it’s a CPU\-intensive task, especially under high event load and/or complicated parsing of incoming data. Therefore, it’s crucial to create as many consumers as you really need and ensure you have enough CPU cores to handle them. We don’t recommend creating too many Kafka Engines per server because it could lead to uncontrolled CPU usage in situations like bulk data upload or catching up a huge kafka lag due to excessive parallelism of the ingesting process.

## kafka\_thread\_per\_consumer meaning

Consider a basic pipeline depicted as a Kafka table with 2 MVs attached. The Kafka broker has 2 topics and 4 partitions.

### kafka\_thread\_per\_consumer \= 0

Kafka engine table will act as 2 consumers, but only 1 insert thread for both of them. It is important to note that the topic needs to have as many partitions as consumers. For this scenario, we use these settings:


```
kafka_num_consumers = 2
kafka_thread_per_consumer = 0

```
The same Kafka engine will create 2 streams, 1 for each consumer, and will join them in a union stream. And it will use 1 thread for inserting `[ 2385 ]`
This is how we can see it in the logs:


```
2022.11.09 17:49:34.282077 [ 2385 ] {} <Debug> StorageKafka (kafka_table): Started streaming to 2 attached views

```
- How ClickHouse® calculates the number of threads depending on the `thread_per_consumer` setting:


```
  auto stream_count = thread_per_consumer ? 1 : num_created_consumers;
      sources.reserve(stream_count);
      pipes.reserve(stream_count);
      for (size_t i = 0; i < stream_count; ++i)
      {
         ......
      }

```

Details:

[https://github.com/ClickHouse/ClickHouse/blob/1b49463bd297ade7472abffbc931c4bb9bf213d0/src/Storages/Kafka/StorageKafka.cpp\#L834](https://github.com/ClickHouse/ClickHouse/blob/1b49463bd297ade7472abffbc931c4bb9bf213d0/src/Storages/Kafka/StorageKafka.cpp#L834)

Also, a detailed graph of the pipeline:

![thread_per_consumer0](/assets/thread_per_consumer0.png)

With this approach, even if the number of consumers increased, the Kafka engine will still use only 1 thread to flush. The consuming/processing rate will probably increase a bit, but not linearly. For example, 5 consumers will not consume 5 times faster. Also, a good property of this approach is the `linearization` of INSERTS, which means that the order of the inserts is preserved and sequential. This option is good for small/medium Kafka topics.

### kafka\_thread\_per\_consumer \= 1

Kafka engine table will act as 2 consumers and 1 thread per consumer. For this scenario, we use these settings:


```
kafka_num_consumers = 2
kafka_thread_per_consumer = 1

```
Here, the pipeline works like this:

![thread_per_consumer1](/assets/thread_per_consumer1.png)

With this approach, the number of consumers remains the same, but each consumer will use their own insert/flush thread, and the consuming/processing rate should increase.

## Background Pool

In Clickhouse there is a special thread pool for background processes, such as streaming engines. Its size is controlled by the background\_message\_broker\_schedule\_pool\_size setting and is 16 by default. If you exceed this limit across all tables on the server, you’ll likely encounter continuous Kafka rebalances, which will slow down processing considerably. For a server with a lot of CPU cores, you can increase that limit to a higher value, like 20 or even 40\. `background_message_broker_schedule_pool_size` \= 20 allows you to create 5 Kafka Engine tables with 4 consumers each of them has its own insert thread. This option is good for large Kafka topics with millions of messages per second.

## Multiple Materialized Views

Attaching multiple Materialized Views (MVs) to a Kafka Engine table can be used when you need to apply different transformations to the same topic and store the resulting data in different tables.

(This approach also applies to the other streaming engines \- RabbitMQ, s3queue, etc).

All streaming engines begin processing data (reading from the source and producing insert blocks) only after at least one Materialized View is attached to the engine. Multiple Materialized Views can be connected to distribute data across various tables with different transformations. But how does it work when the server starts?

Once the first Materialized View (MV) is loaded, started, and attached to the Kafka/s3queue table, data consumption begins immediately—data is read from the source, pushed to the destination, and the pointers advance to the next position. However, any other MVs that haven’t started yet will miss the data consumed by the first MV, leading to some data loss.

This issue worsens with asynchronous table loading. Tables are only loaded upon first access, and the loading process takes time. When multiple MVs direct the data stream to different tables, some tables might be ready sooner than others. As soon as the first table becomes ready, data consumption starts, and any tables still loading will miss the data consumed during that interval, resulting in further data loss for those tables.

That means when you make a design with Multiple MVs `async_load_databases` should be switched off:


```
<async_load_databases>false</async_load_databases>

```
Also, you have to prevent starting to consume until all MVs are loaded and started. For that, you can add an additional Null table to the MV pipeline, so the Kafka table will pass the block to a single Null table first, and only then many MVs start their own transformations to many dest tables:

KafkaTable → dummy\_MV \-\> NullTable \-\> \[MV1, MV2, ….] → \[Table1, Table2, …]


```
create table NullTable Engine=Null as KafkaTable;
create materialized view dummy_MV to NullTable
select * from KafkaTable
--WHERE NOT ignore(throwIf(if((uptime() < 120), 1 , 0)))
WHERE NOT ignore(throwIf(if((uptime() < 120), 1 + sleep(3), 0)))

```
120 seconds should be enough for loading all MVs.

Using an intermediate Null table is also preferable because it’s easier to make any changes with MVs:

- drop the dummy\_MV to stop consuming
- make any changes to transforming MVs by drop/recreate
- create dummy\_MV again to resume consuming

The fix for correctly starting multiple MVs will be available from 25\.5 version \- <https://github.com/ClickHouse/ClickHouse/pull/72123>

# 2\.4 \- Rewind / fast\-forward / replay

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

# 3 \- Schema and Formats

Schema inference and format\-specific integration details.# 3\.1 \- Inferring Schema from AvroConfluent Messages in Kafka for ClickHouse®

Learn how to define Kafka table structures in ClickHouse® by using Avro’s schema registry \& sample message.To consume messages from Kafka within ClickHouse®, you need to define the `ENGINE=Kafka` table structure with all the column names and types.
This task can be particularly challenging when dealing with complex Avro messages, as manually determining the exact schema for
ClickHouse is both tricky and time\-consuming. This complexity is particularly frustrating in the case of Avro formats,
where the column names and their types are already clearly defined in the schema registry.

Although ClickHouse supports schema inference for files, it does not natively support this for Kafka streams.

Here’s a workaround to infer the schema using AvroConfluent messages:

## Step 1: Capture and Store a Raw Kafka Message

First, create a table in ClickHouse to consume a raw message from Kafka and store it as a file:


```
CREATE TABLE test_kafka (raw String) ENGINE = Kafka 
SETTINGS kafka_broker_list = 'localhost:29092', 
         kafka_topic_list = 'movies-raw', 
         kafka_format = 'RawBLOB', -- Don't try to parse the message, return it 'as is'
         kafka_group_name = 'tmp_test'; -- Using some dummy consumer group here.

INSERT INTO FUNCTION file('./avro_raw_sample.avro', 'RawBLOB') 
SELECT * FROM test_kafka LIMIT 1 
SETTINGS max_block_size=1, stream_like_engine_allow_direct_select=1;

DROP TABLE test_kafka;

```
## Step 2: Infer Schema Using the Stored File

Using the stored raw message, let ClickHouse infer the schema based on the AvroConfluent format and a specified schema registry URL:


```
CREATE TEMPORARY TABLE test AS 
SELECT * FROM file('./avro_raw_sample.avro', 'AvroConfluent') 
SETTINGS format_avro_schema_registry_url='http://localhost:8085';

SHOW CREATE TEMPORARY TABLE test\G;

```
The output from the `SHOW CREATE` command will display the inferred schema, for example:


```
Row 1:
──────
statement: CREATE TEMPORARY TABLE test
(
    `movie_id` Int64,
    `title` String,
    `release_year` Int64
)
ENGINE = Memory

```
## Step 3: Create the Kafka Table with the Inferred Schema

Now, use the inferred schema to create the Kafka table:


```
CREATE TABLE movies_kafka
(
    `movie_id` Int64,
    `title` String,
    `release_year` Int64
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'localhost:29092',
         kafka_topic_list = 'movies-raw',
         kafka_format = 'AvroConfluent',
         kafka_group_name = 'movies',
         kafka_schema_registry_url = 'http://localhost:8085';

```
This approach reduces manual schema definition efforts and enhances data integration workflows by utilizing the schema inference capabilities of ClickHouse for AvroConfluent messages.

## Appendix

**Avro** is a binary serialization format used within Apache Kafka for efficiently serializing data with a compact binary format. It relies on schemas, which define the structure of the serialized data, to ensure robust data compatibility and type safety.

**Schema Registry** is a service that provides a centralized repository for Avro schemas. It helps manage and enforce schemas across applications, ensuring that the data exchanged between producers and consumers adheres to a predefined format, and facilitates schema evolution in a safe manner.

In ClickHouse, the **Avro** format is used for data that contains the schema embedded directly within the file or message. This means the structure of the data is defined and included with the data itself, allowing for self\-describing messages. However, embedding the schema within every message is not optimal for streaming large volumes of data, as it increases the workload and network overhead. Repeatedly passing the same schema with each message can be inefficient, particularly in high\-throughput environments.

On the other hand, the **AvroConfluent** format in ClickHouse is specifically designed to work with the Confluent Schema Registry. This format expects the schema to be managed externally in a schema registry rather than being embedded within each message. It retrieves schema information from the Schema Registry, which allows for centralized schema management and versioning, facilitating easier schema evolution and enforcement across different applications using Kafka.

# 4 \- Operations and Troubleshooting

Runtime tuning, resource settings, and error diagnostics.# 4\.1 \- Setting the background message broker schedule pool size

Guide to managing the `background_message_broker_schedule_pool_size` setting for Kafka, RabbitMQ, and NATS table engines in your database.## Overview

When using Kafka, RabbitMQ, or NATS table engines in ClickHouse®, you may encounter issues related to a saturated background thread pool. One common symptom is a warning similar to the following:


```
2025.03.14 08:44:26.725868 [ 344 ] {} <Warning> StorageKafka (events_kafka): [rdk:MAXPOLL] [thrd:main]: Application maximum poll interval (60000ms) exceeded by 159ms (adjust max.poll.interval.ms for long-running message processing): leaving group

```
This warning typically appears **not because ClickHouse fails to poll**, but because **there are no available threads** in the background pool to handle the polling in time. In rare cases, the same error might also be caused by long flushing operations to Materialized Views (MVs), especially if their logic is complex or chained.

To resolve this, you should monitor and, if needed, increase the value of the `background_message_broker_schedule_pool_size` setting.



---

## Step 1: Check Thread Pool Utilization

Run the following SQL query to inspect the current status of your background message broker thread pool:


```
SELECT
    (
        SELECT value
        FROM system.metrics
        WHERE metric = 'BackgroundMessageBrokerSchedulePoolTask'
    ) AS tasks,
    (
        SELECT value
        FROM system.metrics
        WHERE metric = 'BackgroundMessageBrokerSchedulePoolSize'
    ) AS pool_size,
    pool_size - tasks AS free_threads

```
If you have `metric_log` enabled, you can also monitor the **minimum number of free threads over the day**:


```
SELECT min(CurrentMetric_BackgroundMessageBrokerSchedulePoolSize - CurrentMetric_BackgroundMessageBrokerSchedulePoolTask) AS min_free_threads
FROM system.metric_log
WHERE event_date = today()

```
**If `free_threads` is close to zero or negative**, it means your thread pool is saturated and should be increased.



---

## Step 2: Estimate Required Pool Size

To estimate a reasonable value for `background_message_broker_schedule_pool_size`, run the following query:


```
WITH
    toUInt32OrDefault(extract(engine_full, 'kafka_num_consumers\s*=\s*(\d+)')) as kafka_num_consumers,
    extract(engine_full, 'kafka_thread_per_consumer\s*=\s*(\d+|\'true\')') not in ('', '0') as kafka_thread_per_consumer,
    multiIf(
        engine = 'Kafka',  
            if(kafka_thread_per_consumer AND kafka_num_consumers > 0, kafka_num_consumers, 1),
        engine = 'RabbitMQ',
            3,
        engine = 'NATS',
            3,
        0 /* should not happen */
    ) as threads_needed
SELECT 
    ceil(sum(threads_needed) * 1.25)
FROM 
    system.tables
WHERE 
    engine in ('Kafka', 'RabbitMQ', 'NATS')

```
This will return an estimate that includes a 25% buffer to accommodate spikes in load.



---

## Step 3: Apply the New Setting

1. **Create or update** the following configuration file:

**Path:** `/etc/clickhouse-server/config.d/background_message_broker_schedule_pool_size.xml`

**Content:**


```
<yandex>
    <background_message_broker_schedule_pool_size>120</background_message_broker_schedule_pool_size>
</yandex>

```
Replace `120` with the value recommended from Step 2 (rounded up if needed).
2. **(Only for ClickHouse versions 23\.8 and older)**

Add the same setting to the default user profile:

**Path:** `/etc/clickhouse-server/users.d/background_message_broker_schedule_pool_size.xml`

**Content:**


```
<yandex>
    <profiles>
        <default>
            <background_message_broker_schedule_pool_size>120</background_message_broker_schedule_pool_size>
        </default>
    </profiles>
</yandex>

```



---

## Step 4: Restart ClickHouse

After applying the configuration, restart ClickHouse to apply the changes:


```
sudo systemctl restart clickhouse-server

```


---

## Summary

A saturated background message broker thread pool can lead to missed Kafka polls and consumer group dropouts. Monitoring your metrics and adjusting `background_message_broker_schedule_pool_size` accordingly ensures stable operation of Kafka, RabbitMQ, and NATS integrations.

If the problem persists even after increasing the pool size, consider investigating slow MV chains or flushing logic as a potential bottleneck.

# 4\.2 \- Error handling

Error handling## Pre 21\.6

There are couple options:

Certain formats which has schema in built in them (like JSONEachRow) could silently skip any unexpected fields after enabling setting `input_format_skip_unknown_fields`

It’s also possible to skip up to N malformed messages for each block, with used setting `kafka_skip_broken_messages` but it’s also does not support all possible formats.

## After 21\.6

It’s possible to stream messages which could not be parsed, this behavior could be enabled via setting: `kafka_handle_error_mode='stream'` and ClickHouse® wil write error and message from Kafka itself to two new virtual columns: `_error, _raw_message`.

So you can create another Materialized View which would collect to a separate table all errors happening while parsing with all important information like offset and content of message.


```
CREATE TABLE default.kafka_engine
(
    `i` Int64,
    `s` String
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:9092'
kafka_topic_list = 'topic',
kafka_group_name = 'clickhouse',
kafka_format = 'JSONEachRow',
kafka_handle_error_mode='stream';

CREATE TABLE default.kafka_errors
(
    `topic` String,
    `partition` Int64,
    `offset` Int64,
    `raw` String,
    `error` String
)
ENGINE = MergeTree
ORDER BY (topic, partition, offset)
SETTINGS index_granularity = 8192


CREATE MATERIALIZED VIEW default.kafka_errors_mv TO default.kafka_errors
AS
SELECT
    _topic AS topic,
    _partition AS partition,
    _offset AS offset,
    _raw_message AS raw,
    _error AS error
FROM default.kafka_engine
WHERE length(_error) > 0

```
<https://github.com/ClickHouse/ClickHouse/pull/20249>

<https://github.com/ClickHouse/ClickHouse/pull/21850>

[https://altinity.com/blog/clickhouse\-kafka\-engine\-faq](https://altinity.com/blog/clickhouse-kafka-engine-faq)

## Since 25\.8

dead letter queue can be used via setting: `kafka_handle_error_mode='dead_letter_queue'` <https://github.com/ClickHouse/ClickHouse/pull/68873>

and error related data will be saved in `system.dead_letter_queue` table.

![Table connections](/assets/Untitled-2021-08-05-1027.png)
