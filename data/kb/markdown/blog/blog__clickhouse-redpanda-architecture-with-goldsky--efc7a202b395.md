# Goldsky \- A Gold Standard Architecture with ClickHouse and Redpanda


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Goldsky \- A Gold Standard Architecture with ClickHouse and Redpanda

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Dec 20, 2023 · 12 minutes read## Introduction [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#introduction)


As a company rooted in open\-source, we find our users are often the first to identify and develop new architectural patterns or applications for the technology. While we may be experts in ClickHouse, it's virtually impossible for us to try all possible integration technologies or experiment with all datasets representative of all use cases. Whenever we conduct a customer interview, we're therefore always excited to hear about emerging deployment patterns, especially with other popular OSS projects. Upon speaking with our customer Goldsky and hearing of such a pattern, we decided to share their deployment architecture for Redpanda, Apache Flink, and ClickHouse. We see this as having potentially broad applications for those users who need to deliver transformed subsets of a dataset to a number of end customers.


**To highlight the capabilities of this architecture, Goldsky has generously shared data from the widely\-used blockchain Base on a publicly accessible ClickHouse instance. This enables users interested in developing features, products, or platforms with blockchain data to easily create a Proof of Concept using this free and continually updated data source, thanks to the Goldsky platform. By eliminating concerns about ingest pipelines, infrastructure setup, or managing costs associated with direct use of this data through BigQuery, we aim for this proof of concept to serve as a valuable illustration of the efficiency achieved when leveraging ClickHouse and Goldsky for blockchain analytics.**


## Goldsky [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#goldsky)


Goldsky provides crypto data as a service, delivering data from more than 15 of the most popular blockchains to customers' own datastores. This includes blockchain indexing, subgraphs, and data streaming pipelines. By providing the ability for developers to create simple APIs, this data can be exposed in powerful dApps (decentralized applications) without the complexity of needing to concern themselves with the required infrastructure, data management and logic to extract useful information. Typically, the former involves a remote procedure call (RPC) providers and APIs which are complex and challenging to model.


By providing a “data\-pipelines\-as\-a\-service,” Goldsky allows blockchain data to be filtered and transformed by customer\-specific logic, such that only a specific subset of a blockchain is delivered to a smart API endpoint. While users usually expose API endpoints on the data delivered by Goldsky, ClickHouse is increasingly seen as the preferred analytics database should more complex querying be required. In this case, Goldsky needs to deliver a blockchain dataset to a dedicated ClickHouse (often Cloud) cluster. This dataset will often be a subset of a specific blockchain e.g. all blocks pertaining to a specific address or the balance of a wallet. As well as filtering, or only starting the stream from a specific time point, users additionally need the capability to pre\-aggregate data prior to insertion to ClickHouse.


While these processing capabilities are all built into the Goldsky service, this presented a challenge from a data engineering perspective \- how to efficiently stream the same TiB datasets to potentially 10s of thousands of ClickHouse instances while providing customer\-independent processing that may target only subsets.


## Architecture [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#architecture)


![gold_sky_architecture.png](/uploads/gold_sky_architecture_8455529196.png)
The Goldsky architecture consists of Redpanda, Apache Flink and ClickHouse. Data is pushed into Redpanda via direct indexers which can extract structures such as blocks, transactions, traces and logs. Each blockchain exists as multiple topics on Redpanda (one for each data type), from which Apache Flink can consume and transform events. Users write FlinkSQL to transform specific datasets, potentially starting from a specific position on the topic to time limit the data. Transformations are applied in stream before the data is delivered to ClickHouse for analytics. This multi\-tenant architecture allows Goldsky to efficiently process and deliver any crypto dataset to potentially thousands of ClickHouse clusters. All of this is exposed through a simple interface or API, abstracting the complexity and allowing the users to simply write transformations naturally in SQL.



