---
source: blog
url: https://www.ongage.com/
topic: ongage-s-strategic-shift-to-clickhouse-for-real-time-email-marketing
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 6
---

relied heavily on a large MySQL cluster, managed and operated by AWS RDS. As their data volumes increased, the limitations of MySQL started to surface. The performance sharply declined and the analytics page load times became too long.

ClickHouse entered the picture, offering a significant leap in data processing real\-time analytics capabilities. MySQL is still retained for handling transaction data that doesn’t grow significantly, and is used to enrich data in ClickHouse with details such as account and campaign names.

One of the key elements that eased this transition was ClickHouse's built\-in MySQL engine. This feature enabled the Ongage team to extract data from MySQL and convert it into ClickHouse's native table format effortlessly. The MySQL engine was used not just to query data, but also to facilitate a smooth migration into ClickHouse.

## Why ClickHouse Overcame SingleStore in Ongage's Assessment [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#why-clickhouse-overcame-singlestore-in-ongages-assessment)

When selecting a data management solution, the team at Ongage didn't just go with the first option. They explored various solutions, SingleStore being a prime contender. During an in\-depth evaluation, they stacked SingleStore against ClickHouse, considering storage costs and specific feature availability.

From a cost perspective, ClickHouse presented a far more economical choice. SingleStore storage costs were six times more than those of ClickHouse Cloud for identical data volumes. Considering Ongage's data\-intensive operations, this meant a considerable expense.

In terms of feature offerings, ClickHouse offers a clear advantage that SingleStore lacks \- the implementation of Materialized Views. This feature is a major timesaver as it facilitates aggregating a substantial number of events into a smaller, more manageable table. This, in turn, speeds up query execution considerably.

Nevertheless, it's worth noting that SingleStore might be a more suitable fit for organizations prioritizing transactional capabilities. As Ongage specifically sought real\-time analytics, this wasn't one of the factors for them. ClickHouse clearly emerged as the champion, considering the specific needs and plans Ongage had.

## The Decision: Why ClickHouse Cloud? [\#](/blog/ongages-strategic-shift-to-clickhouse-for-real-time-email-marketing#the-decision-why-clickhouse-cloud)

Ongage's decision to use ClickHouse Cloud over the open\-source self\-managed option was influenced by several key factors.
