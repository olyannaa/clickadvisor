# ClickHouse replaces Postgres to power real\-time analytics in Common Room customer portal


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse replaces Postgres to power real\-time analytics in Common Room customer portal

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 20, 2024 · 4 minutes read*Integrating ClickHouse has been a significant step in Common Room’s data management evolution, empowering it to handle the growing complexity and volume of customer data that comes alongside its marketplace success.*


Founded in 2020, [Common Room](https://www.commonroom.io/) is an AI\-powered customer intelligence platform that helps organizations run go\-to\-market (GTM) intelligently from end to end. Digital signal capture, unified identity and account intelligence, and AI and automations come together in one platform to help GTM teams reach the right person with the right context at the right time. One of the founding software engineers, Kirill Sapchuk, [spoke at a recent ClickHouse meetup](/videos/commonroom-clickhouse) to give us the rundown on Common Room and some insights around its data management journey.


![common-room-img1.png](/uploads/common_room_img1_7927389f93.png)
Common Room aggregates data from many different sources—including products, websites, CRMs, LinkedIn, X, Slack, GitHub, Reddit, YouTube, and many more—and connects cross\-channel activity to real people and real accounts. This provides GTM teams with a unified view of customers across the entire digital ecosystem: *“Before Common Room, people would build a spreadsheet and then manually extract data from sources like Twitter or Slack, then struggle to combine and parse it all. It was, at best, a cumbersome process,”* said Kirill. He and the rest of the Common Room team wanted to transform how organizations connect with people.


## Challenges with Postgres powering real\-time analytical workloads [\#](/blog/clickhouse-replaces-postgres-to-power-real-time-analytics-in-common-room-customer-portal#challenges-with-postgres-powering-real-time-analytical-workloads)


Initially, the focus was on pulling in data from different sources to create a unified view of the customer: *“Each individual is represented by what’s called a ‘member object’, which gathers all their information from all the relevant data sources plus other important data. Who are they? What segment? Previous companies? Etc.,”* Kirill explained. Then the team made it possible to search through contacts and their organizations using a rich set of multi\-faceted filters and set up rules for proactive notifications and workflows based on these criteria.


This interactive, data\-driven experience required a powerful analytical database to execute these operations quickly and efficiently. The original architecture relied on Postgres as the sole datastore for both transactional and analytical datasets, but the Common Room team found that as the datasets grew, PostgreSQL was no longer the right fit for the [analytical queries powering its user interface](https://clickhouse.com/resources/engineering/how-to-choose-a-database-for-real-time-analytics-in-2026). The company began to [look for alternatives](https://clickhouse.com/resources/engineering/managed-postgres-for-ai-and-real-time-apps).


![common-room-img2.png](/uploads/common_room_img2_762bea1427.png)
## Enter ClickHouse Cloud [\#](/blog/clickhouse-replaces-postgres-to-power-real-time-analytics-in-common-room-customer-portal#enter-clickhouse-cloud)


Attracted by the active ClickHouse community and a turnkey cloud version ready for testing, Common Room explored using ClickHouse for its use case. Namely, supporting 10\-million\-member records with 100 fields each. *“We had a billion rows to store,”* said Kirill.


Traditional analytical databases are optimized for immutable, append\-only data, but Common Room’s top priority was a solution that could handle frequent updates—25% of records updated daily. ClickHouse provides purpose\-built table engines that handle data with updates without sacrificing the performance of analytical queries. Common Room adopted the `ReplacingMergeTree` table engine to handle updates and noted considerable performance improvements in 23\.12 with the \<FINAL\> modifier. The team also adopted the `VersionCollapsingMergeTree` table engine for more complex scenarios like handling deletions without which the high volume of changes would lead to a 25% increase in the table size daily. Using \+1/\-1 signs allowed for marking old rows for deletion and replacement.


Common Room also implemented refreshable materialized views to provide fast, queryable versions of data for scenarios where some delay was acceptable. To use these views effectively, the team also had to optimize the order of JOIN operations. While Common Room still uses PostgreSQL for point queries and Kafka for batch data transformation, ClickHouse now handles the majority of live, customer\-initiated queries—serving as a fast search engine.


![common-room-img3.png](/uploads/common_room_img3_23f04368d0.png)
ClickHouse has proven to be an invaluable addition to Common Room’s tech stack, allowing them to efficiently process complex analytical queries on top of recent and historical data without compromising performance. [Watch the video](/videos/commonroom-clickhouse) to find out more!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
