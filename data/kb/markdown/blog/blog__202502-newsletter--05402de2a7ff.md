# February 2025 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# February 2025 Newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Feb 19, 2025 · 8 minutes readWell, January went by quickly, didn’t it?! That means it must be time for our second newsletter of 2025\.


This month's big news is the launch of JSONBench, a benchmark suite for JSON analytics. Ryadh Dahimene tells us about agent\-facing analytics, Shahar Gvirtz explains why he likes ClickHouse, Tom Schreiber dives into the join improvements in 25\.1, and more.


## Featured community member: Chris Lawrence [\#](/blog/202502-newsletter#featured-community-member-chris-lawrence)


This month's featured community member is Chris Lawrence, Dev Lead and Senior Software Engineer at [AMP](https://www.linkedin.com/company/use-amp/).


![1_newsletter202502.png](/uploads/1_newsletter202502_4f144a0657.png)
Chris previously co\-founded ReSync Digital, successfully launching over 30 products for early\-stage startups, and has experience in machine vision and IoT solutions through his work with Skip\-Line, LLC.


Chris Lawrence [spoke at the ClickHouse meetup in Melbourne in August 2024](https://clickhouse.com/videos/amp-from-batch-processing-to-streaming). He shared how AMP’s implementation of ClickHouse Cloud has helped them transform their data pipeline from batch processing to real\-time streaming, improving their analytics platform's speed and reliability. Chris also elaborated on his talk in [a recent blog post](https://clickhouse.com/blog/amp-clickhouse-oss-to-clickhouse-cloud).


➡️ [Follow Chris on LinkedIn](https://www.linkedin.com/in/chrislawrence121/)


## Upcoming events [\#](/blog/202502-newsletter#upcoming-events)


### Global events [\#](/blog/202502-newsletter#global-events)


- [v25\.2 Community Call](https://clickhouse.com/company/events/v25-2-community-release-call) \- Feb 27


### Free training [\#](/blog/202502-newsletter#free-training)


- [ClickHouse Fundamentals](https://clickhouse.com/company/events/clickhouse-fundamentals) \- Feb 26 and Mar 19
- [Formation ClickHouse en présentiel](https://clickhouse.com/company/events/202503-emea-paris-inperson-clickhousetraining), Paris \- Mar 4
- [In\-Person ClickHouse Developer Fast Track \- Seattle](https://clickhouse.com/company/events/202503-amer-seattle-inperson-developer-fast-track) \- Mar 5
- [ClickHouse Query Optimization Workshop](https://clickhouse.com/company/events/202503-emea-query-optimization) \- Mar 12
- [ClickHouse Admin Workshop](https://clickhouse.com/company/events/202503-amer-clickhouse-admin-workshop) \- Mar 12
- [In\-Person ClickHouse Developer \- Sydney](https://clickhouse.com/company/events/202503-apj-sydney-inperson-clickhouse-developer) \- Mar 24\-25
- [In\-Person ClickHouse Developer \- Melbourne](https://clickhouse.com/company/events/202503-apj-melbourne-inperson-clickhouse-developer) \- Mar 27\-28
- [In\-Person ClickHouse Developer Fast Track \- Bangalore](https://clickhouse.com/company/events/202504-apj-bangalore-inperson-developer-fast-track) \- Apr 1


### Events in AMER [\#](/blog/202502-newsletter#events-in-amer)


- [Clickhouse Meetup with LA DevOps](https://www.meetup.com/clickhouse-los-angeles-user-group/events/305952193/?slug=clickhouse-los-angeles-user-group&isFirstPublish=true) \- Feb 20
- [ClickHouse Meetup in Seattle](https://www.meetup.com/clickhouse-seattle-user-group/events/305916325/?eventOrigin=your_events) \- Mar 5
- [Scale 22x](https://clickhouse.com/company/events/2025-03-scale-22), Pasadena \- Mar 6 \- Mar 9
- [Game Developers Conference](https://clickhouse.com/company/events/03-2025-san-francisco), San Francisco \- Mar 17
- [ClickHouse Meetup @ Cloudflare](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/306046697/?eventOrigin=group_events_list), San Francisco \- Mar 19
- [ClickHouse Meetup @ Klaviyo](https://www.meetup.com/clickhouse-boston-user-group/events/305882607/?slug=clickhouse-boston-user-group&eventId=300907870&isFirstPublish=true), Boston \- Mar 25
- [ClickHouse Meetup @ Braze](https://www.meetup.com/clickhouse-new-york-user-group/events/305916369/?eventOrigin=group_upcoming_events), New York \- Mar 26
- [Google Next](https://clickhouse.com/company/events/2025-04-google-next), Las Vegas \- Apr 9
- [Open House User Conference](https://clickhouse.com/openhouse), San Francisco \- May 28


### Events in EMEA [\#](/blog/202502-newsletter#events-in-emea)


- [ClickHouse Meetup @ Nexton](https://www.meetup.com/clickhouse-france-user-group/events/305792997/), Paris \- Mar 4
- [KubeCon 2025](https://clickhouse.com/company/events/04-2025-kubecon-london), London \- April 1\-4
- [AWS Summit 2025](https://clickhouse.com/company/events/04-2025-aws-paris), Paris \- April 9
- [AWS Summit 2025](https://clickhouse.com/company/events/2025-04-aws-summit-amsterdam), Amsterdam \- April 16
- [AWS Summit, 2025](https://clickhouse.com/company/events/04-2025-aws-london), London \- April 30


### Events in APAC [\#](/blog/202502-newsletter#events-in-apac)


- [ClickHouse Singapore Meetup](https://www.meetup.com/clickhouse-singapore-meetup-group/events/305917892/) \- Feb 25
- [ClickHouse Shanghai Meetup](https://www.huodongxing.com/event/3794544969111?td=3894807410019), China\- Mar 1
- [Data \& AI Summit NSW](https://forefrontevents.co/event/data-ai-summit-nsw-2025/), Australia \- Mar 18
- [Current Bengaluru](https://current.confluent.io/bengaluru), India \- Mar 19
- [ClickHouse Delhi Meetup](https://www.meetup.com/clickhouse-delhi-user-group/events/306253492/), India \- Mar 22
- [Latency Conference](https://latencyconf.io/), Australia \- Apr 3\-4
- [TEAMZ Web3/AI Summit](https://web3.teamz.co.jp/en), Japan \- Apr 16\-17


## Introducing JSONBench: The billion docs JSON Challenge vs MongoDB, Elasticsearch, and more [\#](/blog/202502-newsletter#introducing-jsonbench-the-billion-docs-json-challenge-vs-mongodb-elasticsearch-and-more)


![2_newsletter202502.png](/uploads/2_newsletter202502_fd28c5c96d.png)
The [November newsletter](https://clickhouse.com/blog/202411-newsletter#how-we-built-a-new-powerful-json-data-type-for-clickhouse) mentioned the new JSON data type and explained its performance benefits. To test these claims, we developed [JSONBench](https://jsonbench.com/), a benchmark suite for JSON analytics.


Tom Schreiber has published a comprehensive blog post comparing how different databases handle JSON data. The analysis covers performance benchmarks and storage approaches across multiple systems, including ClickHouse, MongoDB, and Elasticsearch.


His findings detail how each database performs with analytical queries on JSON data and explore their underlying JSON storage mechanisms.


➡️ [Read the blog post](https://clickhouse.com/blog/json-bench-clickhouse-vs-mongodb-elasticsearch-duckdb-postgresql)


## Shahar Gvirtz: 7 Reasons why I like ClickHouse [\#](/blog/202502-newsletter#shahar-gvirtz-7-reasons-why-i-like-clickhouse)


It’s always fun to come across a blog post by a community member enjoying their time with ClickHouse!


I won’t go through all of Shahar’s reasons for liking ClickHouse, but I did want to highlight one of the things that he likes, which is an underrated feature of ClickHouse \- its ability to compress data. In Shahar’s words:



> Logs stored in ClickHouse take up only 28% of the space they occupy in Elasticsearch.


If you ever need to tell a friend or colleague why you like ClickHouse, you could do worse than point them to this blog post!


➡️ [Read the blog post](https://shahargv.medium.com/7-reasons-why-i-like-clickhouse-9cbb11b142d5)


## Agent\-Facing Analytics [\#](/blog/202502-newsletter#agent-facing-analytics)


![3_newsletter202502.png](/uploads/3_newsletter202502_1727daa7b3.png)
Ryadh Dahimene has written a (IMHO) brilliant blog post explaining a new user persona for [real\-time analytics](https://clickhouse.com/engineering-resources/what-is-real-time-analytics) databases \- AI agents!


Ryadh first takes us on a brief tour of AI developments since the launch of ChatGPT in 2022, including the "sense\-think\-act" loop, the introduction of support for tools by LLMs, and the recent evolution of reasoning models like OpenAI o1 and DeepSeek\-R1\.


He then explores the role of real\-time analytics databases in agentic workflows and introduces the [ClickHouse MCP Server](https://github.com/ClickHouse/mcp-clickhouse/tree/f8cc7e09d71b624691702520a4741e1849b4b4be). This is our implementation of the server side of Anthropic’s Model Context Protocol, which means you can easily converse with a ClickHouse database from the Claude Desktop.


➡️ [Read the blog post](https://clickhouse.com/blog/agent-facing-analytics)


## ClickHouse and Cribl: A Powerful Data Ingestion and Analysis Duo [\#](/blog/202502-newsletter#clickhouse-and-cribl-a-powerful-data-ingestion-and-analysis-duo)


![4_newsletter202502.png](/uploads/4_newsletter202502_08ff7adaee.png)
Cribl Stream is a data processing platform that works with various data sources, including [telemetry data](https://clickhouse.com/engineering-resources/telemetry-data), like logs, metrics, and trace data. It can preprocess, filter, and transform events before forwarding them to destinations, helping optimize storage utilization and query efficiency. Support for ClickHouse was recently added to its list of supported outputs.


David Maislin has written a detailed guide showing how to set up and use this integration. The guide includes step\-by\-step instructions for creating ClickHouse tables, configuring Cribl Stream destinations, and using Cribl Search to query the data. It also demonstrates how to use ClickHouse alongside Cribl's data processing features, complete with examples using Cribl's Datagen feature to generate test data.


➡️ [Read the blog post](https://cribl.io/blog/clickhouse-and-cribl-a-powerful-data-ingestion-and-analysis-duo/)


## ClickHouse Cloud evolution: compute\-compute separation, improved autoscaling, and more! [\#](/blog/202502-newsletter#clickhouse-cloud-evolution-compute-compute-separation-improved-autoscaling-and-more)


![5_newsletter202502.png](/uploads/5_newsletter202502_24dd703b23.png)
ClickHouse Cloud was built in record time and brought to market in December 2022\. Since then, over a thousand companies have onboarded their workloads into our managed service, and every day, they now collectively run 5\.5 billion queries, scanning 3\.5 quadrillion records on top of 100PB of data!


Over the past two years, we've gained valuable insights from working closely with our users and have significantly evolved our cloud architecture. This blog describes the latest improvements, including [compute\-compute separation](https://clickhouse.com/blog/introducing-warehouses-compute-compute-separation-in-clickhouse-cloud), high\-performance machine types ([moving to Graviton in AWS](https://clickhouse.com/blog/graviton-boosts-clickhouse-cloud-performance)), single\-replica services, and more reactive and seamless automatic scaling.


➡️ [Read the blog post](https://clickhouse.com/blog/evolution-of-clickhouse-cloud-new-features-superior-performance-tailored-offerings)


## 25\.1 release [\#](/blog/202502-newsletter#251-release)


In the 25\.1 release blog post, Tom Schreiber did a deep dive into the improvements made to the parallel hash join algorithm probe phase. If you’re interested in database internals, that’s worth a read.


This release also introduced MinMax indices at the table level, improved the Merge table engine and table function, added auto\-increment functionality, and some nice CLI usability improvements.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-01)


## Interesting projects [\#](/blog/202502-newsletter#interesting-projects)


While compiling the newsletter each month, I come across many ClickHouse\-based projects, so I thought I’d share some of them this month.


- [apitally.io](https://apitally.io/) \- An API monitoring and analytics tool for Python / Node.js apps. It helps users understand API usage and performance, spot issues early, and troubleshoot effectively when something goes wrong. The founder mentioned that it uses ClickHouse to store data on a [Hacker News thread](https://news.ycombinator.com/item?id=42915435).
- [Openpanel](https://github.com/Openpanel-dev/openpanel) \- An open\-source alternative to Mixpanel for capturing user behavior across web, mobile apps, and backend services. It uses ClickHouse to store events.
- [Vigilant](https://www.vigilant.run/home) \- A lightweight tool for managing structured logs. It lets you centralize your logs, search them, and create alerts. It [uses ClickHouse under the hood](https://news.ycombinator.com/item?id=42814930).
- [CH\-UI](https://github.com/caioricciuti/ch-ui) \- A user interface for interacting with the ClickHouse Server. It has syntax highlighting for queries and lets you see visual metrics about your instance.


## Video Corner [\#](/blog/202502-newsletter#video-corner)


- As Benjamin Wootton [demonstrates in this hands\-on video](https://clickhouse.com/videos/replicating-data-postgres-clickhouse-cloud), splitting workloads between PostgreSQL for transactions and ClickHouse for analytics is becoming increasingly popular. He walks us through two ways to keep these databases in sync—using the open\-source [PeerDB](https://github.com/PeerDB-io/peerdb) tool or [ClickHouse Cloud's built\-in solution](https://clickhouse.com/docs/en/integrations/clickpipes/postgres).
- I created a video showing [how to use the recently released ClickHouse MCP server](https://clickhouse.com/videos/clickhouse-mcp-server).
- I also created a video showing [how to use the built\-in monitoring dashboard](https://clickhouse.com/videos/clickhouse-monitoring-dashboard) to debug some common problems.
- Leon Kozlowski from Flock Safety explains how they [transformed their traffic analytics system from a slow, daily\-batch Redshift setup to a real\-time solution using ClickHouse](https://clickhouse.com/videos/real-time-traffic-analytics-flock-safety). The system handles over a billion ML predictions per day from its network of surveillance cameras.
- Derek Chia and Karthikayan Muthuramalingam [present a technical overview of integrating ClickHouse with Kafka](https://clickhouse.com/videos/maximising-analytics-clickhouse-kafka), showing how these technologies can work together effectively for real\-time data processing and analytics. Derek explains ClickHouse's capabilities as an open\-source columnar database optimized for analytics, while Karthikayan details Kafka's role as a distributed event streaming platform.


## Post of the month [\#](/blog/202502-newsletter#post-of-the-month)


My favorite post this month was by [Jacob Wolf](https://x.com/JacobWolf), who’s ingesting lots of data into ClickHouse.


![6_newsletter202502.png](/uploads/6_newsletter202502_1b466bad33.png)
➡️ [Read the post](https://x.com/JacobWolf/status/1884316267093582231)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
