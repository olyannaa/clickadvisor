---
source: blog
url: https://www.adevinta.com/
topic: serving-real-time-analytics-across-marketplaces-at-adevinta-with-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 4
---

# Serving Real\-Time Analytics Across Marketplaces at Adevinta with ClickHouse Cloud

\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Serving Real\-Time Analytics Across Marketplaces at Adevinta with ClickHouse Cloud

![photo-elissa-weve.jpeg](/_next/image?url=%2Fuploads%2Fphoto_elissa_weve_4e4a809bed.jpeg&w=96&q=75)[Elissa Weve](/authors/elissa-weve)Apr 24, 2023 · 6 minutes read[Adevinta](https://www.adevinta.com/), a leading online classifieds specialist, operates more than 25 platforms across 11 countries worldwide. Their household brands include Marktplaats in the Netherlands, Mobile.de in Germany, and Leboncoin in France, reaching hundreds of millions of people every month. These platforms are all about matchmaking, and help people find whatever they’re looking for in their local communities – whether it’s a car, an apartment, a sofa, or a new job. Every connection made or item found makes a difference by creating a world where people share more and waste less.

Adevinta’s mission is to provide the best user experience for buying and selling goods and services online. To achieve this objective, Adevinta required a centralized analytics and dashboarding tool to monitor their seller's advertisements, track interactions, and improve performance in real\-time. After assessing various cloud\-based database services like Google BigQuery, Cloud Spanner, and ClickHouse Cloud, they determined that ClickHouse Cloud was the most cost\-effective option that could provide high performance and scalability across multiple marketplaces.

## User\-Facing Real\-Time Analytics and Dashboarding for Sellers [\#](/blog/serving-real-time-analytics-across-marketplaces-at-adevinta#user-facing-real-time-analytics-and-dashboarding-for-sellers)

Adevinta’s Central Data Products team is tasked with building data and machine learning (ML) products to support their various marketplaces. To start with, they focus on specific marketplace problems, devise data solutions, and subsequently expand and scale to other marketplaces. This presents a complex challenge, as they need to constantly consider aspects such as reusability, uptime, and scalability.

To meet the needs of their sellers, Adevinta required a [user\-facing real\-time analytics](https://clickhouse.com/resources/engineering/what-is-real-time-analytics) and dashboarding solution that would allow the sellers to monitor their advertisements in real\-time. This includes tracking views, favorites, and likes, capturing every interaction that occurs on their marketplaces.
