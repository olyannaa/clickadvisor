# ClickHouse v21\.11 Released


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse v21\.11 Released

Rich RaposaNov 11, 2021 · 5 minutes readWe're continuing our monthly release cadence and blog updates at [ClickHouse, Inc](https://clickhouse.com/blog/en/2021/clickhouse-inc/). The 21\.11 release includes asynchronous inserts, interactive mode, UDFs, predefined connections, and compression gains. Thank you to the 142 committers and 4337 commits for making this release possible.


Let's highlight some of these new exciting new capabilities in 21\.11:


## Async Inserts [\#](/blog/click-house-v2111-released#async-inserts)


New asynchronous INSERT mode allows to accumulate inserted data and store it in a single batch utilizing less disk resources(IOPS) enabling support of high rate of INSERT queries. On a client it can be enabled by setting `async_insert` for `INSERT` queries with data inlined in a query or in a separate buffer (e.g. for `INSERT` queries via HTTP protocol). If `wait_for_async_insert` is true (by default) the client will wait until data will be flushed to the table. On the server\-side it can be tuned by the settings `async_insert_threads`, `async_insert_max_data_size` and `async_insert_busy_timeout_ms`.


**How does this help our ClickHouse Users?**


A notable pain point for users was around having to insert data in large batches and performance can sometimes be hindered. What if you have a monitoring use case and you want to do 1M records per second into ClickHouse; you would do large 100k record batches, but if you have 1,000 clients shipping data then that was hard to collect these batches to insert into ClickHouse. Historically to solve for this you might have to use Kafka or buffer tables to help with the balancing and insertion of data.


Now, we've introduced this new mode of Async inserts where you can do a high rate of small inserts concurrently and ClickHouse will automatically group them together into batches and insert it into the table automatically. Every client will get an acknowledgement that the data was inserted successfully.


## Local Interactive Mode [\#](/blog/click-house-v2111-released#local-interactive-mode)


We have added interactive mode for `clickhouse-local` so that you can just run `clickhouse-local` to get a command line ClickHouse interface without connecting to a server and process data from files and external data sources.


**How does this help our ClickHouse Users?**


What if you have an ad\-hoc use case that you want to run analytics on a local file with ClickHouse? Historically, you'd have to spin up an empty ClickHouse server and connect it to the external data source that you were interested in running the query on e.g. S3, HDFS, URL's. Now with ClickHouse Local you can just run it just like a ClickHouse Client and have the same full interactive experience without any additional overhead steps around setup and ingestion of data to try out your idea or hypothesis. Hope you enjoy!


## Executable UDFs [\#](/blog/click-house-v2111-released#executable-udfs)


Added support for executable (scriptable) user defined functions. These are UDFs that can be written in any programming language.


**How does this help our ClickHouse Users?**


We added UDFs in our 21\.10 release. Similar to our October release we're continuing to innovate around the idea of making it more user friendly to plug in tools into ClickHouse as functions. This could be you doing an ML inference in your Python script and now you can define it as a function as available in SQL. Or, what if you wanted to do a DNS lookup? You have a domain name in a ClickHouse table and want to convert to an IP address with some function. Now just plug in an external script and this will go process and convert the domain names into IP addresses.


## Predefined Connections [\#](/blog/click-house-v2111-released#predefined-connections)


Allow predefined connections to external data sources. This allows to avoid specifying credentials or addresses while using external data sources, they can be referenced by names instead.


**How does this help our ClickHouse Users?**


You're just trying to connect ClickHouse to another data source to load data, like MySQL for example, how do you do that? Before this feature you would have to handle all the credentials for MySql, use the MySQL table functions, know the user and password permissions to access certain tables, etc. Now you have a predefined required parameters inside the ClickHouse configuration and the user can just refer to this by a name e.g. MongoDB, HDFS, S3, MySQL and it's a one\-time configuration going forward.


## Compression [\#](/blog/click-house-v2111-released#compression)


Add support for compression and decompression for `INTO OUTFILE` and `FROM INFILE` (with autodetect or with additional optional parameter).


**How does this help our ClickHouse Users?**


Are you just looking to import and export data into ClickHouse more easily if you have compressed data? Before this feature you had to manually specify compression of input and output data into ClickHouse and even for stream insertion you'd still have to manage the decompression there too. Now, you can just write it as a file e.g. mytable.csv.gz \-\-\- and, go!


In the last month, we've added new free Training modules including a What's New in 21\.11\. Take the lesson [here](https://clickhouse.com/learn/lessons/whatsnew-clickhouse-21.11/).


## ClickHouse Release Notes [\#](/blog/click-house-v2111-released#clickhouse-release-notes)


Release 21\.11


Release Date: 2021\-11\-09


Release Notes: [21\.11](https://github.com/ClickHouse/ClickHouse/blob/master/CHANGELOG.md)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
