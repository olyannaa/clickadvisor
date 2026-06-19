---
source: blog
url: https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector
topic: postgres-cdc-connector-for-clickpipes-is-now-in-public-beta
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 4
---

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
