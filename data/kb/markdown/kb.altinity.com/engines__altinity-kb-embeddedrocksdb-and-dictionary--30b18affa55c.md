# EmbeddedRocksDB \& dictionary \| Altinity® Knowledge Base for ClickHouse®


1. [Engines](/engines/)
2. EmbeddedRocksDB \& dictionary
# EmbeddedRocksDB \& dictionary

RocksDB is faster than
[MergeTree](/engines/mergetree-table-engine-family/)
on Key/Value queries because MergeTree primary key index is sparse. Probably it’s possible to speedup MergeTree by reducing `index_granularity`.

NVMe disk is used for the tests.

The main feature of RocksDB is instant updates. You can update a row **instantly** (microseconds):


```
select * from rocksDB where A=15645646;
┌────────A─┬─B────────────────────┐
│ 15645646 │ 12517841379565221195 │
└──────────┴──────────────────────┘
1 rows in set. Elapsed: 0.001 sec.

insert into rocksDB values (15645646, 'xxxx');
1 rows in set. Elapsed: 0.001 sec.

select * from rocksDB where A=15645646;
┌────────A─┬─B────┐
│ 15645646 │ xxxx │
└──────────┴──────┘
1 rows in set. Elapsed: 0.001 sec.

```
Let’s load 100 millions rows:


```
create table rocksDB(A UInt64, B String, primary key A) Engine=EmbeddedRocksDB();
insert into rocksDB select number, toString(cityHash64(number))
from numbers(100000000);

-- 0 rows in set. Elapsed: 154.559 sec. Processed 100.66 million rows, 805.28 MB (651.27 thousand rows/s., 5.21 MB/s.)
-- Size on disk: 1.5GB

create table mergeTreeDB(A UInt64, B String) Engine=MergeTree() order by A;
insert into mergeTreeDB select number, toString(cityHash64(number))
from numbers(100000000);

Size on disk: 973MB

```

```
CREATE DICTIONARY test_rocksDB(A UInt64,B String)
PRIMARY KEY A
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 TABLE rocksDB DB 'default'
         USER 'default'))
LAYOUT(DIRECT());

CREATE DICTIONARY test_mergeTreeDB(A UInt64,B String)
PRIMARY KEY A
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 TABLE mergeTreeDB DB 'default'
         USER 'default'))
LAYOUT(DIRECT());

```
## Direct queries to tables to request 10000 rows by a random key


```
select count() from (
select * from rocksDB where A in (select toUInt64(rand64()%100000000)
 from numbers(10000)))
Elapsed: 0.076 sec. Processed 10.00 thousand rows

select count() from (
select * from mergeTreeDB where A in (select toUInt64(rand64()%100000000)
  from numbers(10000)))
Elapsed: 0.202 sec. Processed 55.95 million rows

```
RocksDB as expected is much faster: **0\.076 sec.** VS **0\.202 sec.**

RocksDB processes less rows: **10\.00 thousand rows** VS **55\.95 million rows**

## dictGet – 100\.00 thousand random rows


```
select count() from (
   select dictGet( 'default.test_rocksDB', 'B', toUInt64(rand64()%100000000) )
   from numbers_mt(100000))
Elapsed: 0.786 sec. Processed 100.00 thousand rows

select count() from (
   select dictGet( 'default.test_mergeTreeDB', 'B', toUInt64(rand64()%100000000) )
   from numbers_mt(100000))
Elapsed: 3.160 sec. Processed 100.00 thousand rows

```
## dictGet – 1million random rows


```
select count() from (
   select dictGet( 'default.test_rocksDB', 'B', toUInt64(rand64()%100000000) )
   from numbers_mt(1000000))
Elapsed: 5.643 sec. Processed 1.00 million rows

select count() from (
   select dictGet( 'default.test_mergeTreeDB', 'B', toUInt64(rand64()%100000000) )
   from numbers_mt(1000000))
Elapsed: 31.111 sec. Processed 1.00 million rows

```
## dictGet – 1million random rows from Hashed


```
CREATE DICTIONARY test_mergeTreeDBHashed(A UInt64,B String)
PRIMARY KEY A
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 TABLE mergeTreeDB DB 'default'
         USER 'default'))
LAYOUT(Hashed())
LIFETIME(0);

0 rows in set. Elapsed: 46.564 sec.

┌─name───────────────────┬─type───┬─status─┬─element_count─┬─RAM──────┐
│ test_mergeTreeDBHashed │ Hashed │ LOADED │     100000000 │ 7.87 GiB │
└────────────────────────┴────────┴────────┴───────────────┴──────────┘

select count() from (
   select dictGet( 'default.test_mergeTreeDBHashed', 'B', toUInt64(rand64()%100000000) )
   from numbers_mt(1000000))
Elapsed: 0.079 sec. Processed 1.00 million rows

```
## dictGet – 1million random rows from SparseHashed


```
CREATE DICTIONARY test_mergeTreeDBSparseHashed(A UInt64,B String)
PRIMARY KEY A
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 TABLE mergeTreeDB DB 'default'
         USER 'default'))
LAYOUT(SPARSE_HASHED())
LIFETIME(0);
0 rows in set. Elapsed: 81.404 sec.

┌─name─────────────────────────┬─type─────────┬─status─┬─element_count─┬─RAM──────┐
│ test_mergeTreeDBSparseHashed │ SparseHashed │ LOADED │     100000000 │ 4.24 GiB │
└──────────────────────────────┴──────────────┴────────┴───────────────┴──────────┘

select count() from (
   select dictGet( 'default.test_mergeTreeDBSparseHashed', 'B', toUInt64(rand64()%100000000) )
   from numbers_mt(1000000))

Elapsed: 0.065 sec. Processed 1.00 million rows

```
Last modified 2024\.02\.01: [Fixed broken links, other housekeeping (33dff8b)](https://github.com/Altinity/altinityknowledgebase/commit/33dff8b40c62828a1baf7b31d3a22f87a0950e8c)
