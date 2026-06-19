# That’s a wrap: highlights from Open House, our first user conference


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# That’s a wrap: highlights from Open House, our first user conference

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 3, 2025 · 13 minutes readLast week, we hosted Open House, our first user conference in San Francisco. The day was packed with product updates, demos, customer stories, and technical deep dives. But that’s not all \- we also announced our [Series C financing](https://clickhouse.com/blog/clickhouse-raises-350-million-series-c-to-power-analytics-for-ai-era).


For those interested in learning more details about what was announced or would like to watch videos of the live sessions, take a look at our [Open House event page](https://clickhouse.com/openhouse).


In this blog post, we'll give a highlight rundown of the product announcements shared on stage at Open House.


![IMG_6370.jpg](/uploads/IMG_6370_28527e27d5.jpg)
## ClickHouse for Real\-Time Analytics [\#](/blog/highlights-from-open-house-our-first-user-conference#clickhouse-for-real-time-analytics)


### Postgres CDC connector for ClickPipes [\#](/blog/highlights-from-open-house-our-first-user-conference#postgres-cdc-connector-for-clickpipes)


Over the past several years, a common pattern has emerged among companies in every industry — from GitLab to Cloudflare to Instacart: they use Postgres and ClickHouse together to tackle their data challenges.


In this architecture, Postgres serves as the system of record for transactional workloads, while ClickHouse handles both real\-time and historical analytics.


![unnamed (12).png](/uploads/unnamed_12_d06dac44f0.png)
This pattern is only accelerating in the AI era. Companies like LangChain, LangFuse, and Vapi are adopting the same Postgres \+ ClickHouse architecture.



> We believe Postgres \+ ClickHouse is becoming the default data stack for modern businesses.


And, we're committed to making that integration seamless. Our Postgres CDC connector is the first major step. **At Open House, we’re excited to have announced that the Postgres CDC connector in ClickPipes is now Generally Available in ClickHouse Cloud**. With just a few clicks, you can replicate your Postgres databases and unlock blazing\-fast, real\-time analytics in ClickHouse Cloud.


Already replicating 100TB\+ of data per month and supporting hundreds of customers \- including Ashby, Seemplicity, and AutoNation \- this connector delivers 10x faster syncs, latency as low as a few seconds, automatic schema changes, fully secure connectivity, and more.


Read the full blog post about this [Postgres CDC GA announcement](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-ga) and try it out yourself with our [quick\-start guide](https://clickhouse.com/docs/integrations/clickpipes/postgres).


### Lightweight Updates [\#](/blog/highlights-from-open-house-our-first-user-conference#lightweight-updates)


Even for OLAP workloads, data mutability is increasingly a key requirement. ClickHouse already supports updates and deletes, but the “traditional” mutations\-based method requires ClickHouse to rewrite entire data parts, even for small changes, and is therefore both resource\-intensive and introduces unpredictable latency.


To address these issues, we’re excited to introduce a new “lightweight” approach for updates and deletes \- the feature is aptly called Lightweight Updates. This method represents updates as "patches" that contain only the changed rows and columns, along with system columns for location, avoiding the need to rewrite entire data parts. These patches are applied during SELECT queries and eventually merge into normal data parts in the background, making updates much faster and reducing the latency variability.


Our benchmarking indicates that these new Lightweight Updates improve performance by several orders of magnitude, depending on data volume, distribution between parts, and other factors, while only nominally affecting SELECT query performance.


Lightweight Updates will be available in ClickHouse Cloud in mid\-July and in open source version 25\.7\+, allowing for frequent updates and deletes with minimal performance impact.


Interested in learning more about these and other updates? Sign up for our [newsletter](https://discover.clickhouse.com/newsletter.html) and release webinars here.


## ClickStack: ClickHouse for Observability [\#](/blog/highlights-from-open-house-our-first-user-conference#clickstack-clickhouse-for-observability)


At Open House, we announced ClickStack, a new open\-source observability stack built on ClickHouse. ClickStack delivers a complete, out\-of\-the\-box experience for logs, metrics, and traces \- powered by the performance and efficiency of ClickHouse, but designed as a full observability stack that’s open, accessible, and ready for everyone.


![clickstack_simple.png](/uploads/clickstack_simple_6ae8ee85d0.png)
ClickStack brings together everything we’ve learned from years of powering observability at scale with ClickHouse, packaging it into a solution that anyone can use. From native support for wide events and JSON, to tight integration with OpenTelemetry and the HyperDX UI, ClickStack eliminates the operational overhead and fragmentation that once made observability a patchwork of compromises needing different stores for each of the pillars of logs, traces, and metrics. It’s fast, scalable, and cost\-efficient \- engineered from the ground up for high\-cardinality, high\-volume workloads.


More than just a stack, ClickStack is a statement: that world\-class observability tooling shouldn’t be reserved for teams with the deepest pockets or large platform engineering teams. With its modular design, opinionated defaults, and full support for custom schemas, Lucene\-like querying (as well as native SQL), ClickStack empowers teams of all sizes to debug faster, store more for less, and own their telemetry without lock\-in. ClickHouse powered observability, finally, for everyone.


Interested in learning more? Read our [announcement blog post](https://clickhouse.com/blog/clickstack-a-high-performance-oss-observability-stack-on-clickhouse) or try it out with our [getting started guide](https://clickhouse.com/docs/use-cases/observability/clickstack/getting-started).


## ClickHouse for Data Warehousing [\#](/blog/highlights-from-open-house-our-first-user-conference#clickhouse-for-data-warehousing)


### ClickHouse, Data Lake, and Lakehouse architectures [\#](/blog/highlights-from-open-house-our-first-user-conference#clickhouse-data-lake-and-lakehouse-architectures)


A series of major updates shared at Open House were around how ClickHouse integrates with Data Lakes and Lakehouse architectures. Announcements included user experience enhancements, performance improvements, expanded compatibility with Iceberg and Delta Lake, and a host of powerful new features on the roadmap.


#### User experience [\#](/blog/highlights-from-open-house-our-first-user-conference#user-experience)


ClickHouse is becoming easier to use with these architectures, with our integration with data catalogs like Unity, AWS Glue, Polaris, and the Hive Metastore. These enable users to query Iceberg, Delta Lake, and Uniform tables directly from ClickHouse.


Additionally, with support for features like time travel and system functions such as iceberg\_history, users can natively leverage the full capabilities of their Iceberg tables directly within ClickHouse.


#### Performance improvements [\#](/blog/highlights-from-open-house-our-first-user-conference#performance-improvements)


ClickHouse performance continues to improve across three key vectors:


- **Partitioning and pruning** support for both Iceberg and Delta Lake tables.
- **Improved caching**, offering better cache locality and extended caching of metadata.
- **Statistic\-based pruning** to avoid unnecessary file reads and reduce query latency.


#### Compatibility with Iceberg and Delta Lake [\#](/blog/highlights-from-open-house-our-first-user-conference#compatibility-with-iceberg-and-delta-lake)


ClickHouse now supports most features of Iceberg v2 and integrates with the Delta Kernel to improve Delta Lake compatibility. These enhancements ensure more consistent and robust behavior when working with modern open table formats.


#### What’s coming next for Data Lake and Lakehouse integrations [\#](/blog/highlights-from-open-house-our-first-user-conference#whats-coming-next-for-data-lake-and-lakehouse-integrations)


ClickHouse is actively working on two major features to bolster support for Data Lake and Lakehouse environments. These include:


##### Distributed Cache [\#](/blog/highlights-from-open-house-our-first-user-conference#distributed-cache)


This new caching mechanism provides a unified caching layer across all compute nodes. It improves:


- Cache hit rate
- Scalability (both horizontal and vertical)
- Consistency across nodes by allowing new nodes to access a shared, pre\-populated cache


You can now [sign up for the private preview waitlist](https://clickhouse.com/cloud/distributed-cache-waitlist) in ClickHouse Cloud to try it out. For a deeper dive, check out the blog post: [Building a Distributed Cache for S3](https://clickhouse.com/blog/building-a-distributed-cache-for-s3)


#### Stateless Workers [\#](/blog/highlights-from-open-house-our-first-user-conference#stateless-workers)


One of the key benefits of Iceberg and Delta Lake is their stateless architecture. To complement this, we’ve introduced functionality that enables offloading query execution to temporary compute nodes, using a new **stateless workers** design. This design uses **data shuffling** to efficiently distribute workloads across a pool of ephemeral nodes.


*Before data shuffling:*


![unnamed (13).png](/uploads/unnamed_13_9b28eeb3c5.png)
*After data shuffling:*


![unnamed (14).png](/uploads/unnamed_14_626186cd1e.png)
While still in the prototype stage, data shuffling is expected to be available for user testing later this year.


These features and improvements are just the tip of the iceberg. There’s more to make ClickHouse even more interoperable, efficient, and robust for your Data Lake and Lakehouse workloads.


Interested in learning more? [Join the waitlist](https://clickhouse.com/cloud/data-lakehouse-waitlist) for ClickHouse lakehouse capabilities.


### SQL Join performance and correlated subqueries [\#](/blog/highlights-from-open-house-our-first-user-conference#sql-join-performance-and-correlated-subqueries)


At Open House, we also announced major performance improvements for joins that dramatically boost speed for real\-world analytical workloads.


These enhancements are available now in ClickHouse 25\.5, with even more optimizations coming in future releases.


Over the past six months, we’ve reengineered key parts of ClickHouse’s join implementation, resulting in 20x faster performance on the TPC\-H benchmark (\*). Improvements include:


- Fully parallelized hash joins, allowing both build and probe phases to run across multiple CPU cores.
- Automatic switching of the build and probe sides, optimizing hash joins based on table size for better cache efficiency.
- Smarter query planning with more aggressive filter pushdown, reduced locking, and even join elimination when possible.


And this is just the beginning. An implementation of global join reorderingis on the way, showing up to 45x speedups in internal tests.


A detailed technical blog post is coming soon. In the meantime, if you’d like to explore the benchmarks yourself, check out our [TPC\-H documentation](https://clickhouse.com/docs/getting-started/example-datasets/tpch) to get started.


(\*) TPC\-H was benchmarked using scale factor 100 on a server with 32 cores and 64 GB main memory.


## ClickHouse for AI/ML [\#](/blog/highlights-from-open-house-our-first-user-conference#clickhouse-for-aiml)


ClickHouse powers the full AI/ML lifecycle, from data exploration to serving models in production. During the exploration and preparation phase, tools like [clickhouse\-local](https://clickhouse.com/docs/operations/utilities/clickhouse-local), [chDB](https://clickhouse.com/chdb) (an in\-process embedded version of ClickHouse), or the ClickHouse server itself allow developers and data scientists to work with ever\-growing amounts of data interactively and efficiently. Whether running ad\-hoc queries, cleaning datasets, or performing feature engineering, ClickHouse offers a fast and flexible environment for iterative data work.


![unnamed (15).png](/uploads/unnamed_15_6a95d4af9e.png)
As models move into training and inference, ClickHouse can serve as both a feature store and a vector store, supporting real\-time retrieval of structured and unstructured data. For example, we recently announced the beta availability of our new vector similarity index, offering an HNSW index with the support of BFloat16 (default) and int8 quantization.


![unnamed (16).png](/uploads/unnamed_16_a557c8a8c1.png)
Finally, with user\-defined functions (UDFs), users can extend ClickHouse with custom logic, enabling more advanced transformations and model\-specific operations. This allows for the integration of ClickHouse directly into ML pipelines, not just as a backend for analytics, but as a component of the AI/ML stack.


### Agent\-Facing Analytics [\#](/blog/highlights-from-open-house-our-first-user-conference#agent-facing-analytics)


In February, we introduced [agent\-facing analytics](https://clickhouse.com/blog/agent-facing-analytics): a new class of analytics workloads that support AI agents and not only regular users. As agentic workloads from copilots, chatbots, and semi\-autonomous systems become more central to workflows, they need timely and structured access to analytical data to function effectively. Two recent features, “Ask AI” in ClickHouse Cloud and the introduction of a remote Model Context Protocol (MCP) server in ClickHouse Cloud, represent steps in that direction.


#### Ask AI in ClickHouse Cloud [\#](/blog/highlights-from-open-house-our-first-user-conference#ask-ai-in-clickhouse-cloud)


The “Ask AI” feature is a turn\-key experience that allows users to trigger complex analysis tasks on top of the data hosted in their ClickHouse Cloud service. Instead of writing SQL or navigating dashboards, users can describe what they are looking for in natural language. The assistant responds with generated queries, visualizations, or summaries, and can incorporate context like active tabs, saved queries, schema details, and dashboards to improve accuracy. It’s designed to work as an embedded assistant, helping users move more quickly from questions to insights, and to from prompts to working dashboards or APIs.


![ask_ai (1).gif](/uploads/ask_ai_1_30e3816c96.gif)
#### Remote MCP Server Integration [\#](/blog/highlights-from-open-house-our-first-user-conference#remote-mcp-server-integration)


Not all users interact with ClickHouse through the Cloud console, however. For example, many developers work directly from their IDEs or connect to the database via custom setups, while others rely on general\-purpose AI assistants such as Claude for most of their explorations. These users, and the agentic workloads acting on their behalf, need a way to securely access and query ClickHouse Cloud without complex setups or custom infrastructure.


The new remote MCP server capability in ClickHouse Cloud addresses this by exposing a standard interface that external agents can use to retrieve analytical context. MCP, or Model Context Protocol, is a standard for structured data access by AI applications powered by LLMs. With this integration, external agents can list databases and tables, inspect schemas, and run scoped, read\-only SELECT queries. Authentication is handled via OAuth, and the server is fully managed on ClickHouse Cloud, so no setup or maintenance is required.


This makes it easier for agentic tools to plug into ClickHouse and retrieve the data they need, whether for analysis, summarization, code generation, or exploration.


![mcp_cursor.gif](/uploads/mcp_cursor_f91238167a.gif)
Note that these features will be rolled out in private preview and continue to evolve with feedback from early adopters. You can join the waitlist at [clickhouse.ai](https://clickhouse.ai) to learn more and request access.


## Conclusion [\#](/blog/highlights-from-open-house-our-first-user-conference#conclusion)


Open House marked a major milestone for ClickHouse, and we’re thankful to all the speakers – including inspiring customer stories from engineers at Weights \& Biases, Open AI, Exabeam, Sierra, Tesla, Anthropic, and Lyft – and attendees who made it such a success.


For those who missed the event or want to revisit the sessions, we'll be publishing recordings of all talks and demos on our [YouTube channel](https://www.youtube.com/c/clickhousedb) in the coming weeks—you can also find detailed information about all announcements at our Open House [event page](https://clickhouse.com/openhouse). For live coverage of the event, see our [thread on X](https://x.com/ClickHouseDB/status/1928124914311053680).


Ready to experience these advancements firsthand? ClickHouse Cloud is the best way to get started. [Sign up today](https://auth.clickhouse.cloud/u/signup/identifier?state=hKFo2SA4REFUUGhYTTFYVEt2MW5LaXV1bmdiajZ5WVkwTXJIVaFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIGFYaHI5bGJUb2NRWVU5eGRfR2xBNXBKbFpIMk5McFVvo2NpZNkgSVBwSDRSTkQwcU5YSFZheWVwZmZnc0dwYlhRbUZpa3I) and receive $300 in free trial credits.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
