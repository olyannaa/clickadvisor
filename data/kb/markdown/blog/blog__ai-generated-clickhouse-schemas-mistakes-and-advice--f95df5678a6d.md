# AI doesn’t always generate perfect ClickHouse schemas (yet)


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# AI doesn’t always generate perfect ClickHouse schemas (yet)

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)[Al Brown](/authors/al-brown)Mar 13, 2026 · 13 minutes readAsk any LLM to design a ClickHouse table for real\-time event analytics and you'll often get something like this:



```

```
1CREATE TABLE events
2(
3    event_id UUID,
4    user_id UInt64 CODEC(Delta, ZSTD(3)),
5    event_type LowCardinality(String),
6    timestamp DateTime64(3) CODEC(DoubleDelta, ZSTD(1)),
7    properties JSON,
8    session_id String CODEC(ZSTD(3)),
9    page_url String CODEC(ZSTD(5)),
10    duration_ms UInt32 CODEC(T64, ZSTD(3))
11)
12ENGINE = ReplacingMergeTree(timestamp)
13PARTITION BY toYYYYMM(timestamp)
14ORDER BY (event_type, user_id, timestamp)
15SETTINGS index_granularity = 4096
16
17-- Projection for user-level queries
18ALTER TABLE events ADD PROJECTION user_events
19(
20    SELECT * ORDER BY (user_id, timestamp)
21);
```

```

This looks reasonable at first glance. It's syntactically correct. It uses ClickHouse\-specific features. You *could* drop this straight into production.


But there are many choices in this schema that might not be right for you:


- **Custom partitioning**. This is the single most common giveaway of an AI\-generated schema. Partitioning in ClickHouse is primarily a data management feature, not a query optimization feature.
- **Custom codecs on every column**. ClickHouse's default compression is already excellent, and ideal for most users. Column\-level codec tuning is something to do when you know you really need it.
- **A projection duplicating most of the table**. Projections are a powerful feature, but they come with real costs at scale that we'll cover later. Adding one from day one, before you've even seen production query patterns, is classic over\-optimization.


None of these choices are inherently wrong, and you may end up using them *at some point*. But it’s also quite likely that you *never* need them. And this is where LLMs can take you down the wrong path. They’re smart, but sometimes they try to be *too smart*.


The right approach is almost always the opposite: start with a basic table, a sensible ORDER BY, default compression, no partitions, no projections. Run your actual workload. Measure. Then add complexity where the data tells you it's needed. The [ClickHouse Agent Skills](https://github.com/ClickHouse/agent-skills) can help an LLM to make the right choices, when they’re needed.


This post walks through the common pitfalls we see when AI generates ClickHouse schemas, drawn from real conversations with our Solutions Architecture team and patterns across dozens of customer engagements.


## Common mistakes [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#common-mistakes)


### 1\. Partitioning for query speed [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#1-partitioning-for-query-speed)


**The scenario:** A user asks their LLM "how do I make this query faster?" and the LLM suggests partitioning by a frequently filtered column.


Outside of niche cases or extreme scale, this is usually wrong.


Partitions in ClickHouse are designed as a data management feature. They *can* speed up queries *if* you partition very carefully, but that's not their primary purpose and the gain isn’t free.


There are a few cases where partitioning on a dimensional field makes sense for performance, and ClickHouse’s Solutions Architects occasionally recommend it to users. But when they do, they walk through all of the trade\-offs:


