# July 2024 Newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# July 2024 Newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jul 16, 2024 · 4 minutes readWelcome to the July ClickHouse newsletter, which will round up what’s happened in real\-time data warehouses over the last month.


This month, we have optimal table sorting in the 24\.6 release, tracking vessels with ClickHouse \& Grafana, and tactics for optimizing CPU usage when running ClickHouse.


 


## Inside this issue [\#](/blog/202407-newsletter#inside-this-issue)


- [Featured community member](/blog/202407-newsletter#featured-community-member)
- [Upcoming events](/blog/202407-newsletter#upcoming-events)
- [24\.6 release](/blog/202407-newsletter#246-release)
- [How to track vessels with Python, ClickHouse, and Grafana](/blog/202407-newsletter#how-to-track-vessels-with-python-clickhouse-and-grafana)
- [ClickHouse MergeTree Engine](/blog/202407-newsletter#clickhouse-mergetree-engine)
- [Optimizing ClickHouse: The Tactics that worked for highlight.io](/blog/202407-newsletter#optimizing-clickhouse-tactics-that-worked-for-highlightio)
- [ClickHouse Cloud updates: July 2024](/blog/202407-newsletter#clickhouse-cloud-updates-july-2024)
- [Video corner: Import patterns](/blog/202407-newsletter#video-corner-import-patterns)
- [Post of the month](/blog/202407-newsletter#post-of-the-month)


 


## Featured community member [\#](/blog/202407-newsletter#featured-community-member)


This month's featured community member is taiyang\-li (李扬)


![202407-featuredmember.png](/uploads/202407_featuredmember_dad0aa43b0.png)
taiyang\-li is a frequent contributor to the ClickHouse database, regularly [contributing pull requests](https://github.com/ClickHouse/ClickHouse/pulls?q=is:pr+author:taiyang-li+) that improve ClickHouse’s performance and string processing capabilities.
In just the last few months, he’s committed code that let the \-UTF8 functions handle strings containing only ASCII characters, fixed concat to accept empty arguments, and improved the compatibility of the upper/lowerUTF8 functions.
And if you’ve noticed that the splitByRegexp, coalesce, or ifNotNull functions are quicker, you can also thank taiyang\-li for that!


[Follow Taiyang\-Li on GitHub](https://github.com/taiyang-li)


 


## Upcoming events [\#](/blog/202407-newsletter#upcoming-events)


- [ClickHouse Fundamentals](/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter) \- July 24th \& 25th
- [ClickHouse Community Call](/company/events/v24-7-community-release-call?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter) \- July 30th
- [Migrating from Postgres to ClickHouse Workshop](/company/events/202407-amer-postgres-to-clickhouse-migration?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter) \- July 31st
- [BigQuery to ClickHouse Workshop](/company/events/202408-clickhouse-bigquery-workshop?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter) \- August 7th
- [ClickHouse Fundamentals](/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter) \- August 13th \& 14th
- [ClickHouse Admin Workshop](/company/events/202408-clickhouse-admin-workshop?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter) \- August 21st


 


## 24\.6 release [\#](/blog/202407-newsletter#246-release)


![24_06_cd46491ba9.png](/uploads/24_06_cd46491ba9_13a3408f28.png)
The latest release of ClickHouse saw the introduction of optimal table sorting. We can use this setting on table creation, and when ingesting data, after sorting by ORDER BY key, ClickHouse will automatically sort data to achieve the best compression. We also had a beta release of chDB that lets you query Pandas DataFrames directly, and functions for Hilbert Curves were added.


[Read the release post](/blog/clickhouse-release-24-06?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter)


 


## How to track vessels with Python, ClickHouse, and Grafana [\#](/blog/202407-newsletter#how-to-track-vessels-with-python-clickhouse-and-grafana)


![vessel.jpg](/uploads/vessel_0b068d3284.jpg)
Ignacio Van Droogenbroeck has written a cool blog post on tracking vessels in San Francisco and Buenos Aires. He shows how to get the data from AisStream’s WebSockets API into ClickHouse and then creates a series of visualizations using Grafana.


[Read the blog post](https://cduser.com/tracking-vessels-using-python-clickhouse-grafana?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter)


 


## ClickHouse MergeTree Engine [\#](/blog/202407-newsletter#clickhouse-mergetree-engine)


![mergetree.png](/uploads/mergetree_67dfbe2252.png)
Tôi là Duyệt has started writing blog posts about using ClickHouse in Kubernetes. A recent post explores the default MergeTree table engine. Tôi explains what happens when data is ingested into a table using this engine. He then goes through how to use it, including inserting data, supported data types, and column modifiers.


[Read the blog post](https://blog.duyet.net/2024/05/clickhouse-mergetree.html?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter)


 


## Optimizing ClickHouse: Tactics that worked for highlight.io [\#](/blog/202407-newsletter#optimizing-clickhouse-tactics-that-worked-for-highlightio)


![cpu-wait.png](/uploads/cpu_wait_75875ad6b1.png)
highlight.io is an open\-source, full\-stack Monitoring Platform. It ingests 100 TB of observability per month, much of which goes into ClickHouse. CTO Vadim Korolik has written a blog post sharing their lessons on optimizing ClickHouse to reduce CPU load. 


[Read the blog post](https://www.highlight.io/blog/lw5-clickhouse-performance-optimization?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter)


 


## ClickHouse Cloud updates: July 2024 [\#](/blog/202407-newsletter#clickhouse-cloud-updates-july-2024)


![cloud-highlights.png](/uploads/cloud_highlights_6d571c03a7.png)
Did you know that we publish a ClickHouse Cloud Changelog every fortnight? In the latest version, we announced the availability of ClickHouse Cloud on Microsoft Azure and a new Query Logs Insights UI to make it easier to debug your queries. The Prometheus endpoints for metrics is also in Private Preview.


[View the changelog](/docs/en/whats-new/cloud?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter)


 


## Video corner: Import patterns [\#](/blog/202407-newsletter#video-corner-import-patterns)


Mark Needham has recorded several videos demonstrating import patterns with ClickHouse:


- [Deriving columns from other columns](/videos/derive-columns-other-columns?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter) shows how to use the DEFAULT, ALIAS, and MATERIALIZED column modifiers
- Next, we learn about the [EPHEMERAL column modifier](/videos/ephemeral-column-modifier?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter), which is used when we don’t want to store a column but rather have that column referenced by the other column modifiers.
- Finally, we use the [Null Table Engine](/videos/null-table-engine?utm_source=clickhouse&utm_medium=web&utm_campaign=202407-newsletter) to route incoming data to different destination tables based on filtering criteria.


 


## Post of the month [\#](/blog/202407-newsletter#post-of-the-month)


Our favorite post this month was by [anhtho](https://x.com/byAnhtho/status/1807761150001688797), who’s using ClickHouse to analyze billing data.


[Read the post](https://x.com/byAnhtho/status/1807761150001688797)


![tweet-1807761150001688797-july224.png](/uploads/tweet_1807761150001688797_july224_a22d88887a.png)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
