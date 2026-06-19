# June 2025 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# June 2025 Newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Jun 18, 2025 · 8 minutes readHello, and welcome to the June 2025 ClickHouse newsletter!


This month, we’ve announced ClickStack, our new open\-source observability solution. We also learn about the mark cache, how the CloudQuery team built a full\-text search engine with ClickHouse, building agentic applications with the MCP Server, analyzing FIX data, and more!


## Featured community member: Joe Karlsson [\#](/blog/202506-newsletter#featured-community-member)


This month's featured community member is Joe Karlsson, Senior Developer Advocate at CloudQuery.


![1_june.png](/uploads/1_june_fea80c139d.png)
Joe is a seasoned developer advocate with over 5 years of experience building developer communities around cutting\-edge data technologies, progressing through roles at MongoDB, SingleStore, Tinybird, and currently CloudQuery, where he specializes in creating technical content, proof\-of\-concepts, and educational resources that help developers effectively leverage modern data infrastructure tools.


Joe is a [prolific writer in the data engineering space](https://www.cloudquery.io/authors/joe-karlsson), covering everything from Kubernetes asset tracing to querying cloud infrastructure for expired dependencies.. He's also shared his hands\-on ClickHouse experience in [How We Handle Billion\-Row ClickHouse Inserts With UUID Range Bucketing](https://www.cloudquery.io/blog/how-we-handle-billion-row-clickhouse-inserts-with-uuid-range-bucketing) and [Six Months with ClickHouse at CloudQuery (The Good, The Bad, and the Unexpected)](https://www.cloudquery.io/blog/six-months-with-clickhouse-at-cloudquery).


➡️ [Follow Joe on LinkedIn](https://www.linkedin.com/in/joekarlsson/)


## Upcoming events [\#](/blog/202506-newsletter#upcoming-events)


### Global events [\#](/blog/202506-newsletter#global-events)


- [v25\.6 Community Call](https://clickhouse.com/company/events/v25-4-community-release-call) \- June 26


### Free training [\#](/blog/202506-newsletter#free-training)


- [ClickHouse Admin Workshop (Virtual)](https://clickhouse.com/company/events/202506-amer-clickhouse-admin-workshop) \- June 25
- [In\-Person ClickHouse Query Optimization Training \- Bangalore](https://clickhouse.com/company/events/202506-apj-bangalore-inperson-query-optimization) \- June 26
- [ClickHouse Deep Dive Training (Virtual)](https://clickhouse.com/company/events/202507-emea-clickhouse-deeep-dive) \- July 2
- [BigQuery to ClickHouse Workshop (Virtual)](https://clickhouse.com/company/events/202507-apj-clickhouse-bigquery-workshop) \- July 9
- [ClickHouse Deep Dive Training \- NYC](https://clickhouse.com/company/events/202507-in-person-clickhouse-deep-dive) \- July 15
- [ClickHouse Query Optimization Workshop (Virtual)](https://clickhouse.com/company/events/202507-emea-query-optimization) \- July 16
- [ClickHouse Fundamentals (Virtual)](https://clickhouse.com/company/events/202507-amer-clickhouse-fundamentals) \- July 30


### Events in AMER [\#](/blog/202506-newsletter#events-in-amer)


- [ClickHouse @ RheinHaus Denver](https://www.meetup.com/clickhouse-denver-user-group/events/308483614) \- June 26th
- [ClickHouse \+ Docker AI Night Chicago](https://www.meetup.com/clickhouse-chicago-meetup-group/events/308463448https://www.meetup.com/clickhouse-chicago-meetup-group/events/308463448) \- July 1st
- [ClickHouse Meetup in Atlanta](https://clickhouse.com/company/events/202503-amer-atl-meetup) \- July 8
- [ClickHouse Social in Philly](https://clickhouse.com/company/events/202507-amer-PH-meetup) \- July 11
- [ClickHouse Meetup in New York](https://clickhouse.com/company/events/202503-amer-NY-meetup) \- July 15
- [AWS Summit New York](https://clickhouse.com/company/events/2025-07-Amer-AWSSummit-NewYork) \- July 16
- [AWS Summit Toronto](https://clickhouse.com/company/events/2025-09-Amer-AWSSummit-Toronto) \- September 4
- [AWS Summit Los Angeles](https://clickhouse.com/company/events/2025-09-Amer-AWSSummit-LosAngeles) \- September 17


### Events in EMEA [\#](/blog/202506-newsletter#events-in-emea)


- [ClickHouse Meetup in Amsterdam](https://clickhouse.com/company/events/202506-EMEA-Amsterdam-meetup) \- June 25
- [Tech BBQ Copenhagen](https://techbbq.dk/) \- August 27\-28
- [AWS Summit Zurich](https://aws.amazon.com/events/summits/zurich/) \- September 11
- [BigData London](https://www.bigdataldn.com/) \- September 24\-25
- [PyData Amsterdam](https://amsterdam.pydata.org/) \- September 24\-25


### Events in APAC [\#](/blog/202506-newsletter#events-in-apac)


- [AWS Summit Japan](https://clickhouse.com/company/events/2025-06-APJ-AWSSummit-Tokyo) \- June 25\-26
- [ClickHouse \+ Netskope \+ Confluent Bangalore Meetup](https://clickhouse.com/company/events/202506-apj-bangalore-meetup) \- June 27
- [ClickHouse Meetup in Perth](https://clickhouse.com/company/events/202507-apj-perth-meetup) \- July 2
- [DB Tech Showcase 2025 Tokyo](https://clickhouse.com/company/events/202507-APJ-Tokyo-DB-Tech-Showcase) \- July 10\-11
- [DataEngBytes Melbourne](https://clickhouse.com/company/events/202507-APJ-Melbourne-DataEngBytes)
- [DataEngBytes Sydney](https://clickhouse.com/company/events/202507-APJ-Sydney-DataEngBytes)


## 25\.5 release [\#](/blog/202506-newsletter#release)


![2_june.png](/uploads/2_june_e7ccb54577.png)
ClickHouse 25\.5 is here, and the vector similarity index has moved from experimental to beta.


We’ve also added Hive metastore catalog support, made clickhouse\-local a bit easier to use (you can skip FROM and SELECT with stdin now), and made the Parquet reader handle Geo types.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-05)


## ClickStack: A high\-performance OSS observability stack on ClickHouse [\#](/blog/202506-newsletter#clickstack)


![3_june.png](/uploads/3_june_0b1dc30c38.png)
At the recent OpenHouse conference, Mike Shi announced ClickStack, our new open\-source observability solution that delivers a complete, out\-of\-the\-box experience for logs, metrics, traces, and session replay powered by ClickHouse's high\-performance database technology.


This product announcement represents our increased investment in the observability ecosystem. It combines the ClickHouse columnar storage engine with a purpose\-built UI from HyperDX \- a company we recently acquired \- to create an accessible, unified observability platform.


The stack is completed with native OpenTelemetry integration, providing standardized data collection that simplifies the instrumentation and ingestion of telemetry data from all your applications and services.


➡️ [Read the blog post](https://clickhouse.com/blog/clickstack-a-high-performance-oss-observability-stack-on-clickhouse)


## Why (and how) CloudQuery built a full\-text search engine with ClickHouse [\#](/blog/202506-newsletter#cloudquery-fts)


![4_june.png](/uploads/4_june_16f5ba31cb.png)
Our featured community member, Joe Karlsson, and his colleague James Riley have published an insightful blog post detailing their innovative approach to implementing full\-text search capabilities.


Rather than adding external search infrastructure like Elasticsearch or MeiliSearch, they built their search index directly within ClickHouse using `ngrambf_v1` Bloom filter indices.


They also explain how they tuned performance, using multi\-size ngram Bloom filters, weighted scoring, and thoughtful partitioning to support sub\-400 ms search across more than 150 million rows. The post concludes with lessons learned, trade\-offs around write performance, and a peek at upcoming features like LLM\-based search and incremental indexing.


➡️ [Read the blog post](https://www.cloudquery.io/blog/why-and-how-we-built-our-own-full-text-search-engine-with-clickhouse)


## Mark Cache: The ClickHouse speed hack you’re not using (yet) [\#](/blog/202506-newsletter#mark-cache)


![5_june.png](/uploads/5_june_05a4ae52ad.png)
In his blog post on The New Stack, Anil Inamdar highlights the mark cache in ClickHouse.


This memory\-resident mechanism stores metadata pointers that allow ClickHouse to quickly locate data without scanning or decompressing entire files, reducing query times and disk I/O for analytical workloads.


Anil explains how we can configure the size of this cache and then monitor performance using built\-in metrics.


➡️ [Read the blog post](https://thenewstack.io/mark-cache-the-clickhouse-speed-hack-youre-not-using-yet/?taid=68474b88a2031300010b4f1a)


## Building an agentic application with ClickHouse MCP Server [\#](/blog/202506-newsletter#agentic-app-clickhouse-mcp)


![10_june.png](/uploads/10_june_3081f67e0c.png)
Lionel Palacin explores how agentic applications powered by LLMs can transform data interaction. Instead of clicking through filters and dropdowns, users can simply ask "Show me the price evolution in Manchester for the last 10 years" and get instant charts with explanations.


Lio takes us through the technical implementation using ClickHouse MCP Server and CopilotKit with React/Next.js, showing developers how to build their own conversational analytics experiences.


➡️ [Read the blog post](https://clickhouse.com/blog/building-an-agentic-application-with-clickhouse-mcp-server-and-copilotkit)


## Analyzing FIX Data With ClickHouse [\#](/blog/202506-newsletter#analyzing-fix)


![7_june.png](/uploads/7_june_5a6c35ed64.png)
Benjamin Wootton shows how we can use ClickHouse to analyze high\-volume Financial Information eXchange (FIX) protocol data commonly used in capital markets trading.


Ben shows how to parse raw FIX messages using ClickHouse's built\-in string and array functions, creating materialized views that incrementally process trade requests and confirmations. By joining this data with market prices and applying window functions, he calculates the financial impact of trade rejections on different banks' profit and loss positions.


➡️ [Read the blog post](https://benjaminwootton.com/insights/analysing-fix-data-with-clickhouse/)


## Building a scalable user segmentation pipeline with ClickHouse and Airflow \- Part 1: Model Training [\#](/blog/202506-newsletter#segmentation-pipeline)


![8_june.png](/uploads/8_june_81f6938436.png)
A/B Tasty is building a scalable, automated user segmentation pipeline using ClickHouse and Apache Airflow. In the first article of a two\-part blog series, Jhon Steven Neira covers the model training phase that periodically learns the clusters (centroids) from user behavior data.


ClickHouse handles aggregating user behavior features and performing K\-Means clustering in SQL. Airflow ensures the training runs on schedule and that daily inference runs reliably each day using the latest available model.


Steven provides a detailed walkthrough of implementing K\-Means clustering in ClickHouse, demonstrating how to use aggregation states and materialized views to build an efficient segmentation system.


➡️ [Read the blog post](https://medium.com/the-ab-tasty-tech-blog/building-a-scalable-user-segmentation-pipeline-with-clickhouse-and-airflow-part-1-model-training-75ab9fb59745)


## ClickHouse in the wild: An odyssey through our data\-driven marketing campaign in Q\-Commerce [\#](/blog/202506-newsletter#data-driven-marketing)


![9_june.png](/uploads/9_june_4ff47eee43.png)
Parham Abbasi shares how Snapp! Market used ClickHouse to drive a personalized marketing campaign at scale. Millions of users were profiled using [MBTI\-style](https://en.wikipedia.org/wiki/Myers%E2%80%93Briggs_Type_Indicator#:~:text=In%20MBTI%20theory%2C%20the%20four,value%20of%20naturally%20occurring%20differences.) traits derived from real purchase behavior, like impulse levels, health focus, and price sensitivity.


The team used a multi\-tiered data lake ([Bronze\-Silver\-Gold](https://clickhouse.com/blog/building-a-medallion-architecture-with-clickhouse)) and ClickHouse’s ability to query Parquet directly to generate production\-ready profiles. They also use the `partial_merge` join algorithm to keep memory use stable across multi\-year datasets, enabling LLM\-generated personas to be delivered at scale.


➡️ [Read the blog post](https://medium.com/@prmbas/clickhouse-in-the-wild-an-odyssey-through-our-data-driven-marketing-campaign-in-q-commerce-93c2a2404a39)


## Quick reads [\#](/blog/202506-newsletter#quick-reads)


- Alexei shows us [how to write a user\-defined function in Golang to check email validity](https://medium.com/@acosetov/building-udfs-in-clickhouse-with-go-a-step-by-step-guide-813076b167f4).
- Alasdair Brown and Mark Needham wrote a blog post about [creating "Hello World" examples for the ClickHouse MCP Server with different AI agent libraries](https://clickhouse.com/blog/integrating-clickhouse-mcp).
- We wrote [a blog summarizing all the announcements at OpenHouse](https://clickhouse.com/blog/highlights-from-open-house-our-first-user-conference), including the Postgres CDC connector in ClickPipes going GA, Lightweight Updates, performance improvements for joins, and more!
- Soumil Shah shows [how to query Iceberg tables stored in S3 with ClickHouse](https://medium.com/@shahsoumil519/learn-how-to-query-s3-tables-with-clickhouse-e81a35f62c27).
- Kevin Meneses González explains [the advantages and disadvantages of each technique for loading data from Kafka into ClickHouse](https://medium.com/data-science-collective/how-to-ingest-raw-kafka-data-into-clickhouse-without-wrecking-your-pipeline-731e58a76e7d%20).
- Lloyd Armstrong [developed a ClickHouse IAM module for Terraform that abstracts and simplifies the creation of roles and the granting of privileges](https://medium.com/@lloydarmstrong/terraforming-clickhouse-for-real-world-data-warehousing-f51bf2d8bdcc).
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
