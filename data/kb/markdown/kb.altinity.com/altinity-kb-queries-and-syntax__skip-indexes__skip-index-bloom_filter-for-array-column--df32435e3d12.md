# Skip index bloom\_filter Example \| Altinity® Knowledge Base for ClickHouse®


1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. [Skip indexes](/altinity-kb-queries-and-syntax/skip-indexes/)
3. Skip index bloom\_filter Example
# Skip index bloom\_filter Example

tested with ClickHouse® 20\.8\.17\.25

[https://clickhouse.com/docs/en/engines/table\-engines/mergetree\-family/mergetree/\#table\_engine\-mergetree\-data\_skipping\-indexes](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree/#table_engine-mergetree-data_skipping-indexes)

### Let’s create test data


```
create table bftest (k Int64, x Array(Int64))
Engine=MergeTree order by k;

insert into bftest select number,
    arrayMap(i->rand64()%565656, range(10)) from numbers(10000000);
insert into bftest select number,
    arrayMap(i->rand64()%565656, range(10)) from numbers(100000000);

```
### Base point (no index)


```
select count() from bftest where has(x, 42);
┌─count()─┐
│     186 │
└─────────┘
1 rows in set. Elapsed: 0.495 sec.
    Processed 110.00 million rows, 9.68 GB (222.03 million rows/s., 19.54 GB/s.)

select count() from bftest where has(x, -42);
┌─count()─┐
│       0 │
└─────────┘
1 rows in set. Elapsed: 0.505 sec.
    Processed 110.00 million rows, 9.68 GB (217.69 million rows/s., 19.16 GB/s.)

```
As you can see ClickHouse read **110\.00 million rows** and the query elapsed **Elapsed: 0\.505 sec**.

### Let’s add an index


```
alter table bftest add index ix1(x) TYPE bloom_filter GRANULARITY 3;

-- GRANULARITY 3 means how many table granules will be in the one index granule
-- In our case 1 granule of skip index allows to check and skip 3*8192 rows.
-- Every dataset is unique sometimes GRANULARITY 1 is better, sometimes
-- GRANULARITY 10.
-- Need to test on the real data.

optimize table bftest final;
-- I need to optimize my table because an index is created for only
-- new parts (inserted or merged)
-- optimize table final re-writes all parts, but with an index.
-- probably in your production you don't need to optimize
-- because your data is rotated frequently.
-- optimize is a heavy operation, better never run optimize table final in a
-- production.

```
### test bloom\_filter GRANULARITY 3


```
select count() from bftest where has(x, 42);
┌─count()─┐
│     186 │
└─────────┘
1 rows in set. Elapsed: 0.063 sec.
    Processed 5.41 million rows, 475.79 MB (86.42 million rows/s., 7.60 GB/s.)

select count() from bftest where has(x, -42);
┌─count()─┐
│       0 │
└─────────┘
1 rows in set. Elapsed: 0.042 sec.
   Processed 1.13 million rows, 99.48 MB (26.79 million rows/s., 2.36 GB/s.)

```
As you can see I got 10 times boost.

### Let’s try to reduce GRANULARITY to drop by 1 table granule


```
alter  table bftest drop index ix1;
alter table bftest add index ix1(x) TYPE bloom_filter GRANULARITY 1;
optimize table bftest final;

select count() from bftest where has(x, 42);
┌─count()─┐
│     186 │
└─────────┘
1 rows in set. Elapsed: 0.051 sec.
    Processed 3.64 million rows, 320.08 MB (71.63 million rows/s., 6.30 GB/s.)

select count() from bftest where has(x, -42);
┌─count()─┐
│       0 │
└─────────┘
1 rows in set. Elapsed: 0.050 sec.
    Processed 2.06 million rows, 181.67 MB (41.53 million rows/s., 3.65 GB/s.)

```
No improvement :(

### Let’s try to change the false/true probability of the bloom\_filter bloom\_filter(0\.05\)


```
alter  table bftest drop index ix1;
alter table bftest add index ix1(x) TYPE bloom_filter(0.05) GRANULARITY 3;
optimize table bftest final;

select count() from bftest where has(x, 42);
┌─count()─┐
│     186 │
└─────────┘
1 rows in set. Elapsed: 0.079 sec.
    Processed 8.95 million rows, 787.22 MB (112.80 million rows/s., 9.93 GB/s.)

select count() from bftest where has(x, -42);
┌─count()─┐
│       0 │
└─────────┘
1 rows in set. Elapsed: 0.058 sec.
    Processed 3.86 million rows, 339.54 MB (66.83 million rows/s., 5.88 GB/s.)

```
No improvement.

### bloom\_filter(0\.01\)


```
alter  table bftest drop index ix1;
alter table bftest add index ix1(x) TYPE bloom_filter(0.01) GRANULARITY 3;
optimize table bftest final;

select count() from bftest where has(x, 42);
┌─count()─┐
│     186 │
└─────────┘
1 rows in set. Elapsed: 0.069 sec.
    Processed 5.26 million rows, 462.82 MB (76.32 million rows/s., 6.72 GB/s.)

select count() from bftest where has(x, -42);
┌─count()─┐
│       0 │
└─────────┘
1 rows in set. Elapsed: 0.047 sec.
    Processed 737.28 thousand rows, 64.88 MB (15.72 million rows/s., 1.38 GB/s.)

```
Also no improvement :(

Outcome: I would use TYPE bloom\_filter GRANULARITY 3\.

Last modified 2025\.01\.16: [Streamlined page metadata, simplified directory structure (afe0f3c)](https://github.com/Altinity/altinityknowledgebase/commit/afe0f3c3e76e848e6941903e93f05dd41fccfea0)
