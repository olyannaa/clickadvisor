---
source: blog
url: https://clickhouse.com/cloud/clickpipes/mysql-cdc-connector)!
topic: mysql-cdc-connector-for-clickpipes-is-now-in-public-beta
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 4
---

# MySQL CDC connector for ClickPipes is now in Public Beta

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# MySQL CDC connector for ClickPipes is now in Public Beta

 Amogh BharadwajJul 17, 2025 · 6 minutes readWe’re excited to open up the [public beta of the MySQL CDC connector in ClickPipes](https://clickhouse.com/cloud/clickpipes/mysql-cdc-connector)! With just a few clicks, you can start streaming your [MySQL](https://clickhouse.com/docs/integrations/clickpipes/mysql/source/generic) data directly into [ClickHouse Cloud](https://clickhouse.cloud/). Simply head to the Data Source tab in your service, choose MySQL CDC, and walk through the guided setup.

The journey to this release started earlier this year. After celebrating our Postgres CDC launch in February, we turned our attention to MySQL—working closely with early users to shape the experience. By April 2025, we had a Private Preview live.
What followed exceeded our expectations. Customers adopted the connector quickly, pushing production workloads through it, offering sharp feedback, and syncing massive volumes of data from MySQL to ClickHouse. That hands\-on input has been invaluable in polishing the product—and now, we're ready to share it with everyone.

## Customer feedback [\#](/blog/mysql-cdc-connector-clickpipes-beta#customer-feedback)

Here’s what some of our reference customers have to say:

"Previously, our CDC workflows relied on a complex broker\-based streaming infrastructure. This approach was not only resource\-intensive but also required significant operational overhead. We've transitioned to using the MySQL CDC connector in ClickPipes, and the impact has been transformative. ClickPipes has allowed us to modernize our data pipeline, reduce maintenance costs, and focus on delivering value through analytics rather than infrastructure management. No more managing clusters, brokers, or custom connectors \- ClickPipes just works out of the box." \-\- [BrainRocket](https://www.brainrocket.com/)

"ClickPipes MySQL CDC connector has been an excellent tool for us to stream our data into Clickhouse . It offered reliable, real\-time replication with about a one\-minute delay. It was simple to set up, cost\-effective, handled both historical and ongoing sync smoothly, and supported private VPC networking to keep our data secure. ClickPipes, paired with ClickHouse Cloud, gives us true real\-time analytics without the complexity. It just works!" \- [NOCD](https://www.treatmyocd.com/)
