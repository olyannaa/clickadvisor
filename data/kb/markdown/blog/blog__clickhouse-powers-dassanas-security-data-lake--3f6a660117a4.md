# ClickHouse Powers Dassana’s Security Data Lake


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Powers Dassana’s Security Data Lake

![](/_next/image?url=%2Fuploads%2FDassana_edd9263fa2.jpg&w=96&q=75)Gaurav KumarJan 23, 2023 · 10 minutes read*We would like to welcome Gaurav Kumar, Founder and CEO of Dassana as a guest to our blog today. Read on to hear why they chose ClickHouse for their Security Data Lake which consolidates disparate data sources to provide contextualized data insights.*


## Challenge with SIEMs [\#](/blog/clickhouse-powers-dassanas-security-data-lake#challenge-with-siems)


Modern enterprises have made significant investments in security products in recent years due to increased cyber risks and their impact on businesses. From little to no visibility, customers now have more visibility than they can manage. A typical large enterprise today uses more than a dozen security technologies. These tools emit data in various shapes and sizes, making it harder to make sense of the data.


For example, if you are tasked with creating a simple executive dashboard that shows the cybersecurity posture of various business units, how will you go about it? Perhaps you want to show how long each business takes to resolve security issues (mean\-time\-to\-remediation)? How about ranking business units by SLA violations?


![Dasana_Dashboard.png](/uploads/Dasana_Dashboard_9f343960e6.png)
*In the screenshot above Dassana provides an interesting insight: there is a spike in SLA violations for medium level severity issues. We can also see which team is likely responsible for this (the Finance team). All of the visualizations in Dassana are drill\-downs so we can find out the underlying reason. Without Dassana, security teams would have spent countless hours fetching data from different sources and normalizing it.*


These seemingly simple questions are painfully answered today by writing complex SIEM queries (if you are lucky, all the data is being sent to SIEM). But then, even modern SIEMs are designed for immutable time series event data, e.g. logs. But security data is much more than just logs. For example, the state of an alert could be “open” or “closed”. Say you want to find out how many alerts are in an “open” state, how will you go about it? If the alert was in an “open” state an hour ago, and you sent that event to a SIEM but now the alert state has changed to “closed”, can you send an update request to your SIEM updating the alert state from “open” to “closed”? Of course, you can’t, it is called immutable for a reason. So the solution to this problem is re\-inserting the updated data, and then just querying the most recent data. These are called last point queries and are quite notorious when run on append\-only systems like SIEMs.


Not only the fundamental “mutating” nature of security data makes SIEMs hard to operate, but SIEMs companies have also stopped innovating and investing in solving basic problems such as data normalization. What AWS calls an “account” id, GCP calls it a “project” id, and Azure calls it a “subscription” id. Wouldn’t it be beautiful if we can just normalize these things and call them something like “AssetContainerId”. This way, if the system supports SQL, you can just write queries like \-



```
select count(*) as count,assetContainerID from findings where status='open' group by assetContainerID

```

![Dasana_Query.png](/uploads/Dasana_Query_5637ad20fe.png)
*In the above example, we are showing the count of assets grouped by normalized asset type.*


That dream is what Dassana is. Dassana ingests data from various security sources like CSPM tools, IDS, etc, and normalizes it \- which allows you to query and visualize it in a schema\-less manner, all thanks to the power of ClickHouse.


## Why we chose ClickHouse [\#](/blog/clickhouse-powers-dassanas-security-data-lake#why-we-chose-clickhouse)


We evaluated more than a dozen different big data systems before settling on ClickHouse. No system comes close to ClickHouse when it comes to the flexibility ClickHouse provides. Specifically, the following features and architectural advantages won us over:


- Different table engines allow us to store data in the format that suits the use case.
- Ability to insert data frequently using asynchronous inserts. Most big data systems force you to batch data which adds a lot of complexity on the application side.
- In\-built accounting system to track query costs such as the number of rows read, etc.
- Ability to automatically move data to a different storage tier. This is an essential feature for data archival and having an in\-built storage tier system has saved us precious development time. As icing on the cake, ClickHouse supports row level and column level TTLs (time to live) too.
- Advanced external dictionary options such as the ability to populate (and refresh) dictionaries from Postgres database and HTTP servers.


As a seed\-funded start\-up, we also evaluated the cost savings at length and found that ClickHouse would cost us a fraction of what it would cost compared to other big data systems.


## How Dassana uses ClickHouse [\#](/blog/clickhouse-powers-dassanas-security-data-lake#how-dassana-uses-clickhouse)


When we first started, under the covers, Dassana heavily used the [ReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree/) table engine to store mutable data. When the state of a finding (alert) needed to be updated, we inserted a new row for the same alert with an updated state value and let the table engine handle deduplication logic. But this didn’t solve the problem when we wanted to provide near real\-time deduplicated results back. This is where advanced features like [AggregatingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree/) with a materialized view came into play.


