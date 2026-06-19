# 10x speed, 10x savings: Constant Contact’s journey from Pinot to ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# 10x speed, 10x savings: Constant Contact’s journey from Pinot to ClickHouse

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 4, 2025 · 8 minutes read
div.w\-full \+ p, pre \+ p {
 text\-align: center;
 font\-style: italic;
}

For decades, [Constant Contact](https://www.constantcontact.com/) has been a household name among small and mid\-sized businesses looking to grow through email and digital marketing. Behind that steady, familiar presence is a quietly innovative company that’s kept pushing forward, rolling out new tools and channels to meet the changing needs of today’s small businesses.


That evolution put new demands on Constant Contact’s data platform. They needed real\-time event processing and interactive dashboards, without constant maintenance headaches.


At a [March 2025 ClickHouse meetup in Boston](https://clickhouse.com/videos/Boston-meetup-constant-contact), software engineer Abhijeet Kushe shared how Constant Contact rebuilt its real\-time analytics stack with ClickHouse, why it was such an improvement over their previous stack, and what the team learned along the way.


## The highs and lows of Apache Pinot [\#](/blog/pinot-to-clickhouse-constant-contact#the-highs-and-lows-of-apache-pinot)


In the fall of 2021, Constant Contact launched [Automated Path Builder (APB)](https://www.constantcontact.com/ca/features/email-marketing-automation), which helps customers engage contacts in real time with marketing workflows triggered by things like email opens, clicks, and order checkouts. The next summer, the company added SMS support, both for one\-off sends and as part of APB journeys. With these new features came more advanced reporting requirements and a need for real\-time, OLAP\-style queries.


A proof of concept with Apache Pinot showed promise. It supported upserts, integrated cleanly with Amazon Kinesis, and allowed for quick data fixes during rollout. Things ran smoothly at first, but by 2023, as data volumes increased, maintenance became more frequent.


![image1.png](/uploads/image1_382b5ce674.png)
*Event volume over time: dips during maintenance, steady growth after migrating to ClickHouse.*


One of the biggest problems was how Pinot handled upserts. At the time, it didn’t support compaction, so the system created a new segment every day. By the end of 2024, those segments had grown to a combined total of around 180 GB. “This forced us to add memory as the data grew,” Abhijeet says. Repartitioning wasn’t an option, since segments were tightly coupled to Kinesis shards. And without any tooling for bulk imports, restoring data could take weeks of non\-stop streaming.


It became clear the company needed a more reliable and scalable partner to help realize its objectives. “Time was running out,” Abhijeet says.


## Transitioning from Apache Pinot to ClickHouse [\#](/blog/pinot-to-clickhouse-constant-contact#transitioning-from-apache-pinot-to-clickhouse)


In 2024, the team began evaluating other OLAP databases. “We looked at ClickHouse, and it fit our requirements,” Abhijeet says. “With the Altinity ClickHouse operator and just a few lines of code, we were able to set it up within 15 or 20 minutes.”


To migrate their historical data, the team used AWS Athena CTAS queries to generate compressed JSON files in S3, then loaded the data directly into ClickHouse using the [s3 table function](https://clickhouse.com/docs/sql-reference/table-functions/s3). “ClickHouse has a great [bulk insert](https://clickhouse.com/docs/optimize/bulk-inserts) feature,” Abhijeet says. “We were able to load all our data in three hours, as opposed to the two or three weeks to load a new Pinot table.”


For real\-time updates, they used ClickHouse’s [ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree) engine, which offered similar behavior to Pinot’s upserts. The data types also mapped cleanly: ClickHouse supported everything they needed, and added even more flexibility with things like [UUIDs](https://clickhouse.com/docs/sql-reference/data-types/uuid) and [LowCardinality](https://clickhouse.com/docs/sql-reference/data-types/lowcardinality) strings.


They also used [clickhouse\-benchmark](https://clickhouse.com/docs/operations/utilities/clickhouse-benchmark), a simple but “extremely powerful” tool, to test queries and guide instance sizing and system design. Since ClickHouse’s [Java client](https://clickhouse.com/docs/integrations/java) mapped closely to their existing Pinot client, Abhijeet says, “It was very easy for me to migrate.”


In three months, Constant Contact was up and running on ClickHouse, with immediate results—including sub\-second response times on a single node and one thread. Pinot, by comparison, needed four servers and three brokers for the same throughput, and even then, some queries took 6\-7 seconds. “The difference was massive,” Abhijeet says.


## A closer look at ClickHouse vs. Pinot [\#](/blog/pinot-to-clickhouse-constant-contact#a-closer-look-at-clickhouse-vs-pinot)


Abhijeet didn’t sit back and simply admire the results. A self\-described “curious engineer,” he wanted to understand *why* ClickHouse was so much faster than Pinot. So he read some whitepapers and started unpacking the architectural differences between the two systems.


One of the biggest differences came down to how each system accesses data on disk. Pinot uses memory\-mapped (MMAP) files, which map segments directly into memory. While this approach can offer fast access under the right conditions, it comes with tradeoffs. Pinot’s segments often exceeded available RAM, leading to performance issues like TLB shootdowns and memory contention.


ClickHouse takes a different approach, using preads (position\-based reads) that “allow us to read the file from any position,” Abhijeet says. “This outperformed MMAP in all cases.” It also benefits from CPU\-level optimizations like prefetching and caching. “This allows ClickHouse to be way faster, whether it’s sequential or random reads,” he says.


Storage format was another big difference. ClickHouse is built on a [log\-structured merge tree (LSM) architecture](https://clickhouse.com/docs/academic_overview) designed for high\-ingest workloads. It handles SSTable merges natively, making upserts and compaction more predictable and reliable. “Pinot, on the other hand, needed a custom merging or compaction format,” Abhijeet says. The 180 GB of Pinot segments they’d accumulated by the end of 2024 was compacted down to a single 35 GB part in ClickHouse.


The two systems also differ in how they’re built. Pinot, written in Java, needed 16 GB of heap memory per process. ClickHouse, written in C\+\+, runs the same workloads with just 2 GB.


Finally, there was the matter of infrastructure. “Pinot is very component\-heavy,” Abhijeet explains. “There are brokers, servers, controllers, ZooKeeper.” ClickHouse is much lighter, requiring just a single server and [ClickHouse Keeper](https://clickhouse.com/clickhouse/keeper) to operate.


All of this added up to a huge difference in cost and performance. Constant Contact was paying nearly 10x the infrastructure cost per month for Pinot. “And with ClickHouse, performance is 10 times faster, too,” Abhijeet says.


## Lessons learned along the way [\#](/blog/pinot-to-clickhouse-constant-contact#lessons-learned-along-the-way)


Fifteen years ago, Abhijeet’s database professor gave him a piece of advice that stuck: “Know thy data.” It’s a simple mantra, but it paid off during Constant Contact’s migration from Pinot to ClickHouse.


Seemingly small design choices, like picking the right Int type or using enums instead of strings, can have a big impact. “Literally, 25% of compression comes for free with strong schema design,” Abhijeet says. “If your data design is perfect, then compression will be good.” He also emphasized the importance of [choosing the right primary key](https://clickhouse.com/docs/best-practices/choosing-a-primary-key) up front—a lesson he learned the hard way, after having to rebuild a table from scratch.


Another big takeaway: automate your backups, and test them. Previously, Constant Contact had to manually write a script to back up ZooKeeper every hour. But since migrating to ClickHouse, that process runs much smoother, with daily backups and routine restore tests to avoid surprises.


## A faster, more scalable database [\#](/blog/pinot-to-clickhouse-constant-contact#a-faster-more-scalable-database)


With ClickHouse, Constant Contact has a database that delivers blazing\-fast performance, a flexible architecture, and plenty of room to grow. The team can spend less time maintaining, and more time building the features that power the company’s best\-in\-class digital marketing tools.


As expectations around speed and personalization keep rising, Constant Contact has the technical foundation it needs to continue helping SMBs punch above their weight in an ultra\-competitive, digital\-first world.


To learn more about ClickHouse and see how it can improve the speed and scalability of your team’s data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
