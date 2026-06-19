# January 2026 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# January 2026 newsletter

![](/_next/image?url=%2Fuploads%2Fmark_needham_a17c08008e.png&w=96&q=75)[Mark Needham](/authors/mark-needham)Jan 15, 2026 · 7 minutes readHello, and welcome to the January 2026 ClickHouse newsletter!


This month, we learn how chDB achieved true zero\-copy integration with Pandas DataFrames, how WKRP migrated their RuneScape tracking plugin from TimescaleDB to ClickHouse, replacing Apache Flink with ClickHouse's Kafka engine, and more!


## Featured community member: lgbo [\#](/blog/202601-newsletter#featured-community-member)


This month's featured community member is lgbo.


![jan20026_image5.png](/uploads/jan20026_image5_7e4ba288f9.png)
lgbo works at BIGO, where they use ClickHouse in their real\-time data pipeline that processes tens of billions of messages daily.


lgbo has submitted several pull requests to address performance issues, including reducing memory usage for window functions, reducing cache misses during hash table iteration, and optimizing CROSS JOINs.


lgbo also improved short\-circuit execution performance by avoiding unnecessary operations on non\-function columns, added a new stringCompare function for lexicographic comparison of substring portions, and fixed a bug where named tuple element names weren't preserved correctly during type derivation.


