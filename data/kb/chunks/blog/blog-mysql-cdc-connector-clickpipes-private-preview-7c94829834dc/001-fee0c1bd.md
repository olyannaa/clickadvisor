---
source: blog
url: https://www.mysql.com/
topic: mysql-cdc-connector-for-clickpipes-is-now-in-private-preview
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 3
---

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
