# October 2024 newsletter


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Community](/blog?category=community)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# October 2024 newsletter

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Oct 17, 2024 · 6 minutes readWelcome to the October ClickHouse newsletter, which will round up what’s happened in real\-time data warehouses over the last month.


This month, we have the impressions and challenges of ClickHouse from a first\-time user, the APPEND clause for Refreshable Materialized Views, the pancake SQL pattern, and more!


 


## Inside this issue [\#](/blog/202410-newsletter#inside-this-issue)


- [Featured community member](https://clickhouse.com/blog/202410-newsletter#featured-community-member)
- [Upcoming events](https://clickhouse.com/blog/202410-newsletter#upcoming-events)
- [ClickHouse for Embedded Analytics: First Impressions and Unexpected Challenges](https://clickhouse.com/blog/202410-newsletter#clickhouse-for-embedded-analytics-first-impressions-and-unexpected-challenges)
- [Using ClickHouse for High\-Volume Data Pipeline Processing and Asynchronous Updates](https://clickhouse.com/blog/202410-newsletter#using-clickhouse-for-high-volume-data-pipeline-processing-and-asynchronous-updates)
- [24\.9 release](https://clickhouse.com/blog/202410-newsletter#249-release)
- [The pancake SQL pattern](https://clickhouse.com/blog/202410-newsletter#the-pancake-sql-pattern)
- [ClickHouse Cloud Live Update: September 2024](https://clickhouse.com/blog/202410-newsletter#clickhouse-cloud-live-update-september-2024)
- [Quick reads](https://clickhouse.com/blog/202410-newsletter#quick-reads)
- [Post of the month](https://clickhouse.com/blog/202410-newsletter#post-of-the-month)


 


## Featured community member [\#](/blog/202410-newsletter#featured-community-member)


This month's featured community member is Duc\-Canh Le, a Software Engineer at Ahrefs.


![featured-member-202410.png](/uploads/featured_member_202410_c1f100c1e1.png)
Duc\-Canh works on data infrastructure at Ahrefs and is responsible for developing and operating ClickHouse on over 600 machines that hold 100 PB of compressed data.


He is a regular contributor to the ClickHouse code base and has made 28 contributions in the calendar year. These include supporting OPTIMIZE on join tables to reduce their memory footprint, fixing a bug when using an empty tuple on the left\-hand side of the \`IN\` function, and a fix for the FINAL clause when run on tables that don’t use adaptive granularity. 


[Follow Duc\-Canh on LinkedIn](https://www.linkedin.com/in/canhld?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter)


 


## Upcoming events [\#](/blog/202410-newsletter#upcoming-events)


**Global events**


- [Release call 24\.10](https://clickhouse.com/company/events/v24-10-community-release-call?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Oct 31
- [ClickHouse Cloud Live Update](https://clickhouse.com/company/events/202411-cloud-update-live?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Nov 12


**Free training**


- [BigQuery to ClickHouse Workshop](https://clickhouse.com/company/events/202410-emea-clickhouse-bigquery-workshop?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Oct 23
- [Query optimization with ClickHouse workshop](https://clickhouse.com/company/events/202410-emea-query-optimization?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Oct 30
- [ClickHouse Fundamentals](https://clickhouse.com/company/events/clickhouse-fundamentals?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Nov 6
- Migrating from Postgres to ClickHouse Workshop
- [Asia Pacific](https://clickhouse.com/company/events/202411-apj-postgres-to-clickhouse-migration?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Nov 20
- [Europe](https://clickhouse.com/company/events/202411-emea-postgres-to-clickhouse-migration?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Nov 27


**Events in AMER**


- [Coffee with ClickHouse in Santa Monica](https://clickhouse.com/company/events/202410-amer-la-coffee-with-clickhouse?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Oct 25
- [KubeCon North America](https://clickhouse.com/company/events/202411-amer-kubecon?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Nov 12\-15
- [Microsoft Ignite \- Chicago](https://clickhouse.com/company/events/202411-amer-microsoft-ignite?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Nov 19\-22


**Events in EMEA**


- [Meetup in Madrid](https://www.meetup.com/clickhouse-spain-user-group/events/303096564) \- Oct 22
- [Coffee with ClickHouse](https://clickhouse.com/company/events/202410-emea-coffee-with-clickhouse?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Oct 23
- [Meetup in Oslo](https://www.meetup.com/open-source-real-time-data-warehouse-real-time-analytics/events/302938622/) \- Oct 31
- [Meetup in Barcelona](https://www.meetup.com/clickhouse-spain-user-group/events/303096876/?eventOrigin=network_page) \- Nov 12
- [Meetup in Ghent](https://www.meetup.com/clickhouse-belgium-user-group/events/303049405) \- Nov 19
- [Meetup in Dubai](https://www.meetup.com/clickhouse-dubai-meetup-group/events/303096989/) \- Nov 21
- [Meetup in Paris](https://www.meetup.com/clickhouse-france-user-group/events/303096434) \- Nov 26


**Events in Asia Pacific**


- [Data \& AI Summit VIC](https://clickhouse.com/company/events/202410-dataai-summit-vic-melbourne?utm_source=clickhouse&utm_medium=email&utm_campaign=202410-newsletter) \- Oct 22


## ClickHouse for Embedded Analytics: First Impressions and Unexpected Challenges [\#](/blog/202410-newsletter#clickhouse-for-embedded-analytics-first-impressions-and-unexpected-challenges)


Jorin Vogel recently started using ClickHouse for an embedded analytics project and shared his first thoughts. He also described things he wished he’d known before starting, including how materialized views work and working with duplicate data. This is a good read if you’re just starting your ClickHouse journey.


[Read the blog post](https://jorin.me/clickhouse-for-embedded-analytics-first-impressions-and-unexpected-challenges/?utm_source=clickhouse&utm_medium=web&utm_campaign=202410-newsletter)


 


## Using ClickHouse for High\-Volume Data Pipeline Processing and Asynchronous Updates [\#](/blog/202410-newsletter#using-clickhouse-for-high-volume-data-pipeline-processing-and-asynchronous-updates)


![pipeline.png](/uploads/pipeline_bcfce69e8c.png)
Marais Kruger works at Evinced (a company focused on accessibility compliance for enterprise clients) and has written a blog post about this experience building a ClickHouse\-based data pipeline.

Marais explains how they designed their pipeline to handle a large volume of incoming data while also handling infrequent updates to that data. He also describes how they made writes idempotent using ClickHouse’s duplicate block detection and a setting used to ensure similar behavior with dependent materialized views.

This one is a good read for the ClickHouse enthusiast or anyone curious about how to design data pipelines at scale.

[Read the blog post](https://blog.devgenius.io/architecting-for-scale-e998fc0adef0?utm_source=clickhouse&utm_medium=web&utm_campaign=202410-newsletter)


 


## 24\.9 release [\#](/blog/202410-newsletter#249-release)


![Blog Banner 24.9 release.png](/uploads/Blog_Banner_24_9_release_fee8640903.png)
The 24\.9 release introduced the APPEND clause for working with refreshable materialized views. When configured, the materialized view’s query will append results to the end of the destination table rather than replacing everything. This is useful if you want to capture snapshots of data from other tables or poll data from an external API and store it in ClickHouse.

This release also made response headers available when using the url table function, automatic inference of the Variant data type, and aggregate functions to query the new JSON data type.

[Read the release post](https://clickhouse.com/blog/clickhouse-release-24-09)


 


## The pancake SQL pattern [\#](/blog/202410-newsletter#the-pancake-sql-pattern)


![pancake.png](/uploads/pancake_22852d5f23.png)
Jacek Migdal had a tricky problem: One of the Quesma dashboards was sending up to 10 queries to populate a single panel, putting the ClickHouse database under pressure. 

Jacek was trying to solve this problem and had a lightbulb moment while feeding his toddler pancakes: Could the dashboard queries be redesigned to look more like pancakes?

Rather than spawning multiple queries, they put everything into one query. The aggregations would be stacked on each other, like a pancake, where each layer is a grouping with a limit, and between layers, they have metric aggregations—our pancake “fillings.”

It worked, and they’re seeing a 50x increase in performance.

[Read the blog post](https://quesma.com/blog-detail/pancake-sql-pattern)


 


## ClickHouse Cloud Live Update: September 2024 [\#](/blog/202410-newsletter#clickhouse-cloud-live-update-september-2024)


![Cloud monthly update feature.png](/uploads/Cloud_monthly_update_feature_41fa8ef49c.png)
We had a special guest, [Dunith Danushka](https://www.linkedin.com/in/dunithd/) from Redpanda, join us for our latest ClickHouse Cloud update call. Dunith and Mark Needham showed how to use the combination of Redpanda Serverless, ClickHouse Cloud, and OpenAI to power a sports commentary Copilot application.

We also had updates on some upcoming features in ClickHouse Cloud, including Bring Your Own Cloud, Compute\-Compute separation, and the JSON data type.

[Watch the recording](https://clickhouse.com/videos/202409-clickhouse-cloud-live-updates)


 


## Quick reads [\#](/blog/202410-newsletter#quick-reads)


- Juan S. Carrillo [wrote a User Defined Function (UDF)](https://clickhouse.com/blog/semantic-versioning-udf) to make it easier to sort software versions.
- Rafal Kwasny explores various options for data storage and focuses on [using ClickHouse for high\-performance financial data analysis](https://rafalkwasny.com/clickhouse-tick-store).
- Alexey Milovidov [shared his favorite ClickHouse features of 2024](https://clickhouse.com/videos/my-favorite-clickhouse-features) at a recent San Francisco meetup.
- Sai Srirampur and Bryan Clark wrote a blog post explaining how to [combine ClickHouse and Neon for real\-time analytics on transactional data](https://neon.tech/blog/postgres-meets-analytics-cdc-from-neon-to-clickhouse-via-peerdb) using PeerDB to sync the data.


 


## Post of the month [\#](/blog/202410-newsletter#post-of-the-month)


Our favorite post this month was by [Carl Lindesvärd](https://x.com/CarlLindesvard/) about ClickHouse’s compression rate, a somewhat underrated feature!


![tweet_1842113023890137251_20241016_155508_via_10015_io.png](/uploads/tweet_1842113023890137251_20241016_155508_via_10015_io_4844142657.png)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
