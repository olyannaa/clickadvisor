# Skip indexes \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-queries-and-syntax/skip-indexes/).

# Skip indexes

Skip indexes- 1: [Example: minmax](#pg-13419932d1c1660a145e1463d236cc97)
- 2: [Skip index bloom\_filter Example](#pg-29ad75a8cef533fb7967d904bf81eccb)
- 3: [Skip indexes examples](#pg-42b18d86b2e42f476b69091e7758ef4c)

ClickHouse® provides a type of index that in specific circumstances can significantly improve query speed. These structures are labeled “skip” indexes because they enable ClickHouse to skip reading significant chunks of data that are guaranteed to have no matching values.

# 1 \- Example: minmax

Example: minmax### Use cases

#### Strong correlation between column from table ORDER BY / PARTITION BY key and other column which is regularly being used in WHERE condition

Good example is incremental ID which increasing with time.


```
CREATE TABLE skip_idx_corr
(
    `key` UInt32,
    `id` UInt32,
    `ts` DateTime
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (key, id);

INSERT INTO skip_idx_corr SELECT
    rand(),
    number,
    now() + intDiv(number, 10)
FROM numbers(100000000);

SELECT count()
FROM skip_idx_corr
WHERE id = 6000000

1 rows in set. Elapsed: 0.167 sec. Processed 100.00 million rows, 400.00 MB
(599.96 million rows/s., 2.40 GB/s.)


ALTER TABLE skip_idx_corr ADD INDEX id_idx id TYPE minmax GRANULARITY 10;
ALTER TABLE skip_idx_corr MATERIALIZE INDEX id_idx;


SELECT count()
FROM skip_idx_corr
WHERE id = 6000000

1 rows in set. Elapsed: 0.017 sec. Processed 6.29 million rows, 25.17 MB
(359.78 million rows/s., 1.44 GB/s.)

```
#### Multiple Date/DateTime columns can be used in WHERE conditions

Usually it could happen if you have separate Date and DateTime columns and different column being used in PARTITION BY expression and in WHERE condition. Another possible scenario when you have multiple DateTime columns which have pretty the same date or even time.


```
CREATE TABLE skip_idx_multiple
(
    `key` UInt32,
    `date` Date,
    `time` DateTime,
    `created_at` DateTime,
    `inserted_at` DateTime
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(date)
ORDER BY (key, time);

INSERT INTO skip_idx_multiple SELECT
    number,
    toDate(x),
    now() + intDiv(number, 10) AS x,
    x - (rand() % 100),
    x + (rand() % 100)
FROM numbers(100000000);


SELECT count()
FROM skip_idx_multiple
WHERE date > (now() + toIntervalDay(105));

1 rows in set. Elapsed: 0.048 sec. Processed 14.02 million rows, 28.04 MB
(290.96 million rows/s., 581.92 MB/s.)

SELECT count()
FROM skip_idx_multiple
WHERE time > (now() + toIntervalDay(105));

1 rows in set. Elapsed: 0.188 sec. Processed 100.00 million rows, 400.00 MB
(530.58 million rows/s., 2.12 GB/s.)

SELECT count()
FROM skip_idx_multiple
WHERE created_at > (now() + toIntervalDay(105));

1 rows in set. Elapsed: 0.400 sec. Processed 100.00 million rows, 400.00 MB
(250.28 million rows/s., 1.00 GB/s.)


ALTER TABLE skip_idx_multiple ADD INDEX time_idx time TYPE minmax GRANULARITY 1000;
ALTER TABLE skip_idx_multiple MATERIALIZE INDEX time_idx;

SELECT count()
FROM skip_idx_multiple
WHERE time > (now() + toIntervalDay(105));

1 rows in set. Elapsed: 0.036 sec. Processed 14.02 million rows, 56.08 MB
(391.99 million rows/s., 1.57 GB/s.)


ALTER TABLE skip_idx_multiple ADD INDEX created_at_idx created_at TYPE minmax GRANULARITY 1000;
ALTER TABLE skip_idx_multiple MATERIALIZE INDEX created_at_idx;

SELECT count()
FROM skip_idx_multiple
WHERE created_at > (now() + toIntervalDay(105));

1 rows in set. Elapsed: 0.076 sec. Processed 14.02 million rows, 56.08 MB
(184.90 million rows/s., 739.62 MB/s.)

```
#### Condition in query trying to filter outlier value


```
CREATE TABLE skip_idx_outlier
(
    `key` UInt32,
    `ts` DateTime,
    `value` UInt32
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (key, ts);

INSERT INTO skip_idx_outlier SELECT
    number,
    now(),
    rand() % 10
FROM numbers(10000000);

INSERT INTO skip_idx_outlier SELECT
    number,
    now(),
    20
FROM numbers(10);

SELECT count()
FROM skip_idx_outlier
WHERE value > 15;

1 rows in set. Elapsed: 0.059 sec. Processed 10.00 million rows, 40.00 MB
(170.64 million rows/s., 682.57 MB/s.)

ALTER TABLE skip_idx_outlier ADD INDEX value_idx value TYPE minmax GRANULARITY 10;
ALTER TABLE skip_idx_outlier MATERIALIZE INDEX value_idx;

SELECT count()
FROM skip_idx_outlier
WHERE value > 15;

1 rows in set. Elapsed: 0.004 sec.

```
# 2 \- Skip index bloom\_filter Example

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

# 3 \- Skip indexes examples

## bloom\_filter


```
create table bftest (k Int64, x Int64) Engine=MergeTree order by k;

insert into bftest select number, rand64()%565656 from numbers(10000000);
insert into bftest select number, rand64()%565656 from numbers(100000000);

select count() from bftest where x = 42;
┌─count()─┐
│     201 │
└─────────┘
1 rows in set. Elapsed: 0.243 sec. Processed 110.00 million rows


alter table bftest add index ix1(x) TYPE bloom_filter GRANULARITY 1;

alter table bftest materialize index ix1;


select count() from bftest where x = 42;
┌─count()─┐
│     201 │
└─────────┘
1 rows in set. Elapsed: 0.056 sec. Processed 3.68 million rows

```
## minmax


```
create table bftest (k Int64, x Int64) Engine=MergeTree order by k;

-- data is in x column is correlated with the primary key
insert into bftest select number, number * 2 from numbers(100000000);

alter table bftest add index ix1(x) TYPE minmax GRANULARITY 1;
alter table bftest materialize index ix1;

select count() from bftest where x = 42;
1 rows in set. Elapsed: 0.004 sec. Processed 8.19 thousand rows

```
## projection


```
create table bftest (k Int64, x Int64, S String) Engine=MergeTree order by k;
insert into bftest select number, rand64()%565656, '' from numbers(10000000);
insert into bftest select number, rand64()%565656, '' from numbers(100000000);
alter table bftest add projection p1 (select k,x order by x);
alter table bftest materialize projection p1 settings mutations_sync=1;
set allow_experimental_projection_optimization=1 ;

-- projection
select count() from bftest where x = 42;
1 rows in set. Elapsed: 0.002 sec. Processed 24.58 thousand rows

-- no projection
select * from bftest where x = 42 format Null;
0 rows in set. Elapsed: 0.432 sec. Processed 110.00 million rows

-- projection
select * from bftest where k in (select k from bftest where x = 42) format Null;
0 rows in set. Elapsed: 0.316 sec. Processed 1.50 million rows

```
