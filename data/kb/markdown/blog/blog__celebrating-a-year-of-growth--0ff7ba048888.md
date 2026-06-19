# Celebrating a Year of Growth


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Celebrating a Year of Growth

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 19, 2023 · 5 minutes readAs the year draws to a close, we wanted to express our heartfelt gratitude to you for being part of the ClickHouse Cloud journey. Your support has been instrumental in shaping an incredible year of growth, and we’re excited to take a moment to reflect on some of the milestones that made 2023 such a remarkable year. 


## Launch \& Platform Expansion [\#](/blog/celebrating-a-year-of-growth#launch--platform-expansion)


We launched [ClickHouse Cloud](https://clickhouse.com/blog/clickhouse-cloud-generally-available) on AWS in December 2022 \- just over a year ago today. Six months later, in June 2023, , we expanded our availability to [Google Cloud](https://clickhouse.com/blog/clickhouse-cloud-on-google-cloud-platform-gcp-is-generally-available) in three geographies, with Azure support in the works for 2024\. Since then, we’ve continued rolling out new region support, with [12 available](https://clickhouse.com/docs/en/cloud/reference/supported-regions) across platforms today. 


We introduced a new service type \- [Dedicated Instances](https://clickhouse.com/pricing), designed for customers who are looking for advanced isolation and protection of data, as well as predictable performance. This service type provides maximal flexibility when it comes to configurations, to ensure the setup is the right fit for your workload. With a Dedicated Service, customers also have the flexibility to define maintenance windows for upgrades. If you’re interested in learning more, please [let us know!](https://clickhouse.com/company/contact)


![map-regions.png](/uploads/map_regions_a4af1bd92a.png)
## Scale and Performance Optimizations [\#](/blog/celebrating-a-year-of-growth#scale-and-performance-optimizations)


Throughout 2023, we made several performance improvements and optimizations to ClickHouse, including the introduction of a brand\-new Engine, SharedMergeTree (SMT). [SharedMergeTree](https://clickhouse.com/docs/en/cloud/reference/shared-merge-tree) is optimized for shared storage, the basis for our ClickHouse Cloud architecture, and results in significantly improved insert throughput and background operations performance compared to our other Engines. We haven’t forgotten about our scaling algorithms, either! We’ve made diligent enhancements across vertical, horizontal, and CPU\-based scaling, too.


## Analyst Productivity [\#](/blog/celebrating-a-year-of-growth#analyst-productivity)


We’ve introduced several new capabilities to our SQL Console experience that make writing and debugging queries a lot smoother.


![compressed_cut_rag_c420958463.gif](/uploads/compressed_cut_rag_c420958463.gif)
AI\-based Query Suggestions


We additionally released API support to programmatically manage your ClickHouse Cloud lifecycle operations, as well as a [Terraform Provider](https://registry.terraform.io/providers/ClickHouse/clickhouse/latest) to ease deployment automation.


## Integrations [\#](/blog/celebrating-a-year-of-growth#integrations)


It has been a busy year on the integrations front!


In September, we announced the general availability of [ClickPipes](https://clickhouse.com/cloud/clickpipes), a turnkey data ingestion service for ClickHouse Cloud. Initially focused on streaming data with support for Apache Kafka, Confluent Cloud, and Amazon MSK, we are currently working on expanding the list of available connectors to include more data sources.


Our 2023 integrations milestones included ClickHouse ecosystem focused releases, such as:


- GA of our official [Kafka Connect Sink](https://github.com/ClickHouse/clickhouse-kafka-connect)
- Support for the [MySQL protocol in ClickHouse Cloud](https://clickhouse.com/blog/clickhouse-cloud-compatible-with-mysql) (read more about our [behind the scenes journey here](https://clickhouse.com/blog/mysql-support-in-clickhouse-the-journey))
- Improved and upgraded [ClickHouse dbt adapter](https://github.com/ClickHouse/dbt-clickhouse)
- Several enhancements to the [Python](https://github.com/ClickHouse/clickhouse-connect), [JS](https://github.com/ClickHouse/clickhouse-js), [Golang](https://github.com/ClickHouse/clickhouse-go), and [Java](https://github.com/ClickHouse/clickhouse-java) language clients
- Improvements to plugins including [Grafana](https://clickhouse.com/blog/introduction-to-clickhouse-and-grafana-webinar), [Metabase](https://clickhouse.com/blog/metabase-clickhouse-plugin-ga-release), [Superset](https://clickhouse.com/blog/visualizing-data-with-superset), [PowerBI Desktop (Beta)](https://github.com/ClickHouse/power-bi-clickhouse), and more


## Security [\#](/blog/celebrating-a-year-of-growth#security)


Our continued commitment to data privacy and security is central to every part of our business and has driven significant ClickHouse milestones this year. 


Data at Rest Protection: We introduced support for Customer Managed Encryption Keys (CMEK) for custom data\-at\-rest encryption and key rotation. This is available for production services deployed in AWS. 


Endpoint Security: We released support for secure endpoints with Private Link in AWS and Private Service Connect in GCP.


S3 Access Security: We've enhanced security by enabling secure access to private S3 buckets using AWS assumed IAM roles.


Compliance: ClickHouse Cloud is certified for SOC 2 Type II and ISO 27001\. You can read more on our compliance and certifications [here](https://clickhouse.com/docs/en/manage/security/compliance-and-certification), and request access to these reports in our [ClickHouse Trust Center.](https://trust.clickhouse.com)


## Cloud Change Log [\#](/blog/celebrating-a-year-of-growth#cloud-change-log)


And that’s not all! We have several other releases and improvements that you can read about on our [change log](https://clickhouse.com/docs/en/whats-new/cloud).


## Customer Spotlights [\#](/blog/celebrating-a-year-of-growth#customer-spotlights)


“At Lyft, we ingest tens of millions of rows and execute millions of read queries in ClickHouse daily with volume continuing to increase. On a monthly basis, this means reading and writing more than 25TB of data.” [Read more](https://eng.lyft.com/druid-deprecation-and-clickhouse-adoption-at-lyft-120af37651fd) about Lyft’s migration to ClickHouse.


“We had prototyped something in BigQuery … but we were seeing 15, 20, 25 second response times.” Hear about how [Clearbit achieved a 10x cost reduction](https://clickhouse.com/videos/clearbit) moving from Postgres to ClickHouse, and how their evaluation of BigQuery as a solution was resulting in double digit response times.  


"Moving over to ClickHouse we were basically able to cut that (Redshift) bill in half." Brooke, Co\-founder and CTO of Vantage, shares how [transitioning to ClickHouse](https://clickhouse.com/videos/vantage) not only optimized Vantage's operations but also dramatically reduced their costs.


## Continued Reading [\#](/blog/celebrating-a-year-of-growth#continued-reading)


- [The Unbundling of the Cloud Data Warehouse](https://clickhouse.com/blog/the-unbundling-of-the-cloud-data-warehouse)
- [The State of SQL\-based Observability](https://clickhouse.com/blog/the-state-of-sql-based-observability)
- [Escape from Snowflake's Costs](https://clickhouse.com/blog/escape-rising-costs-of-snowflake-speed-and-cost-savings-clickhouse-cloud)


With that, we want to close by extending our deepest appreciation for your support and partnership this year. We couldn't have asked for a better community to grow with. 


We hope you have a wonderful and joyous holiday season! 


**Has your ClickHouse Cloud trial ended, but you still have more to explore? [Let us know](/company/contact?loc=year-in-review-2023) and we'll extend your FREE trial.**

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
