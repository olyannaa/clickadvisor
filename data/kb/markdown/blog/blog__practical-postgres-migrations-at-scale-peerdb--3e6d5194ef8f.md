# Making large Postgres migrations practical: 1TB in 2 hours with PeerDB


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Making large Postgres migrations practical: 1TB in 2 hours with PeerDB

![](/_next/image?url=%2Fuploads%2FT02_EM_6_F031_P_U07_DEMQTYCV_d55dd9eefdb0_512_4438f24e85.jpeg&w=96&q=75)[Amogh Bharadwaj](/authors/amogh-bharadwaj)Feb 19, 2026 · 18 minutes readWe launched [Postgres managed by ClickHouse](https://clickhouse.com/cloud/postgres) in January, and with the enthusiasm around the project comes an important next step: enabling teams to migrate their existing Postgres databases quickly and with minimal downtime.


In this post we’ll walk through how [PeerDB](https://github.com/PeerDB-io/peerdb) enables fast, reliable Postgres migrations, at large scale. We will compare performance for a 1TB migration across 3 tools \- [pg\_dump](https://www.postgresql.org/docs/current/app-pgdump.html)/[pg\_restore](https://www.postgresql.org/docs/current/app-pgrestore.html), native [logical replication](https://www.postgresql.org/docs/current/logical-replication.html) and PeerDB. And we’ll look at the purpose\-built optimizations and features for Postgres migrations within PeerDB.


## Why PeerDB for Postgres migration? [\#](/blog/practical-postgres-migrations-at-scale-peerdb#why-peerdb-for-postgres-migration)


For many teams, online migration is critical for adoption. Databases range from hundreds of gigabytes to multiple terabytes, and production environments often cannot tolerate extended downtime. A viable online migration path must therefore deliver:


- High initial load throughput to efficiently copy existing data from source to target Postgres.
- Continuous change data capture (CDC) to keep both databases in sync.
- Ability to support a diverse set of real\-world PostgreSQL workloads, including support for complex data types, constraints, schema evolution, large [TOAST](https://www.postgresql.org/docs/current/storage-toast.html) columns and more.


While tools such as pg\_dump/pg\_restore, native logical replication, and [AWS DMS](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html) each serve specific use cases, they often involve trade\-offs in performance, observability, or operational complexity when applied to large, online migrations. We’ll quantify these trade\-offs in the upcoming benchmarking section.


PeerDB’s Postgres to Postgres migration capability is designed to address these constraints directly. It offers **high\-speed initial load** and continuous CDC while **supporting TOAST columns without requiring REPLICA IDENTITY FULL**, automatic **column additions,** and PeerDB is **fully open source**.


You can use it for **any Postgres to Postgres migration**, including self\-hosted, managed setups or across cloud providers.

## Benchmarking large Postgres migrations [\#](/blog/practical-postgres-migrations-at-scale-peerdb#benchmarking-large-postgres-migrations)


For most large\-scale migrations, the primary bottleneck is the **initial load**, i.e., copying existing data across all tables from source Postgres to target Postgres.


While ongoing change data capture (CDC) keeps systems in sync before cutover, the initial copy of historical data often covers the majority of the overall migration timeline. For datasets measured in terabytes, this phase can take days, and in some cases, weeks, depending on the tool.


Let’s compare performance across pg\_dump/pg\_restore, native logical replication and PeerDB for initial load.


### The setup [\#](/blog/practical-postgres-migrations-at-scale-peerdb#the-setup)


The benchmark setup was as follows:


- **Source database:** AWS RDS instance on Postgres 18 sized at db.r8g.2xlarge, 8 VCPUs, 64GB RAM, 12000 provisioned IOPS, gp3\.
- **Destination database:** Postgres managed by ClickHouse on Postgres 18, 8 VCPUs, 64GB RAM, NVMe backed with 1875 GB storage. This was also in AWS.
- **EC2:** Sized at [c5d.12xlarge](https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#InstanceTypes:instanceType=c5d.12xlarge), running ubuntu\-noble\-24\.04\-amd64


The above setup artifacts were all situated in the region us\-west\-2c.


### The data [\#](/blog/practical-postgres-migrations-at-scale-peerdb#the-data)


The dataset we used is the [firenibble database](https://github.com/PeerDB-io/ab-scale-testing/tree/main) which consists of a table with a variety of types. The benchmark was conducted on a single large table, as this reflects most real\-world schemas, which may contain hundreds of tables, but where one (or a few) large tables become the primary bottleneck during large database migrations.



```

CREATE TABLE IF NOT EXISTS firenibble
(    
    f0 BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    f1 BIGINT,
    f2 BIGINT,
    f3 INTEGER,
    f4 DOUBLE PRECISION,
    f5 DOUBLE PRECISION,
    f6 DOUBLE PRECISION,
    f7 DOUBLE PRECISION,
    f8 VARCHAR COLLATE pg_catalog."default",
    f9 VARCHAR COLLATE pg_catalog."default",
    f10 DATE,
    f11 DATE,
    f12 DATE,
    f13 VARCHAR COLLATE pg_catalog."default",
    f14 VARCHAR COLLATE pg_catalog."default",
    f15 VARCHAR COLLATE pg_catalog."default"
);

```

The tool used to create and populate this table is available in a public repository in PeerDB, you can check it out [here](https://github.com/PeerDB-io/ab-scale-testing). String lengths for population were set to 32\. The table ended up being 1TB in size with 3\.6 billion rows ingested.



```
tb_test=> select pg_size_pretty(pg_relation_size('firenibble'));
 pg_size_pretty 
----------------
 1000 GB
(1 row)

```

### Testing for a 1 terabyte table [\#](/blog/practical-postgres-migrations-at-scale-peerdb#testing-for-a-1-terabyte-table)


We performed the initial load for the above table to Postgres managed by ClickHouse with each of the three tools \- PeerDB, pg\_dump/pg\_restore and native logical replication \- separately.


#### pg\_dump and pg\_restore [\#](/blog/practical-postgres-migrations-at-scale-peerdb#pg_dump-and-pg_restore)


Since we were working with a single table, we leveraged streaming between the dump and the restore here, looking like this:



```
 time pg_dump 
  -d '<source_postgres_connection_string>' 
  -Fc 
  -t firenibble 
  --data-only 
  --verbose 
  | pg_restore 
    -d '<destination_postgres_connection_string>' 
  --data-only 
  --verbose 
  --no-owner 
  --no-acl

```

This allowed dumping and restoring simultaneously without waiting for one to finish. This also avoided the overhead of IOPS needed to dump to disk. The load was conducted with default compression settings for pg\_dump.


While we’re here, we should mention that pg\_dump and pg\_restore **do not offer parallelizing loads for a single table**. We will take a look at how PeerDB achieves this later in this post.



```
pg_restore: connecting to database for restore
pg_restore: processing data for table "public.firenibble"
pg_restore: executing SEQUENCE SET firenibble_f0_seq

real    1024m58.739s
user    1133m6.474s
sys     39m19.008s

```

The full table was loaded at the destination after **17 hours 5 minutes.**


#### Native logical replication [\#](/blog/practical-postgres-migrations-at-scale-peerdb#native-logical-replication)


The source RDS was the publisher, with a publication created with just this one table.



```
tb_test=> CREATE PUBLICATION fire_pub FOR TABLE firenibble;
CREATE PUBLICATION

```

From here, a subscription was created on Postgres managed by ClickHouse, pointing to the above database and publication.



```
logical_replication_test=# CREATE SUBSCRIPTION rds_subscription
logical_replication_test-# CONNECTION '<source_connection_string>'
logical_replication_test-# PUBLICATION fire_pub;
logical_replication_test=# NOTICE:  created replication slot "rds_subscription" on publisher
logical_replication_test-# CREATE SUBSCRIPTION

```

This immediately begins the initial load. Note that here too parallel loading of a single table is not available; it’s done by a single synchronization worker in Postgres.



```
// grep Postgres subscriber logs for "synchronization"
2026-02-17 21:34:27.175 UTC [35026:1] (0,521/2): host=,db=,user=,app=,client= LOG: logical replication table synchronization worker for subscription "rds_subscription", table "firenibble" has started 

2026-02-18 06:15:18.842 UTC [35026:2] (0,521/8): host=,db=,user=,app=,client= LOG: logical replication table synchronization worker for subscription "rds_subscription", table "firenibble" has finished

```

All in all, native logical replication loaded the data in **8 hours 40 minutes**.


#### PeerDB with 8 threads [\#](/blog/practical-postgres-migrations-at-scale-peerdb#peerdb-with-8-threads)


PeerDB’s architecture involves **peers**, which point to data stores, and **mirrors**, which are data movement pipelines between peers. Here, the source peer was RDS and the target peer was Postgres managed by ClickHouse.


When creating a mirror in PeerDB, you can set a value for initial load parallelism as well as other parameters to determine size of logical partitions and **parallelism across tables**.


In our case, since we had 1 table, we had parallelism across tables set to 1, and per\-table parallelism to be 8\.


All in all, PeerDB synced the 1 TB table in **1 hour 49 minutes.**


![1.png](/uploads/1_25ee8d61b6.png)
#### Test matrix [\#](/blog/practical-postgres-migrations-at-scale-peerdb#test-matrix)


We ran initial load tests across different sizes of the above table and parallelism specs of PeerDB. The results are below.




|  | 10 GB | 100 GB | 1000 GB |
| --- | --- | --- | --- |
| **pg\_dump / pg\_restore** | 11 minutes 20 seconds | 1 hour 48 minutes | 17 hours 5 minutes |
| **Native logical replication** | 2 minutes 43 seconds | 23 minutes 33 seconds | 8 hours 40 minutes |
| **PeerDB with 4 threads** | 1 minute 26 seconds | 18 minutes 45 seconds | 4 hours 39 minutes |
| **PeerDB with 8 threads** | 1 minute 25 seconds | 15 minutes 24 seconds | 1 hour 50 minutes |
| **PeerDB with 16 threads** | 1 minute 25 seconds | 10 minutes 34 seconds | 2 hours 10 minutes |


#### The network throughput bottleneck [\#](/blog/practical-postgres-migrations-at-scale-peerdb#the-network-throughput-bottleneck)


The results show an interesting pattern where beyond a certain threshold of parallelism for a given data size, the workload hits the limits of the network bandwidth envelope for the RDS instance and increase in parallel threads no longer give huge gains in performance.


![2.png](/uploads/2_d3350084d4.png)
*Plateaus in network throughputs on the source*
#### Percentage comparison [\#](/blog/practical-postgres-migrations-at-scale-peerdb#percentage-comparison)


Across the matrix, the relative performance of PeerDB looks as follows.


![3.png](/uploads/3_241afce7d2.png)
## Why is PeerDB faster than pg\_dump/pg\_restore and native logical replication? [\#](/blog/practical-postgres-migrations-at-scale-peerdb#why-is-peerdb-faster-than-pg_dumppg_restore-and-native-logical-replication)


The performance gains observed in our benchmarks stem directly from how PeerDB performs the initial load. **Parallel Snapshotting** in PeerDB enables parallelization of the initial load for a single large table by logically partitioning it based on CTID. This approach preserves a consistent snapshot while streaming the partitions concurrently, significantly reducing load time compared to a single\-threaded full\-table scan. Let's look at how this works:


### Consistency [\#](/blog/practical-postgres-migrations-at-scale-peerdb#consistency)


The process begins by creating a **consistent snapshot of the source database** using `pg_export_snapshot()`. This ensures that all parallel threads read from the same point in the database in time.


### Logical partitioning with CTIDs [\#](/blog/practical-postgres-migrations-at-scale-peerdb#logical-partitioning-with-ctids)


CTID is a [system column](https://www.postgresql.org/docs/current/ddl-system-columns.html) per table that represents the physical location of a row inside a table in Postgres.


The table is divided into multiple logical segments using CTIDs. By splitting the table into CTID ranges, we create independent chunks of data.


Each worker then reads one CTID range at a time using a `SELECT` query restricted to that range and streams the results to the destination.


Queries that filter by CTID ranges are efficient because they operate directly on the physical row locations inside the table. In practice, this allows the database to read rows in the order they are stored on disk. Reading data in storage order improves I/O performance and avoids repeatedly scanning the same parts of the table.


In older versions of Postgres, TID range scans are not supported. In these scenarios, PeerDB also offers two other partitioning strategies – MinMax and NTILE \- but these are not in the scope of this post.


### Streaming to destination [\#](/blog/practical-postgres-migrations-at-scale-peerdb#streaming-to-destination)


Each logical partition created above is transferred using PostgreSQL’s binary `COPY` protocol:


- `COPY TO STDOUT` on the source
- `COPY FROM STDIN` on the target


This allows dumping and restoring to happen at the same time, without writing to intermediate files. The binary format also reduces overhead compared to text\-based ones, as will be explained more in detail later.


To avoid using excessive memory, each worker uses cursors to fetch and stream data in batches.


![4.png](/uploads/4_c74894f5eb.png)
### Resiliency and observability [\#](/blog/practical-postgres-migrations-at-scale-peerdb#resiliency-and-observability)


A pain point when dealing with single, sequential loads when using tools like pg\_dump or native logical replication is a lack of **granular visibility** into initial load’s progress. This is a benefit with PeerDB’s parallel initial load where you can see exactly how many partitions are synced, and how many remain. This allows you to estimate initial load times easier.


![5.png](/uploads/5_11eda65417.png)
Another pitfall with single partition dumps is the risk of a failure at some point, causing potentially days or weeks of progress to be lost. PeerDB has **automatic failure retry mechanisms** surrounding every activity it performs. With parallel snapshotting, intermittent errors such as network cuts will impact just that single partition, resulting in an instant retry with negligible impact to the overall initial load time.


## Preserving data fidelity with PostgreSQL’s binary format [\#](/blog/practical-postgres-migrations-at-scale-peerdb#preserving-data-fidelity-with-postgresqls-binary-format)


To reduce migration overhead we don’t just think about parallelism. We also eliminate unnecessary data transformations during transfer or after.


PostgreSQL's wire protocol supports two formats for transmitting data between client and server. The first one is the text format, where data is encoded as human\-readable strings. This requires parsing on the receiving end, and has network overhead due to ASCII encoding.


[**PeerDB uses the binary format**](https://github.com/PeerDB-io/peerdb/pull/1565#pullrequestreview-3818253976)**,** where data is encoded in Postgres' native binary representation. Through this, we do not need to parse information and pass through the data type information to the target, ensuring we create target tables with the exact same data type specifications for every column as on source.


This can be felt strongest when dealing with complex data types such as JSON arrays. When receiving such data in text format, unmarshalling JSON values can cause loss in precision, lack of support for constants such as NaNs or INFs, as well as a hit to sync performance. When dealing in the binary format, no such transformations are necessary.


Preserving data in its native binary representation minimizes the risk of type mismatches or precision issues, ensuring a **predictable and seamless cutover** when application traffic switches to the target.


## Efficient and reliable CDC [\#](/blog/practical-postgres-migrations-at-scale-peerdb#efficient-and-reliable-cdc)


Once the initial snapshot is complete, the system transitions to continuous change data capture (CDC) to **keep the source and target in sync until cutover.** This phase is critical for minimizing downtime and maintaining consistency under ongoing write load.


In this section, we’ll look at two key engineering considerations: efficient replication slot consumption and reducing replication overhead, particularly for large or complex row structures.


### Reading the replication slot [\#](/blog/practical-postgres-migrations-at-scale-peerdb#reading-the-replication-slot)


Consuming the replication slot is crucial when it comes to sustaining high\-throughput ingestion workloads, where falling behind in replication lag can be detrimental to the source Postgres instance’s storage due to a heavy slot – which can only be recovered from via a full resync via dropping the slot.


PeerDB **reuses a single replication connection** across its sync batches, ensuring the replication slot is always active. It includes periodic sending of status standby updates to Postgres to avoid replication timeouts being hit.


It is also architected in a way where pulling data from source and pushing data to destination are independent processes, so failures on the push side will not hinder slot consumption.


PeerDB offers **replication slot lag alerting features** out of the box via Slack and Email, ensuring that there is no scope for outages or surprises for your business workloads.


### Support for unchanged TOAST columns [\#](/blog/practical-postgres-migrations-at-scale-peerdb#support-for-unchanged-toast-columns)


[TOAST](https://www.postgresql.org/docs/current/storage-toast.html) is PostgreSQL's mechanism for handling large field values. During Change Data Capture (CDC) using Postgres’ default logical decoding plugin \- `pgoutput` \- unchanged TOAST columns aren't included in the replication stream and appear as `NULL` values, which can be problematic during data migration. This is one of the [common pitfalls](https://blog.peerdb.io/overcoming-pitfalls-of-postgres-logical-decoding#heading-toast-columns-need-replica-identity-full) of logical decoding users.This can be addressed by setting `REPLICA IDENTITY FULL` on the source tables. However, this is often a concern for users as it requires modifying the source database.


PeerDB supports streaming of unchanged TOAST columns during CDC without having to set `REPLICA IDENTITY FULL` to source tables. In summary, it relies on the previously stored values of the TOAST columns in the target to reconstruct unchanged TOAST columns.


Let’s take a closer look at the internal algorithm.


#### Caching technique for backfills within a batch [\#](/blog/practical-postgres-migrations-at-scale-peerdb#caching-technique-for-backfills-within-a-batch)


When reading logical replication messages from Postgres, PeerDB maintains a cache of CDC records scoped to the current batch of records.


UPDATEs with unchanged TOAST columns are detected using information provided via Postgres’ logical replication protocol for messages. PeerDB is then able to look up these columns present in earlier INSERT or UPDATE records in the same batch, and **backfill the missing values.**


![6.png](/uploads/6_399f4e40c2.png)
#### Using MERGE to retrieve previous state of the TOAST column [\#](/blog/practical-postgres-migrations-at-scale-peerdb#using-merge-to-retrieve-previous-state-of-the-toast-column)


PeerDB stores all pulled change data in a raw table. As part of this effort, we store in the raw table all **unique combinations of TOAST columns** for each table in the batch.


Postgres’ `MERGE` command is then used to replicate insert, update and delete records from the raw table to the target table, making sure to **keep unchanged TOAST column values intact** in the destination table.


We can walk through a simple example `MERGE` command for the above diagram’s table schema.


1. First, we group records by their primary key value, and rank them based on when they were pulled from source.



```
WITH src_rank AS (
    SELECT
        _peerdb_data, -- contains the change-data record (insert, update or delete)
        _peerdb_record_type, -- says if it's insert(0), update(1) or delete(2)
        _peerdb_unchanged_toast_columns, -- comma separated string of columns
        RANK() OVER (
            PARTITION BY (_peerdb_data ->> 'id') :: integer -- group by primary key
            ORDER BY
                _peerdb_timestamp DESC -- rank by latest
        ) AS _peerdb_rank
    FROM
        peerdb_temp._peerdb_raw_my_mirror -- contains all change-data of the mirror
    WHERE
        _peerdb_batch_id = $ 1
        AND _peerdb_destination_table_name = $ 2
)

```

2. Now, we issue a `MERGE` command to push each change\-data to the final table.



```
MERGE INTO "public"."my_table" dst USING (
    SELECT
        (_peerdb_data ->> 'id') AS "id",
        (_peerdb_data ->> 'blob') AS "blob",
        (_peerdb_data ->> 'status') AS "status",
        _peerdb_record_type,
        _peerdb_unchanged_toast_columns
    FROM
        src_rank
    WHERE
        _peerdb_rank = 1
) src ON src."id" = dst."id"

```

3. First, we must account for inserts, which is straightforward.



```
   WHEN NOT MATCHED THEN -- row is not on target, so it is an INSERT
        INSERT
            ("id", "blob", "status", "_peerdb_synced_at")
        VALUES
            (
                src."id",
                src."blob",
                src."status",
                CURRENT_TIMESTAMP
            )

```

4. Now, we get into the conflict handling strategy in the case of updates. In an update record, `_peerdb_unchanged_toast_columns` is a comma\-separated string list of column names whose values are unchanged. If there are no such values, it will be an empty string like so.



```
   WHEN MATCHED -- row exists on target
    AND src._peerdb_record_type != 2  -- this means it isn't a delete, so it's an update
    AND _peerdb_unchanged_toast_columns = '' -- no unchanged toast columns, update everything
    THEN
        UPDATE
        SET
            "id" = src."id",
            "blob" = src."blob",
            "status" = src."status",
            "_peerdb_synced_at" = CURRENT_TIMESTAMP

```

5. In the case above though, for instance, `blob` was unchanged in the update. That would then be handled like:



```
   WHEN MATCHED -- row exists on target
    AND src._peerdb_record_type != 2 -- this means it isn't a delete, so it's an update
    AND _peerdb_unchanged_toast_columns = 'blob' -- unchanged toast column ! we cannot update this guy, because it would wipe out its value to empty string sent by PG
 THEN 
        UPDATE
        SET -- blob not updated here
            "id" = src."id",
            "status" = src."status",
            "_peerdb_synced_at" = CURRENT_TIMESTAMP
            WHEN MATCHED
            AND src._peerdb_record_type = 2 THEN DELETE

```

## A look ahead and getting started [\#](/blog/practical-postgres-migrations-at-scale-peerdb#a-look-ahead-and-getting-started)


At ClickHouse, we’re actively working on making Postgres migrations a one\-click experience. This is a first step in that direction. Stay tuned for more updates in the near future!


[PeerDB](https://github.com/PeerDB-io/peerdb) can be set up with a single command. You can head over to our open\-source repository on GitHub to [get started](https://github.com/PeerDB-io/peerdb?tab=readme-ov-file#get-started). Once ready, create a Postgres to Postgres by ClickHouse mirror with a few clicks by following our [documented guides](https://docs.peerdb.io/mirror/cdc-pg-pg).


In the meantime, if you’d like to explore this firsthand, sign up for the Postgres managed by ClickHouse [private preview](https://clickhouse.com/cloud/postgres) and launch a high\-speed OLTP stack in minutes with the help of our [quickstart](https://clickhouse.com/docs/cloud/managed-postgres/quickstart).

### Try Postgres managed by ClickHouse

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-70-try-postgres-managed-by-clickhouse-get-access&utm_blogctaid=70)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
