# ClickHouse Newsletter September 2022: Deleting data can make you feel better


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter September 2022: Deleting data can make you feel better

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Sep 15, 2022 · 7 minutes readIt’s been an exciting month at ClickHouse. We’ve released Lightweight Deletes, one of the most highly anticipated ClickHouse features of 2022\. And we’re getting close to publicly launching ClickHouse Cloud (sign up for early access [here](https://clickhouse.com/cloud)).


Read on about snazzy features in our ClickHouse 22\.8 LTS (Long Term Support) release, a simple example of the new DELETE query, and a roundup of ClickHouse stories for the last month.


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox as well? Sign up [here](https://discover.clickhouse.com/newsletter.html).


## Upcoming Events [\#](/blog/newsletter_2022_september#upcoming-events)


Mark your calendar:


**ClickHouse v22\.9 Release Webinar**


- ***When?*** Thursday, September 22 @ 9 am PST / 6 pm CEST
- ***How do I join?*** Register [here](https://clickhouse.com/company/events/v22-9-release-webinar).


**Silicon Valley ClickHouse Meetup**


- ***What?*** Come hang out with other users and hear what PostHog, Grafana and Barracuda are doing with ClickHouse.
- ***Where?*** San Jose, CA
- ***When?*** Wednesday, September 28 @ 6 pm PST
- ***How do I join?*** Register [here.](https://www.meetup.com/clickhouse-silicon-valley-meetup-group/events/288140358/)


**AWS re**


- ***What?*** A number of the ClickHouse team are going to be at re! Interested in meeting up with us, maybe grabbing a beverage, and talking about ClickHouse? Let us know!
- ***Where?*** Las Vegas, NV
- ***When?*** November 29 \- December 3, 2022


## ClickHouse v22\.8 LTS [\#](/blog/newsletter_2022_september#clickhouse-v228-lts)


Our new Long Term Support release is out with many new features:


1. **[DELETE query](https://clickhouse.com/docs/en/sql-reference/statements/delete/)** It’s finally here! Lightweight deletes were one of the most requested features in our [2022 roadmap](https://github.com/ClickHouse/ClickHouse/issues/32513) and we delivered it with many months to spare. Whenever you are currently using `ALTER TABLE … DELETE` you should switch to `DELETE FROM … WHERE` in almost all cases. It is much cheaper to execute, though still asynchronous (set `mutations_sync = 2` to wait for the query to complete).
2. **[Extended date ranges](https://github.com/ClickHouse/ClickHouse/pull/39425)** `Date32` and `DateTime64` now support dates from 1900 to 2299 (1925 to 2283 before).
3. **[Parallel distributed insert from S3](https://github.com/ClickHouse/ClickHouse/pull/39107)** ClickHouse can already insert data very quickly on a single machine (typically millions of rows per second). But if you have a cluster of machines, you can now insert from S3 in parallel on all of them. Maybe even billions of rows a second are possible? Somebody should try it.
4. **[JSON logging](https://github.com/ClickHouse/ClickHouse/pull/39277)** ClickHouse can now output its logs in JSON format. This should make it easier to ingest into and query in log management software. You can also ingest into ClickHouse, of course.
5. **\[Infer dates and numbers](<https://github.com/ClickHouse/ClickHouse/pull/39186>** When using schema inference, you can now tell ClickHouse to try to infer dates and numbers from strings.
6. **[Query parameters](https://github.com/ClickHouse/ClickHouse/pull/39906)** can now be set in interactive mode. For example, to define a parameter named `user` just use `SET param_user = alexey`.
7. **[More Pretty formats](https://github.com/ClickHouse/ClickHouse/pull/39646)** Here are 7 more, bringing the total to almost 70\. I personally like `PrettyMonoBlock`, but all formats are really “pretty”.


Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.8/), the [recording](https://youtu.be/yob7AnaBJz0) and please upgrade \- it is a Long Term Support release.


## Query of the Month: Deleting data can make you feel better [\#](/blog/newsletter_2022_september#query-of-the-month-deleting-data-can-make-you-feel-better)


For this month, let’s keep it simple. And tongue in cheek, just a little bit.


If there is one new feature in ClickHouse 22\.8 that you absolutely must try it’s the new DELETE query. Up to now, the only way to delete specific rows in ClickHouse was to use an `ALTER TABLE table DELETE WHERE cond` statement. It would asynchronously rewrite all data files containing rows matching the condition. Since data files in ClickHouse can by default be up to 150 GB this was very expensive and could lead to significant CPU and memory usage.


The new DELETE query takes a different approach. Instead of physically deleting all data immediately it only marks the specified rows as deleted using a hidden column. The data is still there, but it is transparently filtered out of queries. Effectively, all queries are executed with an additional condition `WHERE _deleted = false`. Later, as ClickHouse merges files in the background it will drop any rows marked as deleted during the merge process.


Let’s see how useful the new DELETE query can be.


Just for fun, let’s create a table with a portfolio of stablecoins (cost is cost of purchase per coin on January 1, 2022, price is the value on 26 August 2022\):



```
CREATE TABLE mymoney engine = MergeTree ORDER BY coin AS
SELECT 'USDC' AS coin, 1000 AS amount, 1.0002 AS cost, 0.9999 AS price
UNION ALL SELECT 'USDT', 1000, 1.0001, 1.00
UNION ALL SELECT 'USTC', 1000, 1.00, 0.0275

```

And let’s calculate our portfolio return:



```
SELECT sum(amount * cost) cost, sum(amount * price) value,
value - cost gain_loss, 1 - value / cost pct  FROM mymoney

```

We lost 32% of our money! What happened? Turns out TerraUSD (USTC) was not such a [“stable” stablecoin after all](https://www.investopedia.com/terrausd-crash-shows-risks-of-algorithmic-stablecoins-5272010).


But no matter, the DELETE query will take care of this:



```
SET allow_experimental_lightweight_delete = 1
DELETE FROM mymoney WHERE coin = 'USTC'

```

And now our portfolio return looks much better. If only it was that simple…


## Reading Corner [\#](/blog/newsletter_2022_september#reading-corner)


What we’ve been reading:


1. [Cloudflare Blog: Log analytics using ClickHouse](https://blog.cloudflare.com/log-analytics-using-clickhouse/) Besides using ClickHouse for serving real\-time HTTP and DNS analytics ([link](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse/), [link](https://blog.cloudflare.com/how-cloudflare-analyzes-1m-dns-queries-per-second/)) Cloudflare is also using ClickHouse for storing internal logs. By moving from Elasticsearch to ClickHouse, they were able to remove sampling, and provide fast querying while saving costs.
2. [ClickHouse Plugin for Grafana \- 2\.0 Release](https://clickhouse.com/blog/clickhouse-grafana-plugin-2.0) Version 2\.0 of our popular ClickHouse plugin for Grafana, now supports HTTP connections and the JSON data type, among other changes. Check it out!
3. [Exploring massive, real\-world data sets: 100\+ Years of Weather Records in ClickHouse](https://clickhouse.com/blog/real-world-data-noaa-climate-data) What loading more than a century of weather data into ClickHouse looks like and how you can use it.
4. [Getting Data Into ClickHouse \- Part 1](https://clickhouse.com/blog/getting-data-into-clickhouse-part-1) and [Part 2](https://clickhouse.com/blog/getting-data-into-clickhouse-part-2-json) A walkthrough of getting Hacker News data into ClickHouse and running some fun queries on it.
5. [MySQL CDC to Clickhouse using Decodable's Change Stream Capabilities](https://youtu.be/Nvy1HWB1mT0) Decodable shows in this video how to synchronize data from MySQL to ClickHouse.
6. [New ClickHouse Adopters](https://clickhouse.com/docs/en/introduction/adopters/): A fun addition this month, welcome Nintendo emulator [Dolphin](https://twitter.com/delroth_/status/1567300096160665601). Also welcome to open source ad blocker [AdGuard](https://adguard.com/en/blog/adguard-dns-2-0-goes-open-source.html) and non\-profit project [OONI](https://twitter.com/OpenObservatory/status/1558014810746265600?s=20&t=hvcDU-LIrgCApP0rZCzuoA). Get yourself added as well!


Thanks for reading. We’ll see you next month!


The ClickHouse Team

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
