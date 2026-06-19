# Real\-time event streaming with ClickHouse, Confluent Cloud and ClickPipes


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Real\-time event streaming with ClickHouse, Confluent Cloud and ClickPipes

![Dale McDirmid](/_next/image?url=%2Fuploads%2FDale_Mc_Dirmid_8016f87452.png&w=96&q=75)[Dale McDiarmid](/authors/dale-mcdiarmid)Jul 20, 2023 · 10 minutes read## Introduction [\#](/blog/real-time-event-streaming-with-confluent-cloud-clickhouse-and-clickpipes#introduction)


In a recent post, we explored a real\-time streaming use case using the official ClickHouse Kafka Connector deployed using Confluent Cloud’s custom connector offering. For this, we used an Ethereum blockchain dataset published by Google and made available on a public pub/sub.


In this post, we simplify this architecture using ClickPipes \- a recently released fully managed ingestion service for ClickHouse Cloud. This allows us to reduce our architectural complexity and overcome some of the previous limitations.


## ClickPipes [\#](/blog/real-time-event-streaming-with-confluent-cloud-clickhouse-and-clickpipes#clickpipes)


[ClickPipes](https://clickhouse.com/cloud/clickpipes) is a native ClickHouse Cloud feature that lets users connect to remote Kafka brokers and start ingesting data into their ClickHouse services immediately. This unlocks the full potential of ClickHouse Cloud and enables users to leverage near\-real\-time data for insights and analytics. While currently only Kafka is supported, we plan to expand the list of supported data sources and systems to turn ClickPipes into a fully\-fledged connectivity platform for ClickHouse Cloud. For further details, we recommend our [announcement post](https://clickhouse.com/blog/clickhouse-cloud-clickpipes-for-kafka-managed-ingestion-service).


## The Dataset [\#](/blog/real-time-event-streaming-with-confluent-cloud-clickhouse-and-clickpipes#the-dataset)


We use an Ethereum Cryptocurrency dataset made available by Google in a public project for our test dataset.


No prior experience with crypto is required for reading this blog post, but for those interested, the [Introduction to Ethereum](https://ethereum.org/en/developers/docs/intro-to-ethereum/) provides a useful overview, as well as Google's blog on [how this dataset](https://cloud.google.com/blog/products/data-analytics/ethereum-bigquery-how-we-built-dataset) was constructed.


As a quick reminder, our dataset consists of 4 tables. This is a subset of the full data but is sufficient for most common questions:


- **Blocks** \- Blocks are batches of transactions with a hash of the previous block in the chain. Approximately 17 million rows with a growth rate of 7k per day.
- **Transactions** \- Transactions are cryptographically signed instructions from accounts. An account will initiate a transaction to update the state of the Ethereum network, e.g., transferring ETH from one account to another. Over 2 billion with around 1 million additions per day.
- **Traces** \- Internal transactions that allow querying all Ethereum addresses with their balances. Over 7 billion with 5 million additions per day.
- **Contracts** \- A "smart contract" is simply a program that runs on the Ethereum blockchain. Over 60 million with around 50k additions per day.


## Architectural evolution [\#](/blog/real-time-event-streaming-with-confluent-cloud-clickhouse-and-clickpipes#architectural-evolution)


In an earlier blog post, we explored this dataset in detail, comparing [BigQuery to ClickHouse](https://clickhouse.com/blog/clickhouse-bigquery-migrating-data-for-realtime-queries), where we proposed a batch\-based approach to keep this dataset up\-to\-date in ClickHouse. This was achieved by [periodically exporting data](https://clickhouse.com/blog/clickhouse-bigquery-migrating-data-for-realtime-queries#scheduling-data-export) from the public BigQuery table (via a scheduled query) to GCS and [importing this into ClickHouse](https://clickhouse.com/blog/clickhouse-bigquery-migrating-data-for-realtime-queries#scheduling-data-import) via a simple scheduled cron job.


![Scheduled Export.png](/uploads/Scheduled_Export_27ac957720.png)
While this was sufficient for our needs at the time and used to keep our public [sql.clickhouse.com](https://crypto.clickhouse.com?query=U0hPVyBUYWJsZXMgZnJvbSBldGhlcmV1bQ&) environment up\-to\-date for our crypto enthusiast users, it introduced an unsatisfactory delay (around 30 mins) between the data being available on the blockchain and BigQuery and it being queryable in ClickHouse.


Fortunately, Google also made this dataset available in several [public Pub/Sub topics](https://medium.com/google-cloud/live-ethereum-and-bitcoin-data-in-google-bigquery-and-pub-sub-765b71cd57b5), providing a stream of the events that can be consumed. With a delay of only 4 minutes from the Ethereum blockchain, this source would allow us to offer a comparable service to BigQuery.


Needing a robust pipeline to connect these public Pub/Sub topics to ClickHouse, and wanting to minimize the initial work and any future maintenance overhead, a cloud\-hosted approach using our Kafka Connect connector seemed the ideal solution with Confluent hosting the infrastructure. As well as reducing the latency before the data is available in ClickHouse, Kafka would allow us to buffer up to N day's worth of data and provide us with a replay capability if required.


To achieve this architecture, we also needed a reliable means of sending messages from Pub/Sub to Kafka. Confluent provided a source connector for this purpose, which is also deployable with zero code. Combining these connectors produces the following simple architecture:


![Pub Sub Export(1).png](/uploads/Pub_Sub_Export_1_579ea9c537.png)
For further details on implementing this architecture, see our [previous blog post](https://clickhouse.com/blog/real-time-event-streaming-with-kafka-connect-confluent-cloud-clickhouse).


While this architecture was sufficient for our needs, it does require the user to use Confluent Cloud for all components. While this is not an issue for our specific problem, for users using self\-managed Kafka or MSK with ClickHouse Cloud, ClickPipes offers a simpler solution.


Thanks to ClickPipes, we can simplify this architecture even further. Rather than deploying the Kafka Connector to send data to ClickHouse Cloud, we can simply pull data from the Kafka topic. This is illustrated below:


![Pub Sub Export simplified(1).png](/uploads/Pub_Sub_Export_simplified_1_671841b680.png)
## Introducing ClickPipes [\#](/blog/real-time-event-streaming-with-confluent-cloud-clickhouse-and-clickpipes#introducing-clickpipes)


Our messages are delivered to our Kafka topics in JSON format by the Pub/Sub Connectors, with one topic per data type. Further details on configuring these can be found [here](https://clickhouse.com/blog/real-time-event-streaming-with-kafka-connect-confluent-cloud-clickhouse#create-a-pubsub-subscription).


### Pipeline Recap [\#](/blog/real-time-event-streaming-with-confluent-cloud-clickhouse-and-clickpipes#pipeline-recap)


For our new architecture, we create one ClickPipe per Kafka topic sending the data to the same receiving tables as before. As a reminder, these assume the data is delivered in a column `MessageData` as a JSON string. For example, for the Blocks data:



```
CREATE TABLE default.block_messages
(
  `MessageData` String,
  `AttributesMap` Map(String, String)
)
ENGINE = MergeTree
ORDER BY tuple()

SELECT *
FROM default.block_messages
LIMIT 1
FORMAT PrettyJSONEachRow

```


```
{
    "MessageData": "{\"type\": \"block\", \"number\": 17635706, \"hash\": \"0x44886d4a33deea1b76564ac6068357ee7e167a4e2b625d47e0bd048e7592bdee\", \"parent_hash\": \"0xbabfb51d4d645081c6fb28eccebf27543de094e4bb8e31d1b884a72a0a948f9b\", \"nonce\": \"0x0000000000000000\", \"sha3_uncles\": \"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347\", \"logs_bloom\": \"0x3061030f6188c36a303ebbb18652922694812ca9ee4b60cd10d996afc69c6c6fca611f8dd95032c057023aaf6488090d4213d28ade017aa623368462192f28f6648ac12d6618d8a9488bc46fc00985a291d600c817686c4202a4ac65956b1e25b8606480873fd9032bdcd5a04a3c1cd5a0c14c5714c0d594390455f2087ab2152f06875646c21da32253c35031024227e319a7a3998080a8c424737fd097c06ebed1837b61a8a6725a190ac099a56e0215564c1876ea669bb96a8874228c2a34cb5e340ff9a896ce002a8e47983c12c680e1132a97e954112860b71388c6ac40c9ff369205b292680a6674f47334140906ab1a0ad9488e5620397883a3ac74a5\", \"transactions_root\": \"0xe61ff16a082b53be8893e64224b0840de8f4ba246b7f2e1021227496750ce37d\", \"state_root\": \"0xdcb4abc3f10a51bb1691f5aa6b94d841360d454e44c848e04040e00d492c7a93\", \"receipts_root\": \"0x6376166e9180aa437e67b27c7119ceef073a99bcdbbbca00e5322c92661d7f4f\", \"miner\": \"0x4675c7e5baafbffbca748158becba61ef3b0a263\", \"difficulty\": 0, \"total_difficulty\": 58750003716598352816469, \"size\": 84025, \"extra_data\": \"0x6265617665726275696c642e6f7267\", \"gas_limit\": 30000000, \"gas_used\": 14672410, \"timestamp\": 1688657471, \"transaction_count\": 168, \"base_fee_per_gas\": 36613178634, \"withdrawals_root\": \"0xf213df7058a0ee7055c61c1703db0d27cfbec98a930ec0b46ae60f228aec3f16\", \"withdrawals\": [{\"index\": 9612515, \"validator_index\": 147393, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14340397}, {\"index\": 9612516, \"validator_index\": 147394, \"address\": \"0xbf85eb89b26f48aed0b4c28cf1281381e72bdec1\", \"amount\": 14348823}, {\"index\": 9612517, \"validator_index\": 147395, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14370108}, {\"index\": 9612518, \"validator_index\": 147396, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14389895}, {\"index\": 9612519, \"validator_index\": 147397, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14290983}, {\"index\": 9612520, \"validator_index\": 147398, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14378411}, {\"index\": 9612521, \"validator_index\": 147399, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14297547}, {\"index\": 9612522, \"validator_index\": 147400, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14272411}, {\"index\": 9612523, \"validator_index\": 147401, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 50164441}, {\"index\": 9612524, \"validator_index\": 147402, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14340502}, {\"index\": 9612525, \"validator_index\": 147403, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14330852}, {\"index\": 9612526, \"validator_index\": 147404, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14398952}, {\"index\": 9612527, \"validator_index\": 147405, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14297302}, {\"index\": 9612528, \"validator_index\": 147406, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14292279}, {\"index\": 9612529, \"validator_index\": 147407, \"address\": \"0xbf85eb89b26f48aed0b4c28cf1281381e72bdec1\", \"amount\": 14275314}, {\"index\": 9612530, \"validator_index\": 147409, \"address\": \"0x5363aedb6dcd082c77642d5bf663eabe916031f7\", \"amount\": 14297649}], \"item_id\": \"block_0x44886d4a33deea1b76564ac6068357ee7e167a4e2b625d47e0bd048e7592bdee\", \"item_timestamp\": \"2023-07-06T15:31:11Z\"}",
    "AttributesMap": {
        "item_id": "block_0x44886d4a33deea1b76564ac6068357ee7e167a4e2b625d47e0bd048e7592bdee",
        "item_timestamp": "2023-07-06T15:31:11Z"
    }
}

```

To extract this data to our final table, we use a materialized view that exploits the [JSONExtract family of functions](https://clickhouse.com/docs/en/sql-reference/functions/json-functions).



```
CREATE TABLE blocks
(
  `number` UInt32 CODEC(Delta(4), ZSTD(1)),
  `hash` String,
  `parent_hash` String,
  `nonce` String,
  `sha3_uncles` String,
  `logs_bloom` String,
  `transactions_root` String,
  `state_root` String,
  `receipts_root` String,
  `miner` String,
  `difficulty` Decimal(38, 0),
  `total_difficulty` Decimal(38, 0),
  `size` UInt32 CODEC(Delta(4), ZSTD(1)),
  `extra_data` String,
  `gas_limit` UInt32 CODEC(Delta(4), ZSTD(1)),
  `gas_used` UInt32 CODEC(Delta(4), ZSTD(1)),
  `timestamp` DateTime CODEC(Delta(4), ZSTD(1)),
  `transaction_count` UInt16,
  `base_fee_per_gas` UInt64,
  `withdrawals_root` String,
  `withdrawals.index` Array(UInt64),
  `withdrawals.validator_index` Array(Int64),
  `withdrawals.address` Array(String),
  `withdrawals.amount` Array(UInt64)
)
ENGINE = MergeTree
ORDER BY timestamp

```

This view executes on rows as they are inserted into the table `block_messages`, transforming the data and inserting the results into a final `blocks` table. Our target blocks table schema:



```
CREATE TABLE blocks
(
  `number` UInt32 CODEC(Delta(4), ZSTD(1)),
  `hash` String,
  `parent_hash` String,
  `nonce` String,
  `sha3_uncles` String,
  `logs_bloom` String,
  `transactions_root` String,
  `state_root` String,
  `receipts_root` String,
  `miner` String,
  `difficulty` Decimal(38, 0),
  `total_difficulty` Decimal(38, 0),
  `size` UInt32 CODEC(Delta(4), ZSTD(1)),
  `extra_data` String,
  `gas_limit` UInt32 CODEC(Delta(4), ZSTD(1)),
  `gas_used` UInt32 CODEC(Delta(4), ZSTD(1)),
  `timestamp` DateTime CODEC(Delta(4), ZSTD(1)),
  `transaction_count` UInt16,
  `base_fee_per_gas` UInt64,
  `withdrawals_root` String,
  `withdrawals.index` Array(UInt64),
  `withdrawals.validator_index` Array(Int64),
  `withdrawals.address` Array(String),
  `withdrawals.amount` Array(UInt64)
)
ENGINE = MergeTree
ORDER BY timestamp

```

This same process is used for our data types, traces, transactions and contracts.


![mv_flow.png](/uploads/mv_flow_044b62d925.png)
### Configuring ClickPipes [\#](/blog/real-time-event-streaming-with-confluent-cloud-clickhouse-and-clickpipes#configuring-clickpipes)


Configuring ClickPipes is simple. First, we need to obtain an API key and endpoint from our Confluent Cluster. Note how we record the bootstrap server address below.


[![](/uploads/clickpipes_confluent_details_ffd8b7bafe.gif)](/uploads/clickpipes_confluent_details_ffd8b7bafe.gif)


We can now create a ClickPipe from the Cloud Console with these credentials and endpoints recorded. Below we create a ClickPipe for the blocks dataset, consuming messages from the `block_messages` Kafka topic in Confluent Cloud for insertion into the table of the same name. Note the following tips when selecting Confluent Cloud as the source, which we hope to refine in future iterations:


- Use the API key and secret as the Login and Password
- Ensure the Consumer Group is set to a unique string. In future versions, we may pre\-populate this setting.
- Use the bootstrap endpoint copied earlier as the Server address.


[![](/uploads/clickpipes_ethereum_a4a4c9a962.gif)](/uploads/clickpipes_ethereum_a4a4c9a962.gif)


As shown, we map the Kafka topic to the existing table \- the latter has been pre\-created in our case. Users can also create a new table if desired, mapping the message fields to columns of a different name if required.


## Conclusion [\#](/blog/real-time-event-streaming-with-confluent-cloud-clickhouse-and-clickpipes#conclusion)


In this blog post, we have demonstrated the new ClickHouse Cloud capability ClickPipes, and how this can be used to simplify a streaming architecture presented in a previous blog post. ClickPipes is a native capability of ClickHouse Cloud currently under private preview. Users interested in trying ClickPipes can join our [waitlist here](https://clickhouse.com/cloud/clickpipes#joinwaitlist).


You can follow the instructions [in the docs](https://clickhouse.com/docs/en/integrations/clickpipes) to create your first ClickPipes. More details are available in:


- [ClickPipes website](https://clickhouse.com/cloud/clickpipes)
- [Video demonstration](https://www.youtube.com/watch?v=rSUHqyqdRuk)
- [Documentation](https://clickhouse.com/docs/en/integrations/clickpipes)
- [Announcement blog](https://clickhouse.com/blog/clickhouse-cloud-clickpipes-for-kafka-managed-ingestion-service)
[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
