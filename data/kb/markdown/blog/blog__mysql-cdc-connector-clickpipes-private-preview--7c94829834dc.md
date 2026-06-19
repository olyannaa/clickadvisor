# MySQL CDC connector for ClickPipes is now in Private Preview


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# MySQL CDC connector for ClickPipes is now in Private Preview

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)Apr 10, 2025 · 4 minutes readToday, we’re excited to announce the private preview of the [MySQL](https://www.mysql.com/) Change Data Capture (CDC) connector in [ClickPipes](https://clickhouse.com/cloud/clickpipes)! This enables customers to replicate their MySQL databases to [ClickHouse Cloud](https://clickhouse.cloud/) in just a few clicks and leverage ClickHouse for blazing\-fast analytics. You can use this connector for both continuous replication and one\-time migration from MySQL, no matter where it's running—whether in the cloud (RDS, Aurora, CloudSQL, Azure, etc.) or on\-premises.


The experience is natively integrated into ClickHouse Cloud through ClickPipes, the built\-in ingestion service of ClickHouse Cloud. This eliminates the need for external ETL tools, which are often expensive and require significant overhead to set up and manage. This connector is powered by [**PeerDB**](https://github.com/PeerDB-io/peerdb), a fully open source database replication project by ClickHouse—so there’s no lock\-in, and the value extends to self\-hosted ClickHouse users as well.


[**You can sign up to the private preview by following this link.**](https://clickhouse.com/cloud/clickpipes/mysql-cdc-connector)


After launching our Postgres CDC connector a few months ago—which has been rapidly growing in adoption—there was overwhelming demand from customers to provide similar capabilities for MySQL data sources. We’ve heard all of that feedback and are now launching the MySQL connector in ClickPipes.



## Purpose\-built for MySQL and ClickHouse [\#](/blog/mysql-cdc-connector-clickpipes-private-preview#purpose-built-for-mysql-and-clickhouse)


Our focus at ClickPipes has always been quality over quantity, so any connector we add is built to scale. The same applies to the MySQL CDC connector — it’s designed to handle terabytes of data, delivering blazing\-fast performance with replication latency as low as a few seconds. It supports MySQL\-native features, including replication of JSON and vector types, along with flexible replication modes, including GTID\-based and binary log position\-based (POS) options.


## Key Features [\#](/blog/mysql-cdc-connector-clickpipes-private-preview#key-features)


The [MySQL CDC connector](https://clickhouse.com/docs/integrations/clickpipes/mysql) comes packed with features designed to make it easy to initiate and manage replication from MySQL to ClickHouse Cloud. Here’s a list of key capabilities:


- **Blazing\-Fast Initial Loads (Backfills):** Migrate terabytes of existing data across hundreds of MySQL tables to ClickHouse within a day. You can configure the number of parallel threads to migrate multiple tables simultaneously. Soon, we plan to support intra\-table parallelism—using multiple threads to migrate a single large table.
- **Continuous Replication (CDC):** After the initial load, continuously replicate changes—including all DML operations (INSERTs, UPDATEs, DELETEs)—from MySQL to ClickHouse with latencies as **low as a few seconds**.
- **Table and Column\-Level Filtering:** Selectively replicate only the tables and columns you need from MySQL—helping reduce data transfer and storage overhead while supporting compliance and privacy needs, such as excluding PII.


![tableselector (1).png](/uploads/tableselector_1_ca659eded9.png)
- **Schema Changes:** Automatically replicate schema changes during CDC, including DDL commands like ADD COLUMN and DROP COLUMN on MySQL.
- **Flexible Replication Modes:** The connector relies on MySQL’s binary log for replication and supports both file position\-based (POS) and GTID\-based replication modes.
- **Native Data Type Support:** Fully supports MySQL\-native data types—including vectors, unsigned integers, geospatial types, JSON, vectors and more.
- **MySQL Version Compatibility:** Supports all MySQL versions 8\.0\.1 and above.
- **In\-Place Editing:** Modify existing MySQL CDC Pipes to add new tables, adjust sync intervals (data\-freshness), or update configuration settings—all without downtime.


![editsettings (1).png](/uploads/editsettings_1_debffc96f2.png)
- **Enterprise\-Grade Security:** Securely connect MySQL sources using SSH tunneling, AWS PrivateLink, and IP\-based access controls.
- **Built\-in metrics and monitoring:** Enjoy a fully managed replication solution with built\-in monitoring, metrics, logs, and high availability—eliminating operational overhead for your team.


![metrics (1).png](/uploads/metrics_1_523cd3d942.png)
## How to sign up for Private Preview? [\#](/blog/mysql-cdc-connector-clickpipes-private-preview#how-to-sign-up-for-private-preview)


You can sign up for the private preview by filling out [the form on this page](https://clickhouse.com/cloud/clickpipes/mysql-cdc-connector). Our team will reach out to you within a few days and work closely with you to provide early access. Given the anticipated demand, there may be a slight delay, but we’ll ensure we connect with you as soon as possible.


The Private Preview entails no cost and is fully free. This is a great opportunity for you to get firsthand experience with the native MySQL integration in ClickHouse Cloud and directly influence the roadmap. Looking forward to having you onboard!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
