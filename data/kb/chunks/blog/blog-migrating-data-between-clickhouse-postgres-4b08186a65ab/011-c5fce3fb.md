---
source: blog
url: https://clickhouse.com/docs/integrations/clickpipes/postgres
topic: clickhouse-and-postgresql-a-match-made-in-data-heaven-part-1
ch_version_introduced: '28535.465'
last_updated: '2026-06-12'
chunk_index: 11
total_chunks_in_doc: 14
---

= 0, 'freehold' = 1, 'leasehold' = 2), `addr1` String, `addr2` String, `street` String, `locality` String, `town` String, `district` String, `county` String ) ENGINE = PostgreSQL('db.zcxfcrchxescrtxsnxuc.supabase.co', 'postgres', 'uk_price_paid', 'postgres', '') ``` There are a few takeaways concerning performance:

- ClickHouse can push down filter clauses if they are simple i.e. \=, !\=, \>, \>\=, \<, \<\=, and IN, allowing indexes in Postgres to be potentially exploited. If they involve ClickHouse\-specific functions (or if Postgres determines a full scan is the best execution method), a full table scan will be performed, and Postgres indexes will not be exploited. This can lead to large differences in performance depending on where the query is run due to the need to stream the entire dataset to ClickHouse. If bandwidth connectivity is not an issue, and Postgres would need to perform a full scan even if the query was executed directly, then differences in performance will be less appreciable.
- If using the `postgres` function or table engine, be cognizant of the number of queries required from Postgres. In our earlier example, we minimized the use of the function to speed up queries. Balance this against being able to exploit Postgres indexes to minimize the data streamed to ClickHouse.

## Postgres to ClickHouse [\#](/blog/migrating-data-between-clickhouse-postgres#postgres-to-clickhouse)

Up to now, we’ve only pushed queries down to Postgres. While occasionally useful for ad\-hoc analysis and querying small datasets, you will eventually want to exploit ClickHouse’s MergeTree table and its associated performance on analytical queries. Moving data between Postgres and ClickHouse is as simple as using the `INSERT INTO x SELECT FROM` syntax.

![postgres-db-engine.png](/uploads/postgres_db_engine_026ea3f9f2.png)
In the example below, we create a table and attempt to insert the data from our Supabase\-hosted Postgres instance:
