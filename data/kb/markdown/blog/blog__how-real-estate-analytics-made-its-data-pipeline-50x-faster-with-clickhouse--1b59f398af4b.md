# How Real Estate Analytics made its data pipeline 50x faster with ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Real Estate Analytics made its data pipeline 50x faster with ClickHouse

![](/_next/image?url=%2Fuploads%2Fsam_lee_922a1bf3fd.jpg&w=96&q=75)Yi Sam LeeApr 24, 2025 · 8 minutes read[Real Estate Analytics (REA)](https://rea-global.com/) is on a mission to transform Asia’s property market. Founded in Singapore in 2019, the company operates in Australia, Hong Kong, and Malaysia, using advanced data science and machine learning to provide solutions for governments, financial institutions, developers, real estate professionals, and more.


But as their datasets grew \- spanning over 200 columns and up to 20 million rows \- REA’s MongoDB\-based architecture struggled to keep up. Table refreshes took 30 minutes, and query performance lagged, making it hard to deliver real\-time insights to customers.


At a [February 2025 ClickHouse meetup in Singapore](https://clickhouse.com/videos/singapore-meetup-real-estate-analytics-clickhouse-journey), REA’s Data Lead, Yi Sam Lee, shared how the team turned to ClickHouse to break through these bottlenecks. "ClickHouse saved us from quite a number of headaches" he says. "And to our pleasant surprise, we actually discovered it did more than what we needed".



## MongoDB design limits [\#](/blog/how-real-estate-analytics-made-its-data-pipeline-50x-faster-with-clickhouse#mongodb-design-limits)


In early 2024, one of Sam's product managers came to him with a request. Instead of predefining columns for customer queries, the PM wanted REA's users to have control over which columns to query \- meaning REA needed to make more than 200 columns available for slicing and dicing. The dataset, Sam says, was "a bit scary but manageable," ranging from 3 to 20 million rows. The bigger problem, he explains, was the frequency of updates.


"Out of the 200 columns available, we want to change some of them, and we need it pretty regularly" Sam recalls his PM saying. "That's when my nightmare started to take shape."


At the time, REA's architecture relied on MongoDB as its primary database. While it handled point searches well with indexes, it struggled with aggregations and large\-scale updates. Worse, each additional index added roughly 10% to the refresh time. With a dataset as complex as REA's, a full table refresh took between 25 and 30 minutes \- "clearly not acceptable" for a product marketed as interactive and frequently updated, Sam says.


Sam and his team had optimized the database as much as possible, working with MongoDB engineers to fine\-tune performance. But no matter how much they tweaked it, the fundamental issue remained: performance tradeoffs were unavoidable. "If our PM got too creative, we'd be spending a lot of time waiting for table refreshes" Sam says.


## 50x faster with ClickHouse [\#](/blog/how-real-estate-analytics-made-its-data-pipeline-50x-faster-with-clickhouse#50x-faster-with-clickhouse)


In July of that year, Sam attended a ClickHouse meetup in Singapore. He wasn’t necessarily looking for a replacement database \- just a way to make MongoDB better. But as he listened to other engineers discuss ClickHouse’s speed and efficiency for analytical workloads, he started to wonder if it could be the answer to his problem.


The numbers were compelling. ClickHouse was built for fast aggregations and large\-scale analytics, with a [columnar architecture](https://clickhouse.com/docs/en/faq/general/columnar-database) optimized for high\-dimensional data. Unlike MongoDB, where indexing came with tradeoffs, ClickHouse could handle massive datasets efficiently without the performance downgrades REA was struggling with.


Soon after that meetup, Sam and his team ran a proof of concept. Their first test was simple: could ClickHouse handle the same aggregation queries REA had optimized in MongoDB? The answer was a resounding yes. Queries that had taken several seconds in MongoDB ran 10 times faster in ClickHouse. But the real breakthrough came when they tested table refresh speeds. With MongoDB, a full refresh took up to half an hour. In ClickHouse, the same operation finished in under 30 seconds \- a 50x improvement.


This meant REA no longer had to choose between performance and flexibility. Their PM could adjust the available columns as often as needed, and customers could explore the dataset dynamically without waiting for slow updates.



> "ClickHouse was performant enough for us to keep our PM’s wishlist without breaking the system"
> 
> Yi Sam Lee, REA Data Lead


## A more efficient pipeline [\#](/blog/how-real-estate-analytics-made-its-data-pipeline-50x-faster-with-clickhouse#a-more-efficient-pipeline)


With their slicing and dicing challenges behind them, Sam and the REA team turned their attention to using ClickHouse to optimize data ingestion and transformation.


Their previous pipeline relied on Apache Kafka and a series of containerized consumers to process incoming data before storing it in MongoDB. While this setup worked, ClickHouse gave them a more streamlined approach by removing intermediate processing layers.


![real-estate-analytics.png](/uploads/real_estate_analytics_38b7c2f097.png)
*REA’s old data pipeline (left) and new ClickHouse\-based pipeline (right)*


Instead of routing data through multiple steps, REA redesigned the pipeline to pull in data from web sources (e.g. government databases, property listings), store it in an S3 bucket, and ingest it into ClickHouse.



> "The new architecture saved us quite a number of resources, both in terms of money and development effort"
> 
> Yi Sam Lee, REA Data Lead


Sam highlights several ClickHouse features that made extraction and parsing more efficient. One was its [globs and path functions](https://clickhouse.com/docs/sql-reference/table-functions/file) for batch processing files. Another was its ability to read compressed zip files without extracting them. "We store a lot of zip files in our bronze layer" Sam explains. "Extracting them is possible, but it costs money. With ClickHouse, we can read data directly from the zip file without extracting it."


ClickHouse’s [S3 table function](https://clickhouse.com/docs/sql-reference/table-functions/s3) also proved "very handy" according to Sam. "You can write data directly from ClickHouse to S3 and structure it efficiently, partitioning it into different files as needed" he says. This allowed REA to store data in a structured way without extra ETL jobs.


Parsing structured and semi\-structured data was another area where ClickHouse made a difference. Its native support for JSON parsing and regex\-based extraction meant REA could process raw data directly in ClickHouse, eliminating the need for external transformation jobs. Sam notes that ClickHouse’s SQL\-based approach made adoption much easier overall. "It meant more of our developers could work with ClickHouse right away" he says.


## Tradeoffs and use cases [\#](/blog/how-real-estate-analytics-made-its-data-pipeline-50x-faster-with-clickhouse#tradeoffs-and-use-cases)


While ClickHouse has solved many of REA’s challenges, there are a few gaps they’ve had to work around. One is its handling of historical dates. By default, ClickHouse’s Date type only supports dates from 1970 onward. Even with DateTime64, the lower limit is 1900\. This poses a problem for REA, since property records can stretch back to the 1800s.


Another is spatial data support. Real estate analytics depends on precise location\-based insights. REA needed a way to handle geographic data within ClickHouse, but while ClickHouse offers some support for geometry queries, the lack of native WKT (Well\-Known Text) format support makes visualizing spatial data in tools like DBeaver more difficult.


Finally, in Postgres, REA relies on automatically incrementing IDs for certain workflows, a feature ClickHouse [didn’t natively support at the time](https://clickhouse.com/blog/clickhouse-release-25-01). While "not a showstopper" Sam says, it means they’ve had to adjust how they handle unique identifiers in their pipeline.


Despite these challenges, Sam was eager to share REA’s data journey at the Singapore meetup. He presented three live demos showing ClickHouse in action, including how REA scrapes and processes real estate listings using ClickHouse’s URL engine, how they ingest and analyze government open data from sources like data.gov.sg, and how they store and query structured datasets directly in ClickHouse without additional ETL steps.


If you're interested in seeing these demos firsthand, you can [watch a full recording of Sam’s presentation](https://clickhouse.com/videos/singapore-meetup-real-estate-analytics-clickhouse-journey) at the February 2025 ClickHouse meetup in Singapore.


## Scaling with ClickHouse [\#](/blog/how-real-estate-analytics-made-its-data-pipeline-50x-faster-with-clickhouse#scaling-with-clickhouse)


For Sam and the team, ClickHouse has fundamentally changed how REA processes and analyzes data. Queries that once took half an hour now run in seconds, while their data pipeline is leaner, faster, and more cost\-effective.


"ClickHouse has helped us and solved a lot of our problems" Sam says. Compared to their old setup with MongoDB and Kafka, he has found ClickHouse "quite easy to set up and easy to use." He also shouts out ClickHouse’s open\-source community and documentation. "There’s a lot of great content that shares how to use ClickHouse. I'm very happy for that."


With a faster, more scalable foundation in place, REA is set to keep pushing real estate analytics forward. By making property market data easier to access and act on, they're helping businesses, governments, and real estate professionals make smarter decisions. And with ClickHouse as the core of their stack, they’re ready to scale even further.


To see how ClickHouse can transform your company's data operations, [try ClickHouse Cloud free for 30 days](https://clickhouse.com/cloud).

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