- You will need to pay more attention to how you insert data, ensuring you align inserts with your partitioning strategy, potentially pre\-sorting before inserting or collecting larger batches.
- It affects other operations: how you handle TTLs, how you think about merges, how you monitor part counts
- If you [partition by a high\-cardinality field](https://clickhouse.com/docs/best-practices/choosing-a-partitioning-key), you can end up with a part explosion that degrades performance across the board.



> I recently helped a customer who needed to bring their end\-user query latency down by 200ms. They had complex queries and very high scale. We’d already tuned the ORDER BY, queries, and data types, and partitioning was the last call. I had to explain: “this completely changes how you manage your table. But if you need that extra 200 milliseconds of latency, this is what it's going to take.” I only make that recommendation when we’ve done everything else we can do. \- Jack Borthwick, Solutions Architect


**What to do instead:** [Optimize your `ORDER BY` key first](https://clickhouse.com/docs/best-practices/choosing-a-primary-key). That's where the majority of query performance in ClickHouse comes from. Partitioning should be driven by data lifecycle requirements (dropping old data, managing retention), not query speed.


### 2\. OPTIMIZE TABLE ... FINAL [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#2-optimize-table--final)


**The scenario:** A user adopts `ReplacingMergeTree` to handle deduplication. They insert data and notice duplicates are still showing up in query results. This is expected as ClickHouse deduplicates during background merges, not at insert time. So they ask their LLM: "How do I force deduplication in ClickHouse?"


The LLM responds: run `OPTIMIZE TABLE ... FINAL`.


This forces ClickHouse to merge all parts in a partition down as aggressively as possible. It bypasses the normal part size limits, including the limits set on your service or cluster. This is true across both OSS and Cloud.


The result is that you can end up with parts that are massively oversized, potentially terabytes. This is irreversible, and you can't un\-merge those parts.


The downstream consequences can be worse than the original problem: it can cause future mutations to fail. If you later try to add a column or an index, ClickHouse needs to rewrite those oversized parts, and those operations can break.


**What to do instead:** [Use the `FINAL` keyword](https://clickhouse.com/docs/guides/replacing-merge-tree) in your `SELECT` queries if you need deduplicated reads before merges have completed. Understand that materialising deduplication is eventually consistent by design, and ClickHouse will merge and deduplicate in the background.


### 3\. Materialized View sprawl [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#3-materialized-view-sprawl)


**The scenario:** A user has five slow query shapes. They ask the LLM to optimize each one. The LLM creates an incremental materialized view for each. The user now has five MVs. A month later, they have fifteen. Eventually, ingestion pays the price and becomes too slow.


Materialised Views are a powerful way to optimise queries, but they aren’t free. Every incremental materialized view fires on every insert to the source table, meaning the more materialised views, the more work ClickHouse does during an insert.


We regularly see users end up with a sprawl of countless, intertwined tables with different engines, materialized views, refreshable materialized views, and incompatible features downstream of each other, because the LLM tried to solve each problem in isolation without understanding the overall architecture.


Often, it's such a mess that the user doesn't understand it either. The first step is always the same: map out every table, every view, every dependency, and figure out what each piece is actually doing. Often we find entire branches of the pipeline that are either broken or redundant.


**What to do instead:** Start with zero materialized views. Run your queries against the base table. Profile them. When you find a query pattern that genuinely can't be served at acceptable latency from the base table, add a single MV and measure the impact on ingestion. Treat each MV as a cost you're paying on every insert.


### 4\. JSON column misconfiguration [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#4-json-column-misconfiguration)


**The scenario:** A user has fully unstructured data with dynamic keys. The LLM suggests using ClickHouse's JSON type. The user inserts data that has unbounded variability, resulting in thousands of unique key paths.


[The ClickHouse JSON type is powerful, and can allow you to build highly performant analytics over semi\-structured data](https://clickhouse.com/blog/json-data-type-gets-even-better), even when your data has thousands of key paths. However, it needs to be used appropriately for the nature of your data.


Under the hood, ClickHouse creates physical sub\-columns for your key paths, up to a set limit (`max_dynamic_paths`, default \= 1000\). Using physical sub\-columns makes sense when these key paths are common, and you’re likely to use those columns in your analytics.


However, if your data is truly dynamic with user\-defined properties, varying schemas, or unpredictable fields, you can create hundreds of persistent columns that are mostly empty and never queried. Or worse, raise the `max_dynamic_paths` limit to tens of thousands to accommodate.


The JSON type can be used effectively in both cases, but must be applied differently. We see LLMs rarely apply the appropriate settings for either scenario.


**What to do instead:** If your data is highly dynamic with unpredictable key paths, set `max_dynamic_paths` to 0\. This gives you a bucketed map type with no persistent sub\-columns, and it works well for data where you don't need columnar access to individual keys. Do **not** raise the `max_dynamic_paths` into the thousands.


If your data is semi\-structured and you have a manageable amount of frequently used key paths, use the JSON type and name which specific fields should be stored in a physical sub\-column. If your data is semi\-structured but legitimately has thousands of frequently used key paths, look into the [**advanced serialisation format** within the JSON type](https://clickhouse.com/blog/json-data-type-gets-even-better#advanced-shared-data). Note that the different serialisation formats have their own trade offs, particularly in regards to ingest performance.


### 5\. Projections that don't scale [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#5-projections-that-dont-scale)


**The scenario:** A user needs to serve queries with different ordering requirements. The LLM suggests adding projections. At development scale, perhaps a few hundred gigabytes, this works beautifully. But when the table grows to 5\-10\+ terabytes, latency spikes.


At query time, ClickHouse evaluates the mark counts across all projections to choose the optimal one for the query. As data grows, this evaluation itself becomes expensive. A projection that saved you time at small scale can add one to two seconds of latency at large scale, on every query, regardless of whether that projection is ultimately used.


**What to do instead:** Projections are a great feature at the right scale and for the right use case. If you're working with data under a few terabytes and have well\-defined alternative query patterns, they're a good option. If you're growing toward or past 5\-10TB, test projection performance explicitly with production\-scale data before committing to them.


## Optimisation requires nuance [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#optimisation-requires-nuance)


When an experienced engineer looks at a complex data problem \- say, denormalizing data from Postgres while handling deduplication and joining across tables \- they rarely give you "the answer." They give you three or four options, each with their own trade\-offs. Maybe option A gives you faster queries but slower ingestion. Option B simplifies the pipeline but requires more hardware. Option C decouples the systems but adds operational complexity. They lay out the options and say: pick the one that fits your business.


LLMs bias towards confidence over nuance. Rarely do they say "it depends" and present trade\-offs.


Every well\-adopted system has this challenge: there's a ton of content out there covering the basics: tutorials, getting\-started guides, best\-practices. And there’s some, though often less, content covering advanced topics. LLMs train on all of it and get the fundamentals mostly right. But there's a sharp drop\-off between "best practices content that applies broadly" and "specific, advanced guidance that applies to your exact scenario." So the LLM does the only thing it can: takes generic advice and applies it to your situation without knowing whether it's the right call.


There's a frontier beyond which the LLM is effectively guessing, and it'll never tell you when it's crossed it.


## Our advice for your LLM workflow [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#our-advice-for-your-llm-workflow)


None of this means you should stop using LLMs for ClickHouse. They're a genuine accelerator for getting started, writing queries, and understanding basic concepts. Here's how to get the most out of them without ending up in the situations described above.


**Start simple and earn complexity.** Your initial schema should be boring: a `MergeTree` (or `ReplacingMergeTree` if you need deduplication), a well\-chosen `ORDER BY`, default compression, no partitions, no projections, no MVs. Add complexity only after you've measured your actual workload and identified a specific bottleneck.


**Work with your LLM to understand its choices.** If an LLM generates a schema with particular details that you don’t immediately recognise as correct, ask it about the choices it made. This does two things: it catches problems before they reach production, and it builds your own understanding of the system you're about to operate. Treat the LLM like a sparring partner you can interrogate until you understand every decision in your DDL.


**Know when to talk to a human.** If you're denormalizing data from Postgres, handling complex deduplication, joining tables on ingestion, or working at multi\-terabyte scale — stop and get expert input. There aren't enough patterns on the internet for the LLM to reliably solve these problems. That's not a knock on the technology; it's just the current state of the training data.

### Get started today

ClickHouse Cloud users have access to teams of ClickHouse experts, including the original creators of ClickHouse. Use AI to go fast, and count on ClickHouse support when you need it.[Sign up](https://console.clickhouse.cloud/signUp?loc=blog-cta-93-get-started-today-sign-up&utm_blogctaid=93)## The future is collaborative [\#](/blog/ai-generated-clickhouse-schemas-mistakes-and-advice#the-future-is-collaborative)


We anticipate that more and more engineers will use AI agents to design and operate their databases. It’s an inevitable trend and, on the whole, a good one. LLMs are going to get more capable. There will be more ClickHouse\-specific content for them to train on. The frontier of what they can handle reliably will keep moving forward.


But right now, today, there is a meaningful gap between what LLMs can confidently generate and what will actually work at scale in production. That gap is where the pitfalls in this post live. Until it closes, humans still need to play a critical role in validating AI output, especially for the complex, high\-stakes, scale\-dependent decisions that determine whether your product works or falls over.


Use AI to go fast. Use human judgment to go right.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
