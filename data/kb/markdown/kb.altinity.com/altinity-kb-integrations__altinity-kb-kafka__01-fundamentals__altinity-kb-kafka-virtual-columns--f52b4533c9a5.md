# Kafka engine Virtual columns \| Altinity® Knowledge Base for ClickHouse®


1. [Integrations](/altinity-kb-integrations/)
2. [Kafka engine](/altinity-kb-integrations/altinity-kb-kafka/)
3. [Fundamentals](/altinity-kb-integrations/altinity-kb-kafka/01-fundamentals/)
4. Kafka virtual columns
# Kafka engine Virtual columns

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

Last modified 2026\.03\.12: [Restructure Kafka KB sections and refresh named\-collection guidance (fde5b9e)](https://github.com/Altinity/altinityknowledgebase/commit/fde5b9e9f6579a89f6b9ec2f41821d880733aacb)