In case you are wondering if the data was stored twice, once in ReplacingMergeTree and then again in [AggregatingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree/), the answer is no, thanks to ClickHouse's [TTL](https://clickhouse.com/docs/en/sql-reference/statements/alter/ttl/) feature.


To query duplicated data, we used a “group by” aggregation query. While this approach worked for a while, as our data grew we started hitting performance issues. You can read more about this deduplication approach here [Row\-level Deduplication Strategies for Upserts and Frequent Updates](https://clickhouse.com/docs/en/guides/developer/deduplication)


None of the suggested approaches worked for us at scale, and this is when we realized the magical power of the dictionary feature of ClickHouse.


Let’s take an example. Consider the following schema:



```
CREATE TABLE default.foo (
   tenant UUID,
   record_id UInt64,
   insert_ts UInt64,
   data String,
   insert_ts_dt DateTime MATERIALIZED toDateTime(divide(insert_ts,1000))
)
Engine = ReplacingMergeTree(insert_ts)
ORDER BY (tenant, record_id);

```

Here, `record_id` is the unique “asset id” or the entity id for which we want to query deduplicated data. “data” is just an arbitrary value for the `record_id`.


Now, let’s create a dictionary like this:



```
CREATE OR REPLACE DICTIONARY default.foo_last_point_dict
(
   `record_id_hash` UInt64,
   `insert_ts` UInt64
)
PRIMARY KEY record_id_hash
SOURCE(CLICKHOUSE(
   QUERY '
           SELECT cityHash64(tenant, record_id) as record_id_hash, max(insert_ts)
           FROM table_x
           WHERE {condition}
           GROUP BY record_id_hash
           ORDER BY record_id_hash
       '
   update_field 'insert_ts_dt'
   update_lag 120
))
LIFETIME(5)
LAYOUT(SPARSE_HASHED(PREALLOCATE 0));

```

The most important thing to note here is the query:



```
SELECT cityHash64(tenant, record_id) as record_id_hash, max(insert_ts)
           FROM table_x
           WHERE {condition}
           GROUP BY record_id_hash
           ORDER BY record_id_hash

```

This query is periodically run by ClickHouse according to the LIFETIME (5 seconds above). The value of `insert_ts_dt`, configured via `update_field`, is injected into the `WHERE` clause to determine the data that is returned. This query returns the max `insert_ts` for each `record_id_hash` used to populate the dictionary.
To query the data, we run a SQL query like this:



```
SELECT * FROM foo
WHERE equals(insert_ts, dictGet('default.foo_last_point_dict, 'insert_ts', cityHash64(tenant, record_id)))

```

This query selects the rows in the main table where the `insert_ts` is the same as that in the last\-point (most recent) value in the dictionary.


As with any system, the total complexity remains the same \- you can just shuffle it around. In this case, we wanted great performance, but it comes with the following challenges that one must be aware of:


- If the cardinality of `record_id` is very high, there will be higher memory consumption. Fortunately, we found that we can store hundreds of millions of assets (distinct `record_id`) data on a 32GB RAM box.
- There is a short time window of 5 seconds (dictionary load frequency) during which the query will match stale data. This is within our accuracy budget as anyhow the data is loaded in a streaming fashion and most analytical queries for our use case are about trending and approximation.


It is worth mentioning that we experimented with the “Join” table engine too but found the performance of our dictionary based approach to be far more performant.


## Lessons Learned [\#](/blog/clickhouse-powers-dassanas-security-data-lake#lessons-learned)


While this post has shown you some of the powerful features of ClickHouse, we want to highlight some of our learnings too. ClickHouse, in all its glory and power, is a force that needs to be handled with due care and attention to detail. Some of our learnings are:


1. Production parity. Most likely, you are running ClickHouse on Intel CPUs. Don’t run tests on Apple Silicon and expect everything to work the same on Intel CPUs. Of all the ClickHouse builds, Intel builds are the most stable. Similarly, try allocating the same amount of resources to the test cluster as available to the production cluster. This might sound expensive, but you can turn off the test cluster when not in use. Certain issues only surface when the system is heavily used.
2. Don’t manage ClickHouse manually. It is a crime if you are not using ClickHouse Cloud since this takes away a lot of the complexity of scaling and replicating data.
3. Don’t use experimental features in production. This should be obvious learning, but it is sometimes tempting to use experimental features. For example, we started using projections when they were almost in production, but we should have waited. Wait for the training wheels to come off.


### About Dassana [\#](/blog/clickhouse-powers-dassanas-security-data-lake#about-dassana)


Founded by a team of successful serial entrepreneurs and cloud security veterans, we're building a security data lake to consolidate disparate data sources and provide contextualized data insights. We aim to simplify data access at scale without compromising performance and optimizing costs to enable customers to focus on strategic business priorities.


Learn more about Dassana [here](https://dassana.io/).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
