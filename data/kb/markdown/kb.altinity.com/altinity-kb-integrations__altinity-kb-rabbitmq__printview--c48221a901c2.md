# RabbitMQ \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-integrations/altinity-kb-rabbitmq/).

# RabbitMQ

RabbitMQ engine in ClickHouse® 24\.3\+- 1: [RabbitMQ Error handling](#pg-98ba8cfef289db7021da328f13e65d9e)

### Settings

Basic RabbitMQ settings and use cases: [https://clickhouse.com/docs/en/engines/table\-engines/integrations/rabbitmq](https://clickhouse.com/docs/en/engines/table-engines/integrations/rabbitmq)

### Latest improvements/fixes

##### (v23\.10\+)

- **Allow to save unparsed records and errors in RabbitMQ**:
NATS and FileLog engines. Add virtual columns `_error` and `_raw_message` (for NATS and RabbitMQ), `_raw_record` (for FileLog) that are filled when ClickHouse fails to parse new record.
The behaviour is controlled under storage settings `nats_handle_error_mode` for NATS, `rabbitmq_handle_error_mode` for RabbitMQ, `handle_error_mode` for FileLog similar to `kafka_handle_error_mode`.
If it’s set to `default`, en exception will be thrown when ClickHouse fails to parse a record, if it’s set to `stream`, error and raw record will be saved into virtual columns.
Closes [\#36035](https://github.com/ClickHouse/ClickHouse/issues/36035)
and [\#55477](https://github.com/ClickHouse/ClickHouse/pull/55477)

##### (v24\+)

- [\#45350 RabbitMq Storage Engine should NACK messages if exception is thrown during processing](https://github.com/ClickHouse/ClickHouse/issues/45350)
- [\#59775 rabbitmq: fix having neither acked nor nacked messages](https://github.com/ClickHouse/ClickHouse/pull/59775)
- [\#60312 Make rabbitmq nack broken messages](https://github.com/ClickHouse/ClickHouse/pull/60312)
- [\#61320 Fix logical error in RabbitMQ storage with MATERIALIZED columns](https://github.com/ClickHouse/ClickHouse/pull/61320)
# 1 \- RabbitMQ Error handling

Error handling for RabbitMQ table engineSame approach as in Kafka but virtual columns are different. Check [https://clickhouse.com/docs/en/engines/table\-engines/integrations/rabbitmq\#virtual\-columns](https://clickhouse.com/docs/en/engines/table-engines/integrations/rabbitmq#virtual-columns)


```
CREATE TABLE IF NOT EXISTS rabbitmq.broker_errors_queue
(
  exchange_name String,
  channel_id String,
  delivery_tag UInt64,
  redelivered UInt8,
  message_id String,
  timestamp UInt64
)
engine = RabbitMQ
SETTINGS
    rabbitmq_host_port = 'localhost:5672',
    rabbitmq_exchange_name = 'exchange-test', -- required parameter even though this is done via the rabbitmq config
    rabbitmq_queue_consume = true,
    rabbitmq_queue_base = 'test-errors',
    rabbitmq_format = 'JSONEachRow',
    rabbitmq_username = 'guest',
    rabbitmq_password = 'guest',
    rabbitmq_handle_error_mode = 'stream';

CREATE MATERIALIZED VIEW IF NOT EXISTS rabbitmq.broker_errors_mv
(
  exchange_name String,
  channel_id String,
  delivery_tag UInt64,
  redelivered UInt8,
  message_id String,
  timestamp UInt64
  raw_message String,
  error String
)
ENGINE = MergeTree
ORDER BY (error)
SETTINGS index_granularity = 8192 AS
SELECT
  _exchange_name AS exchange_name,
  _channel_id AS channel_id,
  _delivery_tag AS delivery_tag,
  _redelivered AS redelivered,
  _message_id AS message_id,
  _timestamp AS timestamp,
  _raw_message AS raw_message,
  _error AS error
FROM rabbitmq.broker_errors_queue
WHERE length(_error) > 0

```
