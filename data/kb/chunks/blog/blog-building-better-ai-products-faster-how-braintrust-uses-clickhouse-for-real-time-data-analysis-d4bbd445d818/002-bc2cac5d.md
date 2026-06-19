---
source: blog
url: https://www.braintrust.dev?utm_source=clickhouse
topic: building-better-ai-products-faster-how-braintrust-uses-clickhouse-for-real-time-data-analysis
ch_version_introduced: '5.1'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 5
---

his first company, Impira, in 2017. It used machine learning to help companies extract and manage unstructured data such as documents, videos, images, audio, and webpages. After selling the business to Figma, he took over Figma’s AI team.

“At both Impira and Figma, it was really, really hard for us to make changes to our AI products without breaking everything,” Ankur says.

To overcome this challenge, Ankur built internal toolkits at both companies, using evaluations to systematically test and validate AI models. This process included rigorous logging, performance tracking, output visualization, and failure analysis to enable ongoing improvements without inadvertently breaking other parts of the system.

Then in 2023, Ankur was talking to investor and entrepreneur Elad Gil who steered him to an important realization.

“He was like, ‘Hey, you’ve built the same thing twice,’” Ankur recalls. “‘Other companies are trying to do AI stuff. Maybe they have this problem, too.’”

Ankur began talking to other software developers who were building AI-enabled products. He soon realized there was a widespread need for an enterprise-grade stack that could allow AI companies to evaluate and improve their products faster and more reliably. He raised $5.1 million in seed funding and got to work building Braintrust.

## In Search of Efficiency [#](/blog/building-better-ai-products-faster-how-braintrust-uses-clickhouse-for-real-time-data-analysis#in-search-of-efficiency)

At Figma, Ankur had experienced the limitations of traditional cloud data warehouses for building real-time data driven applications. Over a yearlong period, the data team had engineered a pipeline that took five minutes to process data from an experiment and make it queryable. While impressive compared to other companies where a process like this might take an hour or more, it wasn’t nearly fast enough for the interactive analysis required in modern AI development.

As he began building Braintrust, Ankur recognized the need for a more efficient database that could process large volumes of data with minimal latency. His search led him to ClickHouse, an open-source columnar database management system known for its high performance and low-latency capabilities. Right away he saw that ClickHouse’s ability to process complex queries with minimal delay was essential to meeting the demands of AI companies.
