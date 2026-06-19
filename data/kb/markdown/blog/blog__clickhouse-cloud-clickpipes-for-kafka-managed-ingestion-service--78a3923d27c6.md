# ClickPipes for Kafka \- ClickHouse Cloud Managed Ingestion Service


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickPipes for Kafka \- ClickHouse Cloud Managed Ingestion Service

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene)Jul 18, 2023 · 5 minutes readToday at ClickHouse, we are delighted to announce the release of ClickPipes for Kafka.
This new ClickHouse Cloud experience enables users to simply connect to remote Kafka brokers and start ingesting data into their ClickHouse services right away. This new feature unlocks the full potential of ClickHouse Cloud and enables users to leverage near real\-time data for insights and analytics.


ClickPipes is a native capability of ClickHouse Cloud currently under private preview. You can [join our waitlist here](https://clickhouse.com/cloud/clickpipes#joinwaitlist).



## “Real\-time Analytics ❤️ Real\-time Data” [\#](/blog/clickhouse-cloud-clickpipes-for-kafka-managed-ingestion-service#real-time-analytics-%EF%B8%8F-real-time-data)


Apache Kafka is a ubiquitous event streaming platform that thousands of companies use for high\-performance data pipelines, streaming analytics, data integration, and mission\-critical applications, often in conjunction with ClickHouse. For these reasons, it was obvious for us that we should start by providing world\-class Kafka Support in ClickPipes.


![choose_datasource.png](/uploads/choose_datasource_70485c8655.png)
For this task, we worked closely with our friends at Confluent, through the Connect with Confluent program (CwC). As the leading enterprise Kafka provider, Confluent offers a fully\-managed cloud environment where users can deploy and operate Kafka clusters, Kafka Connect connectors and more.


We announced earlier this year the availability of our official [clickhouse\-kafka\-connect](https://clickhouse.com/blog/kafka-connect-connector-clickhouse-with-exactly-once) sink and we demonstrated using it in Confluent Cloud via the [custom connectors feature](https://clickhouse.com/blog/real-time-event-streaming-with-kafka-connect-confluent-cloud-clickhouse). With ClickPipes, we effectively take this integration path one step further, and provide a native “zero setup” experience to integrate ClickHouse and Confluent Cloud.


## Why another ingestion solution? [\#](/blog/clickhouse-cloud-clickpipes-for-kafka-managed-ingestion-service#why-another-ingestion-solution)


Valuable insights extracted from real\-time analytics applications often depend on the availability of fresh and good quality input data. It’s not uncommon for users to spend a considerable amount of time and effort building and maintaining a sophisticated ingestion layer for their application. This critical component can quickly grow in complexity and will condition the value of the whole data chain.


With Clickhouse, users can rely on a [vibrant ecosystem of integrations](https://clickhouse.com/docs/en/integrations) for this task. But spending time moving data from point A to point B means they are left with less time to focus on the use\-case itself and extracting value from data.


With ClickPipes, we abstract this complexity away by providing a turnkey data ingestion experience. Setting\-up a continuous ingestion job with ClickPipes takes less than a minute.


![clickpipes_1mn.gif](/uploads/clickpipes_1mn_88c2bc30a1.gif)
The main advantages of ClickPipes are:


- **An easy and intuitive data onboarding:** Setting up a new ingestion pipeline takes just a few steps. Select an incoming data source and format, tune your schema, and let your pipeline run.
- **Built for continuous ingestion:** ClickPipes manages your continuous ingestion pipelines so that you don’t have to. Set up your pipeline and let us handle the rest.
- **Designed for speed and scale**: ClickPipes provides the scalability you need to handle increasing data volumes, ensuring your systems can handle future demands effortlessly.
- **Unlock your real time analytics**: Built leveraging our deep expertise in real time data management systems, ClickPipes handles the complexities of real time ingestion for optimal performance.


## Besides Confluent Cloud and Apache Kafka, what’s coming next? [\#](/blog/clickhouse-cloud-clickpipes-for-kafka-managed-ingestion-service#besides-confluent-cloud-and-apache-kafka-whats-coming-next)


ClickPipes [supports](https://clickhouse.com/docs/en/integrations/clickpipes#supported-data-sources) Confluent Cloud and Apache Kafka (at the time of this release). We will be quickly expanding the list of supported data sources and systems to turn ClickPipes into a fully fledged connectivity platform for ClickHouse Cloud.


After Kafka, we decided to focus our efforts on supporting other types of streaming technologies like Cloud native sources of events (Amazon Kinesis, Google Pub/Sub, Azure Event Hub). We are also curious to hear from the community about what they want to see next, so please don’t hesitate to use our [contact form](https://clickhouse.com/company/contact) to let us know! We will be happy to explore anything from monitored object stores to Change\-Data\-Capture scenarios.


## How can I access ClickPipes? [\#](/blog/clickhouse-cloud-clickpipes-for-kafka-managed-ingestion-service#how-can-i-access-clickpipes)


ClickPipes Beta is already available in a private preview model. You can join our waitlist by filling out [this form](https://clickhouse.com/cloud/clickpipes#joinwaitlist) and we will reach out to you once a slot is available for testing. This private preview phase is crucial for us to validate the reliability and production readiness of the platform.


Following this phase, we will make ClickPipes generally available in ClickHouse Cloud later this year.


You can find more information in the following pages:


- [ClickPipes Website](https://clickhouse.com/cloud/clickpipes)
- [Video demonstration](https://www.youtube.com/watch?v=rSUHqyqdRuk)
- [Documentation](https://clickhouse.com/docs/en/integrations/clickpipes)
[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
