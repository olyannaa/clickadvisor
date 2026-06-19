# Zero\-Copy Graph Analytics: Getting Started With LakeHouse Graph


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Zero\-Copy Graph Analytics: Getting Started With LakeHouse Graph

![](/_next/image?url=%2Fuploads%2FImage_from_Slack_1_7e5e2df440.png&w=96&q=75)Maruthi LokanathanFeb 3, 2026 · 10 minutes read## The Problem You Already Know [\#](/blog/zero-copy-graph-analytics#the-problem-you-already-know)


You have a lot of data sitting in your analytical database. Millions of customers, billions of transactions. And now someone asks: “Which customers are connected through shared purchases? What fraud rings exist in our transaction network?”


If you’ve tried answering relationship questions with SQL, you know what happens. You write a recursive CTE. It times out at 3 hops. You try self\-joins. The query plan explodes. So you think: maybe I need a graph database.


And that’s where things get complicated.


To use a graph database, you need to copy your data there. That means building an ETL pipeline. Maintaining it. Watching it break when schemas change upstream. Organizations report that data engineers spend [12 hours per week](https://www.integrate.io/blog/etl-market-size-statistics/) just “chasing data” across disconnected systems. The ETL tools market is projected to grow from [$8\.5 billion to $24\.7 billion by 2033](https://www.integrate.io/blog/etl-market-size-statistics/) \- that’s a lot of money spent moving data around instead of using it.


Here’s the thing: **every time you copy data, you create a sync problem.** Now you have two systems, two schemas, and queries running on data that’s already stale.


What if you didn’t have to copy the data at all?


## How It Usually Works (And Why It Breaks Down) [\#](/blog/zero-copy-graph-analytics#how-it-usually-works-and-why-it-breaks-down)


The traditional approach treats your OLAP database and your graph database as separate systems:


![Zero-Copy Graph Analytics Blog Banner (2).jpg](/uploads/Zero_Copy_Graph_Analytics_Blog_Banner_2_8486c7b04b.jpg)
You get SQL analytics from your warehouse. You get graph queries from your graph database. But connecting them requires that ETL pipeline in the middle.


The pain points add up:


- **Dual storage costs** \- You’re paying to store the same data twice
- **Sync lag** \- Your graph queries run on data that’s minutes to hours old
- **Schema evolution** \- Change a column in the warehouse, now you’re debugging two systems
- **Pipeline ownership** \- Someone has to maintain that sync job forever


One [case study](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-zero-etl-paradigm-transforming-enterprise-data-integration-in-real-time) showed that migrating away from traditional ETL reduced latency by 98% (from 30 minutes to under 30 seconds) and cut operational costs by 66%. That’s not a marginal improvement \- that’s a different way of working.


## The Zero\-Copy Alternative [\#](/blog/zero-copy-graph-analytics#the-zero-copy-alternative)


So what if you could query relationships directly on your existing data?


That’s the idea behind zero\-copy graph analytics. Instead of copying data into a separate graph database, you add a graph query layer on top of your analytical database.


![Zero-Copy Graph Analytics Blog Banner.jpg](/uploads/Zero_Copy_Graph_Analytics_Blog_Banner_bc8b067a03.jpg)
PuppyGraph connects to ClickHouse via JDBC and provides a graph query interface (Cypher/Gremlin). No data movement. The same tables that power your SQL dashboards also serve graph traversals.


What you get:


- **Real\-time data** \- Query data as it exists now, not as of last sync
- **Single source of truth** \- One schema, one storage layer
- **No sync pipeline** \- Nothing to maintain, nothing to break
- **Lower costs** \- No duplicate storage


The key insight is simple: your data already has relationships. Customers buy products. Accounts make transactions. Devices connect to accounts. You don’t need to move data to query those relationships \- you just need the right query interface.


## The Bigger Picture: Lakehouse Graph [\#](/blog/zero-copy-graph-analytics#the-bigger-picture-lakehouse-graph)


Zero\-copy isn’t just a technique \- it’s part of a broader shift in how we think about data architecture.


Think of it like this: you have a library. For years, if you wanted to study books (SQL analytics), you went to the main reading room. If you wanted to understand how books cite each other (graph queries), you had to photocopy everything and take it to a separate research annex across town. Every time the library got new books, someone had to update the annex. It worked, but it was slow and expensive.


The data lakehouse changed the first part of this equation. Open table formats like [Delta Lake and Iceberg](https://www.puppygraph.com/blog/iceberg-vs--delta-lake) turned that reading room into a proper research library \- warehouse\-grade reliability on low\-cost object storage. SQL engines, ML pipelines, and streaming workloads all started converging on the same data. One library, many ways to use it.


But graph remained the outlier. If you wanted to trace relationships, you still had to make copies and maintain that research annex.


The [Lakehouse Graph](https://www.bigdatawire.com/2025/01/24/puppygraph-brings-graph-analytics-to-the-lakehouse/) approach finally closes this gap. Instead of copying data to a separate graph database, you add a graph query layer directly to your lakehouse. The same tables that serve your SQL dashboards also serve graph traversals. One library. All the tools you need. No photocopies.


Here’s what this means in practice: your data team isn’t maintaining two systems anymore. When new data lands in ClickHouse, it’s immediately available for both aggregation queries and relationship traversals. Schema changes happen once. There’s no “graph is 2 hours behind” conversation.


ClickHouse handles what it’s good at \- the heavy aggregations, time\-series analysis, and analytical queries that need to scan billions of rows fast. PuppyGraph adds the graph layer on top, giving you multi\-hop relationship queries without moving data elsewhere. You’re not replacing one system with another \- you’re extending what your existing system can do.


This is the direction modern data architecture is heading: fewer specialized systems, more capabilities on the same data. The question isn’t “SQL or graph?” anymore. It’s “what question do you have?” and the same data answers both.


## Why Graph Queries Matter [\#](/blog/zero-copy-graph-analytics#why-graph-queries-matter)


Not all questions fit naturally into SQL.


SQL works well for set\-based operations: filter these rows, aggregate that column, join these tables. But some questions are fundamentally about traversing relationships:


- Which customers bought similar products to this customer?
- What accounts share devices with flagged accounts?
- How does money flow through a network of transfers?


If you’ve written a 5\-hop query in SQL (find accounts connected to accounts connected to accounts…), you’ve seen the query plan explode. Each hop adds another join. Performance degrades exponentially.


Graph databases handle this differently. They use index\-free adjacency \- each node stores direct pointers to its neighbors. Traversing a relationship is a constant\-time operation, not a table scan. Studies show graph databases can be [50% faster for multi\-hop relationship queries](https://www.puppygraph.com/blog/graph-database-vs-relational-database) compared to relational systems.


The trade\-off was always: do I copy my data into another system? Zero\-copy removes that trade\-off.


## What This Looks Like in Practice [\#](/blog/zero-copy-graph-analytics#what-this-looks-like-in-practice)


I built a reference implementation with two use cases to demonstrate how this works. The full code is in the [GitHub repository](https://github.com/maruthiprithivi/zero_copy_graph_analytics).


### Customer 360: Product Recommendations [\#](/blog/zero-copy-graph-analytics#customer-360-product-recommendations)


The dataset has 35\.4 million records: 1 million customers, 7\.3 million transactions, 27 million interactions.


For aggregations, you use SQL:



```

```
1-- Customer lifetime value by segment
2SELECT segment, AVG(ltv) as avg_ltv, COUNT(*) as customers
3FROM customers
4GROUP BY segment
5ORDER BY avg_ltv DESC;
```

```

For relationship queries, you use Cypher:



```

```
1// Find products frequently bought together
2MATCH (c:Customer)-[:PURCHASED]->(p1:Product)
3MATCH (c)-[:PURCHASED]->(p2:Product)
4WHERE p1.category = 'Electronics'
5  AND p2.category = 'Electronics'
6  AND p1 <> p2
7RETURN p1.name, p2.name, COUNT(DISTINCT c) as co_purchases
8ORDER BY co_purchases DESC
9LIMIT 10;
```

```

Both queries run on the same underlying tables. No sync. No lag.


### Fraud Detection: Finding Hidden Networks [\#](/blog/zero-copy-graph-analytics#fraud-detection-finding-hidden-networks)


The fraud dataset has 1\.29 million records with 5 embedded fraud patterns: account takeover rings, money laundering networks, card fraud, synthetic identity, and merchant collusion.


Individual transactions look normal. It’s only when you see the network that fraud patterns emerge.



```

```
1// Detect accounts sharing devices (account takeover pattern)
2MATCH (a1:FraudAccount)-[:USED_DEVICE]->(d:FraudDevice)<-[:USED_DEVICE]-(a2:FraudAccount)
3WHERE a1 <> a2 AND d.is_suspicious = 1
4RETURN d.device_id, d.location,
5       COLLECT(DISTINCT a1.account_id) as connected_accounts
6ORDER BY SIZE(connected_accounts) DESC
7LIMIT 10;
```

```

This query finds accounts that share a suspicious device \- a classic account takeover pattern. In SQL, this would require self\-joins that get slow at scale. As a graph traversal, it runs in milliseconds.


## What About Query Performance [\#](/blog/zero-copy-graph-analytics#what-about-query-performance)


There is always this question “what is the impact on query performance?” when we talk about running Graph Queries without having a native Graph Storage. Yes, we will experience a higher query latency for the trade\-off we have made. To objectively analyze if this query latency will be significant enough to make a difference we generated appropriate queries for the two use cases we covered in the previous section. It was a total of 97 queries comprised of 42 SQL and 55 Cypher queries that covered specific areas across the two use cases, the following is the summary of the Zero\-Copy Query Performance:




| Metric | Value |
| --- | --- |
| Median Latency | 28ms |
| P95 Latency | 148ms |


The raw numbers matter less than what they represent: you can run both analytical queries and graph traversals on the same data, with response times suitable for interactive use.


And the architecture scales. ClickHouse powers analytics at companies like [Tesla, Anthropic and Cloudflare](https://clickhouse.com/user-stories) at petabyte scale. PuppyGraph is a stateless query layer that scales horizontally with the underlying database.


## Try It Yourself [\#](/blog/zero-copy-graph-analytics#try-it-yourself)


The reference implementation is available on GitHub with everything you need:



```

```
1# Start ClickHouse and PuppyGraph
2make local
3
4# Generate test data
5make generate-local
6
7# Access PuppyGraph UI
8open http://localhost:8081
```

```

The repository includes:


- Two use cases (Customer 360, Fraud Detection) with realistic data patterns
- 97 validated queries you can run immediately
- Both local and hybrid deployment options


## The Takeaway [\#](/blog/zero-copy-graph-analytics#the-takeaway)


If you have relationship questions about your data, you don’t need to choose between copying data to a graph database or writing painful recursive SQL.


The Lakehouse Graph approach brings graph queries to where your data already lives. Zero\-copy means fresher data, simpler architecture, and less infrastructure to maintain. Whether you’re building recommendations, detecting fraud, or mapping supply chains \- the pattern is the same: query relationships without moving data.


The [repository](https://github.com/maruthiprithivi/zero_copy_graph_analytics) has working code you can run in 10 minutes. Take a look.


**References**


- [Integrate.io: ETL Market Size Statistics](https://www.integrate.io/blog/etl-market-size-statistics/)
- [ISACA: The Zero\-ETL Paradigm](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-zero-etl-paradigm-transforming-enterprise-data-integration-in-real-time)
- [BigDataWire: Graph Analytics on the Lakehouse](https://www.bigdatawire.com/2025/01/24/puppygraph-brings-graph-analytics-to-the-lakehouse/)
- [PuppyGraph: Graph vs Relational Databases](https://www.puppygraph.com/blog/graph-database-vs-relational-database)
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
