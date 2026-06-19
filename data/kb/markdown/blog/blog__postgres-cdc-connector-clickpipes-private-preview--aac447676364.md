# Postgres CDC connector for ClickPipes is now in Private Preview


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Postgres CDC connector for ClickPipes is now in Private Preview

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)Nov 25, 2024 · 6 minutes read![postgres-cdc-connector-clickpipes-private-preview.png](/uploads/postgres_cdc_connector_clickpipes_private_preview_f06bd33c0b.png)
Today, we’re excited to announce the private preview of the Postgres Change Data Capture (CDC) connector in ClickPipes! This enables customers to replicate their Postgres databases to ClickHouse Cloud in just a few clicks and leverage ClickHouse for blazing\-fast analytics. You can use this connector for both continuous replication and one\-time migrations use cases from Postgres.


The experience is natively integrated into ClickHouse Cloud through ClickPipes, the integration engine designed to simplify moving massive volumes of data to ClickHouse. This eliminates the need for external ETL tools, which are often expensive, slow, and don’t scale for Postgres.


**[You can sign up to the private preview by following this link](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector)**.


Just a reminder, ClickHouse [joined forces](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database) with PeerDB, a leading Change Data Capture (CDC) provider for Postgres, a few months ago. PeerDB already supports multiple enterprise\-grade workloads and has helped replicate petabytes of data from Postgres to ClickHouse. Over the past few months, the team has worked hard to natively integrate PeerDB into ClickHouse Cloud. This announcement marks the first release of this integration, enabling users to seamlessly move data from Postgres to ClickHouse.


The Postgres CDC connector was built in close collaboration with several customers and design partners who are already running production\-grade workloads. Here are a few customer testimonials:



> “PeerDB has been a game\-changer for us, effortlessly migrating tens of terabytes from our Postgres warehouse into ClickHouse and keeping millions of daily orders synced with just seconds of latency. We're really excited about PeerDB's native integration into ClickHouse Cloud via ClickPipes and all of the opportunities it opens up for us.” \- **[SpotOn](https://www.spoton.com/)**



> “We already reduced our Postgres to ClickHouse snapshot times from 10\+ hours down to 15 minutes with PeerDB. Combining ClickHouse’s powerful analytics natively with PeerDB’s real\-time data capture capabilities will greatly simplify our data processing workflows. This integration will enable us to build analytical applications faster, giving us a competitive edge in the market.” \- **[Vueling](https://www.vueling.com/)**


Without further ado, here is the demo of Postgres CDC connector in ClickPipes:



## Postgres \+ ClickHouse, a powerful data stack [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#postgres--clickhouse-a-powerful-data-stack)


Using ClickHouse and PostgreSQL through a seamless CDC integration creates a powerful data stack by combining PostgreSQL's robust transactional capabilities with ClickHouse's high\-performance analytics. CDC ensures real\-time synchronization, allowing ClickHouse to handle fast queries on massive datasets without burdening PostgreSQL. This integration delivers real\-time insights and scalable analytics, making it an ideal solution for modern, data\-driven workflows. Below are a few main advantages of this architecture:


1. **Full workload isolation:** You can continue building your OLTP application on Postgres and your OLAP application on ClickHouse, with complete workload isolation—analytics will not affect your transactional workload.
2. **No compromises on features:** It also allows you to build your applications using the full capabilities and features (e.g., SQL coverage, performance, etc.) of both Postgres and ClickHouse, each optimized for a specific workload.


We believe customers derive the most value in solving real\-world data problems by leveraging purpose\-built databases like Postgres and ClickHouse as they were designed, with full flexibility, rather than relying on alternatives that retrofit one database engine into another, compromising the full feature set of each. We are observing a clear [trend](https://x.com/kiwicopple/status/1851638636590035054) towards the Postgres \+ ClickHouse architecture among real\-world customers.


## Key Benefits of the Postgres CDC connector [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#key-benefits-of-the-postgres-cdc-connector)


The Postgres CDC connector in ClickPipes is purpose\-built for Postgres and ClickHouse, ensuring a fast, simple and a cost effective replication experience. Here are some key benefits for customers:


### Blazing Fast Performance [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#blazing-fast-performance)


With features like parallel snapshotting, you can achieve 10x faster initial loads, transferring terabytes of data in hours instead of days, and experience replication latency as low as a few seconds for continuous replication (CDC).


### Super Simple [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#super-simple)


You can start replicating your Postgres databases to ClickHouse in just a few clicks and minutes. Simply add your Postgres database as a source, select the specific tables/columns you want to replicate, and you're ready to go.


### Postgres and ClickHouse native features [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#postgres-and-clickhouse-native-features)


This connector supports native Postgres features such as replication of schema changes, partitioned tables, built\-in monitoring and alerting for replication slot size, and support for complex data types such as JSONB and ARRAYs, among others.


On the ClickHouse side, it supports features such as selecting specialized table engines, configuring custom order keys, choosing nullable columns, and so on during the replication process.


### Enterprise\-grade security [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#enterprise-grade-security)


At ClickHouse, security is a top priority, even before performance and features. We’ve extended the same level of security to the Postgres CDC connector in ClickPipes. It includes features such as SSH tunneling and Private Link to securely connect to your Postgres databases. Data in transit is fully encrypted using SSL.


### No vendor lock\-in [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#no-vendor-lock-in)


The Postgres CDC connector is powered by PeerDB, which is fully open source [https://github.com/PeerDB\-io/peerdb/](https://github.com/PeerDB-io/peerdb/). With the exception of the UI, we have ensured that all components are directly extended from the PeerDB open\-source project. This underscores our commitment to open\-source and ensures there is no vendor lock\-in for our customers.


## How to sign up for Private Preview? [\#](/blog/postgres-cdc-connector-clickpipes-private-preview#how-to-sign-up-for-private-preview)


[![postgres-cdc-clickpipes-private-preview-signup.png](/uploads/postgres_cdc_clickpipes_private_preview_signup_12c9afced9.png)](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector)


You can sign up for the private preview by filling out the form on [this page](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector). Our team will reach out to you within a day and closely collaborate with you to provide early access. The Private Preview entails no cost and is fully free. This is a great opportunity for you to get firsthand experience with the native Postgres integration in ClickHouse Cloud and directly influence the roadmap. Looking forward to having you onboard!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
