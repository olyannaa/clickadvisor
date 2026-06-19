# ClickHouse® Materialized Views \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-schema-design/materialized-views/).

# ClickHouse® Materialized Views

Making the most of this powerful ClickHouse® feature- 1: [Idempotent inserts into a materialized view](#pg-efd5546f247797daa53f929da20153b0)
- 2: [Backfill/populate MV in a controlled manner](#pg-7eccdd4920775fe5f6841654ebe7a03d)

ClickHouse® MATERIALIZED VIEWs behave like AFTER INSERT TRIGGER to the left\-most table listed in their SELECT statement and never read data from disk. Only rows that are placed to the RAM buffer by INSERT are read.

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
# 1 \- Idempotent inserts into a materialized view

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
# 2 \- Backfill/populate MV in a controlled manner

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
