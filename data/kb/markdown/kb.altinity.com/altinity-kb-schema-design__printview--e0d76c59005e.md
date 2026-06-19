# Schema design \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-schema-design/).

# Schema design

All you need to know about ClickHouse® schema design, including materialized view, limitations, lowcardinality, codecs.- 1: [ClickHouse® limitations](#pg-f53de7c542782ac20eeebf170caa7854)
- 2: [ClickHouse® row\-level deduplication](#pg-2cd2a3075e1072228f2b708289bcac13)
- 3: [Column backfilling with alter/update using a dictionary](#pg-63a5ff0425a5b07157526dd5851788f6)
- 4: [Functions to count uniqs](#pg-b868fddf1dd2eabdbcf373d3e2a6a0f8)
- 5: [How to change ORDER BY](#pg-eaab0ef7f154800e4f2914cc8c9a3313)
- 6: [Ingestion of AggregateFunction](#pg-f6d8356db42efe167a8ded9555042617)
- 7: [Insert Deduplication / Insert Idempotency](#pg-9aad118d0c2925c045ed160a4356663e)
- 8: [JSONEachRow, Tuples, Maps and Materialized Views](#pg-4ae3680be39fdad44d89a6ca317a7a06)
- 9: [Pre\-Aggregation approaches](#pg-89ddba3a999cc73db4bd1b10d5a302f5)
- 10: [SnowflakeID for Efficient Primary Keys](#pg-ac0ca4ecebb199107ec7fbdb3c2487c9)
- 11: [Two columns indexing](#pg-f42b8501efcb3513ffc74554958a4a63)
- 12: [Best schema for storing many metrics registered from the single source](#pg-d4b8c7f8e2ba403dbadb51cbdaef9e77)
- 13: [Codecs](#pg-4a4953b58f1744c8872edf8e3844bc39)
- 13\.1: [Codecs on array columns](#pg-969f346c16e2b280e2aa45ba85b689be)
- 13\.2: [Codecs speed](#pg-dce00b858322605f3f48434154a40251)
- 13\.3: [How to test different compression codecs](#pg-d7d0b3e12d54a31abbccb07fd95ecf8d)

- 14: [Dictionaries vs LowCardinality](#pg-d58fe82154526e360b0c8f78f0f44c3b)
- 15: [Flattened table](#pg-e7e8eeb0014aeeafecb27b5fa703960c)
- 16: [Floats vs Decimals](#pg-9e86bccea71255b40bb6cd9098c6238a)
- 17: [Ingestion performance and formats](#pg-8d2f7e3ffae35f9280631d757a4face5)
- 18: [IPs/masks](#pg-d8329a49a438905bf2e024e1281fd28b)
- 19: [JSONAsString and Mat. View as JSON parser](#pg-6990e4ebc0462edf166319c5f49186de)
- 20: [LowCardinality](#pg-dc4d37782d587dfdfdeadec24d9440a5)
- 21: [ClickHouse® Materialized Views](#pg-f065ed89a7c944b57841bab2ea6cdb92)
- 21\.1: [Idempotent inserts into a materialized view](#pg-efd5546f247797daa53f929da20153b0)
- 21\.2: [Backfill/populate MV in a controlled manner](#pg-7eccdd4920775fe5f6841654ebe7a03d)

# 1 \- ClickHouse® limitations

How much is too much?In most of the cases ClickHouse® doesn’t have any hard limits. But obviously there there are some practical limitation / barriers for different things \- often they are caused by some system / network / filesystem limitation.

So after reaching some limits you can get different kind of problems, usually it never a failures / errors, but different kinds of degradations (slower queries / high cpu/memory usage, extra load on the network / zookeeper etc).

While those numbers can vary a lot depending on your hardware \& settings there is some safe ‘Goldilocks’ zone where ClickHouse work the best with default settings \& usual hardware.

### Number of tables (system\-wide, across all databases)

- non\-replicated [MergeTree\-family](https://kb.altinity.com/engines/mergetree-table-engine-family/)
tables \= few thousands is still acceptable, if you don’t do realtime inserts in more that few dozens of them. See [\#32259](https://github.com/ClickHouse/ClickHouse/issues/32259)
- ReplicatedXXXMergeTree \= few hundreds is still acceptable, if you don’t do realtime inserts in more that few dozens of them. Every Replicated table comes with it’s own cost (need to do housekeeping operations, monitoring replication queues etc). See [\#31919](https://github.com/ClickHouse/ClickHouse/issues/31919)
- Log family table \= even dozens of thousands is still ok, especially if database engine \= Lazy is used.

### Number of databases

Fewer than number of tables (above). Dozens / hundreds is usually still acceptable.

### Number of inserts per seconds

For usual (non async) inserts \- dozen is enough. Every insert creates a part, if you will create parts too often, ClickHouse will not be able to merge them and you will be getting ’too many parts’.

### Number of columns in the table

Up to a few hundreds. With thousands of columns the inserts / background merges may become slower / require more of RAM.
See for example <https://github.com/ClickHouse/ClickHouse/issues/6943>
<https://github.com/ClickHouse/ClickHouse/issues/27502>

### ClickHouse instances on a single node / VM

One is enough. Single ClickHouse can use resources of the node very efficiently, and it may require some complicated tuning to run several instances on a single node.

### Number of parts / partitions (system\-wide, across all databases)

More than several dozens thousands may lead to performance degradation: slow starts (see <https://github.com/ClickHouse/ClickHouse/issues/10087>
).

### Number of tables \& partitions touched by a single insert

If you have realtime / frequent inserts no more than few.

For the inserts are rare \- up to couple of dozens.

### Number of parts in the single table

More than \~ 5 thousands may lead to issues with alters in Replicated tables (caused by `jute.maxbuffer` overrun, see [details](../altinity-kb-setup-and-maintenance/zookeeper-session-expired.md)
), and query speed degradation.

### Disk size per shard

Less than 10TB of compressed data per server. Bigger disk are harder to replace / resync.

### Number of shards

Dozens is still ok. More may require having more complex (non\-flat) routing.

### Number of replicas in a single shard

2 is minimum for HA. 3 is a ‘golden standard’. Up to 6\-8 is still ok. If you have more with realtime inserts \- it can impact the zookeeper traffic.

### Number of [Zookeeper nodes](https://docs.altinity.com/operationsguide/clickhouse-zookeeper/)
in the ensemble

3 (Three) for most of the cases is enough (you can loose one node). Using more nodes allows to scale up read throughput for zookeeper, but doesn’t improve writes at all.

### Number of [materialized views](/altinity-kb-schema-design/materialized-views/)
attached to a single table.

Up to few. The less the better if the table is getting realtime inserts. (no matter if MV are chained or all are fed from the same source table).

The more you have the more costly your inserts are, and the bigger risks to get some inconsistencies between some MV (inserts to MV and main table are not atomic).

If the table doesn’t have realtime inserts you can have more MV.

### Number of projections inside a single table.

Up to few. Similar to MV above.

### Number of secondary indexes a single table.

One to about a dozen. Different types of indexes has different penalty, bloom\_filter is 100 times heavier than min\_max index
At some point your inserts will slow down. Try to create possible minimum of indexes.
You can combine many columns into a single index and this index will work for any predicate but create less impact.

### Number of [Kafka tables / consumers](https://altinity.com/blog/kafka-engine-the-story-continues)
inside

High number of Kafka tables maybe quite expensive (every consumer \= very expensive librdkafka object with several threads inside).
Usually alternative approaches are preferable (mixing several datastreams in one topic, denormalizing, consuming several topics of identical structure with a single Kafka table, etc).

If you really need a lot of Kafka tables you may need more ram / CPU on the node and
increase `background_message_broker_schedule_pool_size` (default is 16\) to the number of Kafka tables.

# 2 \- ClickHouse® row\-level deduplication

ClickHouse® row\-level deduplication.## ClickHouse® row\-level deduplication.

(This article is about row\-level deduplication of already ingested data. For insert/block\-level deduplication and insert idempotency, see [Insert Deduplication / Insert Idempotency](https://kb.altinity.com/altinity-kb-schema-design/insert_deduplication/)
. For materialized\-view retry semantics, see [Idempotent inserts into a materialized view](https://kb.altinity.com/altinity-kb-schema-design/materialized-views/idempotent_inserts_mv/)
.)

There is quite common requirement to do deduplication on a record level in ClickHouse.

- Sometimes duplicates are appear naturally on collector side.
- Sometime they appear due the the fact that message queue system (Kafka/Rabbit/etc) offers at\-least\-once guarantees.
- Sometimes you just expect insert idempotency on row level.

For the general case, ClickHouse does not provide a cheap built\-in way to enforce arbitrary row\-level uniqueness across an already large table.
That is a different problem from retry\-safe insert deduplication, which ClickHouse supports separately for `MergeTree` family inserts.

The reason is simple: to check if the row already exists you need a lookup that is closer to a key\-value access pattern (which is not what ClickHouse is optimized for),
in general case \- across the whole huge table (which can be terabyte/petabyte size).

But there many usecases when you can achieve something like row\-level deduplication in ClickHouse:

### Approach 0\. Make deduplication before ingesting data to ClickHouse

Pros:

- you have full control
- clean and simple schema and selects in ClickHouse

Cons:

- extra coding and ‘moving parts’, storing some ids somewhere
- check if row exists in ClickHouse before insert can give non\-satisfying results if you use ClickHouse cluster (i.e. Replicated / Distributed tables) \- due to eventual consistency.

### Approach 1\. Allow duplicates during ingestion.

Remove them on SELECT level (by things like GROUP BY)

Pros:

- simple inserts

Cons:

- complicates selects
- all selects will be significantly slower

### Approach 2\. Eventual deduplication using ReplacingMergeTree

Pros:

- simple

Cons:

- can force you to use suboptimal ORDER BY (which will guarantee record uniqueness)
- deduplication is eventual \- you never know when it will happen, and you will get some duplicates if you don’t use `FINAL`
- selects with `FINAL` (`select * from table_name FINAL`) add overhead and should be benchmarked
	- older versions often needed manual optimization <https://github.com/ClickHouse/ClickHouse/issues/31411>
	- performance has improved significantly in recent releases, so `FINAL` is often acceptable in production workloads [https://clickhouse.com/blog/common\-getting\-started\-issues\-with\-clickhouse](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse)
	- additional tuning notes: [https://kb.altinity.com/altinity\-kb\-queries\-and\-syntax/altinity\-kb\-final\-clause\-speed/](https://kb.altinity.com/altinity-kb-queries-and-syntax/altinity-kb-final-clause-speed/)

### Approach 3\. Eventual deduplication using CollapsingMergeTree

Pros:

- you can make the proper aggregations of last state w/o `FINAL` (bookkeeping\-alike sums, counts etc)

Cons:

- complicated
- can force you to use suboptimal ORDER BY (which will guarantee record uniqueness)
- you need to store previous state of the record somewhere, or extract it before ingestion from ClickHouse
- deduplication is eventual (same as with Replacing)

### Approach 4\. Eventual deduplication using Summing/Aggregating/CoalescingMergeTree

use SimpleAggregateFunction( anyLast, …) or AggregateFunction with argMax for Summing/AggregatingMT.
CoalescingMergeTree implies anyLast by default

Pros:

- you can finish deduplication with `GROUP BY` instead of `FINAL` (it’s faster)

Cons:

- quite complicated
- can force you to use suboptimal ORDER BY (which will guarantee record uniqueness)
- deduplication is eventual (same as with ReplacingMergeTree)

Example: keep the latest version of each row in an `AggregatingMergeTree` table and read the finalized state with `GROUP BY`:


```
create table Example4Raw
(
    id UInt64,
    version UInt64,
    metric UInt64
)
engine = MergeTree
order by (id, version);

create table Example4Agg
(
    id UInt64,
    metric_state AggregateFunction(argMax, UInt64, UInt64)
)
engine = AggregatingMergeTree
order by id;

create materialized view Example4AggMV to Example4Agg as
select id, argMaxState(metric, version) as metric_state
from Example4Raw
group by id;

```
In that example the result contains `id = 1, metric = 20` and `id = 2, metric = 30`.


```
create table Example4Raw
(
    id UInt64,
    version UInt64,
    metric UInt64
)
engine = MergeTree
order by (id, version);

create table Example4Agg
(
    id UInt64,
    metric_state Nullable(UInt64)
)
engine = CoalescingTree
order by id;

create materialized view Example4AggMV to Example4Agg as
select id, metric as metric_state
from Example4Raw;

```
### Approach 5\. Keep data fragments where duplicates are possible to isolate.

Usually you can expect the duplicates only in some time window (like 5 minutes, or one hour, or something like that).

You can put that ‘dirty’ data in separate place, and put it to final MergeTree table after deduplication window timeout.
For example \- you insert data in some tiny tables (Engine\=StripeLog) with minute suffix, and move data from tinytable older that X minutes to target MergeTree (with some external queries).
In the meanwhile you can see realtime data using Engine\=Merge / VIEWs etc.

Pros:

- good control
- no duplicated in target table
- perfect ingestion speed

Cons:

- quite complicated

### Approach 6\. Deduplication using MV pipeline.

You insert into some temporary table (even with Engine\=Null) and MV do join or subselect
(which will check the existence of arrived rows in some time frame of target table) and copy new only rows to destination table.

Pros:

- don’t impact the select speed

Cons:

- complicated
- for clusters can be inaccurate due to eventual consistency
- slows down inserts significantly (every insert will need to do lookup in target table first)


```
create table Example1 (id Int64, metric UInt64) 
engine = MergeTree order by id;

create table Example1Null engine = Null as Example1;

create materialized view __Example1 to Example1 as
select * from Example1Null 
where id not in (
   select id from Example1 where id in (
      select id from Example1Null
   )
)

```
In all case: due to eventual consistency of ClickHouse replication you can still get duplicates if you insert into different replicas/shards.

# 3 \- Column backfilling with alter/update using a dictionary

Column backfilling with alter/update using a dictionary## Column backfilling

Sometimes you need to add a column into a huge table and backfill it with a data from another source, without reingesting all data.

#### Replicated setup

In case of a replicated / sharded setup you need to have the dictionary and source table (dict\_table / item\_dict) on all nodes and they have to all have EXACTLY the same data. The easiest way to do this is to make dict\_table replicated.

In this case, you will need to set the setting `allow_nondeterministic_mutations=1` on the user that runs the `ALTER TABLE`. See the [ClickHouse® docs](https://clickhouse.com/docs/en/operations/settings/settings#allow_nondeterministic_mutations)
for more information about this setting.

Here is an example.


```
create database test;
use test;

-- table with an existing data, we need to backfill / update S column

create table fact ( key1 UInt64, key2 String, key3 String, D Date, S String)
Engine MergeTree partition by D order by (key1, key2, key3);

-- example data
insert into fact select number, toString(number%103), toString(number%13), today(), toString(number) from numbers(1e9);
0 rows in set. Elapsed: 155.066 sec. Processed 1.00 billion rows, 8.00 GB (6.45 million rows/s., 51.61 MB/s.)

insert into fact select number, toString(number%103), toString(number%13), today() - 30, toString(number)　from numbers(1e9);
0 rows in set. Elapsed: 141.594 sec. Processed 1.00 billion rows, 8.00 GB (7.06 million rows/s., 56.52 MB/s.)

insert into fact select number, toString(number%103), toString(number%13), today() - 60, toString(number)　from numbers(1e10);
0 rows in set. Elapsed: 1585.549 sec. Processed 10.00 billion rows, 80.01 GB (6.31 million rows/s., 50.46 MB/s.)

select count() from fact;
12000000000                          -- 12 billions rows.


-- table - source of the info to update
create table dict_table ( key1 UInt64, key2 String, key3 String, S String)
Engine MergeTree order by (key1, key2, key3);

-- example data
insert into dict_table select number, toString(number%103), toString(number%13), 
toString(number)||'xxx'　from numbers(1e10);
0 rows in set. Elapsed: 1390.121 sec. Processed 10.00 billion rows, 80.01 GB (7.19 million rows/s., 57.55 MB/s.)

-- DICTIONARY witch will be the source for update / we cannot query dict_table directly
CREATE DICTIONARY item_dict ( key1 UInt64, key2 String, key3 String, S String ) 
PRIMARY KEY key1,key2,key3 SOURCE(CLICKHOUSE(TABLE dict_table DB 'test' USER 'default')) 
LAYOUT(complex_key_cache(size_in_cells 50000000))
Lifetime(60000);



-- let's test that the dictionary is working

select dictGetString('item_dict', 'S', tuple(toUInt64(1),'1','1'));
┌─dictGetString('item_dict', 'S', tuple(toUInt64(1), '1', '1'))─┐
│ 1xxx                                                          │
└───────────────────────────────────────────────────────────────┘
1 rows in set. Elapsed: 0.080 sec.

SELECT dictGetString('item_dict', 'S', (toUInt64(1111111), '50', '1'))
┌─dictGetString('item_dict', 'S', tuple(toUInt64(1111111), '50', '1'))─┐
│ 1111111xxx                                                           │
└──────────────────────────────────────────────────────────────────────┘
1 rows in set. Elapsed: 0.004 sec.


-- Now let's lower number of simultaneous updates/mutations

select value from system.settings where name like '%background_pool_size%';
┌─value─┐
│ 16    │
└───────┘

alter table fact modify setting number_of_free_entries_in_pool_to_execute_mutation=15; -- only one mutation is possible per time / 16 - 15 = 1


-- the mutation itself
alter table test.fact update S = dictGetString('test.item_dict', 'S', tuple(key1,key2,key3)) where 1;

-- mutation took 26 hours and item_dict used bytes_allocated: 8187277280


select * from system.mutations where not is_done \G

Row 1:
──────
database:                   test
table:                      fact
mutation_id:                mutation_11452.txt
command:                    UPDATE S = dictGetString('test.item_dict', 'S', (key1, key2, key3)) WHERE 1
create_time:                2022-01-29 20:21:00
block_numbers.partition_id: ['']
block_numbers.number:       [11452]
parts_to_do_names:          ['20220128_1_954_4','20211230_955_1148_3','20211230_1149_1320_3','20211230_1321_1525_3','20211230_1526_1718_3','20211230_1719_1823_3','20211230_1824_1859_2','20211230_1860_1895_2','20211230_1896_1900_1','20211230_1901_1906_1','20211230_1907_1907_0','20211230_1908_1908_0','20211130_2998_9023_5','20211130_9024_10177_4','20211130_10178_11416_4','20211130_11417_11445_2','20211130_11446_11446_0']
parts_to_do:                17
is_done:                    0
latest_failed_part:
latest_fail_time:           1970-01-01 00:00:00
latest_fail_reason:


SELECT
    table,
    (elapsed * (1 / progress)) - elapsed,
    elapsed,
    progress,
    is_mutation,
    formatReadableSize(total_size_bytes_compressed) AS size,
    formatReadableSize(memory_usage) AS mem
FROM system.merges
ORDER BY progress DESC

┌─table────────────────────────┬─minus(multiply(elapsed, divide(1, progress)), elapsed)─┬─────────elapsed─┬────────────progress─┬─is_mutation─┬─size───────┬─mem───────┐
│ fact                         │                                      7259.920140111059 │  8631.476589565 │  0.5431540560211632 │           1 │ 1.89 GiB   │ 0.00 B    │
│ fact                         │                                      60929.22808705666 │ 23985.610558929 │ 0.28246665649246827 │           1 │ 9.86 GiB   │ 4.25 MiB  │
└──────────────────────────────┴────────────────────────────────────────────────────────┴─────────────────┴─────────────────────┴─────────────┴────────────┴───────────┘


SELECT *　FROM system.dictionaries　WHERE name = 'item_dict'　\G

Row 1:
──────
database:                    test
name:                        item_dict
uuid:                        28fda092-260f-430f-a8fd-a092260f330f
status:                      LOADED
origin:                      28fda092-260f-430f-a8fd-a092260f330f
type:                        ComplexKeyCache
key.names:                   ['key1','key2','key3']
key.types:                   ['UInt64','String','String']
attribute.names:             ['S']
attribute.types:             ['String']
bytes_allocated:             8187277280
query_count:                 12000000000
hit_rate:                    1.6666666666666666e-10
found_rate:                  1
element_count:               67108864
load_factor:                 1
source:                      ClickHouse: test.dict_table
lifetime_min:                0
lifetime_max:                60000
loading_start_time:          2022-01-29 20:20:50
last_successful_update_time: 2022-01-29 20:20:51
loading_duration:            0.829
last_exception:


-- Check that data is updated 

SELECT *
FROM test.fact
WHERE key1 = 11111

┌──key1─┬─key2─┬─key3─┬──────────D─┬─S────────┐
│ 11111 │ 90   │ 9    │ 2021-12-30 │ 11111xxx │
│ 11111 │ 90   │ 9    │ 2022-01-28 │ 11111xxx │
│ 11111 │ 90   │ 9    │ 2021-11-30 │ 11111xxx │
└───────┴──────┴──────┴────────────┴──────────┘

```
# 4 \- Functions to count uniqs

Functions to count uniqs.## Functions to count uniqs



| Function | Function(State) | StateSize | Result | QPS |
| --- | --- | --- | --- | --- |
| uniqExact | uniqExactState | 1600003 | 100000 | 59\.23 |
| uniq | uniqState | 200804 | 100315 | 85\.55 |
| uniqCombined | uniqCombinedState | 98505 | 100314 | 108\.09 |
| uniqCombined(12\) | uniqCombinedState(12\) | 3291 | 98160 | 151\.64 |
| uniqCombined(15\) | uniqCombinedState(15\) | 24783 | 100768 | 110\.18 |
| uniqCombined(18\) | uniqCombinedState(18\) | 196805 | 100332 | 101\.56 |
| uniqCombined(20\) | uniqCombinedState(20\) | 786621 | 100088 | 65\.05 |
| uniqCombined64(12\) | uniqCombined64State(12\) | 3291 | 98160 | 164\.96 |
| uniqCombined64(15\) | uniqCombined64State(15\) | 24783 | 100768 | 133\.96 |
| uniqCombined64(18\) | uniqCombined64State(18\) | 196805 | 100332 | 110\.85 |
| uniqCombined64(20\) | uniqCombined64State(20\) | 786621 | 100088 | 66\.48 |
| uniqHLL12 | uniqHLL12State | 2651 | 101344 | 177\.91 |
| uniqTheta | uniqThetaState | 32795 | 98045 | 144\.05 |
| uniqUpTo(100\) | uniqUpToState(100\) | 1 | 101 | 222\.93 |

Stats collected via script below on 22\.2


```
funcname=( "uniqExact" "uniq" "uniqCombined" "uniqCombined(12)" "uniqCombined(15)" "uniqCombined(18)" "uniqCombined(20)" "uniqCombined64(12)" "uniqCombined64(15)" "uniqCombined64(18)" "uniqCombined64(20)" "uniqHLL12" "uniqTheta" "uniqUpTo(100)")
funcname2=( "uniqExactState" "uniqState" "uniqCombinedState" "uniqCombinedState(12)" "uniqCombinedState(15)" "uniqCombinedState(18)" "uniqCombinedState(20)" "uniqCombined64State(12)" "uniqCombined64State(15)" "uniqCombined64State(18)" "uniqCombined64State(20)" "uniqHLL12State" "uniqThetaState" "uniqUpToState(100)")

length=${#funcname[@]}
 

for (( j=0; j<length; j++ ));
do
  f1="${funcname[$j]}"
  f2="${funcname2[$j]}"
  size=$( clickhouse-client -q "select ${f2}(toString(number)) from numbers_mt(100000) FORMAT RowBinary" | wc -c )
  result="$( clickhouse-client -q "select ${f1}(toString(number)) from numbers_mt(100000)" )"
  time=$( rm /tmp/clickhouse-benchmark.json; echo "select ${f1}(toString(number)) from numbers_mt(100000)" | clickhouse-benchmark -i200 --json=/tmp/clickhouse-benchmark.json &>/dev/null; cat /tmp/clickhouse-benchmark.json | grep QPS  )

  printf "|%s|%s,%s,%s,%s\n" "$f1" "$f2" "$size" "$result" "$time"
done

```
## groupBitmap

Use [Roaring Bitmaps](https://roaringbitmap.org/)
underneath.
Return amount of uniq values.

Can be used with Int\* types
Works really great when your values quite similar. (Low memory usage / state size)

Example with blockchain data, block\_number is monotonically increasing number.


```
SELECT groupBitmap(block_number) FROM blockchain;

┌─groupBitmap(block_number)─┐
│                  48478157 │
└───────────────────────────┘

MemoryTracker: Peak memory usage (for query): 64.44 MiB.
1 row in set. Elapsed: 32.044 sec. Processed 4.77 billion rows, 38.14 GB (148.77 million rows/s., 1.19 GB/s.)

SELECT uniqExact(block_number) FROM blockchain;

┌─uniqExact(block_number)─┐
│                48478157 │
└─────────────────────────┘

MemoryTracker: Peak memory usage (for query): 4.27 GiB.
1 row in set. Elapsed: 70.058 sec. Processed 4.77 billion rows, 38.14 GB (68.05 million rows/s., 544.38 MB/s.)

```
# 5 \- How to change ORDER BY

How to change ORDER BY.## Create a new table and copy data through an intermediate table. Step by step procedure.

We want to add `column3` to the ORDER BY in this table:


```
CREATE TABLE example_table
(
  date Date,
  column1 String,
  column2 String,
  column3 String,
  column4 String
)
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/default/example_table', '{replica}')
PARTITION BY toYYYYMM(date)
ORDER BY (column1, column2)

```
1. Stop publishing/INSERT into `example_table`.
2. `Rename table example_table to example_table_old`
3. Create the new table with the old name. This will preserve all dependencies like materialized views.


```
CREATE TABLE example_table as example_table_old 
ENGINE = ReplicatedMergeTree('/clickhouse/{cluster}/tables/{shard}/default/example_table_new', '{replica}')
PARTITION BY toYYYYMM(date)
ORDER BY (column1, column2, column3)

```
4. Copy data from `example_table_old` into `example_table_temp`

a. Use this query to generate a list of INSERT statements


```
-- old Clickhouse versions before a support of `where _partition_id`
select concat('insert into example_table_temp select * from example_table_old where toYYYYMM(date)=',partition) as cmd, 
database, table, partition, sum(rows), sum(bytes_on_disk), count()
from system.parts
where database='default' and table='example_table_old'
group by database, table, partition
order by partition

-- newer Clickhouse versions with a support of `where _partition_id`
select concat('insert into example_table_temp select * from ', table,' where _partition_id = \'',partition_id, '\';') as cmd, 
database, table, partition, sum(rows), sum(bytes_on_disk), count()
from system.parts
where database='default' and table='example_table_old'
group by database, table, partition_id, partition
order by partition_id

```
b. Create an intermediate table


```
CREATE TABLE example_table_temp as example_table_old 
ENGINE = MergeTree
PARTITION BY toYYYYMM(date)
ORDER BY (column1, column2, column3)

```
c. Run the queries one by one

After each query compare the number of rows in both tables.
If the INSERT statement was interrupted and failed to copy data, drop the partition in `example_table` and repeat the INSERT.
If a partition was copied successfully, proceed to the next partition.

Here is a query to compare the tables:


```
select database, table, partition, sum(rows), sum(bytes_on_disk), count()
from system.parts
where database='default' and table like 'example_table%'
group by database, table, partition
order by partition

```
5. Attach data from the intermediate table to `example_table`

a. Use this query to generate a list of ATTACH statements


```
select concat('alter table example_table attach partition id ''',partition,''' from example_table_temp') as cmd, 
database, table, partition, sum(rows), sum(bytes_on_disk), count()
from system.parts
where database='default' and table='example_table_temp'
group by database, table, partition
order by partition

```
b. Run the queries one by one

Here is a query to compare the tables:


```
select hostName(), database, table, partition, sum(rows), sum(bytes_on_disk), count()
from clusterAllReplicas('my-cluster',system.parts)
where database='default' and table like 'example_table%'
group by hostName(), database, table, partition
order by partition

```
6. Drop `example_table_old` and `example_table_temp`
# 6 \- Ingestion of AggregateFunction

ClickHouse® \- How to insert AggregateFunction data## How to insert AggregateFunction data

### Ephemeral column


```
CREATE TABLE users (
  uid Int16, 
  updated SimpleAggregateFunction(max, DateTime),
  name_stub String Ephemeral,
  name AggregateFunction(argMax, String, DateTime) 
       default arrayReduce('argMaxState', [name_stub], [updated])
) ENGINE=AggregatingMergeTree order by uid;

INSERT INTO users(uid, updated, name_stub) VALUES (1231, '2020-01-02 00:00:00', 'Jane');

INSERT INTO users(uid, updated, name_stub) VALUES (1231, '2020-01-01 00:00:00', 'John');

SELECT
    uid,
    max(updated) AS updated,
    argMaxMerge(name)
FROM users
GROUP BY uid
┌──uid─┬─────────────updated─┬─argMaxMerge(name)─┐
│ 1231 │ 2020-01-02 00:00:00 │ Jane              │
└──────┴─────────────────────┴───────────────────┘

```
### Input function


```
CREATE TABLE users (
  uid Int16, 
  updated SimpleAggregateFunction(max, DateTime),
  name AggregateFunction(argMax, String, DateTime)
) ENGINE=AggregatingMergeTree order by uid;

INSERT INTO users
SELECT uid, updated, arrayReduce('argMaxState', [name], [updated])
FROM input('uid Int16, updated DateTime, name String') FORMAT Values (1231, '2020-01-02 00:00:00', 'Jane');

INSERT INTO users
SELECT uid, updated, arrayReduce('argMaxState', [name], [updated])
FROM input('uid Int16, updated DateTime, name String') FORMAT Values (1231, '2020-01-01 00:00:00', 'John');

SELECT
    uid,
    max(updated) AS updated,
    argMaxMerge(name)
FROM users
GROUP BY uid;
┌──uid─┬─────────────updated─┬─argMaxMerge(name)─┐
│ 1231 │ 2020-01-02 00:00:00 │ Jane              │
└──────┴─────────────────────┴───────────────────┘

```
### Materialized View And Null Engine


```
CREATE TABLE users (
  uid Int16, 
  updated SimpleAggregateFunction(max, DateTime),
  name AggregateFunction(argMax, String, DateTime)
) ENGINE=AggregatingMergeTree order by uid;

CREATE TABLE users_null (
  uid Int16, 
  updated DateTime,
  name String
) ENGINE=Null;

CREATE MATERIALIZED VIEW users_mv TO users AS
SELECT uid, updated, arrayReduce('argMaxState', [name], [updated]) name
FROM users_null;

INSERT INTO users_null Values (1231, '2020-01-02 00:00:00', 'Jane');

INSERT INTO users_null Values (1231, '2020-01-01 00:00:00', 'John');

SELECT
    uid,
    max(updated) AS updated,
    argMaxMerge(name) 
FROM users
GROUP BY uid;
┌──uid─┬─────────────updated─┬─argMaxMerge(name)─┐
│ 1231 │ 2020-01-02 00:00:00 │ Jane              │
└──────┴─────────────────────┴───────────────────┘

```
# 7 \- Insert Deduplication / Insert Idempotency

Using ClickHouse® features to avoid duplicate dataReplicated tables have a special feature insert deduplication (enabled by default).

[Documentation:](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replication/)
*Data blocks are deduplicated. For multiple writes of the same data block (data blocks of the same size containing the same rows in the same order), the block is only written once. The reason for this is in case of network failures when the client application does not know if the data was written to the DB, so the INSERT query can simply be repeated. It does not matter which replica INSERTs were sent to with identical data. INSERTs are idempotent. Deduplication parameters are controlled by merge\_tree server settings.*

### Example


```
create table test_insert ( A Int64 ) 
Engine=ReplicatedMergeTree('/clickhouse/cluster_test/tables/{table}','{replica}') 
order by A;
 
insert into test_insert values(1);
insert into test_insert values(1);
insert into test_insert values(1);
insert into test_insert values(1);

select * from test_insert;
┌─A─┐
│ 1 │                                       -- only one row has been inserted, the other rows were deduplicated
└───┘

alter table test_insert delete where 1;    -- that single row was removed

insert into test_insert values(1);

select * from test_insert;
0 rows in set. Elapsed: 0.001 sec.         -- the last insert was deduplicated again, 
                                           -- because `alter ... delete` does not clear deduplication checksums
                                           -- only `alter table drop partition` and `truncate` clear checksums

```
In `clickhouse-server.log` you may see trace messages `Block with ID ... already exists locally as part ... ignoring it`


```
# cat /var/log/clickhouse-server/clickhouse-server.log|grep test_insert|grep Block
..17:52:45.064974.. Block with ID all_7615936253566048997_747463735222236827 already exists locally as part all_0_0_0; ignoring it.
..17:52:45.068979.. Block with ID all_7615936253566048997_747463735222236827 already exists locally as part all_0_0_0; ignoring it.
..17:52:45.072883.. Block with ID all_7615936253566048997_747463735222236827 already exists locally as part all_0_0_0; ignoring it.
..17:52:45.076738.. Block with ID all_7615936253566048997_747463735222236827 already exists locally as part all_0_0_0; ignoring it.

```
Deduplication checksums are stored in [Zookeeper](https://docs.altinity.com/operationsguide/clickhouse-zookeeper/)
in `/blocks` table’s znode for each partition separately, so when you drop partition, they could be identified and removed for this partition.
(during `alter table delete` it’s impossible to match checksums, that’s why checksums stay in Zookeeper).


```
SELECT name, value
FROM system.zookeeper
WHERE path = '/clickhouse/cluster_test/tables/test_insert/blocks'
┌─name───────────────────────────────────────┬─value─────┐
│ all_7615936253566048997_747463735222236827 │ all_0_0_0 │
└────────────────────────────────────────────┴───────────┘

```
## insert\_deduplicate setting

Insert deduplication is controlled by the [insert\_deduplicate](https://clickhouse.com/docs/en/operations/settings/settings/#settings-insert-deduplicate)
setting

Let’s disable it:


```
set insert_deduplicate = 0;              -- insert_deduplicate is now disabled in this session

insert into test_insert values(1);
insert into test_insert values(1);
insert into test_insert values(1);

select * from test_insert format PrettyCompactMonoBlock;
┌─A─┐
│ 1 │
│ 1 │
│ 1 │                                   -- all 3 insterted rows are in the table
└───┘

alter table test_insert delete where 1;

insert into test_insert values(1);
insert into test_insert values(1);

select * from test_insert format PrettyCompactMonoBlock;
┌─A─┐
│ 1 │
│ 1 │
└───┘

```
Insert deduplication is a user\-level setting, it can be disabled in a session or in a user’s profile (insert\_deduplicate\=0\).

`clickhouse-client --insert_deduplicate=0 ....`

How to disable `insert_deduplicate` by default for all queries:


```
# cat /etc/clickhouse-server/users.d/insert_deduplicate.xml
<?xml version="1.0"?>
<yandex>
    <profiles>
        <default>
            <insert_deduplicate>0</insert_deduplicate>
        </default>
    </profile
</yandex>    

```
Other related settings: [replicated\_deduplication\_window](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings/#replicated-deduplication-window)
, [replicated\_deduplication\_window\_seconds](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings/#replicated-deduplication-window-seconds)
, [insert\_deduplication\_token](https://clickhouse.com/docs/en/operations/settings/settings/#insert_deduplication_token)
.

More info: <https://github.com/ClickHouse/ClickHouse/issues/16037>
<https://github.com/ClickHouse/ClickHouse/issues/3322>

## Non\-replicated MergeTree tables

By default insert deduplication is disabled for non\-replicated tables (for backward compatibility).

It can be enabled by the [merge\_tree](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings/#merge-tree-settings)
setting [non\_replicated\_deduplication\_window](https://clickhouse.com/docs/en/operations/settings/merge-tree-settings/#non-replicated-deduplication-window)
.

Example:


```
create table test_insert ( A Int64 ) 
Engine=MergeTree 
order by A
settings non_replicated_deduplication_window = 100;          -- 100 - how many latest checksums to store
 
insert into test_insert values(1);
insert into test_insert values(1);
insert into test_insert values(1);

insert into test_insert values(2);
insert into test_insert values(2);

select * from test_insert format PrettyCompactMonoBlock;
┌─A─┐
│ 2 │
│ 1 │
└───┘

```
In case of non\-replicated tables deduplication checksums are stored in files in the table’s folder:


```
cat /var/lib/clickhouse/data/default/test_insert/deduplication_logs/deduplication_log_1.txt
1	all_1_1_0	all_7615936253566048997_747463735222236827
1	all_4_4_0	all_636943575226146954_4277555262323907666

```
## Checksums calculation

Checksums are calculated not from the inserted data but from formed parts.

Insert data is separated to parts by table’s partitioning.

Parts contain rows sorted by the table’s `order by` and all values of functions (i.e. `now()`) or Default/Materialized columns are expanded.

### Example with partial insertion because of partitioning:


```
create table test_insert ( A Int64, B Int64 ) 
Engine=MergeTree 
partition by B 
order by A
settings non_replicated_deduplication_window = 100;  


insert into test_insert values (1,1);
insert into test_insert values (1,1)(1,2);

select * from test_insert format PrettyCompactMonoBlock;
┌─A─┬─B─┐
│ 1 │ 1 │
│ 1 │ 2 │                                   -- the second insert was skipped for only one partition!!!
└───┴───┘

```
### Example with deduplication despite the rows order:


```
drop table test_insert;

create table test_insert ( A Int64, B Int64 ) 
Engine=MergeTree 
order by (A, B)
settings non_replicated_deduplication_window = 100;  

insert into test_insert values (1,1)(1,2);
insert into test_insert values (1,2)(1,1);  -- the order of rows is not equal with the first insert

select * from test_insert format PrettyCompactMonoBlock;
┌─A─┬─B─┐
│ 1 │ 1 │
│ 1 │ 2 │
└───┴───┘
2 rows in set. Elapsed: 0.001 sec.          -- the second insert was skipped despite the rows order

```
### Example to demonstrate how Default/Materialize columns are expanded:


```
drop table test_insert;

create table test_insert ( A Int64, B Int64 Default rand() ) 
Engine=MergeTree 
order by A
settings non_replicated_deduplication_window = 100;

insert into test_insert(A) values (1);                 -- B calculated as  rand()
insert into test_insert(A) values (1);                 -- B calculated as  rand()

select * from test_insert format PrettyCompactMonoBlock;
┌─A─┬──────────B─┐
│ 1 │ 3467561058 │
│ 1 │ 3981927391 │
└───┴────────────┘

insert into test_insert(A, B) values (1, 3467561058);  -- B is not calculated / will be deduplicated

select * from test_insert format PrettyCompactMonoBlock;
┌─A─┬──────────B─┐
│ 1 │ 3981927391 │
│ 1 │ 3467561058 │
└───┴────────────┘

```
### Example to demonstrate how functions are expanded:


```
drop table test_insert;
create table test_insert ( A Int64, B DateTime64 ) 
Engine=MergeTree 
order by A
settings non_replicated_deduplication_window = 100;

insert into test_insert values (1, now64());
....
insert into test_insert values (1, now64());

select * from test_insert format PrettyCompactMonoBlock;
┌─A─┬───────────────────────B─┐
│ 1 │ 2022-01-31 15:43:45.364 │
│ 1 │ 2022-01-31 15:43:41.944 │
└───┴─────────────────────────┘

```
## insert\_deduplication\_token

Since ClickHouse® 22\.2 there is a new setting [insert\_deduplication\_token](https://clickhouse.com/docs/en/operations/settings/settings/#insert_deduplication_token)
.
This setting allows you to define an explicit token that will be used for deduplication instead of calculating a checksum from the inserted data.


```
CREATE TABLE test_table
( A Int64 )
ENGINE = MergeTree
ORDER BY A
SETTINGS non_replicated_deduplication_window = 100;

INSERT INTO test_table SETTINGS insert_deduplication_token = 'test' VALUES (1);

-- the next insert won't be deduplicated because insert_deduplication_token is different
INSERT INTO test_table SETTINGS insert_deduplication_token = 'test1' VALUES (1);

-- the next insert will be deduplicated because insert_deduplication_token 
-- is the same as one of the previous
INSERT INTO test_table SETTINGS insert_deduplication_token = 'test' VALUES (2);
SELECT * FROM test_table
┌─A─┐
│ 1 │
└───┘
┌─A─┐
│ 1 │
└───┘

```
# 8 \- JSONEachRow, Tuples, Maps and Materialized Views

How to use Tuple() and Map() with nested JSON messages in MVs## Using JSONEachRow with Tuple() in Materialized views

Sometimes we can have a nested json message with a fixed size structure like this:


```
{"s": "val1", "t": {"i": 42, "d": "2023-09-01 12:23:34.231"}}

```
Values can be NULL but the structure should be fixed. In this case we can use `Tuple()` to parse the JSON message:


```
CREATE TABLE tests.nest_tuple_source
(
    `s` String,
    `t` Tuple(`i` UInt8, `d` DateTime64(3))
)
ENGINE = Null 

```
We can use the above table as a source for a materialized view, like it was a Kafka table and in case our message has unexpected keys we make the Kafka table ignore them with the setting (23\.3\+):

`input_format_json_ignore_unknown_keys_in_named_tuple = 1`


```
CREATE MATERIALIZED VIEW tests.mv_nest_tuple TO tests.nest_tuple_destination
AS
SELECT
    s AS s,
    t.1 AS i,
    t.2 AS d
FROM tests.nest_tuple_source

```
Also, we need a destination table with an adapted structure as the source table:


```
CREATE TABLE tests.nest_tuple_destination
(
    `s` String,
    `i` UInt8, 
    `d` DateTime64(3)
)
ENGINE = MergeTree
ORDER BY tuple()

INSERT INTO tests.nest_tuple_source FORMAT JSONEachRow {"s": "val1", "t": {"i": 42, "d": "2023-09-01 12:23:34.231"}}


SELECT *
FROM nest_tuple_destination

┌─s────┬──i─┬───────────────────────d─┐
│ val1 │ 42 │ 2023-09-01 12:23:34.231 │
└──────┴────┴─────────────────────────┘

```
Some hints:

- 💡 Beware of column names in ClickHouse® they are Case sensitive. If a JSON message has the key names in Capitals, the Kafka/Source table should have the same column names in Capitals.
- 💡 Also this `Tuple()` approach is not for Dynamic json schemas as explained above. In the case of having a dynamic schema, use the classic approach using `JSONExtract` set of functions. If the schema is fixed, you can use `Tuple()` for `JSONEachRow` format but you need to use classic tuple notation (using index reference) inside the MV, because using named tuples inside the MV won’t work:
- 💡 `tuple.1 AS column1, tuple.2 AS column2` **CORRECT!**
- 💡 `tuple.column1 AS column1, tuple.column2 AS column2` **WRONG!**
- 💡 use `AS` (alias) for aggregated columns or columns affected by functions because MV do not work by positional arguments like SELECTs,they work by names\*\*

Example:

- `parseDateTime32BestEffort(t_date)` **WRONG!**
- `parseDateTime32BestEffort(t_date) AS t_date` **CORRECT!**

## Using JSONEachRow with Map() in Materialized views

Sometimes we can have a nested json message with a dynamic size like these and all elements inside the nested json must be of the same type:


```
{"k": "val1", "st": {"a": 42, "b": 1.877363}}

{"k": "val2", "st": {"a": 43, "b": 2.3343, "c": 34.4434}}

{"k": "val3", "st": {"a": 66743}}

```
In this case we can use Map() to parse the JSON message:


```

CREATE TABLE tests.nest_map_source
(
    `k` String,
    `st` Map(String, Float64)
)
Engine = Null 

CREATE MATERIALIZED VIEW tests.mv_nest_map TO tests.nest_map_destination
AS
SELECT
    k AS k,
    st['a'] AS st_a,
    st['b'] AS st_b,
    st['c'] AS st_c
FROM tests.nest_map_source 


CREATE TABLE tests.nest_map_destination
(
    `k` String,
    `st_a` Float64,
    `st_b` Float64,
    `st_c` Float64
)
ENGINE = MergeTree
ORDER BY tuple()

```
By default, ClickHouse will ignore unknown keys in the Map() but if you want to fail the insert if there are unknown keys then use the setting:

`input_format_skip_unknown_fields = 0`


```
INSERT INTO tests.nest_map_source FORMAT JSONEachRow {"k": "val1", "st": {"a": 42, "b": 1.877363}}
INSERT INTO tests.nest_map_source FORMAT JSONEachRow {"k": "val2", "st": {"a": 43, "b": 2.3343, "c": 34.4434}}
INSERT INTO tests.nest_map_source FORMAT JSONEachRow {"k": "val3", "st": {"a": 66743}}


SELECT *
FROM tests.nest_map_destination

┌─k────┬─st_a─┬─────st_b─┬─st_c─┐
│ val1 │   42 │ 1.877363 │    0 │
└──────┴──────┴──────────┴──────┘
┌─k────┬──st_a─┬─st_b─┬─st_c─┐
│ val3 │ 66743 │    0 │    0 │
└──────┴───────┴──────┴──────┘
┌─k────┬─st_a─┬───st_b─┬────st_c─┐
│ val2 │   43 │ 2.3343 │ 34.4434 │
└──────┴──────┴────────┴─────────┘

```
See also:

- [JSONExtract to parse many attributes at a time](/altinity-kb-queries-and-syntax/jsonextract-to-parse-many-attributes-at-a-time/)
- [JSONAsString and Mat. View as JSON parser](/altinity-kb-schema-design/altinity-kb-jsonasstring-and-mat.-view-as-json-parser/)
# 9 \- Pre\-Aggregation approaches

ETL vs Materialized Views vs Projections in ClickHouse®## Pre\-Aggregation approaches: ETL vs Materialized Views vs Projections



|  | ETL | MV | Projections |
| --- | --- | --- | --- |
| Realtime | no | yes | yes |
| How complex queries can be used to build the preaggregaton | any | complex | very simple |
| Impacts the insert speed | no | yes | yes |
| Are inconsistancies possible | Depends on ETL. If it process the errors properly \- no. | yes (no transactions / atomicity) | no |
| Lifetime of aggregation | any | any | Same as the raw data |
| Requirements | need external tools/scripting | is a part of database schema | is a part of table schema |
| How complex to use in queries | Depends on aggregation, usually simple, quering a separate table | Depends on aggregation, sometimes quite complex, quering a separate table | Very simple, quering the main table |
| Can work correctly with ReplacingMergeTree as a source | Yes | No | No |
| Can work correctly with CollapsingMergeTree as a source | Yes | For simple aggregations | For simple aggregations |
| Can be chained | Yes (Usually with DAGs / special scripts) | Yes (but may be not straightforward, and often is a bad idea) | No |
| Resources needed to calculate the increment | May be significant | Usually tiny | Usually tiny |

# 10 \- SnowflakeID for Efficient Primary Keys

SnowflakeID for Efficient Primary KeysIn data warehousing (DWH) environments, the choice of primary key (PK) can significantly impact performance, particularly in terms of RAM usage and query speed. This is where [SnowflakeID](https://en.wikipedia.org/wiki/Snowflake_ID)
comes into play, providing a robust solution for PK management. Here’s a deep dive into why and how Snowflake IDs are beneficial and practical implementation examples.

### Why Snowflake ID?

- **Natural IDs Suck**: Natural keys derived from business data can lead to various issues like complexity and instability. Surrogate keys, on the other hand, are system\-generated and stable.
- Surrogate keys simplify joins and indexing, which is crucial for performance in large\-scale data warehousing.
- Monotonic or sequential IDs help maintain the order of entries, which is essential for performance tuning and efficient range queries.
- Having both a timestamp and a unique ID in the same column allows for fast filtering of rows during SELECT operations. This is particularly useful for time\-series data.

### **Building Snowflake IDs**

There are two primary methods to construct the lower bits of a Snowflake ID:

1. **Hash of Important Columns**:

Using a hash function on significant columns ensures uniqueness and distribution.
2. **Row Number in insert batch**

Utilizing the row number within data blocks provides a straightforward approach to generating unique identifiers.

### **Implementation as UDF**

Here’s how to implement Snowflake IDs using standard SQL functions while utilizing second and millisecond timestamps.

Pack hash to lower 22 bits for DateTime64 and 32bits for DateTime


```
create function toSnowflake64 as (dt,ch) ->
  bitOr(dateTime64ToSnowflakeID(dt),
   bitAnd(bitAnd(ch,0x3FFFFF)+
      bitAnd(bitShiftRight(ch, 20),0x3FFFFF)+
      bitAnd(bitShiftRight(ch, 40),0x3FFFFF),
      0x3FFFFF) 
  );

create function toSnowflake as (dt,ch) ->
  bitOr(dateTimeToSnowflakeID(dt),
   bitAnd(bitAnd(ch,0xFFFFFFFF)+
      bitAnd(bitShiftRight(ch, 32),0xFFFFFFFF),
      0xFFFFFFFF) 
  );
    
with cityHash64('asdfsdnfs;n') as ch,
  now64() as dt
select dt,
  hex(toSnowflake64(dt,ch) as sn) ,
  snowflakeIDToDateTime64(sn);

with cityHash64('asdfsdnfs;n') as ch,
  now() as dt
select dt,
  hex(toSnowflake(dt,ch) as sn) ,
  snowflakeIDToDateTime(sn);

```
### **Creating Tables with Snowflake ID**

**Using Materialized Columns and hash**


```
create table XX 
(
  id Int64 materialized toSnowflake(now(),cityHash64(oldID)),
  oldID  String,
  data String
) engine=MergeTree order by id;

```
Note: Using User\-Defined Functions (UDFs) in CREATE TABLE statements is not always useful, as they expand to create table DDL, and changing them is inconvenient.

**Using a Null Table, Materialized View, and** rowNumberInAllBlocks

A more efficient approach involves using a Null table and materialized views.


```
create table XX 
(
  id Int64,
  data String
) engine=MergeTree order by id;

create table Null (data String) engine=Null;
create materialized view _XX to XX as
select toSnowflake(now(),rowNumberInAllBlocks()) is id, data
from Null;

```
### Converting from UUID to SnowFlakeID for subsequent events

Consider that your event stream only has a UUID column identifying a particular user. Registration time that can be used as a base for SnowFlakeID is presented only in the first ‘register’ event, but not in subsequent events. It’s easy to generate SnowFlakeID for the register event, but next, we need to get it from some other table without disturbing the ingestion process too much. Using Hash JOINs in Materialized Views is not recommended, so we need some “nested loop join” to get data fast. In Clickhouse, the “nested loop join” is still not supported, but Direct Dictionary can work around it.


```
CREATE TABLE UUID2ID_store (user_id UUID, id UInt64) 
ENGINE = MergeTree() -- EmbeddedRocksDB can be used instead
ORDER BY user_id
settings index_granularity=256;

CREATE DICTIONARY UUID2ID_dict (user_id UUID, id UInt64) 
PRIMARY KEY user_id
LAYOUT ( DIRECT ())
SOURCE(CLICKHOUSE(TABLE 'UUID2ID_store'));

CREATE OR REPLACE FUNCTION UUID2ID AS (uuid) -> dictGet('UUID2ID_dict',id,uuid);

CREATE MATERIALIZED VIEW _toUUID_store TO UUID2ID_store AS
select user_id, toSnowflake64(event_time, cityHash64(user_id)) as id
from Actions;

```
**Conclusion**

Snowflake IDs provide an efficient mechanism for generating unique, monotonic primary keys, which are essential for optimizing query performance in data warehousing environments. By combining timestamps and unique identifiers, snowflake IDs facilitate faster row filtering and ensure stable, surrogate key generation. Implementing these IDs using SQL functions and materialized views ensures that your data warehouse remains performant and scalable.

# 11 \- Two columns indexing

How to create ORDER BY suitable for filtering over two different columns in two different queriesSuppose we have telecom CDR data in which A party calls B party. Each data row consists of A party details: event\_timestamp, A MSISDN , A IMEI, A IMSI , A start location, A end location , B MSISDN, B IMEI, B IMSI , B start location, B end location, and some other metadata.

Searches will use one of the A or B fields, for example, A IMSI, within the start and end time window.

A msisdn, A imsi, A imei values are tightly coupled as users rarely change their phones.

The queries will be:


```
select * from X where A = '0123456789' and ts between ...;
select * from X where B = '0123456789' and ts between ...;

```
and both A \& B are high\-cardinality values

ClickHouse® primary skip index (ORDER BY/PRIMARY KEY) works great when you always include leading ORDER BY columns in the WHERE filter. There are exceptions for low\-cardinality columns and high\-correlated values, but here is another case. A \& B both have high cardinality, and it seems that their correlation is at a medium level.

Various solutions exist, and their effectiveness largely depends on the correlation of different column data. Testing all solutions on actual data is necessary to select the best one.

### ORDER BY \+ additional Skip Index


```
create table X (
    A UInt32,
    B UInt32,
    ts DateTime,
    ....
    INDEX ix_B (B) type minmax GRANULARITY 3
) engine = MergeTree
partition by toYYYYMM(ts)
order by (toStartOfDay(ts),A,B);

```
bloom\_filter index type instead of min\_max could work fine in some situations.

### Inverted index as a projection


```
create table X (
    A UInt32,
    B UInt32,
    ts DateTime,
    ....
    PROJECTION ix_B  (
        select A, B,ts ORDER BY B, ts
    )
) engine = MergeTree
partition by toYYYYMM(ts)
order by (toStartOfDay(ts),A,B);

select * from X 
where A in (select A from X where B='....' and ts between ...)
  and B='...' and ts between ... ;

```
- The number of rows the subquery returns should not be very high. 1M rows seems to be a suitable limit.
- A separate table with a Materialized View can also be used similarly.
- accessing pattern for the main table will “point”, so better to lower index\_granularity to 256\. That will increase RAM usage by Primary Key

### mortonEncode

(available from 23\.10\)

Do not prioritize either A or B, but distribute indexing efficiency between them.

- <https://github.com/ClickHouse/ClickHouse/issues/41195>
- [https://www.youtube.com/watch?v\=5GR1J4T4\_d8](https://www.youtube.com/watch?v=5GR1J4T4_d8)
- [https://clickhouse.com/docs/en/operations/settings/settings\#analyze\_index\_with\_space\_filling\_curves](https://clickhouse.com/docs/en/operations/settings/settings#analyze_index_with_space_filling_curves)


```
create table X (
    A UInt32,
    B UInt32,
    ts DateTime,
    ....
) engine = MergeTree
partition by toYYYYMM(ts)
order by (toStartOfDay(ts),mortonEncode(A,B));
select * from X where A = '0123456789' and ts between ...;
select * from X where B = '0123456789' and ts between ...;

```
### mortonEncode with non\-UInt columns

[mortonEncode](https://clickhouse.com/docs/en/sql-reference/functions/encoding-functions#mortonencode)
function requires UInt columns, but sometimes different column types are needed (like String or ipv6\). In such a case, the cityHash64() function can be used both for inserting and querying:


```
create table X (
    A IPv6,
    B IPv6,
    AA alias cityHash64(A),
    BB alias cityHash64(B),
    ts DateTime materialized now()
) engine = MergeTree
partition by toYYYYMM(ts)
order by 
(toStartOfDay(ts),mortonEncode(cityHash64(A),cityHash64(B)))
;

insert into X values ('fd7a:115c:a1e0:ab12:4843:cd96:624c:9a17','fd7a:115c:a1e0:ab12:4843:cd96:624c:9a17')

select * from X where cityHash64(toIPv6('fd7a:115c:a1e0:ab12:4843:cd96:624c:9a17')) =  AA;

```
### hilbertEncode as alternative

(available from 24\.6\)

[hilbertEncode](https://clickhouse.com/docs/en/sql-reference/functions/encoding-functions#hilbertencode)
can be used instead of mortonEncode. On some data it allows better results than mortonEncode.

# 12 \- Best schema for storing many metrics registered from the single source

Best schema for storing many metrics registered from the single sourcePicking the best schema for storing many metrics registered from single source is quite a common problem.

## 1 One row per metric

i.e.: timestamp, sourceid, metric\_name, metric\_value

Pros and cons:

- Pros:
	- simple
	- well normalized schema
	- easy to extend
	- that is quite typical pattern for timeseries databases
- Cons
	- different metrics values stored in same columns (worse compression)
	- to use values of different datatype you need to cast everything to string or introduce few columns for values of different types.
	- not always nice as you need to repeat all ‘common’ fields for each row
	- if you need to select all data for one time point you need to scan several ranges of data.

## 2 Each measurement (with lot of metrics) in it’s own row

In that way you need to put all the metrics in one row (i.e.: timestamp, sourceid, ….)
That approach is usually a source of debates about how to put all the metrics in one row.

### 2a Every metric in it’s own column

i.e.: timestamp, sourceid, metric1\_value, … , metricN\_value

Pros and cons:

- Pros
	- simple
	- really easy to access / scan for rows with particular metric
	- specialized and well adjusted datatypes for every metric.
	- good for dense recording (each time point can have almost 100% of all the possible metrics)
- Cons
	- adding new metric \= changing the schema (adding new column). not suitable when set of metric changes dynamically
	- not applicable when there are too many metrics (when you have more than 100\-200\)
	- when each timepoint have only small subset of metrics recorded \- if will create a lot of sparse filled columns.
	- you need to store ’lack of value’ somehow (NULLs or default values)
	- to read full row \- you need to read a lot of column files.

### 2b Using arrays / Nested / Map

i.e.: timestamp, sourceid, array\_of\_metric\_names, array\_of\_metric\_values

Pros and cons:

- Pros
	- easy to extend, you can have very dynamic / huge number of metrics.
	- you can use Array(LowCardinality(String)) for storing metric names efficiently
	- good for sparse recording (each time point can have only 1% of all the possible metrics)
- Cons
	- you need to extract all metrics for row to reach a single metric
	- not very handy / complicated non\-standard syntax
	- different metrics values stored in single array (bad compression)
	- to use values of different datatype you need to cast everything to string or introduce few arrays for values of different types.

### 2c Using JSON

i.e.: timestamp, sourceid, metrics\_data\_json

Pros and cons:

- Pros
	- easy to extend, you can have very dynamic / huge number of metrics.
	- the only option to store hierarchical / complicated data structures, also with arrays etc. inside.
	- good for sparse recording (each time point can have only 1% of all the possible metrics)
	- ClickHouse® has efficient API to work with JSON
	- nice if your data originally came in JSON (don’t need to reformat)
- Cons
	- uses storage non efficiently
	- different metrics values stored in single array (bad compression)
	- you need to extract whole JSON field to reach single metric
	- slower than arrays

### 2d Using querystring\-format URLs

i.e.: timestamp, sourceid, metrics\_querystring
Same pros/cons as raw JSON, but usually bit more compact than JSON

Pros and cons:

- Pros
	- ClickHouse has efficient API to work with URLs (extractURLParameter etc)
	- can have sense if you data came in such format (i.e. you can store GET / POST request data directly w/o reprocessing)
- Cons
	- slower than arrays

### 2e Several ‘baskets’ of arrays

i.e.: timestamp, sourceid, metric\_names\_basket1, metric\_values\_basket1, …, metric\_names\_basketN, metric\_values\_basketN
The same as 2b, but there are several key\-value arrays (‘basket’), and metric go to one particular basket depending on metric name (and optionally by metric type)

Pros and cons:

- Pros
	- address some disadvantages of 2b (you need to read only single, smaller basket for reaching a value, better compression \- less unrelated metrics are mixed together)
- Cons
	- complex

### 2f Combined approach

In real life Pareto principle is correct for many fields.

For that particular case: usually you need only about 20% of metrics 80% of the time. So you can pick the metrics which are used intensively, and which have a high density, and extract them into separate columns (like in option 2a), leaving the rest in a common ’trash bin’ (like in variants 2b\-2e).

With that approach you can have as many metrics as you need and they can be very dynamic. At the same time the most used metrics are stored in special, fine\-tuned columns.

At any time you can decide to move one more metric to a separate column `ALTER TABLE ... ADD COLUMN metricX Float64 MATERIALIZED metrics.value[indexOf(metrics.names,'metricX')];`

## 3 json type

[https://clickhouse.com/blog/a\-new\-powerful\-json\-data\-type\-for\-clickhouse](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse)

Related links:

[There is one article on our blog on this subject with some benchmarks.](https://www.altinity.com/blog/2019/5/23/handling-variable-time-series-efficiently-in-clickhouse)

[Slides from Percona Live](https://www.percona.com/sites/default/files/ple19-slides/day1-pm/clickhouse-for-timeseries.pdf%22)

# 13 \- Codecs

Codecs

| Codec Name | Recommended Data Types | Performance Notes |
| --- | --- | --- |
| LZ4 | Any | Used by default. Extremely fast; good compression; balanced speed and efficiency |
| ZSTD(level) | Any | Good compression; pretty fast; best for high compression needs. Don’t use levels higher than 3\. |
| LZ4HC(level) | Any | LZ4 High Compression algorithm with configurable level; slower but better compression than LZ4, but decompression is still fast. |
| Delta | Integer Types, Time Series Data, Timestamps | Preprocessor (should be followed by some compression codec). Stores difference between neighboring values; good for monotonically increasing data. |
| DoubleDelta | Integer Types, Time Series Data | Stores difference between neighboring delta values; suitable for time series data |
| Gorilla | Floating Point Types | Calculates XOR between current and previous value; suitable for slowly changing numbers |
| T64 | Integer, Time Series Data, Timestamps | Preprocessor (should be followed by some compression codec). Crops unused high bits; puts them into a 64x64 bit matrix; optimized for 64\-bit data types |
| GCD | Integer Numbers | Preprocessor (should be followed by some compression codec). Greatest common divisor compression; divides values by a common divisor; effective for divisible integer sequences |
| FPC | Floating Point Numbers | Designed for Float64; Algorithm detailed in [FPC paper](https://userweb.cs.txstate.edu/~burtscher/papers/dcc07a.pdf) , [ClickHouse® PR \#37553](https://github.com/ClickHouse/ClickHouse/pull/37553) |
| ZSTD\_QAT | Any | Requires hardware support for QuickAssist Technology (QAT) hardware; provides accelerated compression tasks |
| DEFLATE\_QPL | Any | Requires hardware support for Intel’s QuickAssist Technology for DEFLATE compression; enhanced performance for specific hardware |
| LowCardinality | String | It’s not a codec, but a datatype modifier. Reduces representation size; effective for columns with low cardinality |
| NONE | Non\-compressable data with very high entropy, like some random string, or some AggregateFunction states | No compression at all. Can be used on the columns that can not be compressed anyway. |

See

[How to test different compression codecs](altinity-kb-how-to-test-different-compression-codecs)

[https://altinity.com/blog/2019/7/new\-encodings\-to\-improve\-clickhouse](https://altinity.com/blog/2019/7/new-encodings-to-improve-clickhouse)

[https://www.percona.com/sites/default/files/ple19\-slides/day1\-pm/clickhouse\-for\-timeseries.pdf](https://www.percona.com/sites/default/files/ple19-slides/day1-pm/clickhouse-for-timeseries.pdf)

# 13\.1 \- Codecs on array columns

Codecs on array columns#### Info

Supported since 20\.10 (PR [\#15089](https://github.com/ClickHouse/ClickHouse/pull/15089)
). On older versions you will get exception:
`DB::Exception: Codec Delta is not applicable for Array(UInt64) because the data type is not of fixed size.`
```
DROP TABLE IF EXISTS array_codec_test SYNC

create table array_codec_test( number UInt64, arr Array(UInt64) ) Engine=MergeTree ORDER BY number;
INSERT INTO array_codec_test SELECT number,  arrayMap(i -> number + i, range(100)) from numbers(10000000);


/****  Default LZ4  *****/

OPTIMIZE TABLE array_codec_test FINAL;
--- Elapsed: 3.386 sec.


SELECT * FROM system.columns WHERE (table = 'array_codec_test') AND (name = 'arr')
/*
Row 1:
──────
database:                default
table:                   array_codec_test
name:                    arr
type:                    Array(UInt64)
position:                2
default_kind:         
default_expression:   
data_compressed_bytes:   173866750
data_uncompressed_bytes: 8080000000
marks_bytes:             58656
comment:              
is_in_partition_key:     0
is_in_sorting_key:       0
is_in_primary_key:       0
is_in_sampling_key:      0
compression_codec:    
*/



/****** Delta, LZ4 ******/

ALTER TABLE array_codec_test MODIFY COLUMN arr Array(UInt64) CODEC (Delta, LZ4);

OPTIMIZE TABLE array_codec_test FINAL
--0 rows in set. Elapsed: 4.577 sec.

SELECT * FROM system.columns WHERE (table = 'array_codec_test') AND (name = 'arr')

/*
Row 1:
──────
database:                default
table:                   array_codec_test
name:                    arr
type:                    Array(UInt64)
position:                2
default_kind:         
default_expression:   
data_compressed_bytes:   32458310
data_uncompressed_bytes: 8080000000
marks_bytes:             58656
comment:              
is_in_partition_key:     0
is_in_sorting_key:       0
is_in_primary_key:       0
is_in_sampling_key:      0
compression_codec:       CODEC(Delta(8), LZ4)
*/

```
# 13\.2 \- Codecs speed

Codecs speed
```
create table test_codec_speed engine=MergeTree
ORDER BY tuple()
as select cast(now() + rand()%2000 + number, 'DateTime') as x from numbers(1000000000);

option 1: CODEC(LZ4) (same as default)
option 2: CODEC(DoubleDelta) (`alter table test_codec_speed modify column x DateTime CODEC(DoubleDelta)`);
option 3: CODEC(T64, LZ4) (`alter table test_codec_speed modify column x DateTime CODEC(T64, LZ4)`)
option 4: CODEC(Delta, LZ4) (`alter table test_codec_speed modify column x DateTime CODEC(Delta, LZ4)`)
option 5: CODEC(ZSTD(1)) (`alter table test_codec_speed modify column x DateTime CODEC(ZSTD(1))`)
option 6: CODEC(T64, ZSTD(1)) (`alter table test_codec_speed modify column x DateTime CODEC(T64, ZSTD(1))`)
option 7: CODEC(Delta, ZSTD(1)) (`alter table test_codec_speed modify column x DateTime CODEC(Delta, ZSTD(1))`)
option 8: CODEC(T64, LZ4HC(1)) (`alter table test_codec_speed modify column x DateTime CODEC(T64, LZ4HC(1))`)
option 9: CODEC(Gorilla) (`alter table test_codec_speed modify column x DateTime CODEC(Gorilla)`)

Result may be not 100% reliable (checked on my laptop, need to be repeated in lab environment)


OPTIMIZE TABLE test_codec_speed FINAL (second run - i.e. read + write the same data)
1) 17 sec.
2) 30 sec.
3) 16 sec
4) 17 sec
5) 29 sec
6) 24 sec
7) 31 sec
8) 35 sec
9) 19 sec

compressed size
1) 3181376881
2) 2333793699
3) 1862660307
4) 3408502757
5) 2393078266
6) 1765556173
7) 2176080497
8) 1810471247
9) 2109640716

select max(x) from test_codec_speed
1) 0.597
2) 2.756 :(
3) 1.168
4) 0.752
5) 1.362
6) 1.364
7) 1.752
8) 1.270
9) 1.607

```
# 13\.3 \- How to test different compression codecs

How to test different compression codecs## Example

Create test\_table based on the source table.


```
CREATE TABLE test_table AS source_table ENGINE=MergeTree() PARTITION BY ...;

```
If the source table has Replicated\*MergeTree engine, you would need to change it to non\-replicated.

Attach one partition with data from the source table to test\_table.


```
ALTER TABLE test_table ATTACH PARTITION ID '20210120' FROM source_table;

```
You can modify the column or create a new one based on the old column value.


```
ALTER TABLE test_table MODIFY COLUMN column_a CODEC(ZSTD(2));
ALTER TABLE test_table ADD COLUMN column_new UInt32
                         DEFAULT toUInt32OrZero(column_old) CODEC(T64,LZ4);

```
After that, you would need to populate changed columns with data.


```
ALTER TABLE test_table UPDATE column_a=column_a, column_new=column_new WHERE 1;

```
You can look status of mutation via the `system.mutations` table


```
SELECT * FROM system.mutations;

```
And it’s also possible to kill mutation if there are some problems with it.


```
KILL MUTATION WHERE ...

```
## Useful queries


```
SELECT
    database,
    table,
    count() AS parts,
    uniqExact(partition_id) AS partition_cnt,
    sum(rows),
    formatReadableSize(sum(data_compressed_bytes) AS comp_bytes) AS comp,
    formatReadableSize(sum(data_uncompressed_bytes) AS uncomp_bytes) AS uncomp,
    uncomp_bytes / comp_bytes AS ratio
FROM system.parts
WHERE active
GROUP BY
    database,
    table
ORDER BY comp_bytes DESC

```

```
SELECT
  database,
  table,
  column,
  type,
  sum(rows) AS rows,
  sum(column_data_compressed_bytes) AS compressed_bytes,
  formatReadableSize(compressed_bytes) AS compressed,
  formatReadableSize(sum(column_data_uncompressed_bytes)) AS uncompressed,
  sum(column_data_uncompressed_bytes) / compressed_bytes AS ratio,
  any(compression_codec) AS codec
FROM system.parts_columns AS pc
LEFT JOIN system.columns AS c
ON (pc.database = c.database) AND (c.table = pc.table) AND (c.name = pc.column)
WHERE (database LIKE '%') AND (table LIKE '%') AND active
GROUP BY
  database,
  table,
  column,
  type
ORDER BY database, table, sum(column_data_compressed_bytes) DESC

```
# 14 \- Dictionaries vs LowCardinality

Dictionaries vs LowCardinalityQ. I think I’m still trying to understand how de\-normalized is okay \- with my relational mindset, I want to move repeated string fields into their own table, but I’m not sure to what extent this is necessary

I will look at LowCardinality in more detail \- I think it may work well here

A. If it’s a simple repetition, which you don’t need to manipulate/change in future \- LowCardinality works great, and you usually don’t need to increase the system complexity by introducing dicts.

For example: name of team ‘Manchester United’ will rather not be changed, and even if it will you can keep the historical records with historical name. So normalization here (with some dicts) is very optional, and de\-normalized approach with LowCardinality is good \& simpler alternative.

From the other hand: if data can be changed in future, and that change should impact the reports, then normalization may be a big advantage.

For example if you need to change the used currency rare every day\- it would be quite stupid to update all historical records to apply the newest exchange rate. And putting it to dict will allow to do calculations with latest exchange rate at select time.

For dictionary it’s possible to mark some of the attributes as injective. An attribute is called injective if different attribute values correspond to different keys. It would allow ClickHouse® to replace dictGet call in GROUP BY with cheap dict key.

# 15 \- Flattened table

Flattened tableIt’s possible to use dictionaries for populating columns of fact table.


```
CREATE TABLE customer
(
    `customer_id` UInt32,
    `first_name` String,
    `birth_date` Date,
    `sex` Enum('M' = 1, 'F' = 2)
)
ENGINE = MergeTree
ORDER BY customer_id

CREATE TABLE order
(
    `order_id` UInt32,
    `order_date` DateTime DEFAULT now(),
    `cust_id` UInt32,
    `amount` Decimal(12, 2)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(order_date)
ORDER BY (order_date, cust_id, order_id)

INSERT INTO customer VALUES(1, 'Mike', now() - INTERVAL 30 YEAR, 'M');
INSERT INTO customer VALUES(2, 'Boris', now() - INTERVAL 40 YEAR, 'M');
INSERT INTO customer VALUES(3, 'Sofie', now() - INTERVAL 24 YEAR, 'F');

INSERT INTO order (order_id, cust_id, amount) VALUES(50, 1, 15);
INSERT INTO order (order_id, cust_id, amount) VALUES(30, 1, 10);

SELECT * EXCEPT 'order_date'
FROM order

┌─order_id─┬─cust_id─┬─amount─┐
│       30 │       1 │  10.00 │
│       50 │       1 │  15.00 │
└──────────┴─────────┴────────┘

CREATE DICTIONARY customer_dict
(
    `customer_id` UInt32,
    `first_name` String,
    `birth_date` Date,
    `sex` UInt8
)
PRIMARY KEY customer_id
SOURCE(CLICKHOUSE(TABLE 'customer'))
LIFETIME(MIN 0 MAX 300)
LAYOUT(FLAT)

ALTER TABLE order
  ADD COLUMN `cust_first_name` String DEFAULT dictGetString('default.customer_dict', 'first_name', toUInt64(cust_id)),
  ADD COLUMN `cust_sex` Enum('M' = 1, 'F' = 2) DEFAULT dictGetUInt8('default.customer_dict', 'sex', toUInt64(cust_id)),
    ADD COLUMN `cust_birth_date` Date DEFAULT dictGetDate('default.customer_dict', 'birth_date', toUInt64(cust_id));

INSERT INTO order (order_id, cust_id, amount) VALUES(10, 3, 30);
INSERT INTO order (order_id, cust_id, amount) VALUES(20, 3, 60);
INSERT INTO order (order_id, cust_id, amount) VALUES(40, 2, 20);

SELECT * EXCEPT 'order_date'
FROM order
FORMAT PrettyCompactMonoBlock

┌─order_id─┬─cust_id─┬─amount─┬─cust_first_name─┬─cust_sex─┬─cust_birth_date─┐
│       30 │       1 │  10.00 │ Mike            │ M        │      1991-08-05 │
│       50 │       1 │  15.00 │ Mike            │ M        │      1991-08-05 │
│       10 │       3 │  30.00 │ Sofie           │ F        │      1997-08-05 │
│       40 │       2 │  20.00 │ Boris           │ M        │      1981-08-05 │
│       20 │       3 │  60.00 │ Sofie           │ F        │      1997-08-05 │
└──────────┴─────────┴────────┴─────────────────┴──────────┴─────────────────┘

ALTER TABLE customer UPDATE birth_date = now() - INTERVAL 35 YEAR WHERE customer_id=2;

SYSTEM RELOAD DICTIONARY customer_dict;

ALTER TABLE order
    UPDATE cust_birth_date = dictGetDate('default.customer_dict', 'birth_date', toUInt64(cust_id)) WHERE 1
-- or if you do have track of changes it's possible to lower amount of dict calls
--  UPDATE cust_birth_date = dictGetDate('default.customer_dict', 'birth_date', toUInt64(cust_id)) WHERE customer_id = 2


SELECT * EXCEPT 'order_date'
FROM order
FORMAT PrettyCompactMonoBlock

┌─order_id─┬─cust_id─┬─amount─┬─cust_first_name─┬─cust_sex─┬─cust_birth_date─┐
│       30 │       1 │  10.00 │ Mike            │ M        │      1991-08-05 │
│       50 │       1 │  15.00 │ Mike            │ M        │      1991-08-05 │
│       10 │       3 │  30.00 │ Sofie           │ F        │      1997-08-05 │
│       40 │       2 │  20.00 │ Boris           │ M        │      1986-08-05 │
│       20 │       3 │  60.00 │ Sofie           │ F        │      1997-08-05 │
└──────────┴─────────┴────────┴─────────────────┴──────────┴─────────────────┘

```
`ALTER TABLE order UPDATE` would completely overwrite this column in table, so it’s not recommended to run it often.

# 16 \- Floats vs Decimals

Floats vs DecimalsFloat arithmetics is not accurate: [https://floating\-point\-gui.de/](https://floating-point-gui.de/)

In case you need accurate calculations you should use Decimal datatypes.

### Operations on floats are not associative


```
SELECT (toFloat64(100000000000000000.) + toFloat64(7.5)) - toFloat64(100000000000000000.) AS res

┌─res─┐
│   0 │
└─────┘


SELECT (toFloat64(100000000000000000.) - toFloat64(100000000000000000.)) + toFloat64(7.5) AS res

┌─res─┐
│ 7.5 │
└─────┘

```
### No problem with Decimals:


```
SELECT (toDecimal64(100000000000000000., 1) + toDecimal64(7.5, 1)) - toDecimal64(100000000000000000., 1) AS res

┌─res─┐
│ 7.5 │
└─────┘


SELECT (toDecimal64(100000000000000000., 1) - toDecimal64(100000000000000000., 1)) + toDecimal64(7.5, 1) AS res

┌─res─┐
│ 7.5 │
└─────┘

```
#### Warning

Because ClickHouse® uses MPP order of execution of a single query can vary on each run, and you can get slightly different results from the float column every time you run the query.

Usually, this deviation is small, but it can be significant when some kind of arithmetic operation is performed on very large and very small numbers at the same time.

### Some decimal numbers has no accurate float representation


```
SELECT sum(toFloat64(0.45)) AS res
FROM numbers(10000)

┌───────────────res─┐
│ 4499.999999999948 │
└───────────────────┘


SELECT sumKahan(toFloat64(0.45)) AS res
FROM numbers(10000)

┌──res─┐
│ 4500 │
└──────┘


SELECT toFloat32(0.6) * 6 AS res

┌────────────────res─┐
│ 3.6000001430511475 │
└────────────────────┘

```
### No problem with Decimal:


```
SELECT sum(toDecimal64(0.45, 2)) AS res
FROM numbers(10000)

┌──res─┐
│ 4500 │
└──────┘


SELECT toDecimal32(0.6, 1) * 6 AS res

┌─res─┐
│ 3.6 │
└─────┘

```
### Direct comparisons of floats may be impossible

The same number can have several floating\-point representations and because of that you should not compare Floats directly


```
SELECT (toFloat32(0.1) * 10) = (toFloat32(0.01) * 100) AS res

┌─res─┐
│   0 │
└─────┘


SELECT
    sumIf(0.1, number < 10) AS a,
    sumIf(0.01, number < 100) AS b,
    a = b AS a_eq_b
FROM numbers(100)

┌──────────────────a─┬──────────────────b─┬─a_eq_b─┐
│ 0.9999999999999999 │ 1.0000000000000004 │      0 │
└────────────────────┴────────────────────┴────────┘

```
See also

[https://randomascii.wordpress.com/2012/02/25/comparing\-floating\-point\-numbers\-2012\-edition/](https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/)
[https://stackoverflow.com/questions/4915462/how\-should\-i\-do\-floating\-point\-comparison](https://stackoverflow.com/questions/4915462/how-should-i-do-floating-point-comparison)
[https://stackoverflow.com/questions/2100490/floating\-point\-inaccuracy\-examples](https://stackoverflow.com/questions/2100490/floating-point-inaccuracy-examples)
[https://stackoverflow.com/questions/10371857/is\-floating\-point\-addition\-and\-multiplication\-associative](https://stackoverflow.com/questions/10371857/is-floating-point-addition-and-multiplication-associative)

But:

<https://github.com/ClickHouse/ClickHouse/issues/24909>

# 17 \- Ingestion performance and formats


```
clickhouse-client -q 'select toString(number) s, number n, number/1000 f from numbers(100000000) format TSV' > speed.tsv
clickhouse-client -q 'select toString(number) s, number n, number/1000 f from numbers(100000000) format RowBinary' > speed.RowBinary
clickhouse-client -q 'select toString(number) s, number n, number/1000 f from numbers(100000000) format Native' > speed.Native
clickhouse-client -q 'select toString(number) s, number n, number/1000 f from numbers(100000000) format CSV' > speed.csv
clickhouse-client -q 'select toString(number) s, number n, number/1000 f from numbers(100000000) format JSONEachRow' > speed.JSONEachRow
clickhouse-client -q 'select toString(number) s, number n, number/1000 f from numbers(100000000) format Parquet' > speed.parquet
clickhouse-client -q 'select toString(number) s, number n, number/1000 f from numbers(100000000) format Avro' > speed.avro

-- Engine=Null does not have I/O / sorting overhead
-- we test only formats parsing performance.

create table n (s String, n UInt64, f Float64) Engine=Null


-- clickhouse-client parses formats itself
-- it allows to see user CPU time -- time is used in a multithreaded application
-- another option is to disable parallelism `--input_format_parallel_parsing=0`
-- real -- wall / clock time.

time clickhouse-client -t -q 'insert into n format TSV' < speed.tsv
2.693  real  0m2.728s   user  0m14.066s

time clickhouse-client -t -q 'insert into n format RowBinary' < speed.RowBinary
3.744  real  0m3.773s   user  0m4.245s

time clickhouse-client -t -q 'insert into n format Native' < speed.Native
2.359  real  0m2.382s   user  0m1.945s

time clickhouse-client -t -q 'insert into n format CSV' < speed.csv
3.296  real  0m3.328s  user  0m18.145s

time clickhouse-client -t -q 'insert into n format JSONEachRow' < speed.JSONEachRow
8.872  real  0m8.899s  user  0m30.235s

time clickhouse-client -t -q 'insert into n format Parquet' < speed.parquet
4.905  real  0m4.929s   user  0m5.478s

time clickhouse-client -t -q 'insert into n format Avro' < speed.avro
11.491  real  0m11.519s  user  0m12.166s

```
As you can see the JSONEachRow is the worst format (user 0m30\.235s) for this synthetic dataset. Native is the best (user 0m1\.945s). TSV / CSV are good in wall time but spend a lot of CPU (user time).

# 18 \- IPs/masks

IPs/masks### How do I Store IPv4 and IPv6 Address In One Field?

There is a clean and simple solution for that. Any IPv4 has its unique IPv6 mapping:

- IPv4 IP address: 191\.239\.213\.197
- IPv4\-mapped IPv6 address: ::ffff:191\.239\.213\.197

#### Find IPs matching CIDR/network mask (IPv4\)


```
WITH IPv4CIDRToRange( toIPv4('10.0.0.1'), 8 ) as range
SELECT
  *
FROM values('ip IPv4',
               toIPv4('10.2.3.4'),
               toIPv4('192.0.2.1'),
               toIPv4('8.8.8.8'))
WHERE
   ip BETWEEN range.1 AND range.2;

```
#### Find IPs matching CIDR/network mask (IPv6\)


```
WITH IPv6CIDRToRange
     (
       toIPv6('2001:0db8:0000:85a3:0000:0000:ac1f:8001'),
       32
      ) as range
SELECT
  *
FROM values('ip IPv6',
               toIPv6('2001:db8::8a2e:370:7334'),
               toIPv6('::ffff:192.0.2.1'),
               toIPv6('::'))
WHERE
   ip BETWEEN range.1 AND range.2;

```
# 19 \- JSONAsString and Mat. View as JSON parser

JSONAsString and Mat. View as JSON parserTables with engine Null don’t store data but can be used as a source for materialized views.

JSONAsString a special input format which allows to ingest JSONs into a String column. If the input has several JSON objects (comma separated) they will be interpreted as separate rows. JSON can be multiline.


```
create table entrypoint(J String) Engine=Null;
create table datastore(a String, i Int64, f Float64) Engine=MergeTree order by a;

create materialized view jsonConverter to datastore
as select (JSONExtract(J, 'Tuple(String,Tuple(Int64,Float64))') as x),
        x.1 as a,
        x.2.1 as i,
        x.2.2 as f
from entrypoint;

$ echo '{"s": "val1", "b2": {"i": 42, "f": 0.1}}' | \
    clickhouse-client -q "insert into entrypoint format JSONAsString"

$ echo '{"s": "val1","b2": {"i": 33, "f": 0.2}},{"s": "val1","b2": {"i": 34, "f": 0.2}}' | \
   clickhouse-client -q "insert into entrypoint format JSONAsString"

SELECT * FROM datastore;
┌─a────┬──i─┬───f─┐
│ val1 │ 42 │ 0.1 │
└──────┴────┴─────┘
┌─a────┬──i─┬───f─┐
│ val1 │ 33 │ 0.2 │
│ val1 │ 34 │ 0.2 │
└──────┴────┴─────┘

```
See also: [JSONExtract to parse many attributes at a time](/altinity-kb-queries-and-syntax/jsonextract-to-parse-many-attributes-at-a-time/)

# 20 \- LowCardinality

LowCardinality## Settings

#### allow\_suspicious\_low\_cardinality\_types

In CREATE TABLE statement allows specifying LowCardinality modifier for types of small fixed size (8 or less). Enabling this may increase merge times and memory consumption.

#### low\_cardinality\_max\_dictionary\_size

default \- 8192

Maximum size (in rows) of shared global dictionary for LowCardinality type.

#### low\_cardinality\_use\_single\_dictionary\_for\_part

LowCardinality type serialization setting. If is true, than will use additional keys when global dictionary overflows. Otherwise, will create several shared dictionaries.

#### low\_cardinality\_allow\_in\_native\_format

Use LowCardinality type in Native format. Otherwise, convert LowCardinality columns to ordinary for select query, and convert ordinary columns to required LowCardinality for insert query.

#### output\_format\_arrow\_low\_cardinality\_as\_dictionary

Enable output LowCardinality type as Dictionary Arrow type

# 21 \- ClickHouse® Materialized Views

Making the most of this powerful ClickHouse® featureClickHouse® MATERIALIZED VIEWs behave like AFTER INSERT TRIGGER to the left\-most table listed in their SELECT statement and never read data from disk. Only rows that are placed to the RAM buffer by INSERT are read.

## Useful links

- ClickHouse Materialized Views Illuminated, Part 1:
	- [Blog post](https://altinity.com/blog/clickhouse-materialized-views-illuminated-part-1)
	- [Webinar recording](https://www.youtube.com/watch?app=desktop&v=j15dvPGzhyE)
- ClickHouse Materialized Views Illuminated, Part 2:
	- [Blog post](https://altinity.com/blog/clickhouse-materialized-views-illuminated-part-2)
	- [Webinar recording](https://www.youtube.com/watch?v=THDk625DGsQ)
	- [Slides](https://altinity.com/wp-content/uploads/2024/05/ClickHouse-Materialized-Views-The-Magic-Continues-1.pdf)
- Everything you should know about Materialized Views:
	- [Video](https://www.youtube.com/watch?v=ckChUkC3Pns&t=9353s)
	- [Annotated slides](https://den-crane.github.io/Everything_you_should_know_about_materialized_views_commented.pdf)

## Best practices

1. Use MATERIALIZED VIEW with TO syntax (explicit storage table)

First you create the table which will store the data calculated by MV explicitly, and after that create materialized view itself with TO syntax.


```
CREATE TABLE target ( ... ) Engine=[Replicated][Replacing/Summing/...]MergeTree ...;

CREATE MATERIALIZED VIEW mv_source2target TO target
AS SELECT ... FROM source;

```
That way it’s bit simpler to do schema migrations or build more complicated pipelines when one table is filled by several MV.

With engine\=Atomic it hard to map underlying table with the MV.
2. Avoid using POPULATE when creating MATERIALIZED VIEW on big tables.

Use manual backfilling (with the same query) instead.


	- With POPULATE the data ingested to the source table **during MV populating will not appear in MV**.
	- POPULATE doesn’t work with TO syntax.
	- With manual backfilling, you have much better control on the process \- you can do it in parts, adjust settings etc.
	- In case of some failure ‘in the middle (for example due to timeouts), it’s hard to understand the state of the MV.
```
CREATE MATERIALIZED VIEW mv_source2target TO target
AS SELECT ... FROM source WHERE cond > ...

INSERT INTO target SELECT ... FROM source WHERE cond < ...

```
This way you have full control backfilling process (you can backfill in smaller parts to avoid timeouts, do some cross\-checks / integrity\-checks, change some settings, etc.)

## FAQ

### Q. Can I attach MATERIALIZED VIEW to the VIEW, or engine\=Merge, or engine\=MySQL, etc.?

Since MATERIALIZED VIEWs are updated on every INSERT to the underlying table and you can not insert anything to the usual VIEW, the materialized view update will never be triggered.

Normally, you should build MATERIALIZED VIEWs on the top of the table with the MergeTree engine family.

### Q. I’ve created a materialized error with some error, and since it’s reading from Kafka, I don’t understand where the error is

Look into system.query\_views\_log table or server logs, or system.text\_log table. Also, see the next question.

### Q. How to debug misbehaving MATERIALIZED VIEW?

You can also attach the same MV to a dummy table with engine\=Null and do manual inserts to debug the behavior. In a similar way (as the Materialized view often contains some pieces of the application’s business logic), you can create tests for your schema.

#### Warning

Always test MATERIALIZED VIEWs first on staging or testing environmentsPossible test scenario:

1. create a copy of the original table `CREATE TABLE src_copy ... AS src`
2. create MV on that copy `CREATE MATERIALIZED VIEW ... AS SELECT ... FROM src_copy`
3. check if inserts to src\_copy work properly, and mv is properly filled. `INSERT INTO src_copy SELECT * FROM src LIMIT 100`
4. cleanup the temp stuff and recreate MV on real table.

### Q. Can I use subqueries / joins in MV?

It is possible but it is **a very bad idea** for most of the use cases\*\*.\*\*

So it will most probably work not as you expect and will hit insert performance significantly.

The MV will be attached (as AFTER INSERT TRIGGER) to the left\-most table in the MV SELECT statement, and it will ‘see’ only freshly inserted rows there. It will ‘see’ the whole set of rows of other tables, and the query will be executed EVERY TIME you do the insert to the left\-most table. That will impact the performance speed there significantly.
If you really need to update the MV with the left\-most table, not impacting the performance so much you can consider using dictionary / engine\=Join / engine\=Set for right\-hand table / subqueries (that way it will be always in memory, ready to use).

### Q. How are MVs executed sequentially or in parallel?

By default, the execution is sequential and alphabetical. It can be switched by [parallel\_view\_processing](https://clickhouse.com/docs/en/operations/settings/settings#parallel_view_processing)
.

Parallel processing could be helpful if you have a lot of spare CPU power (cores) and want to utilize it. Add the setting to the insert statement or to the user profile. New blocks created by MVs will also follow the squashing logic similar to the one used in the insert, but they will use the min\_insert\_block\_size\_rows\_for\_materialized\_views and min\_insert\_block\_size\_bytes\_for\_materialized\_views settings.

### Q. How to alter MV implicit storage (w/o TO syntax)

1. take the existing MV definition


```
SHOW CREATE TABLE dbname.mvname;

```
Adjust the query in the following manner:


	- replace ‘CREATE MATERIALIZED VIEW’ to ‘ATTACH MATERIALIZED VIEW’
	- add needed columns;
2. Detach materialized view with the command:


```
DETACH TABLE dbname.mvname ON CLUSTER cluster_name;

```
3. Add the needed column to the underlying ReplicatedAggregatingMergeTree table


```
-- if the Materialized view was created without TO keyword
ALTER TABLE dbname.`.inner.mvname` ON CLUSTER cluster_name add column tokens AggregateFunction(uniq, UInt64);
-- othewise just alter the target table used in `CREATE MATERIALIZED VIEW ...`  `TO ...` clause

```
4. attach MV back using the query you create at p. 1\.


```
ATTACH MATERIALIZED VIEW dbname.mvname ON CLUSTER cluster_name
(
    /* ... */
    `tokens` AggregateFunction(uniq, UInt64)
)
ENGINE = ReplicatedAggregatingMergeTree(...)
ORDER BY ...
AS
SELECT
    /* ... */
    uniqState(rand64()) as tokens
FROM /* ... */
GROUP BY /* ... */

```

As you can see that operation is NOT atomic, so the safe way is to stop data ingestion during that procedure.

If you have version 19\.16\.13 or newer you can change the order of step 2 and 3 making the period when MV is detached and not working shorter (related issue <https://github.com/ClickHouse/ClickHouse/issues/7878>
).

See also:

- <https://github.com/ClickHouse/ClickHouse/issues/1226>
- <https://github.com/ClickHouse/ClickHouse/pull/7533>
# 21\.1 \- Idempotent inserts into a materialized view

How to make idempotent inserts into a materialized view".## Why inserts into materialized views are not idempotent?

ClickHouse® still does not have transactions. They were to be implemented around 2022Q2 but still not in the roadmap.

Because of ClickHouse materialized view is a trigger. And an insert into a table and an insert into a subordinate materialized view it’s two different inserts so they are not atomic altogether.

And insert into a materialized view may fail after the successful insert into the table. In case of any failure a client gets the error about failed insertion.
You may enable insert\_deduplication (it’s enabled by default for Replicated engines) and repeat the insert with an idea to archive idempotate insertion,
and insertion will be skipped into the source table because of deduplication but it will be skipped for materialized view as well because
by default materialized view inherits deduplication from the source table.
It’s controlled by a parameter `deduplicate_blocks_in_dependent_materialized_views` [https://clickhouse.com/docs/en/operations/settings/settings/\#settings\-deduplicate\-blocks\-in\-dependent\-materialized\-views](https://clickhouse.com/docs/en/operations/settings/settings/#settings-deduplicate-blocks-in-dependent-materialized-views)

If your materialized view is wide enough and always has enough data for consistent deduplication then you can enable `deduplicate_blocks_in_dependent_materialized_views`.
Or you may add information for deduplication (some unique information / insert identifier).

### Example 1\. Inconsistency with deduplicate\_blocks\_in\_dependent\_materialized\_views 0


```
create table test (A Int64, D Date) 
Engine =  ReplicatedMergeTree('/clickhouse/{cluster}/tables/{table}','{replica}') 
partition by toYYYYMM(D) order by A;

create materialized view test_mv 
Engine = ReplicatedSummingMergeTree('/clickhouse/{cluster}/tables/{table}','{replica}') 
partition by D order by D as 
select D, count() CNT from test group by D;

set max_partitions_per_insert_block=1; -- trick to fail insert into MV.

insert into test select number, today()+number%3 from numbers(100);
   DB::Exception: Received from localhost:9000. DB::Exception: Too many partitions 

select count() from test;
┌─count()─┐
│     100 │  -- Insert was successful into the test table
└─────────┘

select sum(CNT) from test_mv;
0 rows in set. Elapsed: 0.001 sec.   -- Insert was unsuccessful into the test_mv table (DB::Exception)

-- Let's try to retry insertion
set max_partitions_per_insert_block=100; -- disable trick
insert into test select number, today()+number%3 from numbers(100); -- insert retry / No error
 
select count() from test;
┌─count()─┐
│     100 │  -- insert was deduplicated
└─────────┘
 
select sum(CNT) from test_mv;
0 rows in set. Elapsed: 0.001 sec.    -- Inconsistency! Unfortunatly insert into MV was deduplicated as well

```
That is another example \- <https://github.com/ClickHouse/ClickHouse/issues/56642>

### Example 2\. Inconsistency with deduplicate\_blocks\_in\_dependent\_materialized\_views 1


```
create table test (A Int64, D Date) 
Engine =  ReplicatedMergeTree('/clickhouse/{cluster}/tables/{table}','{replica}') 
partition by toYYYYMM(D) order by A;

create materialized view test_mv 
Engine = ReplicatedSummingMergeTree('/clickhouse/{cluster}/tables/{table}','{replica}') 
partition by D order by D as 
select D, count() CNT from test group by D;

set deduplicate_blocks_in_dependent_materialized_views=1;

insert into test select number, today() from numbers(100);      -- insert 100 rows
insert into test select number, today() from numbers(100,100);  -- insert another 100 rows


select count() from test;
┌─count()─┐
│     200 │  -- 200 rows in the source test table
└─────────┘

select sum(CNT) from test_mv;
┌─sum(CNT)─┐
│      100 │ -- Inconsistency! The second insert was falsely deduplicated because count() was = 100 both times 
└──────────┘

```
### Example 3\. Solution: no inconsistency with deduplicate\_blocks\_in\_dependent\_materialized\_views 1

Let’s add some artificial `insert_id` generated by the source of inserts:


```
create table test (A Int64, D Date, insert_id Int64) 
Engine =  ReplicatedMergeTree('/clickhouse/{cluster}/tables/{table}','{replica}') 
partition by toYYYYMM(D) order by A;

create materialized view test_mv 
Engine = ReplicatedSummingMergeTree('/clickhouse/{cluster}/tables/{table}','{replica}') 
partition by D order by D as 
select D, count() CNT, any(insert_id) insert_id from test group by D;

set deduplicate_blocks_in_dependent_materialized_views=1;

insert into test select number, today(), 333 from numbers(100);
insert into test select number, today(), 444 from numbers(100,100);


select count() from test;
┌─count()─┐
│     200 │
└─────────┘

select sum(CNT) from test_mv;
┌─sum(CNT)─┐
│      200 │ -- no inconsistency, the second (100) was not deduplicated because 333<>444
└──────────┘

set max_partitions_per_insert_block=1;   -- trick to fail insert into MV.
insert into test select number, today()+number%3, 555 from numbers(100);  
    DB::Exception: Too many partitions for single INSERT block (more than 1)


select count() from test;
┌─count()─┐
│     300 │  -- insert is successful into the test table
└─────────┘

select sum(CNT) from test_mv;
┌─sum(CNT)─┐
│      200 │  -- insert was unsuccessful into the test_mv table
└──────────┘

set max_partitions_per_insert_block=100;
insert into test select number, today()+number%3, 555 from numbers(100);   -- insert retry


select count() from test;
┌─count()─┐
│     300 │  -- insert was deduplicated
└─────────┘

select sum(CNT) from test_mv;
┌─sum(CNT)─┐
│      300 │  -- No inconsistency! Insert was not deduplicated.
└──────────┘

```
Idea how to fix it in ClickHouse source code <https://github.com/ClickHouse/ClickHouse/issues/30240>

### Fake (unused) metric to add uniqueness.


```
create materialized view test_mv
   Engine = ReplicatedSummingMergeTree('/clickhouse/{cluster}/tables/{table}','{replica}') 
   partition by D
   order by D
  as
   select
     D,
     count() CNT,
     sum( cityHash(*) ) insert_id
  from test group by D;

```
# 21\.2 \- Backfill/populate MV in a controlled manner

Backfill/populate MV in a controlled mannerQ. How to populate MV create with TO syntax? INSERT INTO mv SELECT \* FROM huge\_table? Will it work if the source table has billions of rows?

A. single huge `insert ... select ...` actually will work, but it will take A LOT of time, and during that time lot of bad things can happen (lack of disk space, hard restart etc). Because of that, it’s better to do such backfill in a more controlled manner and in smaller pieces.

One of the best options is to fill one partition at a time, and if it breaks you can drop the partition and refill it.

If you need to construct a single partition from several sources \- then the following approach may be the best.


```
CREATE TABLE mv_import AS mv;
INSERT INTO mv_import SELECT * FROM huge_table WHERE toYYYYMM(ts) = 202105;
/* or other partition expression*/

/* that insert select may take a lot of time, if something bad will happen
  during that - just truncate mv_import and restart the process */

/* after successful loading of mv_import do*/
ALTER TABLE mv ATTACH PARTITION ID '202105' FROM  mv_import;

```
See also [the ClickHouse® documentation on Manipulating Partitions and Parts](https://clickhouse.com/docs/en/sql-reference/statements/alter/partition)
.

Q. I still do not have enough RAM to GROUP BY the whole partition.

A. Push aggregating to the background during MERGES

There is a modified version of MergeTree Engine, called [AggregatingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree)
. That engine has additional logic that is applied to rows with the same set of values in columns that are specified in the table’s ORDER BY expression. All such rows are aggregated to only one rows using the aggregating functions defined in the column definitions. There are two “special” column types, designed specifically for that purpose:

- [AggregatingFunction](https://clickhouse.com/docs/en/sql-reference/data-types/aggregatefunction)
- [SimpleAggregatingFunction](https://clickhouse.com/docs/en/sql-reference/data-types/simpleaggregatefunction)

INSERT … SELECT operating over the very large partition will create data parts by 1M rows (min\_insert\_block\_size\_rows), those parts will be aggregated during the merge process the same way as GROUP BY do it, but the number of rows will be much less than the total rows in the partition and RAM usage too. Merge combined with GROUP BY will create a new part with a much less number of rows. That data part possibly will be merged again with other data, but the number of rows will be not too big.


```
CREATE TABLE mv_import (
  id UInt64,
  ts SimpleAggregatingFunction(max,DateTime),         -- most fresh
  v1 SimpleAggregatingFunction(sum,UInt64),           -- just sum
  v2 SimpleAggregatingFunction(max,String),           -- some not empty string
  v3 AggregatingFunction(argMax,String,ts)            -- last value
) ENGINE = AggregatingMergeTree()
ORDER BY id;

INSERT INTO mv_import
SELECT id,                              -- ORDER BY column
   ts,v1,v2,                            -- state for SimpleAggregatingFunction the same as value
   initializeAggregation('argMaxState',v3,ts)  -- we need to convert from values to States for columns with AggregatingFunction type
FROM huge_table
WHERE toYYYYMM(ts) = 202105;

```
Actually, the first GROUP BY run will happen just before 1M rows will be stored on disk as a data part. You may disable that behavior by switching off [optimize\_on\_insert](https://clickhouse.com/docs/en/operations/settings/settings#optimize-on-insert)
setting if you have heavy calculations during aggregation.

You may attach such a table (with AggregatingFunction columns) to the main table as in the example above, but if you don’t like having States in the Materialized Table, data should be finalized and converted back to normal values. In that case, you have to move data by INSERT … SELECT again:


```
INSERT INTO MV
SELECT id,ts,v1,v2,  -- nothing special for SimpleAggregatingFunction columns
  finalizeAggregation(v3)
from mv_import FINAL

```
The last run of GROUP BY will happen during FINAL execution and AggregatingFunction types converted back to normal values. To simplify retries after failures an additional temporary table and the same trick with ATTACH could be applied.
