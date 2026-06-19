# Postgres to ClickHouse: Data Modeling Tips


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Postgres to ClickHouse: Data Modeling Tips

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)Aug 28, 2024 · 13 minutes readLast month, we [acquired PeerDB](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database), a company that specializes in Postgres CDC. [PeerDB](https://www.peerdb.io/) makes it fast and simple to replicate data from [Postgres](https://www.postgresql.org/) to [ClickHouse](https://clickhouse.com/). A common question from PeerDB users is how to model their data in ClickHouse after the replication process to maximize the benefits of ClickHouse.


This question arises because ClickHouse and Postgres differ in data modeling, as each is a **purpose\-built database** highly optimized for its specific workload \-Postgres is a transactional (OLTP) database, while ClickHouse is an analytical (OLAP) columnar database. This guide walks you through essential data modeling concepts in ClickHouse for users coming from the Postgres world. Note that this is part 1 of a blog series, with more to come in the future.


## ReplacingMergeTree table engine [\#](/blog/postgres-to-clickhouse-data-modeling-tips#replacingmergetree-table-engine)


PeerDB maps PostgreSQL tables to ClickHouse using the [ReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) engine. ClickHouse performs best with append\-only workloads and [does not recommend](https://clickhouse.com/docs/en/guides/developer/mutations) frequent UPDATEs. This is where ReplacingMergeTree is particularly powerful.


`ReplacingMergeTree` supports workloads that involve both data ingestion and modifications. Each table is append\-only, with user updates ingested as versioned INSERTs. The ReplacingMergeTree engine manages deduplication (merging) of rows in the background. This is one of the key factors that enables ClickHouse to deliver exceptional real\-time ingestion performance.


In PeerDB, both INSERTs and UPDATEs from Postgres are captured as new rows with different versions (using `_peerdb_version`) in ClickHouse. The `ReplacingMergeTree` table engine periodically handles deduplication in the background using the Ordering Key (ORDER BY columns), retaining only the row with the latest `_peerdb_version`. DELETEs from PostgreSQL are propagated as new rows marked as deleted (using the `_peerdb_is_deleted` column). The snippet below shows the target table definition for the `public_goals` table in ClickHouse.



```
clickhouse-cloud :) SHOW CREATE TABLE public_goals;
CREATE TABLE peerdb.public_goals
(
    `id` Int64,
    `owned_user_id` String,
    `goal_title` String,
    `goal_data` String,
    `enabled` Bool,
    `ts` DateTime64(6),
    `_peerdb_synced_at` DateTime64(9) DEFAULT now(),
    `_peerdb_is_deleted` Int8,
    `_peerdb_version` Int64
)
ENGINE = SharedReplacingMergeTree
('/clickhouse/tables/{uuid}/{shard}', '{replica}', _peerdb_version)
PRIMARY KEY id
ORDER BY id
SETTINGS index_granularity = 8192

```

## You might still see duplicates for rows—how should you handle them? [\#](/blog/postgres-to-clickhouse-data-modeling-tips#you-might-still-see-duplicates-for-rowshow-should-you-handle-them)


ReplacingMergeTree clears out duplicates asynchronously in the background but doesn't guarantee the absence of duplicates. So, when you query the data, you might still see duplicates for the same row or primary key but with different versions. This is expected. To remove duplicates, you have a couple of approaches:


### Use FINAL in your queries [\#](/blog/postgres-to-clickhouse-data-modeling-tips#use-final-in-your-queries)


ClickHouse has a unique modifier called [FINAL](https://clickhouse.com/docs/en/sql-reference/statements/select/from#final-modifier), which performs de\-duplication (merging of rows) at query time. This de\-duplication occurs after filtering (WHERE clause) but before aggregations (GROUP BY).


A historical concern has been that FINAL can slow down query performance. While it does impact query performance to some extent, recent releases of ClickHouse have introduced [significant improvements](https://github.com/ClickHouse/ClickHouse/issues/11722) to enhance FINAL query performance. So, don’t hesitate to use the FINAL clause and evaluate how your queries perform. Below is an example of how to use the FINAL clause:



```
SELECT owner_user_id, COUNT(*) FROM goals FINAL 
WHERE enabled = true GROUP BY owner_user_id;

```

### Use argMax to deduplicate rows at query time [\#](/blog/postgres-to-clickhouse-data-modeling-tips#use-argmax-to-deduplicate-rows-at-query-time)


In ClickHouse, [argMax](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/argmax) is a powerful function for deduplicating rows dynamically during query execution. This is particularly useful when you need to retain the most recent or relevant record based on a versioning or timestamp column.


For instance, if you're working with a table like `peerdb.public_goals`, where id is the primary key and `_peerdb_version` tracks versions, you can use argMax to select the row with the highest `_peerdb_version` for each `id`. This approach allows you to efficiently remove duplicates without altering the underlying data. You can then run your aggregations as a subquery over this deduplicated result set for further analysis. Below query is an example of using argMax



```
SELECT
    owned_user_id,
    COUNT(*) AS active_goals_count,
    MAX(ts) AS latest_goal_time
FROM
(
    SELECT
        id,
        argMax(owned_user_id, _peerdb_version) AS owned_user_id,
        argMax(goal_title, _peerdb_version) AS goal_title,
        argMax(goal_data, _peerdb_version) AS goal_data,
        argMax(enabled, _peerdb_version) AS enabled,
        argMax(ts, _peerdb_version) AS ts,
        argMax(_peerdb_synced_at, _peerdb_version) AS _peerdb_synced_at,
        argMax(_peerdb_is_deleted, _peerdb_version) AS _peerdb_is_deleted,
        max(_peerdb_version) AS _peerdb_version
    FROM peerdb.public_goals
    WHERE enabled = true
    GROUP BY id
) AS deduplicated_goals
GROUP BY owned_user_id;

```

### Use WINDOW FUNCTIONS [\#](/blog/postgres-to-clickhouse-data-modeling-tips#use-window-functions)


You can use ClickHouse's [window functions](https://clickhouse.com/docs/en/sql-reference/window-functions) to achieve similar deduplication by selecting the row with the highest `_peerdb_version` within each id partition. Here's an example:



```
SELECT
    owned_user_id,
    COUNT(*) AS active_goals_count,
    MAX(ts) AS latest_goal_time
FROM
(
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY _peerdb_version DESC) AS rn
    FROM peerdb.public_goals
    WHERE enabled = true
) AS ranked_goals
WHERE rn = 1
GROUP BY owned_user_id;

```

### Use Views to simplify deduplication [\#](/blog/postgres-to-clickhouse-data-modeling-tips#use-views-to-simplify-deduplication)


Encapsulate deduplication in a [view](https://clickhouse.com/docs/en/sql-reference/statements/create/view) to make it simple for BI tools to query the most up\-to\-date data. For example, use a window function in the view to keep only the latest version of each row:



```
CREATE VIEW goals AS
SELECT * FROM
(
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY _peerdb_version DESC) AS rn
    FROM peerdb.public_goals
    WHERE enabled = true
) WHERE rn = 1;

```


```

SELECT
    owned_user_id,
    COUNT(*) AS active_goals_count,
    MAX(ts) AS latest_goal_time
FROM goals
GROUP BY owned_user_id;

```

## Nullable Columns [\#](/blog/postgres-to-clickhouse-data-modeling-tips#nullable-columns)


If you're coming from the Postgres world, one surprising aspect of ClickHouse is that it doesn’t store NULL values for columns unless you explicitly wrap the column types in [`Nullable`](https://clickhouse.com/docs/en/sql-reference/data-types/nullable). For example, instead of storing NULL for dates, ClickHouse stores `1970-01-01` as the default value, which might be unexpected. This behavior is due to the fact that storing NULLs can [impact](https://clickhouse.com/docs/en/sql-reference/data-types/nullable) query performance in ClickHouse, as it’s a columnar database. Hence, ClickHouse requires users to explicitly define `Nullable` types.


In PeerDB, we’ve introduced a setting called `PEERDB_NULLABLE`, which, when set to `true`, automatically detects nullable columns in Postgres and marks them as `Nullable` in ClickHouse during the replication process. This means you don’t need to manually define `Nullable` types during replication. You can read more about this feature in the following [PR](https://github.com/PeerDB-io/peerdb/pull/2001).


## **Data Types** [\#](/blog/postgres-to-clickhouse-data-modeling-tips#data-types)


ClickHouse offers a wide variety of data types, ranging from numbers, text, timestamps, dates, and arrays to the recently introduced [JSON](https://github.com/ClickHouse/ClickHouse/issues/54864) type. Many of the data types in Postgres can be natively stored in ClickHouse without much modification.


As a reference, here goes [the data type matrix](https://docs.peerdb.io/datatypes/datatype-matrix) we use at PeerDB when replicating data from Postgres to ClickHouse.


## The Ordering Key [\#](/blog/postgres-to-clickhouse-data-modeling-tips#the-ordering-key)


### What is an Ordering Key? [\#](/blog/postgres-to-clickhouse-data-modeling-tips#what-is-an-ordering-key)


Choosing the right ordering key is crucial for query performance in ClickHouse. Defined by the `ORDER BY` clause when creating a table, the ordering key functions similarly to a index in Postgres but is optimized for analytics. Unlike Postgres, which uses a B\-tree index with entries pointing to each row, ClickHouse uses Sparse Indexing:


1. **Data is sorted based on Ordering Key:** The ordering key ensures that data on disk is sorted according to the specified columns. This allows for better [compression](https://clickhouse.com/docs/en/data-compression/compression-in-clickhouse), as correlated values are stored together.
2. **Ordering Key also creates a sparse index:** The ordering key also creates a sparse index, storing only ranges of columns, with each entry pointing to a group of sorted rows. This keeps the index small, allowing ClickHouse to quickly identify relevant groups of rows using a binary search and execute queries efficiently. You can read more about this [here](https://clickhouse.com/docs/en/migrations/postgresql/designing-schemas#primary-ordering-keys-in-clickhouse).


You can think of ordering keys as similar to [BRIN](https://www.postgresql.org/docs/current/indexes-types.html#INDEXES-TYPES-BRIN) indexes in Postgres, but in ClickHouse, the data is automatically sorted based on the ordering key via asynchronous merging of parts, so you don’t need to handle sorting during data ingestion.


### Choosing an appropriate Ordering Key [\#](/blog/postgres-to-clickhouse-data-modeling-tips#choosing-an-appropriate-ordering-key)


When selecting an ordering key, base your choice on the columns most frequently used in your query filters. **Prioritize columns that are commonly used in WHERE clauses, and order them in ascending sequence of cardinality**—starting with columns that have the fewest distinct values. This approach optimizes data compression and query performance. For a deeper understanding of this topic, refer to the detailed guide [here](https://clickhouse.com/docs/en/data-modeling/schema-design#choosing-an-ordering-key).


### **PRIMARY KEY vs Ordering Key** [\#](/blog/postgres-to-clickhouse-data-modeling-tips#primary-key-vs-ordering-key)


If you observe the table definition of `public_goals`, it has a `PRIMARY KEY`. You might be wondering how the `PRIMARY KEY` differs from the Ordering Key. Let us understand how they differ:


1. `PRIMARY KEY`, if specified, defines the columns in the sparse index, while the columns in the `ORDER BY` clause determine how the data is sorted on disk. They are also used for deduplicating data by the `ReplacingMergeTree`.
2. If the `PRIMARY KEY` isn't specified, the Ordering Key automatically becomes the `PRIMARY KEY` and defines the columns in the sparse index.



> **NOTE:** Columns in the `PRIMARY KEY` should always be prefixed in the Ordering Key. This ensures that the index aligns with the physical data order, maximizing query performance by minimizing unnecessary data scans.


**An example where** `PRIMARY KEY` **could differ from Ordering Key**


An example where you might have different `PRIMARY KEY` and `ORDER BY` columns is when your queries are primarily filtered on `customer_id` rather than `id`. In this case, you can define the `PRIMARY KEY` on just `customer_id` and the `ORDER BY` on `customer_id, id`. This approach ensures a smaller, more efficient sparse index for querying, while data deduplication occurs on `id`, ensuring no data is lost.



> **NOTE:** Unlike in Postgres, where the `PRIMARY KEY` is a B\-tree index that guarantees uniqueness, in ClickHouse, it does not ensure uniqueness. Instead, it defines the columns that should be part of the sparse index.


### Modifying the Ordering Key [\#](/blog/postgres-to-clickhouse-data-modeling-tips#modifying-the-ordering-key)


Choosing the right [ordering key](https://clickhouse.com/docs/en/migrations/postgresql/designing-schemas#primary-ordering-keys-in-clickhouse) is crucial for query performance in ClickHouse, as it acts as an index when querying data. By default, PeerDB uses the PostgreSQL `PRIMARY KEY` to define the ordering key in ClickHouse tables, but you can change it using the following methods:


### Use materialized views [\#](/blog/postgres-to-clickhouse-data-modeling-tips#use-materialized-views)


You can use materialized views to create a new table with a different ordering key suitable for your workload. Include the primary key columns at the end of the ordering key to ensure proper deduplication, as ReplacingMergeTree uses the ORDER BY clause for deduplication, and including the primary key ensures that no data is lost.



```
CREATE MATERIALIZED VIEW goals_mv
ENGINE = ReplacingMergeTree(_peerdb_version)
ORDER BY (enabled, ts, id)  POPULATE AS
SELECT * FROM peerdb.public_goals;

```

**NOTE:** After creating the materialized view, be sure to follow the steps described in the previous section on handling duplicates to ensure proper deduplication during query time.


### Predefine target tables with the desired Ordering Key [\#](/blog/postgres-to-clickhouse-data-modeling-tips#predefine-target-tables-with-the-desired-ordering-key)


To change the ordering key, you can predefine new tables with your desired Ordering Key and then swap them with the existing tables. Here's how you can do it:


**1\. Create a Dummy Mirror:** Create a dummy mirror in PeerDB to generate the default tables with the correct metadata columns and data types.


**2\. Create a New Table with the Desired Ordering Key:** Use the table created by PeerDB to define a new table with your desired ordering key. Include the primary key columns at the end of the ordering key to ensure proper deduplication. Here is an example:



```
CREATE TABLE public_events_new AS public_events
ENGINE = ReplacingMergeTree(_peerdb_version)
ORDER BY (user_id,id);

```

**3\. Drop the Old Table:**



```
DROP TABLE public_events;

```

**4\. Rename the New Table:** Rename the new table to the actual table



```
RENAME TABLE public_events_new TO public_events;

```

**5\. Start MIRROR to Point to the New Table:** Configure the mirror to point to the actual table. PeerDB uses `CREATE TABLE IF NOT EXISTS` behind the scenes and continues to ingest data into the new table.


## Handling DELETEs [\#](/blog/postgres-to-clickhouse-data-modeling-tips#handling-deletes)


As mentioned, DELETEs from PostgreSQL are propagated as new rows marked as deleted (using the `_peerdb_is_deleted` column). To exclude deleted rows from your queries, you can create row\-level policies in ClickHouse based on the `_peerdb_is_deleted` column. Here’s an example:



```
CREATE ROW POLICY policy_name ON table_name
FOR SELECT USING _peerdb_is_deleted = 0;

```

This policy ensures that only rows where `_peerdb_is_deleted` is 0 are visible when querying the table.


## Conclusion [\#](/blog/postgres-to-clickhouse-data-modeling-tips#conclusion)


I hope you enjoyed reading the blog. I aimed to cover the most common data\-modeling challenges you might encounter when migrating from PostgreSQL to ClickHouse. In the next blog, I plan to dive into more advanced topics, such as joins, writing efficient SQL queries, and so on. Alternatively, if you want to avoid maintaining separate transactional and analytical stacks altogether, learn how our [Managed Postgres bridges the gap for AI and real\-time apps](/resources/engineering/managed-postgres-for-ai-and-real-time-apps). If you want to give PeerDB and ClickHouse a try to start replicating data from Postgres to ClickHouse, please check out the links below or reach out to us directly!


1. [Try ClickHouse Cloud for Free](https://clickhouse.com/docs/en/cloud-quick-start)
2. [Try PeerDB Cloud for Free](https://auth.peerdb.cloud/signup)
3. [Docs on Postgres to ClickHouse Replication](https://docs.peerdb.io/mirror/cdc-pg-clickhouse)
4. [Talk to the PeerDB team directly](https://www.peerdb.io/sign-up)
[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
