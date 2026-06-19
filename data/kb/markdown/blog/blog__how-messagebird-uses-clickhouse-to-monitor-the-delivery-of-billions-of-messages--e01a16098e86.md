# How MessageBird Uses ClickHouse to Monitor the Delivery of Billions of Messages


\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How MessageBird Uses ClickHouse to Monitor the Delivery of Billions of Messages

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Aug 14, 2023 · 6 minutes read[MessageBird](https://messagebird.com/) is a cloud communications platform that connects businesses and customers through seamless, contextual conversations. Processing billions of messages, calls, and emails for 29k\+ customers, MessageBird depends heavily on data\-driven insights for efficient operations. ClickHouse, a robust analytical backend, has been integral in delivering these insights since 2017, supporting functions such as monitoring the delivery performance of SMS messages and powering customer\-facing dashboards and APIs.


## Real\-Time Analytics: Driving Customer\-Facing Dashboards and APIs [\#](/blog/how-messagebird-uses-clickhouse-to-monitor-the-delivery-of-billions-of-messages#real-time-analytics-driving-customer-facing-dashboards-and-apis)


At MessageBird, ClickHouse is integral to the company's [real\-time analytics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics) capabilities. The system delivers real\-time data that directly powers its customer\-facing dashboards and APIs. The ability of ClickHouse to support high\-volume data ingestion and low response times means that customer queries are answered swiftly and accurately.


Understanding customer behavior and providing them with the information they need in real\-time is crucial for MessageBird. Whether it's usage statistics, billing details, or performance metrics, the data powered by ClickHouse is immediately available to the end users, driving increased interaction and engagement.


As Javier Llorente, a Senior Data Engineer at MessageBird explained: "I think ClickHouse is really one of the best (solutions) when you have that intersection where you need to perform analytical queries over a huge data set, and you need to have a fast response within seconds. That is where I think ClickHouse has been a really good match for MessageBird."


## Performance Monitoring: Guaranteeing Operational Excellence [\#](/blog/how-messagebird-uses-clickhouse-to-monitor-the-delivery-of-billions-of-messages#performance-monitoring-guaranteeing-operational-excellence)


Performance monitoring is critical for MessageBird. Metrics drawn from their ClickHouse\-driven data infrastructure enable teams to track SMS delivery performance and promptly identify anomalies.


The versatility of ClickHouse plays a crucial role in supporting both internal and external use cases. Within MessageBird, the same ClickHouse cluster is used for a variety of functions. To ensure optimal performance, different policies and quotas are set based on the specific use case. "Although we use the same ClickHouse cluster for various functions, we have different policies and quotas in place depending on the use case. This allows us to control the timeout for queries and manage resource consumption effectively," said Llorente.


Their internal utilization of ClickHouse allows their teams to leverage the data in near real\-time. As Dennis van der Vliet, Senior Engineering Manager at MessageBird, explains, "When a customer raises a concern about message delivery to a specific country, our tooling, powered by ClickHouse, becomes the go\-to resource for understanding the situation."


## MessageBird's Cloud Transition with ClickHouse [\#](/blog/how-messagebird-uses-clickhouse-to-monitor-the-delivery-of-billions-of-messages#messagebirds-cloud-transition-with-clickhouse)


MessageBird first adopted ClickHouse in 2017, transitioning from a custom cron setup on MySQL due to scalability and latency challenges. To further scale its services and manage growing data volumes, MessageBird migrated from a self\-managed, on\-premise solution to ClickHouse Cloud. This transition was driven by the need for a more scalable, resilient, and efficient data infrastructure, but was also significantly influenced by the cost factor.


Migrating to ClickHouse Cloud brought significant benefits, including substantial cost savings from the shift from SSD storage to more economical S3 storage. Moreover, the use of [Projections](https://clickhouse.com/docs/en/sql-reference/statements/alter/projection) in ClickHouse became more cost\-effective due to S3's low data storage costs.


## Cost Efficiency with ClickHouse Cloud [\#](/blog/how-messagebird-uses-clickhouse-to-monitor-the-delivery-of-billions-of-messages#cost-efficiency-with-clickhouse-cloud)


Since moving to ClickHouse Cloud MessageBird has experienced significant savings, with a reduction in costs of approximately 60\-70%. This saving relates not only to the direct costs, such as self\-hosted fees but also to the overhead costs associated with maintenance and infrastructure management. In their experience, the migration to ClickHouse Cloud made considerable economic sense.


## ClickHouse Cloud Scalability and Performance Benefits [\#](/blog/how-messagebird-uses-clickhouse-to-monitor-the-delivery-of-billions-of-messages#clickhouse-cloud-scalability-and-performance-benefits)


Besides cost savings, their shift to ClickHouse Cloud brought substantial scalability and performance improvements. There was a recent situation where increased data volumes led to concerns about slow performance. Before the cloud migration, such a situation would have escalated into a significant incident, owing to the complexities of scaling with their previous self\-hosted setup. However, with ClickHouse Cloud, resolving the situation was straightforward.


“Instead of escalating into an incident as it might have in our previous self\-hosted setup, I simply fired up my computer, scaled up the services in the ClickHouse Cloud console and assured them performance should improve in about 20 minutes,” said van der Vliet.


This example perfectly encapsulates how the cloud\-based infrastructure enables MessageBird to rapidly respond to performance hiccups, ensuring service continuity.


## MessageBird's ClickHouse Cloud Architecture [\#](/blog/how-messagebird-uses-clickhouse-to-monitor-the-delivery-of-billions-of-messages#messagebirds-clickhouse-cloud-architecture)


![MessageBird Architecture.png](/uploads/Message_Bird_Architecture_8c3ab5570a.png)
MessageBird's architecture in ClickHouse Cloud integrates several modern cloud technologies. The data ingestion layer involves an ingestion service that moves data from Google Pub/Sub into ClickHouse using Apache Beam pipelines running on Google Cloud Dataflow. Data for lookup queries is stored in BigTable, which offers low latency and high throughput.
MessageBird leverages the capabilities of ClickHouse's CollapsingMergeTree table engine to ensure only the latest versions of rows are queried.


## The ClickHouse Advantage: Projections [\#](/blog/how-messagebird-uses-clickhouse-to-monitor-the-delivery-of-billions-of-messages#the-clickhouse-advantage-projections)


[Projections](https://clickhouse.com/docs/en/sql-reference/statements/alter/projection) in ClickHouse offer the ability to speed up query performance by storing precalculated results for commonly used transformations or aggregate functions. This functionality significantly improves query performance, particularly for complex analytical queries that would otherwise require scanning large amounts of data or performing costly operations.
With the migration to ClickHouse Cloud, projections have become even more cost\-effective for MessageBird. With the self\-managed setup relying on SSDs, maintaining additional storage for projections could be costly due to the high cost per GB of storage. However, with the move to ClickHouse Cloud, and a shift to S3 storage, projections are now available at a much lower cost.


## Summary [\#](/blog/how-messagebird-uses-clickhouse-to-monitor-the-delivery-of-billions-of-messages#summary)


ClickHouse has proven to be an essential tool for MessageBird, driving its real\-time analytics and performance monitoring capabilities. By moving to ClickHouse Cloud, MessageBird has been able to easily handle high ingestion traffic, and save on costs. The use of ClickHouse's unique features like Projections and specific table engines aligns with the company's commitment to efficiency and innovation. As MessageBird continues its journey, ClickHouse stands as a key component of its robust, scalable, and cost\-effective data infrastructure.


Learn more: <https://messagebird.com/>

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
