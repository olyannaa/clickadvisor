# ClickHouse welcomes PeerDB: Adding the fastest Postgres CDC to the fastest OLAP database


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse welcomes PeerDB: Adding the fastest Postgres CDC to the fastest OLAP database

![](/_next/image?url=%2Fuploads%2FRyadh_d50dc0546c.png&w=96&q=75)![aaron.png](/_next/image?url=%2Fuploads%2Faaron_182cb2976e.png&w=96&q=75)[Ryadh Dahimene](/authors/ryadh-dahimene) and [Aaron Katz](/authors/aaron-katz)Jul 30, 2024 · 7 minutes read![peerdb_blog_cover.png](/uploads/peerdb_blog_cover_26a6c47078.png)
We are thrilled to announce today that ClickHouse is joining forces with PeerDB, a Change Data Capture (CDC) provider focused on Postgres, and we’re happy to welcome the PeerDB team and community into the ClickHouse family.


We believe that by combining our efforts, we’ll be able to offer a seamless and efficient integration between two leading open\-source databases: Postgres and ClickHouse. This will enable bridging the gap between transactional and analytical workloads and unlock more value for users and developers. Moreover, when we met with the PeerDB team, we became even more excited because of the clear cultural fit between our companies, as well as the alignment of our engineering (performance\-focused!) cultures.



## The two sides of the data coin [\#](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database#the-two-sides-of-the-data-coin)


