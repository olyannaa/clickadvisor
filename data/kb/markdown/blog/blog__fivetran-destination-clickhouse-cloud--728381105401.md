# Announcing the Fivetran Destination for ClickHouse Cloud


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Announcing the Fivetran Destination for ClickHouse Cloud

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene)Apr 25, 2024 · 6 minutes readWe’re delighted to announce the availability of the [Fivetran](https://fivetran.com/) destination for ClickHouse Cloud. Thanks to Fivetran's comprehensive range of connectors, users can quickly load data from over 500 sources.


Available in public preview, this destination represents one of the earliest contributions to the [Partner\-Built program](https://fivetran.com/docs/partner-built-program), using the recently released Fivetran SDK. If you want to try this destination, follow the short video we’ve prepared for this blog post or visit the comprehensive documentation here.


We welcome feedback and contributions on this initial version of the destination for which the code has been open\-sourced under the Apache 2\.0 license.


For those keen to try the new destination, we discuss a few important points regarding the implementation and ideal use cases below.


![fivetran-1.png](/uploads/fivetran_1_8721583670.png)
## Why Fivetran? [\#](/blog/fivetran-destination-clickhouse-cloud#why-fivetran)


Fivetran is a leading data integration technology provider that offers automated solutions to streamline data pipelines across various sources and destinations. Its platform is designed to simplify the process of extracting and loading data by providing robust, fully managed connectors that automatically adapt to schema and API changes, ensuring data integrity without requiring ongoing maintenance from users. Supporting over 500 data sources, from databases and SaaS applications to cloud storage, Fivetran is an ideal choice for businesses seeking to centralize their data for analysis in ClickHouse.


This new ClickHouse destination enables seamless automation of data ingestion directly into ClickHouse from the wide range of systems supported by Fivetran. Users can leverage ClickHouse for analytics without the overhead of manual data pipeline management. This integration significantly reduces the workload on data engineering teams and allows analysts to focus on deriving actionable insights from real\-time data.


## When should I use the destination? [\#](/blog/fivetran-destination-clickhouse-cloud#when-should-i-use-the-destination)


We recommend the destination for use cases where moderate volumes of business data need to be loaded into ClickHouse from [applications](https://fivetran.com/docs/connectors/applications) that would otherwise require custom integration code, e.g., Salesforce, Slack, Zendesk. These applications often have complex APIs that would require custom integration code to synchronize with ClickHouse, while supporting the ability to handle inserts, updates, and deletes. With the ClickHouse destination, this complexity is handled by Fivetran and presented as a few simple clicks: ideal for business teams who wish to load Zendesk tickets, Slack chats, or Salesforce accounts into ClickHouse to query and visualize in their preferred BI tool in real\-time.


In implementing the destination we have carefully considered the need to support update and delete operations, using ClickHouse features to ensure they are handled efficiently. As a result, you may also wish to explore using Fivetran for smaller Change Data Capture (CDC) use cases.


![fivetran-2.png](/uploads/fivetran_2_651b95576c.png)
For larger volumes in the TB and PB range, from sources such as object storage and Kafka, we recommend existing ClickHouse tools, such as ClickHouse Kafka Connect and ClickPipes for Cloud users. These are typically more cost\-effective and specifically designed for the bulk and incremental transfer of large data volumes that are already in a structured format.


## Key design decisions [\#](/blog/fivetran-destination-clickhouse-cloud#key-design-decisions)


The Fivetran SDK requires several behaviors from the target data source. Several of these led to key design decisions and the destination only supporting ClickHouse Cloud in the initial release:


- **Need for sequential consistency**—Fivetran supports a wide range of connector sources, many of which inherently support the notion of update and delete events. These need to be handled by the destination. Fivetran does not guarantee that the updates will consist of the full event. We considered using lightweight updates for this problem, but we considered this would struggle with workloads containing a higher number of updates. We therefore decided on an approach where the destination reads the full contents of the row from ClickHouse before reinserting an update copy.


Since the destination could be connected to a proxy or load balancer in front of a ClickHouse cluster, we need to ensure that reads are sequentially consistent i.e., if a row has recently been inserted into one node, a read for the same row must always exceed from other nodes (no stale reads). For this, we use the setting `select_sequential_consistency=1`. For [ClickHouse Cloud’s SharedMergeTree (SMT) engine](https://clickhouse.com/docs/en/cloud/reference/shared-merge-tree#consistency), this operation is much lighter weight than for ReplicatedMergeTree and can be reliably scaled. For ReplicatedMergeTree this requires [quorum inserts](https://clickhouse.com/docs/en/operations/settings/settings#insert_quorum) (Inserts are quorum inserts by default in SMT) to be enabled and incurs significant overhead.
- **Efficient handling of updates and deletes** \- To handle updates and deletes, the Fivetran destination uses the ReplacingMergeTree (SharedReplacingMergeTree more specifically). This is recommended as the optimal means to [handle this workload in ClickHouse](https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1). To ensure accurate counts are returned to analytical queries, users will need to ensure table names include a `FINAL` suffix.
- **Go implementation** \- While Fivetran offers several SDKs, we selected Golang as the language for implementation. The [client for this language](https://github.com/ClickHouse/clickhouse-go) is mature and this aligns with our existing use of the language internally for products such as ClickPipes.


Since SharedMergeTree, on which the destination depends, is limited to ClickHouse Cloud, the current implementation cannot be used with ClickHouse OSS. As Fivetran is exclusively a SaaS service, we don’t anticipate many use cases that will need OSS support. However, the code is permissively licensed, and we welcome contributions to support ReplicatedMergeTree efficiently. Those interested in adding support should see [this issue](https://github.com/ClickHouse/clickhouse-fivetran-destination/issues/3).


## A simple example [\#](/blog/fivetran-destination-clickhouse-cloud#a-simple-example)


To show off the new destination we demonstrate loading data from Zendesk. Zendesk tickets represents a treasure trove of useful business data for analytics. While this would have traditionally required users to familiarize themselves with the Zendesk APIs and ClickHouse ingestion, we show how Fivetran facilitates this in a few simple clicks!



  

The destination includes built\-in documentation for users looking for a more comprehensive experience. Alternatively, you can check out the extensive [docs hosted by Fivetran](https://fivetran.com/docs/destinations/clickhouse) .


## Conclusion [\#](/blog/fivetran-destination-clickhouse-cloud#conclusion)


The new Clickhouse destination for Fivetran is now available in public preview to assist with the loading of complex data sources. Try the destination today and provide your [feedback in the repository](https://github.com/ClickHouse/clickhouse-fivetran-destination/issues/3).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
