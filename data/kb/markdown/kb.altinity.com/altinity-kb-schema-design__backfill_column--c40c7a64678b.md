# Column backfilling with alter/update using a dictionary \| Altinity® Knowledge Base for ClickHouse®


1. [Schema design](/altinity-kb-schema-design/)
2. Column backfilling from dictionary
# Column backfilling with alter/update using a dictionary

## Column backfilling

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
Last modified 2024\.07\.30: [Site cleanup, mostly minor changes (a4a9639\)](https://github.com/Altinity/altinityknowledgebase/commit/a4a96398d6e97ac2935110b426947487e2e202d9)
