# ClickHouse® Materialized Views \| Altinity® Knowledge Base for ClickHouse®


1. [Schema design](/altinity-kb-schema-design/)
2. Materialized Views
# ClickHouse® Materialized Views

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



---

##### [Idempotent inserts into a materialized view](/altinity-kb-schema-design/materialized-views/idempotent_inserts_mv/)

How to make idempotent inserts into a materialized view".

##### [Backfill/populate MV in a controlled manner](/altinity-kb-schema-design/materialized-views/backfill-populate-mv-in-a-controlled-manner/)

Last modified 2025\.04\.09: [SEO improvements to make content easier to find (3b6158c)](https://github.com/Altinity/altinityknowledgebase/commit/3b6158c2a22100a97198a07184f2bce18e189d37)
