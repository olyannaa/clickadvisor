---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Postgres
topic: postgres-cdc-connector-for-clickpipes-is-now-in-private-preview-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 1
total_chunks_in_doc: 4
---

# Postgres CDC connector for ClickPipes is now in Private Preview \| ClickHouse

\[{"@context":"https://schema.org","@type":"BlogPosting","headline":"Postgres CDC connector for ClickPipes is now in Private Preview","description":"We are excited to announce that the Postgres CDC connector for ClickPipes is now in Private Preview. This enables customers to replicate their Postgres databases to ClickHouse Cloud in just a few clicks, eliminating the need for external ETL tools, which ","image":"/uploads/postgres\_cdc\_connector\_clickpipes\_private\_preview\_f06bd33c0b.png","publisher":{"@type":"Organization","name":"ClickHouse","url":"https://clickhouse.com/","logo":{"@type":"ImageObject","url":"https://clickhouse.com/\_next/static/immutable/media/icon1\.3b4swr1c2xvk2\.png"}},"datePublished":"2024\-11\-25T15:46:21\.517Z","dateModified":"2026\-03\-03T12:38:18\.703Z","author":{"@context":"https://schema.org","@type":"Person","name":"Sai Srirampur","url":"https://clickhouse.com/authors/sai\-srirampur","@id":"https://clickhouse.com/authors/sai\-srirampur\#person","image":"/uploads/display\_pic\_copy\_5b0aedef94\.jpeg"}}]\-\>Scroll to top\<\-Back- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/immutable/media/icon-markdown.2-p3ljls89_ww.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/immutable/media/icon-chatgpt.0aw932qxrira1.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/immutable/media/icon-claude.42qslf9ajhpwk.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/immutable/media/icon-v0.0mczhus58alob.svg)**Open in v0** Ask questions about this page
# Postgres CDC connector for ClickPipes is now in Private Preview

![Sai Srirampur](/_next/image?url=%2Fuploads%2Fdisplay_pic_copy_5b0aedef94.jpeg&w=96&q=75)[Sai Srirampur](/authors/sai-srirampur)Nov 25, 2024 · 6 minutes read![postgres-cdc-connector-clickpipes-private-preview.png](/_next/image?url=%2Fuploads%2Fpostgres_cdc_connector_clickpipes_private_preview_f06bd33c0b.png&w=2048&q=75)

Today, we’re excited to announce the private preview of the Postgres Change Data Capture (CDC) connector in ClickPipes! This enables customers to replicate their Postgres databases to ClickHouse Cloud in just a few clicks and leverage ClickHouse for blazing\-fast analytics. You can use this connector for both continuous replication and one\-time migrations use cases from Postgres.

The experience is natively integrated into ClickHouse Cloud through ClickPipes, the integration engine designed to simplify moving massive volumes of data to ClickHouse. This eliminates the need for external ETL tools, which are often expensive, slow, and don’t scale for Postgres.

**[You can sign up to the private preview by following this link](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector)**.

Just a reminder, ClickHouse [joined forces](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database) with PeerDB, a leading Change Data Capture (CDC) provider for Postgres, a few months ago. PeerDB already supports multiple enterprise\-grade workloads and has helped replicate petabytes of data from Postgres to ClickHouse. Over the past few months, the team has worked hard to natively integrate PeerDB into ClickHouse Cloud. This announcement marks the first release of this integration, enabling users to seamlessly move data from Postgres to ClickHouse.

The Postgres CDC connector was built in close collaboration with several customers and design partners who are already running production\-grade workloads. Here are a few customer testimonials:
