# Enhancing Postgres to ClickHouse replication using PeerDB


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Enhancing Postgres to ClickHouse replication using PeerDB

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)Aug 14, 2024 · 7 minutes read![peerdb_postgres_cdc_blog.png](/uploads/peerdb_postgres_cdc_blog_918fcebb10.png)
Providing a fast and simple way to replicate data from [Postgres](https://www.postgresql.org/) to ClickHouse has been a top priority for us over the past few months. Last month, we [acquired](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database) [PeerDB](https://www.peerdb.io/), a company that specializes in Postgres CDC. We're actively integrating PeerDB into [ClickPipes](https://clickhouse.com/cloud/clickpipes) to add Postgres as a source connector. Meanwhile, [PeerDB](https://www.peerdb.io/) is the recommended solution for moving data from Postgres to ClickHouse.


In the past few months, the PeerDB team had the opportunity to work with multiple ClickHouse customers, helping them replicate billions of rows and terabytes of data from Postgres to ClickHouse. In this blog, we will take a deep dive into some of the top features that were released recently to make the replication experience rock\-solid. These features focus on enhancing the speed, stability, and security of replication from Postgres to ClickHouse.


## Efficiently flush the replication slot [\#](/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#efficiently-flush-the-replication-slot)


PeerDB uses Postgres Logical Replication Slots to implement Change Data Capture (CDC). Logical Replication Slots provide a stream of INSERTs, UPDATEs, and DELETEs occurring in the Postgres database. It is recommended to [always consume the replication slot](https://blog.peerdb.io/overcoming-pitfalls-of-postgres-logical-decoding#heading-always-consume-the-replication-slot). If the replication slot isn't consumed continuously, WAL files can accumulate, posing a risk of crashing the Postgres database.


To ensure that the logical replication slot is always consumed, we implemented a [feature](https://github.com/PeerDB-io/peerdb/pull/1780) to always read the replication slot and flush the changes to an internal stage (S3\). An asynchronous process then consumes the changes from S3 and applies them to ClickHouse. Flushing the changes to the internal stage ensures S3 also ensures that replication slot is consumed even when the target (ClickHouse) is down.


## Better memory handling on ClickHouse [\#](/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#better-memory-handling-on-clickhouse)


While replicating data from Postgres to ClickHouse, customers occasionally ran into memory\-related issues on ClickHouse. This was more common when customers were on a free trial of ClickHouse and provisioned an instance with fewer resources (RAM and compute). PeerDB writes rows in batches to ClickHouse via `INSERT` queries and `INSERT SELECT` queries. We were seeing 2 types of issues:


1. Some queries were failing because they were consuming more memory than allocated on the ClickHouse server.
2. Some queries would be killed by [ClickHouse's overcommit tracker.](https://clickhouse.com/docs/en/operations/settings/memory-overcommit)


We attempted to thoroughly understand the various [database settings](https://clickhouse.com/docs/en/operations/settings/settings) that ClickHouse provides, which influence memory utilization. Based on this, we [modified](https://github.com/PeerDB-io/peerdb/pull/1728) the following settings:


1. [`max_block_size`](https://clickhouse.com/docs/en/operations/settings/settings#setting-max_block_size): This is useful for our `INSERT SELECT` queries, where this setting determines how many blocks are loaded by the `SELECT` and inserted. We reduced this with the hope that more blocks would reduce memory spikes when our queries are executed.
2. [`max_insert_block_size`](https://clickhouse.com/docs/en/operations/settings/settings#max_insert_block_size): Similar to `max_block_size` except this applies to our `INSERT` queries. We reduced this for the same reason as above.
3. [`max_threads`](https://clickhouse.com/docs/en/operations/settings/settings#max_threads): This setting controls the number of threads used for processing queries on ClickHouse. According to the documentation, the lower this number, the less memory is consumed. Therefore, we reduced this parameter.
4. [`memory_overcommit_ratio_denominator`](https://clickhouse.com/docs/en/operations/settings/memory-overcommit#user-overcommit-tracker): This is related to the overcommit tracker mentioned earlier. We disabled this setting for our queries by setting it to 0\.
5. [`dial_timeout`](https://clickhouse.com/docs/en/integrations/go#connection-settings-1): Sometimes queries were taking longer than 1 minute, so we [increased the `dial_timeout`](https://github.com/PeerDB-io/peerdb/pull/1772) to a higher value.


These changes drastically reduced memory\-related issues on smaller ClickHouse clusters. We are actively working with the core team to further fine\-tune ClickHouse\-specific settings. Additionally, we are working on a [feature](https://github.com/PeerDB-io/peerdb/pull/1770) that improves the handling of large datasets by breaking them into manageable parts for more efficient processing and storage.


## Row\-level transformations [\#](/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#row-level-transformations)


A few months ago, PeerDB shipped [Lua\-based row\-level transformations](https://blog.peerdb.io/row-level-transformations-in-postgres-cdc-using-lua) while replicating data from Postgres to Queues such as Kafka. We have now extended this feature to ClickHouse. With this feature, customers can write simple Lua scripts to perform row\-level transformations, enabling use cases such as masking PII data, generating columns, and more. Below is a quick demo of this feature to mask PII columns while replicating data from Postgres to ClickHouse:



## Improved security on PeerDB Cloud [\#](/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#improved-security-on-peerdb-cloud)


At PeerDB, safeguarding data replication from Postgres to ClickHouse is crucial. To enhance security, we have implemented several key measures around AWS S3, which we use for internally staging data before pushing it to ClickHouse.


### Temporary credentials with IAM roles [\#](/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#temporary-credentials-with-iam-roles)


One significant enhancement is the use of AWS S3 buckets with strict access controls. Instead of traditional, long\-lived user\-generated access keys, which pose a higher risk of compromise, we use IAM roles to generate temporary credentials. These credentials are automatically rotated by AWS, ensuring they are always up\-to\-date and valid for only short periods, thus minimizing the risk of unauthorized access.


Additionally, with the introduction of the AWS\_SESSION\_TOKEN parameter in ClickHouse version 24\.3\.1, our security practices have been further strengthened. This update allows the use of short\-lived credentials, aligning with our approach to secure data replication.


### Attribute Based Access Control (ABAC) [\#](/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#attribute-based-access-control-abac)


In a multi\-tenant environment, managing access to S3 buckets poses several challenges, such as ensuring tenant isolation, preventing unauthorized access, and minimizing role proliferation. To address these issues, we employ **Attribute Based Access Control** (ABAC). ABAC allows us to define dynamic, fine\-grained access policies based on user roles, resource tags, and environmental variables. This method not only provides enhanced security but also improves scalability by eliminating the need for creating numerous roles. By using ABAC, we ensure that only authorized components can access sensitive data, maintaining a secure and manageable system.


## Conclusion [\#](/blog/enhancing-postgres-to-clickhouse-replication-using-peerdb#conclusion)


Hope you enjoyed reading the blog. PeerDB has spent multiple cycles hardening Postgres CDC experience to ClickHouse and is now supporting multiple customers in replicating billions of records in real\-time from Postgres to ClickHouse. If you want to give PeerDB and ClickHouse a try, please check out the links below or reach out to us directly!


1. [Try PeerDB Cloud for Free](https://auth.peerdb.cloud/signup)
2. [Try ClickHouse Cloud for Free](https://clickhouse.com/docs/en/cloud-quick-start)
3. [Docs on Postgres to ClickHouse Replication](https://docs.peerdb.io/mirror/cdc-pg-clickhouse)
4. [Talk to the PeerDB team directly](https://www.peerdb.io/sign-up)
[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