> Readers may notice the subgraph module above. Subgraphs are a single\-threaded method of indexing that allows for users to write webassembly logic that process the blockchain sequentially using typescript. This allows for custom aggregations by reading and writing state, which can be an easier paradigm to start with. This also allows for additional HTTP calls to the ethereum network to pull contract state during the indexing process. These subgraphs can in turn be used to expose an API or inserted to ClickHouse for analytics. Further details [here](https://docs.goldsky.com/mirror/sources/subgraphs).


We explore each of these technology choices below.


### Redpanda as a backing store [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#redpanda-as-a-backing-store)


Goldsky expended significant effort ensuring all popular blockchains are transformed into a format which can realistically be easily consumed by other services such as ClickHouse. The schema\-driven Avro format represents their current preferred format. Once a blockchain has been transformed, there are several primary challenges:


- Efficient storage of the transformed data for later consumption by customers. The retention period here is infinite
- Keeping this data up\-to\-date such that users can enjoy access to the latest transactions and blocks
- Ensuring the data can be delivered with minimal end\-to\-end latency to any number of destinations, including ClickHouse


Since all blockchain data is inherently time\-series, ordered, and immutable, and with prior experience of Kafka, the Goldsky team identified Redpanda as the preferred Kafka implementation. The principal motivation behind this choice was its [tiered storage architecture](https://docs.redpanda.com/current/manage/tiered-storage/). This allows data to be retained cost\-efficiently on object storage while still delivering data at GiB/sec to downstream destinations, rather than paying for hardware that's not required in traditional Kafka shared\-nothing architectures. When combined with a high\-level of durability, verified by recent [Jepsen tests](https://redpanda.com/blog/redpanda-official-jepsen-report-and-analysis), this feature specifically aligns with the access patterns typical for Goldsky i.e. more recent blocks are of principal interest and data needs to be streamed in sequential order.


For more details on Goldsky’s choice of Redpanda, we recommend the blog ["How Goldsky democratizes streaming data for Web3 developers with Redpanda"](https://redpanda.com/blog/democratize-streaming-data-web3-goldsky-redpanda).


### Apache Flink for processing [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#apache-flink-for-processing)


To satisfy their user requirement to be able to filter and transform data, Goldsky utilize Apache Flink® \- exposing FlinkSQL to their users. While post transformations are simple e.g. filtering data to a specific contract, Flink provides more complex stream processing capabilities such as instream Joins, TopN counts and even [pattern recognition](https://nightlies.apache.org/flink/flink-docs-release-1.17/docs/dev/table/sql/queries/match_recognize/) if required. These features are provided while still maintaining high insertion performance to ClickHouse, with rates reaching 500k events/sec.


For more details on Goldsky’s choice of Flink, we recommend the blog [“Using Changelogs and Streams to Solve Blockchain Data Challenges”](https://goldsky.com/blog/changelogs-streams-blockchain-data), especially with respect to how blockchain reorgs can be efficiently handled.


### ClickHouse for analytics [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#clickhouse-for-analytics)


While ClickHouse is not the only database users request events to be delivered to, it represents the principal choice once query analytics are needed to be performed on large datasets. ClickHouse’s application to the field of crypto analytics is well known, with users exploiting its unrivaled query performance, cost efficiency and enhanced SQL for datasets, which often reach the TiB. Querying blockchain data with SQL is intuitive and popularized by services such as [dune](https://dune.com/docs/data-tables/raw/solana/blocks/).


### ClickHouse for backfills [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#clickhouse-for-backfills)


More recently, Goldsky has begun exploring using ClickHouse for backfilling data. This is often a requirement for customers who need a complete or filtered set of the data. In these cases, ClickHouse can be used to efficiently identify the subset and redirect to the Goldsky pipeline. Redpanda can be used for subsequent updates. This was implemented using a custom hybrid source, which is capable of consuming data from both sources: ClickHouse for the backfill and Redpanda for the incremental. Any aggregations defined in the pipeline would work across both ClickHouse and Redpanda without the user having to know where the data comes from.


## Challenges \& lessons [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#challenges--lessons)


Goldsky’s principal challenge with ClickHouse involved the use of the [ReplacingMergeTree](https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1) engine type, and learning how to use it optimally. This engine choice ensures that updates (or duplicate events) can be efficiently handled. For optimization purposes, Goldsky specifically exploits:


- The ability to [emulate the PREWHERE condition](https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1#final-performance) for the ReplacingMergeTree
- Utilizes partitions for [efficient querying](https://clickhouse.com/blog/clickhouse-postgresql-change-data-capture-cdc-part-1#exploiting-partitions)
- Recent abilities to [control the number of threads](https://clickhouse.com/docs/en/operations/settings/settings#max-final-threads) to use for the FINAL operator


Furthermore, Goldsky provides the ability for users to customize their `ORDER BY` key to align with their access patterns. This is typically a block timestamp or an address. In future, they hope to exploit the support for [projections for the ReplacingMergeTree engine](https://github.com/ClickHouse/ClickHouse/issues/33678).


### An example dataset [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#an-example-dataset)


At ClickHouse, we are always looking for large datasets to expose in our public instances. Keen to test the Goldsky service, we were excited by Goldsky’s offer to send a blockchain to one of our public instances. Looking for a well adopted chain with a significant number of transactions, we settled on Base.


The Base blockchain is a decentralized ledger based on Ethereum L2\. It utilizes a unique consensus mechanism called "Proof of Participation" that combines elements of Proof of Stake and Proof of Work, allowing for efficient transaction processing and consensus while maintaining robust security. This blockchain incorporates features such as smart contracts and decentralized applications (DApps) to support a wide range of use cases, making it a versatile platform for blockchain\-based applications and services. Promoted by Coinbase, this chain also has strong adoption with almost 72 million transactions as of the time of writing.


Users can access this dataset, which is updated in real\-time, at [sql.clickhouse.com](https://sql.clickhouse.com). We offer tables for blocks, logs, transactions, and traces which range from less than 10m rows and a few GiB to over 1 billion and almost 1TiB uncompressed.



```
SELECT
    table,
    formatReadableQuantity(sum(rows)) AS total_rows,
    round(sum(rows) / 42) AS events_per_day,
    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size,
    round(sum(data_uncompressed_bytes) / sum(data_compressed_bytes), 2) AS ratio
FROM system.parts
WHERE (database = 'base') AND active
GROUP BY table
ORDER BY sum(rows) ASC

┌─table───────────────┬─total_rows─────┬─events_per_day─┬─compressed_size─┬─uncompressed_size─┬─ratio─┐
│ base_blocks         │ 7.46 million   │         177546 │ 2.11 GiB        │ 7.60 GiB          │  3.61 │
│ base_transactions   │ 72.89 million  │        1735559 │ 7.02 GiB        │ 56.19 GiB         │     8 │
│ base_decoded_logs   │ 405.76 million │        9660852 │ 22.03 GiB       │ 336.46 GiB        │ 15.27 │
│ base_raw_logs       │ 408.87 million │        9734901 │ 13.53 GiB       │ 216.64 GiB        │ 16.01 │
│ base_decoded_traces │ 1.14 billion   │       27151103 │ 51.70 GiB       │ 1.04 TiB          │ 20.64 │
│ base_raw_traces     │ 1.25 billion   │       29687205 │ 38.38 GiB       │ 816.71 GiB        │ 21.28 │
└─────────────────────┴────────────────┴────────────────┴─────────────────┴───────────────────┴───────┘

6 rows in set. Elapsed: 0.008 sec.

```

Users can perform analytics queries on the cluster with real\-time responses. For example, to count the number of transactions per day since June.



```
SELECT
    toStartOfDay(block_timestamp) AS day,
    COUNT(*) AS txns,
    ROUND(AVG(txns) OVER (ORDER BY day ASC ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)) AS `7d avg`
FROM base_transactions
WHERE day > '2023-07-12'
GROUP BY 1
ORDER BY 1 DESC

┌─────────────────day─┬────txns─┬──7d avg─┐
│ 2023-12-04 00:00:00 │  165727 │  252691 │
│ 2023-12-03 00:00:00 │  283293 │  270246 │
│ 2023-12-02 00:00:00 │  302197 │  275016 │
│ 2023-12-01 00:00:00 │  236117 │  277115 │
│ 2023-11-30 00:00:00 │  263169 │  286202 │
│ 2023-11-29 00:00:00 │  265525 │  290758 │

...

│ 2023-07-17 00:00:00 │   59162 │   62133 │
│ 2023-07-16 00:00:00 │   67629 │   62876 │
│ 2023-07-15 00:00:00 │   77912 │   61291 │
│ 2023-07-14 00:00:00 │   61859 │   52981 │
│ 2023-07-13 00:00:00 │   44103 │   44103 │
└─────────────────────┴─────────┴─────────┘

145 rows in set. Elapsed: 0.070 sec. Processed 72.90 million rows, 291.58 MB (1.04 billion rows/s., 4.15 GB/s.)

```


We recommend users explore the Dune dashboard [here](https://dune.com/watermeloncrypto/base), for query inspiration. Whereas Dune doesn’t provide real\-time query capabilities (0\.070s for above), its queries can easily be translated to ClickHouse syntax and executed on the above service.


## Conclusion [\#](/blog/clickhouse-redpanda-architecture-with-goldsky#conclusion)


We have presented Goldsky’s architecture in this post, exploring why they chose to use Redpanda, Apache Flink, and ClickHouse for their multi\-tenant deployment of ClickHouse. While streaming concepts naturally align to blockchain data and problems such as Top\-N, retractions, and time\-limited joins, ClickHouse can be used to further enhance this architecture by providing real\-time querying capabilities across either subsets or entire blockchains. Together these technologies naturally complement themselves and allow Goldsky to deliver a first\-in\-class blockchain analytics service. As proof of this service, and to the benefit of our community, we have utilized Goldsky to [offer analytics for free on the Base blockchain](https://sql.clickhouse.com). Stay tuned for efforts to expose other blockchains for free!

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
