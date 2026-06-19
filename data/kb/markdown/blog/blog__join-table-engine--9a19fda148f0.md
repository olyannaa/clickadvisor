# ClickHouse Cloud: Fast, Updatable Lookups with the Join Table Engine


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Cloud: Fast, Updatable Lookups with the Join Table Engine

![](/_next/image?url=%2Fuploads%2FImage_512x512_14_950d86cdef.jpeg&w=96&q=75)[Hellmar Becker](/authors/hellmar-becker)May 12, 2026 · 8 minutes read## Dictionaries in ClickHouse [\#](/blog/join-table-engine#dictionaries-in-clickhouse)


When you move data from your transactional or event\-based data sources to an analytical database like ClickHouse, you will likely consider modeling a dimensional schema according to the [Kimball methodology](https://en.wikipedia.org/wiki/Dimensional_modeling).



> [Dimensional modeling](https://en.wikipedia.org/wiki/Dimensional_modeling) always uses the concepts of facts (measures), and dimensions (context). Facts are typically (but not always) numeric values that can be aggregated, and dimensions are groups of hierarchies and descriptors that define the facts.


It follows that fact tables are typically immutable, and data are appended to them; whereas dimension tables are smaller, and subject to (infrequent) updates ([slowly changing dimensions](https://en.wikipedia.org/wiki/Slowly_changing_dimension)). When you run an analytical query, you have to join those dimensions against the fact table.


One common approach to do this in ClickHouse is to have a copy of the dimension data in memory in a [Dictionary](https://clickhouse.com/docs/engines/table-engines/special/dictionary). This approach enables [Direct Joins](https://clickhouse.com/blog/clickhouse-fully-supports-joins-direct-join-part4#direct-join) and is [recommended for optimizing join performance](https://clickhouse.com/blog/postgres-to-clickhouse-data-modeling-tips-v2#optimizing-joins).


A Dictionary is set up by specifying, among others, the `SOURCE` and `LIFETIME` attributes. ClickHouse pulls fresh data from the source and uses `LIFETIME` to determine how often it should refresh the Dictionary. But some customers asked me: Isn't there a way to update a Dictionary like a regular table? And indeed, there is a way to achieve this, using another special table engine.


## The `Join` table engine [\#](/blog/join-table-engine#the-join-table-engine)


The [`Join` table engine](https://clickhouse.com/docs/engines/table-engines/special/join) is just what we need here. It is an in\-memory structure, laying out data for a *specific* type of join that has to be stated in the table definition, and it is backed by a persistence layer. Setting up the `Join` table, you need to configure


- *join strictness*
- *join type*
- the *key column(s)* you want to use in the join.


### Join strictness [\#](/blog/join-table-engine#join-strictness)


This can be `ANY` or `ALL`. With `ALL`, all matching rows are taken from the `Join` table; `ANY` takes only the latest one.


This means with `ANY` type *an **`INSERT`** becomes an **`UPSERT`** by key:* you update a dimension row by inserting another row with the same key.


### Join Type [\#](/blog/join-table-engine#join-type)


One of ClickHouse's [join types](https://clickhouse.com/docs/sql-reference/statements/select/join#supported-types-of-join), like `INNER` or `LEFT` or `RIGHT`. For dimensional modeling, you will mostly use `LEFT`.


## Querying a `Join` table [\#](/blog/join-table-engine#querying-a-join-table)


While a `Join` table can be queried like any regular table using `SELECT`, there are two more ways of using it:


1. If you place the `Join` table in a `JOIN` query where the join parameters match the ones in the definition of the table, ClickHouse will automatically know to use the Direct Join algorithm.
2. You can look up values for a given key using `joinGet`. This works just like `dictGet` for Dictionaries.


## Drawbacks in the open source implementation [\#](/blog/join-table-engine#drawbacks-in-the-open-source-implementation)


So a `Join` table with `ANY LEFT` join condition would be just the thing to implement a [Type 1 slowly changing dimension](https://en.wikipedia.org/wiki/Slowly_changing_dimension#Type_1:_overwrite), right? You can update values for a given key and have a high performing join. Why don't we use it all the time, then?


It turns out that the implementation of the `Join` table engine in open source ClickHouse has a couple of drawbacks that make it less suitable for this use case:


1. **`Join` tables are not distributed**; each cluster node would have to maintain its own copy/version of the table.
2. **The persistence layer is not built for frequent inserts/updates**. The Join table engine persists data as compressed Native\-format .bin files in the table's data directory on disk (one file per INSERT batch). On server startup, these files are read back sequentially and the in\-memory HashJoin hash table is reconstructed from them. This means each update will create a new numbered .bin file. There is no background compaction process — files are never merged automatically. Over time, this leads to performance degradation.


## Implementation in ClickHouse Cloud [\#](/blog/join-table-engine#implementation-in-clickhouse-cloud)


**These issues have been solved very elegantly in ClickHouse Cloud.** In ClickHouse Cloud, a `Join` table is actually transparently implemented as a `SharedJoin` table with a MergeTree family backing table:


- for `ALL` join, this is a `MergeTree` table
- for `ANY` join, a `ReplacingMergeTree` table.


You can find these tables in `system.tables`. The naming convention for the underlying table is `.inner_id.SharedJoin.<uuid of Join table>`.



> **Note:** there is a setting [`join_any_take_last_row`](https://clickhouse.com/docs/operations/settings/settings#join_any_take_last_row) that is **not** honored


The in\-memory table is populated from the persistent (underlying) table using a query (which includes `FINAL` in the case of `ANY` join) on insert to Join table (with filter to select only newest data) and on table load on startup.


## Example: Data Enrichment [\#](/blog/join-table-engine#example-data-enrichment)


Probably the most meaningful use case is enrichment / dimensional modeling with an `ANY LEFT` join. To illustrate this specific case, let's take the example from the ClickHouse [docs](https://clickhouse.com/docs/engines/table-engines/special/join#example) and modify it a bit:



```

```
1-- Create the fact table and insert some data
2CREATE OR REPLACE TABLE id_val (
3    `id` UInt32,
4    `val` UInt32
5) ENGINE = MergeTree
6ORDER BY (id);
7
8INSERT INTO id_val VALUES
9    (1, 11), (2, 12), (3, 13);
10
11-- Creating the right-side Join table:
12CREATE OR REPLACE TABLE id_val_join (
13    `id` UInt32,
14    `val` UInt8
15) ENGINE = Join(ANY, LEFT, id);
16
17-- Insert some values
18INSERT INTO id_val_join VALUES
19    (1, 21), (1, 22), (3, 23);
20
21-- Enrichment query
22SELECT *
23FROM id_val
24ANY LEFT JOIN id_val_join USING (id);
```

```


```
   ┌─id─┬─val─┬─id_val_join.val─┐
1. │  1 │  11 │              22 │
2. │  2 │  12 │               0 │
3. │  3 │  13 │              23 │
   └────┴─────┴─────────────────┘

```

Now, let's find out what happens in the `Join` table and in the underlying table when we upsert an entry for key `1`.



```

```
1-- And another insert
2INSERT INTO id_val_join VALUES (1,42);
```

```

Look up the underlying table:



```

```
1SELECT database, name, uuid, engine
2FROM system.tables
3WHERE name = 'id_val_join'
4FORMAT Vertical;
```

```


```
database:                         default
name:                             id_val_join
uuid:                             64f169ee-977d-46c2-b067-580fdf8c1d4b
engine:                           SharedJoin

```

The `Join` table deduplicates and keeps the latest entry only:



```

```
1SELECT * FROM id_val_join;
```

```


```
   ┌─id─┬─val─┐
1. │  3 │  23 │
2. │  1 │  42 │
   └────┴─────┘

```

Constructing the underlying `ReplacingMergeTree` table from the UUID, we see this one retains the duplicates until they are merged out:



```

```
1SELECT * FROM default.`.inner_id.SharedJoin.64f169ee-977d-46c2-b067-580fdf8c1d4b`;
```

```


```
   ┌─id─┬─val─┐
1. │  1 │  22 │
2. │  3 │  23 │
3. │  1 │  42 │
   └────┴─────┘

```

Finally, running the enrichment query again, we see how the updated dimension entry reflects in the result:



```

```
1SELECT *
2FROM id_val
3ANY LEFT JOIN id_val_join USING (id);
```

```


```
   ┌─id─┬─val─┬─id_val_join.val─┐
1. │  1 │  11 │              42 │
2. │  2 │  12 │               0 │
3. │  3 │  13 │              23 │
   └────┴─────┴─────────────────┘

```

Every time you insert a new row or a set of rows:


- The data is inserted into the underlying `ReplacingMergeTree` table.
- The in\-memory representation is updated on insert to the Join table (with a filter on block ID to select only newest data) and on table load on startup.
- This query also applies `FINAL`, so the in\-memory `Join` table will never have duplicates.
- The `join_any_take_last_row` is ignored. You always get the latest entry.


## Conclusion [\#](/blog/join-table-engine#conclusion)


- The `Join` table engine in ClickHouse provides a precomputed hash map that can be used to speed up JOINs.
- Like a dictionary, a `Join` table is kept in memory. But it is backed by a persistence layer (saved in files).
- In ClickHouse Cloud, `Join` tables are automatically clustered and backed by full `MergeTree` tables, making them suitable for frequent updates.
- In particular, for dimensional modeling in ClickHouse Cloud, use `Join(ANY, LEFT, id)` — upserting, deduplication, and data compaction is automatically handled by the underlying `ReplacingMergeTree`!
### Get started today

Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-560-get-started-today-sign-up&utm_blogctaid=560)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
