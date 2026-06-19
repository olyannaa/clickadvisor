# Monitoring Asynchronous Inserts


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Monitoring Asynchronous Inserts

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Jan 4, 2024 · 15 minutes read## Introduction [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#introduction)


In this follow\-up post about [asynchronous inserts](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse), we give guidance and queries for monitoring asynchronous inserts. This can be helpful for validating that everything is working correctly according to your settings. And, especially identifying insert errors that [occurred](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#insert-errors-can-occur-during-buffer-flush) during buffer flushes for asynchronous inserts performed in [fire and forget mode](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#fire-and-forget-return-behavior).


## Asynchronous insert mechanics primer [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#asynchronous-insert-mechanics-primer)


As a reminder, asynchronous inserts keep the frequency of part creations automatically under control by buffering several (potentially small) inserts server side before a new part gets created. The following diagram visualizes this:
![monitoring_async_inserts_02.png](/uploads/monitoring_async_inserts_02_9956927ad0.png)
When ClickHouse ① receives an asynchronous insert query, then the query’s data is ② immediately written into an in\-memory buffer first. Asynchronously to ①, and only when ③ the next buffer flush takes place, the buffer’s data is [sorted](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#data-is-stored-on-disk-ordered-by-primary-key-columns) and written as a part to the database storage. Before the buffer gets flushed, the data of other asynchronous insert queries from the same or other clients can be collected in the buffer. The part created from the buffer flush will, therefore, potentially contain the data from several asynchronous insert queries. Note that there [can be](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#there-can-be-multiple-parts) multiple parts being created from a single buffer flush, and there [can be](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#there-can-be-multiple-buffers) multiple buffers in operation at any time.


## Relevant system tables [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#relevant-system-tables)


ClickHouse provides [SQL\-based observability](https://clickhouse.com/blog/the-state-of-sql-based-observability) of itself. Each ClickHouse node is constantly monitoring itself and continuously writing metrics, logs, traces, and other observability data into [system tables](https://clickhouse.com/blog/clickhouse-debugging-issues-with-system-tables). This allows us to simply use SQL and ClickHouse itself to look deeply under the hood of ClickHouse data processing mechanisms, like asynchronous inserts. In general, system tables are the number one troubleshooting tool for both our core and support engineers.


This diagram lists the system tables containing observability data collected when ClickHouse receives and executes asynchronous inserts:
![monitoring_async_inserts_03.png](/uploads/monitoring_async_inserts_03_53edd98f35.png)
① When ClickHouse receives and executes an insert query, then this is [logged](https://clickhouse.com/blog/monitoring-troubleshooting-insert-queries-clickhouse) together with execution statistics into the [system.query\_log](https://clickhouse.com/docs/en/operations/system-tables/query_log) table.


② In the [system.metrics](https://clickhouse.com/docs/en/operations/system-tables/metrics) table, you can check the [PendingAsyncInsert](https://clickhouse.com/docs/en/operations/system-tables/metrics#pendingasyncinsert) metric to get the number of asynchronous insert queries whose data is currently buffered and waiting to be flushed.


③ The [system.asynchronous\_insert\_log](https://clickhouse.com/docs/en/operations/system-tables/asynchronous_insert_log) table logs all buffer flush events.


④ Whenever a table part is created, then this event is logged in the [system.part\_log](https://clickhouse.com/docs/en/operations/system-tables/part_log) table.


⑤ The [system.parts](https://clickhouse.com/docs/en/operations/system-tables/parts) table contains meta information about all currently existing table parts.


In the following sections, we present and describe a few handy queries over these aforementioned system tables for introspecting the execution stages of asynchronous inserts.


Note that these queries are assumed to be executed on a [cluster with a specific name](https://clickhouse.com/docs/en/engines/table-engines/special/distributed#distributed-clusters) by utilizing the [clusterAllReplicas](https://clickhouse.com/docs/en/sql-reference/table-functions/cluster) table function. If you are not using a clustered version of ClickHouse, you can query the tables directly from your single node.


## Queries for introspecting async inserts [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#queries-for-introspecting-async-inserts)


To help with debugging, we provide a simple [script](https://gist.github.com/tom-clickhouse/2363ddd25ee96700ebcd66dcca8a8ba9) that creates all of the following queries as handy [parameterized views](https://clickhouse.com/docs/en/sql-reference/statements/create/view#parameterized-view).


### Part creations [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#part-creations)


Remember that the main purpose of asynchronous inserts is to keep the frequency of part creations under control by buffering several (potentially small) inserts ClickHouse\-server side, before a new part gets created.


[Here](https://gist.github.com/tom-clickhouse/7596e3586b545506851635694ba4ad06) is a query over the [system.part\_log](https://clickhouse.com/docs/en/operations/system-tables/part_log) table (joined with [system.parts](https://clickhouse.com/docs/en/operations/system-tables/parts) for additional info) that you can use for double\-checking the frequency of part creations. [Remember](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#there-can-be-multiple-parts) that the table rows buffered in the asynchronous insert buffer can potentially contain several different [partitioning key](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/custom-partitioning-key) values, and therefore, during buffer flush, ClickHouse [will](https://clickhouse.com/blog/common-getting-started-issues-with-clickhouse#poorly-chosen-partitioning-key) create (at [least](https://clickhouse.com/docs/en/operations/settings/settings#settings-max_insert_block_size)) one new part per table partition.


The query is configured with 4 CTE identifiers (`db_name`, `table_name`, `last_x_minutes`, and `last_m_parts_per_node_per_partition`). The parameterized view `monitor_parts` has the same identifiers as parameters.


The query lists, for a specific database and table, the latest m newly created parts during the last x minutes per cluster node (`n`) and per table partition (`ptn`) the creation times (`write`), contained `rows` and compressed size `on disk`.


For convenience, we also show (`prev`) for each part how much time has passed since a previous part was created on the same cluster node for the same table partition.


This is an example result for a `SELECT * FROM monitor_parts(db_name='default', table_name='upclick_metrics’, last_x_minutes=10, last_m_parts_per_node_per_partition=4)` view query:
![monitoring_async_inserts_04.png](/uploads/monitoring_async_inserts_04_b3c16c0fc3.png)
The result shows the latest 4 created parts per cluster node (on a three\-node ClickHouse Cloud service) and per table partition within the last 10 minutes. As our [example target table](https://github.com/ClickHouse/examples/blob/main/blog-examples/async_inserts/upclick-gcp/commands/CREATE_TABLE.sql) doesn’t use a partitioning key, the `ptn` column is empty. We can see that on each of the three cluster nodes, a new part was created every 30 seconds. That was exactly how we configured asynchronous inserts in one of our benchmark [runs](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#benchmark-1) with a 30 seconds buffer flush time. Remember that the buffer exists [per](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#there-can-be-multiple-buffers) node.


### Buffer flushes [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#buffer-flushes)


In case the result of the previous query doesn’t show the expected part creation frequency for asynchronous inserts, a first debugging step would be to check the frequency of buffer flushes.


A query can be found [here](https://gist.github.com/tom-clickhouse/0135b7f125c96bb42a798105653fc8aa), which joins the [system.asynchronous\_insert\_log](https://clickhouse.com/docs/en/operations/system-tables/asynchronous_insert_log) and [system.query\_log](https://clickhouse.com/docs/en/operations/system-tables/query_log) tables. [Remember](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#there-can-be-multiple-buffers) that there is one separate buffer per cluster node and per insert query shape (the syntax of the insert query excluding the values clause / the data) and per [settings](https://clickhouse.com/docs/en/operations/settings/query-level).


The query is configured with 4 CTE identifiers (`db_name`, `table_name`, `last_x_minutes`, and `last_m_flushes_per_node_per_shape_per_settings`). The parameterized view `monitor_flushes` has the same identifiers as parameters.


The query lists, for a specific database and table, information about the latest `m` buffer flushes during the last `x` minutes per cluster node (`n`) per query shape (`q`) id per query settings (`s`) id. For each buffer flush, we list the `flush` time, the number of `rows`, and the amount of uncompressed `data` flushed to disk. For convenience, we also show (`prev`) for each buffer flush how much time has passed since a previous flush took place on the same node for the same query shape and settings. Plus, we show one concrete `sample_query` per insert query shape id and the `sample_settings` corresponding to a settings id.


This is an example result for a `SELECT * FROM monitor_flushes(db_name='default', table_name='upclick_metrics’, last_x_minutes=10, last_m_flushes_per_node_per_shape_per_settings=4)` view query:
![monitoring_async_inserts_05.png](/uploads/monitoring_async_inserts_05_2c1063e0dd.png)
The result shows the latest 4 buffer flushes per cluster node (on a three\-node ClickHouse Cloud service) and per query shape and settings within the last 10 minutes. We can see that on each of the three cluster nodes, a buffer flush took place every 30 seconds. That matches one of our benchmark [runs](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#benchmark-1) with a 30\-second buffer flush [timeout](https://clickhouse.com/docs/en/operations/settings/settings#async-insert-busy-timeout-ms). The flush times correlate with the part creation times returned from the [previous](blog/monitoring-asynchronous-data-inserts-in-clickhouse#part-creations) query. Note that all insert queries have the same shape and settings as indicated in the example result above.


### Insert errors during buffer flushes [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#insert-errors-during-buffer-flushes)


Insert errors can [occur](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#insert-errors-can-occur-during-buffer-flush) during buffer flushes. With the [default](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#default-return-behavior) asynchronous insert return behavior, the sender of the query gets a detailed error message returned instead of an acknowledgment. With the [fire and forget mode](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#fire-and-forget-return-behavior), however, the original insert into the buffer for that query gets successfully acknowledged to the sender, regardless of whether the insert into the target table during a later buffer flush actually succeeds or not.


[Here](https://gist.github.com/tom-clickhouse/9fa07e8a54acde9dfaa0a296f001ab93) is a query for finding out about insert errors during buffer flushes in hindsight. The query runs over the [system.asynchronous\_insert\_log](https://clickhouse.com/docs/en/operations/system-tables/asynchronous_insert_log) table and is configured with 3 CTE identifiers (`db_name`, `table_name`, and `last_x_minutes`). The parameterized view `monitor_flush_errors` has the same identifiers as parameters.


The query lists per cluster node (`n`) and error `status` and `exception` message the latest buffer `flush` times within the last x minutes during which the exception took place. Together with the `query_id` of one of the queries whose buffered data caused the insert error during the buffer flush. You can use this id for querying (or joining) the [system.query\_log](https://clickhouse.com/docs/en/operations/system-tables/query_log) table for getting more information about the specific query.


This is an example result for a `SELECT * FROM monitor_flush_errors(db_name='default', table_name='upclick_metrics’, last_x_minutes=10)` view query:
![monitoring_async_inserts_06.png](/uploads/monitoring_async_inserts_06_7e1fc33d80.png)
The result shows that some parsing errors happened during two buffer flushes per cluster node (on a three\-node ClickHouse Cloud service) within the last 10 minutes.


### Pending flushes [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#pending-flushes)


Lastly, [here](https://gist.github.com/tom-clickhouse/65e2fb5510c6b3f63221c79ba5f0d045) is a query that checks the current value of the [PendingAsyncInsert](https://clickhouse.com/docs/en/operations/system-tables/metrics#pendingasyncinsert) metric in the [system.metrics](https://clickhouse.com/docs/en/operations/system-tables/metrics) table for getting the number of asynchronous insert queries whose data is currently buffered and waiting to be flushed per cluster node.


This is an example query result:
![monitoring_async_inserts_07.png](/uploads/monitoring_async_inserts_07_d8a874e7ae.png)


## Scenarios [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#scenarios)


In this section, we are going to use some of the queries from the previous section to identify the root cause of buffer flush and part write frequencies.


### Simple and straightforward [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#simple-and-straightforward)


When no partitioning key is used in the target table, and each insert query has the same shape and settings, we will see that the buffer gets flushed according to the [configured](https://clickhouse.com/docs/en/operations/settings/settings#asynchronous-insert-settings) flush threshold settings, and there is a 1 relationship between buffer flushes and parts written to disk. This occurs [per](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#there-can-be-multiple-buffers) node. The following two example query results for the [buffer flushes](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#buffer-flushes) and [part creations](blog/monitoring-asynchronous-data-inserts-in-clickhouse#part-creations) queries demonstrate this:
![monitoring_async_inserts_08.png](/uploads/monitoring_async_inserts_08_330f3facff.png)
On a three\-node ClickHouse Cloud service, we configured asynchronous inserts in one of our benchmark [runs](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#benchmark-1) with a 30\-second buffer flush time. We see that there is a buffer flush every 30 seconds on each node, resulting in a part being written to disk every 30 seconds per node. See the highlighted rows in the two query results above, where the same color is used for corresponding buffer flushes and part creations.


### Multiple partitioning keys [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#multiple-partitioning-keys)


When a partitioning key is [used](https://gist.github.com/tom-clickhouse/2362a0279f2159cc162e0105bc745952) in the target table, then there is generally no longer a (per node) 1 relationship between buffer flushes and parts written to disk. Instead, more than one part can be created per buffer flush. The next two example query results show this:
![monitoring_async_inserts_09.png](/uploads/monitoring_async_inserts_09_de264230e3.png)
The highlighted rows in the two query results above indicate that a single buffer flush on one node resulted in three parts being written to disk on the same node at the same time. Because the rows in the buffer contained three different partitioning key values when the buffer was flushed.


### Multiple query shapes [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#multiple-query-shapes)


Because there [is](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#there-can-be-multiple-buffers) one separate buffer per insert query shape (and per node), more than one buffer flush can potentially occur per [configured](https://clickhouse.com/docs/en/operations/settings/settings#asynchronous-insert-settings) buffer flush threshold on a single node. These two example query results sketch this:
![monitoring_async_inserts_10.png](/uploads/monitoring_async_inserts_10_3171ae2deb.png)
We configured asynchronous inserts with a 30\-second buffer flush time. As indicated by the two highlighted rows in the `Buffer flushes` query result above, two buffer flushes took place on the same node on the next buffer flush timeout. Because the node received insert queries for the same target table but with two different syntactic shapes, there are two separate buffers on the node. As indicated by the two highlighted rows in the `Parts written do disk` query result, there is still a 1 relationship between buffer flushes and parts written to disk as there is no partitioning key is used in the target table.


### Multiple settings [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#multiple-settings)


Similarly to different query shapes, there [is](https://clickhouse.com/blog/asynchronous-data-inserts-in-clickhouse#there-can-be-multiple-buffers) a separate buffer per set of unique insert query [settings](https://clickhouse.com/docs/en/operations/settings/query-level). This can be useful for enabling different flush thresholds for data for the same table, and to control resource usage of specific data. We can observe these mixed buffer flush cycles below:
![monitoring_async_inserts_11.png](/uploads/monitoring_async_inserts_11_84c65f38ec.png)
The two highlighted rows in the `Buffer flushes` query result above show that there are two separate and different flush cycles on the same node for the same target table. Because the node received insert queries for the same target table but with two different settings, specifically buffer flush [threshold settings](https://clickhouse.com/docs/en/operations/settings/settings#asynchronous-insert-settings), there are two buffers with separate flush cycles on the node. The two highlighted rows in the `Parts written do disk` query result show that there is still a 1 relationship between buffer flushes and parts written to disk, as there is no partitioning key is used in the target table.


### Combinations [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#combinations)


There can be scenarios with a combination of a partitioned target table and async inserts for this table with different query shapes and settings. This results in each cluster node operating a buffer per different query shape per setting set. This creates ([at least](https://clickhouse.com/docs/en/operations/settings/settings#max_insert_block_size)) one part per different partitioning key value stored in the rows contained in the buffer when one of these buffers gets flushed. Our provided `Buffer flushes` and `Parts written do disk` introspection queries will indicate this properly.


## Summary [\#](/blog/monitoring-asynchronous-data-inserts-in-clickhouse#summary)


In this blog post, we provided guidance and queries for introspecting asynchronous inserts. You can use the provided queries for double\-checking and for troubleshooting your asynchronous insert configurations.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
