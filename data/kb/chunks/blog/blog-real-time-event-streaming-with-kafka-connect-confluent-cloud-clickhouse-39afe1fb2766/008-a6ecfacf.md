---
source: blog
url: https://clickhouse.cloud/signUp?loc=blog-cta-header&utm_source=clickhouse&utm_medium=web&utm_campaign=blog
topic: real-time-event-streaming-with-clickhouse-kafka-connect-and-confluent-cloud
ch_version_introduced: '0.025'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 14
---

`timestamp` DateTime CODEC(Delta(4), ZSTD(1)), `transaction_count` UInt16, `base_fee_per_gas` UInt64, `withdrawals_root` String, `withdrawals` Nested(index Int64, validator_index Int64, address String, amount String) ) ENGINE = MergeTree ORDER BY timestamp ``` Equivalent schemas for the other data types can be found [here](https://github.com/ClickHouse/examples/tree/main/ethereum/streaming/schemas)

This above schema is alittle different than the schema proposed in our [earlier blog post](https://clickhouse.com/blog/clickhouse-bigquery-migrating-data-for-realtime-queries), with the columns `withdrawals_root` and `withdrawals` recently added to the specification[\[1]\[2]](https://ethereum.org/en/staking/withdrawals). We also set the setting `flatten_nested` to `0` to preserve the Nested structure of the `withdrawals` column. This allows us to insert this column as a nested JSON structure.

Below we show a message as held on the Kafka topic `block_messages`.

```
{
  "MessageData": "{\"type\": \"block\", \"number\": 17477635, \"hash\": \"0x6c0e971090f48adfc04303b302e5f14895c104e9a60ec6126b96579194a2c14b\", \"parent_hash\": \"0xdf90825e84c50550be12143d998090883bb92deecbdb5bd84235023f8fcad9c5\", \"nonce\": \"0x0000000000000000\", \"sha3_uncles\": \"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347\", \"logs_bloom\": \"0xc0210585c002844400c000f0a011e324186195244041200041031242148ec051808106400d3030600c384180050003c20a41078488403c3022880000147ea8a348110c0ad50001086800430b83d120e89010000024445881003000848023a010562881021302a60118003c19400c099206904e7008b104301214001042fc007608271140460524a0904e3142174c250174070921a90006686244236043b080468f90b161e00364a20a8b48b15cb205a50c44082cc100040b02812017008c016501800162115c06022539a2401c0ef20020680a00002c201c0010c8920210a0000895a11c0a1844860a00208045810604a0301013015ea86219aa98831e027440\", \"transactions_root\": \"0xefaf112480278167af853214fc55a7fcaff4a879c1e97357be77d95fd114c046\", \"state_root\": \"0x2b5fa13bcecb133578e5e6c328944a551ccb497275ba4263d5b52d9f88bab2e1\", \"receipts_root\": \"0x2ef3cb89ab21d6d861777087ee1791c5a6197d5b6e9f8e0228717b064ad60efe\", \"miner\": \"0xbaf6dc2e647aeb6f510f9e318856a1bcd66c5e19\", \"difficulty\": 0, \"total_difficulty\": 58750003716598352816469, \"size\": 38091, \"extra_data\": \"0x4d616465206f6e20746865206d6f6f6e20627920426c6f636b6e6174697665\", \"gas_limit\": 30000000, \"gas_used\": 6452970, \"timestamp\": 1686739043, \"transaction_count\": 83, \"base_fee_per_gas\": 14420785730, \"withdrawals_root\": \"0x71fbe84200d685e619f28a7f3aedfcacadf5f8bde9be2c20f9d146110f66e558\", \"withdrawals\": [{\"index\": 7083728, \"validator_index\": 649036, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13657565}, {\"index\": 7083729, \"validator_index\": 649037, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13749238}, {\"index\": 7083730, \"validator_index\": 649038, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13636849}, {\"index\": 7083731, \"validator_index\": 649039, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13700532}, {\"index\": 7083732, \"validator_index\": 649040, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13647987}, {\"index\": 7083733, \"validator_index\": 649041, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13712208}, {\"index\": 7083734, \"validator_index\": 649042, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13748808}, {\"index\": 7083735, \"validator_index\": 649043, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13720541}, {\"index\": 7083736, \"validator_index\": 649044, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 49166908}, {\"index\": 7083737, \"validator_index\": 649045, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13747911}, {\"index\": 7083738, \"validator_index\": 649046, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13701501}, {\"index\": 7083739, \"validator_index\": 649047, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13695932}, {\"index\": 7083740, \"validator_index\": 649048, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13708868}, {\"index\": 7083741, \"validator_index\": 649049, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13676192}, {\"index\": 7083742, \"validator_index\": 649050, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13594476}, {\"index\": 7083743, \"validator_index\": 649051, \"address\": \"0x07fac54a901409fe10e56c899be3dcf2471ae321\", \"amount\": 13716126}], \"item_id\": \"block_0x6c0e971090f48adfc04303b302e5f14895c104e9a60ec6126b96579194a2c14b\", \"item_timestamp\": \"2023-06-14T10:37:23Z\"}",
  "AttributesMap": {
    "item_id": "block_0x6c0e971090f48adfc04303b302e5f14895c104e9a60ec6126b96579194a2c14b",
    "item_timestamp": "2023-06-13T18:44:47Z"
  }
}

```

The main body is held in the `MessageData` field as an escaped JSON string. This format is incompatible with the above schema and requires transformation before insertion. For this, we use a materialized view.

### Transforming messages with materialized views [\#](/blog/real-time-event-streaming-with-kafka-connect-confluent-cloud-clickhouse#transforming-messages-with-materialized-views)

Materialized views in ClickHouse can be used to transform rows at insert time. The view triggers at insert time for a table receiving blocks of rows, performing a SELECT operation over the block with the results sent to a target table.
