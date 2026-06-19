# ClickHouse Newsletter October 2022: A cloud has arrived


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Newsletter October 2022: A cloud has arrived

![photo-christoph-wurm[1].jpeg](/_next/image?url=%2Fuploads%2Fphoto_christoph_wurm_1_7af9415ecb.jpeg&w=96&q=75)[Christoph Wurm](/authors/christoph-wurm)Oct 13, 2022 · 9 minutes readThis month, let’s start with some important weather information, then dive into the September release and round it out with some thread work.


By the way, if you’re reading this on our website, did you know you can receive every monthly newsletter as an email in your inbox as well? Sign up [here](https://discover.clickhouse.com/newsletter.html).


## ClickHouse Cloud Beta [\#](/blog/newsletter_2022_october#clickhouse-cloud-beta)


If you’re a frequent reader of this newsletter, then you know that we’ve been hard at work building our [ClickHouse Cloud managed service](https://clickhouse.com/cloud). On Tuesday, October 4, 2022, we made the beta version available to the world!


It’s not just a ClickHouse managed service. Today, when you run ClickHouse yourself you’re probably running it on some VMs or Kubernetes pods and configuring replication, sharding, clusters, distributed tables, etc. to achieve high availability and scalability. That’s not what we did with ClickHouse Cloud. Instead, we moved the data to shared object storage that all ClickHouse nodes can access. With that, there is no need to configure anything extra for replication and sharding \- object storage is already replicated and it is practically infinitely scalable. In addition, object storage is several times cheaper than block storage.


Why does this matter? As a user, you benefit from the significantly lower price of storage and the ease of use of all data storage being taken care of for you. No more setting up replicas and shards and worrying about how to rebalance those when scaling a cluster up or down. No more worries about upgrades (we do those for you). No more worries about backups either (we do those for you, too). And of course, we monitor and support ClickHouse Cloud for you 24/7/365\.


ClickHouse Cloud is the only official ClickHouse managed service built by the creators of ClickHouse and designed from the ground up for the cloud. Give it a try!


Here’s the [release blog post](https://clickhouse.com/blog/clickhouse-cloud-public-beta), a [Quick Start guide](https://clickhouse.com/docs/en/quick-start/), and when you are ready to go head over to [our website](https://clickhouse.com/) and hit the “Try it now” button. Keep in mind it’s still a beta service, so we really appreciate any feedback from you. Also make sure you sign up to our [Launch Webinar](https://clickhouse.com/company/events/cloud-beta) later this month to learn about ClickHouse Cloud directly from our team.


## Upcoming Events [\#](/blog/newsletter_2022_october#upcoming-events)


Mark your calendars:


**ClickHouse v22\.10 Release Webinar**


- ***When? CHANGED TO:*** Wednesday, October 26 @ 9 am PST / 6 pm CEST
- ***How do I join?*** Register [here](https://clickhouse.com/company/events/v22-10-release-webinar).


**ClickHouse Cloud Launch Webinar**


- **What?** Join us for the virtual unveiling of our managed service. We’ll walk through all the features and give you a peek behind the curtain as well. Can’t wait to tell you all about it!
- **When?** Thursday, October 27 @ 9 am PST / 6 pm CEST
- **How do I join?** Register [here](https://clickhouse.com/company/events/cloud-beta).


**AWS re**


- **What?** A number of the ClickHouse team are going to be at re! Interested in meeting up with us, maybe grabbing a beverage, and talking about ClickHouse? Let us know!
- **Where?** Las Vegas, NV
- **When?** November 29 \- December 3, 2022


## ClickHouse v22\.9 [\#](/blog/newsletter_2022_october#clickhouse-v229)


Our first autumn release this year, with some neat new features:


1. [Vector search (ANN)](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/annindexes) ClickHouse has a new index type `annoy`. It implements a search index for Approximate Nearest Neighbor (ANN) search to quickly find the nearest neighbor in multidimensional space (vector search). This is an experimental feature.
2. [KeeperMap table engine](https://github.com/ClickHouse/ClickHouse/pull/39976) A new table engine `KeeperMap` allows storing small amounts of key\-value data in ClickHouse Keeper or ZooKeeper. This is an experimental feature.
3. [Automatically select quorum](https://clickhouse.com/docs/en/operations/settings/settings/#settings-insert_quorum) You can now set `insert_quorum = auto` to have ClickHouse automatically select a majority of replicas to write an insert to before reporting back success to the client. Note: Using insert\_quorum will make inserts take longer.
4. [Readonly users can now change settings](https://clickhouse.com/docs/en/operations/settings/constraints-on-settings/) It can be useful to allow read\-only users to change certain settings, the number of threads or table filters, for example. The setting `changeable_in_readonly` allows you to do just that.
5. [INTERSECT DISTINCT and EXCEPT DISTINCT](https://github.com/ClickHouse/ClickHouse/pull/40792) When combining results from two queries, it’s now possible to remove duplicate rows when using INTERSECT (which returns only rows present in both queries) and EXCEPT (which returns only rows present in the first but not the second query).
6. [Official Node.js client](https://github.com/clickhouse/clickhouse-js) ClickHouse now has an official Node.js client written in Typescript. It supports both reading and writing data over HTTP(S). Give it a try!


Take a look at the [release webinar slides](https://presentations.clickhouse.com/release_22.9/), the [recording](https://youtu.be/rK2BsaaaOCA) and please upgrade unless you want to stay on a Long Term Support (LTS) release.


## Query of the Month: More threads are not always better [\#](/blog/newsletter_2022_october#query-of-the-month-more-threads-are-not-always-better)


Many people, after they have used ClickHouse for a bit, will discover the magic of threads. Maybe loading data takes longer than you’d like or perhaps a query is slower than your boss wants it to be. So you do some googling and in an answer to an old StackOverflow question you read about [max\_threads](https://clickhouse.com/docs/en/operations/settings/settings/#settings-max_threads) and how it can be used to speed everything up.


And yet, as so often in life and technology, it’s not that simple!


By default, ClickHouse will try to determine the correct number of threads based on the number of available CPU cores. You can check what it is set to using `SELECT getSetting('max_threads')`. For example, on my MacBook Pro it returns 10, which is the number of cores in an Apple M1 chip (yes, ClickHouse works on ARM!).


You can set it to use more threads, but it won’t always work well. For example, try this (after you create the right table structure [see here](https://clickhouse.com/docs/en/getting-started/example-datasets/ontime/#creating-a-table)):



```
INSERT INTO ontime SELECT *
FROM s3('https://clickhouse-public-datasets.s3.amazonaws.com/ontime/csv_by_year/*.csv.gz', CSVWithNames)
SETTINGS max_threads = 100

```

Unless you have a really big machine, it will not complete – and use a lot of memory along the way. Effectively, every one of the 100 threads is a separate insert sub\-query and requires its own memory to retrieve and write data.


So should you set `max_threads = 1`? Well, maybe \- for me, the query above will insert data at about 120k rows per second when limited to a single thread. Without `max_threads` it will insert 320k rows per second. However, the optimal insert speed for me is with 4 threads \- 428k rows per second, some 33% faster than with thread autodetection. Sometimes it pays to experiment.


Similarly, when reading data, more threads are not always better. Yes, more threads mean there are more CPU cycles available to a query. However, it also means there are more separate states that all need to be merged back together before the result can be returned. Most importantly, many threads per query will reduce the number of queries per second that can be run.


For example, using the [UK Property Price Paid dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid), we can check what the most popular street names are using:



```
SELECT count(), street FROM uk_price_paid
GROUP BY street ORDER BY count() DESC

```

The top 3: High Street, Station Road, London Road. In the next 7, there are Church Road, Church Street, and Church Lane \- maybe not surprising in a monarchy where the King is both Head of State and Head of the Church.


This above query takes 0\.2 seconds on my machine. If I set `max_threads = 1` it takes 0\.5 seconds. So more threads are better, right?


In this case, yes \- except if I want to run this query many times concurrently. I can execute 10 queries concurrently 10 times (100 queries in total) with `clickhouse-benchmark`:



```
clickhouse-benchmark -c 10 -i 100 -q "<query>”

```

On my machine, it takes about 27 seconds to run all 100 queries, just under 4 queries a second (`QPS: 3.776` according to the result).


With `max_threads = 1` it takes about 10 seconds, or 13 queries per second (`QPS: 13.122`). Three times higher query throughput! And all we had to do was change the number of threads \- but lower, not higher. Generally, if you expect a lot of concurrent queries you should consider explicitly lowering the thread count per query.


## Reading Corner [\#](/blog/newsletter_2022_october#reading-corner)


What we’ve been reading:


- [ClickHouse Cloud is now in Public Beta](https://clickhouse.com/blog/clickhouse-cloud-public-beta) The launch blog post for the new and only official ClickHouse managed service by us, the creators of ClickHouse.
- [Getting Data Into ClickHouse \- Part 3 \- Using S3](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3) Part 3 of a series on how to get data into ClickHouse. Check out Parts 1 and 2 ([here](https://clickhouse.com/blog/getting-data-into-clickhouse-part-1) and [here](https://clickhouse.com/blog/getting-data-into-clickhouse-part-2-json)) as well.
- [Visualizing Data with ClickHouse \- Part 1 \- Grafana](https://clickhouse.com/blog/visualizing-data-with-grafana) First in a series on visualizing data with ClickHouse. We start with Grafana and will follow with posts on Superset and Metabase.


Thanks for reading, we’ll see you next month. And please test ClickHouse Cloud!


The ClickHouse Team

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
