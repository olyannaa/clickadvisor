# TTL \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-queries-and-syntax/ttl/).

# TTL

TTL- 1: [MODIFY (ADD) TTL in ClickHouse®](#pg-aa8d2fd51f7ff30c8a7186980faa36c8)
- 2: [What are my TTL settings?](#pg-999e491b8ff27fc2a84fb0b542e2a0fc)
- 3: [TTL GROUP BY Examples](#pg-aa7585e74ad5fc4d1296e47a4fea8470)
- 4: [TTL Recompress example](#pg-62f8acba4b7f1d56232694670e018078)

# 1 \- MODIFY (ADD) TTL in ClickHouse®

What happens during a MODIFY or ADD TTL query*For a general overview of TTL, see the article [Putting Things Where They Belong Using New TTL Moves](https://altinity.com/blog/2020-3-23-putting-things-where-they-belong-using-new-ttl-moves)
.*

## ALTER TABLE tbl MODIFY (ADD) TTL:

It’s 2 step process:

1. `ALTER TABLE tbl MODIFY (ADD) TTL ...`

Update table metadata: schema .sql \& metadata in ZK.
It’s usually cheap and fast command. And any new INSERT after schema change will calculate TTL according to new rule.

2. `ALTER TABLE tbl MATERIALIZE TTL`

Recalculate TTL for already exist parts.
It can be heavy operation, because ClickHouse® will read column data \& recalculate TTL \& apply TTL expression.
You can disable this step completely by using `materialize_ttl_after_modify` user session setting (by default it’s 1, so materialization is enabled).


```
SET materialize_ttl_after_modify=0;
ALTER TABLE tbl MODIFY TTL

```
If you will disable materialization of TTL, it does mean that all old parts will be transformed according OLD TTL rules.
MATERIALIZE TTL:

1. Recalculate TTL (Kinda cheap, it read only column participate in TTL)
2. Apply TTL (Rewrite of table data for all columns)

You also can only disable apply TTL substep via `materialize_ttl_recalculate_only` merge\_tree setting (by default it’s 0, so clickhouse will apply TTL expression)


```
ALTER TABLE tbl MODIFY SETTING materialize_ttl_recalculate_only=1;

```
It does mean, that TTL rule will not be applied during `ALTER TABLE tbl MODIFY (ADD) TTL ...` query and data is now going to be rewritten.

After this you can apply TTL (MATERIALIZE) per partition manually (which will apply the TTL and rewrite data)


```
ALTER TABLE tbl MATERIALIZE TTL [IN PARTITION partition | IN PARTITION ID 'partition_id'];

```
The idea of `materialize_ttl_after_modify = 0` and `materialize_ttl_recalculate_only = 1` is to use `ALTER TABLE tbl MATERIALIZE TTL IN PARTITION xxx; ALTER TABLE tbl MATERIALIZE TTL IN PARTITION yyy;` and materialize TTL gently or drop/move partitions manually until the old data without/old TTL is processed.

MATERIALIZE TTL done via Mutation:

1. ClickHouse create new parts via hardlinks and write new ttl.txt file
2. ClickHouse remove old(inactive) parts after remove time (default is 8 minutes)

To stop materialization of TTL:


```
SELECT * FROM system.mutations WHERE is_done=0 AND table = 'tbl';
KILL MUTATION WHERE command LIKE '%MATERIALIZE TTL%' AND table = 'tbl'

```
### MODIFY TTL MOVE

today: 2022\-06\-02

Table tbl

Daily partitioning by toYYYYMMDD(timestamp) \-\> 20220602

#### Increase of TTL

TTL timestamp \+ INTERVAL 30 DAY MOVE TO DISK s3 \-\> TTL timestamp \+ INTERVAL 60 DAY MOVE TO DISK s3

- Idea: ClickHouse need to move data from s3 to local disk BACK
- Actual: There is no rule that data earlier than 60 DAY **should be** on local disk

Table parts:


```
20220401    ttl: 20220501       disk: s3
20220416    ttl: 20220516       disk: s3
20220501    ttl: 20220531       disk: s3
20220502    ttl: 20220601       disk: local
20220516    ttl: 20220616       disk: local
20220601    ttl: 20220631       disk: local

```

```
ALTER TABLE tbl MODIFY TTL timestamp + INTERVAL 60 DAY MOVE TO DISK s3;

```
Table parts:


```
20220401    ttl: 20220601       disk: s3
20220416    ttl: 20220616       disk: s3
20220501    ttl: 20220631       disk: s3        (ClickHouse will not move this part to local disk, because there is no TTL rule for that)
20220502    ttl: 20220701       disk: local
20220516    ttl: 20220716       disk: local
20220601    ttl: 20220731       disk: local

```
#### Decrease of TTL

TTL timestamp \+ INTERVAL 30 DAY MOVE TO DISK s3 \-\> TTL timestamp \+ INTERVAL 14 DAY MOVE TO DISK s3

Table parts:


```
20220401    ttl: 20220401       disk: s3
20220416    ttl: 20220516       disk: s3
20220501    ttl: 20220531       disk: s3        
20220502    ttl: 20220601       disk: local     
20220516    ttl: 20220616       disk: local
20220601    ttl: 20220631       disk: local

```

```
ALTER TABLE tbl MODIFY TTL timestamp + INTERVAL 14 DAY MOVE TO DISK s3;

```
Table parts:


```
20220401    ttl: 20220415       disk: s3
20220416    ttl: 20220501       disk: s3
20220501    ttl: 20220515       disk: s3
20220502    ttl: 20220517       disk: local     (ClickHouse will move this part to disk s3 in background according to TTL rule)
20220516    ttl: 20220601       disk: local     (ClickHouse will move this part to disk s3 in background according to TTL rule)
20220601    ttl: 20220616       disk: local

```
### Possible TTL Rules

TTL:


```
DELETE          (With enabled `ttl_only_drop_parts`, it's cheap operation, ClickHouse will drop the whole part)
MOVE
GROUP BY
WHERE
RECOMPRESS

```
Related settings:

Server settings:


```
background_move_processing_pool_thread_sleep_seconds                        |   10      |
background_move_processing_pool_thread_sleep_seconds_random_part            |   1.0     |
background_move_processing_pool_thread_sleep_seconds_if_nothing_to_do       |   0.1     |
background_move_processing_pool_task_sleep_seconds_when_no_work_min         |   10      |
background_move_processing_pool_task_sleep_seconds_when_no_work_max         |   600     |
background_move_processing_pool_task_sleep_seconds_when_no_work_multiplier  |   1.1     |
background_move_processing_pool_task_sleep_seconds_when_no_work_random_part |   1.0     |

```
MergeTree settings:


```
merge_with_ttl_timeout                      │   14400   │       0 │ Minimal time in seconds, when merge with delete TTL can be repeated.
merge_with_recompression_ttl_timeout        │   14400   │       0 │ Minimal time in seconds, when merge with recompression TTL can be repeated.
max_replicated_merges_with_ttl_in_queue     │   1       │       0 │ How many tasks of merging parts with TTL are allowed simultaneously in ReplicatedMergeTree queue.
max_number_of_merges_with_ttl_in_pool       │   2       │       0 │ When there is more than specified number of merges with TTL entries in pool, do not assign new merge with TTL. This is to leave free threads for regular merges and avoid "Too many parts"
ttl_only_drop_parts                         │   0       │       0 │ Only drop altogether the expired parts and not partially prune them.

```
Session settings:


```
materialize_ttl_after_modify                │   1       │       0 │ Apply TTL for old data, after ALTER MODIFY TTL query 

```
# 2 \- What are my TTL settings?

What are my TTL settings?## Using `SHOW CREATE TABLE`

If you just want to see the current TTL settings on a table, you can look at the schema definition.


```
SHOW CREATE TABLE events2_local
FORMAT Vertical

Query id: eba671e5-6b8c-4a81-a4d8-3e21e39fb76b

Row 1:
──────
statement: CREATE TABLE default.events2_local
(
    `EventDate` DateTime,
    `EventID` UInt32,
    `Value` String
)
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/default/events2_local', '{replica}')
PARTITION BY toYYYYMM(EventDate)
ORDER BY (EventID, EventDate)
TTL EventDate + toIntervalMonth(1)
SETTINGS index_granularity = 8192

```
This works even when there’s no data in the table. It does not tell you when the TTLs expire or anything specific to data in one or more of the table parts.

## Using system.parts

If you want to see the actually TTL values for specific data, run a query on system.parts.
There are columns listing all currently applicable TTL limits for each part.
(It does not work if the table is empty because there aren’t any parts yet.)


```
SELECT *
FROM system.parts
WHERE (database = 'default') AND (table = 'events2_local')
FORMAT Vertical

Query id: 59106476-210f-4397-b843-9920745b6200

Row 1:
──────
partition:                             202203
name:                                  202203_0_0_0
...
database:                              default
table:                                 events2_local
...
delete_ttl_info_min:                   2022-04-27 21:26:30
delete_ttl_info_max:                   2022-04-27 21:26:30
move_ttl_info.expression:              []
move_ttl_info.min:                     []
move_ttl_info.max:                     []
default_compression_codec:             LZ4
recompression_ttl_info.expression:     []
recompression_ttl_info.min:            []
recompression_ttl_info.max:            []
group_by_ttl_info.expression:          []
group_by_ttl_info.min:                 []
group_by_ttl_info.max:                 []
rows_where_ttl_info.expression:        []
rows_where_ttl_info.min:               []
rows_where_ttl_info.max:               []

```
# 3 \- TTL GROUP BY Examples

TTL GROUP BY Examples### Example with MergeTree table


```
CREATE TABLE test_ttl_group_by
(
    `key` UInt32,
    `ts` DateTime,
    `value` UInt32,
    `min_value` UInt32 DEFAULT value,
    `max_value` UInt32 DEFAULT value
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (key, toStartOfDay(ts))
TTL ts + interval 30 day 
    GROUP BY key, toStartOfDay(ts) 
    SET value = sum(value), 
    min_value = min(min_value), 
    max_value = max(max_value), 
    ts = min(toStartOfDay(ts));

```
During TTL merges ClickHouse® re\-calculates values of columns in the SET section.

GROUP BY section should be a prefix of a table’s PRIMARY KEY (the same as ORDER BY, if no separate PRIMARY KEY defined).


```
-- stop merges to demonstrate data before / after 
-- a rolling up
SYSTEM STOP TTL MERGES test_ttl_group_by;
SYSTEM STOP MERGES test_ttl_group_by;

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() + number,
    1
FROM numbers(100);

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() - interval 60 day + number,
    2
FROM numbers(100);

SELECT
    toYYYYMM(ts) AS m,
    count(),
    sum(value),
    min(min_value),
    max(max_value)
FROM test_ttl_group_by
GROUP BY m;
┌──────m─┬─count()─┬─sum(value)─┬─min(min_value)─┬─max(max_value)─┐
│ 202102 │     100 │        200 │              2 │              2 │
│ 202104 │     100 │        100 │              1 │              1 │
└────────┴─────────┴────────────┴────────────────┴────────────────┘

SYSTEM START TTL MERGES test_ttl_group_by;
SYSTEM START MERGES test_ttl_group_by;
OPTIMIZE TABLE test_ttl_group_by FINAL;

SELECT
    toYYYYMM(ts) AS m,
    count(),
    sum(value),
    min(min_value),
    max(max_value)
FROM test_ttl_group_by
GROUP BY m;
┌──────m─┬─count()─┬─sum(value)─┬─min(min_value)─┬─max(max_value)─┐
│ 202102 │       5 │        200 │              2 │              2 │
│ 202104 │     100 │        100 │              1 │              1 │
└────────┴─────────┴────────────┴────────────────┴────────────────┘

```
As you can see 100 rows were rolled up into 5 rows (key has 5 values) for rows older than 30 days.

### Example with SummingMergeTree table


```
CREATE TABLE test_ttl_group_by
(
    `key1` UInt32,
    `key2` UInt32,
    `ts` DateTime,
    `value` UInt32,
    `min_value` SimpleAggregateFunction(min, UInt32) 
                                       DEFAULT value,
    `max_value` SimpleAggregateFunction(max, UInt32) 
                                       DEFAULT value
)
ENGINE = SummingMergeTree
PARTITION BY toYYYYMM(ts)
PRIMARY KEY (key1, key2, toStartOfDay(ts))
ORDER BY (key1, key2, toStartOfDay(ts), ts)
TTL ts + interval 30 day 
    GROUP BY key1, key2, toStartOfDay(ts) 
    SET value = sum(value), 
    min_value = min(min_value), 
    max_value = max(max_value), 
    ts = min(toStartOfDay(ts));

-- stop merges to demonstrate data before / after 
-- a rolling up
SYSTEM STOP TTL MERGES test_ttl_group_by;
SYSTEM STOP MERGES test_ttl_group_by;

INSERT INTO test_ttl_group_by (key1, key2, ts, value)
SELECT
    1,
    1,
    toStartOfMinute(now() + number*60),
    1
FROM numbers(100);

INSERT INTO test_ttl_group_by (key1, key2, ts, value)
SELECT
    1,
    1,
    toStartOfMinute(now() + number*60),
    1
FROM numbers(100);

INSERT INTO test_ttl_group_by (key1, key2, ts, value)
SELECT
    1,
    1,
    toStartOfMinute(now() + number*60 - toIntervalDay(60)),
    2
FROM numbers(100);

INSERT INTO test_ttl_group_by (key1, key2, ts, value)
SELECT
    1,
    1,
    toStartOfMinute(now() + number*60 - toIntervalDay(60)),
    2
FROM numbers(100);

SELECT
    toYYYYMM(ts) AS m,
    count(),
    sum(value),
    min(min_value),
    max(max_value)
FROM test_ttl_group_by
GROUP BY m;

┌──────m─┬─count()─┬─sum(value)─┬─min(min_value)─┬─max(max_value)─┐
│ 202102 │     200 │        400 │              2 │              2 │
│ 202104 │     200 │        200 │              1 │              1 │
└────────┴─────────┴────────────┴────────────────┴────────────────┘

SYSTEM START TTL MERGES test_ttl_group_by;
SYSTEM START MERGES test_ttl_group_by;
OPTIMIZE TABLE test_ttl_group_by FINAL;

SELECT
    toYYYYMM(ts) AS m,
    count(),
    sum(value),
    min(min_value),
    max(max_value)
FROM test_ttl_group_by
GROUP BY m;

┌──────m─┬─count()─┬─sum(value)─┬─min(min_value)─┬─max(max_value)─┐
│ 202102 │       1 │        400 │              2 │              2 │
│ 202104 │     100 │        200 │              1 │              1 │
└────────┴─────────┴────────────┴────────────────┴────────────────┘

```
During merges ClickHouse re\-calculates **ts** columns as **min(toStartOfDay(ts))**. It’s possible **only for the last column** of `SummingMergeTree` `ORDER BY` section `ORDER BY (key1, key2, toStartOfDay(ts), ts)` otherwise it will **break** the order of rows in the table.

### Example with AggregatingMergeTree table


```
CREATE TABLE test_ttl_group_by_agg
(
    `key1` UInt32,
    `key2` UInt32,
    `ts` DateTime,
    `counter` AggregateFunction(count, UInt32)
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(ts)
PRIMARY KEY (key1, key2, toStartOfDay(ts))
ORDER BY (key1, key2, toStartOfDay(ts), ts)
TTL ts + interval 30 day 
    GROUP BY key1, key2, toStartOfDay(ts) 
    SET counter = countMergeState(counter),
    ts = min(toStartOfDay(ts));

CREATE TABLE test_ttl_group_by_raw
(
    `key1` UInt32,
    `key2` UInt32,
    `ts` DateTime
) ENGINE = Null;

CREATE MATERIALIZED VIEW test_ttl_group_by_mv
    TO test_ttl_group_by_agg
AS
SELECT
    `key1`,
    `key2`,
    `ts`,
    countState() as counter
FROM test_ttl_group_by_raw
GROUP BY key1, key2, ts;

-- stop merges to demonstrate data before / after 
-- a rolling up
SYSTEM STOP TTL MERGES test_ttl_group_by_agg;
SYSTEM STOP MERGES test_ttl_group_by_agg;

INSERT INTO test_ttl_group_by_raw (key1, key2, ts)
SELECT
    1,
    1,
    toStartOfMinute(now() + number*60)
FROM numbers(100);

INSERT INTO test_ttl_group_by_raw (key1, key2, ts)
SELECT
    1,
    1,
    toStartOfMinute(now() + number*60)
FROM numbers(100);

INSERT INTO test_ttl_group_by_raw (key1, key2, ts)
SELECT
    1,
    1,
    toStartOfMinute(now() + number*60 - toIntervalDay(60))
FROM numbers(100);

INSERT INTO test_ttl_group_by_raw (key1, key2, ts)
SELECT
    1,
    1,
    toStartOfMinute(now() + number*60 - toIntervalDay(60))
FROM numbers(100);

SELECT
    toYYYYMM(ts) AS m,
    count(),
    countMerge(counter)
FROM test_ttl_group_by_agg
GROUP BY m;

┌──────m─┬─count()─┬─countMerge(counter)─┐
│ 202307 │     200 │                 200 │
│ 202309 │     200 │                 200 │
└────────┴─────────┴─────────────────────┘

SYSTEM START TTL MERGES test_ttl_group_by_agg;
SYSTEM START MERGES test_ttl_group_by_agg;
OPTIMIZE TABLE test_ttl_group_by_agg FINAL;

SELECT
    toYYYYMM(ts) AS m,
    count(),
    countMerge(counter)
FROM test_ttl_group_by_agg
GROUP BY m;

┌──────m─┬─count()─┬─countMerge(counter)─┐
│ 202307 │       1 │                 200 │
│ 202309 │     100 │                 200 │
└────────┴─────────┴─────────────────────┘

```
### Multilevel TTL Group by


```
CREATE TABLE test_ttl_group_by
(
    `key` UInt32,
    `ts` DateTime,
    `value` UInt32,
    `min_value` UInt32 DEFAULT value,
    `max_value` UInt32 DEFAULT value
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (key, toStartOfWeek(ts), toStartOfDay(ts), toStartOfHour(ts))
TTL 
ts + interval 1 hour 
GROUP BY key, toStartOfWeek(ts), toStartOfDay(ts), toStartOfHour(ts) 
    SET value = sum(value), 
    min_value = min(min_value), 
    max_value = max(max_value), 
    ts = min(toStartOfHour(ts)),
ts + interval 1 day 
GROUP BY key, toStartOfWeek(ts), toStartOfDay(ts) 
    SET value = sum(value), 
    min_value = min(min_value), 
    max_value = max(max_value), 
    ts = min(toStartOfDay(ts)),
ts + interval 30 day 
GROUP BY key, toStartOfWeek(ts) 
    SET value = sum(value), 
    min_value = min(min_value), 
    max_value = max(max_value), 
    ts = min(toStartOfWeek(ts));
    
SYSTEM STOP TTL MERGES test_ttl_group_by;
SYSTEM STOP MERGES test_ttl_group_by;

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() + number,
    1
FROM numbers(100);

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() - interval 2 hour + number,
    2
FROM numbers(100);    

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() - interval 2 day + number,
    3
FROM numbers(100);    

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() - interval 2 month + number,
    4
FROM numbers(100); 

SELECT
    toYYYYMMDD(ts) AS d,
    count(),
    sum(value),
    min(min_value),
    max(max_value)
FROM test_ttl_group_by
GROUP BY d
ORDER BY d;

┌────────d─┬─count()─┬─sum(value)─┬─min(min_value)─┬─max(max_value)─┐
│ 20210616 │     100 │        400 │              4 │              4 │
│ 20210814 │     100 │        300 │              3 │              3 │
│ 20210816 │     200 │        300 │              1 │              2 │
└──────────┴─────────┴────────────┴────────────────┴────────────────┘

SYSTEM START TTL MERGES test_ttl_group_by;
SYSTEM START MERGES test_ttl_group_by;
OPTIMIZE TABLE test_ttl_group_by FINAL;

SELECT
    toYYYYMMDD(ts) AS d,
    count(),
    sum(value),
    min(min_value),
    max(max_value)
FROM test_ttl_group_by
GROUP BY d
ORDER BY d;

┌────────d─┬─count()─┬─sum(value)─┬─min(min_value)─┬─max(max_value)─┐
│ 20210613 │       5 │        400 │              4 │              4 │
│ 20210814 │       5 │        300 │              3 │              3 │
│ 20210816 │     105 │        300 │              1 │              2 │
└──────────┴─────────┴────────────┴────────────────┴────────────────┘

```
### TTL GROUP BY \+ DELETE


```
CREATE TABLE test_ttl_group_by
(
    `key` UInt32,
    `ts` DateTime,
    `value` UInt32,
    `min_value` UInt32 DEFAULT value,
    `max_value` UInt32 DEFAULT value
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (key, toStartOfDay(ts))
TTL 
ts + interval 180 day,
ts + interval 30 day 
    GROUP BY key, toStartOfDay(ts) 
    SET value = sum(value), 
    min_value = min(min_value), 
    max_value = max(max_value), 
    ts = min(toStartOfDay(ts));

-- stop merges to demonstrate data before / after 
-- a rolling up
SYSTEM STOP TTL MERGES test_ttl_group_by;
SYSTEM STOP MERGES test_ttl_group_by;

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() + number,
    1
FROM numbers(100);

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() - interval 60 day + number,
    2
FROM numbers(100);    

INSERT INTO test_ttl_group_by (key, ts, value)
SELECT
    number % 5,
    now() - interval 200 day + number,
    3
FROM numbers(100);  

SELECT
    toYYYYMM(ts) AS m,
    count(),
    sum(value),
    min(min_value),
    max(max_value)
FROM test_ttl_group_by
GROUP BY m;

┌──────m─┬─count()─┬─sum(value)─┬─min(min_value)─┬─max(max_value)─┐
│ 202101 │     100 │        300 │              3 │              3 │
│ 202106 │     100 │        200 │              2 │              2 │
│ 202108 │     100 │        100 │              1 │              1 │
└────────┴─────────┴────────────┴────────────────┴────────────────┘

SYSTEM START TTL MERGES test_ttl_group_by;
SYSTEM START MERGES test_ttl_group_by;
OPTIMIZE TABLE test_ttl_group_by FINAL;

┌──────m─┬─count()─┬─sum(value)─┬─min(min_value)─┬─max(max_value)─┐
│ 202106 │       5 │        200 │              2 │              2 │
│ 202108 │     100 │        100 │              1 │              1 │
└────────┴─────────┴────────────┴────────────────┴────────────────┘

```
Also see the [Altinity Knowledge Base pages on the MergeTree table engine family](../../../engines/mergetree-table-engine-family)
.

# 4 \- TTL Recompress example

TTL Recompress example*See also [the Altinity Knowledge Base article on testing different compression codecs](../../../altinity-kb-schema-design/codecs/altinity-kb-how-to-test-different-compression-codecs)
.*

## Example how to create a table and define recompression rules


```
CREATE TABLE hits
(
    `banner_id` UInt64,
    `event_time` DateTime CODEC(Delta, Default),
    `c_name` String,
    `c_cost` Float64
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (banner_id, event_time)
TTL event_time + toIntervalMonth(1) RECOMPRESS CODEC(ZSTD(1)),
    event_time + toIntervalMonth(6) RECOMPRESS CODEC(ZSTD(6);

```
Default compression is LZ4\. See [the ClickHouse® documentation](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings#server-settings-compression)
for more information.

These TTL rules recompress data after 1 and 6 months.

CODEC(Delta, Default) – **Default** means to use default compression (LZ4 \-\> ZSTD1 \-\> ZSTD6\) in this case.

## Example how to define recompression rules for an existing table


```
CREATE TABLE hits
(
    `banner_id` UInt64,
    `event_time` DateTime CODEC(Delta, LZ4),
    `c_name` String,
    `c_cost` Float64
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (banner_id, event_time);

ALTER TABLE hits 
  modify column event_time DateTime CODEC(Delta, Default),
  modify TTL event_time + toIntervalMonth(1) RECOMPRESS CODEC(ZSTD(1)),
       event_time + toIntervalMonth(6) RECOMPRESS CODEC(ZSTD(6));

```
All columns have implicit default compression from server config, except `event_time`, that’s why need to change to compression to `Default` for this column otherwise it won’t be recompressed.
