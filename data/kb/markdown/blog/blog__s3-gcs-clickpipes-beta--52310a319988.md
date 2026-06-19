# ClickPipes for Batch Data Loading: Introducing S3 and GCS Support


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickPipes for Batch Data Loading: Introducing S3 and GCS Support

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene)Apr 18, 2024 · 4 minutes read## Introduction [\#](/blog/s3-gcs-clickpipes-beta#introduction)


Building on the success of [ClickPipes for Kafka](https://clickhouse.com/blog/clickpipes-is-generally-available), we're thrilled to announce the expansion of our connectivity platform with new connectors for Amazon S3 and Google Cloud Storage (GCS), currently in beta.


![1.png](/uploads/1_19f50881f7.png)
## Large bulk data loading [\#](/blog/s3-gcs-clickpipes-beta#large-bulk-data-loading)


Loading billions (or [trillions](https://clickhouse.com/blog/clickhouse-1-trillion-row-challenge)!) of rows from scratch into a ClickHouse service can pose certain challenges due to the time\-consuming nature of the task. The longer the process takes, the greater the risk of encountering transient issues such as network glitches that could halt or disrupt the data loading. An interruption can also lead to leaving the destination tables in a partial state that can be tricky to recover from. The new ClickPipes object storage connectors for Amazon S3 and Google Cloud Storage (GCS) were designed to tackle these obstacles and ensure a smooth data loading process without interruptions, no matter how much data is ingested.


The key behind the resiliency of these data loading tasks resides in the smart and efficient use of the ClickHouse destination service ingest capabilities, a tailored orchestration leveraging temporary staging tables that offer atomic units of data management for repeatability, a custom [KeeperMap](https://clickhouse.com/docs/en/engines/table-engines/special/keeper-map) state that allow to track the progress and pause/resume the task, and the resilient ClickPipes underlying infrastructure. If you are curious, you can learn more about the core logic behind the feature in our post about [ClickLoad](https://clickhouse.com/blog/supercharge-your-clickhouse-data-loads-part3#the-core-approach), an open\-source python script implementing a similar orchestration approach.


![2.png](/uploads/2_5647202141.png)
## Continuous loading [\#](/blog/s3-gcs-clickpipes-beta#continuous-loading)


In the beta phase, the ClickPipes connectors for S3 and GCS will offer the capability of bulk data loading. An ingest task will load all the files matched by a [pattern](https://clickhouse.com/docs/en/integrations/clickpipes#s3--gcs-clickpipe-limations) from a specific remote bucket into the ClickHouse destination table. Note that ClickPipes will skip files larger than 1 GB for efficiency reasons, we recommend splitting larger files into 1 GB chunks.


![s3_CP.gif](/uploads/s3_CP_ad92afc7ab.gif)
Once all the data is successfully inserted in the destination table, the ClickPipe object storage connector will reach a “completed” state. In the GA release, we will enable the “continuous mode,” where the ClickPipes job will be running constantly, ingesting matching files that get added into the remote object storage bucket as they arrive. This will allow users to turn any object storage bucket into into a fully fledged staging area for ingesting data into ClickHouse Cloud.


![4.png](/uploads/4_7b53b840b3.png)
![5.png](/uploads/5_8095c9bfd9.png)
## Supported formats and authentication [\#](/blog/s3-gcs-clickpipes-beta#supported-formats-and-authentication)


In this beta release, the object storage connectors support JSON, CSV, TSV, and Parquet formats (as well as their compressed counterparts). For authentication methods, ClickPipes supports public object storage buckets and private buckets with credentials\-based authentication (AWS Access Key ID and Secret or Google HMAC keys). IAM role\-based authentication is also available for Amazon S3 buckets.


## Give it a spin today! [\#](/blog/s3-gcs-clickpipes-beta#give-it-a-spin-today)


Starting today, you can access the new object storage beta connectors in your ClickPipes menu (under Data Sources \> ClickPipes). You can use it with your own S3 bucket or use the following test file hosted on our public bucket for a quick test (69 MB):



```
https://datasets-documentation.s3.eu-west-3.amazonaws.com/github/github-2022-flat.ndjson.gz

```

![6.png](/uploads/6_07d27aaf60.png)
The documentation and more details about how to get started can be found [here](https://clickhouse.com/docs/en/integrations/clickpipes). As always, we’d love to hear your feedback and suggestions ([contact us](https://clickhouse.com/company/contact?loc=clickpipes-s3-beta-blog)). Stay tuned for more updates and enhancements as we continue to evolve ClickPipes into the ultimate connectivity platform for ClickHouse Cloud.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
