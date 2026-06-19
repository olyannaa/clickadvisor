# Why Flock Safety turned to ClickHouse for real\-time vehicle traffic analytics


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Why Flock Safety turned to ClickHouse for real\-time vehicle traffic analytics

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Apr 29, 2025 · 7 minutes read
[Flock Safety](https://www.flocksafety.com/) is on a mission to make communities safer. Founded in Atlanta in 2017, their products include automated license plate readers, video cameras, and gunfire detection systems, all designed to deter crime and aid criminal investigations. Today, Flock Safety serves over 5,000 communities nationwide, with customers ranging from law enforcement agencies to neighborhood associations to major businesses.




Beyond hardware, the company offers a suite of software solutions, including a [traffic analytics platform](https://www.flocksafety.com/traffic-analytics-business) that builds on their popular license plate recognition technology. It provides aggregated vehicle counts, delivering insights to help customers optimize security staffing, operations, and traffic safety. 




“This unlocks a lot of potential for customers to look at insights based on the images that their cameras are capturing,” says Leon Kozlowski, data engineering manager at Flock Safety.




But scaling any data platform comes with challenges, like long refresh times, size constraints, and data availability.




At a [December 2024 ClickHouse meetup in New York City](https://www.youtube.com/watch?v=dN4yrzn8Td4), Leon described Flock Safety’s search for a better data architecture — a journey that led them to [ClickHouse Cloud](https://clickhouse.com/cloud).



## The analytics bottleneck [\#](/blog/why-flock-safety-turned-to-clickhouse#the-analytics-bottleneck)



Flock Safety’s original analytics pipeline relied on Amazon Redshift, DBT, and Prefect, with Amazon QuickSight’s SPICE layer handling dashboards. Data was shared from a provisioned Redshift cluster to a Redshift Serverless instance, where DBT and Prefect transformed it into analytics models. From there, the processed data was synced into SPICE, an in\-memory database that powered QuickSight reports. While this setup offered a structured way to process large volumes of data, it came with limitations that made real\-time insights impossible.






![FS1.png](/uploads/FS_1_b8ad7ac621.png)

Flock Safety’s pre\-ClickHouse data architecture.





The first challenge was the daily refresh cadence. “The transformation layer only ran once a day, both because of the volume of data and the way our architecture was designed to surface that data to customers,” Leon says. This meant customers could only see updates from the previous day or earlier. “They had no intraday context into their data,” he adds.




Then came the issue of long refresh times. Syncing data into SPICE was slow, with some datasets taking up to four hours to process. “This was probably the biggest issue with the old architecture,” Leon says. During that window, data was completely unavailable, leaving customers stuck with outdated information. As a workaround, the team ran refreshes overnight to minimize disruptions, but as Leon notes, “That type of downtime is really not going to be tolerated, especially for law enforcement customers.”




Size constraints compounded the problem. SPICE had a hard limit of 1TB or 1 billion rows per dataset. Customers weren’t just missing real\-time updates — they were losing valuable historical insights.



## The search for a better architecture [\#](/blog/why-flock-safety-turned-to-clickhouse#the-search-for-a-better-architecture)



Recognizing the limitations of their existing setup, Leon and the team set out to find an architecture that could support real\-time analytics at scale without sacrificing performance.




They first explored running direct queries on Redshift instead of syncing data into SPICE. The goal was to speed up queries by removing the in\-memory later. However, as Leon points out, “The concurrency limits on Redshift meant this wasn’t a scalable approach.”




Next, they tested Aurora PostgreSQL, thinking its transactional capabilities might offer better performance. The idea was to sync data from Redshift into Aurora and run QuickSight queries directly. But the results were even worse: “This wasn’t even able to return data to the caller within the timeout specified by Amazon QuickSight,” Leon explains. If a query couldn’t return results without timing out, it wasn’t a viable solution for Flock Safety’s customers.




They then turned to S3 and Trino, attempting to use Trino’s federated queries on data stored in S3\. This approach took some “funky partitioning” to optimize query performance, but even with aggressive tuning, the system still struggled under load. Like Aurora, Trino queries frequently exceeded timeout limits. After testing multiple configurations, Leon says that “these three options definitely were not viable for the SLA we want to provide to our customers.”




Finally, they turned to ClickHouse. With its [AggregatingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree) tables and [materialized views](https://clickhouse.com/docs/en/materialized-view), the database provided “real\-time data with direct queries to ClickHouse, rather than using SPICE,” Leon says. The difference could be seen right away: queries were fast, data was available at all times, and they could extend retention without worrying about in\-memory constraints. After a rigorous POC, ClickHouse was the clear winner.



## Flock Safety’s new data pipeline [\#](/blog/why-flock-safety-turned-to-clickhouse#flock-safetys-new-data-pipeline)



Flock Safety’s new ClickHouse\-based architecture starts with ingestion. Images captured by the company’s cameras are sent to the cloud, where machine learning models extract metadata such as vehicle type, make, and license plate state. This information is then pushed to Amazon Simple Notification Service (SNS), which triggers Amazon Kinesis Data Firehose to deliver the structured data into Amazon S3\. At the same time, transactional data from RDS databases is streamed via Debezium into the same S3 storage layer. 




From there, [ClickPipes](https://clickhouse.com/cloud/clickpipes) ingests data into ClickHouse. “It’s extremely performant, with very low latency,” Leon says of ClickPipes. “This architecture has been very scalable in getting data into ClickHouse.” At its peak, ClickPipes processes over 20 MB per second, allowing Flock Safety’s traffic analytics platform to handle over 1 billion ML predictions per day with zero downtime.






![FS2.png](/uploads/FS_2_71691c1bbb.png)


Data ingestion in Flock Safety’s new ClickHouse\-based architecture.




Data transformation occurs automatically upon ingestion into ClickHouse. ML predictions are inserted into dedicated tables, and materialized views use [AggregateFunction](https://clickhouse.com/docs/en/sql-reference/data-types/aggregatefunction) data types with functions like uniqState to precompute key metrics for simpler queries. “This means there’s no more need for DBT or Prefect to orchestrate any of these transformations,” Leon says. Aggregated data is then stored in AggregatingMergeTree destination tables, supporting fast, real\-time queries without the need for batch processing.




From there, the data is enriched with additional context. [ReplacingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree) dimension tables store metadata like camera locations and organization\-level access rules. With this structure, Amazon QuickSight queries ClickHouse directly, bypassing SPICE’s limitations and ensuring that users always see the most up\-to\-date information.






![FS3.png](/uploads/FS_3_dcfa9ecffd.png)


ClickHouse’s table structure and integration with Amazon QuickSight.




Flock Safety’s transition to ClickHouse was surprisingly smooth, Leon says, thanks to its compatibility with existing ingestion processes. “If anything, the challenge was getting ramped up on table architectures like ReplacingMergeTree and AggregatingMergeTree, but we got a lot of help from Jake, Larry, Shri, and the ClickHouse Cloud team.”



## Real\-time insights, safer communities [\#](/blog/why-flock-safety-turned-to-clickhouse#real-time-insights-safer-communities)



Switching from Redshift to ClickHouse Cloud has delivered huge benefits for Flock Safety’s traffic analytics platform. Removing SPICE eliminated downtime, giving customers 24/7 access to the latest data. Now, instead of waiting for daily refreshes, customers can see real\-time traffic trends as they happen. Queries that once took minutes now complete in under five seconds, even for the platform’s largest customers.




ClickHouse has also unlocked long\-term data retention. With ClickHouse Cloud’s scalable architecture, they can store significantly more traffic count data, giving customers richer insights and deeper trend analysis.




Leon describes the difference as night and day. “With ClickHouse, our customers now have real\-time analytics for their camera traffic, and there are no more constraints on size or row\-level security.” With a scalable, high\-performance database, Flock Safety can keep expanding its analytics capabilities, helping communities stay safer with smarter, data\-driven decisions.




To learn more about ClickHouse and see how it can improve the speed and scalability of your team’s data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).


Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
