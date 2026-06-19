# RabbitMQ Error handling \| Altinity® Knowledge Base for ClickHouse®


1. [Integrations](/altinity-kb-integrations/)
2. [RabbitMQ](/altinity-kb-integrations/altinity-kb-rabbitmq/)
3. RabbitMQ Error handling
# RabbitMQ Error handling

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
Last modified 2024\.08\.29: [Added RabbitMQ error handling and info (d9d304b)](https://github.com/Altinity/altinityknowledgebase/commit/d9d304b8d485cbedcffaa512dc07d8f07ca56726)
