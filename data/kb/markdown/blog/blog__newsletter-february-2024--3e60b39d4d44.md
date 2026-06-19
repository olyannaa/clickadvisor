# February 2024 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# February 2024 Newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Feb 28, 2024 · 3 minutes readWelcome to the February ClickHouse newsletter where we round up what’s been happening in the world of real\-time data warehouses in the last month.


This month, we have a deep dive into ClickHouse’s internals, the Grafana v4\.0 plugin, and the 24\.1 release with the experimental Variant type.


## Inside this issue [\#](/blog/newsletter-february-2024#inside-this-issue)


- [Featured community member](/blog/newsletter-february-2024#featured-community-member)
- [ClickHouse Grafana plugin 4\.0 \- Leveling up SQL Observability](/blog/newsletter-february-2024?utm_source=clickhouse&utm_medium=email&utm_campaign=202402-newsletter#clickhouse-grafana-plugin-40---leveling-up-sql-observability)
- [ClickHouse Cloud Live: February 2024](/blog/newsletter-february-2024?utm_source=clickhouse&utm_medium=email&utm_campaign=202402-newsletter#clickhouse-cloud-live-february-2024)
- [24\.1 release](/blog/newsletter-february-2024?utm_source=clickhouse&utm_medium=email&utm_campaign=202402-newsletter#241-release)
- [Understanding ClickHouse’s Architecture](/blog/newsletter-february-2024?utm_source=clickhouse&utm_medium=email&utm_campaign=202402-newsletter#understanding-the-clickhouse-architecture)
- [Post of the month](/blog/newsletter-february-2024?utm_source=clickhouse&utm_medium=email&utm_campaign=202402-newsletter#post-of-the-month)
- [Upcoming events](/blog/newsletter-february-2024?utm_source=clickhouse&utm_medium=email&utm_campaign=202402-newsletter#upcoming-events)


## Featured community member [\#](/blog/newsletter-february-2024#featured-community-member)


Our featured community member this month is [Benjamin Wooton](https://www.linkedin.com/in/benjaminwootton?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter), founder \& CTO of Ensemble, a company that helps businesses deploy real\-time data, analytics, and AI platforms [based on ClickHouse](https://ensembleanalytics.io/why-clickhouse-cloud?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter).


![ben.png](/uploads/ben_12da3f4537.png)
Benjamin is a passionate advocate of ClickHouse and you’ll often see him engaging in discussions about real\-time data warehouses and similar topics on LinkedIn and Twitter.


He’s also written several blog posts over the last few weeks, covering various use cases. In the most recent one, Benjamin comes up with the optimal way of allocating consultants to projects based on their skills using Google’s OR\-Tools library mixed in with some ClickHouse queries. He also uses a similar toolkit to come up with [a solution to a traveling salesman type problem](https://ensembleanalytics.io/blog/clickhouse-vehicle-route-planning?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter).


And if that’s not enough, Benjamin also presented Building Real\-Time Analytics Systems with ClickHouse at the [ClickHouse London meetup](https://www.meetup.com/clickhouse-london-user-group/events/298891993/) this week.


[Follow Benjamin on LinkedIn](https://www.linkedin.com/in/benjaminwootton/)


 


## ClickHouse Grafana plugin 4\.0 \- leveling up SQL observability [\#](/blog/newsletter-february-2024#clickhouse-grafana-plugin-40---leveling-up-sql-observability)


![grafana2x.png](/uploads/grafana2x_03066c6102.png)
We released the Grafana 4\.0 plugin. With first\-class support for logs and traces, it’s now easier than ever to make sense of log data stored in ClickHouse.


[Read the release post](https://clickhouse.com/blog/clickhouse-grafana-plugin-4-0?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter)


 


## ClickHouse Cloud Live: February 2024 [\#](/blog/newsletter-february-2024#clickhouse-cloud-live-february-2024)


![Cloudupdate.png](/uploads/Cloudupdate_357d49888f.png)
The ClickHouse Cloud update call brought together a bunch of folks to talk about recent releases and the roadmap going forward. A unified console, new authentication options, and more.


[Watch the video](https://clickhouse.com/videos/clickhouse-cloud-update-call-feb2024?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter)


 


## 24\.1 Release [\#](/blog/newsletter-february-2024#241-release)


The 24\.1 release introduces the Variant type, which is the first step on the way to semi structured column support in ClickHouse. We also have more string similarity functions, as well as performance improvements when using the FINAL keyword with the ReplacingMergeTree


[Read the release post](https://clickhouse.com/blog/clickhouse-release-24-01?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter)


 


## Understanding the ClickHouse architecture [\#](/blog/newsletter-february-2024#understanding-the-clickhouse-architecture)


![Understanding the ClickHouse architecture](/rs/238-FPC-317/images/CH%20architecture.png)
Jack Vanlightly, Staff Technologist at Confluent, does a deep dive into the ClickHouse architecture, starting out with the way data is ingested. He explains the writing of parts, how they’re merged, as well as data organization and indexes. He also covers the various table engines, compression techniques, data partitioning, and more.


[Read the blog post](https://jack-vanlightly.com/analyses/2024/1/23/serverless-clickhouse-cloud-asds-chapter-5-part-1?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter)


 


## Post of the month [\#](/blog/newsletter-february-2024#post-of-the-month)


![Tweet.png](/uploads/Tweet_14d584c769.png)
[See the thread](https://twitter.com/baptistejamin/status/1755599333452550224)


 


## Upcoming events [\#](/blog/newsletter-february-2024#upcoming-events)


- [v24\.2 Community Call](https://clickhouse.com/company/events/v24-2-community-release-call?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter) \- February 29th
- [FREE ClickHouse Training](https://clickhouse.com/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=web&utm_campaign=202402-newsletter) \- Various dates in March
- [San Francisco Meetup](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/299058486/) \- March 4th
- [Seattle Meetup](https://www.meetup.com/clickhouse-seattle-user-group/events/298650371/) \- March 11th
- [New York Meetup](https://www.meetup.com/clickhouse-new-york-user-group/events/298640542/) \- March 19th
- [Melbourne Meetup](https://www.meetup.com/clickhouse-australia-user-group/events/299479750/) \- March 20th
- [Paris Meetup](https://www.meetup.com/clickhouse-france-user-group/events/298997115/) \- March 21st
- [Bangalore Meetup](https://www.meetup.com/clickhouse-bangalore-user-group/events/299479850/) \- March 23rd
Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