➡️ [Follow lgbo on GitHub](https://github.com/lgbo-ustc)


## 25\.12 release [\#](/blog/202601-newsletter#release)


![jan20026_image6.png](/uploads/jan20026_image6_a0edc2e602.png)
ClickHouse 25\.12 delivers significant improvements in query performance across the board. We have faster top\-N queries through data skipping indexes, a reimagined lazy reading execution model that's 75 times faster, and a more powerful DPsize join reordering algorithm.


➡️ [Read the release post](https://clickhouse.com/blog/clickhouse-release-25-12)


## The Journey to Zero\-Copy: How chDB Became the Fastest SQL Engine on Pandas DataFrame [\#](/blog/202601-newsletter#chdb)


![jan20026_image7.png](/uploads/jan20026_image7_1d3f81a67a.png)
chDB v4\.0 achieves true zero\-copy integration with Pandas DataFrames. By eliminating serialization steps and implementing direct memory sharing between ClickHouse and NumPy, queries that previously took 30 seconds now complete in under a second.


➡️ [Read the blog post](https://clickhouse.com/blog/chdb-journey-to-zero-copy)


## A small\-time review of ClickHouse [\#](/blog/202601-newsletter#clickhouse_review)


WKRP migrated their RuneScape tracking plugin from TimescaleDB to ClickHouse with impressive results. Storage usage improved dramatically: location data compressed from 4\.28 GiB to 592 MiB (87% reduction), while XP tracking data went from 872 MiB to 168 MiB (81% reduction). Beyond storage, the migration simplified operations \- upgrades now happen through the package manager without coordinated downtime.


The verdict: "Timescale worked well, but ClickHouse has provided better performance and made running the service easier."


➡️ [Read the blog post](https://www.wkrp.xyz/a-small-time-review-of-clickhouse/)


## Solving the "Impossible" in ClickHouse: Advent of Code 2025 [\#](/blog/202601-newsletter#advent_of_code)


![jan20026_image1.png](/uploads/jan20026_image1_245b4653d7.png)
Yes, we're still talking about Christmas in mid\-January, but Zach Naimon's deep dive into solving Advent of Code 2025 entirely in ClickHouse SQL is worth the delayed celebration.


Following strict rules (pure SQL only, raw inputs, single queries), Zach tackled all 12 algorithmic puzzles that typically require Python, Rust, or C\+\+. The solutions showcase ClickHouse's versatility through recursive CTEs for pathfinding, arrayFold for state machines, and specialized functions like intervalLengthSum for geometric problems.


Proof that with the right tools, "impossible" problems become just another data challenge.


➡️ [Read the blog post](https://clickhouse.com/blog/clickhouse-advent-of-code-2025)


## Seven Companies, One Pattern: Why Every Scaled ClickHouse Deployment Looks the Same [\#](/blog/202601-newsletter#seven_companies)


Luke Reilly explains why Uber, Cloudflare, Instacart, GitLab, Lyft, Microsoft, and Contentsquare all build the same four\-layer abstraction stack over ClickHouse: it changes cost curves.


Platform teams absorb schema optimization knowledge once through semantic layers and query translation engines, enabling sublinear scaling \- headcount grows with data volume instead of user count.


Now AI is becoming the fifth layer, with tools like ClickHouse.ai and MCP servers adding natural language interfaces on top of these semantic definitions.


➡️ [Read the blog post](https://medium.com/@lureilly1/seven-companies-one-pattern-why-every-scaled-clickhouse-deployment-looks-the-same-d2ba68606ad6)


## Your AI SRE needs better observability, not bigger models [\#](/blog/202601-newsletter#ai_sre)


![jan20026_image2.png](/uploads/jan20026_image2_f3bbf2f869.png)
Drawing on his experience increasing Confluent's availability from 99\.9% to 99\.95%, Manveer Chawla explains why AI SRE copilots should prioritize investigation over auto\-remediation. Most AI SRE tools fail because they're built on observability platforms with short retention, dropped high\-cardinality dimensions, and slow queries.


The solution? Rethink the observability architecture. Manveer details a reference architecture using ClickHouse that demonstrates the effectiveness of AI copilots, which require better data foundations, rather than larger models.


➡️ [Read the blog post](https://clickhouse.com/blog/ai-sre-observability-architecture)


## Simplifying real\-time data pipelines: How ClickHouse replaced Flink for our Kafka Streams [\#](/blog/202601-newsletter#kafka_streams)


![jan20026_image4.png](/uploads/jan20026_image4_df92d08407.png)
Ashkan Goleh Pour provides a detailed walkthrough of replacing Apache Flink with ClickHouse's native Kafka integration for real\-time streaming.


The architecture uses ClickHouse's Kafka table engine to consume events directly, Materialized Views for continuous SQL transformations, and MergeTree tables for persistent state, thereby eliminating the need for external stream processors.


➡️ [Read the blog post](https://medium.com/towards-data-engineering/simplifying-real-time-data-pipelines-how-clickhouse-replaced-flink-for-our-kafka-streams-13f6f4e1e097)


## Quick reads [\#](/blog/202601-newsletter#quick-reads)


- Georgii Baturin has written a multi\-part series of posts showing [how to use dbt with ClickHouse](https://medium.com/hands-on-dbt-with-clickhouse/hands-on-dbt-with-clickhouse-7-why-tests-matter-and-why-a-green-build-does-not-prove-anything-by-c15f1cb1264d).
- Shuva Jyoti Kar demonstrates [how to build an autonomous AI agent system](https://medium.com/@shuva.jyoti.kar.87/the-speed-of-thought-real-time-analytics-meets-agentic-ai-1864e1ed6165) by connecting ClickHouse with Google's Gemini CLI using the Model Context Protocol (MCP).
- Gulled Hayder shows [how to set up ClickHouse on a Linux system](https://medium.com/@aagulled/getting-clickhouse-ready-for-web-traffic-analysis-6bec9867e1ee) with Python, install and configure the database with proper authentication, generate 1 million rows of synthetic web traffic data, and load it into a MergeTree table for analytics.
- ByteBoss [builds a real\-time cryptocurrency market data pipeline](https://medium.com/@ByteBosss/building-a-real-time-cryptocurrency-market-data-pipeline-from-scratch-9c81acf3f75b) that connects to exchange WebSockets (Binance/Coinbase), normalizes their different data formats, streams through Kafka/Redpanda, automatically processes with ClickHouse materialized views, and visualizes live trading data in Grafana dashboards.


## Interesting projects [\#](/blog/202601-newsletter#interesting-projects)


- [DoomHouse](https://github.com/arniwesth/DoomHouse) \- An experimental "Doom\-like" game engine that renders the 3D graphics entirely in ClickHouse SQL.
- [genezhang/clickgraph](https://hub.docker.com/r/genezhang/clickgraph) \- Stateless, read\-only graph query engine for ClickHouse using Cypher.
- [clickspectre](https://github.com/ppiankov/clickspectre) \- A spectral ClickHouse analyzer that tracks which tables are actually used and by whom.


## Upcoming events [\#](/blog/202601-newsletter#upcoming-events)


### Virtual training [\#](/blog/202601-newsletter#virtual-training)


- [ClickHouse Admin Workshop](https://clickhouse.com/company/events/202602-amer-clickhouse-admin-workshop) \- 12th February
- [ClickHouse Query Optimization Workshop](https://clickhouse.com/company/events/202602-amer-emea-query-optimization) \- 19th February


**Real\-time Analytics**


- [Real\-time Analytics with ClickHouse: Level 2](https://clickhouse.com/company/events/202601-EMEA-Real-time-Analytics-with-ClickHouse-Level2) \- 21st January
- [Real\-time Analytics with ClickHouse: Level 3](https://clickhouse.com/company/events/202601-EMEA-Real-time-Analytics-with-ClickHouse-Level3) \- 28th January


**Observability**


- [Observability with ClickStack: Level 1](https://clickhouse.com/company/events/202601-APJ-Observability-with-ClickStack-Level1) (APJ time) \- 27th January
- [Observability with ClickStack: Level 2](https://clickhouse.com/company/events/202601-APJ-Observability-with-ClickStack-Level2) (APJ time) \- 29th January
- [Observability with ClickStack: Level 1](https://clickhouse.com/company/events/202602-AMER-Observability-with-ClickStack-Level1) \- 4th February
- [Observability with ClickStack: Level 2](https://clickhouse.com/company/events/202602-AMER-Observabiity-with-ClickStackLevel2) \- 5th February


### Events in AMER [\#](/blog/202601-newsletter#events-in-amer)


- [Iceberg Meetup in Menlo Park](https://luma.com/abggijbh) \- 21st January
- [Iceberg Meetup in NYC](https://luma.com/ifxnj82q) \- 23rd January
- [New York Meetup](https://luma.com/iicnlq41) \- 26th January
- [The True Cost of Speed: What Query Performance Really Costs at Scale](https://clickhouse.com/company/events/webinar-true-cost-of-speed) \- 3rd February
- [AI Night SF](https://luma.com/j2ck1sbz) \- 11th February
- [Toronto Meetup](https://www.meetup.com/clickhouse-toronto-user-group/events/312881151/?slug=clickhouse-toronto-user-group&eventId=310164482&isFirstPublish=true) \- 19th February
- [Seattle Meetup](https://luma.com/jsctpwoa) \- 26th February
- [LA Meetup](https://luma.com/wbkqmaqk) \- 6th March


### Events in EMEA [\#](/blog/202601-newsletter#events-in-emea)


- [Data \& AI Paris Meetup](https://luma.com/3szhmv9h) \- 22nd January
- [The Agentic Data Stack: The Future is Conversational](https://clickhouse.com/company/events/agentic-data-stack-ams) (Amsterdam) \- 27th January
- [ClickHouse Meetup in Paris](https://clickhouse.com/company/events/202601-EMEA-Paris-meetup) \- 28th January
- [Apache Iceberg™ Meetup Belgium: FOSDEM Edition](https://luma.com/yx3lhqu9) \- 30th January
- [FOSDEM Community Dinner Brussels](https://luma.com/czvs584m) \- 31st January
- [ClickHouse Meetup in Barcelona](https://clickhouse.com/company/events/202602-EMEA-Barcelona-meetup) \- 5th February
- [ClickHouse Meetup in London](https://clickhouse.com/company/events/202602-EMEA-London-meetup) \- 10th February
- [ClickHouse Meetup in Tbilisi Georgia](https://www.meetup.com/clickhouse-georgia-meetup-group/events/312852206/) \- 24th February


### Events in APAC [\#](/blog/202601-newsletter#events-in-apac)


- [ClickHouse Singapore Meetup](https://clickhouse.com/company/events/202601-APJ-Singapore-Meetup) \- 27th January
- [Boot Camp: Real\-time Analytics with ClickHouse](https://clickhouse.com/company/events/202601-APJ-Real-time-Analytics-w-ClickHouse) \- 27th January
- [ClickHouse Seoul Meetup](https://clickhouse.com/company/events/202601-apj-seoul-meetup) \- 29th January


### Speaking at ClickHouse meetups [\#](/blog/202601-newsletter#speaking-at-clickhouse-meetups)


Want to speak at a ClickHouse meetup? [Apply here!](https://docs.google.com/forms/d/e/1FAIpQLSdpYbh0k3hmLOQ7JLXrubvEbiIul4TxJDp1AVewXHSdzHcmzA/viewform)


Below are some upcoming call for papers (CFPs):


- [Iceberg Summit SF](https://sessionize.com/iceberg-summit-2026/) \- April 6\-8
- [AI Council SF](https://aicouncil.com/apply-to-speak) \- May 12\-14
- [Observability Summit Minneapolis](https://sessionize.com/observability-summit-2026) \- May 21\-22
- [Kubecon India Mumbai](https://events.linuxfoundation.org/kubecon-cloudnativecon-india/program/cfp/) \- June 18\-19
- [GrafanaCon Barcelona](https://pretalx.com/grafanacon-2026/cfp) \- April 20\-22
- [We Are Developers Berlin](https://sessionize.com/wearedevelopers-world-congress-2026-europe) \- July 8\-10
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
