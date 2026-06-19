---
source: blog
url: https://clickhouse.tech/docs/en/engines/table-engines/integrations/kafka/
topic: collecting-semi-structured-data-from-kafka-topics-using-clickhouse-kafka-engine
ch_version_introduced: '2003.02769'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 4
---

# Collecting Semi\-structured Data from Kafka Topics Using ClickHouse Kafka Engine

\-\>Scroll to topBack- [Blog](/blog)
- /
- [User stories](/blog?category=user-stories)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Collecting Semi\-structured Data from Kafka Topics Using ClickHouse Kafka Engine

![superlogy.webp](/_next/image?url=%2Fuploads%2Fsuperlogy_583eb189cf.webp&w=96&q=75)Marijan RalasicJun 15, 2022 · 6 minutes read*We’d like to welcome Marijan Ralasic*, *Data Architect at Superology, as a guest to our blog. Read on to find out how Superology is using ClickHouse alongside Kafka to power customer quantitative data.*

Superology is an experienced product tech company. Since 2012, we have been innovating in the sports betting industry. Being acquired by Superbet group in 2017, we became one of the leading forces in the industry. Today, our platforms are used by hundreds of thousands of people and process millions of transactions daily. To satisfy user needs and accomplish business goals, we use a data\-informed approach at every level of work.

We value personal growth as much as we value company growth. That’s why we don’t follow the traditional corporate model but empower our people to deploy their talents and own their work end\-to\-end.

## **Collecting customer quantitative data** [\#](/blog/collecting-semi-structured-data-from-kafka-topics-using-clickhouse-kafka-engine#collecting-customer-quantitative-data)

Quantitative data is something that businesses can easily count or measure, concrete and unbiased data points. Superology uses quantitative data to create reports, analyze it using statistical tools, and create randomized experimentation processes. Quantitative data from the Superology perspective includes metrics such as counting the number of app or site visits, customer clicks on specific pages, number of comments and followers in our social section, and various conversion events and bounce rates. We use this data to modify our customer experience to increase the satisfaction and usefulness of our application. We want to achieve the best experience for people wanting to find sports statistics, engage in social actions and overall enjoy the sports entertainment industry.

![example4.webp](/uploads/example4_b9b3be0d41.webp)
## **Google protobuf** [\#](/blog/collecting-semi-structured-data-from-kafka-topics-using-clickhouse-kafka-engine#google-protobuf)
