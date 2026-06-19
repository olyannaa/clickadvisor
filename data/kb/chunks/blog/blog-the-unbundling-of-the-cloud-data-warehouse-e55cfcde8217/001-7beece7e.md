---
source: blog
url: https://clickhouse.com/resources/engineering/how-to-choose-a-database-for-real-time-analytics-in-2026
topic: the-unbundling-of-the-cloud-data-warehouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 11
---

# The Unbundling of the Cloud Data Warehouse

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# The Unbundling of the Cloud Data Warehouse

![TanyaBragin.jpeg](/_next/image?url=%2Fuploads%2FTanya_Bragin_84bf5232c3.jpeg&w=96&q=75)[Tanya Bragin](/authors/tanya-bragin)Nov 7, 2023 · 18 minutes readWe owe a lot to the cloud data warehouses, but their era of hegemony is coming to an end.

Over the last 10 years, companies like Snowflake modernized a whole industry, which previously relied on a closed and proprietary ecosystem of self\-managed deployments (powered by Oracle, Teradata, and the like). They enabled organizations to move petabytes of critical workloads to the cloud, opening up these datasets to a wider range of integrations, collaboration, and applications – democratizing access to data and dramatically increasing its value.

Over time, businesses began to examine their data stores more closely, considering both the nature of the information contained within and the potential utility that could be derived. With organizational data now more readily available, development teams transitioned from static batched reporting to constructing interactive applications—both for internal use and external distribution.

However, here is where they started running into challenges. Because cloud data warehouses are designed for offline reporting (just now running on cloud infrastructure), their architecture and pricing models are not optimized to serve as the backend for interactive, data\-driven applications. So organizations end up with poor performance (10s of seconds to minutes response time, instead of sub\-second and milliseconds), skyrocketing costs (often 3\-5x compared to alternatives), and low query concurrency (unfit for externally\-facing applications).

As a result, organizations have turned to the [***real\-time analytics databases***](https://clickhouse.com/resources/engineering/how-to-choose-a-database-for-real-time-analytics-in-2026) optimized to power data\-intensive applications. The adoption and operationalization of these real\-time analytics databases over time has led to a new architectural pattern that we term the ***real\-time data warehouse***. Below, we describe why a traditional data warehouse is not designed for the needs of real\-time analytical applications, and how a real\-time data warehouse addresses these challenges as well as leads to an architectural shift to “unbundle the cloud data warehouse.”

## Traditional data warehouse: one size does not fit all [\#](/blog/the-unbundling-of-the-cloud-data-warehouse#traditional-data-warehouse-one-size-does-not-fit-all)
