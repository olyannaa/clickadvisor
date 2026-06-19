# RunReveal Is Building The Ridiculously Fast Security Data Platform On ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# RunReveal Is Building The Ridiculously Fast Security Data Platform On ClickHouse

![](/_next/image?url=%2Fuploads%2FAlan_727600c354.png&w=96&q=75)Alan BraithwaiteNov 8, 2023 · 6 minutes readWhen I first read about ClickHouse, I was highly skeptical. In search of a better solution for aggregating HTTP analytics on the data team at Cloudflare, I'd experimented with many distributed databases and stream processing frameworks.


ClickHouse came along in 2016 and promised high write throughput and fast aggregations while still being (relatively) simple to operate. After trying Flink, Spark, Druid, Storm, HBase and others, I had serious skepticism that anything not written in house at Cloudflare would stand up to the scale we needed.


I was wrong.


The more I learned about ClickHouse, the more I became convinced it will become the de\-facto standard database for OLAP applications. Because the ClickHouse authors approached designing the database with a "bottoms\-up" approach, they are able to choose the data structures and algorithms to take full advantage of the capabilities of modern hardware.


At [RunReveal](https://runreveal.com/), we're using ClickHouse to build the fastest platform for security teams at all maturity levels to detect, respond and investigate incidents. Furthermore, because of its speed and efficiency, it allows teams to explore their infrastructure without the added worry of how much this query is going to cost you. Evan and I have got a few accidental multi\-thousand\-dollar athena queries under our belt now and we'd rather not have other people go through that experience.



> The more I learned about ClickHouse, the more I became convinced it will become the de\-facto standard database for OLAP applications.



## What makes ClickHouse fly? [\#](/blog/runreveal-is-building-the-ridiculously-fast-security-data-platform-on-clickhouse#what-makes-clickhouse-fly)


The Log Structured Merge Tree (LSM Tree) was invented in 1991 by Patrick O'Neil and is the fundamental storage data structure that gives ClickHouse its speed. LSM Trees are used by many prominent databases that existed before ClickHouse like [Bigtable](https://en.wikipedia.org/wiki/Bigtable), [HBase](https://en.wikipedia.org/wiki/HBase), [LevelDB](https://en.wikipedia.org/wiki/LevelDB), [Apache Cassandra](https://en.wikipedia.org/wiki/Apache_Cassandra), and [InfluxDB](https://en.wikipedia.org/wiki/InfluxDB). However, none of these databases are quite as easy to learn or use as ClickHouse.


Because ClickHouse is designed using a [bottoms\-up approach](https://presentations.clickhouse.com/bdtc_2019), it also integrates many optimizations taking full advantage of the hardware like making heavy use of SIMD instructions, ensuring data structures are CPU\-cache efficient, and using purpose built algorithms to solve the unique problems of processing data at massive scales.


![RunReveal1.png](/uploads/Run_Reveal1_c58b4427fd.png)
The difference is all in the packaging. ClickHouse is extremely simple to get started using for free. Download is a single binary or docker image. They prioritized making the database familiar to people having experience using relational/SQL databases, so the learning curve is drastically reduced relative to the existing NoSQL/big data databases. Bigtable and HBase both have SQL interfaces, but Bigtable is of course closed source, and HBase is a mess to operate.


## My Experience using ClickHouse [\#](/blog/runreveal-is-building-the-ridiculously-fast-security-data-platform-on-clickhouse#my-experience-using-clickhouse)


I saw the power of ClickHouse when we used it at Cloudflare. Cloudflare was a *very* early adopter, picking it up and kicking the tires on it almost immediately upon its first OSS release. Cloudflare runs ClickHouse on bare metal, which was good because ClickHouse was initially designed for running on hosts with directly\-attached SSDs. It wasn't until later that they began integrating support for blob storage.


At Segment, we had an ideal use case for ClickHouse building metrics and analytics for Segment's Protocols product, tracking counts over time for rule invocations, validation failures, and transformation results to help customers better understand the flow of their data.


Shipping ClickHouse at Segment [wasn't easy](https://www.youtube.com/watch?v=kuDvPz3xLCI) though. There was still no cloud product available off\-the\-shelf. Segment was transitioning to Kubernetes, and I wanted to deploy ClickHouse on Kubernetes due to the PersistentVolumeClaim abstraction which would easily enable us to colocate the storage on local SSDs using AWS's new (at the time) i3en instances which had ephemeral direct\-attached NVMe drives. If you haven't explored this instance type, they are very cost efficient. I highly recommend using them for deployments where you need fast direct\-attached drives.


![RunReveal2.png](/uploads/Run_Reveal2_70cc7b3c3b.png)
So after getting the project green lit, I took a stab at deploying ClickHouse on Kubernetes. Although I wasn't the first to do this, there can't have been many deployments of ClickHouse on nodes with ephemeral IP addresses, because I pretty quickly hit a bug in ClickHouse related to an [internal DNS cache of its replicas](https://github.com/ClickHouse/ClickHouse/issues/5287).


The ClickHouse team was very helpful and responsive. They quickly triaged and fixed the issue after I had found and presented the root cause of the issue. They've done a great job of managing the project even if it feels a bit chaotic at times. They move incredibly fast for such a large and ambitious project, yet the stable releases have rarely caused any issues or regressions in my experience.


## ClickHouse \+ RunReveal \= ❤️ [\#](/blog/runreveal-is-building-the-ridiculously-fast-security-data-platform-on-clickhouse#clickhouse--runreveal--%EF%B8%8F)


One defining feature of ClickHouse that truly makes it stand apart from the competition is their materialized views. Similar to materialized views in postgres, ClickHouse also incorporates persisting the result of the view queries to optimize retrievals that can fit any analytics or reporting based application.


At RunReveal we are storing log data which is a perfect use\-case for ClickHouse. We did initially explore alternatives to ClickHouse but seeing as I have familiarity with the database and they'd just launched the ClickHouse cloud service, the answer became quite obvious. No operational overhead for us, but we get to reap the benefit of all the great features they've built. Furthermore, ClickHouse is quickly becoming a great base\-level infrastructure to support AI/ML applications of which we fully intend to take advantage.


[RunReveal](https://runreveal.com/) is the ridiculously fast security data platform for threat detection and investigation that is easy to use, with a flexible deployment model, and provides instant value to companies at all maturity levels. If your security organization needs to search a lot of logs quickly, connect with us ([contact@runreveal.com](mailto:contact@runreveal.com)) and we’ll help you turn your security data into actionable insights.




> To learn more about how ClickHouse can help you improve performance and scalability while reducing costs, [try ClickHouse Cloud free for 30 days](https://auth.clickhouse.cloud/u/signup/).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