There’s a lot to be said about the Postgres and ClickHouse pair. On one hand, Postgres slowly but surely rose to its current position as
the almost de facto transactional backend of the web. Renowned for its reliability, open\-source roots, comprehensive feature set, and strong support for transactional workloads, it wasn’t surprising to see the [2024 StackOverflow survey](https://survey.stackoverflow.co/2024/technology#most-popular-technologies-database-prof) rank Postgres as the number one database for the second year in a row.


On the other hand, in the analytics space, a similar development took place with ClickHouse over the last decade. As an open\-source, high\-performance, columnar database optimized for real\-time analytics and handling large volumes of data with no compromise on speed and efficiency, ClickHouse’s wide adoption is a testament to the ever\-growing need for real\-time analytics in modern software.


![2_sides_of_a_coin.png](/uploads/2_sides_of_a_coin_943a517da9.png)
By integrating Postgres’ robust transactional capabilities with ClickHouse's analytical power via a performant and robust CDC integration, organizations can create a hybrid environment where operational data seamlessly flows into analytical processes. This allows for user\-facing real\-time insights and decision\-making without compromising on data consistency and transactional integrity, and has been successfully adopted at scale by numerous organizations including [GitLab](https://about.gitlab.com/blog/2022/04/29/two-sizes-fit-most-postgresql-and-clickhouse/), [Instacart](https://tech.instacart.com/real-time-fraud-detection-with-yoda-and-clickhouse-bd08e9dbe3f4), [LangChain](https://clickhouse.com/blog/langchain-why-we-choose-clickhouse-to-power-langchain), [Cloudflare](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse), and [many others](https://clickhouse.com/comparison/postgresql).


## Change Data Capture, done right. [\#](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database#change-data-capture-done-right)


Offering a fast and reliable change data capture experience, at the scale at which ClickHouse operates, is not an easy problem to solve. When we started looking into providing a Postgres CDC connector for ClickPipes, we evaluated a list of options ranging from developing our solution, either from scratch or on top of open\-source foundations, to licensing specific technologies. It was obvious from the results of the first tests we ran that PeerDB provided a unique value proposition that resonates well with ClickHouse’s core principles.


Laser\-focused on Postgres as a data source, the PeerDB approach to the CDC problem doesn’t compromise on speed, with blazing\-fast snapshots, while preserving reliability and correctness. Great care is also given to keeping the CDC process non\-invasive to the source Postgres system which often represents a critical operational system. Other features include destination query cost control, resync capabilities, monitoring and alerting on replication slot growth, schema evolution, rich data type mapping, and the use of ClickHouse’s ReplacingMergeTree.


Javier Erro Garcia, Cloud Architecture Manager at Vueling Airlines, shared excitement about the upcoming integration:



> “As a user of both ClickHouse Cloud and PeerDB, I am thrilled about this acquisition. We already reduced our Postgres to ClickHouse snapshot times from 10\+ hours down to 15 minutes with PeerDB. Combining ClickHouse’s powerful analytics natively with PeerDB’s real\-time data capture capabilities will greatly simplify our data processing workflows. This integration will enable us to build analytical applications faster, giving us a competitive edge in the market.”


## What does it mean for the PeerDB project? [\#](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database#what-does-it-mean-for-the-peerdb-project)


The [PeerDB](https://github.com/PeerDB-io/peerdb) project remains under ELv2 license and open to contributions. Furthermore, we are thrilled to announce that we are also releasing [PeerDB Enterprise](https://github.com/PeerDB-io/peerdb-enterprise), currently a commercial, proprietary product featuring production\-grade Helm charts, under the same free and open ELv2 license. This allows any PeerDB user to easily run self\-managed production\-grade CDC workloads with PeerDB going forward.


## What does it mean for the PeerDB Cloud offering? [\#](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database#what-does-it-mean-for-the-peerdb-cloud-offering)


ClickHouse Cloud already comes with its very own dedicated data ingestion platform, aka ClickPipes. ClickPipes is an integration engine that simplifies data ingestion from a variety of sources, including Apache Kafka, Amazon S3, and Google Cloud Storage. As of today, ClickPipes has already been used to reliably and efficiently move more than 1 trillion rows to ClickHouse Cloud.


By joining forces with PeerDB, we’ll add a new connector to enable the Postgres CDC use\-case in ClickPipes, powered by PeerDB. This will be fully integrated into the ClickHouse Cloud experience and will benefit from the same foundations in terms of scalability, monitoring, and infrastructure.


We understand that data\-engineering changes can take time to implement. For this reason, we decided to set the end\-of\-life (EOL) of PeerDB Cloud for existing paid customers using non\-ClickHouse Cloud connectors to be one year from now, i.e. July 30th, 2025\. This is to ensure that organizations that bet on PeerDB technology early on and helped make it a success have sufficient time to plan for an orderly transition. Customers will receive the same support and SLAs as promised in their contracts, and we will assist them with personalized transition plans when needed.


## I want to set up Postgres CDC to ClickHouse Cloud, do I need to wait for the Postgres CDC for ClickPipes to be available? [\#](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database#i-want-to-set-up-postgres-cdc-to-clickhouse-cloud-do-i-need-to-wait-for-the-postgres-cdc-for-clickpipes-to-be-available)


No, you can already sign up to the PeerDB Cloud offering as of today and connect your Postgres database to ClickHouse Cloud. We plan to continue offering this service on its existing terms for users who want to start onboarding straight away. This includes a one\-month free trial.


![peerdb_demo.gif](/uploads/peerdb_demo_b642a3ae51.gif)
Once an equivalent Postgres CDC connector for ClickPipes is generally available, we’ll allow some time for the PeerDB Cloud users to stop their legacy pipelines and declare them again in ClickPipes for Postgres CDC, where they can benefit from the full eco\-system of connectors and ClickHouse Cloud features.


## What’s next? [\#](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database#whats-next)


While we are very excited about bringing Postgres CDC capabilities to Clickhouse Cloud, it does not stop here and the PeerDB foundations are solid and extensible. After integrating the Postgres CDC capability we plan to expand the connector catalog of source CDC connectors to other types of databases. This will be driven primarily by demand and we would love [to get your feedback](https://clickhouse.com/company/contact) about which CDC source connector we should add next.


## Get in touch! [\#](/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database#get-in-touch)


As always, the ClickHouse team would be honored to have the opportunity to partner with you. Whether you're using PeerDB today or are interested in efficient Postgres CDC capabilities, please [contact us!](https://clickhouse.com/company/contact)

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
