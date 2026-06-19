# Postgres CDC connector for ClickPipes is now in Public Beta


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Postgres CDC connector for ClickPipes is now in Public Beta

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)Feb 18, 2025 · 7 minutes readToday, we are excited to announce the availability of [the Postgres CDC connector in ClickPipes in public beta](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector). With this, customers can easily replicate their Postgres databases to ClickHouse Cloud with just a few clicks. Simply go to the **Data Source** tab in your service, choose the Postgres tile, and follow a few steps to integrate your Postgres databases.


![Postgres CDC Add Data Source](/uploads/Postgres_CDC_Add_Data_Source_e058704d02.gif)
After [joining forces with PeerDB](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database), a leading Postgres CDC company, we integrated it natively into ClickHouse Cloud and [released](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-private-preview) the private preview of the Postgres CDC connector in ClickPipes.


The response during the Private Preview was overwhelming! Many customers tested the service, provided valuable feedback, ran production workloads, and replicated multiple petabytes of data from Postgres to ClickHouse. After further refining the experience, we are now ready to make native Postgres CDC in ClickHouse Cloud available to everyone.


## Customer feedback [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#customer-feedback)


The Postgres CDC connector in ClickPipes is already being used by multiple organizations, including [Syntage](https://syntage.com/), [Neon](https://neon.tech/), [Blacksmith](https://www.blacksmith.sh/), [Vapi](https://vapi.ai/), [Adora](https://adora.so/), [Daisychain](https://www.daisychain.app/), [Unify](https://www.unifygtm.com/home-lp), [Ottimate](https://ottimate.com/) and [others](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector). Below are a few testimonials capturing feedback from our reference customers:


*“We are having an amazing experience using the Postgres CDC connector in ClickPipes. We seamlessly moved our 30TB Aurora database to ClickHouse Cloud and are continuously keeping it in sync. We did not expect any ETL tool to handle our load, especially after a bitter experience in the past. However, we were pleasantly surprised by how reliable and performant ClickPipes has been for us.”* \- [Matteus Pedroso](https://www.linkedin.com/in/matheuspedroso/), Co\-founder and CEO, [Syntage](https://syntage.com/)


*“ClickPipes for Postgres has made it incredibly easy for us to keep our billing data in Postgres synchronized with ClickHouse for efficient analytics. The CDC experience is blazing fast, ensuring data freshness within seconds while minimizing the load on our production Postgres database. An invaluable solution for seamlessly integrating Postgres with ClickHouse!”* \- Mo Abedi, Software Engineer in Billing team, [Neon.tech](https://neon.tech/)


## Product Enhancements [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#product-enhancements)



### Built for performance [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#built-for-performance)


The Postgres CDC connector is built on strong foundations, with performance at the forefront. It has been purpose\-built for Postgres and ClickHouse and implements many native optimizations. On the Postgres side, parallel snapshotting enables 10x faster initial loads and backfills, allowing terabyte\-scale migrations in hours, while continuous [flushing of the replication slot](https://clickhouse.com/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#efficiently-flush-the-replication-slot) to intermediary stages ensures data freshness within seconds. On the ClickHouse side, parallel ingestion through multiple replicas and [configurable chunking](https://clickhouse.com/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#better-memory-handling-on-clickhouse) for better memory management improve performance and reliability.


Beyond these foundations, over the past few months, the team has added several features to support enterprise\-grade production workloads. Below are the highlights:


### User facing alerts [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#user-facing-alerts)


This feature enables alerts for failures or potential issues with ClickPipe. Alerts are surfaced via the Notifications center in ClickHouse Cloud and via email. Each alert classifies the issue type—for example, when a replication slot is growing unexpectedly, off stream MVs are failing during ingestion, or there are connectivity issues, among others—and provides self\-mitigation steps to help you resolve them.


![Gif showing how users can configure notifications](/uploads/Postgres_CDC_User_Notifications_cddc06fced.gif)
### Source Monitoring Page [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#source-monitoring-page)


We also introduced a new page that allows you to monitor the source Postgres database during CDC. The page provides key insights, including a list of active replication slots, their status, a chart showing replication slot growth over time, and associated wait events in Postgres. This offers detailed visibility into the progress of replication, helping you identify bottlenecks and optimize performance.


![Visual showing Postgres replication slot status and lag.](/uploads/Postgres_CDC_Source_Monitoring_852798cd65.png)
### Open API Support [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#open-api-support)


A common piece of feedback we've received from customers during the private preview is that it becomes difficult to create and manage pipes with potentially hundreds of tables through the UI. To address this, we added Open API support, which enables you to create and manage pipes programmatically. Currently, Open API support is in private beta. If you're interested in trying it, reach out to our team at [db\-integrations\-support@clickhouse.com](mailto:db-integrations-support@clickhouse.com). The next step in this effort is to add Terraform support for creating and managing ClickPipes for Postgres CDC.


### PeerDB Open Source Enhancements [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#peerdb-open-source-enhancements)


This connector is powered by PeerDB, our [open source](https://github.com/PeerDB-io/peerdb/) Postgres CDC codebase. In the past couple of months, we've made several improvements to make PeerDB enterprise\-ready. In the past two months, we've made 8 minor and 3 major [releases](https://github.com/PeerDB-io/peerdb/releases). Notable improvements include:


- [Improved ingestion performance by using multiple replicas in ClickHouse.](https://github.com/PeerDB-io/peerdb/pull/2256)
- [Eliminated reconnections to the replication slot for better performance under heavy workloads.](https://github.com/PeerDB-io/peerdb/pull/2371)
- [Revamped retry logic to filter false positive errors.](https://github.com/PeerDB-io/peerdb/pull/2122)
- Asynchronous pulling from Postgres and pushing to ClickHouse to enhance replication slot flushing logic.


## Pricing [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#pricing)


During the public beta, the Postgres CDC connector in ClickPipes will be free of charge. We plan to introduce pricing during the next phase, General Availability (GA). The exact pricing is still to be determined, but our goal is to keep it competitive to support real\-time analytics use cases at scale.


## Conclusion [\#](/blog/postgres-cdc-connector-clickpipes-public-beta#conclusion)


I hope you enjoyed reading the blog. The next phase for us is the General Availability (GA) of Postgres CDC in ClickPipes once the feature is ready. During the public beta, if you run into issues, have questions, or want to chat with the product team, please reach out at [db\-integrations\-support@clickhouse.com](mailto:db-integrations-support@clickhouse.com).


Interested in trying the native Postgres CDC capabilities in ClickHouse Cloud? Check out these helpful links:


- [Ingesting data from Postgres to ClickHouse (using CDC)](https://clickhouse.com/docs/en/integrations/clickpipes/postgres)
- [ClickPipes for Postgres FAQ](https://clickhouse.com/docs/en/integrations/clickpipes/postgres/faq)
- [Try ClickHouse Cloud for free](https://clickhouse.com/docs/en/cloud/get-started/cloud-quick-start)
[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
