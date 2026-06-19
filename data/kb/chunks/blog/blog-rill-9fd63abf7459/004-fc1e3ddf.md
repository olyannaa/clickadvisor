---
source: blog
url: https://www.rilldata.com/
topic: rill-and-clickhouse-real-time-operational-bi-for-a-metered-world
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 6
---

easy it is to launch ClickHouse on your local machine," he said, noting that, like ClickHouse, Rill lets developers start a local instance that runs in the browser, connecting to either a local ClickHouse database or [ClickHouse Cloud](https://clickhouse.com/cloud).

The demo centered around three core building blocks inside Rill: sources, metrics, and dashboards. Mike began by loading roughly a million rows of Google Cloud usage data from a Parquet file. He then used an agent\-assisted workflow to generate the YAML configuration needed to ingest the dataset into ClickHouse.

Once connected, Rill analyzed the table structure and generated metric definitions and dashboards automatically. Within seconds, he could explore cloud spending trends—drilling into services, zooming across time ranges, and slicing costs by dimension—all backed by ClickHouse queries. "What's great is how easy and fast it is," Mike says.

With Rill, developers can use AI\-assisted coding tools to define configurations as code. In his demo, Mike used Cursor to generate ingestion syntax, adjust formatting, and modify dashboards. Tasks that once required extensive UI configuration, like changing currency formatting across dashboards, can be done in seconds. "That's the difference between BI\-as\-clicks and BI\-as\-code," he says.

As Mike explained, development happens locally first. Teams iterate against small data partitions, validate metrics, and commit changes to Git before deploying to the cloud. Once deployed, the same definitions power conversational analytics layered on top of the data.

Mike demonstrated this by asking natural\-language questions about cost increases across cloud providers. While conversational BI, he notes, has become relatively common ("everyone's seen a demo of a chatbot slapped over some data"), he emphasized two constraints that determine whether it actually works in practice.

First, text\-to\-SQL approaches don't always scale in real production environments. "If you've got hundreds of tables, you just see the agent get lost," Mike says. "It's like throwing a data engineer at a problem and saying, 'Hey, figure out why our cloud costs are up.'"

Second, interaction speed matters as much as correctness. "You've got to have high performance in the back end," he says. "If you were to throw Rill at [Snowflake or Redshift or BigQuery](https://clickhouse.com/resources/engineering/top-5-cloud-data-warehouses), the answers would just take forever to come back."
