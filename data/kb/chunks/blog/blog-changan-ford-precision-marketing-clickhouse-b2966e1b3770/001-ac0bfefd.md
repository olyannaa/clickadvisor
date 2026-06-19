---
source: blog
url: https://corporate.ford.com/operations/locations/global-plants/changan-ford-automobile-co-ltd-engine-plant.html
topic: how-changan-ford-cut-costs-by-40-and-powered-precision-marketing-with-clickhouse-enterprise-edition
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 6
---

# How Changan Ford cut costs by 40% and powered precision marketing with ClickHouse Enterprise Edition

\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How Changan Ford cut costs by 40% and powered precision marketing with ClickHouse Enterprise Edition

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Sep 22, 2025 · 9 minutes read[Changan Ford](https://corporate.ford.com/operations/locations/global-plants/changan-ford-automobile-co-ltd-engine-plant.html) was founded in 2001 as a joint venture between Changan Automobile Group, one of China’s largest automakers, and Ford Motor Company. In 2017, as part of its digital transformation strategy, the company established a digital marketing department and built a Customer Data Platform (CDP) to unify data from a wide range of online and offline, internal and external sources. With a complete view of each customer, frontline teams could run targeted marketing campaigns and deliver more personalized after\-sales services.

At first, the CDP ran on ClickHouse’s open\-source Community Edition, powering real\-time segmentation queries across trillions of rows. But as the platform grew, so did its demands. Storing seven years of historical data—over 100 TB—sent storage costs climbing. Traffic spikes during marketing campaigns strained the fixed\-resource cluster. Scaling had to be done manually, slowing the team down, and OOM errors became increasingly common.

In 2024, Changan Ford migrated to ClickHouse Enterprise Edition (also known as [ClickHouse Cloud](https://clickhouse.com/cloud)) on Alibaba Cloud. With compute\-storage separation, serverless elasticity, and OSS\-based storage, the new system cut costs by 40%, eased the operational workload, and gave the team stability and confidence even during their most demanding campaigns.

## A unified view of the customer [\#](/blog/changan-ford-precision-marketing-clickhouse#a-unified-view-of-the-customer)

Changan Ford’s digital marketing team relies on the CDP for everything from building detailed user profiles to running analytics, targeting ads, and segmenting audiences. To make that possible, they built a platform that collects data across three main categories:
