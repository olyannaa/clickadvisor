# Supabase Partnership: Native Postgres Replication to ClickHouse, clickhouse\_fdw and more


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Supabase Partnership: Native Postgres Replication to ClickHouse, clickhouse\_fdw and more

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)Oct 30, 2024 · 8 minutes read## Postgres and ClickHouse \- the “default data stack” [\#](/blog/supabase-partnership-native-postgres-replication-clickhouse-fdw#postgres-and-clickhouse---the-default-data-stack)


Over the past few years, a common reference architecture is emerging: customers are using Postgres and ClickHouse together to address most of their data challenges.


On the one hand, you have Postgres, the most popular open source transactional database, which is well\-suited to store and query application data, supporting mission\-critical transactional and web\-app use cases. On the other hand, you have ClickHouse, the most popular open source analytical database, which is well\-suited for supporting all analytics and reporting use cases, powering both customer\-facing and internal applications. Both of them share the same ethos of open source. These reasons make Postgres and ClickHouse a compelling duo for solving a wide range of data challenges for customers thereby making them the “default data stack”.


At [ClickHouse](https://clickhouse.com/), we have been committed to making it easy for customers to implement this architecture—using Postgres and ClickHouse together. One of our recent steps in this direction is the [acquisition of PeerDB](https://techcrunch.com/2024/07/30/real-time-database-startup-clickhouse-acquires-peerdb-to-expand-its-postgres-support/), a leading Postgres [CDC](https://en.wikipedia.org/wiki/Change_data_capture) provider. This enables seamless replication of transactional data from Postgres to ClickHouse, powering real\-time analytics and data warehousing use cases.


## Announcing our Partnership with Supabase \- Supabase and ClickHouse, better together [\#](/blog/supabase-partnership-native-postgres-replication-clickhouse-fdw#announcing-our-partnership-with-supabase---supabase-and-clickhouse-better-together)


As the next step in this direction, we are excited to announce our partnership with [Supabase](https://supabase.io/), a leading managed service provider for Postgres. Supabase’s vision is to offer a seamless experience for app developers to build AI and web apps using Postgres, with features such as out\-of\-the\-box authentication, real\-time capabilities, edge functions, and more. We share a similar vision for [ClickHouse Cloud](https://clickhouse.cloud/), aiming to provide a seamless experience for developers and data engineers building analytical applications with features like serverless, auto\-scaling, and ClickPipes.


Both of us are committed to open source across two communities: Postgres and ClickHouse. We also share a rapidly growing joint customer base. The vision of this partnership is to enable customers to seamlessly integrate Supabase and ClickHouse, helping them build out their data stack and drastically reduce time\-to\-market for different applications.



> "The Supabase team is excited to develop a phenomenal developer experience with the ClickHouse team. ClickHouse and Postgres rapidly becoming the default data stack for Supabase's largest customers. Many of our fastest\-growing AI customers are combining the two open source tools as they scale." \- **Paul Copplestone, CEO of Supabase**



> "ClickHouse is very excited to partner with Supabase to make it easy for customers to use both technologies together. Through this partnership, we aim to make it even simpler for Postgres developers to use ClickHouse in conjunction and build real\-time, data\-driven applications at scale." \- **Aaron Katz, CEO of ClickHouse Inc.**


Below is a testimonial from a joint customer [Adora](https://www.adora.so/), who uses Supabase and ClickHouse together:



> PostgreSQL provides us with our required ACID guarantees, and ClickHouse provides us the ability to perform complex analytics queries that would time out on PostgreSQL. With Supabase and ClickHouse Cloud, a lot of our operational complexity goes away. With PeerDB, we don't have to sacrifice query performance or ACID guarantees \- we can have our data stored and queryable from both worlds. We are excited to see what this partnership has in store to make it even seamless to use Supabase and ClickHouse together. \- **Oliver Tan, Founding Engineer , Adora.so**


## Native Supabase OAuth in PeerDB for Postgres CDC to ClickHouse [\#](/blog/supabase-partnership-native-postgres-replication-clickhouse-fdw#native-supabase-oauth-in-peerdb-for-postgres-cdc-to-clickhouse)


The first feature we are announcing as part of this partnership is the native OAuth integration of Supabase in [PeerDB](https://peerdb.io/), enabling seamless Postgres replication to ClickHouse. With this feature, customers can add their Supabase Postgres databases as data sources (aka Peers) with just one click and start replicating data from Supabase to ClickHouse to enable real\-time analytics. They do not need to explicitly enter database credentials such as hostname, database name, and more. PeerDB also performs the necessary checks to ensure that Postgres is accurately configured for replication to ClickHouse. You can find detailed steps for this integration in this [document](https://docs.peerdb.io/mirror/cdc-supabase-clickhouse) on simple Postgres replication from Supabase to ClickHouse using PeerDB. Here is a quick demo of what this looks like in action:
  




  

We are actively working on integrating PeerDB into [ClickPipes](https://clickhouse.com/cloud/clickpipes), the native ingestion service of ClickHouse. This integration will power the Postgres CDC connector in ClickPipes. We expect this integration to be available for customers in the coming months. The Native OAuth feature to seamlessly add Supabase as a data source will also be extended to ClickPipes.


A big shout\-out to Supabase for adding [critical features](https://supabase.com/blog/supabase-clickhouse-partnership) such as improved disk management and exposing modification of important Postgres replication\-related configs. These features were essential for ensuring a smooth integration of Postgres CDC from Supabase to ClickHouse.


## Support for IPV6 in PeerDB Cloud [\#](/blog/supabase-partnership-native-postgres-replication-clickhouse-fdw#support-for-ipv6-in-peerdb-cloud)


​​We recently added IPv6 support in [PeerDB Cloud](https://peerdb.cloud/) to facilitate Supabase as a native source Peer. Previously, Supabase customers had to enable an add\-on to support IPv4 for Supabase to be used as a source peer for replication to ClickHouse. This feature makes the Supabase integration even smoother, as they no longer need to enable the IPv4 add\-on; PeerDB will replicate data using the IPv6 addresses that Supabase provides by default. We plan to extend IPv6 support to the Postgres CDC connector in ClickPipes once PeerDB is fully integrated in ClickPipes.


## clickhouse\_fdw: Query ClickHouse from Supabase [\#](/blog/supabase-partnership-native-postgres-replication-clickhouse-fdw#clickhouse_fdw-query-clickhouse-from-supabase)


![Supabase ClickHouse Reference Archiecture.png](/uploads/Supabase_Click_House_Reference_Archiecture_0213636772.png)
Once application data in Supabase is continuously replicated to ClickHouse, users can use the clickhouse\_fdw extension provided by Supabase to start querying data in ClickHouse from within Postgres. This enables a variety of use cases, including: a) consolidating to a single query interface to support both transactional (OLTP) and analytical (OLAP) applications; and b) providing a simple way to join transactional data stored in Postgres with analytical data such as logs, telemetry, events, and more. Below is an end\-to\-end demo showing Postgres CDC to ClickHouse and clickhouse\_fdw in action:
  


  

Just as a note, clickhouse\_fdw supports pushdown for LIMIT, WHERE, ORDER BY, etc., but not for aggregates or JOINs. For pushing down JOINs, you can use the FDW support for [parameterized views](https://fdw.dev/catalog/clickhouse/#foreign-table-options)—an exciting feature that Supabase recently added. The demo shows this in action. If your use case requires more advanced SQL queries with 10s of lines containing subqueries, GROUP BYs, JOINs, etc., it is recommended to query ClickHouse directly.


## What is in store for the future? [\#](/blog/supabase-partnership-native-postgres-replication-clickhouse-fdw#what-is-in-store-for-the-future)


We are exploring a few imore deas to make the integration of Supabase and ClickHouse easier for customers. If you are already using (or plan to use) Supabase and ClickHouse together, we would love to chat to learn more about your use case and hear your feedback on what you would like to see to make the integration smoother.


Please [reach out](https://clickhouse.com/company/contact) to us and share your Supabase \+ ClickHouse story and provide feedback for a smoother integration. We’d love for you to be a part of this journey and directly influence our roadmap!


## Get started with integrating Supabase, ClickHouse and PeerDB [\#](/blog/supabase-partnership-native-postgres-replication-clickhouse-fdw#get-started-with-integrating-supabase-clickhouse-and-peerdb)


Hope you enjoyed reading the blog! If you’d like to get started with Supabase Postgres, ClickHouse, and PeerDB for replication between them, you can follow the links below.


- Supabase: [database.new](https://database.new)
- ClickHouse: [clickhouse.com](https://clickhouse.com/)
- PeerDB for Postgres CDC: [peerdb.io](https://www.peerdb.io/)


Reference to the blog from the Supabase team: [https://supabase.com/blog/supabase\-clickhouse\-partnership](https://supabase.com/blog/supabase-clickhouse-partnership)

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
