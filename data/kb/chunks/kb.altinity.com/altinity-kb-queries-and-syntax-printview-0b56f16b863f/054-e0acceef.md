---
source: kb.altinity.com
url: https://github.com/ClickHouse/ClickHouse/blob/8ab5270ded39c8b044f60f73c1de00c8117ab8f2/src/Interpreters/Aggregator.cpp#L382
topic: queries-syntax-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '8.888'
last_updated: '2026-06-12'
chunk_index: 54
total_chunks_in_doc: 117
---

2021-04-29 00:00:00 │ 2 │ │ 2021-04-30 00:00:00 │ 3 │ │ 2021-05-01 00:00:00 │ 4 │ │ 2021-05-02 00:00:00 │ 5 │ │ 2021-05-03 00:00:00 │ 7 │ └─────────────────────┴──────┘ ``` ## Using runningAccumulate (incorrect result over blocks)

```
SELECT
    ts,
    runningAccumulate(state) AS uniq
FROM
(
    SELECT
        toStartOfDay(ts) AS ts,
        uniqExactState(user_id) AS state
    FROM events
    GROUP BY ts
    ORDER BY ts ASC
)
ORDER BY ts ASC

┌──────────────────ts─┬─uniq─┐
│ 2021-04-29 00:00:00 │    2 │
│ 2021-04-30 00:00:00 │    3 │
│ 2021-05-01 00:00:00 │    4 │
│ 2021-05-02 00:00:00 │    5 │
│ 2021-05-03 00:00:00 │    7 │
└─────────────────────┴──────┘

```
# 18 \- Data types on disk and in RAM

Data types on disk and in RAM

| DataType | RAM size (\=byteSize) | Disk Size |
| --- | --- | --- |
| String | string byte length \+ 9string length: 64 bit integerzero\-byte terminator: 1 byte. | string length prefix (varint) \+ string itself:string shorter than 128 \- string byte length \+ 1string shorter than 16384 \- string byte length \+ 2string shorter than 2097152 \- string byte length \+ 2string shorter than 268435456 \- string byte length \+ 4 |
| AggregateFunction(count, ...) |  | varint |

See also the presentation [Data processing into ClickHouse®](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup41/data_processing.pdf)
, especially slides 17\-22\.

# 19 \- DELETE via tombstone column

DELETE via tombstone columnThis article provides an overview of the different methods to handle row deletion in ClickHouse, using tombstone columns and ALTER UPDATE or DELETE. The goal is to highlight the performance impacts of different techniques and storage settings, including a scenario using S3 for remote storage.

1. Creating a Test Table
We will start by creating a simple MergeTree table with a tombstone column (is\_active) to track active rows:

```
CREATE TABLE test_delete
(
    `key` UInt32,
    `ts` UInt32,
    `value_a` String,
    `value_b` String,
    `value_c` String,
    `is_active` UInt8 DEFAULT 1
)
ENGINE = MergeTree
ORDER BY key;

```
2. Inserting Data
Insert sample data into the table:

```
INSERT INTO test_delete (key, ts, value_a, value_b, value_c) SELECT
    number,
    1,
    concat('some_looong_string', toString(number)),
    concat('another_long_str', toString(number)),
    concat('string', toString(number))
FROM numbers(10000000);


INSERT INTO test_delete (key, ts, value_a, value_b, value_c) VALUES (400000, 2, 'totally different string', 'another totally different string', 'last string');

```
3. Querying the Data
To verify the inserted data:
