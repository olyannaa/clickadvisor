# ClickHouse Cloud: Gumlet’s key to processing billions of video and image requests daily


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Cloud: Gumlet’s key to processing billions of video and image requests daily

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 19, 2024 · 9 minutes read
  



## Introduction [\#](/blog/gumlet-processing-billions-of-video-image-requests-with-clickhouse#introduction)


Every day, [Gumlet](https://www.gumlet.com/), a one\-stop media hosting and streaming solution, handles over 2 billion video and image requests for India's largest news organizations, e\-commerce companies, and social media platforms. Serving more than 100 million users per day, the platform is built to deliver content smoothly, reliably, and at lightning speed.


But fast delivery is only part of the story. Gumlet also tracks a variety of metrics like playback time, rebuffer rates, bandwidth usage, and more, helping customers fine\-tune performance and keep users engaged. Unlike simple web traffic metrics, video analytics is uniquely complex, requiring the capture and processing of temporal data in real\-time to account for behaviors like pauses, skips, and buffering. As Gumlet scaled, managing insights across 900 billion rows of data became an increasingly costly and complex challenge.


At a [September 2024 ClickHouse meetup in Bangalore](https://clickhouse.com/videos/tracking-1-billions-video-views-using-clickhouse), Gumlet co\-founder and CEO Aditya Patadia shared how migrating to [ClickHouse Cloud](https://clickhouse.com/cloud) helped the team overcome these challenges, transforming their analytics pipeline to support future growth.


## Challenges with BigQuery [\#](/blog/gumlet-processing-billions-of-video-image-requests-with-clickhouse#challenges-with-bigquery)


Initially, Aditya and the team relied on BigQuery to manage their analytics. Using a direct integration with their CDN provider, Fastly, the company could ingest and query data without any additional tooling. However, as Gumlet's operations scaled to billions of rows daily, they began to experience cracks in the system.


The most pressing issue, Aditya says, was spiraling costs. BigQuery's pricing model, based on ingestion and per\-query charges, became prohibitively expensive. "BigQuery has an ingestion cost when you're syncing data in real\-time, and every query adds to the expense," Aditya explains. "Anyone who has worked with BigQuery knows how quickly these costs can add up, depending on the type and volume of queries you fire."


Another issue was BigQuery's limit of 100 concurrent queries, which created bottlenecks for Gumlet's customers. "If our customers needed to fire more analytics API requests than that, they would fail or go into a queue," Aditya says. "We could have switched to a dedicated BigQuery plan, but that came with its own set of problems."


Storage costs added a further layer of complexity. BigQuery charged based on logical storage, which bills based on the data's theoretical size rather than its physical footprint, meaning Gumlet paid for the full size of every data point, even when the data was small or repetitive. For example, a simple HTTP status code like "200 OK," indicating a successful request, would be charged as 32 bytes. "When you're storing billions of these entries, the costs can quickly get out of control," Aditya says.


## A better data solution [\#](/blog/gumlet-processing-billions-of-video-image-requests-with-clickhouse#a-better-data-solution)


Realizing the limits of BigQuery, Aditya and the team began evaluating alternatives that could better handle their data needs. Their criteria were straightforward: scalable storage, fixed compute costs, exceptional documentation, and, preferably, no maintenance. "We're a relatively lean, remote team of 12 engineers, with no SRE or DevOps team," Aditya says. "We wanted something that would just fly, and that we wouldn't have to manage at all."


They looked at several options, including Athena, Redshift, Snowflake, and ClickHouse. Athena was ruled out early due its slow query speeds, while Redshift offered better performance but came with higher storage and computation costs. Meanwhile, Snowflake's "extremely costly" pricing made it a non\-starter for Gumlet's scale. "We tested Snowflake a little, but the pricing for the data sizes we had was just too high to explore further," Aditya says.


Ultimately, ClickHouse emerged as the best fit for Gumlet's needs. It offered scalable storage, predictable costs, and excellent performance. Plus, its documentation made it easy for Aditya and the team to get started without a steep learning curve.


After evaluating both the open\-source and managed versions, they opted for [ClickHouse Cloud](https://clickhouse.com/cloud). "We were one of the early customers when ClickHouse Cloud first launched," Aditya says. "It was self\-serve and easy to set up. We just went ahead with it and never looked back."


## Gumlet's new data architecture [\#](/blog/gumlet-processing-billions-of-video-image-requests-with-clickhouse#gumlets-new-data-architecture)


Migrating to ClickHouse wasn't simply a matter of swapping out one database for another. It required Aditya and the team to rethink their entire data pipeline.


The first step was redesigning the ingestion process. Previously, Gumlet relied on their CDN provider, Fastly, to push data directly into BigQuery. With the move to ClickHouse, they implemented a custom ingestion pipeline using a Golang\-based service to process and batch data before writing it to the database. ClickHouse works best with [large batch inserts](https://clickhouse.com/docs/en/optimize/bulk-inserts), so they optimized the pipeline to write 20,000 rows at a time. "This let us get the best performance while keeping insertion frequency high enough for real\-time analytics," Aditya says.


![Blog_Gumlet_202411_FNL.png](/uploads/Blog_Gumlet_202411_FNL_eb416eade7.png)
*Gumlet's new ClickHouse\-based analytics pipeline*


They also took advantage of ClickHouse's built\-in integrations to streamline other parts of their workflow. For instance, logs from their CDN and internal services, stored in AWS S3, could be ingested directly into ClickHouse using its [S3 import functionality.](https://clickhouse.com/docs/en/integrations/s3) This eliminated the need for complex ETL pipelines and made it easier to analyze billions of rows of log data.


Query performance was another area of focus. The team used ClickHouse's [materialized views](https://clickhouse.com/docs/en/materialized-view) to pre\-aggregate data for common analytics requests, such as playback metrics and rebuffer rates. As Aditya explains, materialized views gave them the ability to pre\-compute results and serve real\-time dashboards without adding latency.


## The benefits of ClickHouse [\#](/blog/gumlet-processing-billions-of-video-image-requests-with-clickhouse#the-benefits-of-clickhouse)


For Aditya and the Gumlet team, migrating to ClickHouse has brought a number of big\-time improvements, ranging from cost to performance and scalability.


One of the most important wins was cost predictability. Unlike BigQuery's variable per\-query pricing model, ClickHouse Cloud offers fixed compute costs, with only storage costs tied to usage. "We know what we're going to get charged for compute month to month, which is very important, because that's the costly part, not storage," Aditya says.


Another big benefit has been improvements in ingestion speed. By processing batch inserts efficiently and taking advantage of ClickHouse's S3 integration, they've eliminated the need for complex ETL processes. "Since moving to ClickHouse, we just throw everything at it, and it handles it all in less than two minutes," Aditya says.


Aditya also highlights the rapid response times since switching to the new system, with no limits on the number of concurrent queries. "We can run, like, 500 queries in one go, and it handles them really quickly — within two or three seconds, not minutes," he says. "It's the fastest database in the world. You can't argue with that."


Finally, as a managed service, ClickHouse Cloud has simplified Gumlet's operations, helping them offload tasks like scaling, replication, and backups. This frees up valuable engineering resources and lets the team focus entirely on improving their product.


## Lessons learned [\#](/blog/gumlet-processing-billions-of-video-image-requests-with-clickhouse#lessons-learned)


While Gumlet's migration to ClickHouse was a success, like any major change it came with a few learnings, which Aditya shared for anyone considering a move to ClickHouse.


One of these was the need to adapt tools and workflows to fit the new system. For instance, Gumlet decided to switch to Metabase for their business intelligence (BI) needs, as ClickHouse lacks native support for their previous BI tool, Google Data Studio. Similarly, not all ETL tools support ClickHouse at the moment, so the team had to choose alternatives that were compatible with their data processing needs.


The migration also highlighted the importance of schema design. "ClickHouse requires careful planning upfront, especially for primary keys," Aditya says. "Changing a primary key later on means dropping and recreating the table, so it's important to get it right the first time." He also highlights the value of ClickHouse features like [LowCardinality](https://clickhouse.com/docs/en/sql-reference/data-types/lowcardinality) and [Delta compression](https://clickhouse.com/docs/en/data-compression/compression-in-clickhouse#choosing-the-right-column-compression-codec) for improving query performance and lowering storage costs.


Lastly, the team identified a few technical considerations, such as switching from DateTime64 to standard DateTime for better performance in large databases. While these adjustments required some upfront effort, they contributed to a more efficient and cost\-effective data pipeline.


## Video analytics without limits [\#](/blog/gumlet-processing-billions-of-video-image-requests-with-clickhouse#video-analytics-without-limits)


Gumlet's journey to ClickHouse has been transformative, helping the company scale their analytics capabilities while maintaining cost efficiency, predictability, and performance.


By reimagining their data architecture and tapping into ClickHouse Cloud's advanced features, Aditya and the team have built a pipeline capable of processing billions of rows of data daily. From faster ingestion to lightning\-quick query responses, the migration means Gumlet can deliver actionable, real\-time insights that help its customers optimize performance.


With ClickHouse powering its analytics, Gumlet has the flexibility and performance to keep growing while staying true to its mission of providing the fastest and most reliable video hosting and streaming services to customers across India.


To learn more about ClickHouse and discover how it can transform your company's data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/blog/clickhouse-cloud-generally-available).

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
